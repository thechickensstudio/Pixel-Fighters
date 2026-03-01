import pygame
import os

class Player:
    def __init__(self, x, y, character, player_id, sound_manager=None):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.character = character
        self.player_id = player_id
        self.sound_manager = sound_manager
        
        # Physics
        self.vel_x = 0
        self.vel_y = 0
        self.speed = 5
        self.jump_power = 18  # Increased from original 15
        self.gravity = 0.8
        self.max_fall_speed = 20
        self.air_mobility = 0.3
        self.ground_friction = 0.8
        self.air_resistance = 0.95
        
        # Combat
        self.damage = 0
        self.lives = 3
        self.is_attacking = False
        self.attack_cooldown = 0
        self.attack_duration = 15
        self.attack_range = 50
        self.hitstun = 0
        self.invincible = 0
        self.just_died = False  # Prevent repeated trap deaths
        
        # Power-up system
        self.powered_up = False
        self.powerup_timer = 0
        self.powerup_duration = 600  # 10 seconds at 60 FPS
        self.powerup_multiplier = 2.0  # Double damage when powered up
        
        # State
        self.on_ground = False
        self.ground_frames = 0  # Counter for how many frames on ground (prevents flickering)
        self.facing_right = True
        self.can_jump = True
        self.has_double_jump = True
        
        # Animation
        self.animations = {}
        self.idle_sprite = None  # Separate static sprite for idle (NOT an animation)
        self.current_animation = "run"  # Start with run (will switch based on movement)
        self.animation_frame = 0
        self.animation_speed = 0.15  # Base speed, overridden per animation in update_animation()
        self.load_animations()
        
    def load_animations(self):
        """Load all sprite animations for the character"""
        character_path = f"assets/Main Characters/{self.character}"
        
        # Load idle animation - simple continuous loop like traps
        idle_path = os.path.join(character_path, "Idle (32x32).png")
        self.idle_frames = []
        if os.path.exists(idle_path):
            sprite_sheet = pygame.image.load(idle_path).convert_alpha()
            # Load all idle frames
            frames = self.split_sprite_sheet(sprite_sheet, 32, 32)
            self.idle_frames = frames
        else:
            # Fallback: create a simple rectangle
            fallback = pygame.Surface((32, 32))
            fallback.fill((100, 100, 100))
            self.idle_frames = [fallback]
        
        # Idle animation state (separate from other animations)
        self.idle_animation_frame = 0.0
        self.idle_animation_speed = 0.12  # Medium speed idle (11 frames in ~1.5 seconds)
        
        # Load all OTHER animations (not idle)
        animation_files = {
            "run": "Run (32x32).png",
            "jump": "Jump (32x32).png",
            "fall": "Fall (32x32).png",
            "hit": "Hit (32x32).png",
            "double_jump": "Double Jump (32x32).png",
        }
        
        for anim_name, filename in animation_files.items():
            filepath = os.path.join(character_path, filename)
            if os.path.exists(filepath):
                sprite_sheet = pygame.image.load(filepath).convert_alpha()
                frames = self.split_sprite_sheet(sprite_sheet, 32, 32)
                self.animations[anim_name] = frames
            else:
                self.animations[anim_name] = []
    
    def split_sprite_sheet(self, sprite_sheet, frame_width, frame_height):
        """Split a sprite sheet into individual frames"""
        frames = []
        sheet_width = sprite_sheet.get_width()
        sheet_height = sprite_sheet.get_height()
        
        for y in range(0, sheet_height, frame_height):
            for x in range(0, sheet_width, frame_width):
                frame = sprite_sheet.subsurface((x, y, frame_width, frame_height))
                frames.append(frame)
        
        return frames
    
    def handle_input(self, keys, left_key, right_key, jump_key):
        """Handle player input"""
        if self.hitstun > 0:
            return  # Can't control during hitstun
        
        # Horizontal movement
        if keys[left_key]:
            if self.on_ground:
                self.vel_x = -self.speed
            else:
                self.vel_x -= self.air_mobility
                self.vel_x = max(self.vel_x, -self.speed)
            self.facing_right = False
            
        elif keys[right_key]:
            if self.on_ground:
                self.vel_x = self.speed
            else:
                self.vel_x += self.air_mobility
                self.vel_x = min(self.vel_x, self.speed)
            self.facing_right = True
        
        else:
            # Apply friction
            if self.on_ground:
                self.vel_x *= self.ground_friction
            else:
                self.vel_x *= self.air_resistance
        
        # Jumping (simple and responsive)
        if keys[jump_key]:
            if self.can_jump and self.on_ground:
                self.vel_y = -self.jump_power
                self.on_ground = False
                self.can_jump = False
                self.current_animation = "jump"
                # Play jump sound
                if self.sound_manager:
                    self.sound_manager.play_sound('jump', 0.3)
            elif self.has_double_jump and not self.on_ground and not self.can_jump:
                self.vel_y = -self.jump_power
                self.has_double_jump = False
                self.current_animation = "double_jump"
                # Play jump sound
                if self.sound_manager:
                    self.sound_manager.play_sound('jump', 0.3)
        else:
            self.can_jump = True
    
    def update(self, platforms):
        """Update player physics and state"""
        # Update idle animation continuously (like traps do)
        self.idle_animation_frame += self.idle_animation_speed
        if self.idle_animation_frame >= len(self.idle_frames):
            self.idle_animation_frame = 0
        
        # Update timers
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.hitstun > 0:
            self.hitstun -= 1
        if self.invincible > 0:
            self.invincible -= 1
        
        # Update power-up timer
        if self.powerup_timer > 0:
            self.powerup_timer -= 1
            if self.powerup_timer == 0:
                self.powered_up = False
        
        # Apply gravity
        if not self.on_ground:
            self.vel_y += self.gravity
            self.vel_y = min(self.vel_y, self.max_fall_speed)
        
        # Update position
        self.x += self.vel_x
        self.y += self.vel_y
        
        # Platform collision
        collision_found = False
        for platform in platforms:
            if self.check_platform_collision(platform):
                collision_found = True
                self.has_double_jump = True
                break
        
        # Use ground_frames counter to prevent flickering
        # Give 3 frames of grace period when leaving ground
        if collision_found:
            self.ground_frames = 3
            self.on_ground = True
        else:
            if self.ground_frames > 0:
                self.ground_frames -= 1
                self.on_ground = True  # Still consider on ground for grace period
            else:
                self.on_ground = False
        
        # Update animation
        self.update_animation()
        
        # Screen bounds (left and right)
        if self.x < 0:
            self.x = 0
            self.vel_x = 0
        elif self.x > 1200 - self.width:
            self.x = 1200 - self.width
            self.vel_x = 0
    
    def check_platform_collision(self, platform):
        """Check and resolve collision with a platform"""
        # Check if player is falling onto platform OR standing on it
        if self.vel_y >= 0:
            # Check horizontal overlap
            if (self.x + self.width > platform.x and 
                self.x < platform.x + platform.width):
                # Check if player's bottom is near platform top
                # Increased tolerance from 10 to 20 to prevent flickering
                if (self.y + self.height >= platform.y - 2 and 
                    self.y + self.height <= platform.y + platform.height + 20):
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    return True
        return False
    
    def update_animation(self):
        """Update animation state and frame"""
        # Determine animation based on state
        if self.is_attacking:
            self.current_animation = "hit"
        elif self.hitstun > 0:
            self.current_animation = "hit"
        elif not self.on_ground:
            if self.vel_y < 0:
                # Don't override double jump animation immediately
                if self.current_animation != "double_jump" or self.animation_frame >= len(self.animations.get("double_jump", [])) - 1:
                    self.current_animation = "jump"
            else:
                self.current_animation = "fall"
        elif abs(self.vel_x) > 1.0:
            self.current_animation = "run"
        else:
            self.current_animation = "idle"
            # Stop completely when idle
            if abs(self.vel_x) < 0.1:
                self.vel_x = 0
        
        # Idle animation is handled separately (continuously updated in update())
        # Skip frame updates for idle here
        if self.current_animation == "idle":
            return
        
        # Update frame with animation-specific speeds for actual animations
        if self.current_animation in self.animations and self.animations[self.current_animation]:
            anim_speed = self.animation_speed
            if self.current_animation == "run":
                anim_speed = 0.2   # Faster for running
            elif self.current_animation == "hit":
                anim_speed = 0.25  # Fast for attack
            
            self.animation_frame += anim_speed
            
            if self.animation_frame >= len(self.animations[self.current_animation]):
                self.animation_frame = 0
                if self.is_attacking:
                    self.is_attacking = False
    
    def attack(self, other_player):
        """Perform an attack"""
        if self.attack_cooldown > 0 or self.hitstun > 0:
            return
        
        self.is_attacking = True
        self.attack_cooldown = self.attack_duration
        self.animation_frame = 0
        
        # Play attack sound
        if self.sound_manager:
            self.sound_manager.play_sound('attack', 0.4)
        
        # Check if attack hits
        distance = abs(self.x - other_player.x)
        y_diff = abs(self.y - other_player.y)
        
        # Check if in range and facing the right direction
        in_range = distance < self.attack_range and y_diff < 50
        facing_correct = (self.facing_right and self.x < other_player.x) or \
                        (not self.facing_right and self.x > other_player.x)
        
        if in_range and facing_correct and other_player.invincible == 0:
            # Play hit sound
            if self.sound_manager:
                self.sound_manager.play_sound('hit', 0.5)
            
            # Apply damage (doubled if powered up)
            damage_dealt = 10
            if self.powered_up:
                damage_dealt *= self.powerup_multiplier
            other_player.damage += damage_dealt
            
            # Apply knockback based on damage (increased if powered up)
            knockback_multiplier = 1 + (other_player.damage / 100)
            if self.powered_up:
                knockback_multiplier *= 1.5
            knockback_x = 8 * knockback_multiplier
            knockback_y = -6 * knockback_multiplier
            
            if self.facing_right:
                other_player.vel_x = knockback_x
            else:
                other_player.vel_x = -knockback_x
            
            other_player.vel_y = knockback_y
            other_player.hitstun = 20
    
    def activate_powerup(self):
        """Activate fruit power-up"""
        self.powered_up = True
        self.powerup_timer = self.powerup_duration
        # Play powerup sound
        if self.sound_manager:
            self.sound_manager.play_sound('powerup', 0.5)
    
    def hit_by_trap(self):
        """Player hit by a trap - instant death (lose a life)"""
        if self.invincible > 0 or self.just_died:
            return  # Don't die if invincible or already just died
        
        # Play trap hit sound
        if self.sound_manager:
            self.sound_manager.play_sound('trap_hit', 0.6)
        
        # Mark as just died to prevent repeated deaths
        self.just_died = True
        
        # Lose a life immediately
        self.lives -= 1
        
        # Respawn if has lives left
        if self.lives > 0:
            respawn_x = 200 if self.player_id == "player1" else 900
            self.respawn(respawn_x, 100)
        # If no lives left, game over will be handled by main game loop
    
    def respawn(self, x, y):
        """Respawn the player at a location"""
        self.x = x
        self.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.damage = 0
        self.hitstun = 0
        self.invincible = 120  # 2 seconds of invincibility
        self.has_double_jump = True
        self.just_died = False  # Reset death flag after respawn
        # Keep power-up through respawn
    
    def draw(self, screen):
        """Draw the player"""
        # Handle idle with simple continuous animation like traps
        if self.current_animation == "idle":
            if self.idle_frames:
                # Get current idle frame - simple continuous loop
                frame_index = int(self.idle_animation_frame) % len(self.idle_frames)
                image = self.idle_frames[frame_index]
                
                # Flip if facing left
                if not self.facing_right:
                    image = pygame.transform.flip(image, True, False)
                
                # Flash white when invincible
                if self.invincible > 0 and (self.invincible // 5) % 2 == 0:
                    image = image.copy()
                    image.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_ADD)
                
                # Glow effect when powered up
                if self.powered_up:
                    image = image.copy()
                    # Pulsing glow effect
                    glow_intensity = int(100 + 50 * abs((self.powerup_timer % 60) / 30 - 1))
                    image.fill((255, 215, 0, glow_intensity), special_flags=pygame.BLEND_RGBA_ADD)
                
                screen.blit(image, (int(self.x), int(self.y)))
                return
        
        # Handle all other animations normally
        if self.current_animation in self.animations and self.animations[self.current_animation]:
            frames = self.animations[self.current_animation]
            frame_index = int(self.animation_frame) % len(frames)
            image = frames[frame_index]
            
            # Flip if facing left
            if not self.facing_right:
                image = pygame.transform.flip(image, True, False)
            
            # Flash white when invincible
            if self.invincible > 0 and (self.invincible // 5) % 2 == 0:
                image = image.copy()
                image.fill((255, 255, 255, 128), special_flags=pygame.BLEND_RGBA_ADD)
            
            # Glow effect when powered up
            if self.powered_up:
                image = image.copy()
                # Pulsing glow effect
                glow_intensity = int(100 + 50 * abs((self.powerup_timer % 60) / 30 - 1))
                image.fill((255, 215, 0, glow_intensity), special_flags=pygame.BLEND_RGBA_ADD)
            
            screen.blit(image, (int(self.x), int(self.y)))
        else:
            # Fallback: draw a colored rectangle
            color = (255, 0, 0) if self.player_id == "player1" else (0, 0, 255)
            pygame.draw.rect(screen, color, (int(self.x), int(self.y), self.width, self.height))
        
        # Draw attack hitbox when attacking (for debugging)
        # if self.is_attacking:
        #     hitbox_x = self.x + self.width if self.facing_right else self.x - self.attack_range
        #     pygame.draw.rect(screen, (255, 255, 0), (hitbox_x, self.y, self.attack_range, self.height), 2)
