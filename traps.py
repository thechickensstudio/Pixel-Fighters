import pygame
import random
import os

class Trap:
    """Base class for traps"""
    def __init__(self, x, y, trap_type):
        self.x = x
        self.y = y
        self.trap_type = trap_type
        self.animation_frames = []
        self.animation_frame = 0
        self.animation_speed = 0.15
        self.width = 32
        self.height = 32
        self.active = True
        
    def load_animation(self, sprite_path, frame_width, frame_height):
        """Load sprite sheet animation"""
        try:
            sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
            sheet_width = sprite_sheet.get_width()
            num_frames = sheet_width // frame_width
            
            for i in range(num_frames):
                frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
                self.animation_frames.append(frame)
            
            self.width = frame_width
            self.height = frame_height
        except Exception as e:
            print(f"Error loading trap animation: {e}")
            # Fallback
            fallback = pygame.Surface((frame_width, frame_height), pygame.SRCALPHA)
            pygame.draw.rect(fallback, (255, 0, 0), (0, 0, frame_width, frame_height))
            self.animation_frames = [fallback]
    
    def update(self):
        """Update animation"""
        if self.animation_frames:
            self.animation_frame += self.animation_speed
            if self.animation_frame >= len(self.animation_frames):
                self.animation_frame = 0
    
    def check_collision(self, player):
        """Check if player touches the trap"""
        if not self.active:
            return False
        
        # Bounding box collision
        if (self.x < player.x + player.width and
            self.x + self.width > player.x and
            self.y < player.y + player.height and
            self.y + self.height > player.y):
            return True
        return False
    
    def draw(self, screen):
        """Draw the trap"""
        if self.animation_frames and self.active:
            frame_index = int(self.animation_frame) % len(self.animation_frames)
            screen.blit(self.animation_frames[frame_index], (int(self.x), int(self.y)))


class Fire(Trap):
    """Fire trap - stationary, deals 10% damage"""
    def __init__(self, x, y):
        super().__init__(x, y, "fire")
        self.load_animation("assets/Traps/Fire/On (16x32).png", 16, 32)
        self.animation_speed = 0.2
        self.damage_cooldown = {}  # Track damage cooldown per player


class SpikeHead(Trap):
    """Spike head trap - stationary with blinking animation"""
    def __init__(self, x, y):
        super().__init__(x, y, "spike_head")
        self.load_animation("assets/Traps/Spike Head/Blink (54x52).png", 54, 52)
        self.animation_speed = 0.1


class RockHead(Trap):
    """Rock head trap - falls from the sky, kills only when falling on head"""
    def __init__(self, x, y):
        super().__init__(x, y, "rock_head")
        self.load_animation("assets/Traps/Rock Head/Blink (42x42).png", 42, 42)
        self.animation_speed = 0.15
        
        # Physics for falling
        self.vel_y = 0
        self.gravity = 0.5
        self.max_fall_speed = 12
        self.is_falling = True
        self.hit_ground = False
        self.can_be_platform = False  # Becomes platform after landing
        
    def update(self):
        """Update rock head physics and animation"""
        super().update()
        
        if self.is_falling:
            # Apply gravity
            self.vel_y += self.gravity
            self.vel_y = min(self.vel_y, self.max_fall_speed)
            
            # Update position
            self.y += self.vel_y
            
            # Check if off screen (remove)
            if self.y > 800:
                self.active = False
    
    def check_platform_collision(self, platforms):
        """Check if rock head hits a platform"""
        if self.hit_ground:
            return
        
        for platform in platforms:
            if self.vel_y > 0:
                if (self.x + self.width > platform.x and 
                    self.x < platform.x + platform.width):
                    if (self.y + self.height > platform.y and 
                        self.y + self.height < platform.y + platform.height + 10):
                        self.y = platform.y - self.height
                        self.vel_y = 0
                        self.is_falling = False
                        self.hit_ground = True
                        self.can_be_platform = True  # Now players can land on it
                        break
    
    def check_player_landing(self, player):
        """Check if player is landing on top of the rock head (after it landed)"""
        if not self.can_be_platform:
            return False
        
        # Only allow landing from above when player is falling
        if player.vel_y > 0:
            # Check if player's feet are near rock head's top
            if (player.x + player.width > self.x and 
                player.x < self.x + self.width):
                if (player.y + player.height > self.y and 
                    player.y + player.height < self.y + 15):
                    player.y = self.y - player.height
                    player.vel_y = 0
                    player.on_ground = True
                    player.ground_frames = 3  # Reset grace period counter
                    player.has_double_jump = True
                    return True
        return False
    
    def check_deadly_collision(self, player):
        """Check if falling rock hits player on the head (instant death)"""
        if not self.is_falling:
            return False  # Not deadly once landed
        
        # Check if rock is falling onto player's head (top half of player)
        if (self.x < player.x + player.width and
            self.x + self.width > player.x and
            self.y + self.height > player.y and
            self.y < player.y + player.height / 2):  # Only top half counts as "head"
            return True
        return False


class TrapManager:
    """Manages all traps in the game"""
    def __init__(self, sound_manager=None):
        self.static_traps = []  # Fire and spike heads
        self.falling_traps = []  # Rock heads
        self.sound_manager = sound_manager
        
        # Rock head spawning
        self.rock_spawn_timer = 0
        self.min_rock_interval = 240  # 4 seconds
        self.max_rock_interval = 480  # 8 seconds
        self.next_rock_spawn = random.randint(self.min_rock_interval, self.max_rock_interval)
    
    def add_static_trap(self, trap):
        """Add a fire or spike head trap"""
        self.static_traps.append(trap)
    
    def spawn_rock_head(self):
        """Spawn a rock head at random position"""
        x = random.randint(100, 1100)
        y = -50  # Above screen
        rock = RockHead(x, y)
        self.falling_traps.append(rock)
    
    def update(self, platforms, player1, player2):
        """Update all traps"""
        # Update static traps with different damage types
        for trap in self.static_traps:
            trap.update()
            
            # Check collision with players
            if trap.check_collision(player1):
                if isinstance(trap, Fire):
                    # Fire deals 10% damage with cooldown
                    player_id = id(player1)
                    if player_id not in trap.damage_cooldown or trap.damage_cooldown[player_id] <= 0:
                        player1.damage += 10
                        trap.damage_cooldown[player_id] = 60  # 1 second cooldown
                elif isinstance(trap, SpikeHead):
                    # Spike head kills instantly
                    player1.hit_by_trap()
            
            if trap.check_collision(player2):
                if isinstance(trap, Fire):
                    # Fire deals 10% damage with cooldown
                    player_id = id(player2)
                    if player_id not in trap.damage_cooldown or trap.damage_cooldown[player_id] <= 0:
                        player2.damage += 10
                        trap.damage_cooldown[player_id] = 60  # 1 second cooldown
                elif isinstance(trap, SpikeHead):
                    # Spike head kills instantly
                    player2.hit_by_trap()
            
            # Update fire damage cooldowns
            if isinstance(trap, Fire):
                for player_id in list(trap.damage_cooldown.keys()):
                    if trap.damage_cooldown[player_id] > 0:
                        trap.damage_cooldown[player_id] -= 1
        
        # Spawn rock heads
        self.rock_spawn_timer += 1
        if self.rock_spawn_timer >= self.next_rock_spawn:
            self.spawn_rock_head()
            self.rock_spawn_timer = 0
            self.next_rock_spawn = random.randint(self.min_rock_interval, self.max_rock_interval)
        
        # Update falling rock heads
        rocks_to_remove = []
        for rock in self.falling_traps:
            rock.update()
            rock.check_platform_collision(platforms)
            
            # Check if rock can be used as platform (after landing)
            if rock.can_be_platform:
                rock.check_player_landing(player1)
                rock.check_player_landing(player2)
            
            # Check deadly collision (only when falling)
            if rock.check_deadly_collision(player1):
                player1.hit_by_trap()
                # Rock continues to fall/land
            
            if rock.check_deadly_collision(player2):
                player2.hit_by_trap()
                # Rock continues to fall/land
            
            # Remove if inactive
            if not rock.active:
                rocks_to_remove.append(rock)
        
        # Remove inactive rocks
        for rock in rocks_to_remove:
            if rock in self.falling_traps:
                self.falling_traps.remove(rock)
    
    def draw(self, screen):
        """Draw all traps"""
        # Draw static traps
        for trap in self.static_traps:
            trap.draw(screen)
        
        # Draw falling rock heads
        for rock in self.falling_traps:
            rock.draw(screen)
    
    def reset(self):
        """Reset all traps"""
        self.falling_traps.clear()
        self.rock_spawn_timer = 0
        self.next_rock_spawn = random.randint(self.min_rock_interval, self.max_rock_interval)
