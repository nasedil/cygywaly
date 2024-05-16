# Example file showing a basic pygame "game loop"
import pygame

from world import World

# pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

world = World(100, 1)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    world.draw(screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        world.hero.lift = 2.2
    if keys[pygame.K_DOWN]:
        pass
    if keys[pygame.K_LEFT]:
        world.hero.push = -world.hero.speed_x / 4
    if keys[pygame.K_RIGHT]:
        world.hero.push = 0.2

    # flip() the display to put your work on screen
    pygame.display.flip()

    delta = clock.tick_busy_loop(60)  # limits FPS to 60
    world.proceed(delta / 1000)

pygame.quit()
