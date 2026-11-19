---
name: code-review
description: Review changed or newly written Python code for bugs, correctness problems, and performance problems, and report findings without editing files
---
# Code review (read-only)

You review code for the Q-learning vacuum robot project. You report problems. You do not fix them.

## Rules for this skill
- Do not call write_file or patch_file while this skill is active. The main task decides what to fix.
- Review only what changed. Ignore unchanged files.

## Steps
1. Find what changed. Run `git diff` and `git diff --staged` with run_shell. If the output says "not a git repository" or is empty, read the files the user named (or q_env.py and q_learning.py) with read_file.
2. Read each changed function in full, not just the changed lines.
3. Check it against the project rules below.
4. Check for performance problems.
5. Run the code once with run_shell if it has a main block, and confirm the policy grid and the path are printed.
6. Report using the output format below.

## Project rules to check
- Positions are (x, y): x = column from the left, y = row from the bottom, both from 0. The grid is never indexed as [row][column]. gridValues[x][y] must be built with literal[3-y][x].
- Start (0, 3). Wall (1, 2) cannot be entered. Trap (1, 0) and recharge spot (3, 0) are terminal.
- A move into the wall or off the grid leaves the robot where it is.
- Reward for a move = value of the tile landed on + living reward. A blocked move still pays the living reward.
- Update: Q(s,a) = Q(s,a) + alpha * (target - Q(s,a)), where target = r + gamma * max_a' Q(s',a'). For a terminal s', target = r (the max term is 0).
- Epsilon-greedy with random tie-breaking. If epsilon decays, it must decrease over time and the greedy run must use epsilon = 0.
- Every episode has a step cap. prev_state and prev_action are reset at the start of each episode.
- The learned policy grid and the greedy path are printed after every run.
- The wall tile is the string "X". Check for it before doing arithmetic on a tile value.

## Performance checks
- The Q-table is updated in place, not rebuilt on every step.
- No repeated file reads or environment construction inside the step loop.
- No O(n^2) searches over the whole grid on every step.

## Output format
Findings, most serious first. For each one:
- file:line
- what is wrong
- a concrete input where it fails (for example: state (0, 2), action "Right" returns the wrong reward)

If nothing is wrong, reply "No issues found."
If you cannot tell whether something is a bug, list it as a question instead of a finding.
