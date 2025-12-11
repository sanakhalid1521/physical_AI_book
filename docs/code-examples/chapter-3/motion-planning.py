"""
Example: Motion Planning and Pathfinding
This code demonstrates motion planning algorithms for humanoid robot navigation,
including A* pathfinding and trajectory optimization.
"""

import numpy as np
import matplotlib.pyplot as plt
from heapq import heappop, heappush
import math

class GridEnvironment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width))
        self.obstacles = set()

    def add_obstacle(self, x, y):
        """Add an obstacle to the grid"""
        if 0 <= x < self.width and 0 <= y < self.height:
            self.grid[y, x] = 1
            self.obstacles.add((x, y))

    def is_valid(self, x, y):
        """Check if a position is valid (not out of bounds or obstacle)"""
        return (0 <= x < self.width and
                0 <= y < self.height and
                self.grid[y, x] == 0)

    def get_neighbors(self, x, y):
        """Get valid neighboring cells"""
        neighbors = []
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1),  # 4-connectivity
                       (-1, -1), (-1, 1), (1, -1), (1, 1)]:  # Diagonals
            nx, ny = x + dx, y + dy
            if self.is_valid(nx, ny):
                # Add cost for diagonal moves
                cost = math.sqrt(2) if abs(dx) + abs(dy) == 2 else 1
                neighbors.append((nx, ny, cost))
        return neighbors

class AStarPlanner:
    def __init__(self, environment):
        self.env = environment

    def heuristic(self, pos1, pos2):
        """Calculate heuristic distance (Euclidean)"""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def plan_path(self, start, goal):
        """Plan a path using A* algorithm"""
        # Priority queue: (f_score, g_score, x, y)
        open_set = [(0, 0, start[0], start[1])]
        came_from = {}
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        while open_set:
            current_f, current_g, x, y = heappop(open_set)
            current = (x, y)

            if current == goal:
                # Reconstruct path
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.append(start)
                return path[::-1]  # Return reversed path

            for nx, ny, move_cost in self.env.get_neighbors(x, y):
                neighbor = (nx, ny)
                tentative_g = current_g + move_cost

                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self.heuristic(neighbor, goal)
                    heappush(open_set, (f_score[neighbor], tentative_g, nx, ny))

        return []  # No path found

class TrajectoryOptimizer:
    def __init__(self):
        pass

    def smooth_path(self, path, weight_data=0.5, weight_smooth=0.1, tolerance=0.00001):
        """Smooth a path using optimization"""
        if len(path) < 3:
            return path

        # Convert path to numpy array for easier manipulation
        smoothed_path = np.array(path, dtype=float)

        change = tolerance
        while change >= tolerance:
            change = 0.0
            for i in range(1, len(path) - 1):
                for j in range(len(path[0])):  # For x and y coordinates
                    aux = smoothed_path[i][j]
                    # Smooth based on original path and neighbors
                    smoothed_path[i][j] += weight_data * (path[i][j] - smoothed_path[i][j])
                    smoothed_path[i][j] += weight_smooth * (smoothed_path[i-1][j] +
                                                           smoothed_path[i+1][j] -
                                                           2.0 * smoothed_path[i][j])
                    change += abs(aux - smoothed_path[i][j])

        return [tuple(point) for point in smoothed_path]

def create_sample_environment():
    """Create a sample environment with obstacles"""
    env = GridEnvironment(20, 20)

    # Add some obstacles to create a maze-like environment
    for i in range(5, 15):
        env.add_obstacle(i, 10)  # Horizontal wall

    for i in range(5, 10):
        env.add_obstacle(5, i)   # Vertical wall

    for i in range(12, 18):
        env.add_obstacle(i, 5)   # Another horizontal wall

    for i in range(12, 17):
        env.add_obstacle(15, i)  # Vertical wall

    return env

def main():
    # Create environment
    env = create_sample_environment()

    # Define start and goal positions
    start = (1, 1)
    goal = (18, 18)

    # Plan path using A*
    planner = AStarPlanner(env)
    path = planner.plan_path(start, goal)

    if path:
        print(f"Path found with {len(path)} steps")

        # Optimize the path
        optimizer = TrajectoryOptimizer()
        smoothed_path = optimizer.smooth_path(path)

        # Visualize the results
        plt.figure(figsize=(12, 5))

        # Plot original grid
        plt.subplot(1, 2, 1)
        plt.imshow(env.grid, cmap='binary', origin='upper')

        # Plot path
        if path:
            path_array = np.array(path)
            plt.plot(path_array[:, 0], path_array[:, 1], 'r-', linewidth=2, label='A* Path')
            plt.plot(start[0], start[1], 'go', markersize=10, label='Start')
            plt.plot(goal[0], goal[1], 'ro', markersize=10, label='Goal')

        plt.title('A* Path Planning')
        plt.legend()

        # Plot smoothed path
        plt.subplot(1, 2, 2)
        plt.imshow(env.grid, cmap='binary', origin='upper')

        if smoothed_path:
            smoothed_array = np.array(smoothed_path)
            plt.plot(smoothed_array[:, 0], smoothed_array[:, 1], 'b-', linewidth=2, label='Smoothed Path')
            plt.plot(start[0], start[1], 'go', markersize=10, label='Start')
            plt.plot(goal[0], goal[1], 'ro', markersize=10, label='Goal')

        plt.title('Smoothed Trajectory')
        plt.legend()

        plt.tight_layout()
        plt.show()

        print("Motion planning complete! Path found and optimized.")
    else:
        print("No path found from start to goal")

if __name__ == "__main__":
    main()