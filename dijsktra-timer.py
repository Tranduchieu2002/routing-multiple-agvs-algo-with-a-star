import matplotlib.pyplot as plt
import time

from dijkstra import dijkstra_search
from boardCenter import generateBoard

# Test the A* search algorithm for various board sizes
board_sizes = [200, 300, 400, 500, 600, 700, 800, 900, 1000]
time_results = []
step_results = []

for size in board_sizes:
    grid = generateBoard(size)
    start_pos = (size - 1, 0)
    goal_pos = (0, 0)
    start_time = time.time()
    path = dijkstra_search(grid, start_pos, goal_pos)
    end_time = time.time()
    execution_time = end_time - start_time
    time_results.append(execution_time)
    if path:
        steps = len(path)
        step_results.append(steps)
    else:
        step_results.append(None)

# Plotting
plt.figure(figsize=(10, 5))

plt.subplot(1, 2, 1)
plt.plot(board_sizes, time_results, marker='o', color='b')
plt.title('Thời gian thực thi và kích thước bảng')
plt.xlabel('Kích thước bảng')
plt.ylabel('Thời gian chạy (seconds)')

plt.subplot(1, 2, 2)
plt.plot(board_sizes, step_results, marker='o', color='r')
plt.title('Số bước và kích thước bảng')
plt.xlabel('Kích thước bảng')
plt.ylabel('Số bước')

plt.tight_layout()
plt.show()
