import pygame
from views.GameView import View
from views.SelectDifficulty import DifficultySelectionView
from models.model import Board, get_difficulty_settings
from controller.controller import Controller

def main():
    while True:
        # Display difficulty selection screen
        selection_view = DifficultySelectionView()
        selection_view.run()
        difficulty = selection_view.difficulty
        
        if not difficulty:
            pygame.quit()
            return
        
        # Initialize game with selected difficulty
        width, height, num_mines = get_difficulty_settings(difficulty)
        board = Board(width, height, num_mines)
        game_view = View(board)
        controller = Controller(game_view)
        
        # Run the game
        while True:
            if not controller.run():
                break  # Exit the game loop and return to difficulty selection

if __name__ == "__main__":
    main()