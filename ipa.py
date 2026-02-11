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

import os
import codecs
from . import speechPlayer

dataPath=os.path.join(os.path.dirname(__file__),'data.py')

data=eval(codecs.open(dataPath,'r','utf8').read(),None,None)

def iterPhonemes(**kwargs):
	for k,v in data.items():
		if all(v[x]==y for x,y in kwargs.items()):
			yield k

def setFrame(frame,phoneme):
	values=data[phoneme]
	for k,v in values.items():
		setattr(frame,k,v)

def applyPhonemeToFrame(frame,phoneme):
	for k,v in phoneme.items():
		if not k.startswith('_'):
			setattr(frame,k,v)

def _IPAToPhonemesHelper(text):
	textLen=len(text)
	index=0
	offset=0
	curStress=0
	for index in range(textLen):
		index=index+offset
		if index>=textLen:
			break
		char=text[index]
		if char=='ˈ':
			curStress=1
			continue
		elif char=='ˌ':
			curStress=2
			continue
		isLengthened=(text[index+1:index+2]=='ː')
		isTiedTo=(text[index+1:index+2]=='͡')
		isTiedFrom=(text[index-1:index]=='͡') if index>0 else False
		phoneme=None
		if isTiedTo:
			phoneme=data.get(text[index:index+3])
			offset+=2 if phoneme else 1
		elif isLengthened:
			phoneme=data.get(text[index:index+2])
			offset+=1
		if not phoneme:
			phoneme=data.get(char)
		if not phoneme:
			yield char,None
			continue
		phoneme=phoneme.copy()
		if curStress:
			phoneme['_stress']=curStress
			curStress=0
		if isTiedFrom:
			phoneme['_tiedFrom']=True
		elif isTiedTo:
			phoneme['_tiedTo']=True
		if isLengthened:
			phoneme['_lengthened']=True
		phoneme['_char']=char
		yield char,phoneme

def IPAToPhonemes(ipaText):
	phonemeList=[]
	textLength=len(ipaText)
	# Collect phoneme info for each IPA character, assigning diacritics (lengthened, stress) to the last real phoneme
	newWord=True
	lastPhoneme=None
	syllableStartPhoneme=None
	for char,phoneme in _IPAToPhonemesHelper(ipaText):
		if char==' ':
			newWord=True
		elif phoneme:
			stress=phoneme.pop('_stress',0)
			if lastPhoneme and not lastPhoneme.get('_isVowel') and phoneme and phoneme.get('_isVowel'):
				lastPhoneme['_syllableStart']=True
				syllableStartPhoneme=lastPhoneme
			elif stress==1 and lastPhoneme and lastPhoneme.get('_isVowel'):
				phoneme['_syllableStart']=True
				syllableStartPhoneme=phoneme
			if lastPhoneme and lastPhoneme.get('_isStop') and not lastPhoneme.get('_isVoiced') and phoneme and phoneme.get('_isVoiced') and not phoneme.get('_isStop') and not phoneme.get('_isAfricate'): 
				psa=data['h'].copy()
				psa['_postStopAspiration']=True
				psa['_char']=None
				phonemeList.append(psa)
				lastPhoneme=psa
			if newWord:
				newWord=False
				phoneme['_wordStart']=True
				phoneme['_syllableStart']=True
				syllableStartPhoneme=phoneme
			if stress:
				syllableStartPhoneme['_stress']=stress
			elif phoneme.get('_isStop') or phoneme.get('_isAfricate'):
				gap=dict(_silence=True,_preStopGap=True)
				phonemeList.append(gap)
			phonemeList.append(phoneme)
			lastPhoneme=phoneme
	return phonemeList

def correctHPhonemes(phonemeList):
	finalPhonemeIndex=len(phonemeList)-1
	# Correct all h phonemes (including inserted aspirations) so that their formants match the next phoneme, or the previous if there is no next
	for index in range(len(phonemeList)):
		prevPhoneme=phonemeList[index-1] if index>0 else None
		curPhoneme=phonemeList[index]
		nextPhoneme=phonemeList[index+1] if index<finalPhonemeIndex else None
		if curPhoneme.get('_copyAdjacent'):
			adjacent=nextPhoneme if nextPhoneme and not nextPhoneme.get('_silence') else prevPhoneme 
			if adjacent:
				for k,v in adjacent.items():
					if not k.startswith('_') and k not in curPhoneme:
						curPhoneme[k]=v

def calculatePhonemeTimes(phonemeList,baseSpeed):
	lastPhoneme=None
	syllableStress=0
	speed=baseSpeed
	for index,phoneme in enumerate(phonemeList):
		nextPhoneme=phonemeList[index+1] if len(phonemeList)>index+1 else None
		syllableStart=phoneme.get('_syllableStart')
		if syllableStart:
			syllableStress=phoneme.get('_stress')
			if syllableStress:
				speed=baseSpeed/1.5 if syllableStress==1 else baseSpeed/1.2
			else:
				speed=baseSpeed
		phonemeDuration=60.0/speed
		phonemeFadeDuration=10.0/speed
		if phoneme.get('_preStopGap'):
			phonemeDuration=41.0/speed
		elif phoneme.get('_postStopAspiration'):
			phonemeDuration=20.0/speed
		elif phoneme.get('_isStop'):
			phonemeDuration=min(10.0/speed,10.0)
			phonemeFadeDuration=0.001
		elif phoneme.get('_isAfricate'):
			phonemeDuration=24.0/speed
			phonemeFadeDuration=0.001
		elif not phoneme.get('_isVoiced'):
			phonemeDuration=45.0/speed
		else: # is voiced
			if phoneme.get('_isVowel'):
				if lastPhoneme and (lastPhoneme.get('_isLiquid') or lastPhoneme.get('_isSemivowel')): 
					phonemeFadeDuration=25.0/speed
				if phoneme.get('_tiedTo'):
					phonemeDuration=40.0/speed
				elif phoneme.get('_tiedFrom'):
					phonemeDuration=20.0/speed
					phonemeFadeDuration=20.0/speed
				elif not syllableStress and not syllableStart and nextPhoneme and not nextPhoneme.get('_wordStart') and (nextPhoneme.get('_isLiquid') or nextPhoneme.get('_isNasal')):
					if nextPhoneme.get('_isLiquid'):
						phonemeDuration=30.0/speed
					else:
						phonemeDuration=40.0/speed
			else: # not a vowel
				phonemeDuration=30.0/speed
				if phoneme.get('_isLiquid') or phoneme.get('_isSemivowel'):
					phonemeFadeDuration=20.0/speed
		if phoneme.get('_lengthened'):
			phonemeDuration*=1.05
		phoneme['_duration']=phonemeDuration
		phoneme['_fadeDuration']=phonemeFadeDuration
		lastPhoneme=phoneme

def calculatePhonemePitches(phonemeList,speed,basePitch,inflection,clauseType):
	totalVoicedDuration=0
	finalInflectionStartTime=0
	needsSetFinalInflectionStartTime=False
	finalVoicedIndex=0
	lastPhoneme=None
	for index,phoneme in enumerate(phonemeList):
		if phoneme.get('_wordStart'):
			needsSetFinalInflectionStartTime=True
		if phoneme.get('_isVoiced'):
			finalVoicedIndex=index
			if needsSetFinalInflectionStartTime:
				finalInflectionStartTime=totalVoicedDuration
				needsSetFinalInflectionStartTime=False
		if phoneme.get('_isVoiced'):
			totalVoicedDuration+=phoneme['_duration']
		elif lastPhoneme and lastPhoneme.get('_isVoiced'):
			totalVoicedDuration+=lastPhoneme['_fadeDuration']
		lastPhoneme=phoneme
	durationCounter=0
	curBasePitch=basePitch
	lastEndVoicePitch=basePitch
	stressInflection=inflection/1.5
	lastPhoneme=None
	syllableStress=False
	firstStress=True
	for index,phoneme in enumerate(phonemeList):
		if phoneme.get('_syllableStart'):
			syllableStress=phoneme.get('_stress')==1
		voicePitch=lastEndVoicePitch
		inFinalInflection=durationCounter>=finalInflectionStartTime
		if phoneme.get('_isVoiced'):
			durationCounter+=phoneme['_duration']
		elif lastPhoneme and lastPhoneme.get('_isVoiced'):
			durationCounter+=lastPhoneme['_fadeDuration']
		oldBasePitch=curBasePitch
		if not inFinalInflection:
			curBasePitch=basePitch/(1+(inflection/25000.0)*durationCounter*speed)
		else:
			ratio=float(durationCounter-finalInflectionStartTime)/float(totalVoicedDuration-finalInflectionStartTime)
			if clauseType=='.':
				ratio/=1.5
			elif clauseType=='?':
				ratio=0.5-(ratio/1.2)
			elif clauseType==',':
				ratio/=8
			else:
				ratio=ratio/1.75
			curBasePitch=basePitch/(1+(inflection*ratio*1.5))
		endVoicePitch=curBasePitch
		if syllableStress and phoneme.get('_isVowel'):
			if firstStress:
				voicePitch=oldBasePitch*(1+stressInflection/3)
				endVoicePitch=curBasePitch*(1+stressInflection)
				firstStress=False
			elif index<finalVoicedIndex:
				voicePitch=oldBasePitch*(1+stressInflection/3)
				endVoicePitch=oldBasePitch*(1+stressInflection)
			else:
				voicePitch=basePitch*(1+stressInflection)
			stressInflection*=0.9
			stressInflection=max(stressInflection,inflection/2)
			syllableStress=False
		if lastPhoneme:
			lastPhoneme['endVoicePitch']=voicePitch
		phoneme['voicePitch']=voicePitch
		lastEndVoicePitch=phoneme['endVoicePitch']=endVoicePitch
		lastPhoneme=phoneme

def generateFramesAndTiming(ipaText,speed=1,basePitch=100,inflection=0.5,clauseType=None):
	phonemeList=IPAToPhonemes(ipaText)
	if len(phonemeList)==0:
		return
	correctHPhonemes(phonemeList)
	calculatePhonemeTimes(phonemeList,speed)
	calculatePhonemePitches(phonemeList,speed,basePitch,inflection,clauseType)
	for phoneme in phonemeList:
		frameDuration=phoneme.pop('_duration')
		fadeDuration=phoneme.pop('_fadeDuration')
		if phoneme.get('_silence'):
			yield None,frameDuration,fadeDuration
		else:
			frame=speechPlayer.Frame()
			frame.preFormantGain=1.0
			frame.outputGain=2.0
			applyPhonemeToFrame(frame,phoneme)
			yield frame,frameDuration,fadeDuration
