import pygame
import math
from settings import *

class Enemies:
    def __init__(self, level):
        self.rect = pygame.Rect(200, 200, WIDTH, HEIGHT)
        self.rect.center = (WIDTH, HEIGHT)
        self.level = level
        
    def move_towards_player(self, player):
        enemy_vector = pygame.Vector2(self.rect.center)
        player_vector = pygame.Vector2(player.rect.center)
        direction = player_vector - enemy_vector
        if direction.length() != 0:
            towards = direction.normalize()
            self.rect.center += towards * speed
        else:
            pass
        
    def collide_player(self, player):
        if self.rect.colliderect(player):
            self.rect = pygame.Rect(200, 200, WIDTH, HEIGHT)
        else:
            pass
        
    def check_collision(self):
        for row in range(len(self.level.grid)):
            for column in range(len(self.level.grid[0])):
                if self.level.grid[row][column] == 1:
                    wall_rect = pygame.Rect((MARGIN + WIDTH) * column + MARGIN, (MARGIN + HEIGHT) * row + MARGIN, WIDTH, HEIGHT)
                    if self.rect.colliderect(wall_rect):
                        self.rect = pygame.Rect(200, 200, WIDTH, HEIGHT)
                    else:
                        pass