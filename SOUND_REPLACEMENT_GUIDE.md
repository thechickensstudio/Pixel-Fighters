# 🔊 Sound Replacement Guide - Improve Your Game's Audio

## Current Situation

Right now, your game uses **placeholder sounds** from pygame's examples. These are low quality and generic. You can replace them with professional, high-quality sounds!

## Sound Files to Replace

Located in: `/home/raffaga/Code/h_d_game/assets/sounds/`

| Sound Effect | Current File | Used For |
|--------------|--------------|----------|
| Jump | `whiff.wav` | Jumping & double jumping |
| Attack | `punch.wav` | When player attacks |
| Hit | `boom.wav` | When attack connects |
| Death | `car_door.wav` | Falling off stage |
| Collect Fruit | `whiff.wav` | Picking up fruits |
| Power-up | `secosmic_lo.wav` | Activating power-up |
| Trap Hit | `boom.wav` | Hit by spikes/traps |
| Background Music | `house_lo.ogg` | Gameplay music |

## 🎵 Where to Get Better Sounds (Free!)

### Best Free Sound Libraries:

1. **Freesound.org** (Best for game sounds)
   - URL: https://freesound.org
   - Free account required
   - Search for: "jump", "punch", "hit", "power up", etc.
   - Filter by: Creative Commons license

2. **OpenGameArt.org** (Made for games!)
   - URL: https://opengameart.org/art-search-advanced?keys=sound
   - Royalty-free game sounds
   - No account needed

3. **Mixkit.co/free-sound-effects/** (High quality)
   - No attribution required
   - Game sound effects category

4. **Zapsplat.com** (Professional quality)
   - Free with attribution
   - Great for retro game sounds

5. **JSFXR.com** (Create your own!)
   - Browser-based sound generator
   - Perfect for retro/pixel art games
   - Export as WAV

### Recommended Searches:

- **Jump**: "8-bit jump", "cartoon jump", "game jump"
- **Attack**: "sword swoosh", "punch", "whip", "woosh"
- **Hit**: "game hit", "impact", "punch impact", "8-bit hit"
- **Power-up**: "power up", "level up", "collect", "pickup"
- **Death**: "game over", "death", "fall"
- **Music**: "chiptune", "8-bit music", "game music loop"

## 📥 How to Replace Sounds

### Method 1: Simple Replacement

1. **Download your new sound** (as WAV, OGG, or MP3)
2. **Rename it** to match the current file:
   ```bash
   # Example for jump sound:
   # Your downloaded file: awesome_jump.wav
   # Rename to: whiff.wav
   ```
3. **Copy to the sounds folder:**
   ```bash
   cp your_new_sound.wav /home/raffaga/Code/h_d_game/assets/sounds/whiff.wav
   ```
4. **Rebuild the web version:**
   ```bash
   cd /home/raffaga/Code/h_d_game
   ./venv/bin/pygbag --build .
   cp -r build/web website/game
   ```

### Method 2: Custom Names (Better Organization)

1. **Copy your sounds** to `assets/sounds/` with descriptive names:
   ```
   assets/sounds/
   ├── jump_sound.wav
   ├── attack_swoosh.wav
   ├── hit_impact.wav
   ├── death_fall.wav
   ├── fruit_collect.wav
   ├── powerup_activate.wav
   └── background_music.ogg
   ```

2. **Edit sound_manager.py** (line 27):
   ```python
   sound_files = {
       # Player actions
       'jump': 'jump_sound',        # Changed from 'whiff'
       'attack': 'attack_swoosh',   # Changed from 'punch'
       'hit': 'hit_impact',         # Changed from 'boom'
       'death': 'death_fall',       # Changed from 'car_door'
       
       # Items
       'collect_fruit': 'fruit_collect',
       'powerup': 'powerup_activate',
       
       # Traps
       'trap_hit': 'hit_impact',
   }
   ```

3. **Rebuild:**
   ```bash
   cd /home/raffaga/Code/h_d_game
   ./venv/bin/pygbag --build .
   cp -r build/web website/game
   ```

## 🎚️ Adjusting Sound Quality

### Volume Levels

Edit `sound_manager.py` line 17-18:

```python
self.sfx_volume = 1.0     # 0.0 to 1.0 (currently max)
self.music_volume = 0.4   # 0.0 to 1.0 (lower so it doesn't overpower SFX)
```

### Per-Sound Volume

Edit where sounds are played in `player.py`:

```python
# Example: Make jump quieter
self.sound_manager.play_sound('jump', 0.5)  # Change 0.5 to 0.3 for quieter

# Example: Make attack louder
self.sound_manager.play_sound('attack', 1.0)  # Max volume
```

### Audio Format Recommendations

**For best web compatibility:**
- **OGG format** - Best for web, smaller file size
- **WAV format** - Works locally, auto-converted for web
- **MP3 format** - Works but may have slight delay

**Recommended settings when exporting:**
- **Sample Rate**: 22050 Hz or 44100 Hz
- **Bit Rate**: 128 kbps (for OGG)
- **Channels**: Mono or Stereo (Mono = smaller files)

## 🛠️ Free Audio Editing Tools

To improve/edit your sounds:

1. **Audacity** (Free, powerful)
   - Download: https://www.audacityteam.org/
   - Features: Cut, normalize, add effects
   - Export to WAV, OGG, MP3

2. **Online Audio Converter**
   - URL: https://online-audio-converter.com/
   - Convert between formats
   - Trim and adjust volume

## 🎯 Quick Sound Improvement Tips

### Make Sounds More "Punchy":

1. **Normalize** - Makes sounds louder without distortion
2. **Add reverb** - Gives depth (don't overdo it)
3. **Compress** - Evens out volume
4. **Trim silence** - Remove dead air at start/end
5. **Fade in/out** - Prevents clicking

### Example: Improving a Jump Sound in Audacity

1. Open `whiff.wav` in Audacity
2. Select all (Ctrl+A)
3. Effect > Normalize (check "Normalize to -1.0 dB")
4. Effect > Compressor (use defaults)
5. Trim silence from start/end
6. Export as WAV or OGG
7. Replace in `assets/sounds/`

## 📋 Quick Replacement Checklist

- [ ] Browse freesound.org or opengameart.org
- [ ] Download 8 sound files (jump, attack, hit, death, collect, powerup, trap, music)
- [ ] Edit in Audacity (normalize, trim)
- [ ] Export as WAV or OGG
- [ ] Copy to `assets/sounds/` folder
- [ ] Rename to match current files OR edit sound_manager.py
- [ ] Test locally: `./venv/bin/python main.py`
- [ ] Rebuild web: `./venv/bin/pygbag --build .`
- [ ] Update website: `cp -r build/web website/game`
- [ ] Refresh browser and test!

## 🎮 After Replacing Sounds

Always test:
1. **Local version** - Make sure sounds work before building for web
2. **Web version** - Rebuild and test in browser
3. **Volume balance** - Music shouldn't drown out effects

## 📞 Need Help?

If you want me to help you:
1. Download specific sounds
2. Edit sound_manager.py with new filenames
3. Rebuild the web version

Just let me know which sounds you want to replace!

---

**Pro Tip**: Start with just replacing 2-3 sounds (like jump and attack) to see the improvement, then do the rest!
