from math import copysign
from random import uniform, randint

import pygame
import pygame.gfxdraw

STAR_DENSITY = 100
OBSTACLE_DENSITY = 2
OBSTACLE_SCALE = 0.1
STAR_RADIUS = 0.005
HEIGHT = 0.5
VIEW_WIDTH = 2

class Creature(object):
    def __init__(self, size):
        self.size = size
        self.x = 0
        self.y = 0
        self.speed_x = 0.03
        self.speed_y = 0
        self.lift = 0
        self.push = 0

class World(object):
    def __init__(self, length, difficulty):
        self.length = length
        self.difficulty = difficulty
        self.back_stars = []
        self.back_color = (10, 2, 15)
        self.back_stars_color = [100 for i in range(3)]
        self.blink_range = 30

        self.back_stars = [(uniform(0, self.length), uniform(-HEIGHT*10, HEIGHT*10), uniform(1, 10))
                           for i in range(int(STAR_DENSITY*self.length))]
        self.front_stars = [(uniform(0, self.length), uniform(-HEIGHT*10, HEIGHT*10), uniform(0.5, 1))
                           for i in range(int(STAR_DENSITY*self.length))]
        
        min_obstacle_size = OBSTACLE_SCALE*self.difficulty * 0.1
        self.obstacles = [(uniform(0, self.length), uniform(-HEIGHT*1, HEIGHT*1), uniform(min_obstacle_size, OBSTACLE_SCALE*self.difficulty))
                           for i in range(int(self.difficulty*OBSTACLE_DENSITY*self.length))]

        self.gravity = 1

        self.hero = Creature(size=0.1)
        
    def proceed(self, delta):
        self.hero.y += self.hero.speed_y * delta
        self.hero.x += self.hero.speed_x * delta
        self.hero.speed_x += self.hero.push * delta
        self.hero.speed_y += (self.hero.lift - self.gravity) * delta
        self.hero.lift = max(0, self.hero.lift-5*delta)
        self.hero.push = copysign(max(0, abs(self.hero.push)-0.19*delta), self.hero.push)

    def draw(self, surface):
        window_width, window_height = pygame.display.get_window_size()
        scale = window_width / VIEW_WIDTH
        VIEW_HEIGHT = window_height / scale
        
        for star in self.back_stars:
            x = (star[0] - self.hero.x) / star[2] + (VIEW_WIDTH / 2)
            y = star[1] / star[2] + (VIEW_HEIGHT / 2)
            radius = STAR_RADIUS / star[2]
            color = [i + randint(0, self.blink_range) for i in self.back_stars_color]
            pygame.draw.circle(surface, color, (x*scale, window_height - y*scale), radius*scale)
        
        for obstacle in self.obstacles:
            x = (obstacle[0] - self.hero.x) + (VIEW_WIDTH / 2)
            y = obstacle[1] + (VIEW_HEIGHT / 2)
            pygame.draw.circle(surface, "brown", (x*scale, window_height - y*scale), obstacle[2]*scale)
        
        y = HEIGHT + (VIEW_HEIGHT / 2)
        pygame.draw.rect(surface, "brown", (0, 0, window_width, window_height - y*scale))
        y = -HEIGHT + (VIEW_HEIGHT / 2)
        pygame.draw.rect(surface, "brown", (0, window_height - y*scale, window_width, window_height))

        x = VIEW_WIDTH / 2
        y = self.hero.y + (VIEW_HEIGHT / 2)
        pygame.draw.circle(surface, "magenta", (x*scale, window_height - y*scale), self.hero.size*scale)

        for star in self.front_stars:
            x = (star[0] - self.hero.x) / star[2] + (VIEW_WIDTH / 2)
            y = star[1] / star[2] + (VIEW_HEIGHT / 2)
            radius = STAR_RADIUS / star[2]
            color = [i + randint(0, self.blink_range) for i in self.back_stars_color]
            pygame.draw.circle(surface, color, (x*scale, window_height - y*scale), radius*scale)