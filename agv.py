from typing import List, Tuple
from AStar import a_star_search 


class AGV:
  def __init__(self, board, start, destination):
    self.start: list[int] = start
    self.id = 0
    self.stop = 0
    self.position: list[int] = start
    self.destination: list[int] = destination
    self.color = (255,100,150)
    self.final_destination: list[int] = destination
    self.path: list = []
    self.status: int= 0 # 
    self.energy: int = 0
    self.isStart = True
    self.isFinished = False
    self.isVisited = set()
    print("path:: ", self.path)
    if (self.path is None):
        Exception("No path found")
    self.position = start

  def find_shortest_path(self, board, start, destination, directions: List[Tuple[int, int]] = [(0, 1), (0, -1), (-1, 0)]):
    # Implement A* algorithm here to find the shortest path
    # Return the path as a list of points
    return a_star_search(board, start, destination, directions)
  def is_done(self):

    is_done = self.position == self.final_destination
    if is_done:
      self.status == 0
    return is_done
  def update(self):
    # Move the AGV along its path
    if self.path:
      self.position = self.path.pop(0)
      self.draw({})

  def draw(self, screen):
      # Draw the AGV on the screen
    pass