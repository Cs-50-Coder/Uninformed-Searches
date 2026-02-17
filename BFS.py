import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import deque
import time

# Grid legend
EMPTY = 0
WALL = 1
START = 2
TARGET = 3

# Colors
cmap = mcolors.ListedColormap(['white', 'black', 'cyan', 'magenta', 'yellow', 'green'])
# 0: empty, 1: wall, 2: start, 3: target, 4: explored, 5: frontier
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


start = (0,0)
target = (9,9)

def get_neighbors(node, grid):
    r, c = node
    moves = [
        (-1, 0),  # Up
        (0, 1),   # Right
        (1, 0),   # Bottom
        (1, 1),   # Bottom-Right
        (0, -1),  # Left
        (-1, -1)  # Top-Left
    ]
    neighbors = []
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid) and 0 <= nc < len(grid[0]) and grid[nr][nc] != WALL:
            neighbors.append((nr, nc))
    return neighbors
def bfs_visual(grid, start, target):
    frontier = deque([start])
    explored = set()
    parent = {}

    fig, ax = plt.subplots()
    plt.ion()

    while frontier:
        current = frontier.popleft()
        explored.add(current)

        # Mark explored
        if current != start and current != target:
            grid[current[0]][current[1]] = 4  # explored

        # Check for target
        if current == target:
            # Reset grid (remove explored & frontier colors)
            for r in range(len(grid)):
                for c in range(len(grid[0])):
                    if grid[r][c] == 4 or grid[r][c] == 5:
                        grid[r][c] = EMPTY


            path = []
            node = target
            while node != start:
                path.append(node)
                node = parent[node]
            path.append(start)
            path.reverse()
            for node in path:
                if node != start and node != target:
                    grid[node[0]][node[1]] = 5  # final path
                ax.clear()
                ax.imshow(grid, cmap=cmap)
                plt.pause(0.1)
            plt.ioff()
            plt.show()
            return path

        for neighbor in get_neighbors(current, grid):
            if neighbor not in explored and neighbor not in frontier:
                parent[neighbor] = current
                frontier.append(neighbor)
                # Mark frontier for visualization
                if neighbor != target:
                    grid[neighbor[0]][neighbor[1]] = 5
        # Update plot
        ax.clear()
        ax.imshow(grid, cmap=cmap)
        plt.pause(0.2)

bfs_visual(grid, start, target)
