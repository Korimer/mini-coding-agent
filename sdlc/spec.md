# Spec: Agent Skills component

## Behavior
- **S1 (C1, C6) Discovery.** `SkillRegistry.discover()` scans `skill/`. A folder holding `skill.md` is a skill; a flat `skill/<name>.md` is also accepted. A folder without `skill.md` is ignored. A missing `skill/` gives an empty registry.
- **S2 (C1) Format.** `skill.md` starts with `---` frontmatter holding `name:` and `description:`, then the instructions. If `name` is missing the folder name is used.
- **S3 (C1, C6) Similarity.** `match(prompt)` builds a bag-of-words vector of the prompt and of each skill's `name + description` (lowercase, stopwords removed, crude plural stemming), computes cosine similarity, and returns every skill with score >= threshold, best first. Default threshold 0.15.
- **S4 (C2) Logging.** Each `match` appends a `similarity_check` line to `.mini-coding-agent/logs/skills.jsonl` with `ts, prompt, scores, threshold, selected`, even when nothing is selected.
- **S5 (C2) Activation.** `MiniAgent.activate_skill(name, reason)` stores the skill as active, appends a `skill_executed` line (`skill, reason, score, path`), records it in the session under `skills_used`, and prints `[skill] <name> activated (<reason>)`. `reason` is `prompt_match` or `tool_request`.
- **S6 (C1) Injection.** Active skills are added to every model prompt as `Active skill: <name>` followed by the skill body. Active skills are cleared at the start of each user request.
- **S7 (C3) Tool.** `use_skill(name)` activates a skill mid-run. An unknown name returns `error: ...`. A skill that is already active returns a message instead of activating twice.
- **S8 (C4) SDLC skill.** `skill/sdlc/skill.md` tells the agent to write `sdlc/intent.md, spec.md, plan.md, tasks.md, report.md` in that order, one `write_file` call each, with templates and these rules: use real names, read before overwrite, report only evidence that was seen.
- **S9 (C5) Lab 5 skills.** `gridworld-env` writes `q_env.py`; `q-learning` writes `q_learning.py` and prints the policy and the greedy path; `code-review` reviews the result read-only.

- **S10 (C7) post_run hook.** `hooks.py` provides `HookRegistry` with one event, `post_run`. `MiniAgent.ask()` runs the agent loop (`_ask`) and then fires `post_run` with `prompt, final, status, skills, tools, seconds`. The built-in hook `print_run_summary` prints the prompt, status (`answered` or `stopped`), seconds, skills used, and each tool call with its clipped result. It does not repeat the final answer because the CLI prints that. A hook that raises is caught and logged, never breaking the run. Sub-agents (`delegate`) do not print their own summary. Each hook call appends a `hook_run` line to `.mini-coding-agent/logs/hooks.jsonl`.

## Interfaces
- Files: `skills.py` (registry), `hooks.py` (hook registry and summary hook), `mini_coding_agent.py` (integration, section "7) Agent Skills Component"), `skill/<name>/skill.md`.
- CLI: `--skills-dir` (default `skill`), `--skill-threshold` (default 0.15), `--approval auto` (needed so skills can call `write_file`), `--max-steps`, `--no-hooks`.
- REPL: `/skills` lists discovered skills.
- Logs: `.mini-coding-agent/logs/skills.jsonl` and `hooks.jsonl`, one JSON object per line.

## Acceptance tests
| Spec | Input | Expected |
|---|---|---|
| S3 | "Train the vacuum robot with Q-learning" | selected = `q-learning`, `gridworld-env` |
| S3 | "Follow the SDLC and write the intent spec plan tasks and report files in the sdlc folder" | selected = `sdlc` only |
| S3 | "What is the weather like on Mars" | selected = [] and a log line exists |
| S4 | any prompt | log line has prompt, scores for every skill, threshold |
| S5 | prompt match | `skill_executed` with `reason: prompt_match` and a score |
| S7 | model calls `use_skill` with `q-learning` | `skill_executed` with `reason: tool_request` |
| S7 | `use_skill` with `nope` | result starts with `error:` |
| S8 | SDLC prompt, approval auto | files appear under `sdlc/` |
| S10 | any request | summary printed after the run, `hook_run` line with `status: ok` |
| S10 | hook that raises | run still returns, log line has `status: error` |
| S10 | `--no-hooks` | no summary printed |
