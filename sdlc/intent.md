# Intent: Agent Skills component for mini-coding-agent

## Problem
`mini-coding-agent` (https://github.com/rasbt/mini-coding-agent) has the standard code-agent components but no **agent skills** component. It cannot find a skill folder, decide a skill fits a prompt, and follow that skill's instructions. There is also no record of why a skill was or was not used.

## Goal
1. Discover skill folders such as `skill/q-learning/`, each holding a `skill.md`.
2. Score a user prompt against every skill with a similarity check.
3. Trigger the matching skills by injecting their instructions into the agent prompt, either when the prompt matches or when the model asks for one with the `use_skill` tool.
4. Log the prompt, the similarity check, and every executed skill.
5. Ship a skill (`sdlc`) that makes the agent follow the SDLC and write its stage documents to `./sdlc`.
6. Use the Lab 5 skills to solve Lab 4 (Q-learning vacuum robot) through the agent.

## Lab 4 in one line
A vacuum robot learns to move on a 4x4 grid with Q-learning, with no transition model (T) or reward table (R) given. Start (0, 3), wall (1, 2), trap (1, 0) = -1, recharge spot (3, 0) = +10.

## Success criteria
- [ ] C1: "Train the vacuum robot with Q-learning" triggers `q-learning` and `gridworld-env`; an unrelated prompt triggers nothing.
- [ ] C2: Every prompt writes a `similarity_check` log line (prompt, scores, threshold, selected) and every activation writes a `skill_executed` line.
- [ ] C3: The model can load a skill mid-run with `use_skill`; an unknown name is an error.
- [ ] C4: "Follow the SDLC ..." triggers only the `sdlc` skill, and that skill leads to five files in `sdlc/`: intent, spec, plan, tasks, report.
- [ ] C5: Lab 4 is solved through the agent: policy grid and greedy path printed, path avoids the wall and the trap.
- [ ] C6: Only the standard library is used for matching.

## Non-goals
- No embedding models or external services.
- No skill marketplace or skill authoring UI.
- No MCP integration.

## Course constraint
Use 3 of 4 features: hooks, MCP, skills, sub-agents. Chosen: **skills** (this work), **sub-agents** (the existing read-only `delegate` tool), **hooks** (not yet built, see report.md). Not chosen: MCP.

## Risks
| Risk | Mitigation |
|---|---|
| Keyword similarity picks the wrong skill | Log all scores, keep the threshold configurable (`--skill-threshold`), test near-miss prompts |
| Small local model ignores a long skill | Keep each skill short, with numbered steps and exact tool names |
| Step budget (default 6) too small for 5 documents | Run with `--max-steps 12` or more |
