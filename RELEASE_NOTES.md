# NVSpeechPlayer v1.1.0 - Advanced NVDA Compatibility Update

**Release Date:** February 18, 2026

This release incorporates advanced compatibility improvements for NVDA 2025.3+, based on code patterns from the [tgeczy/TGSpeechBox](https://github.com/tgeczy/TGSpeechBox) public repository.

---

## 🎉 What's New

### ✅ Complete Feature Parity with tgeczy/TGSpeechBox

All NVDA 2025.3+ compatibility improvements have been successfully integrated:

#### 🔧 **1. Explicit ctypes Prototypes** (`speechPlayer.py`)
- **Problem:** Without explicit return types, ctypes defaults to `c_int` (32-bit), causing pointer truncation on 64-bit systems
- **Solution:** Added `_setupPrototypes()` method declaring all 5 DLL function signatures
- **Impact:** Prevents crashes on 64-bit Windows and future Python versions
- **Attribution:** Code pattern from tgeczy/TGSpeechBox

#### ⚡ **2. Background Worker Thread** (`nvSpeechPlayer/__init__.py`)
- **Problem:** Heavy phoneme conversion can block NVDA's main thread
- **Solution:** Added `_BgThread` class with queue-based task execution
- **Impact:** Infrastructure ready for non-blocking phoneme conversion
- **Attribution:** Threading pattern from tgeczy/TGSpeechBox

#### ⏱️ **3. Fixed synthDoneSpeaking Timing** (`nvSpeechPlayer/__init__.py`)
- **Problem:** Speech completion was notified immediately, not after audio finished
- **Solution:** Changed to trigger after audio playback drains using callback
- **Impact:** Prevents NVDA from starting next utterance prematurely
- **Attribution:** Timing fix from tgeczy/TGSpeechBox

---

## 📊 Technical Changes

### Files Modified
- `speechPlayer.py` (+42 lines, -4 lines)
- `nvdaAddon/synthDrivers/nvSpeechPlayer/__init__.py` (+124 lines, -41 lines)

### Code Improvements
- Replaced `from ctypes import *` with explicit imports
- Added initialization error checking with `RuntimeError`
- Changed public attributes to private (`_wavePlayer`, `_keepAlive`, etc.)
- Added proper exception handling in terminate methods
- Improved logging with debug messages

---

## 🔄 Compatibility

| NVDA Version | Status |
|--------------|--------|
| 2019.3 - 2024.x | ✅ Fully compatible (with fallbacks) |
| 2025.1 - 2025.3+ | ✅ Full support with new APIs |
| Future versions | ✅ Prepared with explicit type declarations |

---

## 🙏 Attribution

This release incorporates code from the [tgeczy/TGSpeechBox](https://github.com/tgeczy/TGSpeechBox) public repository. We acknowledge and thank @tgeczy for their contributions utilized from their publicly available repository.

---

## 🐛 Bug Fixes

- Fixed 64-bit pointer truncation in speechPlayer.dll initialization
- Fixed premature speech completion notifications
- Improved thread safety and cleanup

---

## 🔗 Links

- **Pull Request:** https://github.com/kaveinthran/NVSpeechPlayer/pull/1
- **Full Changelog:** https://github.com/kaveinthran/NVSpeechPlayer/compare/v1.0.0...v1.1.0
- **Source Attribution:** https://github.com/tgeczy/TGSpeechBox/commit/e6f76ff0efb7d3d46b09f9c413f6a015d69f3ed5
