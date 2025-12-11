"""
Example: Planning and Reasoning
This code demonstrates automated planning and logical reasoning systems
for humanoid robot decision-making.
"""

import heapq
from collections import defaultdict, deque
import random

class Proposition:
    """A simple proposition for logical reasoning"""
    def __init__(self, name, params=None):
        self.name = name
        self.params = params or []

    def __str__(self):
        if self.params:
            return f"{self.name}({', '.join(map(str, self.params))})"
        return self.name

    def __eq__(self, other):
        return self.name == other.name and self.params == other.params

    def __hash__(self):
        return hash((self.name, tuple(self.params)))

class Action:
    """An action with preconditions and effects"""
    def __init__(self, name, preconditions, effects, cost=1):
        self.name = name
        self.preconditions = set(preconditions)
        self.effects = set(effects)  # Positive effects
        self.cost = cost

    def applicable(self, state):
        """Check if action is applicable in given state"""
        return self.preconditions.issubset(state)

    def apply(self, state):
        """Apply action to state and return new state"""
        new_state = state.copy()
        # Remove negative effects (not explicitly modeled here)
        # Add positive effects
        new_state.update(self.effects)
        return new_state

class ForwardPlanner:
    """Forward state-space planner"""
    def __init__(self, actions):
        self.actions = actions

    def plan(self, initial_state, goal_state):
        """Plan using forward search (Dijkstra's algorithm)"""
        # Priority queue: (cost, state, path)
        queue = [(0, frozenset(initial_state), [])]
        visited = set()
        visited.add(frozenset(initial_state))

        while queue:
            cost, current_state, path = heapq.heappop(queue)

            # Check if goal is achieved
            if goal_state.issubset(current_state):
                return path

            # Try all applicable actions
            for action in self.actions:
                if action.applicable(current_state):
                    new_state = action.apply(current_state)
                    new_state_frozen = frozenset(new_state)

                    if new_state_frozen not in visited:
                        visited.add(new_state_frozen)
                        new_cost = cost + action.cost
                        new_path = path + [action]
                        heapq.heappush(queue, (new_cost, new_state_frozen, new_path))

        return None  # No plan found

class KnowledgeBase:
    """Simple knowledge base for logical reasoning"""
    def __init__(self):
        self.facts = set()
        self.rules = []  # Forward-chaining rules

    def add_fact(self, fact):
        """Add a fact to the knowledge base"""
        self.facts.add(fact)

    def add_rule(self, conditions, conclusion):
        """Add a rule: if conditions then conclusion"""
        self.rules.append((conditions, conclusion))

    def forward_chain(self):
        """Apply forward chaining to derive new facts"""
        new_facts = True
        while new_facts:
            new_facts = False
            for conditions, conclusion in self.rules:
                if all(cond in self.facts for cond in conditions) and conclusion not in self.facts:
                    self.facts.add(conclusion)
                    new_facts = True

    def query(self, fact):
        """Check if fact is known"""
        return fact in self.facts

class TaskPlanner:
    """High-level task planner for humanoid robots"""
    def __init__(self):
        self.knowledge_base = KnowledgeBase()
        self.setup_domain_knowledge()

    def setup_domain_knowledge(self):
        """Setup domain-specific knowledge and rules"""
        # Define some rules for humanoid tasks
        self.knowledge_base.add_rule(
            [Proposition("robot_at", ["location_A"]), Proposition("object_at", ["object_X", "location_A"])],
            Proposition("can_grasp", ["object_X"])
        )

        self.knowledge_base.add_rule(
            [Proposition("holding", ["object_X"]), Proposition("robot_at", ["location_B"])],
            Proposition("object_at", ["object_X", "location_B"])
        )

        self.knowledge_base.add_rule(
            [Proposition("door_closed", ["door_1"])],
            Proposition("path_blocked", ["door_1"])
        )

        self.knowledge_base.add_rule(
            [Proposition("door_open", ["door_1"])],
            Proposition("path_clear", ["door_1"])
        )

    def create_actions(self):
        """Create domain-specific actions"""
        actions = [
            Action("move_to",
                   [Proposition("at_door", ["D"])],  # Need to be at door to open it
                   [Proposition("door_open", ["D"]), Proposition("door_closed", ["D"])],  # Effect: door becomes open, was closed
                   cost=2),

            Action("grasp_object",
                   [Proposition("robot_at", ["L"]), Proposition("object_at", ["O", "L"]), Proposition("arm_free")],
                   [Proposition("holding", ["O"]), Proposition("not_arm_free")],
                   cost=1),

            Action("move_object",
                   [Proposition("holding", ["O"]), Proposition("robot_at", ["L1"])],
                   [Proposition("object_at", ["O", "L2"]), Proposition("robot_at", ["L2"])],
                   cost=5),

            Action("navigate",
                   [Proposition("path_clear", ["P"])],
                   [Proposition("robot_at", ["destination"]), Proposition("at_door", ["D"])],
                   cost=3)
        ]

        # Create specific instances of actions
        specific_actions = []
        locations = ["kitchen", "living_room", "bedroom", "hallway"]
        objects = ["cup", "book", "ball"]
        doors = ["door_kl", "door_lb", "door_bh"]  # kitchen-living, living-bedroom, bedroom-hallway

        for loc in locations:
            for obj in objects:
                specific_actions.append(
                    Action(f"grasp_{obj}_at_{loc}",
                           [Proposition("robot_at", [loc]), Proposition("object_at", [obj, loc]), Proposition("arm_free")],
                           [Proposition("holding", [obj]), Proposition("robot_at", [loc])],
                           cost=1)
                )

            for dest in locations:
                if loc != dest:
                    specific_actions.append(
                        Action(f"move_from_{loc}_to_{dest}",
                               [Proposition("robot_at", [loc])],
                               [Proposition("robot_at", [dest])],
                               cost=3)
                    )

        for door in doors:
            specific_actions.append(
                Action(f"open_{door}",
                       [Proposition("robot_at", [door.split('_')[1]]), Proposition("door_closed", [door])],  # Simplified
                       [Proposition("door_open", [door])],
                       cost=2)
            )

        return specific_actions + actions

def simulate_robot_environment():
    """Simulate a robot environment with initial conditions"""
    initial_state = {
        Proposition("robot_at", ["kitchen"]),
        Proposition("object_at", ["cup", "kitchen"]),
        Proposition("object_at", ["book", "living_room"]),
        Proposition("door_closed", ["door_kl"]),
        Proposition("arm_free"),
        Proposition("battery_level", ["high"])
    }

    goal_state = {
        Proposition("object_at", ["cup", "bedroom"]),
        Proposition("robot_at", ["bedroom"])
    }

    return initial_state, goal_state

def main():
    print("Planning and Reasoning Demonstration")
    print("=" * 50)

    # Create planner and problem
    task_planner = TaskPlanner()
    actions = task_planner.create_actions()
    initial_state, goal_state = simulate_robot_environment()

    print(f"Initial state: {[str(p) for p in list(initial_state)[:5]]}...")  # Show first 5 facts
    print(f"Goal state: {[str(p) for p in goal_state]}")

    # Plan using forward search
    planner = ForwardPlanner(actions)
    plan = planner.plan(initial_state, goal_state)

    if plan:
        print(f"\nPlan found with {len(plan)} actions:")
        for i, action in enumerate(plan):
            print(f"  {i+1}. {action.name}")

        # Execute plan and update knowledge base
        current_state = initial_state.copy()
        for action in plan:
            current_state = action.apply(current_state)
            # Add resulting facts to knowledge base
            for fact in current_state:
                task_planner.knowledge_base.add_fact(fact)

        # Perform reasoning after plan execution
        task_planner.knowledge_base.forward_chain()

        print(f"\nAfter plan execution:")
        print(f"  Robot successfully moved cup to bedroom: {task_planner.knowledge_base.query(Proposition('object_at', ['cup', 'bedroom']))}")
        print(f"  Robot is in bedroom: {task_planner.knowledge_base.query(Proposition('robot_at', ['bedroom']))}")

    else:
        print("\nNo plan found!")

    # Demonstrate logical reasoning capabilities
    print(f"\nLogical Reasoning Capabilities:")
    kb = task_planner.knowledge_base

    # Add some facts and demonstrate inference
    kb.add_fact(Proposition("robot_at", ["location_A"]))
    kb.add_fact(Proposition("object_at", ["object_X", "location_A"]))
    kb.forward_chain()

    can_grasp = kb.query(Proposition("can_grasp", ["object_X"]))
    print(f"  Can robot grasp object_X at location_A? {can_grasp}")

    print(f"\nPlanning and reasoning demonstration complete!")

if __name__ == "__main__":
    main()