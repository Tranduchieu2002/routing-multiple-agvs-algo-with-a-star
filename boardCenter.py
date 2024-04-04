#0: Không có đường đi
# 1: Có đường đi
# 2: Có vật cản
# 3: Có AGV

# Path: board-center.py
from typing import List
from random import randint
from Cell import Cell


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
def generate_from_grid(grid):
    board = []
    for row in grid:
        temp_row = []
        for val in row:
            cell = Cell(val)
            temp_row.append(cell)
        board.append(temp_row)
    return board
      
board: List[List[Cell]] = generate_from_grid(grid= grid)

def generateBoard(size): 
  
  board: List[List[Cell]] = [[0 for _ in range(size)] for _ in range(size)]
  for i in range(size):
    for j in range(size):
      randomStatus = 1
      cell = Cell()
      cell.status = randomStatus
      board[i][j] = cell
  return board