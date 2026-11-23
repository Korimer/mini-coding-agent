"""Component 8) Hooks for mini_coding_agent.py (standard library only).

A hook is a function the agent calls automatically at a fixed point in its life.
The agent does not choose to run it and the model does not see it.

Events:
  post_run  fired once when MiniAgent.ask() finishes (answer or step limit).

A hook receives one dict (the payload) and may print. A hook that raises is
caught and logged; it never breaks the run. Every call is logged to
.mini-coding-agent/logs/hooks.jsonl as {"event": "hook_run", ...}.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

EVENTS = {"post_run"}


class HookRegistry:
    def __init__(self, log_path):
        self.log_path = Path(log_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.hooks = {event: [] for event in EVENTS}

    def register(self, event, fn, name=None):
        if event not in EVENTS:
            raise ValueError(f"unknown hook event '{event}'; known: {', '.join(sorted(EVENTS))}")
        self.hooks[event].append((name or getattr(fn, "__name__", "hook"), fn))

    def run(self, event, payload):
        for name, fn in self.hooks.get(event, []):
            entry = {"event": "hook_run", "hook_event": event, "hook": name, "status": "ok"}
            try:
                fn(payload)
            except Exception as exc:  # fail open: a broken hook must not stop the agent
                entry.update(status="error", error=str(exc))
            self.log(entry)

    def log(self, entry):
        entry = {"ts": datetime.now(timezone.utc).isoformat(), **entry}
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")


def print_run_summary(payload):
    """Built-in post_run hook: print what the run did.

    The final answer is not repeated here because the CLI prints it right after.
    """
    def one_line(text, limit=100):
        text = " ".join(str(text).split())
        return text if len(text) <= limit else text[: limit - 3] + "..."

    tools = payload["tools"]
    skills = ", ".join(payload["skills"]) or "none"
    print()
    print("=== run summary (post_run hook) ===")
    print(f"prompt : {one_line(payload['prompt'])}")
    print(f"status : {payload['status']} ({len(tools)} tool call(s), {payload['seconds']:.1f}s)")
    print(f"skills : {skills}")
    for index, tool in enumerate(tools, 1):
        print(f"  {index}. {tool['name']} -> {one_line(tool['result'])}")
    print("===================================")
