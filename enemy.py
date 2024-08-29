import pygame, random
from settings import *
from player import *

class Enemies:
    def __init__(self, level):
        self.level = level
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)
        self.rect.center = self.spawn_position()
        self.image = pygame.image.load('tiles/jerry.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        
    def spawn(self):    
       for row in range(len(self.level.grid)):
            for column in range(len(self.level.grid[0])):
                if self.level.grid[row][column] == 0:  
                    x = random.randint(500,500)
                    y = random.randint(500,500)
                    return (x, y)
                
    def spawn_position(self):
        for row in range(len(self.level.grid)):
            for column in range(len(self.level.grid[0])):
                if self.level.grid[row][column] == 0:  
                    x = random.randint(100,600)
                    y = random.randint(100,600)
                    return (x, y)
        
    def move_towards_player(self, player, speed):
        enemy_vector = pygame.Vector2(self.rect.center)
        player_vector = pygame.Vector2(player.rect.center)
        direction = player_vector - enemy_vector
        
        if direction.length() != 0:
            towards = direction.normalize()
            potential_rect = self.rect.move(towards * speed)
            if not self.check_collision(potential_rect):
                self.rect.center += towards * speed
        
    def collide_player(self, player):
        if self.rect.colliderect(player.rect):
            self.rect.center = self.spawn()
        
    def check_collision(self, rect=None):
        if rect is None:
            rect = self.rect
            
        for row in range(len(self.level.grid)):
            for column in range(len(self.level.grid[0])):
                if self.level.grid[row][column] == 1 or self.level.grid[row][column] == 2:
                    wall_rect = pygame.Rect(
                        (MARGIN + WIDTH) * column + MARGIN, 
                        (MARGIN + HEIGHT) * row + MARGIN, 
                        WIDTH, HEIGHT)
                    
                    if rect.colliderect(wall_rect):
                        if rect.left < wall_rect.right:
                            rect.x -= 3
                        if rect.right > wall_rect.left:
                            rect.x += 3
                        if rect.top < wall_rect.bottom:
                            rect.y -= 3
                        if rect.bottom > wall_rect.top:
                            rect.y += 3  
                        return True
        return False
                    
    def recheck_collisions_on_level_change(self, new_level):
        self.level = new_level
        self.rect.center = self.spawn_position()

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
        
    