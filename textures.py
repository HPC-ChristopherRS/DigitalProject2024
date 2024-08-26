import pygame 
from settings import *

#<3 texture imports <3#
wall_image = pygame.image.load('tiles/rock_wall.png').convert()
wall_image2 = pygame.image.load('tiles/wall2.png').convert()
pipe1 = pygame.image.load('tiles/pipe_bottom_left.png').convert()
background_image = pygame.image.load('tiles/rock_floor.png').convert()
wall_right_1 = pygame.image.load('tiles/wall_right_1.png').convert()
wall_right_2 = pygame.image.load('tiles/wall_right_2.png').convert()
wall_top_1 = pygame.image.load('tiles/wall_top_1.png').convert()
wall_top_2 = pygame.image.load('tiles/wall_top_2.png').convert()

def draw_grid(screen, level):
    for row in range(20):
        for column in range(20):
            if level.get_grid()[row][column] == 1:
                screen.blit(wall_image, 
                            [(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN])
                
            elif level.get_grid()[row][column] == 2:
                screen.blit(wall_image2, 
                            [(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN])
                
            elif level.get_grid()[row][column] == 3:
                screen.blit(pipe1, 
                            [(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN])
                
            elif level.get_grid()[row][column] == 4:
                screen.blit(wall_right_1, 
                            [(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN])
              
            elif level.get_grid()[row][column] == 5:
                screen.blit(wall_right_2, 
                            [(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN])
                
            elif level.get_grid()[row][column] == 6:
                screen.blit(wall_top_1, 
                            [(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN])
              
            elif level.get_grid()[row][column] == 7:
                screen.blit(wall_top_2, 
                            [(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN])

            else:
                screen.blit(background_image, 
                            [(MARGIN + WIDTH) * column + MARGIN,
                             (MARGIN + HEIGHT) * row + MARGIN])