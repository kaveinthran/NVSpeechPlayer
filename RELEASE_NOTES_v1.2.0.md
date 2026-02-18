# nvSpeechPlayer v1.2.0 - NVDA 2025.3+ Compatibility Update

## What's New in v1.2

This release brings improved compatibility with NVDA 2025.3 and later, merging fixes from the community (tgeczy/TGSpeechBox).

### Bug Fixes & Improvements

- **Background worker thread**: Audio processing now runs in a dedicated background thread, fixing `synthDoneSpeaking` timing issues on modern NVDA.
- **Fixed TypeError in `feed()` call**: Corrected argument passing to `wavePlayer.feed()` which caused crashes on NVDA 2025.3+.
- **Debug logging for `idle()` exceptions**: Exceptions in the audio idle loop are now caught and logged instead of silently crashing the synth.
- **Improved `speechPlayer.py`**: Various robustness improvements for 64-bit NVDA.

### Installation

1. Download `nvSpeechPlayer_v1.2.nvda-addon` below
2. Open it with NVDA (or drag into the NVDA Add-on Manager)
3. Restart NVDA when prompted

### Compatibility

- Minimum NVDA version: 2019.3
- Tested up to: NVDA 2026.1 (alpha-54514)
