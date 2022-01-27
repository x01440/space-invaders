import pygame

# Local imports
import constants

class Bullet:
    x: int = 0
    y: int = 0
    speed: int = 0
    window = None

    def __init__(self, window, x, y, speed, id):
        self.id = id
        self.x = x
        self.y = y
        self.speed = speed
        self.window = window
        pygame.draw.rect(self.window, constants.COLOR_GREEN, self.getBulletRectangleDimensions())

    def move(self):
        self.y -= constants.BULLET_SPEED
        pygame.draw.rect(self.window, constants.COLOR_GREEN, self.getBulletRectangleDimensions())

    def getBulletRectangleDimensions(self):
        return (self.x - 5, self.y - 10, 10, 20)

    def getBulletBoundaries(self):
        return (self.x - 5, self.y - 10, self.x + 5, self.y + 10)

    def getBulletBottomEdge(self):
        return self.y + 10
