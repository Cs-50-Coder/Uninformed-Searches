import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

EMPTY = 0
WALL = 1
START = 2
TARGET = 3

# Colors: 0-empty, 1-wall, 2-start, 3-target, 4-explored, 5-final path
cmap = mcolors.ListedColormap(['white', 'black', 'cyan', 'magenta', 'yellow'])

grid = [
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,2,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,1,0,1,0,0,0,0],
    [0,0,0,0,0,1,0,1,0,0,0,0],
    [0,0,0,0,0,1,1,1,3,0,0,0],
    [0,0,0,0,0,1,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0]
]

start_pos = (5, 2)
target_pos = (9, 8)

directions = [
    (-1, 0),  # Up
    (0, 1),   # Right
    (0, -1),  # Left
    (-1, -1), # Up-Left
    (1, 0),   # Down
    (1, 1)    # Down-Right
]

def get_valid_neighbors(position, grid_matrix):
    row, col = position
    neighbors = []
    for d_row, d_col in directions:
        new_row, new_col = row + d_row, col + d_col
        if 0 <= new_row < len(grid_matrix) and 0 <= new_col < len(grid_matrix[0]) and grid_matrix[new_row][new_col] != WALL:
            neighbors.append((new_row, new_col))
    return neighbors

def dls_visual(grid_matrix, start_node, goal_node, limit):
    """Depth-Limited Search with GUI visualization (no terminal messages)."""
    fig, ax = plt.subplots()
    plt.ion()
    stack = [(start_node, 0)]
    visited_nodes = set()
    parent_map = {}

    while stack:
        current, depth = stack.pop()
        visited_nodes.add(current)

        if current != start_node and current != goal_node:
            grid_matrix[current[0]][current[1]] = 4  # explored

        if current == goal_node:
            # reset explored for clean path display
            for r in range(len(grid_matrix)):
                for c in range(len(grid_matrix[0])):
                    if grid_matrix[r][c] in (4, 5):
                        grid_matrix[r][c] = EMPTY
            # Draw final path
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
                ax.clear()
                ax.imshow(grid_matrix, cmap=cmap)
                plt.pause(0.1)
            plt.ioff()
            plt.show()
            return

        if depth < limit:
            for neighbor in get_valid_neighbors(current, grid_matrix):
                if neighbor not in visited_nodes and (neighbor, depth+1) not in stack:
                    parent_map[neighbor] = current
                    stack.append((neighbor, depth+1))

        ax.clear()
        ax.imshow(grid_matrix, cmap=cmap)
        plt.pause(0.05)

    plt.ioff()
    plt.show()
    return

depth_limit = int(input("Enter depth limit for DLS: "))
dls_visual(grid, start_pos, target_pos, depth_limit)
