# NV Speech Player User Guide

## Quick Start

NV Speech Player is a free Klatt-based speech synthesizer for NVDA that sounds similar to Eloquence and DECtalk.

### Which Variant Should I Choose?

Two variants are available - **you can install both and switch between them**:

| Variant | Description | Best For |
|---------|-------------|----------|
| **nvSpeechPlayer** | Modern eSpeak-style intonation | Users who prefer more expressive, varied pitch patterns |
| **nveloq** | Classic Eloquence-style intonation | Users who prefer smooth, predictable pitch similar to old Eloquence |

**Not sure?** Install both and try them! Both variants can coexist peacefully.

### Installation

1. **Download** the variant you want:
   - [nvSpeechPlayer_master-59765b0.nvda-addon](nvSpeechPlayer_master-59765b0.nvda-addon) (Standard)
   - [nveloq_master-aa158e5.nvda-addon](nveloq_master-aa158e5.nvda-addon) (Eloquence-style)

2. **Install**: Double-click the downloaded .nvda-addon file (or press Enter on it in Windows Explorer)

3. **Confirm**: NVDA will ask if you want to install the add-on. Choose "Yes"

4. **Restart**: NVDA will prompt you to restart. Choose "Yes" to complete installation

5. **Select**: After restart, press `NVDA+Control+S` to open Synth Settings, then:
   - Choose "nvSpeechPlayer" or "nveloq" from the synthesizer list
   - Press OK

### What's the Difference?

Both variants use the **same voice engine** (Klatt synthesis) and sound fundamentally the same. The only difference is **how pitch changes** as the synthesizer speaks:

#### nvSpeechPlayer (Standard)
- Uses a **table-based** intonation system
- Pitch changes are based on sentence structure (head, nucleus, tail)
- Similar to how eSpeak handles intonation
- More complex, varied pitch patterns
- **Introduced**: May 2014 (commit 646f7f9)

#### nveloq (Eloquence-style)
- Uses **smooth mathematical** pitch curves
- Pitch changes based on syllable stress
- Similar to classic Eloquence synthesizer
- Smoother, more predictable intonation
- **Based on**: April 2014 code (commit ee80f4d)

**Think of it like this:**
- **nvSpeechPlayer** = More dramatic actor reading a story
- **nveloq** = Calm narrator with steady, smooth delivery

Both are equally responsive and fast. It's purely a matter of personal preference!

### Switching Between Variants

If you have both installed:

1. Press `NVDA+Control+S` (Synth Settings)
2. Choose "nvSpeechPlayer" or "nveloq" from the Synthesizer dropdown
3. Press OK
4. NVDA will switch immediately - no restart needed

### Available Voices

Both variants include the same voices:
- **Adam** (default)
- **Benjamin** (deeper, slightly different formants)
- **Caleb** (whisper - aspirated voice only)
- **David** (lower pitch)

### Adjustable Settings

- **Rate**: Speaking speed (0-100)
- **Pitch**: Voice pitch (0-100)
- **Volume**: Loudness (0-100)
- **Inflection**: Amount of pitch variation (0-100)
- **Voice**: Choose from available voices

### System Requirements

- **NVDA**: Version 2019.3 or later (tested through 2025.3)
- **Windows**: Any version supported by NVDA
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
