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

def dls_step(grid_matrix, start_node, goal_node, limit, fig_ax, parent_map):
    """One depth-limited DFS run using the given figure/axis."""
    stack = [(start_node, 0)]
    visited_nodes = set()
    
    fig, ax = fig_ax

    while stack:
        current, depth = stack.pop()
        visited_nodes.add(current)

        if current != start_node and current != goal_node:
            grid_matrix[current[0]][current[1]] = 4  # explored

        if current == goal_node:
            path = []
            node = goal_node
            while node != start_node:
                path.append(node)
                node = parent_map[node]
            path.append(start_node)
            path.reverse()
            return path

        if depth < limit:
            for neighbor in get_valid_neighbors(current, grid_matrix):
                if neighbor not in visited_nodes and (neighbor, depth+1) not in stack:
                    parent_map[neighbor] = current
                    stack.append((neighbor, depth+1))

        ax.clear()
        ax.imshow(grid_matrix, cmap=cmap)
        plt.pause(0.05)
    return None

def ids_visual(grid_matrix, start_node, goal_node, max_depth=20):
    fig, ax = plt.subplots()
    plt.ion()
    parent_map = {}
    
    for depth in range(max_depth):
        # Reset explored cells for each iteration but keep figure
        temp_grid = [row.copy() for row in grid_matrix]
        path = dls_step(temp_grid, start_node, goal_node, depth, (fig, ax), parent_map)
        if path:
            print(f"Path found at depth {depth}")
            # Draw final path
            for step in path:
                if step != start_node and step != goal_node:
                    temp_grid[step[0]][step[1]] = 5
                ax.clear()
                ax.imshow(temp_grid, cmap=cmap)
                plt.pause(0.1)
            plt.ioff()
            plt.show()
            return path
    print("No path found within max depth")
    plt.ioff()
    plt.show()
    return None

# Run IDS
ids_visual(grid, start_pos, target_pos)
