import heapq
from typing import List, Tuple
from boardCenter import generateBoard
from Cell import Cell

def is_valid(row, col, ROW, COL):
    return 0 <= row < ROW and 0 <= col < COL

def is_unblocked(grid: List[List[Cell]], row: int, col: int):
    return grid[row][col].status == 1

def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

def calculate_h_value(row, col, dest):
    row_diff = abs(row - dest[0])
    col_diff = abs(col - dest[1])
    return row_diff + col_diff

def trace_path(cell_details, dest):
    path = []
    row = dest[0]
    col = dest[1]

    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        temp_row = cell_details[row][col].parent_i
        temp_col = cell_details[row][col].parent_j
        row = temp_row
        col = temp_col

    path.append((row, col))
    path.reverse()

    return path

def a_star_search(grid: List[List[Cell]], src, dest, directions: List[Tuple[int, int]] = [(0, 1), (0, -1), (-1, 0)]):
    ROW = len(grid)
    COL = len(grid[0])

    if not is_valid(src[0], src[1], ROW=ROW, COL=COL) or not is_valid(dest[0], dest[1], ROW=ROW, COL=COL):
        print("Source or destination is invalid")
        return

    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return

    if is_destination(src[0], src[1], dest):
        print("We are already at the destination")
        return

    closed_list = [[False for _ in range(COL)] for _ in range(ROW)]
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    i = src[0]
    j = src[1]
    cell_details[i][j].f = float('inf')  # Correct initialization
    cell_details[i][j].g = float('inf')  # Correct initialization
    cell_details[i][j].h = float('inf')  # Correct initialization
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    while len(open_list) > 0:
        p = heapq.heappop(open_list)

        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            if is_valid(new_i, new_j, ROW, COL) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                if is_destination(new_i, new_j, dest):
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    print("The destination cell is found")
                    path = trace_path(cell_details, dest)
                    return path
                else:
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    print("Failed to find the destination cell")
    return None

# # Test the A* search algorithm
# grid = generateBoard(90) 
# import time
# start_time = time.time()
# a_star_search(grid, (63, 0), (0, 0))
# print("--- %s seconds ---" % (time.time() - start_time))
