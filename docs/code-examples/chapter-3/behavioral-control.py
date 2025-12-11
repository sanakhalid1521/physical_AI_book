"""
Example: Behavioral Control Systems
This code demonstrates behavioral control for humanoid robots using
Finite State Machines (FSM) and Behavior Trees.
"""

import time
import random
from enum import Enum
from abc import ABC, abstractmethod

class RobotState(Enum):
    IDLE = "idle"
    WALKING = "walking"
    GRASPING = "grasping"
    AVOIDING_OBSTACLE = "avoiding_obstacle"
    RETURNING_HOME = "returning_home"

class FiniteStateMachine:
    def __init__(self):
        self.current_state = RobotState.IDLE
        self.state_start_time = time.time()
        self.target_position = None
        self.obstacle_detected = False

    def update(self, sensor_data):
        """Update FSM based on sensor data"""
        self.obstacle_detected = sensor_data.get('obstacle', False)

        # State transition logic
        if self.obstacle_detected and self.current_state == RobotState.WALKING:
            self.current_state = RobotState.AVOIDING_OBSTACLE
        elif not self.obstacle_detected and self.current_state == RobotState.AVOIDING_OBSTACLE:
            self.current_state = RobotState.WALKING
        elif self.current_state == RobotState.GRASPING and sensor_data.get('object_grasped', False):
            self.current_state = RobotState.RETURNING_HOME
        elif self.current_state == RobotState.RETURNING_HOME and sensor_data.get('at_home', False):
            self.current_state = RobotState.IDLE

    def get_action(self):
        """Get action based on current state"""
        if self.current_state == RobotState.IDLE:
            return self.idle_behavior()
        elif self.current_state == RobotState.WALKING:
            return self.walking_behavior()
        elif self.current_state == RobotState.AVOIDING_OBSTACLE:
            return self.avoid_obstacle_behavior()
        elif self.current_state == RobotState.GRASPING:
            return self.grasping_behavior()
        elif self.current_state == RobotState.RETURNING_HOME:
            return self.return_home_behavior()

    def idle_behavior(self):
        return {'action': 'wait', 'target': None}

    def walking_behavior(self):
        return {'action': 'move', 'target': self.target_position or (1, 1)}

    def avoid_obstacle_behavior(self):
        return {'action': 'move', 'target': (random.uniform(-1, 1), random.uniform(-1, 1))}

    def grasping_behavior(self):
        return {'action': 'grasp', 'target': 'object'}

    def return_home_behavior(self):
        return {'action': 'move', 'target': (0, 0)}

class BehaviorNode(ABC):
    """Base class for behavior tree nodes"""

    class Status(Enum):
        SUCCESS = "success"
        FAILURE = "failure"
        RUNNING = "running"

    def __init__(self, name):
        self.name = name
        self.status = None

    @abstractmethod
    def tick(self, blackboard):
        """Execute the behavior and return status"""
        pass

class SequenceNode(BehaviorNode):
    """Sequence node - executes children in order until one fails"""
    def __init__(self, name, children):
        super().__init__(name)
        self.children = children
        self.current_child_idx = 0

    def tick(self, blackboard):
        while self.current_child_idx < len(self.children):
            child_status = self.children[self.current_child_idx].tick(blackboard)

            if child_status == self.Status.FAILURE:
                self.current_child_idx = 0  # Reset for next time
                return self.Status.FAILURE
            elif child_status == self.Status.RUNNING:
                return self.Status.RUNNING
            elif child_status == self.Status.SUCCESS:
                self.current_child_idx += 1

        # All children succeeded
        self.current_child_idx = 0  # Reset for next time
        return self.Status.SUCCESS

class SelectorNode(BehaviorNode):
    """Selector node - executes children in order until one succeeds"""
    def __init__(self, name, children):
        super().__init__(name)
        self.children = children
        self.current_child_idx = 0

    def tick(self, blackboard):
        while self.current_child_idx < len(self.children):
            child_status = self.children[self.current_child_idx].tick(blackboard)

            if child_status == self.Status.SUCCESS:
                self.current_child_idx = 0  # Reset for next time
                return self.Status.SUCCESS
            elif child_status == self.Status.RUNNING:
                return self.Status.RUNNING
            elif child_status == self.Status.FAILURE:
                self.current_child_idx += 1

        # All children failed
        self.current_child_idx = 0  # Reset for next time
        return self.Status.FAILURE

class ActionNode(BehaviorNode):
    """Action node - performs a specific action"""
    def __init__(self, name, action_func):
        super().__init__(name)
        self.action_func = action_func

    def tick(self, blackboard):
        return self.action_func(blackboard)

class ConditionNode(BehaviorNode):
    """Condition node - checks a condition"""
    def __init__(self, name, condition_func):
        super().__init__(name)
        self.condition_func = condition_func

    def tick(self, blackboard):
        if self.condition_func(blackboard):
            return self.Status.SUCCESS
        else:
            return self.Status.FAILURE

class Blackboard:
    """Shared memory for behavior tree"""
    def __init__(self):
        self.data = {}

    def set(self, key, value):
        self.data[key] = value

    def get(self, key, default=None):
        return self.data.get(key, default)

class BehaviorTreePlanner:
    def __init__(self):
        self.blackboard = Blackboard()
        self.setup_behavior_tree()

    def setup_behavior_tree(self):
        """Setup the behavior tree for a pick-and-place task"""
        # Conditions
        check_battery = ConditionNode("CheckBattery",
                                    lambda bb: bb.get("battery_level", 100) > 20)
        check_object_detected = ConditionNode("CheckObjectDetected",
                                            lambda bb: bb.get("object_detected", False))
        check_object_reachable = ConditionNode("CheckObjectReachable",
                                             lambda bb: bb.get("object_reachable", False))
        check_object_grasped = ConditionNode("CheckObjectGrasped",
                                           lambda bb: bb.get("object_grasped", False))
        check_home_reached = ConditionNode("CheckHomeReached",
                                         lambda bb: bb.get("at_home", False))

        # Actions
        move_to_object = ActionNode("MoveToObject",
                                  lambda bb: self.move_to_object_action(bb))
        grasp_object = ActionNode("GraspObject",
                                lambda bb: self.grasp_object_action(bb))
        move_to_home = ActionNode("MoveToHome",
                                lambda bb: self.move_to_home_action(bb))
        release_object = ActionNode("ReleaseObject",
                                  lambda bb: self.release_object_action(bb))

        # Sequences
        approach_and_grasp = SequenceNode("ApproachAndGrasp", [
            check_object_detected,
            check_object_reachable,
            move_to_object,
            grasp_object
        ])

        return_and_release = SequenceNode("ReturnAndRelease", [
            check_object_grasped,
            move_to_home,
            release_object
        ])

        # Main selector (root)
        self.root = SelectorNode("MainBehavior", [
            check_battery,
            SequenceNode("PickAndPlace", [
                approach_and_grasp,
                return_and_release
            ])
        ])

    def move_to_object_action(self, blackboard):
        """Move to detected object"""
        print("Moving to object...")
        # Simulate movement
        time.sleep(0.5)
        blackboard.set("at_object", True)
        return BehaviorNode.Status.SUCCESS

    def grasp_object_action(self, blackboard):
        """Grasp the object"""
        print("Grasping object...")
        # Simulate grasping
        time.sleep(0.3)
        blackboard.set("object_grasped", True)
        return BehaviorNode.Status.SUCCESS

    def move_to_home_action(self, blackboard):
        """Move to home position"""
        print("Moving to home position...")
        # Simulate movement
        time.sleep(0.5)
        blackboard.set("at_home", True)
        return BehaviorNode.Status.SUCCESS

    def release_object_action(self, blackboard):
        """Release the object"""
        print("Releasing object...")
        # Simulate release
        time.sleep(0.2)
        blackboard.set("object_grasped", False)
        return BehaviorNode.Status.SUCCESS

    def update(self):
        """Update the behavior tree"""
        return self.root.tick(self.blackboard)

def simulate_sensor_data():
    """Simulate sensor data for the robot"""
    return {
        'obstacle': random.random() < 0.2,  # 20% chance of obstacle
        'object_grasped': random.random() < 0.7,  # 70% chance of object grasped
        'at_home': random.random() < 0.1,  # 10% chance at home
    }

def main():
    print("Demonstrating Behavioral Control Systems")
    print("=" * 50)

    # Demonstrate FSM
    print("\n1. Finite State Machine Example:")
    fsm = FiniteStateMachine()

    for step in range(10):
        sensor_data = simulate_sensor_data()
        fsm.update(sensor_data)
        action = fsm.get_action()
        print(f"Step {step}: State={fsm.current_state.value}, Action={action['action']}")

    print("\n" + "=" * 50)

    # Demonstrate Behavior Tree
    print("\n2. Behavior Tree Example:")
    bt_planner = BehaviorTreePlanner()

    # Simulate the robot's task execution
    bt_planner.blackboard.set("battery_level", 80)
    bt_planner.blackboard.set("object_detected", True)
    bt_planner.blackboard.set("object_reachable", True)

    for step in range(15):
        status = bt_planner.update()
        print(f"Step {step}: Behavior tree status = {status.value}")

        # Update some conditions to simulate task progress
        if step == 3:
            bt_planner.blackboard.set("object_grasped", True)
        if step == 7:
            bt_planner.blackboard.set("at_home", True)

        time.sleep(0.1)  # Small delay to simulate real-time execution

    print("\nBehavioral control demonstration complete!")

if __name__ == "__main__":
    main()