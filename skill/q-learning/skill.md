---
name: q-learning
description: Implement tabular Q-learning with a Q-table, update rule, epsilon-greedy exploration, discount factor, learning rate, epsilon, episodes, training loop, and greedy policy
---
# Tabular Q-learning (model-free)

Deliverable: q_learning.py. It imports the environment from q_env.py. If q_env.py does not exist yet, call use_skill with gridworld-env first.

## Algorithm
- The agent never uses T or R directly. It only sees what step() returns.
- Q is a defaultdict(float) keyed by (state, action). All values start at 0.
- After each move from s with action a to s' with reward r:
  - if s' is terminal: target = r
  - otherwise: target = r + GAMMA * max over a' of Q[(s', a')]
  - Q[(s, a)] += ALPHA * (target - Q[(s, a)])
- Epsilon-greedy: with probability EPSILON pick a random action, otherwise the best action. Break ties randomly.
- An episode starts at (0, 3) and ends at a terminal tile or at the step cap. Q carries over between episodes.

## Hyperparameters (variables at the top of the file)
- LIVING_REWARD = -0.04, GAMMA = 0.9, ALPHA = 0.1, EPSILON = 0.1
- EPISODES = 1000, MAX_STEPS = 200 for training, 50 for the final greedy run.
- Epsilon may optionally decay (for example 1.0 down to 0.05). If so, say so in the summary.
- Why these values: a small negative living reward pushes the robot toward short paths, gamma 0.9 values the +10 tile without ignoring distance, alpha 0.1 keeps updates stable, epsilon 0.1 keeps some exploration.

## Steps
1. Confirm q_env.py exists with list_files. If not, call use_skill with gridworld-env.
2. Write q_learning.py with write_file: a train() function, a best_action(state) function, and a main block. Update the Q-table in place. Do not rebuild it each step.
3. Run it with run_shell: python q_learning.py
4. Output must include:
   - the learned policy grid (use print_policy from q_env.py)
   - the greedy path from (0, 3) with epsilon = 0, printed with print_path
5. Finish with a short summary: hyperparameters used, whether the path reaches (3, 0), and how many moves it took.

## Pitfalls
- Reset prev_state and prev_action at the start of every episode.
- Terminal states have no future value, so use target = r, not r + gamma * max Q.
- A greedy run can loop when Q-values are tied. Always cap it with a step limit.
- If the path does not reach (3, 0), raise EPISODES or add epsilon decay and run again.
