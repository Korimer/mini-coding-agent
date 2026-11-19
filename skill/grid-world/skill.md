---
name: gridworld-env
description: Build the 4x4 vacuum robot grid world environment with start, wall, trap, and recharge tiles, (x, y) coordinates, move offsets, step function, and path display
---
# Vacuum robot grid world environment

Deliverable: q_env.py (standard library only). It defines the world only. It does not learn anything.

## Layout
- Positions are (x, y): x = column from the left, y = row from the bottom, both from 0. Store the grid as gridValues[x][y]. Never index as [row][column].
- Literal grid, top row first (y=3 down to y=0):
  - y=3: 0 0 0 0
  - y=2: 0 X 0 0
  - y=1: 0 0 0 0
  - y=0: 0 -1 0 10
- Build gridValues from the literal with: gridValues = [[literal[3-y][x] for y in range(4)] for x in range(4)]. So gridValues[0][3] is the top left and gridValues[0][0] is the bottom left.
- Start (0, 3). Wall "X" at (1, 2), cannot be entered. Trap (1, 0) = -1. Recharge spot (3, 0) = +10. Trap and recharge spot are terminal.

## Moves
- Actions: Up (0,1), Down (0,-1), Left (-1,0), Right (1,0).
- A move into the wall or off the grid leaves the robot where it is.
- Reward for a move = value of the tile landed on + living_reward (default -0.04). A blocked move still pays the living reward.

## What q_env.py must provide
- Constants: ACTIONS, START, GRID_LITERAL, gridValues, LIVING_REWARD.
- is_terminal(state): True for (1, 0) and (3, 0).
- step(state, action): returns (next_state, reward, done).
- print_policy(best_action_fn): 4x4 grid, top row first, arrows for ordinary tiles, X for the wall, -1 and 10 for the terminals.
- print_path(path): prints each (x, y) in order, marking start and end.

## Steps
1. If a reference file such as lab4_vacuum.py exists, read it with read_file and reuse the layout.
2. Do not use the aima package, %pip or notebook magics. Write plain Python.
3. Write q_env.py with write_file.
4. Check it with run_shell: python -c "import q_env; print(q_env.step((0,3),'Down'))". Expect ((0, 2), -0.04, False).
5. If the Q-learning algorithm is needed next, call use_skill with q-learning.

## Pitfalls
- Never index the grid as [row][column].
- Build a fresh path list for each run. Do not prepend the start tile to the same list twice.
- The wall tile is the string "X". Check for it before doing arithmetic on a tile value.
