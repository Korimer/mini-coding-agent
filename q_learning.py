from typing import Dict, Tuple, List
import random

# Hyperparameters
LIVING_REWARD = -0.04
GAMMA = 0.9
ALPHA = 0.1
EPSILON = 0.1
EPISODES = 1000
MAX_STEPS = 200

from q_env import ACTIONS, START, gridValues, is_terminal, step, print_policy, print_path

# Q-table: defaultdict(float) keyed by (state, action), all start at 0
Q: Dict[Tuple[Tuple[int, int], Tuple[int, int]], float] = {}


def train() -> None:
    """Train the agent using epsilon-greedy Q-learning."""
    for episode in range(EPISODES):
        state = START
        done = False
        steps = 0
        
        while not done and steps < MAX_STEPS:
            # Epsilon-greedy action selection
            if random.random() < EPSILON:
                action = random.choice(ACTIONS)
            else:
                # Best action (break ties randomly)
                q_values = [Q.get((state, a), 0.0) for a in ACTIONS]
                max_q = max(q_values)
                best_actions = [a for a in ACTIONS if Q.get((state, a), 0.0) == max_q]
                action = random.choice(best_actions)
            
            # Take the step
            next_state, reward, done = step(state, action)
            
            # Update Q-value
            if is_terminal(next_state):
                target = reward
            else:
                target = reward + GAMMA * max(Q.get((next_state, a), 0.0) for a in ACTIONS)
            
            current_q = Q.get((state, action), 0.0)
            Q[(state, action)] = current_q + ALPHA * (target - current_q)
            
            state = next_state
            steps += 1


def best_action(state: Tuple[int, int]) -> Tuple[int, int]:
    """Return the greedy action for a given state."""
    q_values = [Q.get((state, a), 0.0) for a in ACTIONS]
    max_q = max(q_values)
    return random.choice([a for a in ACTIONS if Q.get((state, a), 0.0) == max_q])


def main() -> None:
    # Train the agent
    train()
    
    # Print learned policy
    print("Learned Policy:")
    print_policy(best_action)
    
    # Run greedy path with epsilon = 0
    state = START
    path = [state]
    done = False
    steps = 0
    
    while not done and steps < MAX_STEPS:
        action = best_action(state)
        next_state, reward, done = step(state, action)
        path.append(next_state)
        state = next_state
        steps += 1
    
    print("\nGreedy Path:")
    print_path(path)
    
    # Check if reached target
    reached = (3, 0) in path
    moves = len(path) - 1
    print(f"\nReached recharge: {reached}, Moves: {moves}")


if __name__ == "__main__":
    main()
