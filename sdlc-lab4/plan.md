===== sdlc-lab4/plan.md =====
# Plan: Q-Learning Implementation

## Approach
Implement tabular Q-learning in a single module (q_learning.py) that imports
the environment from q_env.py. A dict-based Q-table keyed by (state, action)
is defined once at module level and mutated in place by train(). Missing keys
read as 0.0, which satisfies the "all values start at 0" requirement without
pre-populating the table.

## Components
1. Environment (q_env.py): 4x4 grid, wall at (1, 2), trap at (1, 0) with
   value -1, recharge at (3, 0) with value 10. Provides ACTIONS, START,
   step(), is_terminal(), gridValues(), print_policy(), print_path().
2. Agent (q_learning.py): hyperparameters, Q-table, train(), best_action(),
   main().

## Design decisions
- Epsilon-greedy with fixed EPSILON = 0.1 (decay left optional per Intent).
- Random tie-breaking among max-Q actions, both in training and in
  best_action(), so untrained states do not bias toward the first action.
- Terminal check on next_state before bootstrapping, so terminal targets
  are just r (S3, T4).
- Bumping into a wall or boundary returns (state, LIVING_REWARD, False);
  the agent learns to avoid these through the living penalty.
- Environment reward = tile value + LIVING_REWARD, so the agent never needs
  its own reward function.

## Mapping to spec
- S1, S5 -> train() + main() greedy run
- S2 -> module-level Q = {}, in-place updates
- S3 -> update line inside train()
- S4 -> epsilon-greedy branch inside train()
- T1-T4 -> see verification.md

## Risks
- Fixed epsilon and alpha may leave unvisited states with arbitrary policy
  arrows (cosmetic only; not on the greedy path).
- A stale Q-table if train() is called twice in one process. Mitigation:
  call Q.clear() first if re-running.
- Spec S5 says the final greedy run is capped at 50 steps, but main() reuses
  MAX_STEPS (200). Resolve in tasks (T6).

## Out of scope
Decaying epsilon, SARSA, function approximation, visualization.
