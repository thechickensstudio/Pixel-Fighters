import pygame
import sys
import random
import asyncio
from player import Player
from game_platform import Platform
from character_select import CharacterSelect
from fruit import FruitManager
from traps import TrapManager, Fire, SpikeHead
from sound_manager import SoundManager

# Pre-initialize audio mixer with high-quality settings (must be BEFORE pygame.init())
# Larger buffer (8192) reduces crackling in web browsers
pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=8192)

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pixel Fighters")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = "character_select"  # character_select, playing, game_over
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Create enhanced background
        self.background = self.create_background()
        
        # Character selection
        self.character_select = CharacterSelect()
        
        # Game objects (initialized after character selection)
        self.player1 = None
        self.player2 = None
        self.platforms = []
        self.fruit_manager = None
    
    def create_background(self):
        """Create an enhanced background with gradient and tiled pattern"""
        # Create base surface
        background = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Create gradient sky (top to bottom)
        for y in range(SCREEN_HEIGHT):
            # Blend from light blue to darker blue
            ratio = y / SCREEN_HEIGHT
            r = int(135 * (1 - ratio * 0.3))
            g = int(206 * (1 - ratio * 0.2))
            b = int(235 * (1 - ratio * 0.1))
            pygame.draw.line(background, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Load and tile background pattern
        try:
            tile = pygame.image.load("assets/Background/Blue.png").convert_alpha()
            tile_width = tile.get_width()
            tile_height = tile.get_height()
            
            # Tile across the background with transparency
            tile.set_alpha(60)  # Make it subtle
            for x in range(0, SCREEN_WIDTH, tile_width):
                for y in range(0, SCREEN_HEIGHT, tile_height):
                    background.blit(tile, (x, y))
        except:
            pass
        
        # Add some clouds
        cloud_color = (255, 255, 255, 100)
        cloud_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        
        # Draw simple cloud shapes
        cloud_positions = [
            (200, 100, 80, 40),
            (500, 80, 100, 50),
            (800, 120, 90, 45),
            (1000, 90, 110, 55),
            (100, 180, 70, 35),
            (600, 200, 95, 48),
        ]
        
        for x, y, w, h in cloud_positions:
            pygame.draw.ellipse(cloud_surface, cloud_color, (x, y, w, h))
            pygame.draw.ellipse(cloud_surface, cloud_color, (x + 20, y - 10, w * 0.8, h * 0.8))
            pygame.draw.ellipse(cloud_surface, cloud_color, (x + w - 30, y - 5, w * 0.6, h * 0.7))
        
        background.blit(cloud_surface, (0, 0))
        
        return background
        
    def get_stage_layout(self, stage_num):
        """Get platform and trap layout for a specific stage"""
        if stage_num == 1:
            # Stage 1: Classic - STONE terrain (row 1 - actual gray/light stone)
            terrain_row = 1  # Light gray stone terrain
            platforms = [
                Platform(400, 550, 400, 16, terrain_row),  # Main platform
                Platform(100, 400, 200, 16, terrain_row),  # Left platform
                Platform(900, 400, 200, 16, terrain_row),  # Right platform
                Platform(500, 250, 200, 16, terrain_row),  # Top platform
            ]
            spawn_positions = [(450, 450), (700, 450)]
            traps = [
                Fire(420, 534),      # Left fire on main
                Fire(760, 534),      # Right fire on main
                SpikeHead(130, 348), # Left spike
                SpikeHead(980, 348), # Right spike
            ]
            
        elif stage_num == 2:
            # Stage 2: Tower - BRICK red/orange (row 4)
            terrain_row = 4  # Brick red/orange
            platforms = [
                Platform(200, 550, 300, 16, terrain_row),  # Left main platform at y=550
                Platform(700, 550, 300, 16, terrain_row),  # Right main platform at y=550
                Platform(450, 450, 300, 16, terrain_row),  # Middle platform at y=450
                Platform(300, 350, 200, 16, terrain_row),  # Left upper at y=350
                Platform(700, 350, 200, 16, terrain_row),  # Right upper at y=350
                Platform(500, 200, 200, 16, terrain_row),  # Top platform at y=200
            ]
            # Spawn on middle platform: y=450-32=418
            spawn_positions = [(500, 418), (650, 418)]  # Both on middle platform
            traps = [
                Fire(220, 534),      # Left bottom fire
                Fire(950, 534),      # Right bottom fire
                SpikeHead(500, 398), # Center spike
                SpikeHead(750, 334), # Right upper spike
            ]
            
        else:  # stage_num == 3
            # Stage 3: Gauntlet - CAVE STONE (row 8)
            terrain_row = 8  # Cave stone
            platforms = [
                Platform(100, 550, 200, 16, terrain_row),  # Far left: x=100-300, y=550-566
                Platform(350, 500, 150, 16, terrain_row),  # Left-mid: x=350-500, y=500-516
                Platform(550, 450, 150, 16, terrain_row),  # Center: x=550-700, y=450-466
                Platform(750, 500, 150, 16, terrain_row),  # Right-mid: x=750-900, y=500-516
                Platform(950, 550, 200, 16, terrain_row),  # Far right: x=950-1150, y=550-566
                Platform(400, 300, 400, 16, terrain_row),  # Top long: x=400-800, y=300-316
            ]
            # Spawn properly on platforms
            # Player 1: Far left platform center (x=200), top surface (y=550-32=518)
            # Player 2: At x=1100 (on far right platform), top surface (y=550-32=518)
            spawn_positions = [(200, 518), (1100, 518)]  # Player 2 on far right platform edge
            traps = [
                Fire(370, 484),      # Left-mid fire
                Fire(770, 484),      # Right-mid fire
                Fire(600, 284),      # Top center fire
                SpikeHead(120, 498), # Far left spike
                SpikeHead(1030, 498),# Far right spike
            ]
        
        return platforms, spawn_positions, traps
    
    def init_game(self, char1, char2):
        """Initialize the game with selected characters"""
        # Randomly select a stage (1, 2, or 3)
        self.current_stage = random.randint(1, 3)
        platforms, spawn_positions, traps = self.get_stage_layout(self.current_stage)
        
        # Create platforms
        self.platforms = platforms
        
        # Spawn players at stage-specific positions (pass sound manager)
        self.player1 = Player(spawn_positions[0][0], spawn_positions[0][1], char1, "player1", self.sound_manager)
        self.player2 = Player(spawn_positions[1][0], spawn_positions[1][1], char2, "player2", self.sound_manager)
        
        # Initialize fruit manager
        self.fruit_manager = FruitManager(self.sound_manager)
        
        # Initialize trap manager and add stage-specific traps
        self.trap_manager = TrapManager(self.sound_manager)
        for trap in traps:
            self.trap_manager.add_static_trap(trap)
        
        self.state = "playing"
        
        # Start background music
        self.sound_manager.play_music()
        
        print(f"Stage {self.current_stage} selected!")  # Debug info
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if self.state == "character_select":
                result = self.character_select.handle_event(event)
                if result:
                    char1, char2 = result
                    self.init_game(char1, char2)
            
            elif self.state == "playing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "character_select"
                        self.character_select.reset()
                        # Stop background music
                        self.sound_manager.stop_music()
                    
                    # Player 1 attack
                    if event.key == pygame.K_f:
                        self.player1.attack(self.player2)
                    
                    # Player 2 attack
                    if event.key == pygame.K_COMMA:
                        self.player2.attack(self.player1)
            
            elif self.state == "game_over":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        self.state = "character_select"
                        self.character_select.reset()
                        # Stop background music
                        self.sound_manager.stop_music()
    
    def update(self):
        if self.state == "playing":
            # Get keys for continuous input
            keys = pygame.key.get_pressed()
            
            # Player 1 controls (WASD)
            self.player1.handle_input(keys, pygame.K_a, pygame.K_d, pygame.K_w)
            
            # Player 2 controls (Arrow keys)
            self.player2.handle_input(keys, pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP)
            
            # Update players
            self.player1.update(self.platforms)
            self.player2.update(self.platforms)
            
            # Update fruits
            self.fruit_manager.update(self.platforms, self.player1, self.player2)
            
            # Update traps
            self.trap_manager.update(self.platforms, self.player1, self.player2)
            
            # Check if anyone reached 100% damage (instant death)
            if self.player1.damage >= 100 and not self.player1.just_died:
                self.player1.just_died = True
                self.player1.lives -= 1
                if self.player1.lives > 0:
                    self.player1.respawn(450, 100)
                    
            if self.player2.damage >= 100 and not self.player2.just_died:
                self.player2.just_died = True
                self.player2.lives -= 1
                if self.player2.lives > 0:
                    self.player2.respawn(700, 100)
            
            # Check if anyone is KO'd (fell off screen)
            if self.player1.y > SCREEN_HEIGHT + 100:
                # Play death sound
                self.sound_manager.play_sound('death', 0.5)
                self.player1.lives -= 1
                if self.player1.lives > 0:
                    self.player1.respawn(200, 100)
                else:
                    self.state = "game_over"
                    self.winner = "Player 2"
                    self.sound_manager.stop_music()
            
            if self.player2.y > SCREEN_HEIGHT + 100:
                # Play death sound
                self.sound_manager.play_sound('death', 0.5)
                self.player2.lives -= 1
                if self.player2.lives > 0:
                    self.player2.respawn(900, 100)
                else:
                    self.state = "game_over"
                    self.winner = "Player 1"
                    self.sound_manager.stop_music()
            
            # Check if anyone ran out of lives (from traps or other deaths)
            if self.player1.lives <= 0:
                self.state = "game_over"
                self.winner = "Player 2"
            elif self.player2.lives <= 0:
                self.state = "game_over"
                self.winner = "Player 1"
    
    def draw(self):
        if self.state == "character_select":
            self.character_select.draw(self.screen)
        
        elif self.state == "playing":
            # Draw background
            self.screen.blit(self.background, (0, 0))
            
            # Draw platforms
            for platform in self.platforms:
                platform.draw(self.screen)
            
            # Draw traps (behind players)
            self.trap_manager.draw(self.screen)
            
            # Draw fruits
            self.fruit_manager.draw(self.screen)
            
            # Draw players
            self.player1.draw(self.screen)
            self.player2.draw(self.screen)
            
            # Draw UI
            self.draw_ui()
        
        elif self.state == "game_over":
            self.screen.fill(BLACK)
            font = pygame.font.Font(None, 74)
            text = font.render(f"{self.winner} Wins!", True, WHITE)
            text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50))
            self.screen.blit(text, text_rect)
            
            font_small = pygame.font.Font(None, 36)
            restart_text = font_small.render("Press ENTER to return to character select", True, WHITE)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def draw_ui(self):
        font = pygame.font.Font(None, 36)
        
        # Player 1 info (top left)
        p1_text = font.render(f"P1: {self.player1.damage}%", True, RED)
        lives1_text = font.render(f"Lives: {self.player1.lives}", True, RED)
        self.screen.blit(p1_text, (20, 20))
        self.screen.blit(lives1_text, (20, 55))
        
        # Player 1 power-up status
        if self.player1.powered_up:
            font_powerup = pygame.font.Font(None, 28)
            powerup_time = self.player1.powerup_timer // 60  # Convert frames to seconds
            powerup_text = font_powerup.render(f"POWER UP! {powerup_time}s", True, (255, 215, 0))
            self.screen.blit(powerup_text, (20, 90))
        
        # Player 2 info (top right)
        p2_text = font.render(f"P2: {self.player2.damage}%", True, BLUE)
        lives2_text = font.render(f"Lives: {self.player2.lives}", True, BLUE)
        self.screen.blit(p2_text, (SCREEN_WIDTH - 150, 20))
        self.screen.blit(lives2_text, (SCREEN_WIDTH - 150, 55))
        
        # Player 2 power-up status
        if self.player2.powered_up:
            font_powerup = pygame.font.Font(None, 28)
            powerup_time = self.player2.powerup_timer // 60  # Convert frames to seconds
            powerup_text = font_powerup.render(f"POWER UP! {powerup_time}s", True, (255, 215, 0))
            self.screen.blit(powerup_text, (SCREEN_WIDTH - 210, 90))
        
        # Controls hint
        font_small = pygame.font.Font(None, 20)
        hint = font_small.render("P1: WASD + F to attack | P2: Arrows + , to attack | ESC: Menu", True, WHITE)
        self.screen.blit(hint, (SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT - 30))
    
    async def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            await asyncio.sleep(0)  # Yield control for web compatibility
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    asyncio.run(game.run())
