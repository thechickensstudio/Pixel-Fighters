import pygame
import random
import os

class Fruit:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 32
        self.height = 32
        self.vel_y = 0
        self.gravity = 0.5
        self.collected = False
        
        # Choose random fruit
        self.fruit_types = [
            "Apple.png",
            "Bananas.png", 
            "Cherries.png",
            "Kiwi.png",
            "Melon.png",
            "Orange.png",
            "Pineapple.png",
            "Strawberry.png"
        ]
        
        self.fruit_type = random.choice(self.fruit_types)
        
        # Animation
        self.animation_frames = []
        self.animation_frame = 0
        self.animation_speed = 0.2
        self.load_fruit_animation()
        
        # Load collected animation
        self.collected_frames = []
        self.load_collected_animation()
        
        # Animation for collected effect
        self.collected_timer = 0
        self.collected_duration = 30  # frames
    
    def load_fruit_animation(self):
        """Load fruit sprite animation"""
        try:
            fruit_path = f"assets/Items/Fruits/{self.fruit_type}"
            sprite_sheet = pygame.image.load(fruit_path).convert_alpha()
            
            # Split sprite sheet into frames (17 frames of 32x32)
            sheet_width = sprite_sheet.get_width()
            frame_width = 32
            num_frames = sheet_width // frame_width
            
            for i in range(num_frames):
                frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, 32))
                self.animation_frames.append(frame)
        except Exception as e:
            print(f"Error loading fruit animation: {e}")
            # Fallback: create a colored circle
            fallback = pygame.Surface((32, 32), pygame.SRCALPHA)
            pygame.draw.circle(fallback, (255, 100, 100), (16, 16), 12)
            self.animation_frames = [fallback]
    
    def load_collected_animation(self):
        """Load collected effect animation"""
        try:
            collected_path = "assets/Items/Fruits/Collected.png"
            sprite_sheet = pygame.image.load(collected_path).convert_alpha()
            
            # Split collected sprite sheet into frames
            sheet_width = sprite_sheet.get_width()
            frame_width = 32
            num_frames = sheet_width // frame_width
            
            for i in range(num_frames):
                frame = sprite_sheet.subsurface((i * frame_width, 0, frame_width, 32))
                self.collected_frames.append(frame)
        except Exception as e:
            print(f"Error loading collected animation: {e}")
            self.collected_frames = []
        
    def update(self, platforms):
        """Update fruit physics"""
        if self.collected:
            self.collected_timer += 1
            # Float upward when collected
            self.y -= 2
            # Animate collected effect
            if self.collected_frames:
                self.animation_frame += self.animation_speed * 1.5
            return self.collected_timer >= self.collected_duration
        
        # Apply gravity
        self.vel_y += self.gravity
        self.vel_y = min(self.vel_y, 15)
        
        # Update position
        self.y += self.vel_y
        
        # Update animation
        if self.animation_frames:
            self.animation_frame += self.animation_speed
            if self.animation_frame >= len(self.animation_frames):
                self.animation_frame = 0
        
        # Check platform collision
        for platform in platforms:
            if self.check_platform_collision(platform):
                break
        
        # Remove if off screen
        return self.y > 800
    
    def check_platform_collision(self, platform):
        """Check collision with platform"""
        if self.vel_y > 0:
            if (self.x + self.width > platform.x and 
                self.x < platform.x + platform.width):
                if (self.y + self.height > platform.y and 
                    self.y + self.height < platform.y + platform.height + 10):
                    self.y = platform.y - self.height
                    self.vel_y = 0
                    return True
        return False
    
    def check_player_collision(self, player):
        """Check if player collects the fruit"""
        if self.collected:
            return False
        
        # Simple bounding box collision
        if (self.x < player.x + player.width and
            self.x + self.width > player.x and
            self.y < player.y + player.height and
            self.y + self.height > player.y):
            self.collected = True
            return True
        
        return False
    
    def draw(self, screen):
        """Draw the fruit with animation"""
        if self.collected and self.collected_frames:
            # Draw collected animation with fading
            frame_index = int(self.animation_frame) % len(self.collected_frames)
            image = self.collected_frames[frame_index].copy()
            alpha = int(255 * (1 - self.collected_timer / self.collected_duration))
            image.set_alpha(alpha)
            screen.blit(image, (int(self.x), int(self.y)))
        elif self.animation_frames:
            # Draw normal fruit animation
            frame_index = int(self.animation_frame) % len(self.animation_frames)
            screen.blit(self.animation_frames[frame_index], (int(self.x), int(self.y)))


class FruitManager:
    def __init__(self, sound_manager=None):
        self.fruits = []
        self.spawn_timer = 0
        self.min_spawn_interval = 180  # 3 seconds at 60 FPS
        self.max_spawn_interval = 420  # 7 seconds at 60 FPS
        self.next_spawn = random.randint(self.min_spawn_interval, self.max_spawn_interval)
        self.sound_manager = sound_manager
        
    def update(self, platforms, player1, player2):
        """Update all fruits and handle spawning"""
        # Spawn new fruits
        self.spawn_timer += 1
        if self.spawn_timer >= self.next_spawn:
            self.spawn_fruit()
            self.spawn_timer = 0
            self.next_spawn = random.randint(self.min_spawn_interval, self.max_spawn_interval)
        
        # Update existing fruits
        fruits_to_remove = []
        for fruit in self.fruits:
            # Update physics
            should_remove = fruit.update(platforms)
            
            # Check player collision
            if fruit.check_player_collision(player1):
                # Play collect sound
                if self.sound_manager:
                    self.sound_manager.play_sound('collect_fruit', 0.4)
                player1.activate_powerup()
            elif fruit.check_player_collision(player2):
                # Play collect sound
                if self.sound_manager:
                    self.sound_manager.play_sound('collect_fruit', 0.4)
                player2.activate_powerup()
            
            # Mark for removal if off screen or animation done
            if should_remove:
                fruits_to_remove.append(fruit)
        
        # Remove fruits
        for fruit in fruits_to_remove:
            self.fruits.remove(fruit)
    
    def spawn_fruit(self):
        """Spawn a new fruit at random x position"""
        x = random.randint(50, 1150)
        y = -50  # Spawn above screen
        fruit = Fruit(x, y)
        self.fruits.append(fruit)
    
    def draw(self, screen):
        """Draw all fruits"""
        for fruit in self.fruits:
            fruit.draw(screen)
    
    def reset(self):
        """Clear all fruits"""
        self.fruits.clear()
        self.spawn_timer = 0
        self.next_spawn = random.randint(self.min_spawn_interval, self.max_spawn_interval)
