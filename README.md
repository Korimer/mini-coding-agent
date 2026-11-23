&nbsp;
# Mini-Coding-Agent

This folder contains a small standalone coding agent:

- code: `mini_coding_agent.py`
- CLI: `mini-coding-agent`

It is a minimal local agent loop with:

- workspace snapshot collection
- stable prompt plus turn state
- structured tools
- approval handling for risky tools
- transcript and memory persistence
- bounded delegation

The model backend is currently based on Ollama.

<a href="https://magazine.sebastianraschka.com/p/components-of-a-coding-agent">
  <img src="https://substack-post-media.s3.amazonaws.com/public/images/49b97718-57f4-4977-99c8-8ad5c4d32af3_1548x862.png" width="500px">
</a>

<br>

**[The detailed tutorial: Components of a Coding Agent](https://magazine.sebastianraschka.com/p/components-of-a-coding-agent)**

&nbsp;
## Group 15 addition: Agent Skills component (CS440)

This fork adds a seventh component, **agent skills**, and a `post_run` hook. The rest of this README describes the original agent; this section covers what changed.

### Project structure
```
mini_coding_agent.py     agent, with skills wired in (use_skill tool, /skills command, --skills-dir, --skill-threshold)
skills.py                skill registry: discovery, similarity check, JSONL logging
hooks.py                 post_run hook: prints a run summary, logs to hooks.jsonl
skill/<name>/skill.md    skills: frontmatter (name, description), then instructions
  code-review/           review changed Python code without editing it
  grid-world/            build the 4x4 vacuum grid world (q_env.py)
  q-learning/            tabular Q-learning for the vacuum robot (q_learning.py)
  sdlc/                  write the SDLC stage documents
sdlc-agent/              SDLC documents for building the skills component
sdlc-lab4/               SDLC documents for the Lab 4 solution
q_env.py, q_learning.py  Lab 4 solution written by the agent using the skills
lab4_run/logs/           logs from that run (skills.jsonl, hooks.jsonl)
tests.py                 unit tests for skills and hooks
```

### How a skill is triggered
1. At startup, the agent reads every `skill/<name>/skill.md`.
2. For each prompt, it computes the cosine similarity between the prompt's words and each skill's name and description (bag of words, common words removed). Every skill scoring at least the threshold (default 0.15) is loaded into the prompt.
3. During a run, the model can also load a skill by name with the `use_skill` tool.

### How to run
Requires Python 3.10 or newer and Ollama.
```bash
ollama pull qwen3.5:9b
python3 mini_coding_agent.py --model qwen3.5:9b --max-steps 20 --max-new-tokens 2048
```
- `/skills` lists the skills the agent found.
- `--skills-dir` (default `skill`), `--skill-threshold` (default 0.15), `--no-hooks` (turn off the run summary).
- Writing whole files needs a larger `--max-steps` and `--max-new-tokens` than the defaults.

### Logs
Written to `.mini-coding-agent/logs/` in the working folder. That folder is gitignored, so a copy from the Lab 4 run is in `lab4_run/logs/`.
- `skills.jsonl`: `similarity_check` events (prompt, score per skill, threshold, selected skills) and `skill_executed` events (skill, reason, score, path).
- `hooks.jsonl`: one event per hook run.

### Lab 4 with the mini agent
Prompt used:
> Solve Lab 4: build the 4x4 vacuum robot grid world and train the robot with tabular Q-learning, using epsilon-greedy exploration, then print the greedy path. The skills are already active, so do not call use_skill. Start by writing q_env.py.

`python3 q_learning.py` then prints the learned policy and the greedy path, which reaches the recharge spot in 6 moves. The full run history, including what had to be fixed, is in `sdlc-agent/report.md`.

### Tests
```bash
python3 -m unittest tests
```

&nbsp;
## Six Core Components

<a href="https://magazine.sebastianraschka.com/p/components-of-a-coding-agent">
  <img alt="Six core components of a coding agent" src="https://sebastianraschka.com/images/github/mini-coding-agent/six-components.webp" width="500px">
</a>

This coding harness is organized around six practical building blocks:

1. **Live repo context**  
   The agent collects stable workspace facts upfront, such as repo layout, instructions, and git state.
2. **Prompt shape and cache reuse**  
   A stable prompt prefix, which is separate from the changing request, transcript, and memory so repeated model calls can reuse the static parts efficiently.
3. **Structured tools, validation, and permissions**  
   The model works through named tools with checked inputs, workspace path validation, and approval gates instead of free-form arbitrary actions.
4. **Context reduction and output management**  
   Long outputs are clipped, repeated reads are deduplicated, and older transcript entries are compressed to keep prompt size under control.
5. **Transcripts, memory, and resumption**  
   The runtime keeps both a full durable transcript and a smaller working memory so sessions can be resumed while preserving important state via working memory.
6. **Delegation and bounded subagents**  
   Scoped subtasks can be delegated to helper agents that inherit enough context to help (but operate within limits).

&nbsp;
## Requirements

You need:

- Python 3.10+
- Ollama installed
- an Ollama model pulled locally

Optional:

- `uv` for environment management and the `mini-coding-agent` CLI entry point

This project has no Python runtime dependency beyond the standard library, so you can run it directly with `python mini_coding_agent.py` if you do not want to use `uv`.

&nbsp;
## Install Ollama

Install Ollama on your machine so the `ollama` command is available in your shell.

Official installation link: [ollama.com/download](https://ollama.com/download)

Then verify:

```bash
ollama --help
```

Start the server:

```bash
ollama serve
```

In another terminal, pull a model. Example:

```bash
ollama pull qwen3.5:4b
```

Qwen 3.5 model library:

- [ollama.com/library/qwen3.5](https://ollama.com/library/qwen3.5)

The default in this project is `qwen3.5:4b`. If you have sufficient memory, it is worth trying a larger model such as `qwen3.5:9b` or another larger Qwen 3.5 variant. The agent just sends prompts to Ollama's `/api/generate` endpoint.

&nbsp;
## Project Setup

Clone the repo or your fork and change into it:

```bash
git clone https://github.com/rasbt/mini-coding-agent.git
cd mini-coding-agent
```

If you forked it first, use your fork URL instead:

```bash
git clone https://github.com/<your-github-user>/mini-coding-agent.git
cd mini-coding-agent
```



&nbsp;
## Basic Usage

Start the agent:

```bash
cd mini-coding-agent
uv run mini-coding-agent
```

Without `uv`, run the script directly:

```bash
cd mini-coding-agent
python mini_coding_agent.py
```

By default it uses:

- model: `qwen3.5:4b`
- approval: `ask`

For a concrete usage example, see [EXAMPLE.md](EXAMPLE.md).

&nbsp;
## Approval Modes

Risky tools such as shell commands and file writes are gated by approval.

- `--approval ask`
  prompts before risky actions (default and recommended)
- `--approval auto`
  allows risky actions automatically, including arbitrary command execution and file writes by the model; use only with trusted prompts and trusted repositories
- `--approval never`
  denies risky actions

Example:

```bash
uv run mini-coding-agent --approval auto
```



&nbsp;
## Resume Sessions

The agent saves sessions under the target workspace root in:

```text
.mini-coding-agent/sessions/
```

Resume the latest session:

```bash
uv run mini-coding-agent --resume latest
```


Resume a specific session:

```bash
uv run mini-coding-agent --resume 20260401-144025-2dd0aa
```


&nbsp;
## Interactive Commands

Inside the REPL, slash commands are handled directly by the agent instead of
being sent to the model as a normal task.

- `/help`
  shows the list of available interactive commands
- `/memory`
  prints the distilled session memory, including the current task, tracked files, and notes
- `/session`
  prints the path to the current saved session JSON file
- `/reset`
  clears the current session history and distilled memory but keeps you in the REPL
- `/exit`
  exits the interactive session
- `/quit`
  exits the interactive session; alias for `/exit`

&nbsp;
## Main CLI Flags

```bash
uv run mini-coding-agent --help
```

Without `uv`:

```bash
python mini_coding_agent.py --help
```

CLI flags are passed before the agent starts. Use them to choose the workspace,
model connection, resume behavior, approval mode, and generation limits.

Important flags:

- `--cwd`
  sets the workspace directory the agent should inspect and modify; default: `.`
- `--model`
  selects the Ollama model name, such as `qwen3.5:4b`; default: `qwen3.5:4b`
- `--host`
  points the agent at the Ollama server URL (usually not needed); default: `http://127.0.0.1:11434`
- `--ollama-timeout`
  controls how long the client waits for an Ollama response (usually not needed); default: `300` seconds
- `--resume`
  resumes a saved session by id or uses `latest`; default: start a new session
- `--approval`
  controls how risky tools are handled: `ask`, `auto`, or `never`; default: `ask`
- `--max-steps`
  limits how many model and tool turns are allowed for one user request; default: `6`
- `--max-new-tokens`
  caps the model output length for each step; default: `512`
- `--temperature`
  controls sampling randomness; default: `0.2`
- `--top-p`
  controls nucleus sampling for generation; default: `0.9`

&nbsp;
## Example

See [EXAMPLE.md](EXAMPLE.md)

&nbsp;
## Notes & Tips

- The agent expects the model to emit either `<tool>...</tool>` or `<final>...</final>`.
- Different Ollama models will follow those instructions with different reliability.
- If the model does not follow the format well, use a stronger instruction-following model.
- The agent is intentionally small and optimized for readability, not robustness.
