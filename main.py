from numpy import true_divide
from graphics import *
import time

BULLET_SPEED = 25 # 25px
GAME_PACE = 300 # 300ms
MOVE_STEP_SIZE = 15 # 10px
INVADER_SIZE = 25 # 25px
INVADER_START_OFFSET = 100 # 100px
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
    alive = False
    x = 0
    y = 0
    graphic: Rectangle

    def __init__(self, x, y):
      self.x = x
      self.y = y
      graphic = Rectangle(Point(x, y), Point(x+25, y+25))
      graphic.setOutline('blue')
      graphic.setFill('blue')
      self.graphic = graphic
      self.alive = True

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

def make_invaders(rows: int, num_per_row: int):
    for y in range(rows):
        invaders.append([])
        for x in range(num_per_row):
            invader_x = INVADER_START_OFFSET + x * (INVADER_SIZE + 10)
            invader_y = INVADER_START_OFFSET + y * (INVADER_SIZE + 10)
            invader = Invader(invader_x, invader_y)
            invaders[y].append(invader)

def draw_invaders(win):
    for row in invaders:
        for invader in row:
            invader.graphic.draw(win)

ship = Ship(600, 600)
def main():
    win = GraphWin('Space Invaders', 1200, 800)

    # Draw the ship
    ship.draw(win)  

    # Draw the invaders
    make_invaders(8, 20)
    draw_invaders(win)

    # Initialize time
    last_time = time.time()
    while True:
        # Move cycle
        current_time = time.time()
        if current_time - GAME_PACE < last_time:
            # Move bullets
            for bullet in bullets:
                bullet.move()
                if bullet.y < 0:
                    bullet.remove()
                    bullets.remove(bullet)

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

