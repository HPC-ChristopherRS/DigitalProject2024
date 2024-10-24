import pygame
from settings import *
from level import *
from inventory import *

import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, level, health):
        super().__init__()
        self.level = level
        self.health = health
        self.sprites = []
        self.sprites2 = []
        self.state = 1  #initial animation state
        self.is_animating = True
        self.current_sprite = 0
        self.click_time = None

        #load the images for the player animations
        self.sprites.append(pygame.image.load('jerry/jerry.png').convert_alpha())
        self.sprites.append(pygame.image.load('jerry/jerry.png').convert_alpha())
        self.sprites.append(pygame.image.load('jerry/jerry1.png').convert_alpha())
        self.sprites2.append(pygame.image.load('jerry/madjerry.png').convert_alpha())
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [100, 294] #player spawn for first level

    #animation, if False animation stops playing
    def animate(self):
        self.is_animating = True
        self.click_time = pygame.time.get_ticks() #save the time of last click
        self.state = 2 #sets player state to 2 on click

    def stop_animation(self):
        self.is_animating = False
        self.current_sprite = 0

    def update_self(self):
        #idle animation
        current_time = pygame.time.get_ticks()

        #check time since last click
        if self.click_time is not None and current_time - self.click_time >= 250:
            self.state = 1 #after 0.25s goes back to idle animation
            self.click_time = None #resets last click time

        #handle animation for state 1 (idle)
        if self.state == 1:
            if self.is_animating:
                self.current_sprite += 0.05
                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0
                self.image = self.sprites[int(self.current_sprite)]

        #handle animation for state 2 (shooting)
        elif self.state == 2:
            if self.is_animating:
                self.current_sprite += 0.05
                if self.current_sprite >= len(self.sprites2):
                    self.current_sprite = 0
                self.image = self.sprites2[int(self.current_sprite)]

    #movement handling, moves players dx and dy values, calling collision detection function to ensure they don't go through walls
    def move(self, dx, dy):
        self.rect.x += dx * 1.5
        self.check_collision(dx, 0)
        self.rect.y += dy * 1.5
        self.check_collision(0, dy)

    #checks level grid for walls, if a wall is in the way the player will not move
    def check_collision(self, dx, dy):
        grid = self.level.get_grid() 
        for row in range(len(grid)):
            for column in range(len(grid[0])):
                if grid[row][column] in range (1,15): #range of tiles, 1-15, 0 is background so player glitches out of the level
                    wall_rect = pygame.Rect(
                        (MARGIN + WIDTH) * column + MARGIN, 
                        (MARGIN + HEIGHT) * row + MARGIN, 
                        WIDTH, HEIGHT
                    )
                    if self.rect.colliderect(wall_rect):
                        if dx > 0: #right
                            self.rect.right = wall_rect.left
                        if dx < 0: #left
                            self.rect.left = wall_rect.right
                        if dy > 0: #down
                            self.rect.bottom = wall_rect.top
                        if dy < 0: #up
                            self.rect.top = wall_rect.bottom
   
                        if grid[row][column] in [2, 3, 14]: #tiles that player can interact with with a key
                            key = 'items/key.png' if grid[row][column] == 2 else 'items/key1.png' if grid[row][column] == 3 else 'items/key2.png' #checks to see if key is held and if the player is touching the aliging tile
                            if key in items:
                                self.level.load_level(self.level.level_number + 1) #increases level number by 1
                                event = pygame.event.Event(CUSTOM_EVENT)
                                pygame.event.post(event) #runs the event to update the level code in the mainloop

    #dash handling, checks direction from main and moves the player rect in the corresponding direction
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

        steps = 10 #steps to break the dash into, so it doesn't directly teleport to the new postition as you could teleport through walls (op)
        dx = (new_rect.x - self.rect.x) / steps
        dy = (new_rect.y - self.rect.y) / steps

        #checks if the new rect is within the bounds of the level
        for _ in range(steps):
            if 0 <= self.rect.x + dx <= 620 and 0 <= self.rect.y + dy <= 620:
                #move incrementally checking for collisions at each step
                self.rect.x += dx
                self.check_collision(dx, 0)
                self.rect.y += dy
                self.check_collision(0, dy)
            else:
                break #movement stops if player is out of bounds or collision is detected

    #draws the player surface
    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)