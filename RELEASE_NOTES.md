# NVSpeechPlayer v1.1.0 - Advanced NVDA Compatibility Update

**Release Date:** February 18, 2026

This release incorporates advanced compatibility improvements for NVDA 2025.3+, based on code patterns from the tgeczy/TGSpeechBox public repository.

## What's New

### Complete Feature Parity with tgeczy/TGSpeechBox

All NVDA 2025.3+ compatibility improvements have been successfully integrated:

1. **Explicit ctypes Prototypes** (speechPlayer.py)
   - Prevents 64-bit pointer truncation on modern systems
   - Attribution: Code pattern from tgeczy/TGSpeechBox

2. **Background Worker Thread** (nvSpeechPlayer/__init__.py)
   - Infrastructure ready for non-blocking phoneme conversion
   - Attribution: Threading pattern from tgeczy/TGSpeechBox

3. **Fixed synthDoneSpeaking Timing** (nvSpeechPlayer/__init__.py)
   - Prevents NVDA from starting next utterance prematurely
   - Attribution: Timing fix from tgeczy/TGSpeechBox

## Technical Changes

- Files Modified: speechPlayer.py, nvSpeechPlayer/__init__.py
- Lines Added: 166
- Lines Removed: 45

## Compatibility

Fully compatible with NVDA 2019.3 through 2026.1+

## Attribution

This release incorporates code from the tgeczy/TGSpeechBox public repository (https://github.com/tgeczy/TGSpeechBox/commit/e6f76ff). We acknowledge and thank @tgeczy for their contributions.

## Links

- Pull Request: https://github.com/kaveinthran/NVSpeechPlayer/pull/1
- Full Changelog: https://github.com/kaveinthran/NVSpeechPlayer/compare/v1.0.0...v1.1.0