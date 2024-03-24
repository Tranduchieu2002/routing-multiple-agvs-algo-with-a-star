class Cell:
  def __init__(self):
    self.parent_i = 0  # Parent cell's row index
    self.parent_j = 0  # Parent cell's column index
    self.f = float('inf')  # Total cost of the cell (g + h)
    self.g = float('inf')  # Cost from start to this cell
    self.h = 0  # Heuristic cost from this cell to destination
    self.status = 0  # 0: Unvisited, 1: Open, 2: Closed, 3: Blocked
    self.AGV = None
