import math
import sys
import pygame
from collections import defaultdict
from typing import List
from boardCenter import board  # Importing the boardCenter module
from agv import AGV
from Cell import Cell  # Importing the AGV class

store_image = pygame.image.load("house.png")
depot_image = pygame.image.load("depot.png")
charging_station_image = pygame.image.load("station.png")
rock_image = pygame.image.load("rock.png")
agv_image = pygame.image.load("agv-robot.png")
STATUS_LABEL = {
    0: 'Ready to go',
    1: 'Going to Depot',
    2: 'Going to Store',
    3: 'Go back to Station'
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
        self.screen_width, self.screen_height = 840, 860
        self.intersection = []
        self.ROW = len(self.grid)
        self.COL = len(self.grid[0])
        self.cell_size = 50  # Size of each cell
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.insert_rock_button_rect = pygame.Rect(self.screen_width - 180, 50, 160, 50)  # Define button rectangle
        pygame.font.init()
        self.font = pygame.font.Font(None, 24)
        text = self.font.render("Control Panel", True, (0, 0, 0))
        text_rect = text.get_rect(center=(self.screen_width - 100, 20))
        self.screen.blit(text, text_rect)
    def draw_totalTime(self):
        pass
            
    def initObjects(self):
        self.stations = [[self.ROW - 1, 0],[self.ROW - 1, self.COL - 1]]
        for station in self.stations:
            self.grid[station[0]][station[1]].status = 1
            self.grid[station[0]][station[1]].isChargingStation = True
        self.stores = [[0, 0], [0, (self.COL - 1)]]
        for store in self.stores:
            self.grid[store[0]][store[1]].isStore = True
            self.grid[store[0]][store[1]].status = 1
        self.depots = [[(self.ROW) // 2, 0], [(self.ROW - 1) // 2, self.COL - 1]]
        for depot in self.depots:
            self.grid[depot[0]][depot[1]].isDepot = True
            self.grid[depot[0]][depot[1]].status = 1

    def draw_control(self):
        pass
    def draw_AGVs(self):
        # return
        for agv in self.AGVs:
            x, y = agv.position
            # Calculate the coordinates based on cell size and position
            agv_x = y * (500 // self.COL) + (500 // self.COL - self.cell_size) // 2  # Adjusted x-coordinate
            agv_y = x * (500 // self.ROW) + (500 // self.ROW - self.cell_size) // 2  # Adjusted y-coordinate
            draw_agv = pygame.transform.scale(agv_image, (self.cell_size, self.cell_size))
            self.screen.blit(draw_agv, (agv_x, agv_y))

            # pygame.draw.rect(self.screen, STATUS_COLORS[agv.status], (agv_x, agv_y, self.cell_size, self.cell_size))
    def draw_AGV_info(self):
        # Draw AGV information board
        board_width = 200
        board_height = self.screen_height
        pygame.draw.rect(self.screen, (200, 200, 200), (self.screen_width - board_width, 0, board_width, board_height))

        # Display AGV information
        text_y = 20
        for agv in self.AGVs:
            text = f"AGV {agv.id}: {STATUS_LABEL.get(agv.status, 'Unknown')}"
            text_render = self.font.render(text, True, (0, 0, 0))
            text_rect = text_render.get_rect(midleft=(self.screen_width - board_width + 10, text_y))
            self.screen.blit(text_render, text_rect)
            text_y += 30
    
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
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    # Check if mouse click is within the button rectangle
                    if self.insert_rock_button_rect.collidepoint(mouse_pos):
                        # Insert rock at mouse position
                        cell_x = mouse_pos[1] // self.cell_size
                        cell_y = mouse_pos[0] // self.cell_size
                        self.grid[cell_x][cell_y].status = 1  # Set cell status to rock (1)
                        # Redraw the grid with the updated cell status
                        self.draw_grid()
                        # Update the display
                        pygame.display.update()
    def draw_grid(self):
        # Define the size of the grid
        grid_width = 500
        grid_height = 500

        # Calculate the cell size based on the grid dimensions
        cell_width = grid_width // self.COL
        cell_height = grid_height // self.ROW

        # Draw grid lines
        for i in range(self.ROW + 1):
            pygame.draw.line(self.screen, (150, 150, 150), (0, i * cell_height), (grid_width, i * cell_height))
        for j in range(self.COL + 1):
            pygame.draw.line(self.screen, (150, 150, 150), (j * cell_width, 0), (j * cell_width, grid_height))

        # Draw cells
        for i in range(self.ROW):
            for j in range(self.COL):
                cell = self.grid[i][j]
                image = None  # Default no image
                if cell.isStore:
                    image = store_image  # Store
                elif cell.isDepot:
                    image = depot_image  # Depot
                elif cell.isChargingStation:
                    image = charging_station_image  # Charging Station
                elif cell.status == 0:
                    image = rock_image
                    
                # Draw the image
                if image:
                    # Resize image to fit cell size
                    image = pygame.transform.scale(image, (cell_width, cell_height))
                    self.screen.blit(image, (j * cell_width, i * cell_height))    

        # Add text to buttons
        font = pygame.font.Font(None, 24)
        text = font.render("Insert Rock", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.insert_rock_button_rect.center)
        self.screen.blit(text, text_rect)
    

    def findShortestInMultiRoutes(self, agv: AGV, dest: List[List[int]]):
        minCosts = INF
        minRoute = None
        agv.final_destination = self.stores[0]
        finalDestination = agv.final_destination
        directions = [(0, 1), (0, -1), (-1, 0)]
        for d in dest:
          if dest == self.stations:
              directions =  [(0, 1), (0, -1), (1, 0)]
          route = agv.find_shortest_path(self.grid, agv.position, d, directions)
          if route == None:
              continue
          if route != None and len(route) < minCosts:
              minCosts = len(route)
              finalDestination = d
              minRoute = route
          minCosts = min(minCosts, len(route))
        agv.path = minRoute
        agv.final_destination = finalDestination
    def move(self, agv: AGV):
        path = agv.path
        (x, y) = agv.position
        # TODO: check conflicts in total AGV

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
        # check conflict down here
        isConflict = not agv.isStart and  self.checkConflict(agv)
        print('Check conflict :: ', isConflict)
        if(isConflict):
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
            for agv in self.AGVs:
                print('AGV  ' + str(agv.id) + '  ' + STATUS_LABEL[agv.status])
            print('Bước ' + str((counter + 1)))
            self.screen.fill((255, 255, 255))  # Clear the screen
            self.draw_grid()  # Redraw grid lines
            self.draw_AGVs()  # Draw AGVs on the grid
            self.draw_control()
            self.draw_AGV_info()
            pygame.display.flip()  # Update the display
            pygame.time.delay(500) 
            self.clock.tick(60)  # Cap the frame rate to 60 FPS
            counter += 1

# Creating an instance of SupervisorCenter
supervisor = SupervisorCenter()
supervisor.start()
