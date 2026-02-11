# NV Speech Player
A Klatt-based speech synthesis engine written in c++
Author: NV Access Limited

## Download & Install

**⭐ NEW: Dual Intonation Mode in ONE Add-on! ⭐**

**nvSpeechPlayer** (Recommended) - Switchable dual-mode add-on
- Download: [nvSpeechPlayer_master-bc89128.nvda-addon](nvSpeechPlayer_master-bc89128.nvda-addon)
- **Includes BOTH intonation modes in one add-on:**
  - **nvEspeak mode** (default): Modern eSpeak-style intonation (post-2014)
  - **NVeloq mode**: Classic Eloquence-style intonation (pre-2014)
- **Switch modes on-the-fly** via synth settings without restarting NVDA
- Access via synth settings ring: Navigate to "Intonation: NVeloq (Eloquence-style)" and toggle

**Alternative: Separate Add-ons**

If you prefer separate installations:

1. **nvEspeak only**: Use the main nvSpeechPlayer add-on above (leave mode unchecked)
2. **NVeloq only** (Eloquence-style): [nveloq_master-bc89128.nvda-addon](nveloq_master-bc89128.nvda-addon)

All variants compatible with **NVDA 2019.3 through 2026.1+ (64-bit)**

To install: Download the .nvda-addon file and open it. NVDA will prompt you to install the add-on.

## What's the Difference Between Modes?

The nvSpeechPlayer add-on now includes **BOTH intonation systems** with an easy mode switcher:

### nvEspeak Mode (Post-2014, Default)
- **Table-based intonation**: Uses distinct preHead, head, nucleus, and tail components
- Matches eSpeak's intonation model
- Introduced in commit 646f7f9 (May 2014)
- More varied, expressive pitch patterns
- Timing: 1.4x/1.1x stress speed, 6ms stops

### NVeloq Mode (Pre-2014, Eloquence-style)
- **Smooth mathematical pitch curves**: Based on syllable stress
- Sounds like classic Eloquence synthesizer
- Original system from commit ee80f4d (April 2014)
- Smoother, more predictable intonation
- Timing: 1.5x/1.2x stress speed, 10ms stops

### How to Switch Modes

1. Open NVDA Synth Settings: `NVDA+Ctrl+S`
2. Navigate to **"Intonation: NVeloq (Eloquence-style)"**
3. Check/uncheck to toggle between modes
4. Or use synth settings ring to switch on-the-fly

Both modes use the **same Klatt synthesis engine and phoneme data** - only pitch/intonation and timing differ.

## Recent Updates (2025-2026)

### 🎉 NEW: Dual Intonation Mode Switcher (2026)
- **ONE add-on with BOTH intonation styles** - no need for separate installations!
- **Switch modes on-the-fly** via synth settings without restarting
- Toggle between nvEspeak (post-2014) and NVeloq (pre-2014 Eloquence-style)
- Access via synth settings ring for quick comparison
- Default to nvEspeak, check "Intonation: NVeloq" to enable Eloquence-style

### Compatibility Updates
- **64-bit support**: Rebuilt for NVDA 2026.x 64-bit compatibility
- Fixed NVDA 2021.1+ API compatibility (speech command imports)
- Added backward compatibility for NVDA 2019.3-2024.x
- Fixed WavePlayer initialization for different NVDA versions
- See [COMPATIBILITY.md](COMPATIBILITY.md) for technical details

## Maintenance Note
NV Access is no longer maintaining the original project. This fork provides compatibility updates and preserves both intonation styles for the community.

Note that the eSpeak-ng/espeak-ng project also includes a copy of the speechPlayer code as an alternative Klatt implementation.
 
## Overview
NV Speech Player is a free and open-source prototype speech synthesizer that can be used by NVDA. It generates speech using Klatt synthesis, making it somewhat similar to speech synthesizers such as Dectalk and Eloquence.

## Licence and copyright
NV Speech Player is Copyright (c) 2014 NV Speech Player contributors
NV Speech Player is covered by the GNU General Public License (Version 2). 
You are free to share or change this software in any way you like 
as long as it is accompanied by the license and you make all 
source code available to anyone who wants it. This applies to 
both original and modified copies of this software, plus any 
derivative works.
For further details, you can view the license online at: 
http://www.gnu.org/licenses/old-licenses/gpl-2.0.html

## Background
The 70s and 80s saw much research in speech synthesis. One of the most prominent synthesis models that appeared was a formant-frequency synthesis known as Klatt synthesis. Some well-known Klatt synthesizers are Dectalk and Eloquence. They are well suited for use by the blind as they are extremely responsive, their pronunciation is smooth and predictable, and they are small in memory footprint. However, research soon moved onto other forms of synthesis such as concatinative speech, as although this was slower, it was much closer to the human voice. This was an advantage for usage in mainstream applications such as GPS units or telephone systems, but not necessarily so much of an advantage to the blind, who tend to care more about responsiveness and predictability over prettiness.

Although synthesizers such as Dectalk and Eloquence continued to be maintained and available for nearly 20 years, now they are becoming harder to get, with multiple companies saying that these, and their variants, have been end-of-lifed and will not be updated anymore. 

Concatinative synthesis is now starting to show promise as a replacement as the responsiveness and smoothness is improving. However, most if not all of the acceptable quality synthesizers are commercial and are rather expensive.

Both Dectalk and Eloquence were closed-source commercial products themselves. However, there is a substantial amount of source code and research material on Klatt synthesis available to the community. NV Speech Player tries to take advantage of this by being a 
modern prototype of a Klatt synthesizer, in the hopes to either be a replacement for synthesizers like Dectalk or Eloquence, or at least restart research and conversation around this synthesis method.

The eSpeak synthesizer, itself a free and open-source product has proved well as a replacement to a certain number of people in the community, but many people who hear it are extremely quick to point out its "metallic" sound and cannot seem to continue to use it. Although the authors of NV Speech Player still prefer eSpeak as their synthesizer of choice, they would still hope to try and understand better this strange resistance to eSpeak which may have something to do with eSpeak's spectral frequency synthesis verses Klatt synthesis. It may also have to do with the fact that consonants are also gathered from recorded speech and can therefore be perceived as being injected into the speech stream.

## Implementation
The synthesis engine itself is written in C++ using modern idioms, but closely following the implementation of klsyn-88, found at http://linguistics.berkeley.edu/phonlab/resources/

eSpeak is used to parse text into phonemes represented in IPA, making use of existing eSpeak dictionary processing. eSpeak can be found at: http://espeak.sourceforge.net/

The Klatt formant data for each individual phoneme was collected mostly from a project called PyKlatt: http://code.google.com/p/pyklatt/ However it has been further tweaked based on testing and matching with eSpeak's own data.

The rules for phoneme lengths, gaps, speed and intonation have been coded by hand in Python, though eSpeak's own intonation data was tried to be copied as much as possible.
 
## Building NV Speech Player
You will need:
- Python 3.7: http://www.python.org
- SCons 3: http://www.scons.org/
- Visual Studio 2019 Community 
 
To build: run scons

After building, there will be a nvSpeechPlayer_xxx.nvda-addon file in the root directory, where xxx is the git revision or hardcoded version number.
Installing this add-on into NVDA will allow you to use the Speech Player synthesizer in NVDA. Note everything you need is in the add-on, no extra dlls or files need to be copied.
 
