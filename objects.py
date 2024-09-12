import pygame, random
from settings import *

class Object():
    def __init__(self, level):
        self.level = level
        self.rect = pygame.Rect(0, 0, 26, 26)
        self.rect.center = self.spawn_position()
        self.image = pygame.image.load('items/power.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        
    def spawn_position(self):
        for row in range(len(self.level.grid)):
            for column in range(len(self.level.grid[0])):
                if self.level.grid[row][column] == 0:  
                    x = random.randint(20,600)
                    y = random.randint(20,600)
                    return (x, y)
        
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)