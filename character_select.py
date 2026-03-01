import pygame
import os

class CharacterSelect:
    def __init__(self):
        self.characters = ["Mask Dude", "Ninja Frog", "Pink Man", "Virtual Guy"]
        self.character_previews = {}
        self.load_previews()
        
        # Selection state
        self.player1_selected = None
        self.player2_selected = None
        self.player1_index = 0
        self.player2_index = 1
        
        # UI
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Colors
        self.bg_color = (20, 20, 40)
        self.p1_color = (255, 100, 100)
        self.p2_color = (100, 100, 255)
        self.white = (255, 255, 255)
        self.gray = (150, 150, 150)
    
    def load_previews(self):
        """Load preview images for each character"""
        for char in self.characters:
            try:
                # Load idle animation as preview
                preview_path = f"assets/Main Characters/{char}/Idle (32x32).png"
                if os.path.exists(preview_path):
                    sprite_sheet = pygame.image.load(preview_path).convert_alpha()
                    # Get first frame
                    frame = sprite_sheet.subsurface((0, 0, 32, 32))
                    # Scale up for display
                    frame = pygame.transform.scale(frame, (128, 128))
                    self.character_previews[char] = frame
            except Exception as e:
                print(f"Error loading preview for {char}: {e}")
                # Create placeholder
                placeholder = pygame.Surface((128, 128))
                placeholder.fill((100, 100, 100))
                self.character_previews[char] = placeholder
    
    def handle_event(self, event):
        """Handle input events, returns (char1, char2) when both players ready"""
        if event.type == pygame.KEYDOWN:
            # Player 1 controls (A/D to navigate, W to confirm)
            if self.player1_selected is None:
                if event.key == pygame.K_a:
                    self.player1_index = (self.player1_index - 1) % len(self.characters)
                elif event.key == pygame.K_d:
                    self.player1_index = (self.player1_index + 1) % len(self.characters)
                elif event.key == pygame.K_w:
                    self.player1_selected = self.characters[self.player1_index]
            
            # Player 2 controls (Arrow keys to navigate, Up to confirm)
            if self.player2_selected is None:
                if event.key == pygame.K_LEFT:
                    self.player2_index = (self.player2_index - 1) % len(self.characters)
                elif event.key == pygame.K_RIGHT:
                    self.player2_index = (self.player2_index + 1) % len(self.characters)
                elif event.key == pygame.K_UP:
                    self.player2_selected = self.characters[self.player2_index]
            
            # Both players ready
            if self.player1_selected and self.player2_selected:
                return (self.player1_selected, self.player2_selected)
        
        return None
    
    def reset(self):
        """Reset selection state"""
        self.player1_selected = None
        self.player2_selected = None
        self.player1_index = 0
        self.player2_index = 1
    
    def draw(self, screen):
        """Draw character selection screen"""
        screen.fill(self.bg_color)
        
        # Title
        title = self.font_large.render("CHARACTER SELECT", True, self.white)
        title_rect = title.get_rect(center=(600, 80))
        screen.blit(title, title_rect)
        
        # Instructions
        inst1 = self.font_small.render("P1: A/D to move, W to select", True, self.p1_color)
        inst2 = self.font_small.render("P2: Arrows to move, UP to select", True, self.p2_color)
        screen.blit(inst1, (50, 620))
        screen.blit(inst2, (50, 650))
        
        # Character boxes
        box_width = 200
        box_height = 250
        spacing = 50
        start_x = (1200 - (box_width * len(self.characters) + spacing * (len(self.characters) - 1))) // 2
        y_pos = 250
        
        for i, char in enumerate(self.characters):
            x_pos = start_x + i * (box_width + spacing)
            
            # Determine box color based on selection
            p1_selecting = (i == self.player1_index and self.player1_selected is None)
            p2_selecting = (i == self.player2_index and self.player2_selected is None)
            p1_locked = (self.player1_selected == char)
            p2_locked = (self.player2_selected == char)
            
            # Draw box background
            box_color = self.gray
            if p1_locked:
                box_color = self.p1_color
            elif p2_locked:
                box_color = self.p2_color
            
            pygame.draw.rect(screen, box_color, (x_pos, y_pos, box_width, box_height), 3)
            
            # Draw selection indicator
            if p1_selecting:
                pygame.draw.rect(screen, self.p1_color, (x_pos - 5, y_pos - 5, box_width + 10, box_height + 10), 5)
            if p2_selecting:
                pygame.draw.rect(screen, self.p2_color, (x_pos - 10, y_pos - 10, box_width + 20, box_height + 20), 5)
            
            # Draw character preview
            if char in self.character_previews:
                preview = self.character_previews[char]
                preview_rect = preview.get_rect(center=(x_pos + box_width // 2, y_pos + 80))
                screen.blit(preview, preview_rect)
            
            # Draw character name
            name_text = self.font_small.render(char, True, self.white)
            name_rect = name_text.get_rect(center=(x_pos + box_width // 2, y_pos + 200))
            screen.blit(name_text, name_rect)
        
        # Ready status
        ready_y = 150
        if self.player1_selected:
            p1_ready = self.font_medium.render("P1 READY!", True, self.p1_color)
            screen.blit(p1_ready, (50, ready_y))
        
        if self.player2_selected:
            p2_ready = self.font_medium.render("P2 READY!", True, self.p2_color)
            p2_ready_rect = p2_ready.get_rect(right=1150, top=ready_y)
            screen.blit(p2_ready, p2_ready_rect)
        
        # Start game prompt
        if self.player1_selected and self.player2_selected:
            start_text = self.font_medium.render("STARTING GAME...", True, self.white)
            start_rect = start_text.get_rect(center=(600, 580))
            screen.blit(start_text, start_rect)
