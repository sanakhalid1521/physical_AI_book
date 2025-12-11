"""
Example: Learning-Based Control
This code demonstrates learning-based control algorithms for humanoid robots,
including Q-learning and imitation learning approaches.
"""

import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict

class QLearningAgent:
    """Q-Learning agent for discrete state-action spaces"""
    def __init__(self, n_states, n_actions, learning_rate=0.1, discount_factor=0.95, epsilon=0.1):
        self.n_states = n_states
        self.n_actions = n_actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.epsilon = epsilon

        # Initialize Q-table
        self.q_table = np.zeros((n_states, n_actions))

    def get_action(self, state):
        """Choose action using epsilon-greedy policy"""
        if random.random() < self.epsilon:
            # Explore: random action
            return random.randint(0, self.n_actions - 1)
        else:
            # Exploit: best known action
            return np.argmax(self.q_table[state])

    def update(self, state, action, reward, next_state):
        """Update Q-value using Q-learning formula"""
        best_next_action = np.argmax(self.q_table[next_state])
        td_target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        td_error = td_target - self.q_table[state][action]
        self.q_table[state][action] += self.learning_rate * td_error

class SimpleEnvironment:
    """Simple grid world environment for humanoid navigation"""
    def __init__(self, width=5, height=5):
        self.width = width
        self.height = height
        self.state_size = width * height
        self.action_size = 4  # up, right, down, left

        # Define special positions
        self.start_pos = (0, 0)
        self.goal_pos = (width-1, height-1)
        self.obstacle_pos = [(1, 1), (2, 2), (3, 1)]  # Some obstacles

        self.reset()

    def reset(self):
        """Reset environment to initial state"""
        self.agent_pos = self.start_pos
        return self._get_state()

    def _get_state(self):
        """Convert position to state index"""
        x, y = self.agent_pos
        return y * self.width + x

    def _is_valid_position(self, pos):
        """Check if position is valid (within bounds and not obstacle)"""
        x, y = pos
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        if pos in self.obstacle_pos:
            return False
        return True

    def step(self, action):
        """Take action and return (next_state, reward, done)"""
        x, y = self.agent_pos

        # Calculate new position based on action
        if action == 0:  # up
            new_pos = (x, y - 1)
        elif action == 1:  # right
            new_pos = (x + 1, y)
        elif action == 2:  # down
            new_pos = (x, y + 1)
        elif action == 3:  # left
            new_pos = (x - 1, y)
        else:
            new_pos = (x, y)  # invalid action

        # Check if new position is valid
        if self._is_valid_position(new_pos):
            self.agent_pos = new_pos

        # Calculate reward and check if done
        if self.agent_pos == self.goal_pos:
            reward = 100  # Reached goal
            done = True
        elif self.agent_pos in self.obstacle_pos:
            reward = -10  # Hit obstacle
            done = False
        else:
            reward = -1  # Time penalty
            done = False

        next_state = self._get_state()
        return next_state, reward, done

class ImitationLearningAgent:
    """Simple imitation learning agent that learns from expert demonstrations"""
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size

        # Simple tabular approach for imitation learning
        self.policy = defaultdict(lambda: np.zeros(action_size))
        self.visit_counts = defaultdict(int)

    def observe_expert(self, state, action):
        """Learn from expert demonstration"""
        self.visit_counts[state] += 1
        self.policy[state][action] += 1

    def get_action(self, state):
        """Get action based on learned policy"""
        if state in self.policy:
            # Choose action based on frequency in demonstrations
            action_probs = self.policy[state] / np.sum(self.policy[state])
            return np.random.choice(self.action_size, p=action_probs)
        else:
            # If state not seen, choose randomly
            return random.randint(0, self.action_size - 1)

def generate_expert_demonstration(env):
    """Generate expert demonstration for imitation learning"""
    # This is a simple "expert" that knows how to reach the goal
    # In practice, this would come from a human demonstrator or optimal planner
    expert_path = [
        (0, 1), (0, 2), (0, 3),  # Go down
        (1, 3), (2, 3),          # Go right (avoid obstacle at 2,2)
        (3, 3), (4, 3), (4, 4)   # Continue to goal
    ]

    demonstrations = []
    for pos in expert_path:
        # Convert position to state
        state = pos[1] * env.width + pos[0]
        # Determine action needed to move to next position
        if pos == (0, 1):
            action = 2  # down from start
        elif pos == (0, 2):
            action = 2  # down
        elif pos == (0, 3):
            action = 1  # right
        elif pos == (1, 3):
            action = 1  # right
        elif pos == (2, 3):
            action = 1  # right
        elif pos == (3, 3):
            action = 1  # right
        elif pos == (4, 3):
            action = 2  # down
        elif pos == (4, 4):
            action = 2  # down (or could be any action, we're at goal)

        demonstrations.append((state, action))

    return demonstrations

def train_q_learning_agent():
    """Train Q-learning agent"""
    env = SimpleEnvironment()
    agent = QLearningAgent(env.state_size, env.action_size)

    episodes = 1000
    rewards = []

    for episode in range(episodes):
        state = env.reset()
        total_reward = 0
        done = False

        while not done:
            action = agent.get_action(state)
            next_state, reward, done = env.step(action)
            agent.update(state, action, reward, next_state)
            state = next_state
            total_reward += reward

        rewards.append(total_reward)

        # Decay exploration rate
        if agent.epsilon > 0.01:
            agent.epsilon *= 0.995

    return agent, rewards

def train_imitation_learning_agent():
    """Train imitation learning agent"""
    env = SimpleEnvironment()
    agent = ImitationLearningAgent(env.state_size, env.action_size)

    # Get expert demonstrations
    demonstrations = generate_expert_demonstration(env)

    # Learn from demonstrations
    for state, action in demonstrations:
        agent.observe_expert(state, action)

    return agent

def evaluate_agent(env, agent, num_episodes=10):
    """Evaluate agent performance"""
    success_count = 0
    avg_reward = 0

    for episode in range(num_episodes):
        state = env.reset()
        total_reward = 0
        done = False
        steps = 0
        max_steps = 50  # Prevent infinite loops

        while not done and steps < max_steps:
            if hasattr(agent, 'get_action'):
                action = agent.get_action(state)
            else:
                action = random.randint(0, env.action_size - 1)  # Random for comparison

            state, reward, done = env.step(action)
            total_reward += reward
            steps += 1

        avg_reward += total_reward
        if done and env.agent_pos == env.goal_pos:
            success_count += 1

    avg_reward /= num_episodes
    success_rate = success_count / num_episodes

    return avg_reward, success_rate

def main():
    print("Learning-Based Control Demonstration")
    print("=" * 50)

    # Train Q-learning agent
    print("\n1. Training Q-Learning Agent...")
    q_agent, q_rewards = train_q_learning_agent()

    # Evaluate Q-learning agent
    env = SimpleEnvironment()
    q_avg_reward, q_success_rate = evaluate_agent(env, q_agent)
    print(f"Q-Learning - Average Reward: {q_avg_reward:.2f}, Success Rate: {q_success_rate:.2f}")

    # Train Imitation Learning agent
    print("\n2. Training Imitation Learning Agent...")
    il_agent = train_imitation_learning_agent()

    # Evaluate Imitation Learning agent
    env = SimpleEnvironment()
    il_avg_reward, il_success_rate = evaluate_agent(env, il_agent)
    print(f"Imitation Learning - Average Reward: {il_avg_reward:.2f}, Success Rate: {il_success_rate:.2f}")

    # Plot learning curve
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(q_rewards)
    plt.title('Q-Learning Training Curve')
    plt.xlabel('Episode')
    plt.ylabel('Total Reward')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    env = SimpleEnvironment()
    methods = ['Random', 'Q-Learning', 'Imitation']
    success_rates = [0.1, q_success_rate, il_success_rate]  # Random is roughly 10% success
    plt.bar(methods, success_rates)
    plt.title('Success Rate Comparison')
    plt.ylabel('Success Rate')
    plt.ylim(0, 1)

    plt.tight_layout()
    plt.show()

    print(f"\nLearning-based control demonstration complete!")
    print(f"Q-Learning achieved {q_success_rate*100:.1f}% success rate")
    print(f"Imitation Learning achieved {il_success_rate*100:.1f}% success rate")

if __name__ == "__main__":
    main()