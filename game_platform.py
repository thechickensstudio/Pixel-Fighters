import pygame

class Platform:
    def __init__(self, x, y, width, height, terrain_row=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
        # Load terrain sprite sheet
        try:
            sprite_sheet = pygame.image.load("assets/Terrain/Terrain (16x16).png").convert_alpha()
            self.has_texture = True
            
            # Extract individual tiles from sprite sheet (16x16 each)
            # Different rows for different terrain styles
            # terrain_row: 0=grass, 1=stone, 2=dirt, etc.
            row_y = terrain_row * 16
            
            self.tile_left = sprite_sheet.subsurface((0, row_y, 16, 16))      # Left edge
            self.tile_center = sprite_sheet.subsurface((16, row_y, 16, 16))   # Center fill
            self.tile_right = sprite_sheet.subsurface((32, row_y, 16, 16))    # Right edge
            
        except Exception as e:
            print(f"Error loading terrain: {e}")
            self.has_texture = False
            self.color = (101, 67, 33)  # Brown color
    
    def draw(self, screen):
        """Draw the platform with proper edges and center tiles"""
        if self.has_texture:
            # Calculate how many tiles we need
            num_tiles = self.width // 16
            
            # Draw platform tiles
            for i in range(num_tiles):
                tile_x = self.x + (i * 16)
                
                if i == 0:
                    # Left edge
                    screen.blit(self.tile_left, (tile_x, self.y))
                elif i == num_tiles - 1:
                    # Right edge
                    screen.blit(self.tile_right, (tile_x, self.y))
                else:
                    # Center tiles
                    screen.blit(self.tile_center, (tile_x, self.y))
            
            # Fill remaining space if width doesn't divide evenly by 16
            remainder = self.width % 16
            if remainder > 0:
                cropped = self.tile_right.subsurface((0, 0, remainder, 16))
                screen.blit(cropped, (self.x + num_tiles * 16, self.y))
                
        else:
            # Fallback: draw colored rectangle
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
            # Add border
            pygame.draw.rect(screen, (80, 50, 20), (self.x, self.y, self.width, self.height), 2)
