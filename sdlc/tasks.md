# Tasks
- [x] T1: Registry with discovery, frontmatter, cosine match, JSONL log (verify: `python3 -m unittest tests`)
- [x] T2: `use_skill` tool, prompt injection, `skill_executed` log, `/skills` (verify: AgentTests in `tests.py`)
- [x] T3: Lab 5 skills `gridworld-env`, `q-learning`, `code-review` (verify: `/skills` lists them)
- [x] T4: `sdlc` skill (verify: RealSkillFolderTests, scripted run writes files to `sdlc/`)
- [x] T5: Fix packaging, add `skills` to `py-modules` in `pyproject.toml` (verify: `grep py-modules pyproject.toml`)
- [x] T6: Write the five stage files to `sdlc/` (verify: `ls sdlc`)
- [ ] T7: Solve Lab 4 through the agent with a real Ollama model (verify: `q_env.py` and `q_learning.py` exist, policy grid and path printed, `skills.jsonl` shows `q-learning` and `gridworld-env` executed)
- [ ] T8: Add the third course feature, hooks (verify: a hook fires and shows in a log)
- [ ] T9: Update `report.md` with the T7 evidence
