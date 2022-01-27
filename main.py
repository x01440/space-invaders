import pygame
import sys
import time

# Local imports
import constants
import invader
import score_box
import ship
import weapon

bullets = {}
globals = {
    constants.BULLET_ID: 0,
    constants.GAME_SCORE: 0,
    constants.LAST_FIRE_TIME: 0
}
invaders = []

def check_invader_hit(fleet: invader.InvaderFleet):
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

def execute_input(window, spaceship: ship.Ship, bullets):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            print('Key pressed: ' + str(event.key))

    # Movement key check
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
            spaceship.move(-constants.SHIP_SPEED, 0)
    elif keys[pygame.K_RIGHT]:
        spaceship.move(constants.SHIP_SPEED, 0)
    elif keys[pygame.K_UP]:
        spaceship.move(0, -constants.SHIP_SPEED)
    elif keys[pygame.K_DOWN]:
        spaceship.move(0, constants.SHIP_SPEED)

    # Firing key checks, can happen at the same time as movement
    if keys[pygame.K_SPACE]:
            # Start bullet, debounce fire to only fire one bullet
            current_time = time.time()
            if (len(bullets) < 2) and (current_time - globals[constants.LAST_FIRE_TIME] > constants.SHIP_FIRE_DELAY):
                globals[constants.LAST_FIRE_TIME] = time.time()
                globals[constants.BULLET_ID] += 1
                bullet_id = globals[constants.BULLET_ID]
                bullet = weapon.Bullet(window, spaceship.x + 20, spaceship.y - 20, constants.BULLET_SPEED, bullet_id)
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
    spaceship = ship.Ship(window, 600, 600)

    # Draw the invaders
    fleet = invader.InvaderFleet(window, 6, 10)

    # Init the score
    score = score_box.Score(window, 10, 20)

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
            execute_input(window, spaceship, bullets)

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
            spaceship.draw()

            # Draw the score
            score.draw(str(globals[constants.GAME_SCORE]))

            last_time = current_time
            pygame.display.update()

main()
