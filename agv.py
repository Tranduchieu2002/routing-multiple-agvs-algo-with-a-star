from AStar import a_star_search 


class AGV:
  def __init__(self, board, start, destination):
    self.start: list[int] = start
    self.id = 0
    self.stop = 0
    self.position: list[int] = start
    self.destination: list[int] = destination
    self.final_destination: list[int] = destination
    self.path = []
    print("path:: ", self.path)
    if (self.path is None):
        Exception("No path found")
    self.position = start

  def find_shortest_path(self, board, start, destination):
    # Implement A* algorithm here to find the shortest path
    # Return the path as a list of points
    return a_star_search(board, start, destination)
  def is_done(self):
    return self.position == self.final_destination
  def update(self):
    # Move the AGV along its path
    if self.path:
      self.position = self.path.pop(0)
      self.draw({})

  def draw(self, screen):
      # Draw the AGV on the screen
    pass