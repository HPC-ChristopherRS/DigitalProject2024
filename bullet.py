import pygame
import math
from settings import *
from enemy import *

class Bullet:
    def __init__(self, x, y):
        self.pos = (x, y)
        self.mx, self.my = pygame.mouse.get_pos()
        self.dir = (self.mx - x, self.my - y)
        self.length = math.hypot(*self.dir)
        if self.length == 0.0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / self.length, self.dir[1] / self.length)
        self.angle = math.degrees(math.atan2(-self.dir[1], self.dir[0]))

        self.bullet = pygame.image.load('tiles/player_bullet.png').convert_alpha()
        self.bullet = pygame.transform.rotate(self.bullet, self.angle)
        self.rect = self.bullet.get_rect(center=self.pos)
        self.speed = 4

    def update(self):
        self.pos = (self.pos[0] + self.dir[0] * self.speed, 
                    self.pos[1] + self.dir[1] * self.speed)
        self.rect.center = self.pos 

    def draw(self, surf):
        surf.blit(self.bullet, self.rect)

    def check_collision(self, grid, tile_size):
        x, y = self.pos
        col = int(x // tile_size)
        row = int(y // tile_size)

        if 0 <= col < len(grid[0]) and 0 <= row < len(grid):
            if grid[row][col] == 1 or grid[row][col] == 2 or grid[row][col] == 3 or grid[row][col] == 4 or grid[row][col] == 5 or grid[row][col] == 6 or grid[row][col] == 7 or grid[row][col] == 8 or grid[row][col] == 9 or grid[row][col] == 10 or grid[row][col] == 11 or grid[row][col] == 12:
                return True
        return False


