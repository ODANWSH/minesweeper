import random

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

class Board:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.grid = [[Cell() for _ in range(width)] for _ in range(height)]
        self.game_over = False
        self.mines_remaining = num_mines
        self.create_board()

    def create_board(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if not self.grid[y][x].is_mine:
                self.grid[y][x].is_mine = True
                self.update_adjacent_cells(x, y)
                mines_placed += 1

    def update_adjacent_cells(self, x, y):
        for i in range(max(0, x - 1), min(self.width, x + 2)):
            for j in range(max(0, y - 1), min(self.height, y + 2)):
                if not self.grid[j][i].is_mine:
                    self.grid[j][i].adjacent_mines += 1

    def reveal_cell(self, x, y):
        if self.game_over or self.grid[y][x].is_revealed or self.grid[y][x].is_flagged:
            return

        self.grid[y][x].is_revealed = True
        if self.grid[y][x].is_mine:
            self.game_over = True
            return

        if self.grid[y][x].adjacent_mines == 0:
            for i in range(max(0, x - 1), min(self.width, x + 2)):
                for j in range(max(0, y - 1), min(self.height, y + 2)):
                    if not self.grid[j][i].is_revealed:
                        self.reveal_cell(i, j)

    def set_flag(self, x, y):
        if not self.grid[y][x].is_revealed:
            self.grid[y][x].is_flagged = not self.grid[y][x].is_flagged
            self.mines_remaining += -1 if self.grid[y][x].is_flagged else 1

    def check_win(self):
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

def get_difficulty_settings(difficulty):
    if difficulty == 'easy':
        return (2, 2, 1)
    elif difficulty == 'medium':
        return (16, 16, 40)
    elif difficulty == 'hard':
        return (30, 16, 99)
    else:
        raise ValueError("Difficulty not recognized. Choose 'easy', 'medium', or 'hard'.")
