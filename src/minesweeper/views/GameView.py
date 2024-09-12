import pygame
from models.model import Board

# Define colors
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)  # Define green color for the number 2

# Define fonts
pygame.font.init()
font = pygame.font.SysFont(None, 20)
timer_font = pygame.font.SysFont(None, 28)

# Load assets
flag_image = pygame.transform.scale(pygame.image.load('assets/flag.png'), (20, 20))
mine_image = pygame.transform.scale(pygame.image.load('assets/bomb.png'), (20, 20))

class View:
    def __init__(self, board):
        self.board = board

        # Dynamic screen size based on board dimensions
        self.screen_size = (20 + board.width * 22, 20 + board.height * 22 + 150)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Minesweeper")

    def draw(self, game_over_time=None, elapsed_time=None):
        self.screen.fill(GRAY)

        # Draw the grid first to avoid text being hidden behind cells
        for y in range(self.board.height):
            for x in range(self.board.width):
                cell = self.board.grid[y][x]
                rect = pygame.Rect(x * 22 + 20, y * 22 + 100, 20, 20)  # Adjusted y position to move rects down

                if cell.is_revealed:
                    if cell.is_mine:
                        color = RED  # Red for mines
                    elif cell.adjacent_mines == 0:
                        color = WHITE  # White for empty revealed cells
                    else:
                        color = GRAY  # Default color for revealed cells with adjacent mines
                else:
                    color = GRAY  # Default color for unrevealed cells

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 2)

                if cell.is_flagged:
                    self.screen.blit(flag_image, rect)
                elif cell.is_revealed:
                    if cell.is_mine:
                        self.screen.blit(mine_image, rect)
                    elif cell.adjacent_mines > 0:
                        # Change text color based on number of adjacent mines
                        if cell.adjacent_mines == 1:
                            text_color = BLUE
                        elif cell.adjacent_mines == 2:
                            text_color = GREEN  # Green for the number 2
                        else:
                            text_color = RED  # Default color for other numbers
                        text_surf = font.render(str(cell.adjacent_mines), True, text_color)
                        self.screen.blit(text_surf, (rect.x + 4, rect.y + 2))

        # Always display the timer and mines count, even after the game ends
        if elapsed_time is not None:
            # Render the timer text
            timer_text = timer_font.render(f"Time: {elapsed_time}s", True, RED)
            # Create a background rectangle that fits the text size exactly
            timer_rect = pygame.Rect(10, 10, timer_text.get_width() + 10, timer_text.get_height() + 10)
            pygame.draw.rect(self.screen, BLACK, timer_rect)  # Black background for the timer
            self.screen.blit(timer_text, (timer_rect.x + 5, timer_rect.y + 5))  # Center the text in the rect

            # Render the mines count text
            mines_text = timer_font.render(f"Mines: {self.board.mines_remaining}", True, RED)
            # Create a background rectangle that fits the text size exactly
            mines_rect = pygame.Rect(self.screen_size[0] - mines_text.get_width() - 20, 10, mines_text.get_width() + 10, mines_text.get_height() + 10)
            pygame.draw.rect(self.screen, BLACK, mines_rect)  # Black background for mines count
            self.screen.blit(mines_text, (mines_rect.x + 5, mines_rect.y + 5))  # Center the text in the rect

        pygame.display.flip()

    def handle_click(self, pos, right_click=False):
        if self.board.game_over:
            return  # Ignore clicks if the game is over

        x, y = pos
        x = (x - 20) // 22
        y = (y - 100) // 22  # Adjusted y position to account for the new starting position of the grid

        if 0 <= x < self.board.width and 0 <= y < self.board.height:
            if right_click:
                self.board.set_flag(x, y)
            else:
                self.board.reveal_cell(x, y)

            self.draw()

            if self.board.game_over:
                pygame.time.wait(2000)  # Wait for 2 seconds to show the game over state
                self.draw(game_over_time=True)  # Redraw to show final state without erasing timer/mines