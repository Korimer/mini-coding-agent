"""Component 7) Agent Skills for mini_coding_agent.py (standard library only).

A skill is a folder under the skills directory (default: skill/) that holds a
skill.md file, e.g. skill/pr-review/skill.md. A flat skill/<name>.md file is
also accepted. skill.md starts with one-line frontmatter keys:

    ---
    name: pr-review
    description: what the skill does, in words a matching prompt would use
    ---
    instructions...

The registry:
  1. discovers skills,
  2. scores a prompt against every skill (cosine similarity, bag of words),
  3. logs the prompt, every score, the threshold and the selection,
  4. logs each executed skill (see MiniAgent.activate_skill).
"""

import json
import math
import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

STOPWORDS = {
    "a", "an", "and", "the", "of", "to", "for", "in", "on", "with", "it", "is",
    "this", "that", "me", "my", "i", "please", "then", "or", "be", "as", "at",
}


def _now():
    return datetime.now(timezone.utc).isoformat()


class SkillRegistry:
    def __init__(self, root, log_path, threshold=0.15):
        # root may be one folder or a list (nearest first); the first folder defining a name wins
        self.roots = [Path(r) for r in (root if isinstance(root, (list, tuple)) else [root])]
        self.root = self.roots[0]
        self.log_path = Path(log_path)
        self.threshold = float(threshold)
        self.last_scores = {}
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.skills = self.discover()

    # ---------- discovery ----------
    def discover(self):
        skills = {}
        for root in self.roots:
            self._discover_in(root, skills)
        return skills

    def _discover_in(self, root, skills):
        if not root.is_dir():
            return
        for entry in sorted(root.iterdir()):
            if entry.is_dir():
                md = next((p for p in sorted(entry.iterdir()) if p.name.lower() == "skill.md"), None)
                fallback = entry.name
            elif entry.is_file() and entry.suffix.lower() == ".md" and entry.stem.lower() not in {"readme", "skill"}:
                md, fallback = entry, entry.stem
            else:
                continue
            if md is None:
                continue
            meta, body = self.parse_frontmatter(md.read_text(encoding="utf-8", errors="replace"))
            name = meta.get("name") or fallback
            if name in skills:
                continue
            skills[name] = {
                "name": name,
                "description": meta.get("description", ""),
                "path": str(md),
                "body": body.strip(),
            }

    @staticmethod
    def parse_frontmatter(text):
        text = text.replace("\r\n", "\n")
        match = re.match(r"\A---[ \t]*\n(.*?)\n---[ \t]*(?:\n|\Z)(.*)\Z", text, re.S)
        if not match:
            return {}, text
        meta = {}
        for line in match.group(1).splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                meta[key.strip()] = value.strip()
        return meta, match.group(2)

    # ---------- similarity ----------
    @staticmethod
    def tokens(text):
        words = []
        for word in re.findall(r"[a-z0-9]+", str(text).lower()):
            if word in STOPWORDS:
                continue
            if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
                word = word[:-1]  # crude plural stemming: bugs -> bug
            words.append(word)
        return words

    @classmethod
    def vec(cls, text):
        return Counter(cls.tokens(text))

    @staticmethod
    def cosine(a, b):
        dot = sum(a[key] * b[key] for key in a if key in b)
        norm_a = math.sqrt(sum(v * v for v in a.values()))
        norm_b = math.sqrt(sum(v * v for v in b.values()))
        return dot / (norm_a * norm_b) if norm_a and norm_b else 0.0

    def match(self, prompt):
        """Return the skill names at or above the threshold, best first. Always logs."""
        prompt_vec = self.vec(prompt)
        scores = {
            name: round(self.cosine(prompt_vec, self.vec(skill["name"] + " " + skill["description"])), 4)
            for name, skill in self.skills.items()
        }
        self.last_scores = scores
        selected = [
            name for name, score in sorted(scores.items(), key=lambda item: (-item[1], item[0]))
            if score >= self.threshold
        ]
        self.log({
            "event": "similarity_check",
            "prompt": prompt,
            "scores": scores,
            "threshold": self.threshold,
            "selected": selected,
        })
        return selected

    # ---------- logging / display ----------
    def log(self, entry):
        entry = {"ts": _now(), **entry}
        with self.log_path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(entry) + "\n")

    def describe(self):
        if not self.skills:
            return f"No skills found in {', '.join(map(str, self.roots))}"
        lines = [f"Skills in {', '.join(map(str, self.roots))} (threshold {self.threshold}):"]
        for name, skill in self.skills.items():
            lines.append(f"- {name}: {skill['description']}")
        return "\n".join(lines)
