import os
import pygame
import sys
import time

# Local imports
import constants

bullets = {}
globals = {
    constants.BULLET_ID: 0,
    constants.GAME_SCORE: 0,
    constants.LAST_FIRE_TIME: 0
}
invaders = []

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

class Invader:
    alive: bool = False
    current_image_shown: int
    images = []
    image_switch_time = 1 # Switch once per second
    last_timer: int = 0
    point_value: int = 100
    vertical_size: int = 25
    window = None
    x: int = 0
    y: int = 0

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
    direction: int = constants.INVADER_SPEED
    fleet_offset: int = constants.INVADER_START_OFFSET
    images = []
    invaders = []
    invader_rows: int = 0
    invader_num_per_row: int = 0
    invaders_win = False
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

class Score:
    font: pygame.font.Font
    number_ships: int = 0
    score: int = 0
    window = None
    x: int = 0
    y: int = 0

    def __init__(self, window, x, y):
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.window = window
        self.x = x
        self.y = y

    def draw(self):
        # Render the score
        text = self.font.render('Score: ' + str(globals[constants.GAME_SCORE]), True, constants.COLOR_BLUE, constants.COLOR_WHITE)
        self.window.blit(text, (self.x, self.y))

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

def check_invader_hit(fleet: InvaderFleet):
    if len(bullets) == 0:
        return
    bullet_to_remove = None
    for id in bullets:
        invader_hit = fleet.check_invader_hit(bullets[id].getBulletBoundaries())
        if invader_hit:
            print('Bullet Hit!')
            globals[constants.GAME_SCORE] += invader_hit.point_value
            bullet_to_remove = id
    if bullet_to_remove is not None:
        bullets.pop(bullet_to_remove)

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
            ship.move(-constants.SHIP_SPEED, 0)
    elif keys[pygame.K_RIGHT]:
        ship.move(constants.SHIP_SPEED, 0)
    elif keys[pygame.K_UP]:
        ship.move(0, -constants.SHIP_SPEED)
    elif keys[pygame.K_DOWN]:
        ship.move(0, constants.SHIP_SPEED)

    # Firing key checks, can happen at the same time as movement
    if keys[pygame.K_SPACE]:
            # Start bullet, debounce fire to only fire one bullet
            current_time = time.time()
            if (len(bullets) < 2) and (current_time - globals[constants.LAST_FIRE_TIME] > constants.SHIP_FIRE_DELAY):
                globals[constants.LAST_FIRE_TIME] = time.time()
                globals[constants.BULLET_ID] += 1
                bullet_id = globals[constants.BULLET_ID]
                bullet = Bullet(window, ship.x + 20, ship.y - 20, constants.BULLET_SPEED, bullet_id)
                bullets[bullet_id] = bullet

    # Quit key check
    if keys[pygame.K_q]:
            pygame.quit()
            sys.exit()

def main():
    window = pygame.display.set_mode((constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    pygame.display.set_caption('Mike and Parker Space Invaders')
    pygame.init()

    # Initialize and draw objects

    # Draw the ship
    ship = Ship(window, 600, 600)

    # Draw the invaders
    fleet = InvaderFleet(window, 6, 10)

    # Init the score
    score = Score(window, 10, 20)

    # Initialize time
    last_time = time.time()
    while True:
        # Move cycle
        # Bullets move
        current_time = time.time()
        if current_time - constants.GAME_PACE > last_time:
            # Clear display buffer
            window.fill(constants.COLOR_WHITE)

            # Execute input
            execute_input(window, ship, bullets)

            # Move bullets
            id_to_remove = None
            for id in bullets:
                bullets[id].move()
                if bullets[id].getBulletBottomEdge() < 0:
                    # No need to undraw, bullet will disappear
                    id_to_remove = id
            if id_to_remove is not None:
                bullets.pop(id_to_remove)

            # If bullet hits an invader, then the invader disappears
            if len(bullets) > 0:
                check_invader_hit(fleet)

            # Move invaders
            fleet.move_invaders()

            # Refresh ship
            ship.draw()

            # Draw the score
            score.draw()

            last_time = current_time
            pygame.display.update()


main()
