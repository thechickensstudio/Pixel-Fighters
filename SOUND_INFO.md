# Sound System Documentation - Pixel Fighters

## Overview
Pixel Fighters now includes a comprehensive sound system with sound effects and background music.

## Sound Files Location
All sound files are stored in: `assets/sounds/`

Current sound files (using pygame example sounds as placeholders):
- `boom.wav` - Used for hits and trap impacts
- `punch.wav` - Attack sound
- `whiff.wav` - Jump and fruit collection
- `car_door.wav` - Death sound
- `secosmic_lo.wav` - Power-up activation
- `house_lo.ogg` - Background music

## Sound Manager Class
Location: `sound_manager.py`

### Features:
- Centralized sound management
- Volume control for SFX and music separately
- Sound effect caching for performance
- Background music looping
- Graceful fallback if sounds fail to load

### Usage Example:
```python
# Create sound manager
sound_manager = SoundManager()

# Play a sound effect
sound_manager.play_sound('jump', volume_override=0.3)

# Start background music
sound_manager.play_music()

# Stop music
sound_manager.stop_music()

# Adjust volumes
sound_manager.set_sfx_volume(0.7)
sound_manager.set_music_volume(0.4)
```

## Sound Effects Integrated

### Player Actions (player.py)
- **Jump**: Plays when jumping or double jumping (volume: 0.3)
- **Attack**: Plays when attacking (volume: 0.4)
- **Hit**: Plays when attack connects (volume: 0.5)
- **Power-up**: Plays when activating fruit power-up (volume: 0.5)
- **Trap Hit**: Plays when hit by instant-kill trap (volume: 0.6)

### Fruit Collection (fruit.py)
- **Collect Fruit**: Plays when picking up a fruit (volume: 0.4)

### Game Events (main.py)
- **Death**: Plays when falling off stage (volume: 0.5)
- **Background Music**: Loops during gameplay, stops on menu/game over

## Customizing Sounds

### Replacing Sound Files
1. Add your sound files to `assets/sounds/`
2. Edit `sound_manager.py` in the `load_sounds()` method
3. Update the filename mappings:
```python
sound_files = {
    'jump': 'your_jump_sound.wav',
    'attack': 'your_attack_sound.wav',
    # etc...
}
```

### Supported Formats
- WAV (recommended for sound effects)
- OGG (recommended for music)
- MP3 (supported but may have slight delay)

### Volume Adjustment
Edit these values in `SoundManager.__init__()`:
```python
self.sfx_volume = 0.6  # 0.0 to 1.0
self.music_volume = 0.3  # 0.0 to 1.0
```

Or adjust per-sound using `volume_override`:
```python
sound_manager.play_sound('jump', volume_override=0.2)
```

## Implementation Details

### Sound Manager Integration
The `SoundManager` is created in `main.py` and passed to:
- Player objects (for jump, attack, hit sounds)
- FruitManager (for collection sounds)
- TrapManager (for trap damage sounds)

### Performance Considerations
- Sounds are loaded once at initialization
- Sound effects use pygame.mixer.Sound (multiple simultaneous sounds)
- Music uses pygame.mixer.music (single stream, low memory)
- Failed sound loads create None placeholders (no crashes)

## Testing
Run the game and test sounds:
1. Jump around - should hear jump sounds
2. Attack - should hear punch/whoosh
3. Get hit - should hear impact sound
4. Collect fruit - should hear collection + power-up sounds
5. Fall off stage - should hear death sound
6. Background music should loop continuously

## Future Enhancements
- Character-specific attack sounds
- Stage-specific background music
- Victory/defeat fanfares
- Menu navigation sounds
- Combo sound effects
- Dynamic music intensity based on gameplay
