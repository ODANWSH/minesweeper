import pygame
from model import Board
from view import GameView

class Controller:
    def __init__(self, view):
        self.view = view
        self.running = True
        self.start_time = pygame.time.get_ticks()  # Initialize the start time
        self.game_over_time = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                right_click = event.button == 3  # Right mouse button
                if self.view.board.game_over:
                    # Restart the game
                    self.restart_game()
                else:
                    self.view.handle_click(pos, right_click)

    def update_model(self):
        if self.view.board.check_win():
            print("You Win!")
            self.view.board.game_over = True
            self.game_over_time = (pygame.time.get_ticks() - self.start_time) // 1000
        elif self.view.board.game_over:
            print("Game Over")
            if self.game_over_time is None:
                self.game_over_time = (pygame.time.get_ticks() - self.start_time) // 1000

    def update_view(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) // 1000 if not self.view.board.game_over else None
        self.view.draw(self.game_over_time, elapsed_time)

    def run(self):
        while self.running:
            self.handle_events()
            self.update_model()
            self.update_view()

    def restart_game(self):
        # Recreate the view and the controller
        self.view = GameView(Board(self.view.board.width, self.view.board.height, self.view.board.num_mines))
        
        self.start_time = pygame.time.get_ticks()  # Reset the start time
        self.game_over_time = None  # Reset the game over time
        self.view.board.game_over = False  # Reset game over status
        self.update_view()  # Update the view for the new game
        
