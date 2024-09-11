import pygame

# Define colors
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
HOVER_COLOR = (170, 170, 170)
BUTTON_COLOR = (50, 150, 255)
HOVER_BUTTON_COLOR = (80, 180, 255)

# Define fonts
pygame.font.init()
font = pygame.font.SysFont(None, 20)
small_font = pygame.font.SysFont(None, 30)
timer_font = pygame.font.SysFont(None, 28)

# Load assets
flag_image = pygame.transform.scale(pygame.image.load('assets/bomb.png'), (20, 20))
mine_image = pygame.transform.scale(pygame.image.load('assets/bomb.png'), (20, 20))

class GameView:
    def __init__(self, board):
        self.board = board
        self.screen_size = (20 + board.width * 22, 20 + board.height * 22 + 100)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Minesweeper")
        self.start_time = pygame.time.get_ticks()  # Initialize the start time
        self.game_over_time = None  # Variable to store the final time when game ends

    def draw(self):
        self.screen.fill(GRAY)
        
        # Calculate elapsed time
        if self.game_over_time is None:  # Timer is running
            elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        else:  # Timer has stopped (game over)
            elapsed_time = self.game_over_time

        timer_text = timer_font.render(f"Time: {elapsed_time}s", True, WHITE)
        self.screen.blit(timer_text, (20, 20))  # Display the timer at the top

        # Display remaining mines
        mines_text = timer_font.render(f"Mines: {self.board.mines_remaining}", True, WHITE)
        self.screen.blit(mines_text, (20, 50))  # Display mines remaining below the timer

        for y in range(self.board.height):
            for x in range(self.board.width):
                cell = self.board.grid[y][x]
                rect = pygame.Rect(x * 22 + 20, y * 22 + 100, 20, 20)
                color = GREEN if cell.is_revealed else WHITE
                if cell.is_flagged:
                    self.screen.blit(flag_image, rect)  # Draw flag image
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                if cell.is_revealed and cell.is_mine:
                    self.screen.blit(mine_image, rect)  # Draw mine image
                elif cell.is_revealed and cell.adjacent_mines > 0:
                    text_surf = font.render(str(cell.adjacent_mines), True, BLACK)
                    self.screen.blit(text_surf, (rect.x + 4, rect.y + 2))

        pygame.display.flip()

    def handle_click(self, pos, right_click=False):
        if self.board.game_over or self.board.check_win():
            return
        
        x, y = pos
        x = (x - 20) // 22
        y = (y - 100) // 22
        if 0 <= x < self.board.width and 0 <= y < self.board.height:
            if right_click:
                self.board.set_flag(x, y)
            else:
                self.board.reveal_cell(x, y)
            
            if self.board.game_over:  # Stop the timer if game is over
                self.game_over_time = (pygame.time.get_ticks() - self.start_time) // 1000
                print("Game Over")
            elif self.board.check_win():
                print("You Win!")
                self.game_over_time = (pygame.time.get_ticks() - self.start_time) // 1000

def select_difficulty(screen):
    # Dummy function for now
    return 'easy'
