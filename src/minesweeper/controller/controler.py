import pygame
import sys

class Controller:
    def __init__(self, view):
        self.view = view

    def run(self):
        while not self.view.board.game_over:
            self.view.handle_events()
            if self.view.board.check_win():
                print("You win!")
                self.view.board.game_over = True
            self.view.update()
