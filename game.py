# Example file showing a basic pygame "game loop"
import pygame

from world import World

# pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True

world = World(10, 1)

position_x = 0
speed = 0.9
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    # RENDER YOUR GAME HERE
    world.draw(screen, position_x)
    pygame.draw.circle(screen, "red", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos.y -= 3 * speed
    if keys[pygame.K_DOWN]:
        player_pos.y += 3 * speed
    if keys[pygame.K_LEFT]:
        player_pos.x -= 3 * speed
    if keys[pygame.K_RIGHT]:
        player_pos.x += 3 * speed

    # flip() the display to put your work on screen
    pygame.display.flip()

    delta = clock.tick(60)  # limits FPS to 60
    position_x += speed * delta / 1000

pygame.quit()
