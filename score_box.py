import pygame

# Local imports
import constants

class Score:
    font: pygame.font.Font
    number_ships: int = 0
    score: int = 0
    window = None
    x: int = 0
    y: int = 0

    def __init__(self, window, x, y):
        self.font = pygame.font.SysFont('courier', 32)
        self.window = window
        self.x = x
        self.y = y

    def draw(self, game_score: int):
        # Render the score
        text = self.font.render(
            'Score: ' + game_score,
            True,
            constants.COLOR_BLUE,
            constants.COLOR_WHITE)
        self.window.blit(text, (self.x, self.y))