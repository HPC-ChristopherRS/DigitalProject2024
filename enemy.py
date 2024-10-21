import pygame
import random
from main import *
from settings import *
from player import *
from bullet import *

class Enemies:
    occupied_positions = set() #class variable to track occupied positions

    def __init__(self, level, health):
        self.level = level
        self.rect = pygame.Rect(0, 0, WIDTH, HEIGHT)

        #define fixed spawn positions based on the level
        if level.level_number == 1:
            self.spawn_positions = [(500, 200), (500, 200), (500, 200)] #if the number of enemies exceeds spawn pos amount, they spawn at 0,0
        elif level.level_number == 2:
            self.spawn_positions = [(555, 200), (600, 200), (650, 200)]
        elif level.level_number == 3:
            self.spawn_positions = [(555, 100), (555, 200), (555, 300), (555, 400), (555, 500), (555, 600)]
        elif level.level_number == 4:
            self.spawn_positions = [(555, 100), (555, 200), (555, 300), (555, 400), (555, 500), (555, 600)]

        self.image = pygame.image.load('jerry/jerrbear.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.health = 5
        self.spawn()

    def spawn(self):
        #available spawn checker
        available_positions = [pos for pos in self.spawn_positions if pos not in Enemies.occupied_positions]
        
        if available_positions: #check to see any open spawns
            self.position = random.choice(available_positions) #randomly picks an available spawn
            self.rect.center = self.position
            Enemies.occupied_positions.add(self.position) #sets that spawn to taken
            self.is_spawned = True #spawns

    #moves the enemy towards the play by finding the distance between them and minusing them, normalising to ensure they move at a constant speed towards the player
    def move_towards_player(self, player, speed):
        #vector of enemies pos
        enemy_vector = pygame.Vector2(self.rect.center)
        #vector of players pos
        player_vector = pygame.Vector2(player.rect.center)
        #direction vector is found by minusing enemy from player
        direction = player_vector - enemy_vector
        
        #checks to see if the length is 0, because normalising by 0 is undefined
        if direction.length() != 0:
            self.towards = direction.normalize()
            self.potential_rect = self.rect.move(self.towards * speed)
            #checks for collisons, if none are found the enemy moves towards the player, needed for proper wall collisions
            if not self.check_collision(self.potential_rect):
                self.rect.center += self.towards * speed

    #checks collision and then damages the player
    def collide_player(self, player):
        if self.rect.colliderect(player.rect):
            player.health -= 1
            print(player.health)
            if player.health == 0:
                pass

    #checks for walls, if wall no move into wall, pushed out by 3. Checks the entire 20 by 20 2d array for walls, fun
    def check_collision(self, rect=None):
        if rect is None:
            rect = self.rect
            
        for row in range(len(self.level.grid)):
            for column in range(len(self.level.grid[0])):
                if self.level.grid[row][column] in range(1, 13): #range of tiles, 1-13
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

    #draws the enemy surface
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)
