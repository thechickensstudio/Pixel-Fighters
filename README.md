# Pixel Fighters

A 2D fighting game built with Python and Pygame.

## Features

- **2-Player Local Multiplayer**: Battle against a friend on the same computer
- **4 Playable Characters**: Choose from Mask Dude, Ninja Frog, Pink Man, or Virtual Guy
- **Physics-Based Combat**: Realistic gravity, jumping, and knockback mechanics
- **Damage System**: Damage percentage increases knockback, just like Smash Bros
- **Multiple Stages**: Fight across 3 different stage layouts with unique platforms and traps
- **Hazards & Traps**: Dodge fire traps, spike heads, and falling rock heads
- **Power-ups**: Collect falling fruits to gain temporary double damage
- **Sound Effects & Music**: Immersive audio with attack, jump, hit, and collection sounds
- **Smooth Animations**: Character animations for idle, running, jumping, and attacking
- **Lives System**: Each player starts with 3 lives

## Installation

### Quick Setup (Recommended)

The game runs in a Python virtual environment to keep dependencies isolated.

#### Linux/Mac:
```bash
# Run the setup script (one time only)
bash setup.sh

# Run the game
bash run.sh
```

#### Windows:
```cmd
# Run the setup script (one time only)
setup.bat

# Run the game
run.bat
```

### Manual Setup

If you prefer to set up manually:

1. Make sure you have Python 3.7+ installed
2. Create a virtual environment:
   ```bash
   python3 -m venv venv
   ```

3. Activate the virtual environment:
   - **Linux/Mac**: `source venv/bin/activate`
   - **Windows**: `venv\Scripts\activate.bat`

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Run the game:
   ```bash
   python main.py
   ```

6. When finished, deactivate the virtual environment:
   ```bash
   deactivate
   ```

## Controls

### Character Selection
- **Player 1**: Use `A` and `D` to navigate characters, press `W` to select
- **Player 2**: Use `←` and `→` to navigate characters, press `↑` to select

### In-Game Controls

#### Player 1 (Red)
- `A` - Move left
- `D` - Move right
- `W` - Jump (press again in air for double jump)
- `F` - Attack

#### Player 2 (Blue)
- `←` - Move left
- `→` - Move right
- `↑` - Jump (press again in air for double jump)
- `,` - Attack

### General Controls
- `ESC` - Return to character selection

## Gameplay

- **Objective**: Knock your opponent off the stage to score a KO
- **Damage**: Each hit increases your opponent's damage percentage
- **Knockback**: Higher damage means stronger knockback when hit
- **Lives**: Each player has 3 lives. Lose all lives to lose the game
- **Respawn**: After being KO'd, players respawn with 2 seconds of invincibility
- **Platforms**: Use platforms strategically to recover and avoid falling
- **Traps**: 
  - **Fire**: Deals 10% damage on contact (1 second cooldown)
  - **Spike Heads**: Instant death - lose a life immediately
  - **Rock Heads**: Falling hazards that kill on impact
- **Power-ups**: Collect fruits that fall from the sky to gain double damage for 10 seconds
- **Stages**: Each match randomly selects one of 3 unique stages with different layouts

## Game Mechanics

### Movement
- Smooth horizontal movement with acceleration
- Double jump capability for recovery
- Air mobility and ground friction physics

### Combat
- Attack range: Close-range melee attacks
- Damage: 10% per hit
- Knockback: Scales with damage percentage
- Hitstun: Brief stun after being hit
- Attack cooldown: Prevents spamming

### Platforms
- Pass-through platforms allow jumping up from below
- Use platforms to avoid falling off stage
- Strategic positioning is key to victory

## Tips

1. **Watch Your Damage**: The higher your percentage, the farther you'll fly when hit
2. **Use Double Jump Wisely**: Save your double jump for recovery
3. **Platform Movement**: Move between platforms to avoid attacks
4. **Spacing**: Keep optimal distance to land hits while avoiding opponent's attacks
5. **Edge Guarding**: Position yourself to intercept recovering opponents

## Assets

This game uses pixel art assets including:
- Character sprites with multiple animations
- Platform/terrain tiles
- Background images

All assets are located in the `assets/` directory.

## Development

The game is structured with the following modules:

- `main.py` - Main game loop and state management
- `player.py` - Player class with physics, animations, and combat
- `platform.py` - Platform collision and rendering
- `character_select.py` - Character selection screen
- `fruit.py` - Fruit power-up system with collection mechanics
- `traps.py` - Hazard system including fire, spikes, and falling rocks
- `sound_manager.py` - Sound effects and music management

## Sound System

The game includes a comprehensive sound system:

### Sound Effects
- **Jump**: Plays when players jump or double jump
- **Attack**: Plays when initiating an attack
- **Hit**: Plays when an attack successfully lands
- **Collect Fruit**: Plays when picking up power-up fruits
- **Power-up**: Plays when activating the fruit power-up effect
- **Trap Hit**: Plays when hit by spikes or other instant-kill traps
- **Death**: Plays when falling off the stage

### Background Music
- Looping background music plays during gameplay
- Music automatically stops when returning to character select or game over

### Customization
The sound system is modular and uses the `SoundManager` class. You can:
- Replace sound files in `assets/sounds/` with your own WAV, MP3, or OGG files
- Adjust volume levels in `sound_manager.py`
- Add new sound effects by editing the `load_sounds()` method

## Future Enhancements

Possible features to add:
- Special moves/abilities for each character
- More stage varieties
- AI opponent mode
- More characters
- Tournament mode
- Online multiplayer

## Credits

Built with Python, Pygame and AI by Hjälmar and Daniel.

Enjoy the game!
