import math
import sys
import pygame
from collections import defaultdict
from typing import List
from DFS import dfs_search, find_path_dfs
from constants import *
from dijkstra import dijkstra_search
from AStar import a_star_search
from boardCenter import board, generateBoard  # Importing the boardCenter module
from agv import AGV
from Cell import Cell
from widgets import Alignment, Button, Label, Table, TableCell, Frame  # Importing the AGV class

store_image = pygame.image.load("res/images/house.png")
depot_image = pygame.image.load("res/images/depot.png")
charging_station_image = pygame.image.load("res/images/station.png")
rock_image = pygame.image.load("res/images/rock.png")
agv_image = pygame.image.load("res/images/agv-robot.png")
STATUS_LABEL = {
    0: 'Sẵn sàng nhận lệnh',
    1: 'Đi đến kho hàng',
    2: 'Đang đến cửa hàng',
    3: 'Đang trở về trạm sạc'
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
    "color": "#22c55e",
    "energy": 100,
},
{
    "station": 1,
    "color": "#22c55e",
    "energy": 100,
},
{
    "station": 1,
    "color": "#22c55e",
    "energy": 100,
},
{
    "station": 0,
    "color": "#22c55e",
    "energy": 100,
},
]
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWACCEL)

class SupervisorCenter:
    def __init__(self):
        self.stations = []
        self.stores = []
        self.board = generateBoard(15)
        self.depots = []
        self.grid: list[list[Cell]] = self.board  # Accessing the board from boardCenter
        self.AGVs: list[AGV] = []
        self.intersection = []
        self.ROW = len(self.board)
        self.COL = len(self.board[0])
        self.cell_size = CELL_SIZE
        self.screen = WINDOW
        self.clock = pygame.time.Clock()
        self.insert_rock_button_rect = pygame.Rect(SCREEN_WIDTH - 180, 50, 160, 50)  # Define button rectangle
        self.pre_routing_to_station = defaultdict(list)
        self.pre_routing_to_store = defaultdict(list)
        self.pre_routing_to_depot = defaultdict(list)
        self.pre_routing_to_goback_depot = defaultdict(list)
        pygame.font.init()
        font_path = "./fonts/BeVietnamPro-Medium.ttf"  # Replace with the path to your font file
        font_size = 16  # Adjust size as needed
        self.font = pygame.font.Font(font_path, font_size)

        self.is_running = True
        self.is_paused = True
        # Buttons
        self.stop_button_rect = pygame.Rect(600, 50, 150, 50)
        self.continue_button_rect = pygame.Rect(600, 150, 150, 50)
        self.stop_btn = None
        self.start_btn = None
        self.create_buttons()
        self.agv_info_table = self.create_agv_info_table()

    def draw(self):
        # Draw AGV info table
        self.create_agv_info_table()

        # Draw buttons
        self.start_btn.draw()
        self.stop_btn.draw()

        pygame.display.flip()  # Update the display

    def create_buttons(self):
        # Create Button instance for Stop button
        self.stop_btn = Button(
            "Stop",
            0,
            0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            padding=6,
            font_size=20,
            outline=False,
            surface=self.screen,
        )
        # Position the Stop button
        self.stop_btn.rect.centery = HEIGHT // 2
        self.stop_btn.rect.right = WIDTH - 20

        # Create Button instance for Start button
        self.start_btn = Button(
            "Start",
            0,
            0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            padding=6,
            font_size=20,
            outline=False,
            surface=self.screen,
        )
        # Position the Start button
        self.start_btn.rect.centery = HEIGHT // 2
        self.start_btn.rect.right = self.stop_btn.rect.left - 10

    def preRouting(self):
        visited = [[False for _ in range(self.COL)] for _ in range(self.ROW)]
        
        # Calculate shortest paths from stations to depots
        for station in self.stations:
            shortestPath = self.findShortestPath(station, dest=self.depots)
            if shortestPath is None:
                continue
            self.pre_routing_to_depot[(station[0], station[1])] = shortestPath
            # for path in shortestPath:
                # visited[path[0]][path[1]] = True
                # self.grid[path[0]][path[1]].status = 0
        
        # Calculate shortest paths from depots to stores
        for depot in self.depots:
            shortestPath = self.findShortestPath(depot, self.stores)
            if shortestPath is None:
                continue
            self.pre_routing_to_store[tuple(depot)] = shortestPath
            # for path in shortestPath:
            #     # visited[path[0]][path[1]] = True
            #     self.grid[path[0]][path[1]].status = 0
        
        # Calculate shortest paths from stores to go-back depots
        for store in self.stores:
            shortestPath = self.findShortestPath(store, self.stations, )
            print('Path go to depot::' , shortestPath)
            if shortestPath is None:
                continue
            self.pre_routing_to_goback_depot[tuple(store)] = shortestPath
            # for path in shortestPath:
            #     visited[path[0]][path[1]] = True
                # self.grid[path[0]][path[1]].status = 0
                
        # Mark visited cells as inaccessible
        self.grid = self.board


        # for store in self.stores:
        #     pre_routing[store].append(self.findShortestInMultiRoutes(store, self.depots))
        # for depot in self.depots:
        #     pre_routing[depot].append(self.findShortestInMultiRoutes(depot, self.stores))
        #     pre_routing[depot].append(self.findShortestInMultiRoutes(depot, self.stations))
    def initObjects(self):
        self.stations = [[self.ROW - 1, 0],[self.ROW - 1, self.COL - 1]]
        for station in self.stations:
            self.grid[station[0]][station[1]].status = 1
            self.grid[station[0]][station[1]].isChargingStation = True
        self.stores = [[0, 0], [0, (self.COL - 1)]]
        for store in self.stores:
            self.grid[store[0]][store[1]].isStore = True
            self.grid[store[0]][store[1]].status = 1
        self.depots = [[(self.ROW - 1) // 2, (self.COL - 1) // 2],[(self.ROW - 1) // 2, (self.COL - 1)]]
        for depot in self.depots:
            self.grid[depot[0]][depot[1]].isDepot = True
            self.grid[depot[0]][depot[1]].status = 1

    def draw_control(self):
        pass
    def draw_AGVs(self):
        # Iterate through AGVs and draw them on the grid
        for agv in self.AGVs:
            x, y = agv.position
            # Calculate the coordinates based on cell size and position
            agv_x = y * (MAZE_WIDTH // self.COL) + (MAZE_WIDTH // self.COL - self.cell_size) // 2
            agv_y = x * (MAZE_HEIGHT // self.ROW) + (MAZE_HEIGHT // self.ROW - self.cell_size) // 2
            draw_agv = pygame.transform.scale(agv_image, (self.cell_size, self.cell_size))
            self.screen.blit(draw_agv, (agv_x, agv_y))

            # pygame.draw.rect(self.screen, STATUS_COLORS[agv.status], (agv_x, agv_y, self.cell_size, self.cell_size))
    def create_agv_info_table(self):
    # Check if there are AGVs present
        if not self.AGVs:
            print("No AGVs present.")
            return
        table_cells = []

        # Define the layout of the AGV info table
        agv_info = []
        table_cells: list[list[TableCell]] = [[
        TableCell(
            child=Label(
                "AGV ID", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            ),
            color=DARK_BLUE,
        ),
        TableCell(
            child=Label(
                "Status", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            ),
            color=DARK_BLUE,
        ),
        TableCell(
            child=Label(
                "Energy", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            ),
            color=DARK_BLUE,
        ),
        TableCell(
            child=Label(
                "Position", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            ),
            color=DARK_BLUE,
        ),
        TableCell(
            child=Label(
                "Path", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=WINDOW,
            ),
            color=DARK_BLUE,
        ),
    ]]
        headers = ["AGV ID", "Status", "Energy", "Position", "Path"]
        for agv in self.AGVs:
            agv_data = [
                str(agv.id),
                STATUS_LABEL.get(agv.status, 'Unknown'),
                str(agv.energy),
                str(agv.position),
                str(len(agv.path) if agv.path else "No Path")
            ]
            agv_info.append(agv_data)

        # Create a frame to contain the board control and AGV info table
        frame_width = BOARD_WIDTH
        frame_x = MAZE_WIDTH + 10  # Position the frame to the right of the maze
        frame_y = 100  # Adjust this value as needed for the vertical position

        # Populate table cells with AGV information
        for i in range(len(agv_info)):
            row_cells = []
            for j in range(len(headers)):
                cell_content = agv_info[i][j] if len(agv_info[i]) > j else ''  # Check if the data exists
                cell = TableCell(
                    child=Label(
                        cell_content, 0, 0,
                        background_color=pygame.Color(*WHITE),
                        foreground_color=pygame.Color(*BLACK),
                        padding=6, font_size=20, outline=False,
                        surface=self.screen,
                    ),
                    color=WHITE
                )
                row_cells.append(cell)
            table_cells.append(row_cells)

        frame = Frame(frame_x, 10, frame_width, 300, self.screen)  # Note: Height set to 0 initially
        table = Table(frame_x, frame_y,  len(table_cells), len(headers), table_cells,)
        frame.mount(table,0, 0)
        frame.draw()
        
        self.create_buttons()

    def checkConflict(self, agv: AGV):
        isConflict = False
        if agv.path:
            for nextPath in agv.path[:min(len(agv.path), BASE)]:
                print('Check conflict', nextPath)
                if self.grid[nextPath[0]][nextPath[1]].agv is not None:
                    isConflict = True
                    break
        return isConflict

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    # Check if stop button is clicked
                    print(event.pos)
                    if self.stop_button_rect.collidepoint(event.pos):
                        self.is_paused = True
                    # Check if continue button is clicked
                    elif self.continue_button_rect.collidepoint(event.pos):
                        self.is_paused = False
    def draw_grid(self):
        grid_width = MAZE_WIDTH
        grid_height = MAZE_HEIGHT
        cell_width = grid_width // self.COL
        cell_height = grid_height // self.ROW

        for i in range(self.ROW + 1):
            pygame.draw.line(self.screen, (150, 150, 150), (0, i * cell_height), (grid_width, i * cell_height))
        for j in range(self.COL + 1):
            pygame.draw.line(self.screen, (150, 150, 150), (j * cell_width, 0), (j * cell_width, grid_height))

        for i in range(self.ROW):
            for j in range(self.COL):
                cell = self.grid[i][j]
                image = None  
                if cell.isStore:
                    image = store_image  
                elif cell.isDepot:
                    image = depot_image  
                elif cell.isChargingStation:
                    image = charging_station_image  
                elif cell.status == 0:
                    image = rock_image
                if cell.agv:
                    agv = cell.agv
                    x, y = agv.position
                    agv_x = y * (MAZE_WIDTH // self.COL) + (MAZE_WIDTH // self.COL - self.cell_size) // 2
                    agv_y = x * (MAZE_HEIGHT // self.ROW) + (MAZE_HEIGHT // self.ROW - self.cell_size) // 2
                    draw_agv = pygame.transform.scale(agv_image, (self.cell_size, self.cell_size))
                    self.screen.blit(draw_agv, (agv_x, agv_y))
                if image:
                    image = pygame.transform.scale(image, (cell_width, cell_height))
                    self.screen.blit(image, (j * cell_width, i * cell_height))

        font = pygame.font.Font(None, 24)
        text = font.render("Insert Rock", True, (255, 255, 255))
        text_rect = text.get_rect(center=self.insert_rock_button_rect.center)
        self.screen.blit(text, text_rect)
    def findShortestPath(self, start: List[int], dest: List[int], directions = [(0, 1), (0, -1), (-1, 0),(1,0)]) -> List[int]:
        minCosts = INF
        minRoute = None
        for d in dest:
          if dest in self.stations:
              directions =  [(0, 1), (0, -1), (1, 0)]
          route = dijkstra_search(self.grid, start, d, directions)
          if route == None:
              continue
          if route != None and len(route) < minCosts:
              minCosts = len(route)
              minRoute = route
          minCosts = min(minCosts, len(route))
        
        return minRoute
    def findShortestInMultiRoutes(self, agv: AGV, dest: List[List[int]]):
        minCosts = INF
        minRoute = None
        print('Final Destination', self.stores[0])
        agv.final_destination = self.stores[0].copy()
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
        if len(minRoute) > agv.energy:
            minRoute = None
        else:
            agv.energy -= len(minRoute)
        
        if (minRoute == None):
            agv.stop = 100
        agv.path = minRoute
        agv.final_destination = finalDestination
    def move(self, agv: AGV):
        if agv.status == STATUS["INSTATION"] and agv.isStart:
            agv.status == STATUS["GOING_DEPOT"]
        path = agv.path
        if not path or agv.energy <= 10:  # No path, AGV is idle
            return
        isConflict = self.checkConflict(agv)
        agv.energy -= 1
        next_point = path[0]  # Next position in the path
        
        next_x, next_y = next_point

        # Check if next position is occupied by another AGV
        if isConflict and self.grid[next_x][next_y].agv is not None and [next_x, next_y] not in self.depots and [next_x, next_y] not in self.stores:
            # Conflict, AGV stops moving
            agv.stop = 3
            return

        # Move AGV
        self.grid[agv.position[0]][agv.position[1]].agv = None  # Clear current position
        self.grid[next_x][next_y].agv = agv  # Update next position
        agv.position = next_point  # Update AGV's position

        # Check if AGV reached a depot or store
        if list(next_point) in self.depots:
            print(self.pre_routing_to_goback_depot.keys())
            # Update AGV's path and final destination to go to a depot
            agv.path = self.pre_routing_to_store.get((next_x, next_y))
            agv.status = STATUS["GOING_STORE"]
            agv.stop = 3
            agv.final_destination = agv.path[-1] if agv.path else None
        if list(next_point) in self.stores:
            agv.status = STATUS["GOBACK"]
            agv.stop = 3
            # Update AGV's path and final destination to go to a depot
            agv.path = self.pre_routing_to_goback_depot.get((next_x, next_y))
            agv.final_destination = agv.path[-1] if agv.path else None
        else:
            # AGV is moving towards its current destination
            agv.final_destination = agv.path[-1] if agv.path else None
            if not agv.path:  # AGV reached its destination
                agv.status = STATUS["INSTATION"]  # Update AGV's status
                agv.final_destination = None
        
        # Remove the first position from the path as AGV moved to that position
        if (agv.path):
            agv.path = agv.path[1:]
    def deadlock(self, agv: AGV):
        stuck: bool = False
        cur = agv.position
        
        pass
    def initAGVs(self):
        stops = defaultdict(int)
        for i in range(len(data)):
            station = data[i]["station"]
            energy = data[i]["energy"]
            agv = AGV(self.grid, self.stations[station], self.stores[0])
            # star together have to wait 3s
            if stops[station]:
                agv.stop = 3
            agv.energy = energy
            stops[station] += 3
            agv.stop = stops.get(station, 0)
            self.AGVs.append(agv)
    def start(self):
        print("Starting the Supervisor Center")
        self.initObjects()
        pygame.init()
        self.preRouting()
        self.initAGVs()
        self.screen.fill((255, 255, 255))  # Fill screen with white
        self.draw_grid()  # Draw grid lines
        self.draw()
        pygame.display.flip()  # Update the display
        self.clock.tick(60)  # Cap the frame rate to 60 FPS

        # Set is_paused to True initially
        self.is_paused = True

        # Draw buttons before starting the simulation
        # self.draw_AGV_info()
        pygame.display.flip()

        for i in range(len(self.AGVs)):
            agv = self.AGVs[i]
            agv.id = i
            agv.path = self.pre_routing_to_depot[tuple(agv.position)]

        counter = 0
        listDone = [False for _ in range(len(self.AGVs))]

        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        # Check if the mouse click occurred within the bounds of the stop button
                        if self.stop_btn.rect.collidepoint(event.pos):
                            # Execute the stop action here
                            self.is_paused = True
                        # Check if the mouse click occurred within the bounds of the start button
                        elif self.start_btn.rect.collidepoint(event.pos):
                            # Toggle the state of is_paused
                            self.is_paused = not self.is_paused

            # If paused, skip simulation logic
            if self.is_paused:
                continue
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
                print('AGV  ' + str(agv.id) + '  ' + STATUS_LABEL[agv.status] , agv.path)
            print('Bước ' + str((counter + 1)))
            self.screen.fill(WHITE)  # Clear the screen
            self.draw_grid()  # Redraw grid lines
            self.draw_AGVs()  # Draw AGVs on the grid
            self.draw_control()
            self.draw()
            pygame.display.flip()
            pygame.time.delay(500) 
            self.clock.tick(60)  # Cap the frame rate to 60 FPS
            counter += 1

# Creating an instance of SupervisorCenter
supervisor = SupervisorCenter()
supervisor.start()
