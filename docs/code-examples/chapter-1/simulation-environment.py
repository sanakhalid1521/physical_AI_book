"""
Example: Simulation Environment Setup
This code demonstrates setting up a basic simulation environment for humanoid robots
using PyBullet physics engine.
"""

import pybullet as p
import pybullet_data
import time
import numpy as np

class SimulationEnvironment:
    def __init__(self):
        # Connect to physics server
        self.physicsClient = p.connect(p.GUI)  # or p.DIRECT for non-graphical version
        p.setAdditionalSearchPath(pybullet_data.getDataPath())

        # Set gravity
        p.setGravity(0, 0, -9.81)

        # Load plane
        self.planeId = p.loadURDF("plane.urdf")

        # Store robot ID
        self.robotId = None

    def load_humanoid_robot(self):
        """Load a simple humanoid robot model"""
        # For this example, we'll use a simple model
        # In practice, you might load a more complex URDF
        self.robotId = p.loadURDF("r2d2.urdf", [0, 0, 1])
        print("Humanoid robot loaded in simulation")

    def get_robot_state(self):
        """Get current state of the robot"""
        if self.robotId is None:
            return None

        position, orientation = p.getBasePositionAndOrientation(self.robotId)
        linear_vel, angular_vel = p.getBaseVelocity(self.robotId)

        return {
            'position': position,
            'orientation': orientation,
            'linear_velocity': linear_vel,
            'angular_velocity': angular_vel
        }

    def apply_force(self, link_index, force, position):
        """Apply force to a specific link of the robot"""
        p.applyExternalForce(
            self.robotId,
            link_index,
            force,
            position,
            p.WORLD_FRAME
        )

    def step_simulation(self):
        """Step the simulation forward"""
        p.stepSimulation()
        time.sleep(1./240.)  # Slow down to real-time

    def reset_simulation(self):
        """Reset the simulation"""
        p.resetSimulation()

    def disconnect(self):
        """Disconnect from physics server"""
        p.disconnect()

def main():
    # Create simulation environment
    sim = SimulationEnvironment()

    # Load humanoid robot
    sim.load_humanoid_robot()

    print("Simulation environment ready!")
    print("Starting simulation loop...")

    # Run simulation for a few steps
    for i in range(100):
        robot_state = sim.get_robot_state()
        if robot_state:
            print(f"Step {i}: Position = {robot_state['position'][:2]}")  # Just x, y

        sim.step_simulation()

        # Apply a small force occasionally to see movement
        if i % 50 == 0 and sim.robotId is not None:
            sim.apply_force(-1, [10, 0, 0], [0, 0, 0])

    # Clean up
    sim.disconnect()
    print("Simulation finished!")

if __name__ == "__main__":
    main()