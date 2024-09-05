import pygame
from settings import *

class Player:
    def __init__(self, level, health):
        self.level = level
        self.rect = pygame.Rect(100, 100, WIDTH, HEIGHT)
        self.image = pygame.image.load('tiles/jerry.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.health = 5

    def move(self, dx, dy):
        self.rect.x += dx * 1.5
        self.check_collision(dx, 0)
        self.rect.y += dy * 1.5
        self.check_collision(0, dy)

    def check_collision(self, dx, dy):
        grid = self.level.get_grid() 
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column] == 1 or grid[row][column] == 2:
                    wall_rect = pygame.Rect(
                        (MARGIN + WIDTH) * column + MARGIN, 
                        (MARGIN + HEIGHT) * row + MARGIN, 
                        WIDTH, HEIGHT
                    )
                    if self.rect.colliderect(wall_rect):
                        if dx > 0:  # Right
                            self.rect.right = wall_rect.left
                        if dx < 0:  # Left
                            self.rect.left = wall_rect.right
                        if dy > 0:  # Down
                            self.rect.bottom = wall_rect.top
                        if dy < 0:  # Up
                            self.rect.top = wall_rect.bottom

    def dash(self, direction):
        new_rect = self.rect.copy()
        if direction == 'right':
            new_rect.x += DASH_DISTANCE
        elif direction == 'left':
            new_rect.x -= DASH_DISTANCE
        elif direction == 'down':
            new_rect.y += DASH_DISTANCE
        elif direction == 'up':
            new_rect.y -= DASH_DISTANCE
        elif direction == 'up-right':
            new_rect.x += DASH_DISTANCE
            new_rect.y -= DASH_DISTANCE
        elif direction == 'up-left':
            new_rect.x -= DASH_DISTANCE
            new_rect.y -= DASH_DISTANCE
        elif direction == 'down-right':
            new_rect.x += DASH_DISTANCE
            new_rect.y += DASH_DISTANCE
        elif direction == 'down-left':
            new_rect.x -= DASH_DISTANCE
            new_rect.y += DASH_DISTANCE

        if 0 <= new_rect.x <= 620 and 0 <= new_rect.y <= 620:
            self.check_collision(new_rect.x - self.rect.x, new_rect.y - self.rect.y)
            self.rect = new_rect

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
