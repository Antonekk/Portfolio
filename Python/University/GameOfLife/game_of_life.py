#Antoni Strasz

from matplotlib import pyplot as plt
import numpy as np
import random



ALIVE_CELL_COLOR = (255,255,255)
DEAD_CELL_COLOR = (0,0,0)

#Tworzy nowy grid na podstawie poprzedniego zgodzie z zasadami gry
def game_update(grid_helper: np.ndarray):
    new_grid = np.zeros((grid_helper.shape[0],grid_helper.shape[1],3))
    new_helper_grid = np.zeros(grid_helper.shape)

    for row, col in np.ndindex((grid_helper.shape[0],grid_helper.shape[1])):

        cell_status = grid_helper[row,col]
        neighbours_sum = np.sum(grid_helper[row-1:row+2,col-1:col+2]) - cell_status

        if (cell_status == 0 and neighbours_sum == 3) or (cell_status == 1 and (neighbours_sum in (2,3))):
            new_grid[row,col] = ALIVE_CELL_COLOR
            new_helper_grid[row,col] = 1
        else:
            new_grid[row,col] = DEAD_CELL_COLOR
            new_helper_grid[row,col] = 0

    return new_grid, new_helper_grid


#Generuje losowy board (wyświetlany i pomocniczy)
def gen_random_board(x: int,y: int):
    grid = np.zeros((x,y,3))
    grid_helper = np.zeros((x,y))
    for i in range(x):
        for j in range(y):
            if random.randint(0,5) == 1:
                grid[i,j] = ALIVE_CELL_COLOR if random.randint(0,10) == 1 else DEAD_CELL_COLOR
                grid_helper[i,j] = 1

    return grid,grid_helper

def game_of_life(x: int,y: int, generations: int):
    #Pomocniczy grid żeby łatwiej sprawdzać warunki
    grid,grid_helper = gen_random_board(x,y)
    plt.ion()
    for i in range(0,generations):
        imgplot = plt.imshow(grid)
        grid, grid_helper = game_update(grid_helper)
        plt.draw()
        plt.pause(0.001)
        plt.clf()


game_of_life(100,120, 100)

