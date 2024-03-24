from AStar import a_star_search 


class AGV:
  def __init__(self, board, start, destination):
    self.start = start
    self.destination = destination
    self.final_destination = destination
    self.path = self.find_shortest_path(board, start, destination)
    print("path:: ", self.path)
    if (self.path is None):
        Exception("No path found")
    self.position = start

  def find_shortest_path(self, board, start, destination):
    # Implement A* algorithm here to find the shortest path
    # Return the path as a list of points
    return a_star_search(board, start, destination)
      
  def update(self):
    # Move the AGV along its path
    if self.path:
      self.position = self.path.pop(0)
      self.draw({})

  def draw(self, screen):
      # Draw the AGV on the screen
    pass