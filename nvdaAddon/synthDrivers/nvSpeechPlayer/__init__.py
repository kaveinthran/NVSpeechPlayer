###
#This file is a part of the NV Speech Player project. 
#URL: https://bitbucket.org/nvaccess/speechplayer
#Copyright 2014 NV Access Limited.
#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License version 2.0, as published by
#the Free Software Foundation.
#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#This license can be found at:
#http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
###

# Advanced NVDA compatibility improvements inspired by tgeczy/TGSpeechBox
# Original implementation: https://github.com/tgeczy/TGSpeechBox/commit/e6f76ff0efb7d3d46b09f9c413f6a015d69f3ed5
# Credits: @tgeczy for background worker pattern, explicit ctypes prototypes, and timing fixes

import re
import threading
import math
from collections import OrderedDict
import ctypes
import weakref
import queue
from . import speechPlayer
from . import ipa
import config
import nvwave
import speech
from logHandler import log
from synthDrivers import _espeak
from synthDriverHandler import SynthDriver, VoiceInfo, synthIndexReached, synthDoneSpeaking

# Try modern import first, fall back to old path for backward compatibility
try:
	from autoSettingsUtils.driverSetting import NumericDriverSetting, BooleanDriverSetting
except ImportError:
	from driverHandler import NumericDriverSetting, BooleanDriverSetting

# Import speech commands with backward compatibility for different NVDA versions
try:
	from speech.commands import IndexCommand, PitchCommand
except ImportError:
	try:
		from speech import IndexCommand, PitchCommand
	except ImportError:
		# Fallback for very old NVDA versions
		IndexCommand = None
		PitchCommand = None

# Import AudioPurpose if available (NVDA 2024.x+)
try:
	from nvwave import AudioPurpose
	HAS_AUDIO_PURPOSE = True
except ImportError:
	HAS_AUDIO_PURPOSE = False


class _BgThread(threading.Thread):
	def __init__(self, q, stopEvent):
		super().__init__(name=f"{self.__class__.__module__}.{self.__class__.__qualname__}")
		self.daemon = True
		self._q = q
		self._stop = stopEvent
	
	def run(self):
		while not self._stop.is_set():
			try:
				item = self._q.get(timeout=0.2)
			except queue.Empty:
				continue
			try:
				if item is None:
					return
				func, args, kwargs = item
				func(*args, **kwargs)
			except Exception:
				log.error("nvSpeechPlayer: error in background thread", exc_info=True)
			finally:
				try:
					self._q.task_done()
				except Exception:
					pass


class AudioThread(threading.Thread):

	_wavePlayer=None
	_keepAlive=True
	_isSpeaking=False
	_synthEvent=None
	_initializeEvent=None

	def __init__(self,synth, speechPlayerObj,sampleRate):
		self._synthRef=weakref.ref(synth)
		self._speechPlayer=speechPlayerObj
		self._sampleRate=sampleRate
		self._initializeEvent=threading.Event()
		super(AudioThread,self).__init__()
		self.start()
		self._initializeEvent.wait()

	def terminate(self):
		self._initializeEvent.clear()
		self._keepAlive=False
		self._isSpeaking=False
		self._synthEvent.set()
		self._initializeEvent.wait()

	def run(self):
		try:
			# Get output device from config (try modern path first)
			try:
				outputDevice = config.conf["audio"]["outputDevice"]
			except KeyError:
				outputDevice = config.conf["speech"]["outputDevice"]

			# Create WavePlayer with version-appropriate signature
			if HAS_AUDIO_PURPOSE:
				self._wavePlayer = nvwave.WavePlayer(
					channels=1,
					samplesPerSec=self._sampleRate,
					bitsPerSample=16,
					outputDevice=outputDevice,
					wantDucking=True,
					purpose=AudioPurpose.SPEECH
				)
			else:
				# Fallback for older NVDA (2019.3-2023.x)
				self._wavePlayer = nvwave.WavePlayer(
					channels=1,
					samplesPerSec=self._sampleRate,
					bitsPerSample=16,
					outputDevice=outputDevice
				)
			self._synthEvent=threading.Event()
		finally:
			self._initializeEvent.set()
		while self._keepAlive:
			self._synthEvent.wait()
			self._synthEvent.clear()
			lastIndex=None
			while self._keepAlive:
				data=self._speechPlayer.synthesize(8192)
				if self._isSpeaking and data:
					indexNum=self._speechPlayer.getLastIndex()
					self._wavePlayer.feed(
						ctypes.string_at(data,data.length*2),
						onDone=lambda indexNum=indexNum: synthIndexReached.notify(synth=self._synthRef(),index=indexNum) if indexNum>=0 else False
					)
					lastIndex=indexNum
				else:
					indexNum=self._speechPlayer.getLastIndex()
					if indexNum>0 and indexNum!=lastIndex:
						synthIndexReached.notify(synth=self._synthRef(),index=indexNum)
					# Fix synthDoneSpeaking timing - notify AFTER audio playback completes
					if self._keepAlive and self._wavePlayer:
						s = self._synthRef()
						if s:
							def doneCb(synth=s):
								synthDoneSpeaking.notify(synth=synth)
							# Feed 0-byte buffer with callback to trigger after playback drains
							try:
								self._wavePlayer.feed(b"", len(0), onDone=doneCb)
							except TypeError:
								# Fallback for older NVDA
								self._wavePlayer.feed(b"", onDone=doneCb)
						try:
							self._wavePlayer.idle()
						except Exception:
							pass
					break
		self._initializeEvent.set()

re_textPause=re.compile(r"(?<=[.?!,:;])\s",re.DOTALL|re.UNICODE)

voices={
	'Adam':{
		'cb1_mul':1.3,
		'pa6_mul':1.3,
		'fricationAmplitude_mul':0.85,
	},
		'Benjamin':{
		'cf1_mul':1.01,
		'cf2_mul':1.02,
		#'cf3_mul':0.96,
		'cf4':3770,
		'cf5':4100,
		'cf6':5000,
		'cfNP_mul':0.9,
		'cb1_mul':1.3,
		'fricationAmplitude_mul':0.7,
		'pa6_mul':1.3,
	},
	'Caleb ':{
		'aspirationAmplitude':1,
		'voiceAmplitude':0,
	},
	'David':{
		'voicePitch_mul':0.75,
		'endVoicePitch_mul':0.75,
		'cf1_mul':0.75,
		'cf2_mul':0.85,
		'cf3_mul':0.85,
	},
}

def applyVoiceToFrame(frame,voiceName):
	v=voices[voiceName]
	for paramName in (x[0] for x in frame._fields_):
		absVal=v.get(paramName)
		if absVal is not None:
			setattr(frame,paramName,absVal)
		mulVal=v.get('%s_mul'%paramName)
		if mulVal is not None:
			setattr(frame,paramName,getattr(frame,paramName)*mulVal)

class SynthDriver(SynthDriver):

	exposeExtraParams=True

	def __init__(self):
		if self.exposeExtraParams:
			self._extraParamNames=[x[0] for x in speechPlayer.Frame._fields_]
			self.supportedSettings=SynthDriver.supportedSettings+tuple(NumericDriverSetting("speechPlayer_%s"%x,"frame.%s"%x,normalStep=1) for x in self._extraParamNames)
			for x in self._extraParamNames:
				setattr(self,"speechPlayer_%s"%x,50)
		self.player=speechPlayer.SpeechPlayer(16000)
		_espeak.initialize()
		_espeak.espeakDLL.espeak_TextToPhonemes.restype = ctypes.c_void_p
		_espeak.setVoiceByLanguage('en')
		self.pitch=50
		self.rate=50
		self.volume=90
		self.inflection=65
		self.intonationMode=False
		
		# Initialize background worker thread
		self._bgQueue = queue.Queue()
		self._bgStop = threading.Event()
		self._bgThread = _BgThread(self._bgQueue, self._bgStop)
		self._bgThread.start()
		
		self.audioThread=AudioThread(self,self.player,16000)

	@classmethod
	def check(cls):
		return True

	name="nvSpeechPlayer"
	description="nvSpeechPlayer"

	supportedSettings=(
		SynthDriver.VoiceSetting(),
		SynthDriver.RateSetting(),
		SynthDriver.PitchSetting(),
		SynthDriver.VolumeSetting(),
		SynthDriver.InflectionSetting(),
		BooleanDriverSetting("intonationMode", "Intonation: NVeloq (Eloquence-style)", defaultVal=False, availableInSettingsRing=True)
	)

	supportedCommands = {
		IndexCommand,
		PitchCommand,
	}

	supportedNotifications = {synthIndexReached,synthDoneSpeaking}

	_curPitch=50
	_curVoice='Adam'
	_curInflection=0.5
	_curVolume=1.0
	_curRate=1.0
	_intonationMode=False  # False=nvEspeak (post-2014), True=NVeloq (pre-2014)

	def speak(self,speakList):
		userIndex=None
		pitchOffset=0
		# Merge adjacent strings
		index=0
		while index<len(speakList):
			item=speakList[index]
			if index>0:
				lastItem=speakList[index-1]
				if isinstance(item,str) and isinstance(lastItem,str):
					speakList[index-1]=" ".join([lastItem,item])
					del speakList[index]
					continue
			index+=1
		endPause=20
		for item in speakList:
			if isinstance(item, PitchCommand):
				pitchOffset=item.offset
			elif isinstance(item, IndexCommand):
				userIndex=item.index
			elif isinstance(item,str):
				textList=re_textPause.split(item)
				lastIndex=len(textList)-1
				for index,chunk in enumerate(textList):
					if not chunk: continue
					chunk=chunk.strip()
					if not chunk: continue
					clauseType=chunk[-1]
					if clauseType in ('.','!'):
						endPause=150
					elif clauseType=='?':
						endPause=150
					elif clauseType==',':
						endPause=120
					else:
						endPause=100
						clauseType=None
					endPause/=self._curRate
					textBuf=ctypes.create_unicode_buffer(chunk)
					textPtr=ctypes.c_void_p(ctypes.addressof(textBuf))
					chunks=[]
					while textPtr:
						phonemeBuf=_espeak.espeakDLL.espeak_TextToPhonemes(ctypes.byref(textPtr),_espeak.espeakCHARS_WCHAR,0x36100+0x82)
						if not phonemeBuf: continue
						chunks.append(ctypes.string_at(phonemeBuf))
					chunk=b"".join(chunks).decode('utf8') 
					chunk=chunk.replace('ə͡l','ʊ͡l')
					chunk=chunk.replace('a͡ɪ','ɑ͡ɪ')
					chunk=chunk.replace('e͡ɪ','e͡i')
					chunk=chunk.replace('ə͡ʊ','o͡u')
					chunk=chunk.strip()
					if not chunk: continue
					pitch=self._curPitch+pitchOffset
					basePitch=25+(21.25*(pitch/12.5))
					# Select mode: False=nvEspeak (post-2014), True=NVeloq (pre-2014)
					mode = 'eloquence' if self._intonationMode else 'espeak'
					for args in ipa.generateFramesAndTiming(chunk,speed=self._curRate,basePitch=basePitch,inflection=self._curInflection,clauseType=clauseType,mode=mode):
						frame=args[0]
						if frame:
							applyVoiceToFrame(frame,self._curVoice)
							if self.exposeExtraParams:
								for x in self._extraParamNames:
									ratio=getattr(self,"speechPlayer_%s"%x)/50.0
									setattr(frame,x,getattr(frame,x)*ratio)
							frame.preFormantGain*=self._curVolume
						self.player.queueFrame(*args,userIndex=userIndex)
						userIndex=None
		self.player.queueFrame(None,endPause,max(10.0,10.0/self._curRate),userIndex=userIndex)
		self.audioThread._isSpeaking=True
		self.audioThread._synthEvent.set()

	def cancel(self):
		self.player.queueFrame(None,20,5,purgeQueue=True)
		self.audioThread._isSpeaking=False
		self.audioThread._synthEvent.set()
		self.audioThread._wavePlayer.stop()

	def pause(self,switch):
		self.audioThread._wavePlayer.pause(switch)

	def _enqueue(self, func, *args, **kwargs):
		if self._bgStop.is_set():
			return
		self._bgQueue.put((func, args, kwargs))

	def _get_rate(self):
		return int(math.log(self._curRate/0.25,2)*25.0)

	def _set_rate(self,val):
		self._curRate=0.25*(2**(val/25.0))

	def _get_pitch(self):
		return self._curPitch

	def _set_pitch(self,val):
		self._curPitch=val

	def _get_volume(self):
		return int(self._curVolume*75)

	def _set_volume(self,val):
		self._curVolume=val/75.0

	def _get_inflection(self):
		return int(self._curInflection/0.01)

	def _set_inflection(self,val):
		self._curInflection=val*0.01

	def _get_voice(self):
		return self._curVoice

	def _set_voice(self,voice):
		if voice not in self.availableVoices:
			voice='Adam'
		self._curVoice=voice
		if self.exposeExtraParams:
			for paramName in self._extraParamNames:
				setattr(self,"speechPlayer_%s"%paramName,50)

	def _get_intonationMode(self):
		return self._intonationMode

	def _set_intonationMode(self,val):
		self._intonationMode=val

	def _getAvailableVoices(self):
		d=OrderedDict()
		for name in sorted(voices):
			d[name]=VoiceInfo(name,name)
		return d

	def terminate(self):
		try:
			self.cancel()
		except Exception:
			pass
		
		# Clean up background thread
		try:
			self._bgStop.set()
			try:
				self._bgQueue.put(None)
			except Exception:
				pass
			try:
				self._bgThread.join(timeout=2.0)
			except Exception:
				pass
		except Exception:
			pass
		
		# Clean up audio thread and resources
		self.audioThread.terminate()
		del self.player
		_espeak.terminate()
