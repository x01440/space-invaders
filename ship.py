import os
import pygame

# Local imports
import constants

class Ship:
    alive: bool = True
    x: int = 0
    y: int = 0
    ship_image = None
    window = None

    def __init__(self, window, x, y):
        self.window = window
        self.x = x
        self.y = y
        self.ship_image = pygame.image.load(os.path.join('img', 'ship.png'))
        self.ship_image = pygame.transform.scale(self.ship_image, (40, 40))
        self.window.blit(self.ship_image, (self.x, self.y))

    def move(self, offset_x, offset_y):
        self.x = self.x + offset_x
        # Don't let the ship go into the invader fleet
        if (self.y + offset_y > constants.SHIP_BOUNDARY):
            self.y = self.y + offset_y
        self.draw()

    def draw(self):
        self.window.blit(self.ship_image, (self.x, self.y))