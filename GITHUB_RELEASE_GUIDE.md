# GitHub Release Setup Guide

This guide explains how to create releases on GitHub so users can download the addon.

## Creating a New Release

### Step 1: Push Your Code to GitHub

First, make sure your latest changes are committed and pushed:

```bash
cd J:\claude\NVSpeechPlayer
git add .
git commit -m "Update nvSpeechPlayer: default inflection 65, settings ring support, updated docs"
git push origin main
```

### Step 2: Create a Release on GitHub

1. **Go to your repository** on GitHub:
   - Navigate to: `https://github.com/kaveinthran/NVSpeechPlayer`

2. **Click "Releases"** on the right sidebar
   - Or go directly to: `https://github.com/kaveinthran/NVSpeechPlayer/releases`

3. **Click "Draft a new release"** (or "Create a new release")

4. **Fill in the release details:**

   - **Tag version**: `v1.0.0` (or your preferred version number)
     - Click "Choose a tag" and type a new tag name
     - Format: `v1.0.0`, `v1.1.0`, etc.

   - **Release title**: `nvSpeechPlayer v1.0.0 - Dual Intonation Mode`

   - **Description**:
     ```markdown
     ## NV Speech Player - Dual Intonation Mode

     A free Klatt-based speech synthesizer for NVDA with switchable intonation modes.

     ### ⭐ What's New
     - **Dual intonation modes** in one add-on
     - Switch between nvEspeak (modern) and NVeloq (Eloquence-style) on-the-fly
     - Default inflection improved to 65 for better naturalness
     - Settings ring support for quick mode switching
     - NVDA 2019.3 through 2026.1+ compatibility

     ### 📥 Installation

     1. Download `nvSpeechPlayer_master-633c036.nvda-addon` below
     2. Open the file (double-click or press Enter)
     3. Follow NVDA prompts to install
     4. Restart NVDA
     5. Select nvSpeechPlayer in Voice Settings (`NVDA+Ctrl+V`)

     ### 🎯 Features

     - **nvEspeak mode** (default): Modern eSpeak-style intonation
     - **NVeloq mode**: Classic Eloquence-style intonation
     - Toggle via Voice Settings dialog or settings ring
     - Voices: Adam, Benjamin, Caleb, David
     - Adjustable rate, pitch, volume, inflection

     ### 📖 Documentation

     See [USER_GUIDE.md](https://github.com/kaveinthran/NVSpeechPlayer/blob/main/USER_GUIDE.md) for full instructions.

     ### System Requirements

     - NVDA 2019.3 or later
     - Windows (any version supported by NVDA)
     - 32-bit architecture
     ```

5. **Attach the addon file:**
   - Scroll to "Attach binaries" section
   - Drag and drop `nvSpeechPlayer_master-633c036.nvda-addon` from your computer
   - Or click "choose your files" and browse to select it

6. **Set as latest release:**
   - Check ✅ "Set as the latest release"

7. **Click "Publish release"**

## File to Upload

Upload this file to the release:
- `nvSpeechPlayer_master-633c036.nvda-addon` (64 KB)

Located at: `J:\claude\NVSpeechPlayer\nvSpeechPlayer_master-633c036.nvda-addon`

## After Publishing

Once published, users can download from:
- Direct link: `https://github.com/kaveinthran/NVSpeechPlayer/releases/latest/download/nvSpeechPlayer_master-633c036.nvda-addon`
- Releases page: `https://github.com/kaveinthran/NVSpeechPlayer/releases`

## Creating Future Releases

When you make updates:

1. Build the addon: `scons nvdaAddon`
2. Commit and push changes
3. Create a new release with a new version tag (e.g., `v1.1.0`)
4. Upload the new `.nvda-addon` file
5. Update README.md and USER_GUIDE.md if needed

## Version Numbering

Suggested versioning scheme:
- `v1.0.0` - Initial release
- `v1.0.1` - Bug fixes
- `v1.1.0` - Minor features
- `v2.0.0` - Major changes

## Tips

- Always test the addon before creating a release
- Include clear installation instructions in the release notes
- Mention compatibility (NVDA versions, Windows versions)
- List what's new or fixed in each release
- Keep older releases available for users who need them
