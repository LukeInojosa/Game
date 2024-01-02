import matplotlib.pyplot as plt
import numpy as np
import random
from queue import Queue
def create_maze(dim,start):
    # Create a grid filled with walls
    maze = np.zeros((dim*2+1, dim*2+1))

    # Define the starting point
    x, y = start
    maze[2*x+1, 2*y+1] = 1

    # Initialize the stack with the starting point
    stack = [(x, y)]
    while len(stack) > 0:
        x, y = stack[-1]

        # Define possible directions
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if nx >= 0 and ny >= 0 and nx < dim and ny < dim and maze[2*nx+1, 2*ny+1] == 0:
                maze[2*nx+1, 2*ny+1] = 1
                maze[2*x+1+dx, 2*y+1+dy] = 1
                stack.append((nx, ny))
                break
        else:
            stack.pop()
            
    # Create an entrance and an exit
    maze[ start] = 1
    maze[-2, -1] = 1

    return maze

