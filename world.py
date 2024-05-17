from collections import deque
import math
from math import copysign, atan2, sqrt
from random import uniform, randint

import pygame
import pygame.gfxdraw
from math import cos
from math import sin

STAR_DENSITY = 100
OBSTACLE_DENSITY = 1
OBSTACLE_SCALE = 0.1
STAR_RADIUS = 0.005
HEIGHT = 0.5
VIEW_WIDTH = 2

class Creature(object):
    def __init__(self, size):
        self.size = size
        self.x = -1
        self.y = 0
        self.speed_x = 0.03
        self.speed_y = 0
        self.lift = 0
        self.push = 0
        self.tail = deque(maxlen=10)
        self.blood = []

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
        
        min_obstacle_size = OBSTACLE_SCALE*self.difficulty * 0.2
        self.obstacles = [(uniform(0, self.length), uniform(-HEIGHT*1, HEIGHT*1), uniform(min_obstacle_size, OBSTACLE_SCALE*self.difficulty))
                           for i in range(int(self.difficulty*OBSTACLE_DENSITY*self.length))]

        self.gravity = 1

        self.hero = Creature(size=0.07)

        self.is_hit = False
        
    def proceed(self, delta):
        self.hero.y += self.hero.speed_y * delta
        self.hero.x += self.hero.speed_x * delta
        self.hero.speed_x = max(0, self.hero.speed_x)
        self.hero.speed_x += self.hero.push * delta
        self.hero.speed_y += (self.hero.lift - self.gravity) * delta
        self.hero.lift = max(0, self.hero.lift-5*delta)
        self.hero.push = copysign(max(0, abs(self.hero.push)-0.19*delta), self.hero.push)
        self.hero.tail.append(atan2(self.hero.speed_y, self.hero.speed_x))

        if self.is_hit:
            for blood_drop in self.hero.blood:
                blood_drop[1] += blood_drop[3] * delta
                blood_drop[0] += blood_drop[2] * delta
                blood_drop[1] -= self.gravity * delta
            angle = uniform(0, math.pi*2)
            speed = uniform(0.1, 0.5)
            self.hero.blood.append([self.hero.x, self.hero.y, cos(angle)*speed, sin(angle)*speed])
            return

        self.is_hit = self.test_hit()
        if self.is_hit:
            self.hero.lift = 0
            self.hero.push = -1
            self.hero.speed_y *= -1
            self.hero.speed_x *= 0

    def test_hit(self):
        for obstacle in self.obstacles:
            if ((self.hero.x - obstacle[0]) ** 2 + (self.hero.y - obstacle[1]) ** 2) < (obstacle[2] + self.hero.size) ** 2:
                self.is_hit = True
                return True
        if abs(self.hero.y) + self.hero.size > HEIGHT:
            self.is_hit = True
            return True
        return False

    def draw(self, surface):
        window_width, window_height = pygame.display.get_window_size()
        scale = window_width / VIEW_WIDTH
        VIEW_HEIGHT = window_height / scale

        surface.fill(self.back_color)
        
        for star in self.back_stars:
            x = (star[0] - self.hero.x) / star[2] + (VIEW_WIDTH / 2)
            y = star[1] / star[2] + (VIEW_HEIGHT / 2)
            radius = STAR_RADIUS / star[2]
            color = [i + randint(0, self.blink_range) for i in self.back_stars_color]
            pygame.draw.circle(surface, color, (x*scale, window_height - y*scale), radius*scale)

        x = VIEW_WIDTH / 2
        y = self.hero.y + (VIEW_HEIGHT / 2)
        color = [200, 110, 180] if self.is_hit else [180, 110, 220]
        pygame.draw.circle(surface, color, (x*scale, window_height - y*scale), self.hero.size*scale)
        radius = self.hero.size
        stretch = 0.1 + sqrt(self.hero.push ** 2 + (self.hero.lift - self.gravity) ** 2) / 1.7 + sqrt(self.hero.speed_x ** 2 + self.hero.speed_y ** 2) / 2.5
        for angle in self.hero.tail:
            x = x - radius * cos(angle) * stretch
            y = y - radius * sin(angle) * stretch
            radius /= 2
            pygame.draw.circle(surface, color, (x*scale, window_height - y*scale), radius*scale)
        for blood_drop in self.hero.blood:
            x = blood_drop[0] - self.hero.x + (VIEW_WIDTH / 2)
            y = blood_drop[1] + (VIEW_HEIGHT / 2)
            pygame.draw.circle(surface, "red", (x*scale, window_height - y*scale), self.hero.size*scale/10)

        color = (50, 60, 20)
        for obstacle in self.obstacles:
            x = (obstacle[0] - self.hero.x) + (VIEW_WIDTH / 2)
            y = obstacle[1] + (VIEW_HEIGHT / 2)
            pygame.draw.circle(surface, color, (x*scale, window_height - y*scale), obstacle[2]*scale)

        for star in self.front_stars:
            x = (star[0] - self.hero.x) / star[2] + (VIEW_WIDTH / 2)
            y = star[1] / star[2] + (VIEW_HEIGHT / 2)
            radius = STAR_RADIUS / star[2]
            color = [i + randint(0, self.blink_range) for i in self.back_stars_color]
            pygame.draw.circle(surface, color, (x*scale, window_height - y*scale), radius*scale)

        color = (50, 60, 20)
        y = HEIGHT + (VIEW_HEIGHT / 2)
        pygame.draw.rect(surface, color, (0, 0, window_width, window_height - y*scale))
        y = -HEIGHT + (VIEW_HEIGHT / 2)
        pygame.draw.rect(surface, color, (0, window_height - y*scale, window_width, window_height))