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
        self.mines_remaining = num_mines
        self.game_over = False
        
        self._place_mines()
        self._calculate_adjacent_mines()

    def _place_mines(self):
        mines_placed = 0
        while mines_placed < self.num_mines:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)
            if not self.grid[y][x].is_mine:
                self.grid[y][x].is_mine = True
                mines_placed += 1

    def _calculate_adjacent_mines(self):
        for y in range(self.height):
            for x in range(self.width):
                if self.grid[y][x].is_mine:
                    continue
                count = 0
                for dy in [-1, 0, 1]:
                    for dx in [-1, 0, 1]:
                        ny, nx = y + dy, x + dx
                        if 0 <= ny < self.height and 0 <= nx < self.width and self.grid[ny][nx].is_mine:
                            count += 1
                self.grid[y][x].adjacent_mines = count

    def reveal_cell(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height) or self.grid[y][x].is_revealed:
            return
        self.grid[y][x].is_revealed = True
        if self.grid[y][x].is_mine:
            self.game_over = True
        elif self.grid[y][x].adjacent_mines == 0:
            for dy in [-1, 0, 1]:
                for dx in [-1, 0, 1]:
                    if dy == 0 and dx == 0:
                        continue
                    self.reveal_cell(x + dx, y + dy)

    def set_flag(self, x, y):
        if not (0 <= x < self.width and 0 <= y < self.height) or self.grid[y][x].is_revealed:
            return
        self.grid[y][x].is_flagged = not self.grid[y][x].is_flagged
        self.mines_remaining += -1 if self.grid[y][x].is_flagged else 1

    def check_win(self):
        for y in range(self.height):
            for x in range(self.width):
                cell = self.grid[y][x]
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

def get_difficulty_settings(difficulty):
    """Return the board size and number of mines based on the difficulty."""
    if difficulty == 'easy':
        return (9, 9, 10)
    elif difficulty == 'medium':
        return (16, 16, 40)
    elif difficulty == 'hard':
        return (30, 16, 99)
    else:
        raise ValueError(f"Unknown difficulty level: {difficulty}")