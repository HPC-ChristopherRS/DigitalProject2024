import pygame

#general variables with multiple uses between files
WIDTH, HEIGHT, MARGIN = 32, 32, 0 #grid tile size
COOLDOWN_TIME = 1000 #dash cooldown
DASH_DISTANCE = 100 #x/y distance for dash
speed = 2.5 #player speed
enemy_speed = 5
screen = pygame.display.set_mode((960, 640)) #screen size
health = 5 #player health
CUSTOM_EVENT = pygame.USEREVENT + 1 #custom event setup for level update
bomb_chance = 0.10 #10 chance of a bomb (they are very op as they clear everything on screen)
duck_chance = 0.05 #chance of spawning duck 1 = 100%, 0 = 0%
duck_item = 'items/duck.png'