import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import deque

EMPTY = 0
WALL = 1
START = 2
TARGET = 3

cmap = mcolors.ListedColormap(['white', 'black', 'cyan', 'magenta', 'yellow'])

grid = [
    [2,0,0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,0,1,0,0,0,0,0],
    [0,0,0,0,0,1,1,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,3,0,0],
    [0,0,1,1,1,1,1,1,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0]
]

start_pos = (0, 0)
target_pos = (9, 9)


def get_valid_neighbors(position, grid_matrix):
    row, col = position
    directions = [(-1,0),(0,1),(1,0),(1,1),(0,-1),(-1,-1)]
    valid_neighbors = []
    for d_row, d_col in directions:
        new_row, new_col = row + d_row, col + d_col
        if 0 <= new_row < len(grid_matrix) and 0 <= new_col < len(grid_matrix[0]) and grid_matrix[new_row][new_col] != WALL:
            valid_neighbors.append((new_row, new_col))
    return valid_neighbors


def bfs_visual(grid_matrix, start_node, goal_node):
    queue = deque([start_node])
    visited = set()
    parent_map = {}

    fig, ax = plt.subplots()
    plt.ion()

    while queue:
        current = queue.popleft()
        visited.add(current)

        if current != start_node and current != goal_node:
            grid_matrix[current[0]][current[1]] = 4  # mark explored

        if current == goal_node:
            # reset explored colors for a clean path display
            for r in range(len(grid_matrix)):
                for c in range(len(grid_matrix[0])):
                    if grid_matrix[r][c] == 4 or grid_matrix[r][c] == 5:
                        grid_matrix[r][c] = EMPTY

            # reconstruct path
            path = []
            node = goal_node
            while node != start_node:
                path.append(node)
                node = parent_map[node]
            path.append(start_node)
            path.reverse()

            for step in path:
                if step != start_node and step != goal_node:
                    grid_matrix[step[0]][step[1]] = 5  # mark final path
                ax.clear()
                ax.imshow(grid_matrix, cmap=cmap)
                plt.pause(0.1)

            plt.ioff()
            plt.show()
            return path

        for neighbor in get_valid_neighbors(current, grid_matrix):
            if neighbor not in visited and neighbor not in queue:
                parent_map[neighbor] = current
                queue.append(neighbor)

        ax.clear()
        ax.imshow(grid_matrix, cmap=cmap)
        plt.pause(0.1)


bfs_visual(grid, start_pos, target_pos)
