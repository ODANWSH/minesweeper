import pygame
from view import GameView
from model import Board, get_difficulty_settings

def main():
    pygame.init()
    
    # Définir les paramètres du jeu directement
    difficulty = 'medium'  # Vous pouvez changer à 'easy', 'medium', ou 'hard'
    width, height, num_mines = get_difficulty_settings(difficulty)
    
    # Créer le plateau de jeu
    board = Board(width, height, num_mines)
    
    # Créer la vue du jeu
    game_view = GameView(board)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                game_view.handle_click(pos)
                
        game_view.draw()
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()
