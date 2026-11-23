import json
import tempfile
import unittest
from pathlib import Path

from skills import SkillRegistry

try:
    from mini_coding_agent import FakeModelClient, MiniAgent, SessionStore, WorkspaceContext
    HAVE_AGENT = True
except ImportError:
    HAVE_AGENT = False

SKILLS = {
    "pr-review": (
        "Review changed or newly written Python code in a pull request (PR) for bugs, "
        "correctness problems, and performance problems, and report findings without editing files",
        "PR REVIEW BODY",
    ),
    "gridworld-env": (
        "Build the 4x4 vacuum robot grid world environment with start, wall, trap, and recharge "
        "tiles, (x, y) coordinates, move offsets, step function, and path display",
        "GRIDWORLD BODY",
    ),
    "q-learning": (
        "Implement tabular Q-learning with a Q-table, update rule, epsilon-greedy exploration, "
        "discount factor, learning rate, epsilon, episodes, training loop, and greedy policy",
        "QLEARNING BODY",
    ),
}


def write_skills(root, flat=False):
    root = Path(root)
    for name, (description, body) in SKILLS.items():
        text = f"---\nname: {name}\ndescription: {description}\n---\n# {name}\n{body}\n"
        if flat:
            root.mkdir(parents=True, exist_ok=True)
            (root / f"{name}.md").write_text(text, encoding="utf-8")
        else:
            (root / name).mkdir(parents=True, exist_ok=True)
            (root / name / "skill.md").write_text(text, encoding="utf-8")


def read_log(path):
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines()]


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.log = self.root / "logs" / "skills.jsonl"

    def registry(self, flat=False, threshold=0.15):
        write_skills(self.root / "skill", flat=flat)
        return SkillRegistry(self.root / "skill", self.log, threshold)

    def test_discovery_folder_layout(self):
        self.assertEqual(set(self.registry().skills), set(SKILLS))

    def test_discovery_flat_layout(self):
        self.assertEqual(set(self.registry(flat=True).skills), set(SKILLS))

    def test_discovery_ignores_folder_without_skill_md(self):
        (self.root / "skill" / "empty").mkdir(parents=True)
        self.assertNotIn("empty", self.registry().skills)

    def test_missing_directory_is_empty(self):
        reg = SkillRegistry(self.root / "nope", self.log)
        self.assertEqual(reg.skills, {})
        self.assertEqual(reg.match("anything"), [])

    def test_frontmatter(self):
        meta, body = SkillRegistry.parse_frontmatter("---\nname: x\ndescription: y: z\n---\nhello\n")
        self.assertEqual(meta, {"name": "x", "description": "y: z"})
        self.assertEqual(body.strip(), "hello")

    def test_A1_qlearning_prompt_selects_env_and_qlearning(self):
        selected = self.registry().match("Implement Q-learning for the vacuum robot grid world and run it")
        self.assertIn("gridworld-env", selected)
        self.assertIn("q-learning", selected)
        self.assertNotIn("pr-review", selected)

    def test_A2_review_prompt_selects_only_pr_review(self):
        self.assertEqual(self.registry().match("Review this PR for bugs"), ["pr-review"])

    def test_A3_unrelated_prompt_selects_nothing_but_is_logged(self):
        reg = self.registry()
        self.assertEqual(reg.match("What is the weather like on Mars"), [])
        entry = read_log(self.log)[-1]
        self.assertEqual(entry["event"], "similarity_check")
        self.assertEqual(entry["selected"], [])

    def test_log_has_prompt_scores_threshold(self):
        reg = self.registry()
        reg.match("Review this PR for bugs")
        entry = read_log(self.log)[0]
        self.assertEqual(entry["prompt"], "Review this PR for bugs")
        self.assertEqual(set(entry["scores"]), set(SKILLS))
        self.assertEqual(entry["threshold"], 0.15)

    def test_threshold_controls_selection(self):
        self.assertEqual(self.registry(threshold=0.99).match("Review this PR for bugs"), [])


@unittest.skipUnless(HAVE_AGENT, "mini_coding_agent.py not importable")
class AgentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        write_skills(self.root / "skill")
        self.log = self.root / ".mini-coding-agent" / "logs" / "skills.jsonl"

    def agent(self, outputs):
        workspace = WorkspaceContext.build(self.root)
        store = SessionStore(self.root / ".mini-coding-agent" / "sessions")
        client = FakeModelClient(outputs)
        agent = MiniAgent(client, workspace, store, approval_policy="never", skills_dir="skill")
        return agent, client

    def test_prompt_trigger_adds_skill_body_and_logs_execution(self):
        agent, client = self.agent(["<final>ok</final>"])
        agent.ask("Review this PR for bugs")
        self.assertIn("Active skill: pr-review", client.prompts[0])
        self.assertIn("PR REVIEW BODY", client.prompts[0])
        events = read_log(self.log)
        executed = [e for e in events if e["event"] == "skill_executed"]
        self.assertEqual([(e["skill"], e["reason"]) for e in executed], [("pr-review", "prompt_match")])

    def test_A4_use_skill_valid_logs_tool_request(self):
        agent, client = self.agent([
            '<tool>{"name":"use_skill","args":{"name":"q-learning"}}</tool>',
            "<final>done</final>",
        ])
        agent.ask("hello there")  # matches nothing by prompt
        self.assertIn("QLEARNING BODY", client.prompts[1])
        executed = [e for e in read_log(self.log) if e["event"] == "skill_executed"]
        self.assertEqual([(e["skill"], e["reason"]) for e in executed], [("q-learning", "tool_request")])

    def test_A4_use_skill_invalid_name_is_an_error(self):
        agent, _ = self.agent([])
        result = agent.run_tool("use_skill", {"name": "does-not-exist"})
        self.assertTrue(result.startswith("error:"))

    def test_multiple_skills_active_together(self):
        agent, client = self.agent(["<final>ok</final>"])
        agent.ask("Implement Q-learning for the vacuum robot grid world and run it")
        self.assertIn("GRIDWORLD BODY", client.prompts[0])
        self.assertIn("QLEARNING BODY", client.prompts[0])

    def test_skills_clear_on_next_request(self):
        agent, client = self.agent(["<final>a</final>", "<final>b</final>"])
        agent.ask("Review this PR for bugs")
        agent.ask("hello there")
        self.assertNotIn("PR REVIEW BODY", client.prompts[1])


REAL_SKILLS = Path(__file__).parent / "skill"


class RealSkillFolderTests(unittest.TestCase):
    """Run the similarity check against the skills actually shipped in skill/."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.reg = SkillRegistry(REAL_SKILLS, Path(self.tmp.name) / "skills.jsonl")

    def test_sdlc_skill_is_discovered_with_required_sections(self):
        self.assertIn("sdlc", self.reg.skills)
        body = self.reg.skills["sdlc"]["body"]
        for stage in ("intent.md", "spec.md", "plan.md", "tasks.md", "report.md"):
            self.assertIn(stage, body)

    def test_sdlc_prompts_select_only_sdlc(self):
        for prompt in (
            "Follow the SDLC and write the intent spec plan tasks and report files in the sdlc folder",
            "Write the sdlc documents for this project",
        ):
            self.assertEqual(self.reg.match(prompt), ["sdlc"], prompt)

    def test_lab4_prompts_do_not_select_sdlc(self):
        for prompt in (
            "Train the vacuum robot with Q-learning",
            "Implement Q-learning for the vacuum robot grid world and run it",
        ):
            selected = self.reg.match(prompt)
            self.assertNotIn("sdlc", selected, prompt)
            self.assertIn("q-learning", selected, prompt)

    def test_unrelated_prompt_selects_nothing(self):
        self.assertEqual(self.reg.match("What is the weather like on Mars"), [])


if __name__ == "__main__":
    unittest.main()
