import pygame
import math
from settings import *

class Bullet:
    def __init__(self, x, y):
        self.pos = (x, y)
        mx, my = pygame.mouse.get_pos()
        self.dir = (mx - x, my - y)
        length = math.hypot(*self.dir)
        if length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / length, self.dir[1] / length)
        angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pygame.Surface((10, 10)).convert_alpha()
        self.bullet.fill((255, 255, 255))
        self.bullet = pygame.transform.rotate(self.bullet, angle)
        self.speed = 5

    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed, 
                    self.pos[1] + self.dir[1] * self.speed)

    def draw(self, surf):
        bullet_rect = self.bullet.get_rect(center=self.pos)
        surf.blit(self.bullet, bullet_rect)

    def check_collision(self, grid, tile_size):
        x, y = self.pos
        col = int(x // tile_size)
        row = int(y // tile_size)

        if 0 <= col < len(grid[0]) and 0 <= row < len(grid):
            if grid[row][col] == 1 or grid[row][col] == 2:
                return True
        return False

