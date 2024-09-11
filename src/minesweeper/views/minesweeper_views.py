import pygame, random
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Colors
LIGHTGRAY = (198, 198, 198)
GRAY = (192, 192, 192)
BLACK = (132, 132, 132)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
DARKGRAY = (100, 100, 100)
HOVER_COLOR = (170, 170, 170)  # Light hover color for blocks
BUTTON_COLOR = (50, 150, 255)
HOVER_BUTTON_COLOR = (80, 180, 255)
TEXT_COLOR = (0, 0, 0)

# Font setup
pygame.font.init()
font = pygame.font.SysFont("Arial", 20)
small_font = pygame.font.SysFont("Arial", 30)
timer_font = pygame.font.SysFont("Arial", 28)

# Rectangle dimensions
rect_width = 20
rect_height = 20
rect_dist = 2

# Block class to represent each individual rectangle
class Block:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, rect_width, rect_height)
        self.color = LIGHTGRAY
        self.hidden = False
        self.hovered = False

    def draw(self, surface):
        if self.hovered:
            pygame.draw.rect(surface, HOVER_COLOR, self.rect, 0)
        else:
            pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, BLACK, self.rect, 1)

    def toggle_color(self):
        if self.color == LIGHTGRAY:
            self.color = GREEN
        if self.hidden:
            self.color = RED

    def set_hidden(self):
        self.hidden = True

    def is_revealed(self):
        return self.color == GREEN

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

# Game class to manage the overall game logic
class Game:
    def __init__(self, grid_size, num_hidden):
        self.grid_size = grid_size  # (rows, cols)
        self.num_hidden = num_hidden
        self.blocks = []
        self.hidden_blocks = []
        self.create_grid()
        self.start_time = 0  # Time starts at 0
        self.game_started = False  # Track whether the game has started
        self.game_over = False  # Flag to check if the game is over
        self.victory = False  # Flag to check if the player has won
        self.final_time = None  # Variable to store final time after game over

    def create_grid(self):
        rows, cols = self.grid_size
        for i in range(rows):
            for j in range(cols):
                x = 20 + j * (rect_dist + rect_width)
                y = 100 + i * (rect_dist + rect_height)  # Leave space at the top for the timer
                block = Block(x, y)
                self.blocks.append(block)
        
        # Randomly hide blocks (red blocks)
        self.hidden_blocks = random.sample(self.blocks, self.num_hidden)
        for block in self.hidden_blocks:
            block.set_hidden()

    def handle_click(self, mouse_pos):
        if not self.game_started:
            self.start_time = pygame.time.get_ticks()
            self.game_started = True

        for block in self.blocks:
            if block.rect.collidepoint(mouse_pos):
                block.toggle_color()
                if block.color == RED:
                    self.game_over = True
                    self.final_time = (pygame.time.get_ticks() - self.start_time) // 1000

    def check_victory(self):
        if all(block.is_revealed() for block in self.blocks if not block.hidden):
            self.victory = True
            self.game_over = True
            self.final_time = (pygame.time.get_ticks() - self.start_time) // 1000

    def draw(self, surface):
        surface.fill(GRAY)
        for block in self.blocks:
            block.draw(surface)

        # If the game is ongoing, update the timer
        if self.game_started and not self.game_over:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
            timer_text = timer_font.render(f"Time: {elapsed_time}s", True, WHITE)
            surface.blit(timer_text, (20, 20))

        # If the game is over, display final time or victory message
        if self.game_over:
            if self.victory:
                victory_text = font.render(f"You Win! Time: {self.final_time}s", True, WHITE)
                surface.blit(victory_text, (surface.get_width() // 2 - victory_text.get_width() // 2, 20))
            else:
                final_text = font.render(f"Final Time: {self.final_time}s", True, WHITE)
                surface.blit(final_text, (surface.get_width() // 2 - final_text.get_width() // 2, 20))

# Button class for selecting difficulty
class Button:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.hovered = False

    def draw(self, surface):
        color = HOVER_BUTTON_COLOR if self.hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=12)
        text_surf = small_font.render(self.text, True, WHITE)
        surface.blit(text_surf, (self.rect.x + (self.rect.width - text_surf.get_width()) // 2,
                                 self.rect.y + (self.rect.height - text_surf.get_height()) // 2))

    def check_hover(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

# Difficulty selection screen
def select_difficulty(screen):
    screen.fill(GRAY)
    title = font.render("Select Difficulty", True, WHITE)
    screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))

    easy_button = Button(150, 150, 200, 50, "Easy")
    intermediate_button = Button(150, 220, 200, 50, "Intermediate")
    hard_button = Button(150, 290, 200, 50, "Hard")

    buttons = [easy_button, intermediate_button, hard_button]

    pygame.display.update()

    while True:
        mouse_pos = pygame.mouse.get_pos()
        for button in buttons:
            button.check_hover(mouse_pos)

        screen.fill(GRAY)
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 50))
        for button in buttons:
            button.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.is_clicked(mouse_pos):
                    return (9, 9), 10
                if intermediate_button.is_clicked(mouse_pos):
                    return (16, 16), 40
                if hard_button.is_clicked(mouse_pos):
                    return (16, 30), 99

# Main loop
def main():
    screen = pygame.display.set_mode((500, 500))  # Initialize screen variable
    pygame.display.set_caption("Minesweeper")

    # Pass the screen object to the select_difficulty function
    grid_size, num_hidden = select_difficulty(screen)

    screen_size = (20 + grid_size[1] * (rect_width + rect_dist), 20 + grid_size[0] * (rect_height + rect_dist) + 100)
    pygame.display.set_mode(screen_size)

    game = Game(grid_size, num_hidden)
    running = True

    while running:
        mouse_pos = pygame.mouse.get_pos()

        for block in game.blocks:
            block.check_hover(mouse_pos)

        game.draw(screen)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN and not game.game_over:
                game.handle_click(mouse_pos)
                game.check_victory()

    pygame.quit()
