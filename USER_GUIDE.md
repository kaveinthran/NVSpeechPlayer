# NV Speech Player User Guide

## Quick Start

NV Speech Player is a free Klatt-based speech synthesizer for NVDA that sounds similar to Eloquence and DECtalk.

### ⭐ NEW: Dual Intonation Mode!

**ONE add-on now includes BOTH modes!** No need for separate installations.

The **nvSpeechPlayer** add-on now features a built-in mode switcher:

| Mode | Description | How to Enable |
|------|-------------|---------------|
| **nvEspeak** (default) | Modern eSpeak-style intonation - varied, expressive | Leave "Intonation: NVeloq" unchecked |
| **NVeloq** | Classic Eloquence-style - smooth, predictable | Check "Intonation: NVeloq (Eloquence-style)" in synth settings |

**Benefits:**
- ✅ Switch modes instantly without restarting NVDA
- ✅ Compare both styles easily using synth settings ring
- ✅ ONE add-on - no separate installations needed
- ✅ Choose your preferred mode anytime

### Installation

1. **Download** the recommended add-on:
   - [nvSpeechPlayer_master-bc89128.nvda-addon](nvSpeechPlayer_master-bc89128.nvda-addon) **(Recommended - includes both modes!)**
   - Or [nveloq_master-bc89128.nvda-addon](nveloq_master-bc89128.nvda-addon) (Standalone NVeloq-only variant)

2. **Install**: Double-click the downloaded .nvda-addon file (or press Enter on it in Windows Explorer)

3. **Confirm**: NVDA will ask if you want to install the add-on. Choose "Yes"

4. **Restart**: NVDA will prompt you to restart. Choose "Yes" to complete installation

5. **Select**: After restart, press `NVDA+Control+S` to open Synth Settings, then:
   - Choose "nvSpeechPlayer" from the synthesizer list
   - Press OK

### How to Switch Intonation Modes

**Method 1: Via Synth Settings Dialog**
1. Press `NVDA+Ctrl+S` to open Synth Settings
2. Tab to **"Intonation: NVeloq (Eloquence-style)"** checkbox
3. Check = NVeloq mode (Eloquence-style), Uncheck = nvEspeak mode (default)
4. Press OK - changes take effect immediately!

**Method 2: Via Synth Settings Ring** (Quick Toggle)
1. Press `NVDA+Ctrl+Arrow Keys` to navigate synth settings
2. Find **"Intonation: NVeloq (Eloquence-style)"**
3. Press `NVDA+Ctrl+Up/Down` to toggle on/off
4. Hear the difference instantly!

### What's the Difference?

Both variants use the **same voice engine** (Klatt synthesis) and sound fundamentally the same. The only difference is **how pitch changes** as the synthesizer speaks:

#### nvEspeak Mode (Default - Unchecked)
- Uses a **table-based** intonation system
- Pitch changes based on sentence structure (preHead, head, nucleus, tail)
- Similar to how eSpeak handles intonation
- More complex, varied pitch patterns
- Timing: 1.4x/1.1x stressed syllables, 6ms stops
- **Introduced**: May 2014 (commit 646f7f9)

#### NVeloq Mode (Eloquence-style - Checked)
- Uses **smooth mathematical** pitch curves
- Pitch changes based on syllable stress formulas
- Similar to classic Eloquence synthesizer
- Smoother, more predictable intonation
- Timing: 1.5x/1.2x stressed syllables, 10ms stops
- **Based on**: April 2014 code (commit ee80f4d)

**Think of it like this:**
- **nvEspeak** = More dramatic actor with varied expression
- **NVeloq** = Calm narrator with smooth, steady delivery

Both modes are equally responsive and fast. Switch anytime to find your preference!

### Available Voices

Both variants include the same voices:
- **Adam** (default)
- **Benjamin** (deeper, slightly different formants)
- **Caleb** (whisper - aspirated voice only)
- **David** (lower pitch)

### Adjustable Settings

- **Voice**: Choose from available voices (Adam, Benjamin, Caleb, David)
- **Rate**: Speaking speed (0-100)
- **Pitch**: Voice pitch (0-100)
- **Volume**: Loudness (0-100)
- **Inflection**: Amount of pitch variation (0-100)
- **Intonation: NVeloq (Eloquence-style)**: Toggle between nvEspeak/NVeloq modes (checkbox)

### System Requirements

- **NVDA**: Version 2019.3 or later (tested through 2026.1)
- **Architecture**: 64-bit (x86_64) - compatible with NVDA 2026.x
- **Windows**: Any 64-bit version supported by NVDA
- **Disk Space**: ~60KB per variant

### Troubleshooting

**Problem**: Add-on won't install
- **Solution**: Make sure you're running NVDA 2019.3 or later

**Problem**: Synthesizer not in the list
- **Solution**: Restart NVDA after installation

**Problem**: Speech sounds robotic or strange
- **Solution**: Try adjusting the Inflection setting (higher = more natural variation)

**Problem**: Want to uninstall
- **Solution**: Go to NVDA menu > Tools > Manage Add-ons, select the variant, and choose Remove

### Comparison to Other Synthesizers

| Feature | nvSpeechPlayer/nveloq | eSpeak | Eloquence | DECtalk |
|---------|----------------------|--------|-----------|---------|
| **Type** | Klatt synthesis | Formant | Klatt | Klatt |
| **Speed** | Very fast | Very fast | Very fast | Very fast |
| **Cost** | Free | Free | Commercial | Commercial |
| **Naturalness** | Good | Good | Good | Good |
| **Size** | 60KB | ~2MB | Varies | Varies |
| **Available** | Yes | Yes | End-of-life | End-of-life |

### Why Two Variants?

In May 2014 (commit 646f7f9), NV Speech Player's intonation system was completely rewritten to match eSpeak's approach. While this made the code simpler, some users felt the **April 2014 version** (commit ee80f4d) sounded more like classic Eloquence.

This project preserves **both intonation styles** so users can choose their preference:
- **nvSpeechPlayer**: The modern version with eSpeak-style intonation
- **nveloq**: The classic version with Eloquence-style intonation

Both are maintained and updated for modern NVDA compatibility.

### Getting Help

- **Issues**: Report bugs at https://github.com/kaveinthran/NVSpeechPlayer/issues
- **Source Code**: https://github.com/kaveinthran/NVSpeechPlayer
- **Original Project**: https://bitbucket.org/nvaccess/speechplayer

### License

NV Speech Player is free and open-source software licensed under the GNU General Public License (GPL) version 2.

You are free to:
- Use it for any purpose
- Share it with others
- Modify it as you wish
- Distribute modified versions

As long as you:
- Include the GPL license
- Make source code available
- Credit the original authors

Full license: http://www.gnu.org/licenses/old-licenses/gpl-2.0.html

### Credits

- **Original Author**: NV Access Limited (2014)
- **Compatibility Updates**: Community maintained (2025)
- **Klatt Synthesis**: Based on klsyn-88 from UC Berkeley
- **Phoneme Data**: Derived from PyKlatt project
- **Text-to-Phoneme**: Uses eSpeak
