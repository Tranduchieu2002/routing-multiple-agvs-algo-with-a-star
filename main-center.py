import math
import pygame
from collections import defaultdict
from typing import List
from boardCenter import board  # Importing the boardCenter module
from agv import AGV
from Cell import Cell  # Importing the AGV class

STATUS_LABEL = {
    0: 'Đang Bắt Đầu',
    1: 'Đang đến dipot',
    2: 'Đang đến cửa hàng',
    3: 'Đang về'
}

STATUS_COLORS = {
    0: '#22c55e',
    1: '#facc15',
    2: '#e11d48',
    3: '#2563eb'
}

STATUS =  {
    "INSTATION": 0,
    "GOING_DEPOT": 1,
    "GOING_STORE": 2,
    "GOBACK": 3         
}

INF = 1000000000
BASE = 3
PI = math.pi
data = [{
    "station": 0,
    "color": "#22c55e"
}, {
    "station": 1,
    "color": "#22c55e"
}, {
    "station": 0,
    "color": "#22c55e"
},
 {
    "station": 1,
    "color": "#22c55e"
}]
class SupervisorCenter:
    def __init__(self):
        self.stations = []
        self.stores = []
        self.depots = []
        self.grid: list[list[Cell]] = board  # Accessing the board from boardCenter
        self.AGVs: list[AGV] = []
        self.screen_width, self.screen_height = 1140, 860
        self.intersection = []
        self.ROW = len(self.grid)
        self.COL = len(self.grid[0])
        self.cell_size = 40  # Size of each cell
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()

    def initIntersection(self):
        for i in range(self.ROW):
            for j in range(self.COL):
                pass
                # if self.grid[i][j].status == 2:
                #   self.intersection.append([i,j])

    def draw_board(self):
        for i in range(self.ROW):
            for j in range(self.COL):
                print(self.grid[i][j].status, end=" ")
            

    def initObjects(self):
        self.stations = [[self.ROW - 1, 0],[self.ROW - 1, self.COL - 1]]
        for station in self.stations:
            self.grid[station[0]][station[1]].status = 1
        self.stores = [[0, 0], [0, (self.COL - 1)]]
        for store in self.stores:
            self.grid[store[0]][store[1]].status = 1
        self.depots = [[(self.ROW) // 2, 0], [(self.ROW - 1) // 2, self.COL - 1]]
        for depot in self.depots:
            self.grid[depot[0]][depot[1]].status = 1

    def draw_control(self):
        pass

    def whenMeetInIntersection(self):
        pass
    def calcCircle(self, agv: AGV):
        return PI * BASE 
    def checkConflict(self, agv: AGV):
        isConflict = False
        if agv.path:
            for i in range(len(self.AGVs)):
                if self.AGVs[i].id == agv.id:
                    continue
                if self.AGVs[i].path:
                    if agv.path[:min(len(agv.path), BASE)] in self.AGVs[i].path[0]:
                        isConflict = True
                        break
        return isConflict

    def findShortestInMultiRoutes(self, agv: AGV, dest: List[List[int]]):
        minCosts = INF
        minRoute = None
        for d in dest:
          route = agv.find_shortest_path(self.grid, agv.position, d)
          if route == None:
              continue
          print(route)
          if route != None and len(route) < minCosts:
              minCosts = len(route)
              minRoute = route
          minCosts = min(minCosts, len(route))
        agv.path = minRoute

    def move(self, agv: AGV):
        path = agv.path
        (x, y) = agv.position
        # TODO: check conflicts in total AGV
        # for _ in range(BASE):
            # if self.grid[]
        if agv.position in self.stations:
            agv.status = STATUS["INSTATION"]
        if agv.status == 0 and agv.isStart:
              agv.status = STATUS['GOING_DEPOT']
        if not path:
          isDepot = [x, y] in self.depots
          isStore = [x, y] in self.stores
          print('isDepot: ', isDepot, isStore, self.depots, agv.position)

          if agv.status == 0 and not agv.isStart:
              agv.status = STATUS['GOING_DEPOT']
          if isDepot:
              self.findShortestInMultiRoutes(agv, self.stores)
              if agv.path == None:
                  return
              agv.status = STATUS["GOING_STORE"]
          if isStore:
              self.findShortestInMultiRoutes(agv, self.stations)
              if agv.path == None:
                  return
              agv.status = STATUS["GOBACK"]
        if(not agv.isStart and self.checkConflict()):
            agv.stop = 1
        self.grid[x][y].agv = None  # remove the AGV from the current cell
        if path:
            if not agv.isStart and self.grid[path[0][0]] and self.grid[path[0][1]]:
                agv.stop = 1
                
            nextPoint = path.pop(0)
            isDepot = nextPoint in self.depots
            isStore = nextPoint in self.stores
            if isDepot:
                self.findShortestInMultiRoutes(agv, self.stores)
            if isStore:
                self.findShortestInMultiRoutes(agv, self.stations)
            self.grid[nextPoint[0]][nextPoint[1]].AGV = agv
            agv.position = nextPoint
    def draw_grid(self):
        # Draw grid lines
        for i in range(self.ROW + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * self.cell_size), (self.screen_width, i * self.cell_size))
        for j in range(self.COL + 1):
            pygame.draw.line(self.screen, (0, 0, 0), (j * self.cell_size, 0), (j * self.cell_size, self.screen_height))
        for i in range(self.ROW):
          for j in range(self.COL):
            if self.grid[i][j].status == 0:
              pygame.draw.rect(self.screen, (0, 0, 0), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
            if self.grid[i][j].isStore:
              pygame.draw.rect(self.screen, (0, 0, 0), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
            if self.grid[i][j].isDepot:
              pygame.draw.rect(self.screen, (0, 0, 0), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
            if self.grid[i][j].isChargingStation:
              pygame.draw.rect(self.screen, (0, 0, 0), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))

            # if self.grid[i][j].agv:
            #     pygame.draw.rect(self.screen, (0, 0, 0), (j * self.cell_size, i * self.cell_size, self.cell_size, self.cell_size))
            # if self.grid[i][j].status == 2:
            #   pygame.draw.circle(self.screen, (0, 0, 0), (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size // 2), 10)
            # if self.grid[i][j].status == 3:
            #   pygame.draw.line(self.screen, (0, 0, 255), (j * self.cell_size + self.cell_size // 2, i * self.cell_size), (j * self.cell_size + self.cell_size // 2, i * self.cell_size + self.cell_size), 3)

    def draw_AGVs(self):
        for agv in self.AGVs:
            x, y = agv.position
            pygame.draw.rect(self.screen, STATUS_COLORS[agv.status], (y * self.cell_size, x * self.cell_size, self.cell_size, self.cell_size))
    def initAGVs(self):
        print("Init AGVs", data)
        stops = defaultdict(int)
        for i in range(len(data)):
            station = data[i]["station"]
            agv = AGV(self.grid, self.stations[station], self.stores[0])
            # star together have to wait 3s
            if stops[station]:
                agv.stop = 3
            stops[station] += 3
            agv.stop = stops.get(station, 0)
            self.AGVs.append(agv)
            
    def start(self):
        print("Starting the Supervisor Center")
        self.initObjects()
        pygame.init()
        self.initAGVs()
        self.screen.fill((255, 255, 255))  # Fill screen with white
        self.draw_grid()  # Draw grid lines
        pygame.display.flip()  # Update the display
        self.clock.tick(60)  # Cap the frame rate to 60 FPS
        for i in range(len(self.AGVs)):
          agv = self.AGVs[i]
          agv.id = i
          self.findShortestInMultiRoutes(agv, self.depots)
          print("Founded Path", agv.path)
        running = True
        counter = 0
        listDone = [False for _ in range(len(self.AGVs))]
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            for agv in self.AGVs:
                if (agv.stop > 0):
                    agv.stop -= 1
                    continue
                self.move(agv)
                if agv.position in self.stores:
                    listDone[agv.id] = True
                if all(listDone):
                    running = False
            label = ''
            for agv in self.AGVs:
                print(str(agv.id) + STATUS_LABEL[agv.status])
            print('Bước ' + str((counter + 1)))
            self.screen.fill((255, 255, 255))  # Clear the screen
            self.draw_grid()  # Redraw grid lines
            self.draw_AGVs()  # Draw AGVs on the grid
            pygame.display.flip()  # Update the display
            pygame.time.delay(500) 
            self.clock.tick(60)  # Cap the frame rate to 60 FPS
            counter += 1

# Creating an instance of SupervisorCenter
supervisor = SupervisorCenter()
supervisor.start()
