"""
Example: Autonomous Learning and Adaptation
This code demonstrates systems that enable humanoid robots to learn and adapt
autonomously in changing environments.
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import deque
import random
from abc import ABC, abstractmethod

class ExperienceReplayBuffer:
    """Replay buffer for storing and sampling experiences"""
    def __init__(self, capacity=10000):
        self.buffer = deque(maxlen=capacity)

    def push(self, state, action, reward, next_state, done):
        """Add experience to buffer"""
        self.buffer.append((state, action, reward, next_state, done))

    def sample(self, batch_size):
        """Sample random batch from buffer"""
        batch = random.sample(self.buffer, min(len(self.buffer), batch_size))
        states, actions, rewards, next_states, dones = map(np.stack, zip(*batch))
        return states, actions, rewards, next_states, dones

    def __len__(self):
        return len(self.buffer)

class OnlineLearner(ABC):
    """Abstract base class for online learning algorithms"""
    def __init__(self, learning_rate=0.01):
        self.learning_rate = learning_rate

    @abstractmethod
    def update(self, state, action, reward, next_state, done):
        """Update the learning model with new experience"""
        pass

    @abstractmethod
    def predict(self, state):
        """Predict value or action for given state"""
        pass

class LinearFunctionApproximator(OnlineLearner):
    """Simple linear function approximator for learning"""
    def __init__(self, state_size, action_size, learning_rate=0.01):
        super().__init__(learning_rate)
        self.state_size = state_size
        self.action_size = action_size
        # Initialize weights for each action
        self.weights = np.random.randn(action_size, state_size + 1) * 0.01  # +1 for bias

    def predict(self, state):
        """Predict Q-values for all actions"""
        # Add bias term
        state_with_bias = np.append(state, 1)
        return np.dot(self.weights, state_with_bias)

    def update(self, state, action, reward, next_state, done):
        """Update weights using temporal difference learning"""
        # Get current Q-value
        state_with_bias = np.append(state, 1)
        current_q = np.dot(self.weights[action], state_with_bias)

        # Get target Q-value
        if done:
            target_q = reward
        else:
            next_state_with_bias = np.append(next_state, 1)
            next_q_values = np.dot(self.weights, next_state_with_bias)
            target_q = reward + 0.95 * np.max(next_q_values)  # Using gamma=0.95

        # Calculate temporal difference error
        td_error = target_q - current_q

        # Update weights
        self.weights[action] += self.learning_rate * td_error * state_with_bias

class AdaptiveLearningSystem:
    """System for adaptive learning and continuous improvement"""
    def __init__(self, state_size, action_size):
        self.learner = LinearFunctionApproximator(state_size, action_size)
        self.replay_buffer = ExperienceReplayBuffer(capacity=5000)
        self.performance_history = deque(maxlen=100)
        self.adaptation_threshold = 0.1  # Threshold for triggering adaptation

    def learn_from_experience(self, state, action, reward, next_state, done):
        """Learn from a single experience"""
        # Store experience in replay buffer
        self.replay_buffer.push(state, action, reward, next_state, done)

        # Update with current experience
        self.learner.update(state, action, reward, next_state, done)

        # Sample from replay buffer for additional learning
        if len(self.replay_buffer) > 32:
            batch_states, batch_actions, batch_rewards, batch_next_states, batch_dones = \
                self.replay_buffer.sample(32)

            for i in range(len(batch_states)):
                self.learner.update(
                    batch_states[i], batch_actions[i], batch_rewards[i],
                    batch_next_states[i], batch_dones[i]
                )

    def evaluate_performance(self, current_performance):
        """Evaluate if performance is degrading and adaptation is needed"""
        self.performance_history.append(current_performance)

        if len(self.performance_history) >= 10:
            recent_avg = np.mean(list(self.performance_history)[-5:])
            earlier_avg = np.mean(list(self.performance_history)[:5])

            # If performance is significantly worse, trigger adaptation
            if earlier_avg - recent_avg > self.adaptation_threshold:
                return True

        return False

    def adapt_learning_parameters(self):
        """Adapt learning parameters based on performance"""
        # Increase learning rate when performance is degrading
        self.learner.learning_rate = min(self.learner.learning_rate * 1.1, 0.1)
        print(f"Adapted learning rate to {self.learner.learning_rate:.4f}")

class SelfAssessmentModule:
    """Module for self-monitoring and self-evaluation"""
    def __init__(self):
        self.task_success_rates = {}
        self.error_patterns = []
        self.confidence_scores = {}

    def record_task_outcome(self, task_name, success, confidence=0.5):
        """Record the outcome of a task"""
        if task_name not in self.task_success_rates:
            self.task_success_rates[task_name] = []

        self.task_success_rates[task_name].append(success)
        self.confidence_scores[task_name] = confidence

    def analyze_performance(self, task_name):
        """Analyze performance on a specific task"""
        if task_name not in self.task_success_rates:
            return None

        outcomes = self.task_success_rates[task_name]
        success_rate = np.mean(outcomes) if outcomes else 0
        recent_performance = np.mean(outcomes[-5:]) if len(outcomes) >= 5 else success_rate

        return {
            'overall_success_rate': success_rate,
            'recent_success_rate': recent_performance,
            'total_attempts': len(outcomes),
            'confidence': self.confidence_scores.get(task_name, 0.5)
        }

    def identify_improvement_areas(self):
        """Identify areas for improvement based on performance"""
        improvement_areas = []

        for task_name, outcomes in self.task_success_rates.items():
            if len(outcomes) >= 5:  # Need enough data
                recent_performance = np.mean(outcomes[-5:])
                overall_performance = np.mean(outcomes)

                if recent_performance < 0.7:  # Below threshold
                    improvement_areas.append({
                        'task': task_name,
                        'recent_performance': recent_performance,
                        'suggestion': 'Focus more practice on this task'
                    })

        return improvement_areas

class AutonomousLearningAgent:
    """Main agent that combines all autonomous learning components"""
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.adaptive_system = AdaptiveLearningSystem(state_size, action_size)
        self.self_assessment = SelfAssessmentModule()
        self.task_history = []
        self.exploration_rate = 0.3

    def select_action(self, state):
        """Select action using epsilon-greedy policy"""
        if random.random() < self.exploration_rate:
            return random.randint(0, self.action_size - 1)
        else:
            q_values = self.adaptive_system.learner.predict(state)
            return np.argmax(q_values)

    def learn_and_adapt(self, state, action, reward, next_state, done, task_name="default"):
        """Main learning and adaptation cycle"""
        # Learn from experience
        self.adaptive_system.learn_from_experience(state, action, reward, next_state, done)

        # Record task outcome for self-assessment
        success = reward > 0  # Simplified success criterion
        self.self_assessment.record_task_outcome(task_name, success)

        # Evaluate performance and adapt if necessary
        performance = self.self_assessment.analyze_performance(task_name)
        if performance and self.adaptive_system.evaluate_performance(performance['recent_success_rate']):
            self.adaptive_system.adapt_learning_parameters()

        # Reduce exploration over time
        self.exploration_rate = max(0.05, self.exploration_rate * 0.999)

    def get_improvement_suggestions(self):
        """Get suggestions for improvement based on self-assessment"""
        return self.self_assessment.identify_improvement_areas()

def simulate_changing_environment():
    """Simulate an environment that changes over time"""
    class ChangingEnvironment:
        def __init__(self):
            self.time_step = 0
            self.environment_state = "normal"

        def step(self, action):
            self.time_step += 1

            # Change environment conditions periodically
            if self.time_step % 100 == 0:
                self.environment_state = random.choice(["normal", "obstacle", "slippery"])

            # Define rewards based on environment state
            if self.environment_state == "normal":
                reward = 1 if action == 0 else 0  # Action 0 is correct in normal state
            elif self.environment_state == "obstacle":
                reward = 1 if action == 1 else 0  # Action 1 is correct when obstacle present
            else:  # slippery
                reward = 1 if action == 2 else 0  # Action 2 is correct in slippery conditions

            # Add some noise to rewards
            reward += random.gauss(0, 0.1)

            # Generate next state (simplified)
            next_state = np.array([np.sin(self.time_step * 0.1), np.cos(self.time_step * 0.1)])
            done = False

            return next_state, reward, done

    return ChangingEnvironment()

def main():
    print("Autonomous Learning and Adaptation Demonstration")
    print("=" * 60)

    # Initialize the agent
    state_size = 2
    action_size = 3
    agent = AutonomousLearningAgent(state_size, action_size)

    # Simulate learning over time
    env = simulate_changing_environment()
    current_state = np.array([0.0, 0.0])
    total_reward = 0
    episode_rewards = []

    print("\nStarting autonomous learning simulation...")

    for step in range(500):
        # Select action
        action = agent.select_action(current_state)

        # Take action in environment
        next_state, reward, done = env.step(action)

        # Learn and adapt
        agent.learn_and_adapt(current_state, action, reward, next_state, done, "navigation_task")

        # Update state and accumulate reward
        current_state = next_state
        total_reward += reward

        if step % 50 == 0:
            episode_rewards.append(total_reward)
            print(f"Step {step}: Total Reward = {total_reward:.2f}, "
                  f"Exploration Rate = {agent.exploration_rate:.3f}")

    print(f"\nLearning completed! Total reward: {total_reward:.2f}")

    # Analyze performance
    performance_analysis = agent.self_assessment.analyze_performance("navigation_task")
    if performance_analysis:
        print(f"\nPerformance Analysis:")
        print(f"  Overall Success Rate: {performance_analysis['overall_success_rate']:.2f}")
        print(f"  Recent Success Rate: {performance_analysis['recent_success_rate']:.2f}")
        print(f"  Total Attempts: {performance_analysis['total_attempts']}")

    # Get improvement suggestions
    suggestions = agent.get_improvement_suggestions()
    if suggestions:
        print(f"\nImprovement Suggestions:")
        for suggestion in suggestions:
            print(f"  - {suggestion['task']}: {suggestion['suggestion']} "
                  f"(Recent performance: {suggestion['recent_performance']:.2f})")
    else:
        print(f"\nNo improvement areas identified - performance is good!")

    # Demonstrate adaptation
    print(f"\nDemonstrating adaptation to environment changes:")
    print(f"  Learning rate adapted to: {agent.adaptive_system.learner.learning_rate:.4f}")
    print(f"  Final exploration rate: {agent.exploration_rate:.3f}")

    # Plot learning curve
    plt.figure(figsize=(12, 4))

    plt.subplot(1, 2, 1)
    plt.plot(episode_rewards)
    plt.title('Learning Curve: Total Reward Over Time')
    plt.xlabel('Episode (x50 steps)')
    plt.ylabel('Total Reward')
    plt.grid(True)

    plt.subplot(1, 2, 2)
    # Show action selection over time (simplified visualization)
    action_counts = [0, 0, 0]
    test_state = np.array([0.5, 0.5])
    for _ in range(100):
        action = agent.select_action(test_state)
        action_counts[action] += 1

    plt.bar(['Action 0', 'Action 1', 'Action 2'], action_counts)
    plt.title('Final Action Selection Distribution')
    plt.ylabel('Selection Count')

    plt.tight_layout()
    plt.show()

    print(f"\nAutonomous learning demonstration complete!")

if __name__ == "__main__":
    main()