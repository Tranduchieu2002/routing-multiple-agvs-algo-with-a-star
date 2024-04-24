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

def trace_path(cell_details, dest):
    path = []
    row, col = dest

    while not (cell_details[row][col].parent_i == row and cell_details[row][col].parent_j == col):
        path.append((row, col))
        row, col = cell_details[row][col].parent_i, cell_details[row][col].parent_j

    path.append((row, col))
    path.reverse()

    return path

def dijkstra_search(grid: List[List[Cell]], src, dest, directions: List[Tuple[int, int]] = [(0, 1), (0, -1), (-1, 0)]):
    ROW, COL = len(grid), len(grid[0])

    if not is_valid(src[0], src[1], ROW, COL) or not is_valid(dest[0], dest[1], ROW, COL):
        print("Source or destination is invalid")
        return None

    if not is_unblocked(grid, src[0], src[1]) or not is_unblocked(grid, dest[0], dest[1]):
        print("Source or the destination is blocked")
        return None

    closed_list = [[False] * COL for _ in range(ROW)]
    cell_details = [[Cell() for _ in range(COL)] for _ in range(ROW)]

    i, j = src
    for row in range(ROW):
        for col in range(COL):
            cell_details[row][col].g = float('inf')

    cell_details[i][j].g = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    while open_list:
        p = heapq.heappop(open_list)
        g, i, j = p

        if closed_list[i][j]:
            continue

        closed_list[i][j] = True

        if is_destination(i, j, dest):
            print("The destination cell is found")
            path = trace_path(cell_details, dest)
            return path

        for dir in directions:
            new_i, new_j = i + dir[0], j + dir[1]
            if is_valid(new_i, new_j, ROW, COL) and is_unblocked(grid, new_i, new_j):
                g_new = g + 1  # Assuming each move cost is 1
                if g_new < cell_details[new_i][new_j].g:
                    cell_details[new_i][new_j].g = g_new
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    heapq.heappush(open_list, (g_new, new_i, new_j))

    print("Failed to find the destination cell")
    return None

# Test the Dijkstra's search algorithm
# grid = generateBoard(100)

# import time
# start_time = time.time()
# path = dijkstra_search(grid, (len(grid) - 1, 0), (0, 0))
# if path:
#     print("Path found:", path)
# print("--- %s seconds ---" % (time.time() - start_time))
