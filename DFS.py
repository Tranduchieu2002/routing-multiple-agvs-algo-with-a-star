from typing import List, Tuple
from boardCenter import board
from boardCenter import generateBoard
from Cell import Cell

def is_valid(row, col, ROW, COL):
    return 0 <= row < ROW and 0 <= col < COL

# Check if a cell is unblocked
def is_unblocked(grid: List[List[Cell]], row: int, col: int):
    return grid[row][col].status == 1

# Check if a cell is the destination
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Trace the path from source to destination
def trace_path(cell_details, dest):
    path = []
    row = dest[0]
    col = dest[1]

    # Trace the path from destination to source using parent cells
    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    # Add the source cell to the path
    path.append((row, col))
    # Reverse the path to get the path from source to destination
    path.reverse()

    return path

def dfs_search(grid: List[List[Cell]], src, dest, visited, path):
    ROW = len(grid)
    COL = len(grid[0])
    i, j = src

    # If current cell is already visited, return
    if visited[i][j]:
        return False

    # Mark current cell as visited
    visited[i][j] = True

    # If destination is found, trace the path and return
    if is_destination(i, j, dest):
        path.append((i, j))
        return True

    # Explore all adjacent cells
    for direction in [(0, 1), (0, -1), (-1, 0)]:
        new_i, new_j = i + direction[0], j + direction[1]
        if is_valid(new_i, new_j, ROW, COL) and is_unblocked(grid, new_i, new_j):
            if dfs_search(grid, (new_i, new_j), dest, visited, path):
                path.append((i, j))
                return True

    return False

def find_path_dfs(grid, src, dest):
    ROW = len(grid)
    COL = len(grid[0])

    if not is_valid(src[0], src[1], ROW, COL) or not is_valid(dest[0], dest[1], ROW, COL):
        print("Source or destination is invalid")
        return

    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return

    visited = [[False for _ in range(COL)] for _ in range(ROW)]
    path = []

    if dfs_search(grid, src, dest, visited, path):
        return path[::-1]
    else:
        print("Failed to find the destination cell")
        return None

# Test the DFS search algorithm
grid = generateBoard(100)

import time
start_time = time.time()
path = find_path_dfs(grid, (len(grid) - 1, 0), (0, 0))
if path:
    print("Path found:", path)
print("--- %s seconds ---" % (time.time() - start_time))
