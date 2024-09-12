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
flag_image = pygame.transform.scale(pygame.image.load('assets/flag.png'), (20, 20))
mine_image = pygame.transform.scale(pygame.image.load('assets/bomb.png'), (20, 20))

class GameView:
    def __init__(self, board):
        self.board = board
        self.screen_size = (20 + board.width * 22, 20 + board.height * 22 + 100)
        self.screen = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption("Minesweeper")

    def draw(self, game_over_time=None, elapsed_time=None):
        self.screen.fill(GRAY)
        
        # Calculate elapsed time
        if elapsed_time is not None:
            timer_text = timer_font.render(f"Time: {elapsed_time}s", True, WHITE)
            self.screen.blit(timer_text, (20, 20))

        # Display remaining mines
        mines_text = timer_font.render(f"Mines: {self.board.mines_remaining}", True, WHITE)
        self.screen.blit(mines_text, (20, 50))

        for y in range(self.board.height):
            for x in range(self.board.width):
                cell = self.board.grid[y][x]
                rect = pygame.Rect(x * 22 + 20, y * 22 + 100, 20, 20)
                color = GREEN if cell.is_revealed else WHITE
                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                
                if cell.is_flagged:
                    self.screen.blit(flag_image, rect)
                elif cell.is_revealed and cell.is_mine:
                    self.screen.blit(mine_image, rect)
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
            
            self.draw()

            if self.board.game_over:
                self.display_game_over_message("Game Over! Click to restart.")
            elif self.board.check_win():
                self.display_game_over_message("You Win! Click to restart.")

    def display_game_over_message(self, message):
        self.screen.fill(GRAY)
        message_text = font.render(message, True, RED)
        self.screen.blit(message_text, (self.screen.get_width() // 2 - message_text.get_width() // 2, self.screen.get_height() // 2 - message_text.get_height() // 2))
        
        pygame.display.flip()

        # Wait for user to click to restart
        waiting_for_click = True
        while waiting_for_click:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    import sys
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    waiting_for_click = False
                    return
