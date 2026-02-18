# NVSpeechPlayer v1.1.0 Release Notes

**Release Date:** February 18, 2026

## 🎉 What's New

This release adds advanced NVDA compatibility improvements inspired by tgeczy/TGSpeechBox, ensuring robust operation with NVDA 2025.3+ while maintaining backward compatibility with older versions (2019.3+).

---

## ✨ Features & Improvements

### 🔧 Explicit ctypes Prototypes (speechPlayer.py)
**Prevents 64-bit pointer truncation on modern systems**

- Added `_setupPrototypes()` method to declare all DLL function signatures explicitly
- Prevents ctypes from defaulting to 32-bit `c_int` for pointer returns
- Replaced `from ctypes import *` with explicit imports for better code clarity
- Added initialization error checking with `RuntimeError` on failure

**Impact:** Fixes crashes on 64-bit Windows systems and future Python versions

### ⚡ Background Worker Thread (nvSpeechPlayer/__init__.py)
**Non-blocking infrastructure for improved responsiveness**

- Added `_BgThread` class for queue-based task execution
- Exception isolation prevents background errors from crashing NVDA
- Clean shutdown with 2-second timeout
- `_enqueue()` helper method ready for future non-blocking phoneme conversion

**Impact:** Prepares for smoother performance under heavy load

### ⏱️ Fixed synthDoneSpeaking Timing (nvSpeechPlayer/__init__.py)
**Corrects speech completion notification**

- Changed notification to trigger AFTER audio playback drains, not immediately
- Uses 0-byte buffer feed with callback to detect actual completion
- Includes TypeError fallback for older NVDA versions

**Impact:** Prevents NVDA from starting next utterance before previous one finishes

### 🛡️ Code Quality Improvements
- Changed public attributes to private (`_wavePlayer`, `_keepAlive`, etc.) for encapsulation
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

## 📊 Changes Summary

- **Files Changed:** 2
- **Lines Added:** 166
- **Lines Removed:** 45
- **Net Change:** +121 lines

### Modified Files:
1. `speechPlayer.py` - Explicit ctypes prototypes and error checking
2. `nvdaAddon/synthDrivers/nvSpeechPlayer/__init__.py` - Background worker and timing fixes

---

## 🙏 Credits

These improvements are based on work by **@tgeczy** in [tgeczy/TGSpeechBox](https://github.com/tgeczy/TGSpeechBox/commit/e6f76ff0efb7d3d46b09f9c413f6a015d69f3ed5).

Special thanks for:
- Background worker pattern
- Explicit ctypes prototypes
- Speech completion timing fixes

---

## 📥 Installation

Download the `.nvda-addon` file from the [releases page](https://github.com/kaveinthran/NVSpeechPlayer/releases/tag/v1.1.0) and install it in NVDA.

---

## 🐛 Bug Fixes from v1.0.0

- Fixed 64-bit pointer truncation issues
- Fixed premature speech completion notifications
- Improved thread safety and cleanup

---

## 🔗 Links

- **Full Changelog:** https://github.com/kaveinthran/NVSpeechPlayer/compare/v1.0.0...v1.1.0
- **Pull Request:** https://github.com/kaveinthran/NVSpeechPlayer/pull/1
- **Original Inspiration:** https://github.com/tgeczy/TGSpeechBox/commit/e6f76ff

---

**Enjoy the improved stability and compatibility!** 🚀