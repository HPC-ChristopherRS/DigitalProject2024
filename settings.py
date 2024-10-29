import pygame

#general variables with multiple uses between files
WIDTH, HEIGHT, MARGIN = 32, 32, 0 #grid tile size
COOLDOWN_TIME = 2000 #dash cooldown
DASH_DISTANCE = 100 #x/y distance for dash
speed = 2.5 #enemy speed
screen = pygame.display.set_mode((960, 640)) #screen size
CUSTOM_EVENT = pygame.USEREVENT + 1 #custom event setup for level update
CUSTOM_EVENT2 = pygame.USEREVENT + 1 #custom event setup for level update
bomb_chance = 0.10 #10 chance of a bomb (they are very op as they clear everything on screen)
duck_chance = 0.05 #chance of spawning duck 1 = 100%, 0 = 0%
