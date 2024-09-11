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
HOVER_COLOR = (170, 170, 170)
FLAG_COLOR = (255, 255, 0)  # Yellow for flagged blocks

# Font setup
pygame.font.init()
font = pygame.font.SysFont("Arial", 50)
small_font = pygame.font.SysFont("Arial", 30)
timer_font = pygame.font.SysFont("Arial", 36)

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
        self.flagged = False  # To indicate if a block is flagged

    def draw(self, surface):
        # Draw the block with hover and flagging logic
        if self.flagged:
            pygame.draw.rect(surface, FLAG_COLOR, self.rect, 0)  # Draw flagged block as yellow
        elif self.hovered:
            pygame.draw.rect(surface, HOVER_COLOR, self.rect, 0)
        else:
            pygame.draw.rect(surface, self.color, self.rect, 0)
        pygame.draw.rect(surface, BLACK, self.rect, 1)

    def toggle_color(self):
        if not self.flagged:  # Don't toggle if the block is flagged
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

    def toggle_flag(self):
        # Toggle the flagged state of the block if it's not revealed
        if self.color == LIGHTGRAY:
            self.flagged = not self.flagged

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

    def handle_left_click(self, mouse_pos):
        if not self.game_started:
            self.start_time = pygame.time.get_ticks()
            self.game_started = True

        if self.game_over:
            return  # Prevent further actions if the game is over

        for block in self.blocks:
            if block.rect.collidepoint(mouse_pos):
                block.toggle_color()
                if block.color == RED:
                    self.game_over = True  # Set game over flag
                    self.final_time = (pygame.time.get_ticks() - self.start_time) // 1000

    def handle_right_click(self, mouse_pos):
        if self.game_over:
            return  # Prevent flagging after the game is over

        # Right-click toggles a flag on the block
        for block in self.blocks:
            if block.rect.collidepoint(mouse_pos):
                block.toggle_flag()

    def check_victory(self):
        if all(block.is_revealed() for block in self.blocks if not block.hidden):
            self.victory = True
            self.game_over = True
            self.final_time = (pygame.time.get_ticks() - self.start_time) // 1000

    def draw(self, surface):
        surface.fill(GRAY)
        for block in self.blocks:
            block.draw(surface)

        # Draw timer if the game is ongoing
        if self.game_started and not self.game_over:
            current_time = (pygame.time.get_ticks() - self.start_time) // 1000
            timer_surface = timer_font.render(f"Time: {current_time}", True, BLACK)
            surface.blit(timer_surface, (20, 20))
        
        # Draw final time if the game is over
        if self.final_time is not None:
            final_time_surface = timer_font.render(f"Final Time: {self.final_time}s", True, BLACK)
            surface.blit(final_time_surface, (20, 20))

        # Draw "Game Over" message if the player loses
        if self.game_over and not self.victory:
            game_over_surface = font.render("Game Over", True, RED)
            surface.blit(game_over_surface, (self.grid_size[1] * rect_width // 2 - 100, 50))

        # Draw "You Win" message if the player wins
        if self.victory:
            victory_surface = font.render("You Win!", True, GREEN)
            surface.blit(victory_surface, (self.grid_size[1] * rect_width // 2 - 100, 50))

# Main function to run the game
def main():
    # Select difficulty (for example, using grid size 9x9 and 10 hidden blocks)
    grid_size = (9, 9)
    num_hidden = 10
    screen = pygame.display.set_mode((400, 400))  # Adjust size as needed
    pygame.display.set_caption("Minesweeper")

    # Create the game object
    game = Game(grid_size, num_hidden)

    clock = pygame.time.Clock()

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        for block in game.blocks:
            block.check_hover(mouse_pos)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left-click
                    game.handle_left_click(mouse_pos)
                elif event.button == 3:  # Right-click (flagging)
                    game.handle_right_click(mouse_pos)

        # Check for victory condition
        game.check_victory()

        # Draw the game
        game.draw(screen)
        pygame.display.update()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()