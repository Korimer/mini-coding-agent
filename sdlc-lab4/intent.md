# Intent: Implement Q-Learning Agent for Vacuum World

## Objective
Implement a tabular Q-learning agent that learns to navigate a 4x4 vacuum world from (0, 3) to (3, 0). The agent will use model-free learning to discover an optimal policy without explicit reward functions beyond the environment's step returns.

## Scope
- Implement `q_learning.py` in `SUBMISSIONS/Lab 4/`
- Import and use `vacuum_world.py` from gridworld-env skill for the environment
- Train the agent over multiple episodes with epsilon-greedy exploration
- Output the learned policy grid and a greedy path from (0, 3) to (3, 0)

## Key Decisions
- Use in-place Q-table updates across episodes
- Apply small negative living reward (-0.04) to encourage shorter paths
- Set gamma=0.9 to value future rewards without ignoring distance
- Use alpha=0.1 for stable learning rate
- Start with epsilon=0.1 and optionally decay over time

## Success Criteria
- Agent reaches (3, 0) in greedy run within step cap
- Policy grid shows clear direction toward goal
- Training converges within reasonable episode count

## Dependencies
- `vacuum_world.py` from gridworld-env skill
- Standard Python libraries only
