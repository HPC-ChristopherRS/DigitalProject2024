import pygame
from settings import *

class Level:
    def __init__(self, level_number):
        self.level_number = level_number
        self.grid = self.create_grid()

    def create_grid(self):
        grid = [[0] * 20 for _ in range(20)]
        for row in range(20):
            grid[0][row] = grid[row][0] = grid[19][row] = grid[row][19] = 1

        if self.level_number == 1:
            for column in range(8, 12):
                grid[4][column] = 1

        if self.level_number == 2:
            for column in range(8, 12):
                grid[6][column] = 1
        return grid

    def load_level(self, level_number):
        self.level_number = level_number
        self.grid = self.create_grid()

    def get_grid(self):
        return self.grid

