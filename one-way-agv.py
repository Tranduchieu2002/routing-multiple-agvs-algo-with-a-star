import math
import heapq
import pprint
import pygame
import sys

from Cell import Cell
# destination = Điểm đến
# Define the size of the grid
ROW = 9
COL = 10

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Define the Cell class

# Check if a cell is valid (within the grid)
def is_valid(row, col):
    return 0 <= row < ROW and 0 <= col < COL

# Check if a cell is unblocked
def is_unblocked(grid, row, col):
    return grid[row][col] == 1

# Check if a cell is the destination
def is_destination(row, col, dest):
    return row == dest[0] and col == dest[1]

# Calculate the heuristic value of a cell (Euclidean distance to destination)
def calculate_h_value(row, col, dest):
  row_diff = abs(row - dest[0])
  col_diff = abs(col - dest[1])
  return row_diff + col_diff

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

# Implement the A* search algorithm
def a_star_search(grid, src, dest):
    # Initialize Pygame
    pygame.init()
    clock = pygame.time.Clock()

    # Set up the display
    screen_width = COL * 50
    screen_height = ROW * 50
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("A* Pathfinding Visualization")

    # Check if the source and destination are valid
    if not is_valid(src[0], src[1]) or not is_valid(dest[0], dest[1]):
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
    cell_details[i][j].f = 0
    cell_details[i][j].g = 0
    cell_details[i][j].h = 0
    cell_details[i][j].parent_i = i
    cell_details[i][j].parent_j = j

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, i, j))

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)

        # Mark the cell as visited
        i = p[1]
        j = p[2]
        closed_list[i][j] = True

        # Plot the current cell
        screen.fill(WHITE)
        for row in range(ROW):
            for col in range(COL):
                color = WHITE
                if grid[row][col] == 0:
                    color = BLACK
                pygame.draw.rect(screen, color, pygame.Rect(col * 50, row * 50, 50, 50))
                pygame.draw.rect(screen, BLUE, pygame.Rect(dest[1] * 50, dest[0] * 50, 50, 50))
                pygame.draw.rect(screen, RED, pygame.Rect(src[1] * 50, src[0] * 50, 50, 50))
        pygame.draw.rect(screen, ORANGE, pygame.Rect(j * 50, i * 50, 50, 50))
        pygame.display.flip()
        clock.tick(2)  # Adjust the speed here (higher value for slower animation)

        # For each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        for dir in directions:
            new_i = i + dir[0]
            new_j = j + dir[1]

            # If the successor is valid, unblocked, and not visited
            if is_valid(new_i, new_j) and is_unblocked(grid, new_i, new_j) and not closed_list[new_i][new_j]:
                # If the successor is the destination
                if is_destination(new_i, new_j, dest):
                    # Set the parent of the destination cell
                    cell_details[new_i][new_j].parent_i = i
                    cell_details[new_i][new_j].parent_j = j
                    print("The destination cell is found")
                    # Trace and print the path from source to destination
                    path = trace_path(cell_details, dest)
                    # Vẽ đường dẫn
                    for (row, col) in path:
                        pygame.draw.rect(screen, GREEN, pygame.Rect(col * 50, row * 50, 50, 50))
                        pygame.display.flip()
                        pygame.time.delay(500)  # Delay for visualization
                    # pygame.quit()
                    # sys.exit()
                    return path
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[i][j].g + 1.0
                    h_new = calculate_h_value(new_i, new_j, dest)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_i][new_j].f == float('inf') or cell_details[new_i][new_j].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_i, new_j))
                        # Update the cell details
                        cell_details[new_i][new_j].f = f_new
                        cell_details[new_i][new_j].g = g_new
                        cell_details[new_i][new_j].h = h_new
                        cell_details[new_i][new_j].parent_i = i
                        cell_details[new_i][new_j].parent_j = j

    # If the destination is not found after visiting all cells
    print("Failed to find the destination cell")
    # pygame.quit()

def main():
    # Define the grid (1 for unblocked, 0 for blocked)
    queue = [[8,0]]
    grid = [
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0, 1, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 1, 1, 0],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]
    ]

    # Define the source and destination
    dest = [0, COL - 1]
    paths = []
    while queue: 
        src = queue.pop(0)
        paths.append(a_star_search(grid, src, dest))
        print(f'Số đường đi từ {src} -> đến {dest} : {len(paths[0])}')
    pprint.pprint(paths)

if __name__ == "__main__":
    main()
