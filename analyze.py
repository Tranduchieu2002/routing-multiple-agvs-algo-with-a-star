import time
import resource
import matplotlib.pyplot as plt
from AStar import a_star_search
from dijkstra import dijkstra_search
from boardCenter import generateBoard

def get_memory_usage():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024  # Convert to MB

def analyze_algorithms():
    input_sizes = [10, 100, 300, 700, 1000]
    a_star_time_avg = []
    a_star_steps_avg = []
    a_star_memory_avg = []

    dijkstra_time_avg = []
    dijkstra_steps_avg = []
    dijkstra_memory_avg = []

    with open('algorithm_data.txt', 'w') as file:
        file.write('Input Size,A* Time Avg,A* Steps Avg,A* Memory Avg,Dijkstra Time Avg,Dijkstra Steps Avg,Dijkstra Memory Avg\n')

        for size in input_sizes:
            grid = generateBoard(size)
            src_dest_pairs = [(generate_random_cell(grid), generate_random_cell(grid)) for _ in range(10)]  # Generate 10 random pairs
            a_star_time = []
            a_star_steps = []
            a_star_memory = []

            dijkstra_time = []
            dijkstra_steps = []
            dijkstra_memory = []

            for src, dest in src_dest_pairs:
                start_time = time.time()
                a_star_path = a_star_search(grid, src, dest)
                if a_star_path is None:
                    continue
                a_star_time.append(time.time() - start_time)
                start_time = time.time()
                dijkstra_path = dijkstra_search(grid, src, dest)
                if dijkstra_path is None:
                    continue
                dijkstra_time.append(time.time() - start_time)
                if dijkstra_path and a_star_path:
                    a_star_steps.append(len(a_star_path))
                    a_star_memory.append(get_memory_usage())
                    dijkstra_steps.append(len(dijkstra_path))
                    dijkstra_memory.append(get_memory_usage())

            a_star_time_avg.append(sum(a_star_time) / len(a_star_time) if a_star_time else 0)
            a_star_steps_avg.append(sum(a_star_steps) / len(a_star_steps) if a_star_steps else 0)
            a_star_memory_avg.append(sum(a_star_memory) / len(a_star_memory) if a_star_memory else 0)

            dijkstra_time_avg.append(sum(dijkstra_time) / len(dijkstra_time) if dijkstra_time else 0)
            dijkstra_steps_avg.append(sum(dijkstra_steps) / len(dijkstra_steps) if dijkstra_steps else 0)
            dijkstra_memory_avg.append(sum(dijkstra_memory) / len(dijkstra_memory) if dijkstra_memory else 0)

            file.write(f'{size},{a_star_time_avg[-1]},{a_star_steps_avg[-1]},{a_star_memory_avg[-1]},'
                       f'{dijkstra_time_avg[-1]},{dijkstra_steps_avg[-1]},{dijkstra_memory_avg[-1]}\n')

    plot_statistics(a_star_time_avg, dijkstra_time_avg, 'Time')
    plot_statistics(a_star_steps_avg, dijkstra_steps_avg, 'Steps')
    plot_statistics(a_star_memory_avg, dijkstra_memory_avg, 'Memory')

def plot_statistics(a_star_values, dijkstra_values, title):
    input_sizes = [10, 100, 300, 700, 1000]
    plt.figure(figsize=(8, 5))
    plt.plot(input_sizes, a_star_values, label='A* Search', marker='o')
    plt.plot(input_sizes, dijkstra_values, label="Dijkstra's Algorithm", marker='o')
    plt.title('Average ' + title + ' vs Input Size')
    plt.xlabel('Input Size')
    plt.ylabel(title)
    plt.legend()
    plt.grid(True)
    plt.show()

# Helper function to generate random cell within grid
def generate_random_cell(grid):
    ROW = len(grid)
    COL = len(grid[0])
    import random
    return (random.randint(0, ROW-1), random.randint(0, COL-1))

# Test the analysis function
analyze_algorithms()
