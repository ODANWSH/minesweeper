

class Cell:
    def __init__(self):
        self.is_mine = False  # Si la case contient une mine
        self.is_revealed = False  # Si la case a été révélée
        self.is_flagged = False  # Si la case est marquée par un drapeau
        self.adjacent_mines = 0  # Nombre de mines autour de cette case
    
    def reveal(self):
        self.is_revealed = True
    
    def toggle_flag(self):
        self.is_flagged = not self.is_flagged





class Board:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows  # Nombre de lignes
        self.cols = cols  # Nombre de colonnes
        self.num_mines = num_mines  # Nombre de mines à placer
        self.grid = self.create_board()  # Plateau de jeu sous forme de grille de cellules
        self.generate_mines()  # Placer les mines sur le plateau

    def create_board(self):
        # Crée un plateau vide avec des instances de la classe Cell
        return [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

    def generate_mines(self):
        # Placer des mines aléatoirement sur le plateau
        import random
        mines_placed = 0
        while mines_placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not self.grid[row][col].is_mine:
                self.grid[row][col].is_mine = True
                mines_placed += 1
                # Après avoir placé la mine, mettre à jour les cellules voisines
                self.update_adjacent_cells(row, col)

    def update_adjacent_cells(self, row, col):
        # Met à jour le nombre de mines adjacentes pour les cellules autour d'une mine
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                if not self.grid[i][j].is_mine:
                    self.grid[i][j].adjacent_mines += 1

    def set_flag(self, row, col):
        # Marquer ou démarcher une case
        self.grid[row][col].toggle_flag()

    def reveal_cell(self, row, col):
        # Révéler une case (à développer : propagation si aucune mine adjacente)
        cell = self.grid[row][col]
        if not cell.is_flagged and not cell.is_revealed:
            cell.reveal()
            # Si la case révélée n'a pas de mines adjacentes, révéler ses voisines
            if cell.adjacent_mines == 0:
                self.reveal_adjacent_cells(row, col)

    def reveal_adjacent_cells(self, row, col):
        # Révéler récursivement les cases adjacentes sans mines adjacentes
        for i in range(max(0, row - 1), min(self.rows, row + 2)):
            for j in range(max(0, col - 1), min(self.cols, col + 2)):
                if not self.grid[i][j].is_revealed and not self.grid[i][j].is_mine:
                    self.reveal_cell(i, j)

    def check_win(self):
        # Vérifier si toutes les cases non-minées ont été révélées
        for row in self.grid:
            for cell in row:
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True
