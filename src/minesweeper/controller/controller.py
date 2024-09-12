import pygame
from models.model import Board
from views.GameView import View
from views.SelectDifficulty import DifficultySelectionView

class Controller:
    def __init__(self, view):
        self.view = view
        self.running = True
        self.start_time = pygame.time.get_ticks()  # Get the starting time
        self.game_over_time = None
        self.selection_view = None
        self.return_to_selection = False  # Flag to return to selection after 2 seconds

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                return True  # Quit the game loop
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.view.board.game_over:
                    pos = pygame.mouse.get_pos()
                    if event.button == 1:  # Left click
                        self.view.handle_click(pos, right_click=False)
                    elif event.button == 3:  # Right click
                        self.view.handle_click(pos, right_click=True)

    def update_model(self):
        if self.view.board.check_win():
            print("You Win!")
            self.view.board.game_over = True
            self.game_over_time = pygame.time.get_ticks()
        elif self.view.board.game_over:
            if self.game_over_time is None:
                self.game_over_time = pygame.time.get_ticks()

    def update_view(self):
        # Calculate elapsed time since the game started
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000
        if self.view.board.game_over:
            # Show the final time even if the game is over
            elapsed_time = (self.game_over_time - self.start_time) // 1000
        self.view.draw(elapsed_time=elapsed_time)

    def run(self):
        while self.running:
            if self.selection_view:
                self.selection_view.run()
                self.view = View(Board(self.selection_view.width, self.selection_view.height, self.selection_view.num_mines))
                self.start_time = pygame.time.get_ticks()  # Reset the start time
                self.game_over_time = None  # Reset game over time
                self.view.board.game_over = False  # Reset game over status
                self.selection_view = None  # Exit selection view
                continue

            # Handle events for clicks or quitting
            if self.handle_events():
                return  # Quit the game loop

            self.update_model()
            self.update_view()