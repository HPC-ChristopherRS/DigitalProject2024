import pygame
from settings import *

# <3 texture imports <3 #
textures = {
    #textures are asigned a number to be used in the grids array
    1: pygame.image.load('tiles/rock_wall.png').convert(),
    2: pygame.image.load('tiles/keyhole.png').convert(),
    3: pygame.image.load('tiles/keyhole1.png').convert(),
    4: pygame.image.load('tiles/wall_right_1.png').convert(),
    5: pygame.image.load('tiles/wall_right_2.png').convert(),
    6: pygame.image.load('tiles/wall_top_1.png').convert(),
    7: pygame.image.load('tiles/wall_top_2.png').convert(),
    8: pygame.image.load('tiles/wall_bottom_1.png').convert(),
    9: pygame.image.load('tiles/wall_bottom_2.png').convert(),
    10: pygame.image.load('tiles/wall_left_1.png').convert(),
    11: pygame.image.load('tiles/wall_left_2.png').convert(),
    12: pygame.image.load('tiles/blank_wall.png').convert(),
    13: pygame.image.load('tiles/tv.png').convert_alpha(),
    14: pygame.image.load('tiles/keyhole2.png').convert_alpha(),
    }

#background image imports
background_image = pygame.image.load('tiles/rock_floor.png').convert()
background_image2 = pygame.image.load('tiles/floor2.png').convert()

#inventory icons import
jerry = pygame.image.load("jerry/jerry.png").convert()
power_png = pygame.image.load("items/power.png").convert()
bomb_png = pygame.image.load("items/bomb.png").convert()
coin_png = pygame.image.load("items/coin.png").convert()

#code that draws the level grid textures, collsions still work without this
def draw_grid(screen, level):
    grid = level.get_grid()
    #check level to set background tile
    if level.level_number == 2 or level.level_number == 3:
        #darws the textures ontop of the 20 by 20 grid
        for row in range(20):
            for column in range(20):
                tile_type = grid[row][column]
                tile_image = textures.get(tile_type, background_image)
            
                screen.blit(tile_image, 
                            [(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN])

    #check level to set background tile
    elif level.level_number ==1:
        #darws the textures ontop of the 20 by 20 grid
        for row in range(20):
            for column in range(20):
                tile_type = grid[row][column]
                tile_image = textures.get(tile_type, background_image2)
            
                screen.blit(tile_image, 
                            [(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN])
