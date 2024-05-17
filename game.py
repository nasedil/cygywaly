# Example file showing a basic pygame "game loop"
import pygame

from world import World

# pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

level = 1
lost = False
world = None

font = pygame.font.SysFont('sans', 30)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not world or world.finished:
        world = World(10 + 5 * level/10, level)
        message = font.render('Level ' + str(level), True, 'white', None)
        level += 1

    world.draw(screen)
    screen.blit(message, (0, 0))

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

    if world.dead:
        lost = True

    pygame.display.flip()

    delta = clock.tick_busy_loop(60)
    world.proceed(delta / 1000)

pygame.quit()
