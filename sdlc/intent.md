# intent.md: Agent Skills Component for mini-coding-agent

**Stage:** 1 of 5 (Intent / Requirements framing)
**Status:** Draft v1

## Problem
`mini-coding-agent` (https://github.com/rasbt/mini-coding-agent) implements the standard code-agent components but has no **agent skills** component. The agent cannot discover a skill folder, decide that a skill is relevant to a prompt, and follow that skill's instructions.

## Goal
Add a skills component so that the agent can:
1. **Discover** skill folders (e.g. `skills/pr-review/`, `skills/q-learning-vacuum/`), each containing a `SKILL.md`.
2. **Match** a user prompt (or a mid-run need) against skill descriptions using a similarity check.
3. **Trigger** the best-matching skill by loading `SKILL.md` and injecting its instructions into the agent's context so the agent executes them.
4. **Log** the prompt, the similarity check, and the executed skill.

## Demonstration goal
Use the skill created in Lab 5 to solve **Lab 4** through the mini agent: a vacuum robot learning to navigate a 4x4 grid with **Q-learning**, with no transition model (T) or reward table (R) given.

```
start 0  0  0
0     X  0  0
0     0  0  0
0    -1  0  10
```

## Course constraints
- Use **3 of 4** features: hooks, MCP, skills, sub-agents.
  - Chosen: **skills** (required), **hooks**, **sub-agents**.
  - Not chosen: **MCP** (needs an external server and adds no value for this lab).
- Follow an SDLC for code agents. Each stage leaves a file: `intent.md`, `spec.md`, `plan.md`, `tasks.md`, `report.md`.

## Success criteria
- [ ] Prompt "train the vacuum robot with Q-learning" triggers the Lab 5 skill; an unrelated prompt triggers none.
- [ ] Every run writes a log entry with: prompt, per-skill similarity scores, threshold, decision, executed skill.
- [ ] Lab 4 is solved end to end via the skill: Q-table learned, greedy path printed, path avoids the -1 cell and the wall.
- [ ] Hooks and sub-agents are demonstrably used (visible in logs).
- [ ] All five SDLC files exist and are consistent with the code.

## Non-goals
- No embedding models or external services; matching must run locally with the standard library.
- No MCP integration.
- No skill authoring UI or skill marketplace.

## Risks
| Risk | Mitigation |
|---|---|
| Repo's loop has no clean hook points | Wrap the existing prompt-building and tool-call functions instead of rewriting them |
| Keyword similarity picks the wrong skill | Log scores; tune the threshold; add tests for near-miss prompts |
| Lab 5 skill is not RL-related | Decide in spec.md whether to adapt it or add an RL skill alongside it |
