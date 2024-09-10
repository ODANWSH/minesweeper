import pygame, random
from pygame.locals import *

# Dimensions and colors
SIZE = 250, 250
LIGHTGRAY = (198, 198, 198)
GRAY = (192, 192, 192)
BLACK = (132, 132, 132)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption('Minesweeper')

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

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, BLACK, self.rect, 1)

    def toggle_color(self):
        if self.color == LIGHTGRAY:
            self.color = GREEN
        if self.hidden:
            self.color = RED

    def set_hidden(self):
        self.hidden = True

# Game class to manage the overall game logic
class Game:
    def __init__(self):
        self.blocks = []
        self.hidden_blocks = []
        self.create_grid()
        self.start_time = 0  # Time starts at 0
        self.game_started = False  # Track whether the game has started
        self.font = pygame.font.Font(None, 36)  # Font for timer
        
    def create_grid(self):
        # Initialize the grid of blocks
        for i in range(9):
            for j in range(9):
                x = 20 + i * (rect_dist + rect_width)
                y = 20 + j * (rect_dist + rect_height)
                block = Block(x, y)
                self.blocks.append(block)
        # Randomly hide 10 blocks
        self.hidden_blocks = random.sample(self.blocks, 10)
        for block in self.hidden_blocks:
            block.set_hidden()

    def handle_click(self, mouse_pos):
        # Start the timer on the first click
        if not self.game_started:
            self.start_time = pygame.time.get_ticks()
            self.game_started = True
        for block in self.blocks:
            if block.rect.collidepoint(mouse_pos):
                block.toggle_color()

    def draw(self, surface):
        surface.fill(GRAY)
        for block in self.blocks:
            block.draw(surface)
        # Calculate and render the timer only if the game has started
        if self.game_started:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000  # Time in seconds
            timer_text = self.font.render(f"{elapsed_time}s", True, BLACK)
            surface.blit(timer_text, (SIZE[0] - timer_text.get_width() - 3, 3))  # Top-right corner
            

# Main loop
def main():
    game = Game()
    running = True
    while running:
        # Draw the blocks
        game.draw(screen)
        # Update the display
        pygame.display.update()
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Mouse click detection
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                game.handle_click(mouse_pos)
    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()