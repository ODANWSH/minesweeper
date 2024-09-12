import pygame
import sys

# Define colors
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BUTTON_COLOR = (50, 150, 255)
HOVER_BUTTON_COLOR = (80, 180, 255)

# Define fonts
pygame.font.init()
font = pygame.font.SysFont(None, 40)

class DifficultySelectionView:
    def __init__(self):
        pygame.init()
        self.screen_size = (600, 400)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Select Difficulty")
        self.difficulty = None

    def draw(self):
        self.screen.fill(GRAY)
        
        # Draw buttons with spacing
        button_spacing = 80
        start_y = 100
        
        self.draw_button("Easy", (self.screen_size[0] // 2, start_y), "easy")
        self.draw_button("Medium", (self.screen_size[0] // 2, start_y + button_spacing), "medium")
        self.draw_button("Hard", (self.screen_size[0] // 2, start_y + 2 * button_spacing), "hard")
        
        pygame.display.flip()

    def draw_button(self, text, position, difficulty_value):
        button_radius = 20
        button_width = 180
        button_height = 60

        button_rect = pygame.Rect(position[0] - button_width // 2, position[1] - button_height // 2, button_width, button_height)
        
        # Draw rounded rectangle
        self.draw_rounded_rect(self.screen, button_rect, button_radius, BUTTON_COLOR, HOVER_BUTTON_COLOR, pygame.mouse.get_pos())
        
        # Draw text on the button
        text_surf = font.render(text, True, WHITE)
        self.screen.blit(text_surf, (button_rect.x + (button_width - text_surf.get_width()) // 2, button_rect.y + (button_height - text_surf.get_height()) // 2))

    def draw_rounded_rect(self, surface, rect, radius, color, hover_color, mouse_pos):
        x, y, width, height = rect
        rect_surf = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(rect_surf, (0, 0, 0, 0), (0, 0, width, height))
        pygame.draw.rect(rect_surf, hover_color if rect.collidepoint(mouse_pos) else color, (0, 0, width, height), border_radius=radius)
        surface.blit(rect_surf, (x, y))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_button_pressed(mouse_pos, (self.screen_size[0] // 2, 100)):
                        self.difficulty = 'easy'
                        return
                    elif self.is_button_pressed(mouse_pos, (self.screen_size[0] // 2, 180)):
                        self.difficulty = 'medium'
                        return
                    elif self.is_button_pressed(mouse_pos, (self.screen_size[0] // 2, 260)):
                        self.difficulty = 'hard'
                        return
            self.draw()

    def is_button_pressed(self, mouse_pos, position):
        button_radius = 20
        button_width = 180
        button_height = 60
        button_rect = pygame.Rect(position[0] - button_width // 2, position[1] - button_height // 2, button_width, button_height)
        return button_rect.collidepoint(mouse_pos)