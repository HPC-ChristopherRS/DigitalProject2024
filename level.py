import pygame
from settings import *

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.grid = self.create_grid()

    def create_grid(self):
        grid = [[0] * 20 for _ in range(20)]
        for row in range(20):
            grid[0][row] = grid[row][0] = grid[19][row] = grid[row][19] = grid[1][1] = grid[18][18] = grid[1][18] = grid[18][1] = 1

        if self.level_number == 1:
            for column in range(8, 12):
                grid[4][column] = 1
        return grid