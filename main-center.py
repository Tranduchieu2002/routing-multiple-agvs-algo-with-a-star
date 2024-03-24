import boardCenter  # Importing the boardCenter module
from agv import AGV  # Importing the AGV class
class SupervisorCenter:
  def __init__(self):
    self.grid = boardCenter.board  # Accessing the board from boardCenter
    self.AGVs: list[AGV] = []
    self.screen_width, self.screen_height = 1140, 860
    self.ROW = len(self.grid)
    self.COL = len(self.grid[0])
    # self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
      
  def draw_control(self):
    pass
      
  def start(self):
    print("Starting the Supervisor Center")
    
    self.AGVs.append(AGV(self.grid, [8,0],[0,0]))
    # self.AGVs.append(AGV(8, 8))
    print(self.grid)
    
# Creating an instance of SupervisorCenter
supervisor = SupervisorCenter()
supervisor.start()
# supervisor.draw_board()
