import pygame
from settings import *

GRID_SIZE = 3
CELL_SIZE = 225 // GRID_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

#item list, appending items adds to the inventory :D
items = []
#9 item list so it can return 9 as an enumerate cuz too lazy to adjust code :3
cell = [1,2,3,4,5,6,7,8,9]
def inventory_grid():

    #Loop through the items returning an enumerate object and draw them
    for i, item in enumerate(cell):
        #Calculate size of rows and columns
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        
        #Calculate position to draw the cellgrid
        x = col * CELL_SIZE +685
        y = row * CELL_SIZE +310
        
        image = pygame.image.load('tiles/in.png')
        image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE)) #change size of the cellbackground
        screen.blit(image, (x, y)) #draw the cell/background

    #reused code from cells
    for i, item in enumerate(items):
        row = i // GRID_SIZE
        col = i % GRID_SIZE
        
        x = col * CELL_SIZE +685
        y = row * CELL_SIZE +310

        image = pygame.image.load(item)
        image = pygame.transform.scale(image, (CELL_SIZE, CELL_SIZE))
        screen.blit(image, (x, y))

