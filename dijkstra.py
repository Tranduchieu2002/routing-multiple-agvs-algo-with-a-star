import heapq
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
    return (row, col) == dest

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

def dijkstra_search(grid: List[List[Cell]], src, dest, directions: List[Tuple[int, int]] = [(0, 1), (0, -1), (-1, 0)]):
    ROW = len(grid)
    COL = len(grid[0])
    # Check if the source and destination are valid
    if not is_valid(src[0], src[1], ROW= ROW, COL= COL) or not is_valid(dest[0], dest[1], ROW= ROW, COL= COL):
        print("Source or destination is invalid")
        return

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return

    # Check if we are already at the destination
    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    # Initialize the start cell details
    i = src[0]
    j = src[1]
    cell_details[i][j].g = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Main loop of Dijkstra's search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest g value from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True
        # For each direction, check the successors
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the successor is valid, unblocked, and not visited
            if is_valid(new_i, new_j, ROW, COL) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    print("The destination cell is found")
                    # Trace and print the path from source to destination
                    path = trace_path(cell_details, dest)
                    return path
                else:
                    # Calculate the new g value
                    g_new = cell_details[i][j].g + 1.0

                    # If the cell is not in the open list or the new g value is smaller
                    if cell_details[new_i][new_j].g == float('inf') or cell_details[new_i][new_j].g > g_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (g_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    print("Failed to find the destination cell")
    return None
# Test the Dijkstra's search algorithm

# # Define the grid
# grid = generateBoard(90)

# import time
# start_time = time.time()
# dijkstra_search(grid, (63, 0), (0, 0))
# print("--- %s seconds ---" % (time.time() - start_time))
