# NVDA Compatibility Updates

This document details the technical changes made to ensure NV Speech Player works with modern NVDA versions (2019.3 through 2025.3+).

## Overview

The original NV Speech Player code was written for NVDA 2014-2018 era. Several breaking changes in NVDA's API required updates to maintain compatibility with NVDA 2019.3 and later, particularly NVDA 2021.1 which introduced significant API changes.

## Supported NVDA Versions

- **Minimum**: NVDA 2019.3.0
- **Last Tested**: NVDA 2025.3.2
- **Fully Compatible**: NVDA 2019.3 through 2025.3+

## Breaking Changes Fixed

### 1. Speech Commands Module Restructuring (NVDA 2021.1)

**Issue**: In NVDA 2021.1 (PR #12126), speech commands were moved from the `speech` module to `speech.commands` submodule.

**Error**:
```
AttributeError: module 'speech' has no attribute 'IndexCommand'
AttributeError: module 'speech' has no attribute 'PitchCommand'
```

**Fix**: Added backward-compatible imports that try modern path first, then fall back to legacy:

```python
# Import speech commands with backward compatibility
try:
    from speech.commands import IndexCommand, PitchCommand
except ImportError:
    try:
        from speech import IndexCommand, PitchCommand
    except ImportError:
        # Fallback for very old NVDA versions
        IndexCommand = None
        PitchCommand = None
```

**Files Changed**:
- `nvdaAddon/synthDrivers/nvSpeechPlayer/__init__.py`
- `nvdaAddon/synthDrivers/nveloq/__init__.py`

### 2. Driver Settings API Changes

**Issue**: `NumericDriverSetting` moved from `driverHandler` to `autoSettingsUtils.driverSetting`.

**Fix**: Try modern import path first, fall back to legacy:

```python
try:
    from autoSettingsUtils.driverSetting import NumericDriverSetting
except ImportError:
    from driverHandler import NumericDriverSetting
```

### 3. Audio API Enhancements (NVDA 2024.x)

**Issue**: NVDA 2024.x introduced `AudioPurpose` enum for better audio ducking control.

**Fix**: Detect availability and use when present:

```python
try:
    from nvwave import AudioPurpose
    HAS_AUDIO_PURPOSE = True
except ImportError:
    HAS_AUDIO_PURPOSE = False

# Later in code:
if HAS_AUDIO_PURPOSE:
    self.wavePlayer = nvwave.WavePlayer(
        channels=1,
        samplesPerSec=self.sampleRate,
        bitsPerSample=16,
        outputDevice=outputDevice,
        wantDucking=True,
        purpose=AudioPurpose.SPEECH
    )
else:
    # Fallback for NVDA 2019.3-2023.x
    self.wavePlayer = nvwave.WavePlayer(
        channels=1,
        samplesPerSec=self.sampleRate,
        bitsPerSample=16,
        outputDevice=outputDevice
    )
```

### 4. isinstance() Checks in speak() Method

**Issue**: The `speak()` method used `isinstance(item, speech.PitchCommand)` which broke with the module restructuring.

**Fix**: Use the imported class names directly:

```python
# Before (broken):
if isinstance(item, speech.PitchCommand):
    pitchOffset=item.offset
elif isinstance(item, speech.IndexCommand):
    userIndex=item.index

# After (fixed):
if isinstance(item, PitchCommand):
    pitchOffset=item.offset
elif isinstance(item, IndexCommand):
    userIndex=item.index
```

### 5. supportedCommands Declaration

**Issue**: `supportedCommands` was declared as a set referencing module-qualified names.

**Fix**: Use imported class names in the set:

```python
# Before (broken):
supportedCommands = {
    speech.IndexCommand,
    speech.PitchCommand,
}

# After (fixed):
supportedCommands = {
    IndexCommand,
    PitchCommand,
}
```

## Configuration Compatibility

### Audio Output Device

Added support for both modern and legacy config paths:

```python
try:
    outputDevice = config.conf["audio"]["outputDevice"]
except KeyError:
    outputDevice = config.conf["speech"]["outputDevice"]
```

## Two Variants Explained

### Directory Structure

Both variants are built from the same codebase but create separate synth drivers:

```
nvdaAddon/
├── synthDrivers/
│   ├── nvSpeechPlayer/    # Standard variant
│   │   └── __init__.py    # name = "nvSpeechPlayer"
│   └── nveloq/            # Eloquence-style variant
│       └── __init__.py    # name = "nveloq"
```

**Important**: The directory name must match the synth driver's `name` property, or NVDA will fail to load with:
```
ModuleNotFoundError: No module named 'synthDrivers.xyz'
```

### Intonation Differences

**nvSpeechPlayer (Standard)**:
- Uses `ipa.py` with eSpeak-style table-based intonation (post-646f7f9)
- Pitch contours defined by preHead, head, nucleus, tail components
- More complex intonation system matching eSpeak

**nveloq (Eloquence-style)**:
- Uses `ipa.py` with smooth formula-based pitch curves (pre-646f7f9, based on ee80f4d)
- Pitch calculated using mathematical formulas based on syllable stress
- Timing tweaks: stressed syllables at 1.5x speed, unstressed at 1.2x speed
- Stop phonemes limited to 10ms duration
- Produces intonation similar to classic Eloquence synthesizer

Both variants share:
- Same Klatt synthesis engine (`speechPlayer.dll`)
- Same phoneme formant data (`data.py`)
- Same IPA processing
- Same audio threading and playback code

## Build System Updates

### Manifest Configuration

Each variant has its own manifest template:

**nvdaAddon/manifest.ini.in** (Standard):
```ini
name=nvSpeechPlayer
summary=nvSpeechPlayer
version=_version_
minimumNVDAVersion = 2019.3.0
lastTestedNVDAVersion = 2025.3.2
```

**nvdaAddon/manifest.ini.in** (nveloq):
```ini
name=nveloq
summary=nvSpeechPlayer (Eloquence-style intonation)
description=A free Klatt-based speech synthesizer with Eloquence-style intonation from pre-646f7f9
version=_version_
minimumNVDAVersion = 2019.3.0
lastTestedNVDAVersion = 2025.3.2
```

### SCons Build Configuration

The build system creates separate .nvda-addon packages:

```python
# Standard variant (sconstruct)
addon=env.ZipArchive(
    target="nvSpeechPlayer_%s.nvda-addon"%env['version'],
    source=[Dir('synthDrivers/nvSpeechPlayer'),'manifest.ini'],
    relativeTo=addonRelPath
)

# Eloquence variant (nvdaAddon/sconscript)
addon=env.ZipArchive(
    target="nveloq_%s.nvda-addon"%env['version'],
    source=[Dir('synthDrivers'),'manifest.ini'],
    relativeTo=addonRelPath
)
```

## Testing

Both variants have been tested with:
- NVDA 2025.3.2 (latest at time of writing)
- Python 3.11.9
- Windows 10.0.19045

All compatibility code includes fallbacks to maintain support for NVDA 2019.3+.

## Commit History

Key commits for compatibility updates:

- `23490f0`: Restored Eloquence-style intonation from ee80f4d
- `24c303b`: Added speech.commands imports and fixed supportedCommands
- `59765b0`: Fixed isinstance() calls in speak() method for both variants
- `698c5fa`: Renamed Eloquence variant synth driver to 'nveloq'
- `aa158e5`: Renamed directory structure to match synth name

## References

- NVDA API Changes: https://www.nvaccess.org/files/nvda/documentation/developerGuide.html
- NVDA 2021.1 Breaking Changes: PR #12126
- Original NV Speech Player: https://bitbucket.org/nvaccess/speechplayer
- Klatt Synthesis: http://linguistics.berkeley.edu/phonlab/resources/

## Future Compatibility

The backward-compatible import pattern used should maintain compatibility with:
- Future NVDA versions that maintain current API
- Older NVDA versions back to 2019.3

If future NVDA versions introduce breaking changes, similar try/except import patterns can be added to maintain backward compatibility.
