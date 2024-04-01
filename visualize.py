import pygame
import heapq
from AStar import a_star_search
from board import board
import random
import math
PI = math.pi
# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# write a function generate color for each AGV
def generate_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return (r, g, b)

class AGV:
    def __init__(self, start, destination):
        self.start = start
        self.destination = destination
        self.path = self.find_shortest_path(start, destination)
        if (self.path is None):
            Exception("No path found")
        self.position = start

    def find_shortest_path(self, board, start, destination):
        # Implement A* algorithm here to find the shortest path
        # Return the path as a list of points
        return a_star_search(self,board, start, destination)
        
    def update(self):
        # Move the AGV along its path
        if self.path:
            self.position = self.path.pop(0)
            self.draw({})

    def draw(self, screen):
        # Draw the AGV on the screen
        pygame.draw.circle(screen, (255, 0, 0), self.position, 10)

class SupervisorCenter():
    
    # using trigger when notify for AGVs
    # create function draw board
    def __init__(self):
        self.grid = board
        self.agvs = []
        self.screen_width, self.screen_height = 1140, 860
        self.ROW = len(board)
        self.COL = len(board[0])
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
    def draw_control(self):
        pass
    def draw_board(self, screen):
        n1,n2 = (self.screen_height - 30) // self.ROW,self.screen_width // self.COL
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if board[i][j] == 1:
                  pygame.draw.circle(screen, 'white', (j * n2 + (0.5 * n2), i * n1 + (0.5 * n1)), 4)
                if board[i][j] == 2:
                    pygame.draw.circle(screen, 'white', (j * n2 + (0.5 * n2), i * n1 + (0.5 * n1)), 10)
                if board[i][j] == 3:
                    pygame.draw.line(screen, BLUE, (j * n2 + (0.5 * n2), i * n1),
                                    (j * n2 + (0.5 * n2), i * n1 + n1), 3)
                
    def trigger(self):
      pass
    def start(self):
      pygame.init()

      
      clock = pygame.time.Clock()
      FPS = 60
      # Create AGV instances
    #   agvs = [AGV((100, 100), (600, 500)),
    #           AGV((200, 200), (400, 300)),
    #           AGV((300, 300), (200, 100))]

      # Main Pygame loop
      running = True
      self.screen.fill(BLACK)
      while running:
          for event in pygame.event.get():
              if event.type == pygame.QUIT:
                  running = False
          self.draw_board(self.screen)
          pygame.display.update()
          # Update AGVs
        #   for agv in agvs:
        #       agv.update()

          # Draw everything
        #   for agv in agvs:
        #       agv.draw(screen)
        #   pygame.display.flip()

          # Cap the frame rate
      clock.tick(FPS) # slow down to 25 FPS

      pygame.quit()

if __name__ == "__main__":
    supervisor = SupervisorCenter()
    supervisor.start()