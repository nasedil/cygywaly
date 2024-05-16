from random import uniform, randint

import pygame
import pygame.gfxdraw

STAR_DENSITY = 1000
STAR_RADIUS = 0.005
HEIGHT = 1
VIEW_WIDTH = 2

class World(object):
    def __init__(self, length, difficulty):
        self.length = length
        self.difficulty = difficulty
        self.back_stars = []
        self.back_color = (10, 2, 15)
        self.back_stars_color = [200 for i in range(3)]
        self.blink_range = 50
        self.generate()

    def generate(self):
        self.back_stars = [(uniform(0, self.length), uniform(-HEIGHT, HEIGHT), uniform(0.5, 10))
                           for i in range(int(STAR_DENSITY*self.length))]

    def draw(self, surface, position_x):
        window_width, window_height = pygame.display.get_window_size()
        scale = window_width / VIEW_WIDTH
        VIEW_HEIGHT = window_height / scale
        for star in self.back_stars:
            x = (star[0] - position_x) / star[2] + (VIEW_WIDTH / 2)
            y = star[1] / star[2] + (VIEW_HEIGHT / 2)
            radius = STAR_RADIUS / star[2]
            color = [i + randint(0, self.blink_range) for i in self.back_stars_color]
            pygame.draw.circle(surface, color, (x*scale, window_height-y*scale), radius*scale)
            #pygame.gfxdraw.filled_circle(surface, int(x*scale), int(star[1]*scale), int(radius*scale), color)