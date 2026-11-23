# Report: Agent Skills component

## What was built
- `skills.py`: skill registry (discovery, frontmatter, cosine similarity, JSONL log).
- `mini_coding_agent.py`: component 7, `use_skill` tool, prompt injection, `--skills-dir`, `--skill-threshold`, `/skills`.
- `skill/gridworld-env`, `skill/q-learning`, `skill/code-review`: Lab 5 skills.
- `skill/sdlc`: skill that writes the five stage documents to `sdlc/`.
- `hooks.py` and `ask()` wrapper: `post_run` hook that prints a run summary and logs to `hooks.jsonl`; `--no-hooks` flag.
- `tests.py`: 24 unit tests.
- `pyproject.toml`: `skills` and `hooks` added to `py-modules` (without it an installed package could not import `skills.py`).

## Evidence
Command: `python3 -m unittest tests`
Result: `Ran 24 tests ... OK`

Similarity check on the real `skill/` folder (threshold 0.15):

| Prompt | Selected | Top scores |
|---|---|---|
| Follow the SDLC and write the intent spec plan tasks and report files in the sdlc folder | sdlc | sdlc 0.78 |
| Train the vacuum robot with Q-learning | q-learning, gridworld-env | 0.43, 0.19 |
| Implement Q-learning for the vacuum robot grid world and run it | q-learning, gridworld-env | 0.40, 0.29 |
| Review this PR for bugs | code-review | 0.35 |
| What is the weather like on Mars | none | all 0.0 |

Scripted run (real `MiniAgent` and real `skill/` folder, but a scripted `FakeModelClient` instead of an LLM, `--approval auto`): the SDLC prompt produced these log lines and `write_file` created `sdlc/intent.md` and `sdlc/spec.md`.
```
similarity_check  selected=['sdlc'] threshold=0.15
skill_executed    skill=sdlc reason=prompt_match score=0.7766
```
Example `post_run` output (from the HookTests):
```
=== run summary (post_run hook) ===
prompt : Create hello.py
status : answered (1 tool call(s), 0.0s)
skills : none
  1. write_file -> wrote hello.py (12 chars)
===================================
```
The `tests/test_mini_coding_agent.py` file (pytest, not installed here) was run through a small shim: 17 of 19 passed; one failure was my shim lacking `pytest.skip`, the other (`test_welcome_screen_keeps_box_shape_for_long_paths`) also fails on the original unmodified code.

Note: with `--approval never` (or `ask` and a denial) `write_file` is refused, so the SDLC skill needs `--approval auto`.

## Success criteria
- [x] C1: prompt triggers the right skills, unrelated prompt triggers none (table above, unit tests).
- [x] C2: `similarity_check` and `skill_executed` lines are written (unit tests, scripted run).
- [x] C3: `use_skill` loads a skill mid-run; unknown name is an error (unit tests).
- [ ] C4: Trigger and file writing verified with a scripted model only. Not yet verified that a real Ollama model follows the skill and writes all five files within the step budget.
- [ ] C5: Lab 4 not yet run through the agent. It needs a running Ollama model, which was not available.
- [x] C6: Standard library only.

## Deviations and open issues
- `intent.md` and earlier drafts said `skills/` and `SKILL.md`; the implementation uses `skill/` and `skill.md`. These documents were rewritten to match the code.
- An earlier `requirements.md` described a different design than the code and was removed.
- **Hooks are minimal.** Only the `post_run` event exists, with one built-in hook. There is no config file and no `PreToolUse`/`PostToolUse` events. Whether this satisfies the course definition of hooks is unconfirmed.
- `tests.py` imported a module that no longer existed (`skill_registry`); fixed to `skills`.
- Matching is keyword-based, so a prompt that shares no words with a skill description will not trigger it. The model can still load the skill with `use_skill`.
