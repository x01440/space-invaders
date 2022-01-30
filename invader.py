import os
import pygame
import time

# Local imports
import constants

class Invader:
    alive: bool = False
    current_image_shown: int
    exploding: bool = False
    images = []
    image_switch_time = 1 # Switch once per second
    last_timer: int = 0
    point_value: int = 100
    vertical_size: int = 25
    window = None
    x: int = 0
    y: int = 0

    def __init__(self, window: pygame.Surface, x: int, y: int, images):
        self.x = x
        self.y = y
        self.window = window
        self.images = images
        self.last_timer = time.time()
        self.current_image_shown = 0
        self.window.blit(self.images[0], (self.x, self.y))
        self.alive = True

    def move(self):
        if self.alive:
            # Move and switch image on the schedule set for this invader
            current_time = time.time()
            if current_time - self.image_switch_time > self.last_timer:
                self.current_image_shown += 1
                if self.current_image_shown == len(self.images):
                    self.current_image_shown = 0
                self.last_timer = current_time
            self.window.blit(self.images[self.current_image_shown], (self.x, self.y))

    def explode(self):
        # Do explosion effect
        self.alive = False
        self.exploding = True

class InvaderFleet:
    direction: int = constants.INVADER_SPEED
    explosion_image = None
    fleet_offset: int = constants.INVADER_START_OFFSET
    images = []
    invaders = []
    invader_rows: int = 0
    invader_num_per_row: int = 0
    invaders_win = False
    window = None

    def __init__(self, window: pygame.Surface, rows: int, num_per_row: int):
        self.explosion_image = pygame.image.load(os.path.join('img', 'explosion.jpg'))
        self.invader_rows = rows
        self.invader_num_per_row = num_per_row
        self.images.append(pygame.image.load(os.path.join('img', 'invader1-1.png')))
        self.images.append(pygame.image.load(os.path.join('img', 'invader1-2.png')))
        self.images[0] = pygame.transform.scale(self.images[0], (25, 25))
        self.images[1] = pygame.transform.scale(self.images[1], (25, 25))
        self.window = window
        self.make_invaders()

    def make_invaders(self):
        for y in range(self.invader_rows):
            self.invaders.append([])
            for x in range(self.invader_num_per_row):
                invader_x = constants.INVADER_START_OFFSET + x * (constants.INVADER_SIZE + constants.INVADER_SPACING)
                invader_y = constants.INVADER_START_OFFSET + y * (constants.INVADER_SIZE + constants.INVADER_SPACING)
                invader = Invader(self.window, invader_x, invader_y, self.images)
                self.invaders[y].append(invader)

    def check_invader_hit(self, boundaries: tuple) -> Invader:
        x1, y1, x2, y2 = boundaries
        invader_hit = None
        for y in range(self.invader_rows):
            for x in range(self.invader_num_per_row):
                invader = self.invaders[y][x]
                if ((x1 > invader.x and x1 < invader.x + 25) or (x2 > invader.x and x2 < invader.x + 25)):
                    if ((y1 > invader.y and y1 < invader.y + 25) or (y2 > invader.y and y2 < invader.y + 25)):
                        if invader.alive == True:
                            invader_hit = invader
                            invader.explode()
        return invader_hit

    def move_invaders(self):
        vertical_move = 0
        invader_right_edge = self.fleet_offset + self.invader_num_per_row * (constants.INVADER_SIZE + constants.INVADER_SPACING)
        invader_left_edge = self.fleet_offset

        # If invaders change direction, move them down
        # Check if invaders are at right edge
        if invader_right_edge > constants.WINDOW_WIDTH - constants.INVADER_START_OFFSET:
            self.direction = -constants.INVADER_SPEED
            vertical_move = constants.INVADER_VERTICAL_MOVE

        # Check if invaders are at left edge
        if invader_left_edge < constants.INVADER_START_OFFSET:
            self.direction = constants.INVADER_SPEED
            vertical_move = constants.INVADER_VERTICAL_MOVE

        for y in range(self.invader_rows):
            for x in range(self.invader_num_per_row):
                self.invaders[y][x].x += self.direction
                self.invaders[y][x].y += vertical_move
                self.invaders[y][x].move()
                self.invaders_win = self.check_invader_win(self.invaders[y][x])
        # Move the whole fleet
        self.fleet_offset += self.direction

    def check_invader_win(self, invader: Invader):
        invader_win = True if invader.y + invader.vertical_size >= constants.WIN_GAME_HEIGHT else False
        return invader_win
