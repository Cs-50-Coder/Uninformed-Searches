import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import deque

EMPTY = 0
WALL = 1
START = 2
TARGET = 3

cmap = mcolors.ListedColormap(
    ['white', 'black', 'cyan', 'magenta', 'yellow', 'green']
)

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
    directions = [
        (-1, 0),
        (0, 1),
        (1, 0),
        (1, 1),
        (0, -1),
        (-1, -1)
    ]

    valid_neighbors = []

    for d_row, d_col in directions:
        new_row = row + d_row
        new_col = col + d_col

        if (
            0 <= new_row < len(grid_matrix)
            and 0 <= new_col < len(grid_matrix[0])
            and grid_matrix[new_row][new_col] != WALL
        ):
            valid_neighbors.append((new_row, new_col))

    return valid_neighbors


def bfs_visual(grid_matrix, start_node, goal_node):
    frontier_queue = deque([start_node])
    visited_nodes = set()
    parent_map = {}

    figure, axis = plt.subplots()
    plt.ion()

    while frontier_queue:
        current_node = frontier_queue.popleft()
        visited_nodes.add(current_node)

        if current_node != start_node and current_node != goal_node:
            grid_matrix[current_node[0]][current_node[1]] = 4

        if current_node == goal_node:
            for r in range(len(grid_matrix)):
                for c in range(len(grid_matrix[0])):
                    if grid_matrix[r][c] == 4 or grid_matrix[r][c] == 5:
                        grid_matrix[r][c] = EMPTY

            path = []
            node = goal_node

            while node != start_node:
                path.append(node)
                node = parent_map[node]

            path.append(start_node)
            path.reverse()

            for step in path:
                if step != start_node and step != goal_node:
                    grid_matrix[step[0]][step[1]] = 5

                axis.clear()
                axis.imshow(grid_matrix, cmap=cmap)
                plt.pause(0.1)

            plt.ioff()
            plt.show()
            return path

        for neighbor in get_valid_neighbors(current_node, grid_matrix):
            if neighbor not in visited_nodes and neighbor not in frontier_queue:
                parent_map[neighbor] = current_node
                frontier_queue.append(neighbor)

                if neighbor != goal_node:
                    grid_matrix[neighbor[0]][neighbor[1]] = 5

        axis.clear()
        axis.imshow(grid_matrix, cmap=cmap)
        plt.pause(0.2)


bfs_visual(grid, start_pos, target_pos)
