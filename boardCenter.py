#0: Không có đường đi
# 1: Có đường đi
# 2: Có vật cản
# 3: Có AGV

# Path: board-center.py
from typing import List
from random import randint
from cell import Cell


board: List[List[int]] = [
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

def generateBoard(size): 
  
  board: List[List[Cell]] = [[0 for _ in range(size)] for _ in range(size)]
  for i in range(size):
    for j in range(size):
      randomStatus = randint(0, 3)
      board[i][j] = randomStatus
  return board