# Build Instructions for NVSpeechPlayer

## Prerequisites

### Required Software
- **Python 3.7+**: http://www.python.org
- **SCons 3+**: `pip install scons` or http://www.scons.org/
- **Visual Studio 2019 Community** or later (Windows only)
- **Windows OS**: Required for building (uses Windows APIs)

### Why Windows is Required
The speechPlayer synthesis engine is written in C++ and uses Windows-specific APIs:
- `windows.h` - Windows API headers
- `winmm.lib` - Windows Multimedia library
- MSVC compiler flags (`/EHsc`, `/MT`, `/GL`, etc.)

## Build Steps

### 1. Install Dependencies

```bash
# Install SCons
pip install scons

# Ensure Visual Studio 2019+ is installed with C++ development tools
```

### 2. Build the Project

```bash
# Navigate to repository root
cd NVSpeechPlayer

# Run SCons build
scons
```

This will:
1. Compile `src/*.cpp` files into `speechPlayer.dll` (32-bit)
2. Copy required files to `build/nvdaAddon/synthDrivers/nvSpeechPlayer/`
3. Create `nvSpeechPlayer_<version>.nvda-addon` package

### 3. Build Output

After a successful build, you will find:
- `speechPlayer.dll` - The compiled speech synthesis engine
- `nvSpeechPlayer_<version>.nvda-addon` - The installable NVDA add-on package

Example: `nvSpeechPlayer_copilot-check-completion-status-551c8cb.nvda-addon`

## What's Inside the Addon

The `.nvda-addon` file is a ZIP archive containing:

```
manifest.ini
synthDrivers/
  nvSpeechPlayer/
    __init__.py          - Main synthesizer driver (dual-mode support)
    ipa.py               - IPA phoneme definitions
    speechPlayer.py      - Python wrapper for DLL
    speechPlayer.dll     - C++ synthesis engine
    data.py              - Phoneme formant data
```

## Current Status

### ✅ Completed
- All Python code (synthesizer drivers for both modes)
- Documentation (README, USER_GUIDE, COMPATIBILITY, RELEASE_NOTES)
- Build scripts (sconstruct, sconscripts)
- C++ source code for speechPlayer engine

### ⚠️ Not Completed (Requires Windows Build)
- `speechPlayer.dll` - Must be compiled on Windows with Visual Studio
- `nvSpeechPlayer_<version>.nvda-addon` - Cannot be created without the DLL

## Building for Release

### Step 1: Build on Windows

1. Open "x64 Native Tools Command Prompt for VS 2019" (or later)
2. Navigate to repository directory
3. Run:
   ```cmd
   python -m pip install scons
   scons release=true
   ```

### Step 2: Verify the Build

Check that these files exist:
- `speechPlayer.dll` (in root directory)
- `nvSpeechPlayer_<version>.nvda-addon` (in root directory)

### Step 3: Test the Addon

1. Install NVDA 2019.3 or later
2. Double-click the `.nvda-addon` file
3. Confirm installation
4. Restart NVDA
5. Open Voice Settings (`NVDA+Ctrl+S`)
6. Select "nvSpeechPlayer" from the synthesizer list
7. Test speech output

### Step 4: Create GitHub Release

1. Go to https://github.com/kaveinthran/NVSpeechPlayer/releases
2. Click "Draft a new release"
3. Set tag version: `v1.1.0` (or appropriate version)
4. Set release title: `NVSpeechPlayer v1.1.0 - Advanced NVDA Compatibility Update`
5. Copy release notes from `RELEASE_NOTES.md`
6. Attach the `.nvda-addon` file
7. Check "Set as the latest release"
8. Click "Publish release"

## Troubleshooting

### Error: "windows.h: No such file or directory"
- **Cause**: Building on Linux/Mac or Visual Studio not installed
- **Solution**: Must build on Windows with Visual Studio installed

### Error: "fatal error C1083: Cannot open include file: 'windows.h'"
- **Cause**: Visual Studio C++ tools not installed
- **Solution**: Install "Desktop development with C++" workload in Visual Studio Installer

### Error: "LINK : fatal error LNK1104: cannot open file 'winmm.lib'"
- **Cause**: Windows SDK not installed
- **Solution**: Install Windows SDK via Visual Studio Installer

### Build succeeds but addon doesn't work
- **Check**: Architecture mismatch (64-bit vs 32-bit)
- **Solution**: NVDA is currently 32-bit only, ensure you're building for x86 (32-bit)

## Alternative: Using Pre-built Releases

If you don't have Windows or Visual Studio, download pre-built releases from:
https://github.com/kaveinthran/NVSpeechPlayer/releases

## Environment Notes

The build system (sconstruct) is configured for:
- **Target Architecture**: x86 (32-bit) - matches NVDA
- **Compiler**: MSVC (Microsoft Visual C++)
- **Build Tool**: SCons
- **Platform**: Windows only

## Next Steps After Building

Once you have successfully built the addon:

1. **Version tagging**: Commit the DLL if needed (or keep it as a build artifact)
2. **Release creation**: Upload to GitHub Releases page
3. **Documentation**: Update README with download links
4. **Testing**: Verify compatibility across NVDA versions (2019.3 - 2026.1+)
