import math
import sys
import pygame
from collections import defaultdict
from typing import List
from AStar import a_star_search
from boardCenter import board, generateBoard  # Importing the boardCenter module
from agv import AGV
from Cell import Cell  # Importing the AGV class

store_image = pygame.image.load("house.png")
depot_image = pygame.image.load("depot.png")
charging_station_image = pygame.image.load("station.png")
rock_image = pygame.image.load("rock.png")
agv_image = pygame.image.load("agv-robot.png")
agv_image_2 = pygame.image.load("agv2.jpg")
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
    "path": [(4, 4), (5, 4), (6, 4), (5, 4),(4, 4), (4,4),(5, 4), (6, 4), (7, 4), (7, 5), (7, 6), (7, 7), (7, 8), (7, 9), (8, 9)]
},
{
    "station": 1,
    "color": "#22c55e",
    "energy": 100,
    "icon": agv_image_2,
    "path": [(8, 9), (7, 9), (7, 8), (7, 7), (7, 6), (7, 5), (7, 4), (6, 4), (5,4), (5, 5), [4, 5], (4, 4),  (4, 5), (4, 6), (4, 7), (3, 7), (2, 7), (2, 8), (2, 9), (1, 9), (0, 9)]
},
]
class SupervisorCenter:
    def __init__(self):
        self.stations = []
        self.stores = []
        self.board = board
        self.depots = []
        self.grid: list[list[Cell]] = self.board  # Accessing the board from boardCenter
        self.AGVs: list[AGV] = []
        self.screen_width, self.screen_height = 1200, 860
        self.intersection = []
        self.ROW = len(self.board)
        self.COL = len(self.board[0])
        self.cell_size = 50  # Size of each cell
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        self.insert_rock_button_rect = pygame.Rect(self.screen_width - 180, 50, 160, 50)  # Define button rectangle
        self.pre_routing_to_station = defaultdict(list)
        self.pre_routing_to_store = defaultdict(list)
        self.pre_routing_to_depot = defaultdict(list)
        self.pre_routing_to_goback_depot = defaultdict(list)
        pygame.font.init()
        font_path = "./fonts/BeVietnamPro-Medium.ttf"  # Replace with the path to your font file
        font_size = 16  # Adjust size as needed
        self.font = pygame.font.Font(font_path, font_size)

        self.is_running = True
        self.is_paused = False
        # Buttons
        self.stop_button_rect = pygame.Rect(600, 50, 150, 50)
        self.continue_button_rect = pygame.Rect(600, 150, 150, 50)
        
    def draw_totalTime(self):
        pass
    def draw_buttons(self, board_width, board_height):
    # Draw stop button
        stop_button_rect = pygame.Rect(self.screen_width - board_width, board_height - 80, 100, 50)
        pygame.draw.rect(self.screen, (255, 0, 0), stop_button_rect)
        stop_button_text = self.font.render("Stop", True, (255, 255, 255))
        stop_button_text_rect = stop_button_text.get_rect(center=stop_button_rect.center)
        self.screen.blit(stop_button_text, stop_button_text_rect)
        
        # Draw continue button
        continue_button_rect = pygame.Rect(self.screen_width - board_width + 150, board_height - 80, 150, 50)
        pygame.draw.rect(self.screen, (0, 255, 0), continue_button_rect)
        continue_button_text = self.font.render("Continue", True, (255, 255, 255))
        continue_button_text_rect = continue_button_text.get_rect(center=continue_button_rect.center)
        self.screen.blit(continue_button_text, continue_button_text_rect)

        mouse_pos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if click[0]:  # Check if left mouse button is clicked
            if stop_button_rect.collidepoint(mouse_pos):
                # Handle stop button click
                self.is_paused = True
                # Add your stop game logic here
            elif continue_button_rect.collidepoint(mouse_pos):
                # Handle continue button click
                self.is_paused = False
                print("Continue button clicked")
    def preRouting(self):
        visited = [[False for _ in range(self.COL)] for _ in range(self.ROW)]
        
        # Calculate shortest paths from stations to depots
        for station in self.stations:
            shortestPath = self.findShortestPath(station, dest=self.depots)
            if shortestPath is None:
                continue
            self.pre_routing_to_depot[(station[0], station[1])] = shortestPath
            for path in shortestPath:
                visited[path[0]][path[1]] = True
                # self.grid[path[0]][path[1]].status = 0
        
        # Calculate shortest paths from depots to stores
        for depot in self.depots:
            shortestPath = self.findShortestPath(depot, self.stores)
            print('Path go to store::' , shortestPath)
            if shortestPath is None:
                continue
            self.pre_routing_to_store[tuple(depot)] = shortestPath
            for path in shortestPath:
                visited[path[0]][path[1]] = True
                # self.grid[path[0]][path[1]].status = 0
        
        # Calculate shortest paths from stores to go-back depots
        for store in self.stores:
            shortestPath = self.findShortestPath(store, self.depots)
            if shortestPath is None:
                continue
            self.pre_routing_to_goback_depot[tuple(store)] = shortestPath
            for path in shortestPath:
                visited[path[0]][path[1]] = True
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
        # return
        i = 0
        for agv in self.AGVs:
            x, y = agv.position
            # Calculate the coordinates based on cell size and position
            agv_x = y * (500 // self.COL) + (500 // self.COL - self.cell_size) // 2  # Adjusted x-coordinate
            agv_y = x * (500 // self.ROW) + (500 // self.ROW - self.cell_size) // 2  # Adjusted y-coordinate
            if data[i].get("icon"):
                draw_agv = pygame.transform.scale(data[i].get("icon"), (self.cell_size, self.cell_size))
            else:
                draw_agv = pygame.transform.scale(agv_image, (self.cell_size, self.cell_size))
            self.screen.blit(draw_agv, (agv_x, agv_y))
            i += 1
            # pygame.draw.rect(self.screen, STATUS_COLORS[agv.status], (agv_x, agv_y, self.cell_size, self.cell_size))
    def draw_AGV_info(self):
    # Draw AGV information board
        board_width = 600  # Increased width to accommodate table
        board_height = self.screen_height
        pygame.draw.rect(self.screen, (200, 200, 200), (self.screen_width - board_width, 0, board_width, board_height))

        # Define column positions
        col_positions = [self.screen_width - board_width + 10, self.screen_width - board_width + 130, self.screen_width - board_width + 340, self.screen_width - board_width + 450, self.screen_width - board_width + 560]

        # Display table headers
        headers = ["AGV ID", "Status", "Energy", "Position", "Path"]
        header_y = 20
        for i, header in enumerate(headers):
            header_render = self.font.render(header, True, (0, 0, 0))
            header_rect = header_render.get_rect(midleft=(col_positions[i], header_y))
            self.screen.blit(header_render, header_rect)

        # Display AGV information
        text_y = 60  # Start Y position for AGV info
        for agv in self.AGVs:
            agv_info = [f"{agv.id}", f"{STATUS_LABEL.get(agv.status, 'Unknown')}", f"{agv.energy}", f"{agv.position}",f"{len(agv.path) if agv.path else 0}"]
            for i, info in enumerate(agv_info):
                text_render = self.font.render(info, True, (0, 0, 0))
                text_rect = text_render.get_rect(midleft=(col_positions[i], text_y))
                self.screen.blit(text_render, text_rect)
            text_y += 30  # Move to next row
        self.draw_buttons(board_width, board_height)

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
                if cell.agv:
                    agv = cell.agv
                    x, y = agv.position
                    # Calculate the coordinates based on cell size and position
                    agv_x = y * (500 // self.COL) + (500 // self.COL - self.cell_size) // 2  # Adjusted x-coordinate
                    agv_y = x * (500 // self.ROW) + (500 // self.ROW - self.cell_size) // 2  # Adjusted y-coordinate
                    draw_agv = pygame.transform.scale(agv_image, (self.cell_size, self.cell_size))
                    self.screen.blit(draw_agv, (agv_x, agv_y))
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
    
    def findShortestPath(self, start: List[int], dest: List[int]) -> List[int]:
        minCosts = INF
        minRoute = None
        directions = [(0, 1), (0, -1), (-1, 0)]
        for d in dest:
          if dest == self.stations:
              directions =  [(0, 1), (0, -1), (1, 0)]
          route = a_star_search(self.grid, start, d, directions)
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
            # agv.path = self.pre_routing_to_store.get((next_x, next_y))
            agv.status = STATUS["GOING_STORE"]
            agv.stop = 3
            agv.final_destination = agv.path[-1] if agv.path else None
        elif list(next_point)  in self.stores:
            agv.status = STATUS["GOING_DEPOT"]
            agv.stop = 3
            # Update AGV's path and final destination to go to a depot
            agv.path = self.pre_routing_to_goback_depot.get(tuple(next_point))
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
            path = data[i]["path"]
            agv = AGV(self.grid, self.stations[station], self.stores[0])
            agv.path = path
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
        pygame.display.flip()  # Update the display
        self.clock.tick(60)  # Cap the frame rate to 60 FPS
        for i in range(len(self.AGVs)):
          agv = self.AGVs[i]
          agv.id = i
        #   agv.path = self.pre_routing_to_depot[tuple(agv.position)]
        running = True
        counter = 0
        listDone = [False for _ in range(len(self.AGVs))]
        while self.is_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_running = False
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
