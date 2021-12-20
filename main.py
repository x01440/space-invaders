import os
import pygame
import sys
import time

BULLET_SPEED = 8 # 8px
GAME_PACE = 0.1 # move every half second
INVADER_SIZE = 25 # 25px
INVADER_SPACING = 25 # 25px
INVADER_SPEED = 2 # 1px
INVADER_START_OFFSET = 100 # 100px
SHIP_BOUNDARY = 500
SHIP_SPEED = 5 # 5px
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
    point_value: int = 100
    image_switch_time = 1 # Switch once per second
    current_image_shown: int
    last_timer: int = 0
    images = []

    def __init__(self, window, x: int, y: int, images):
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

class InvaderFleet:
    direction: int = INVADER_SPEED
    fleet_offset: int = INVADER_START_OFFSET
    images = []
    invaders = []
    invader_rows: int = 0
    invader_num_per_row: int = 0
    window = None

    def __init__(self, window, rows: int, num_per_row: int):
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
                invader_x = INVADER_START_OFFSET + x * (INVADER_SIZE + INVADER_SPACING)
                invader_y = INVADER_START_OFFSET + y * (INVADER_SIZE + INVADER_SPACING)
                invader = Invader(self.window, invader_x, invader_y, self.images)
                self.invaders[y].append(invader)

    def check_invader_hit(self, x1, x2, y1, y2):
        is_hit = False
        for y in range(self.invader_rows):
            for x in range(self.invader_num_per_row):
                invader = self.invaders[y][x]
                if ((x1 > invader.x and x1 < invader.x + 25) or (x2 > invader.x and x2 < invader.x + 25)):
                    if ((y1 > invader.y and y1 < invader.y + 25) or (y2 > invader.y and y2 < invader.y + 25)):
                        if invader.alive == True:
                            is_hit = True
                            invader.explode()
        return is_hit

    def move_invaders(self):
        invader_right_edge = self.fleet_offset + self.invader_num_per_row * (INVADER_SIZE + INVADER_SPACING)
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
        if (self.y + offset_y > SHIP_BOUNDARY):
            self.y = self.y + offset_y
        self.draw()

    def draw(self):
        self.window.blit(self.ship_image, (self.x, self.y))

def check_invader_hit(fleet: InvaderFleet):
    bullet_to_remove = None
    for b in bullets:
        if fleet.check_invader_hit(b.x - 5, b.x + 5, b.y, b.y + 20):
            print('Bullet Hit!')
            bullet_to_remove = b
    if bullet_to_remove:
        bullets.remove(b)

def execute_input(window, ship: Ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            print('Key pressed: ' + str(event.key))

    # Movement key check
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
            ship.move(-SHIP_SPEED, 0)
    elif keys[pygame.K_RIGHT]:
        ship.move(SHIP_SPEED, 0)
    elif keys[pygame.K_UP]:
        ship.move(0, -SHIP_SPEED)
    elif keys[pygame.K_DOWN]:
        ship.move(0, SHIP_SPEED)

    # Firing key checks, can happen at the same time as movement
    if keys[pygame.K_SPACE]:
            # Start bullet
            if (len(bullets) < 2):
                bullet = Bullet(window, ship.x + 20, ship.y - 20, BULLET_SPEED)
                bullets.append(bullet)

    # Quit key check
    if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

def main():
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
        if current_time - GAME_PACE > last_time:
            # Clear display buffer
            window.fill(COLOR_WHITE)

            # Execute input
            execute_input(window, ship, bullets)

            # Move bullets
            for bullet in bullets:
                bullet.move()
                if bullet.y < 0:
                    # No need to undraw, bullet will disappear
                    bullets.remove(bullet)

            # If bullet hits an invader, then the invader disappears
            check_invader_hit(fleet)

            # Move invaders
            fleet.move_invaders()

            # Refresh ship
            ship.draw()

            last_time = current_time
            pygame.display.update()


main()
