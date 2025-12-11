"""
Example: Real-World Deployment Challenges
This code demonstrates approaches to handle challenges of deploying humanoid robots
in real-world environments, including uncertainty handling and safety measures.
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple, Optional

class SafetyLevel(Enum):
    """Safety levels for robot operation"""
    NORMAL = "normal"
    CAUTION = "caution"
    WARNING = "warning"
    EMERGENCY = "emergency"

@dataclass
class RobotState:
    """Current state of the robot"""
    position: Tuple[float, float, float]
    orientation: Tuple[float, float, float]  # Roll, pitch, yaw
    velocity: Tuple[float, float, float]
    joint_angles: List[float]
    battery_level: float
    temperature: float

@dataclass
class EnvironmentalState:
    """State of the environment around the robot"""
    obstacles: List[Tuple[float, float, float]]  # x, y, radius
    humans_nearby: List[Tuple[float, float]]     # x, y positions
    surface_conditions: str                      # flat, uneven, slippery, etc.
    lighting_conditions: str                     # bright, dim, dark
    noise_level: float                          # 0.0 to 1.0

class UncertaintyHandler:
    """Handles uncertainty in perception and action"""
    def __init__(self):
        self.uncertainty_models = {}
        self.confidence_thresholds = {
            'position': 0.8,
            'obstacle_detection': 0.7,
            'human_detection': 0.75
        }

    def estimate_uncertainty(self, sensor_reading, sensor_type):
        """Estimate uncertainty based on sensor type and reading"""
        base_uncertainty = {
            'lidar': 0.05,
            'camera': 0.1,
            'imu': 0.02,
            'force_torque': 0.08
        }

        # Add environmental factors
        uncertainty = base_uncertainty.get(sensor_type, 0.1)

        # Increase uncertainty in poor conditions
        if sensor_type == 'camera':
            # Camera uncertainty increases with poor lighting
            uncertainty *= random.uniform(1.0, 2.0)  # Simulate varying conditions

        return uncertainty

    def propagate_uncertainty(self, control_input, time_step):
        """Propagate uncertainty through robot dynamics"""
        # Simplified uncertainty propagation
        process_noise = np.array([0.01, 0.01, 0.05])  # position, orientation, velocity
        return process_noise * time_step

class SafetyMonitor:
    """Monitors safety conditions and triggers appropriate responses"""
    def __init__(self):
        self.safety_level = SafetyLevel.NORMAL
        self.emergency_stop_active = False
        self.safety_history = []

    def assess_situation(self, robot_state: RobotState, env_state: EnvironmentalState) -> SafetyLevel:
        """Assess current safety level based on robot and environment state"""
        safety_factors = []

        # Check proximity to humans
        if env_state.humans_nearby:
            for human_pos in env_state.humans_nearby:
                robot_pos = robot_state.position
                distance = np.sqrt(sum((a-b)**2 for a, b in zip(robot_pos[:2], human_pos)))
                if distance < 0.5:  # Less than 0.5m is dangerous
                    safety_factors.append(SafetyLevel.EMERGENCY)
                elif distance < 1.0:  # Less than 1m is caution
                    safety_factors.append(SafetyLevel.WARNING)

        # Check battery level
        if robot_state.battery_level < 0.15:  # Below 15% is dangerous
            safety_factors.append(SafetyLevel.WARNING)

        # Check temperature
        if robot_state.temperature > 75:  # Overheating
            safety_factors.append(SafetyLevel.WARNING)

        # Check surface conditions
        if env_state.surface_conditions in ['uneven', 'slippery']:
            safety_factors.append(SafetyLevel.CAUTION)

        # Determine overall safety level
        if SafetyLevel.EMERGENCY in safety_factors:
            return SafetyLevel.EMERGENCY
        elif SafetyLevel.WARNING in safety_factors:
            return SafetyLevel.WARNING
        elif SafetyLevel.CAUTION in safety_factors:
            return SafetyLevel.CAUTION
        else:
            return SafetyLevel.NORMAL

    def trigger_response(self, safety_level: SafetyLevel):
        """Trigger appropriate safety response"""
        if safety_level == SafetyLevel.EMERGENCY:
            self.emergency_stop_active = True
            print("EMERGENCY STOP ACTIVATED")
        elif safety_level == SafetyLevel.WARNING:
            print("WARNING: Reducing speed and increasing caution")
        elif safety_level == SafetyLevel.CAUTION:
            print("CAUTION: Adjusting behavior for safety")
        else:
            self.emergency_stop_active = False

class RobustController:
    """Controller that handles uncertainty and disturbances"""
    def __init__(self):
        self.uncertainty_handler = UncertaintyHandler()
        self.safety_monitor = SafetyMonitor()
        self.control_history = []

    def compute_safe_control(self, robot_state: RobotState, env_state: EnvironmentalState,
                           desired_trajectory: List[Tuple[float, float, float]]):
        """Compute control action considering safety and uncertainty"""
        # Assess current safety situation
        current_safety = self.safety_monitor.assess_situation(robot_state, env_state)
        self.safety_monitor.trigger_response(current_safety)

        if self.safety_monitor.emergency_stop_active:
            return self.emergency_stop()

        # Plan trajectory considering obstacles
        safe_trajectory = self.avoid_obstacles(robot_state, env_state, desired_trajectory)

        # Compute control with uncertainty consideration
        control_action = self.robust_control(robot_state, safe_trajectory)

        # Log for history
        self.control_history.append({
            'safety_level': current_safety,
            'control_action': control_action,
            'timestamp': len(self.control_history)
        })

        return control_action

    def avoid_obstacles(self, robot_state: RobotState, env_state: EnvironmentalState,
                       desired_trajectory: List[Tuple[float, float, float]]):
        """Modify trajectory to avoid obstacles"""
        robot_pos = robot_state.position
        safe_trajectory = []

        for point in desired_trajectory:
            # Check if point is too close to obstacles
            too_close = False
            for obs_pos in env_state.obstacles:
                distance = np.sqrt((point[0] - obs_pos[0])**2 + (point[1] - obs_pos[1])**2)
                if distance < obs_pos[2] + 0.3:  # Add safety margin
                    too_close = True
                    break

            if not too_close:
                safe_trajectory.append(point)
            else:
                # Find alternative path around obstacle
                safe_point = self.find_safe_point_around_obstacle(robot_pos, point, obs_pos)
                safe_trajectory.append(safe_point)

        return safe_trajectory

    def find_safe_point_around_obstacle(self, robot_pos, target_pos, obstacle_pos):
        """Find a safe point to navigate around an obstacle"""
        # Simple approach: go around the obstacle
        dx = target_pos[0] - robot_pos[0]
        dy = target_pos[1] - robot_pos[1]
        dist = np.sqrt(dx**2 + dy**2)

        if dist > 0:
            # Move perpendicular to the line from robot to target, avoiding obstacle
            perp_x = -dy/dist * 0.5  # 0.5m offset
            perp_y = dx/dist * 0.5
            return (obstacle_pos[0] + perp_x, obstacle_pos[1] + perp_y, target_pos[2])

        return target_pos

    def robust_control(self, robot_state: RobotState, trajectory: List[Tuple[float, float, float]]):
        """Compute robust control action"""
        if not trajectory:
            return "STOP"

        # Simple proportional control with safety considerations
        target = trajectory[0]
        current_pos = robot_state.position

        # Calculate desired movement
        dx = target[0] - current_pos[0]
        dy = target[1] - current_pos[1]

        # Consider uncertainty in control
        uncertainty = self.uncertainty_handler.estimate_uncertainty(current_pos, 'position')
        safety_factor = 1.0 - uncertainty  # Reduce speed with higher uncertainty

        # Return control command
        return {
            'type': 'move',
            'target': target,
            'speed_factor': min(safety_factor, 1.0),
            'uncertainty': uncertainty
        }

    def emergency_stop(self):
        """Emergency stop procedure"""
        return {
            'type': 'emergency_stop',
            'action': 'halt_all_motors',
            'reason': 'safety_threshold_exceeded'
        }

class DeploymentSimulator:
    """Simulates real-world deployment conditions"""
    def __init__(self):
        self.time_step = 0
        self.robot_state = RobotState(
            position=(0, 0, 0),
            orientation=(0, 0, 0),
            velocity=(0, 0, 0),
            joint_angles=[0] * 20,  # Example humanoid joint configuration
            battery_level=1.0,
            temperature=25.0
        )
        self.controller = RobustController()

    def simulate_step(self):
        """Simulate one step of deployment"""
        self.time_step += 1

        # Simulate environmental changes
        env_state = self.generate_environmental_state()

        # Simulate robot state changes
        self.update_robot_state(env_state)

        # Get desired trajectory (for this example, a simple path)
        desired_trajectory = [
            (5 + random.uniform(-0.1, 0.1), 3 + random.uniform(-0.1, 0.1), 0),
            (10 + random.uniform(-0.1, 0.1), 7 + random.uniform(-0.1, 0.1), 0)
        ]

        # Compute safe control action
        control_action = self.controller.compute_safe_control(
            self.robot_state, env_state, desired_trajectory
        )

        return control_action, env_state

    def generate_environmental_state(self) -> EnvironmentalState:
        """Generate environmental state with some randomness"""
        # Add obstacles
        obstacles = []
        if self.time_step % 20 == 0:  # Add obstacles periodically
            obstacles.append((random.uniform(2, 8), random.uniform(1, 6), 0.5))

        # Add humans periodically
        humans = []
        if self.time_step % 15 == 0:
            humans.append((random.uniform(-1, 1), random.uniform(-1, 1)))

        # Surface and lighting conditions
        surface_conditions = random.choice(['flat', 'uneven', 'slippery'])
        lighting_conditions = random.choice(['bright', 'dim', 'normal'])

        return EnvironmentalState(
            obstacles=obstacles,
            humans_nearby=humans,
            surface_conditions=surface_conditions,
            lighting_conditions=lighting_conditions,
            noise_level=random.uniform(0.0, 0.3)
        )

    def update_robot_state(self, env_state: EnvironmentalState):
        """Update robot state based on environment"""
        # Update position based on some motion (simplified)
        self.robot_state.position = (
            self.robot_state.position[0] + random.uniform(-0.1, 0.1),
            self.robot_state.position[1] + random.uniform(-0.1, 0.1),
            self.robot_state.position[2]
        )

        # Update other state variables
        self.robot_state.battery_level = max(0.0, self.robot_state.battery_level - 0.001)
        self.robot_state.temperature = 25 + random.uniform(-2, 5)

def main():
    print("Real-World Deployment Challenges Demonstration")
    print("=" * 60)

    # Initialize simulator
    simulator = DeploymentSimulator()
    safety_monitor = simulator.controller.safety_monitor

    print("\nStarting deployment simulation with safety monitoring...")

    safety_levels_over_time = []
    positions = []

    for step in range(100):
        control_action, env_state = simulator.simulate_step()

        # Record safety level
        current_safety = safety_monitor.safety_level
        safety_levels_over_time.append(current_safety.value)

        # Record position
        positions.append(simulator.robot_state.position[:2])

        if step % 20 == 0:
            print(f"Step {step}: Safety Level = {current_safety.value}, "
                  f"Control = {control_action.get('type', control_action) if isinstance(control_action, dict) else control_action}")

    print(f"\nDeployment simulation completed!")
    print(f"Final safety level: {safety_monitor.safety_level.value}")
    print(f"Final battery level: {simulator.robot_state.battery_level:.2f}")

    # Analyze safety events
    emergency_count = safety_levels_over_time.count('emergency')
    warning_count = safety_levels_over_time.count('warning')
    caution_count = safety_levels_over_time.count('caution')

    print(f"\nSafety Analysis:")
    print(f"  Emergency stops triggered: {emergency_count}")
    print(f"  Warnings issued: {warning_count}")
    print(f"  Caution periods: {caution_count}")

    # Visualization
    plt.figure(figsize=(15, 5))

    plt.subplot(1, 3, 1)
    safety_numeric = [0 if s == 'normal' else 1 if s == 'caution' else 2 if s == 'warning' else 3 for s in safety_levels_over_time]
    plt.plot(safety_numeric)
    plt.title('Safety Level Over Time')
    plt.ylabel('Safety Level (0=Normal, 3=Emergency)')
    plt.xlabel('Time Step')
    plt.grid(True)

    plt.subplot(1, 3, 2)
    positions_array = np.array(positions)
    plt.plot(positions_array[:, 0], positions_array[:, 1], 'b-', linewidth=2)
    plt.title('Robot Trajectory')
    plt.xlabel('X Position')
    plt.ylabel('Y Position')
    plt.grid(True)

    plt.subplot(1, 3, 3)
    safety_counts = [safety_levels_over_time.count('normal'), caution_count, warning_count, emergency_count]
    safety_labels = ['Normal', 'Caution', 'Warning', 'Emergency']
    plt.bar(safety_labels, safety_counts)
    plt.title('Safety Events Distribution')
    plt.ylabel('Count')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()

    print(f"\nReal-world deployment challenges demonstration complete!")
    print("Key takeaways:")
    print("- Safety monitoring is critical for real-world deployment")
    print("- Uncertainty handling improves robot reliability")
    print("- Adaptive behavior based on environmental conditions is essential")

if __name__ == "__main__":
    main()