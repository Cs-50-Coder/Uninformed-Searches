import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from collections import deque

EMPTY = 0
WALL = 1
START = 2
TARGET = 3

# Colors: 0-empty, 1-wall, 2-start, 3-target, 4-final path
cmap = mcolors.ListedColormap(['white', 'black', 'cyan', 'magenta', 'yellow'])

grid = [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,2,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,1,0,0,0,0],
    [0,0,0,0,0,1,0,1,0,0,0,0],
    [0,0,0,0,0,1,1,1,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,3,0,0,0,0,0,0]
]

start_pos = (5, 2)
target_pos = (11, 5)

directions = [(-1,0),(0,1),(1,0),(1,1),(0,-1),(-1,-1)]

def get_valid_neighbors(pos, grid_matrix):
    r, c = pos
    neighbors = []
    for dr, dc in directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < len(grid_matrix) and 0 <= nc < len(grid_matrix[0]) and grid_matrix[nr][nc] != WALL:
            neighbors.append((nr, nc))
    return neighbors

def reconstruct_path(meet_node, parent_start, parent_goal, start_node, goal_node):
    path = []
    node = meet_node
    while node != start_node:
        path.append(node)
        node = parent_start[node]
    path.append(start_node)
    path.reverse()
    node = parent_goal.get(meet_node)
    while node is not None and node != goal_node:
        path.append(node)
        node = parent_goal.get(node)
    if goal_node not in path:
        path.append(goal_node)
    return path

def bidirectional_search_visual(grid_matrix, start_node, goal_node):
    temp_grid = [row.copy() for row in grid_matrix]
    queue_start = deque([start_node])
    queue_goal = deque([goal_node])
    visited_start = {start_node}
    visited_goal = {goal_node}
    parent_start = {}
    parent_goal = {}
    meet_node = None

    fig, ax = plt.subplots()
    plt.ion()

    while queue_start or queue_goal:
        if queue_start and meet_node is None:
            cur = queue_start.popleft()
            if cur != start_node and cur != goal_node:
                temp_grid[cur[0]][cur[1]] = 4
            for n in get_valid_neighbors(cur, temp_grid):
                if n not in visited_start:
                    visited_start.add(n)
                    parent_start[n] = cur
                    queue_start.append(n)
                if n in visited_goal:
                    meet_node = n
                    break

        if queue_goal and meet_node is None:
            cur = queue_goal.popleft()
            if cur != start_node and cur != goal_node:
                temp_grid[cur[0]][cur[1]] = 4
            for n in get_valid_neighbors(cur, temp_grid):
                if n not in visited_goal:
                    visited_goal.add(n)
                    parent_goal[n] = cur
                    queue_goal.append(n)
                if n in visited_start:
                    meet_node = n
                    break

        ax.clear()
        ax.imshow(temp_grid, cmap=cmap, vmin=0, vmax=4)
        plt.pause(0.05)

        if meet_node:
            break

    if meet_node:
        path = reconstruct_path(meet_node, parent_start, parent_goal, start_node, goal_node)
        clean_grid = [row.copy() for row in grid_matrix]
        for step in path:
            if step != start_node and step != goal_node:
                clean_grid[step[0]][step[1]] = 4
            ax.clear()
            ax.imshow(clean_grid, cmap=cmap, vmin=0, vmax=4)
            plt.pause(0.05)

    plt.ioff()
    plt.show()

bidirectional_search_visual(grid, start_pos, target_pos)
