from random import uniform, randint

import pygame
import pygame.gfxdraw

STAR_DENSITY = 1000
STAR_RADIUS = 0.02
HEIGHT = 1
VIEW_WIDTH = 2

class World(object):
    def __init__(self, length, difficulty):
        self.length = length
        self.difficulty = difficulty
        self.back_stars = []
        self.back_color = (0, 0, 0)
        self.back_stars_color = (randint(50, 250), randint(50, 250), randint(50, 250), 128)
        self.generate()

    def generate(self):
        self.back_stars = [(uniform(0, self.length), uniform(0, HEIGHT), uniform(0.5, 10))
                           for i in range(int(STAR_DENSITY*self.length))]

    def draw(self, surface, position_x):
        window_width, _ = pygame.display.get_window_size()
        scale = window_width / VIEW_WIDTH
        for star in self.back_stars:
            x = (star[0] - position_x) / star[2] + (VIEW_WIDTH / 2)
            radius = STAR_RADIUS / star[2]
            color = (randint(50, 250), randint(50, 250), randint(50, 250), 128)
            #pygame.draw.circle(surface, self.back_stars_color, (x*scale, star[1]*scale), radius*scale)
            pygame.gfxdraw.filled_circle(surface, int(x*scale), int(star[1]*scale), int(radius*scale), color)