from numpy import true_divide
from graphics import *
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
bullets = []
invaders = []

class Bullet:
    x = 0
    y = 0
    speed = 0
    graphic: Rectangle

    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.graphic = Rectangle(Point(x-5, y-10), Point(x+5, y+10))
    
    def draw(self, win):
        self.graphic.draw(win)

    def remove(self):
        self.graphic.undraw()

    def move(self):
        self.y -= BULLET_SPEED
        self.graphic.move(0, -BULLET_SPEED)

class Invader:
    alive: bool = False
    x: int = 0
    y: int = 0
    graphic: Rectangle

    def __init__(self, x, y):
      self.x = x
      self.y = y
      graphic = Rectangle(Point(x, y), Point(x+25, y+25))
      graphic.setOutline('blue')
      graphic.setFill('blue')
      self.graphic = graphic
      self.alive = True

class InvaderFleet:
    direction: int = INVADER_SPEED
    fleet_offset: int = INVADER_START_OFFSET
    invaders = []
    invader_rows: int = 0
    invader_num_per_row: int = 0

    def __init__(self, rows: int, num_per_row: int):
        self.invader_rows = rows
        self.invader_num_per_row = num_per_row
        self.make_invaders()

    def make_invaders(self):
        for y in range(self.invader_rows):
            self.invaders.append([])
            for x in range(self.invader_num_per_row):
                invader_x = INVADER_START_OFFSET + x * (INVADER_SIZE + INVADER_SPACING)
                invader_y = INVADER_START_OFFSET + y * (INVADER_SIZE + INVADER_SPACING)
                invader = Invader(invader_x, invader_y)
                self.invaders[y].append(invader)

    def draw_invaders(self, win):
        for row in self.invaders:
            for invader in row:
                invader.graphic.draw(win)

    def move_invaders(self):
        invader_right_edge = self.fleet_offset + self.invader_num_per_row * (INVADER_SIZE + self.direction)
        # Check if invaders are at right edge
        if invader_right_edge > WINDOW_WIDTH - INVADER_START_OFFSET:
            self.direction = -INVADER_SPEED
        # Check if invaders are at left edge

        for y in range(self.invader_rows):
            for x in range(self.invader_num_per_row):
                self.invaders[y][x].x += self.direction
                self.invaders[y][x].graphic.move(self.direction, 0)
        self.fleet_offset += INVADER_SPACING

class Ship:
    alive = True
    x = 0
    y = 0
    graphic: Circle

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.graphic = Circle(Point(x, y), 25)
    
    def draw(self, win: GraphWin):
        self.graphic.draw(win)

    def move(self, offset_x, offset_y):
        self.x = self.x + offset_x
        self.y = self.y + offset_y
        self.graphic.move(offset_x, offset_y)

ship = Ship(600, 600)
def main():
    win = GraphWin('Space Invaders', WINDOW_WIDTH, WINDOW_HEIGHT)

    # Draw the ship
    ship.draw(win)  

    # Draw the invaders
    fleet = InvaderFleet(6, 10)
    fleet.draw_invaders(win)

    # Initialize time
    last_time = time.time()
    while True:
        # Move cycle
        # Bullets move
        current_time = time.time()
        if current_time - GAME_PACE < last_time:
            # Move bullets
            for bullet in bullets:
                bullet.move()
                if bullet.y < 0:
                    bullet.remove()
                    bullets.remove(bullet)
        # Invaders moving
        if current_time - GAME_PACE * 3 < last_time:
            fleet.move_invaders()

        k = win.checkKey()

        if(k):
            print('Key pressed: ' + k)

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
                bullet = Bullet(ship.x, ship.y - 20, BULLET_SPEED)
                bullets.append(bullet)
                bullet.draw(win)
        elif k == 'period' or k == 'q':
            break 
    win.close()

main()

