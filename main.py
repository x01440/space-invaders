from numpy import true_divide
from graphics import *
import pygame
import sys
import time

BULLET_SPEED = 25 # 25px
GAME_PACE = 300 # 300ms
MOVE_STEP_SIZE = 15 # 10px
INVADER_SIZE = 25 # 25px
INVADER_SPACING = 25 # 25px
INVADER_SPEED = 5 # 5px
INVADER_START_OFFSET = 100 # 100px
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

# Pygame colors
COLOR_BLACK = (0,0,0)
COLOR_BLUE = (0, 0, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 0, 0)
COLOR_WHITE = (255,255,255)

bullets = []
invaders = []

class Bullet:
    x: int = 0
    y: int = 0
    speed: int = 0
    window = None

    def __init__(self, window, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.window = window
        pygame.draw.rect(self.window, COLOR_GREEN, (self.x - 5, self.y - 5, 10, 20))

    def move(self):
        self.y -= BULLET_SPEED
        pygame.draw.rect(self.window, COLOR_GREEN, (self.x - 5, self.y - 5, 10, 20))

class Invader:
    alive: bool = False
    x: int = 0
    y: int = 0
    window = None

    def __init__(self, window, x: int, y: int):
        self.x = x
        self.y = y
        self.window = window
        pygame.draw.rect(self.window, COLOR_BLUE, (self.x, self.y, 25, 25))
        self.alive = True

    def move(self):
        pygame.draw.rect(self.window, COLOR_BLUE, (self.x, self.y, 25, 25))

class InvaderFleet:
    direction: int = INVADER_SPEED
    fleet_offset: int = INVADER_START_OFFSET
    invaders = []
    invader_rows: int = 0
    invader_num_per_row: int = 0
    window = None

    def __init__(self, window, rows: int, num_per_row: int):
        self.invader_rows = rows
        self.invader_num_per_row = num_per_row
        self.window = window
        self.make_invaders()

    def make_invaders(self):
        for y in range(self.invader_rows):
            self.invaders.append([])
            for x in range(self.invader_num_per_row):
                invader_x = INVADER_START_OFFSET + x * (INVADER_SIZE + INVADER_SPACING)
                invader_y = INVADER_START_OFFSET + y * (INVADER_SIZE + INVADER_SPACING)
                invader = Invader(self.window, invader_x, invader_y)
                self.invaders[y].append(invader)

    def move_invaders(self):
        invader_right_edge = self.fleet_offset + self.invader_num_per_row * (INVADER_SIZE + self.direction)
        invader_left_edge = self.fleet_offset
        # Check if invaders are at right edge
        if invader_right_edge > WINDOW_WIDTH - INVADER_START_OFFSET:
            self.direction = -INVADER_SPEED
        # Check if invaders are at left edge
        if invader_left_edge < INVADER_START_OFFSET:
            self.direction = INVADER_SPEED

        for y in range(self.invader_rows):
            for x in range(self.invader_num_per_row):
                self.invaders[y][x].x += self.direction
                self.invaders[y][x].move()
        # Move the whole fleet
        self.fleet_offset += self.direction

class Ship:
    alive = True
    x = 0
    y = 0
    window = None

    def __init__(self, window, x, y):
        self.window = window
        self.x = x
        self.y = y
        pygame.draw.circle(self.window, COLOR_RED, (self.x, self.y), 25)

    def move(self, offset_x, offset_y):
        self.x = self.x + offset_x
        self.y = self.y + offset_y
        self.draw()

    def draw(self):
        pygame.draw.circle(self.window, COLOR_RED, (self.x, self.y), 25)

def main():
    # win = GraphWin('Space Invaders', WINDOW_WIDTH, WINDOW_HEIGHT)
    window = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
    pygame.init()

    # Initialize and draw objects

    # Draw the ship
    ship = Ship(window, 600, 600)

    # Draw the invaders
    fleet = InvaderFleet(window, 6, 10)

    # Initialize time
    last_time = time.time()
    while True:
        # Move cycle
        # Bullets move
        current_time = time.time()
        if current_time - GAME_PACE < last_time:
            # Clear display buffer
            window.fill(COLOR_WHITE)
            # Move bullets
            for bullet in bullets:
                bullet.move()
                if bullet.y < 0:
                    # No need to undraw, bullet will disappear
                    bullets.remove(bullet)
            # Move invaders
            if current_time - GAME_PACE * 3 < last_time:
                fleet.move_invaders()

            # Refresh ship
            ship.draw()

            pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            # KEYDOWN           key, mod, unicode, scancode
            if event.type == pygame.KEYDOWN:
                print('Key pressed: ' + event.key)
                k = event.key
                if k == 'Left':
                    ship.move(-MOVE_STEP_SIZE, 0)
                elif k == 'Right':
                    ship.move(MOVE_STEP_SIZE, 0)
                elif k == 'Up':
                    ship.move(0, -MOVE_STEP_SIZE)
                elif k == 'Down':
                    ship.move(0, MOVE_STEP_SIZE)
                elif k == 'space':
                    # Start bullet
                    if (len(bullets) < 2):
                        bullet = Bullet(window, ship.x, ship.y - 20, BULLET_SPEED)
                        bullets.append(bullet)
                elif k == 'period' or k == 'q':
                    break

main()

