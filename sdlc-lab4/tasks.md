===== sdlc-lab4/tasks.md =====
# Tasks: Q-Learning Implementation

Status key: [x] done, [ ] open

- [x] T1. Define environment (q_env.py): grid, ACTIONS, START, step(),
      is_terminal(), print_policy(), print_path().
      Covers: S1

- [x] T2. Add hyperparameters at top of q_learning.py
      (LIVING_REWARD, GAMMA, ALPHA, EPSILON, EPISODES, MAX_STEPS).
      Covers: Interfaces / Hyperparameters

- [x] T3. Define module-level Q-table, initially empty (implicit 0.0).
      Covers: S2, T3

- [x] T4. Implement train(): epsilon-greedy selection with random
      tie-breaking, terminal-aware target, in-place Q update.
      Covers: S2, S3, S4, T3, T4

- [x] T5. Implement best_action(state) with random tie-breaking.
      Covers: S4, T1

- [ ] T6. Add FINAL_STEPS = 50 and use it in main()'s greedy loop in place
      of MAX_STEPS.
      Covers: S5, T2 (currently implemented with 200, spec says 50)

- [x] T7. Implement main(): train, print policy, run greedy path, print
      whether (3, 0) was reached and move count.
      Covers: S5, T1, T2

- [x] T8. Run python q_learning.py repeatedly and across seeds; record
      results in verification.md.
      Covers: T1, T2

- [ ] T9. Clean up docs: copy q_learning.py and q_env.py into
      SUBMISSIONS/Lab 4/ as named in intent.md, and decide whether q_env.py
      replaces vacuum_world.py (intent.md still names vacuum_world.py).
      Covers: Intent scope/dependencies

- [ ] T10. Fix stale comment on the Q-table in q_learning.py: it says
       "defaultdict(float)" but the code uses a plain dict with .get().
