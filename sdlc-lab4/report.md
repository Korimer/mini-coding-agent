===== sdlc-lab4/report.md =====
# Report: Q-Learning Agent for Vacuum World

## Summary
Implemented a tabular Q-learning agent (q_learning.py) that learns to move
from (0, 3) to the recharge tile at (3, 0) in a 4x4 grid with one wall at
(1, 2) and one trap at (1, 0). The agent uses epsilon-greedy exploration
(EPSILON = 0.1), ALPHA = 0.1, GAMMA = 0.9, a living reward of -0.04, and
trains for 1000 episodes of up to 200 steps each.

## Outcome
- The greedy path reaches (3, 0) in 6 moves, which is the shortest possible.
- 200 of 200 random seeds succeeded within 50 steps, so the result is not a
  fluke of one lucky run.
- All four acceptance tests (T1-T4) pass; see verification.md.

## SDLC artifacts
- intent.md: goal, scope, key decisions, success criteria
- spec.md: behaviors S1-S5, interfaces, acceptance tests T1-T4
- plan.md: approach, design decisions, risks
- tasks.md: task breakdown mapped to spec items
- verification.md: test results and issues found
- report.md: this document

## What went well
- Terminal handling was simple to specify and verify: one conditional in the
  update step (T4).
- Tie-breaking randomly kept early training from always favoring the first
  action in ACTIONS.
- Environment and agent were kept in separate files, so the agent code only
  depends on step(), is_terminal(), and ACTIONS.

## What did not go as planned
- The spec says the final greedy run is capped at 50 steps, but the code
  reuses MAX_STEPS (200). The agent passes at 50, but the code and spec
  should agree (tasks T6).
- intent.md still names vacuum_world.py as the dependency, while the code
  uses q_env.py (tasks T9).
- The spec's "Covers Intent criterion" quotes do not match intent.md's
  wording, which weakens traceability.
- A code comment says defaultdict(float) but the Q-table is a plain dict.

## Limitations
- Fixed epsilon and alpha; no decay. States rarely visited can show
  arbitrary policy arrows (for example (1, 3) points left).
- Q-table persists if train() is called twice in one process.
- Single small deterministic grid; results do not say how the approach
  scales or handles stochastic transitions.

## Possible next steps
- Add epsilon decay and compare convergence speed.
- Clear Q at the start of train() or expose a reset function.
- Add a small automated test file that asserts T2 across several seeds.

## Conclusion
The implementation meets the intent and passes all acceptance tests. The
open items are documentation and spec alignment, not functional bugs.
