import pygame

class Controller:
    def __init__(self, view):
        self.view = view
        self.running = True
        self.start_time = pygame.time.get_ticks()  # Initialize the start time
        self.game_over_time = None  # Variable to store the final time when game ends

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                right_click = event.button == 3  # Right mouse button
                self.view.handle_click(pos, right_click)

    def update_model(self):
        # Met à jour le modèle en fonction des interactions
        if self.view.board.check_win():
            print("You Win!")
            self.view.board.game_over = True
            self.game_over_time = (pygame.time.get_ticks() - self.start_time) // 1000
        elif self.view.board.game_over:
            print("Game Over")
            if self.game_over_time is None:  # Record time if not already set
                self.game_over_time = (pygame.time.get_ticks() - self.start_time) // 1000

    def update_view(self):
        # Redessine la vue avec les nouvelles informations du modèle
        self.view.draw(self.game_over_time, (pygame.time.get_ticks() - self.start_time) // 1000)
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            if self.view.board.game_over:
                self.handle_game_over()
            self.update_model()
            self.update_view()

    def handle_game_over(self):
        # Affiche un message ou gère la fin du jeu
        if self.view.board.game_over:
            print("Game Over! Final Time:", self.game_over_time)
            self.running = False
