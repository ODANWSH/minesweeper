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
        self.screen_size = (400, 300)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Select Difficulty")
        self.difficulty = None

    def draw(self):
        self.screen.fill(GRAY)
        self.draw_button("Easy", (150, 100), "easy")
        self.draw_button("Medium", (150, 150), "medium")
        self.draw_button("Hard", (150, 200), "hard")
        pygame.display.flip()

    def draw_button(self, text, position, difficulty_value):
        button_rect = pygame.Rect(position[0] - 60, position[1] - 30, 120, 60)
        mouse_pos = pygame.mouse.get_pos()
        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, HOVER_BUTTON_COLOR, button_rect)
        else:
            pygame.draw.rect(self.screen, BUTTON_COLOR, button_rect)
        text_surf = font.render(text, True, WHITE)
        self.screen.blit(text_surf, (position[0] - text_surf.get_width() // 2, position[1] - text_surf.get_height() // 2))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.is_button_pressed(mouse_pos, (150, 100)):
                        self.difficulty = 'easy'
                        return
                    elif self.is_button_pressed(mouse_pos, (150, 150)):
                        self.difficulty = 'medium'
                        return
                    elif self.is_button_pressed(mouse_pos, (150, 200)):
                        self.difficulty = 'hard'
                        return
            self.draw()

    def is_button_pressed(self, mouse_pos, position):
        button_rect = pygame.Rect(position[0] - 60, position[1] - 30, 120, 60)
        return button_rect.collidepoint(mouse_pos)
