# Plan: Agent Skills component

## Steps
1. **Registry** (S1, S2, S3, S4): write `skills.py` with discovery, frontmatter parsing, cosine similarity, JSONL logging.
2. **Agent integration** (S5, S6, S7): in `mini_coding_agent.py` add `skill_text`, `activate_skill`, the `use_skill` tool, the prompt section, the `--skills-dir` and `--skill-threshold` flags, and `/skills`.
3. **Lab 5 skills** (S9): write `skill/gridworld-env`, `skill/q-learning`, `skill/code-review`.
4. **SDLC skill** (S8): write `skill/sdlc/skill.md`; tune its description so SDLC prompts select it and Lab 4 prompts do not.
5. **Tests** (all): unit tests in `tests.py` with temporary skills, plus tests against the real `skill/` folder.
6. **Lab 4 run** (S9, C5): start the agent with `--approval auto --max-steps 12`, give it the Lab 4 prompt, check the log and the printed path.
7. **Report**: fill `sdlc/report.md` from real output.

## Files to create or change
- New: `skills.py`, `skill/*/skill.md`, `sdlc/*.md`, `tests.py`
- Changed: `mini_coding_agent.py`, `pyproject.toml` (add `skills` to `py-modules`)

## Order and dependencies
Step 1 before 2. Steps 3 and 4 need step 1 (they are read by it). Step 5 needs 1 to 4. Step 6 needs a running Ollama model and cannot be done without it.
