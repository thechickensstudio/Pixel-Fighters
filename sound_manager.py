import pygame
import os

class SoundManager:
    """Manages all game sounds and music"""
    
    def __init__(self):
        # Mixer is already pre-initialized in main.py before pygame.init()
        # No need to call mixer.init() here again
        
        # Sound effects dictionary
        self.sounds = {}
        
        # Music
        self.music_playing = False
        
        # Volume settings
        self.sfx_volume = 1.0  # Increased for web compatibility
        self.music_volume = 0.4
        
        # Load all sounds
        self.load_sounds()
    
    def load_sounds(self):
        """Load all sound effects"""
        sound_files = {
            # Player actions
            'jump': 'whiff',
            'attack': 'punch',
            'hit': 'boom',
            'death': 'car_door',
            
            # Items
            'collect_fruit': 'whiff',
            'powerup': 'secosmic_lo',
            
            # Traps
            'trap_hit': 'boom',
        }
        
        for sound_name, base_filename in sound_files.items():
            # Try multiple formats for web compatibility (prioritize high-quality OGG)
            for ext in ['-hq.ogg', '-pygbag.ogg', '.ogg', '.wav']:
                filepath = os.path.join('assets/sounds', base_filename + ext)
                try:
                    if os.path.exists(filepath):
                        sound = pygame.mixer.Sound(filepath)
                        sound.set_volume(self.sfx_volume)
                        self.sounds[sound_name] = sound
                        print(f"Loaded sound: {sound_name} from {filepath}")
                        break
                except Exception as e:
                    continue
            
            # If no sound was loaded, set to None
            if sound_name not in self.sounds:
                print(f"Warning: Could not load sound {base_filename}")
                self.sounds[sound_name] = None
    
    def play_sound(self, sound_name, volume_override=None):
        """Play a sound effect"""
        if sound_name in self.sounds and self.sounds[sound_name]:
            sound = self.sounds[sound_name]
            if volume_override is not None:
                sound.set_volume(volume_override)
            else:
                sound.set_volume(self.sfx_volume)
            sound.play()
    
    def play_music(self, music_file=None):
        """Play background music (looping)"""
        if music_file is None:
            # Try high-quality version first, then fallback
            for music_path in ['assets/sounds/house_lo-hq.ogg', 'assets/sounds/house_lo-pygbag.ogg', 'assets/sounds/house_lo.ogg', 'assets/sounds/house_lo.wav']:
                if os.path.exists(music_path):
                    music_file = music_path
                    break
        
        try:
            pygame.mixer.music.load(music_file)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
            self.music_playing = True
            print(f"Playing music: {music_file}")
        except Exception as e:
            print(f"Warning: Could not load music {music_file}: {e}")
    
    def stop_music(self):
        """Stop background music"""
        pygame.mixer.music.stop()
        self.music_playing = False
    
    def pause_music(self):
        """Pause background music"""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause background music"""
        pygame.mixer.music.unpause()
    
    def set_sfx_volume(self, volume):
        """Set sound effects volume (0.0 to 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            if sound:
                sound.set_volume(self.sfx_volume)
    
    def set_music_volume(self, volume):
        """Set music volume (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
