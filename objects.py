import pygame, random
from settings import *

class Power:
    #power item setup
    def __init__(self, level, x, y):
        self.level = level
        self.rect = pygame.Rect(x, y, 32, 32)
        if random.random() < duck_chance: #if the randomly generated value is less than the perentage chance (5%) then it spawns a duck
            self.image = pygame.image.load('items/duck.png').convert_alpha() 
            self.duck = True #duck item/power up, used to handle collision
        elif random.random() < bomb_chance: #if the randomly generated value is less than the perentage chance (10%) then it spawns a bomb
            self.image = pygame.image.load('items/bomb.png').convert_alpha()
            self.duck = False 
            self.bomb = True #bomb used to handle collision
        else:
            self.image = pygame.image.load('items/power.png').convert_alpha()
            self.duck = False 
            self.bomb = False #normal power as its neither

    def draw(self, surface):
            surface.blit(self.image, self.rect.topleft) #draw power

class Objects():
    #key item setup/spawn
    occupied_positions = set() #class variable to track occupied positions

    def __init__(self, level):
        self.level = level
        self.rect = pygame.Rect(0, 0, 32, 32)

        if level.level_number in range(1, 4): #changes the sprite based on the level, as different key sprites depend on level
            self.image = pygame.image.load('items/key.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
            self.spawn_positions = [(200, 200)] #define fixed spawn positions based on the level x,y     
        elif level.level_number == 5:
            self.image = pygame.image.load('items/key3.png').convert_alpha()
            self.spawn_positions = [(304, 176)]     
        elif level.level_number == 6:
            self.image = pygame.image.load('items/key3.png').convert_alpha()
            self.spawn_positions = [(320, 128)]   
        self.spawn()

    def spawn(self):
        #available spawn checker
        available_positions = [pos for pos in self.spawn_positions if pos not in Objects.occupied_positions] #chekcs list to see if the spawn is set to taken
        
        if available_positions: #checks to see any open spawns
            self.position = random.choice(available_positions) #randomly picks an available spawn
            self.rect.center = self.position #moves to spawn position
            Objects.occupied_positions.add(self.position) #sets that spawn to taken in the list
        
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
