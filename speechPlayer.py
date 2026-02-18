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

from ctypes import (
	Structure,
	POINTER,
	byref,
	c_double,
	c_int,
	c_short,
	c_uint,
	c_void_p,
	cdll,
)
import os
import sys

speechPlayer_frameParam_t=c_double

class Frame(Structure):
	_fields_=[(name,speechPlayer_frameParam_t) for name in [
		'voicePitch',
		'vibratoPitchOffset',
		'vibratoSpeed',
		'voiceTurbulenceAmplitude',
		'glottalOpenQuotient',
		'voiceAmplitude',
		'aspirationAmplitude',
		'cf1','cf2','cf3','cf4','cf5','cf6','cfN0','cfNP',
		'cb1','cb2','cb3','cb4','cb5','cb6','cbN0','cbNP',
		'caNP',
		'fricationAmplitude',
		'pf1','pf2','pf3','pf4','pf5','pf6',
		'pb1','pb2','pb3','pb4','pb5','pb6',
		'pa1','pa2','pa3','pa4','pa5','pa6',
		'parallelBypass',
		'preFormantGain',
		'outputGain',
		'endVoicePitch',
	]]

_dllDir = os.path.dirname(__file__)
if sys.maxsize > 2**32:
    dllPath = os.path.join(_dllDir, 'speechPlayer_x64.dll')
else:
    dllPath = os.path.join(_dllDir, 'speechPlayer_x86.dll')

class SpeechPlayer(object):

	def _setupPrototypes(self):
		"""Set ctypes function signatures to prevent 64-bit pointer truncation."""
		# void* speechPlayer_initialize(int sampleRate);
		self._dll.speechPlayer_initialize.argtypes = (c_int,)
		self._dll.speechPlayer_initialize.restype = c_void_p
		
		# void speechPlayer_queueFrame(void* handle, Frame* frame, uint minSamples, uint fadeSamples, int userIndex, bool purgeQueue);
		self._dll.speechPlayer_queueFrame.argtypes = (c_void_p, POINTER(Frame), c_uint, c_uint, c_int, c_int)
		self._dll.speechPlayer_queueFrame.restype = None
		
		# int speechPlayer_synthesize(void* handle, uint numSamples, short* out);
		self._dll.speechPlayer_synthesize.argtypes = (c_void_p, c_uint, POINTER(c_short))
		self._dll.speechPlayer_synthesize.restype = c_int
		
		# int speechPlayer_getLastIndex(void* handle);
		self._dll.speechPlayer_getLastIndex.argtypes = (c_void_p,)
		self._dll.speechPlayer_getLastIndex.restype = c_int
		
		# void speechPlayer_terminate(void* handle);
		self._dll.speechPlayer_terminate.argtypes = (c_void_p,)
		self._dll.speechPlayer_terminate.restype = None

	def __init__(self,sampleRate):
		self.sampleRate=int(sampleRate)
		self._dll=cdll.LoadLibrary(dllPath)
		self._setupPrototypes()
		self._speechHandle=self._dll.speechPlayer_initialize(self.sampleRate)
		if not self._speechHandle:
			raise RuntimeError("speechPlayer_initialize failed")

	def queueFrame(self,frame,minFrameDuration,fadeDuration,userIndex=-1,purgeQueue=False):
		frame=byref(frame) if frame else None
		if userIndex is None: userIndex=-1
		self._dll.speechPlayer_queueFrame(self._speechHandle,frame,int(minFrameDuration*(self.sampleRate/1000.0)),int(fadeDuration*(self.sampleRate/1000.0)),int(userIndex),int(purgeQueue))

	def synthesize(self,numSamples):
		buf=(c_short*numSamples)()
		res=self._dll.speechPlayer_synthesize(self._speechHandle,numSamples,buf)
		if res>0:
			buf.length=min(res,len(buf))
			return buf
		else:
			return None

	def getLastIndex(self):
		return self._dll.speechPlayer_getLastIndex(self._speechHandle)

	def __del__(self):
		self._dll.speechPlayer_terminate(self._speechHandle)

class VowelChart(object):

	def __init__(self,fileName):
		self._vowels={}
		with open(fileName,'r') as f:
			for line in f.readlines():
				params=line.split()
				vowel=params.pop(0)
				flag=params.pop(0)
				if flag=='1': continue
				starts=[int(params[x]) for x in range(3)]
				ends=[int(params[x]) for x in range(3,6)]
				self._vowels[vowel]=starts,ends

	def applyVowel(self,frame,vowel,end=False):
		data=self._vowels[vowel][0 if not end else 1]
		frame.cf1=data[0]
		frame.cb1=60
		frame.ca1=1
		frame.cf2=data[1]
		frame.cb2=90
		frame.ca2=1
		frame.cf3=data[2]
		frame.cb3=120
		frame.ca3=1
		frame.ca4=frame.ca5=frame.ca6=frame.caN0=frame.caNP=0
		frame.fricationAmplitude=0
		frame.voiceAmplitude=1
		frame.aspirationAmplitude=0
