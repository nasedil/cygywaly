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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    world.draw(screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        running = False
    if keys[pygame.K_UP] and not world.is_hit:
        world.hero.lift = 2.2
    if keys[pygame.K_DOWN]:
        world.hero.lift /= 2
    if keys[pygame.K_LEFT] and not world.is_hit:
        world.hero.push = -world.hero.speed_x / 4
    if keys[pygame.K_RIGHT] and not world.is_hit:
        world.hero.push = 0.2

    pygame.display.flip()

    delta = clock.tick_busy_loop(60)
    world.proceed(delta / 1000)

pygame.quit()
