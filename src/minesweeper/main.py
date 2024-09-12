import pygame
from view import GameView
from difficulty_selection_view import DifficultySelectionView
from model import Board, get_difficulty_settings
from controller import Controller

def main():
    while True:
        # Display difficulty selection screen
        selection_view = DifficultySelectionView()
        selection_view.run()
        difficulty = selection_view.difficulty
        
        if not difficulty:
            raise ValueError("Difficulty was not selected.")
        
        # Initialize game with selected difficulty
        width, height, num_mines = get_difficulty_settings(difficulty)
        board = Board(width, height, num_mines)
        game_view = GameView(board)
        controller = Controller(game_view)
        
        # Run the game
        while True:
            controller.handle_events()
            controller.update_model()
            controller.update_view()
            
            if game_view.board.game_over or game_view.board.check_win():
                break

if __name__ == "__main__":
    main()
