"""
Example: Basic Physical AI Concept
This code demonstrates a simple physical AI concept where a robot learns
through interaction with its environment.
"""

import numpy as np
import matplotlib.pyplot as plt

class SimplePhysicalAI:
    def __init__(self):
        self.position = np.array([0.0, 0.0])
        self.velocity = np.array([0.0, 0.0])
        self.environment_forces = np.array([0.0, 0.0])

    def sense_environment(self, target_pos):
        """Sense the environment and calculate forces"""
        # Calculate attractive force to target
        attraction = (target_pos - self.position) * 0.1

        # Add some environmental resistance
        resistance = -self.velocity * 0.05

        self.environment_forces = attraction + resistance

    def update_motion(self):
        """Update position based on forces"""
        # Simple physics integration
        acceleration = self.environment_forces
        self.velocity += acceleration * 0.1
        self.position += self.velocity * 0.1

    def learn_from_interaction(self, target_pos):
        """Learn from interaction with environment"""
        # This is a simplified learning mechanism
        # In a real system, this would update internal models
        error = np.linalg.norm(target_pos - self.position)
        return error

def main():
    robot = SimplePhysicalAI()
    target = np.array([5.0, 3.0])

    positions = []
    for step in range(100):
        robot.sense_environment(target)
        robot.update_motion()
        error = robot.learn_from_interaction(target)
        positions.append(robot.position.copy())

        if error < 0.1:  # Close enough to target
            print(f"Target reached at step {step}")
            break

    # Plot the path
    positions = np.array(positions)
    plt.plot(positions[:, 0], positions[:, 1], 'b-', label='Robot Path')
    plt.plot(target[0], target[1], 'ro', label='Target')
    plt.plot(0, 0, 'go', label='Start')
    plt.legend()
    plt.title('Simple Physical AI: Learning through Environment Interaction')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    main()