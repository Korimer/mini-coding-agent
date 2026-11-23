# Spec: Q-Learning Implementation

## Behavior

1. **S1**: The agent learns a policy to navigate from (0, 3) to (3, 0) in the vacuum world environment.
   - Covers Intent criterion: "The agent must learn a policy that navigates from start to goal."

2. **S2**: The Q-table is initialized with all values at 0 and updated incrementally after each step.
   - Covers Intent criterion: "The agent must use tabular Q-learning with incremental updates."

3. **S3**: Updates follow the rule: `Q[(s, a)] += ALPHA * (target - Q[(s, a)])` where target is r or r + GAMMA * max(Q[s']).
   - Covers Intent criterion: "The agent must use standard Q-learning update rule with gamma discounting."

4. **S4**: Actions are selected using epsilon-greedy policy with ties broken randomly.
   - Covers Intent criterion: "The agent must balance exploration and exploitation via epsilon-greedy selection."

5. **S5**: Training runs for EPISODES episodes with MAX_STEPS limit per episode, then a final greedy run with 50 steps.
   - Covers Intent criterion: "The agent must train for multiple episodes and evaluate on a greedy policy."

## Interfaces

- **Files**: `q_learning.py` (main implementation), `q_env.py` (environment import)
- **Functions**: 
  - `train()` - runs the training loop
  - `best_action(state)` - returns best action for a state
  - `print_policy()` - prints learned policy grid
  - `print_path()` - prints greedy path from start to goal
- **Hyperparameters** (at top of q_learning.py):
  - LIVING_REWARD = -0.04, GAMMA = 0.9, ALPHA = 0.1, EPSILON = 0.1
  - EPISODES = 1000, MAX_STEPS = 200 (training), 50 (final run)

## Acceptance tests

- **T1**: After training, `print_policy()` shows a policy that moves toward (3, 0).
  - Input: Run `python q_learning.py`
  - Expected Output: Policy grid with actions directing robot to goal

- **T2**: The greedy path from (0, 3) reaches (3, 0) within 50 steps.
  - Input: Final greedy run in `main()` block
  - Expected Output: Path printed by `print_path()` ending at (3, 0)

- **T3**: Q-table values are updated in place during training (no rebuild per step).
  - Input: Inspect `q_learning.py` source
  - Expected Output: Single Q-table definition outside functions, updates inside train()

- **T4**: Terminal states use target = r, non-terminal use target = r + GAMMA * max(Q[s']).
  - Input: Read update logic in train()
  - Expected Output: Conditional check for terminal state before computing target