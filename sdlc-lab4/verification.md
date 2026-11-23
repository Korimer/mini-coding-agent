===== sdlc-lab4/verification.md =====
# Verification: Q-Learning Implementation

Method: ran python q_learning.py 10 times (unseeded) and a 200-seed batch
(seeds 0-199, Q cleared and retrained each time, greedy run capped at 50
steps).

## Results

Learned policy (sample run; row y=3 at top):
    v < v v
    v X v v
    > > > v
    ^ -1 > 10

Greedy path, every run: (0, 3) -> ... -> (3, 0), 6 moves
(6 is the minimum possible, since the wall at (1, 2) and trap at (1, 0)
do not lengthen the shortest route).

Batch: 0 failures out of 200 seeds; min and max moves both 6.

## Acceptance tests

- T1 PASS. Policy arrows on the path lead toward (3, 0).
  Note: cell (1, 3) shows "<", pointing away from the goal. It is not on the
  greedy path, so behavior is unaffected, but it shows unvisited or
  under-trained states can have arbitrary arrows.
- T2 PASS. Greedy path reaches (3, 0) in 6 moves, within 50.
  Caveat: main() actually allows MAX_STEPS = 200 steps. Passing at 50 was
  confirmed separately in the 200-seed batch. See T6 in tasks.md.
- T3 PASS. Single module-level Q = {} definition; only train() mutates it.
- T4 PASS. train() checks is_terminal(next_state) and sets target = reward
  for terminals, else reward + GAMMA * max(Q[next_state, a]).

## Spec coverage

- S1 PASS  S2 PASS  S3 PASS  S4 PASS
- S5 PARTIAL. Training matches (EPISODES = 1000, MAX_STEPS = 200); the final
  greedy run uses 200 steps instead of the specified 50 until T6 is done.

## Issues found
1. Final greedy run step cap is 200, not 50 (spec S5). Open (T6).
2. intent.md names vacuum_world.py; implementation imports q_env.py. Open (T9).
3. spec.md "Covers Intent criterion" quotes do not match the wording in
   intent.md (the Intent has Success Criteria bullets, not those quoted
   sentences). Suggest rewording spec traceability to the actual Success
   Criteria.
4. Stale "defaultdict(float)" comment in q_learning.py. Open (T10).
5. Intent says epsilon decay is optional; not implemented. Acceptable.

## Conclusion
Implementation meets all four acceptance tests and Intent success criteria.
Remaining items are spec/doc alignment, not functional defects.
