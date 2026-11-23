---
name: sdlc
description: Follow the software development lifecycle SDLC by writing the stage documents intent, spec, plan, tasks, and report as markdown files in the sdlc folder
---
# SDLC: stage documents for a code agent

Deliverable: five markdown files in ./sdlc/, written in this order, one write_file call each:
intent.md -> spec.md -> plan.md -> tasks.md -> report.md

Each stage must exist before the next one starts. Keep every file under 60 lines. Use plain markdown.

## Rules for this skill
- Write only inside sdlc/ while this skill is active, plus ticking boxes in sdlc/tasks.md. Implementation code is written by the main task, between tasks.md and report.md.
- Name real things. Before naming a file, function, folder or log path, check it with list_files, search or read_file. Never invent names.
- Do not overwrite a stage file you have not read. If it exists, read it and use patch_file to fix only what is wrong.
- Never claim a result you did not see. report.md may only cite run_shell output, test output or log lines you actually read.

## Steps
1. Run list_files on sdlc/ and read any stage file that already exists.
2. Read README.md and the files the task names, so the stages describe the real project.
3. Write sdlc/intent.md with the template below.
4. Write sdlc/spec.md. Every spec item must trace back to a success criterion in intent.md.
5. Write sdlc/plan.md. Every plan step must name the spec item it delivers.
6. Write sdlc/tasks.md as a checklist. Each task is one small action that can be verified.
7. Do the work in tasks.md. After each finished task, patch its "- [ ]" to "- [x]".
8. Run the checks (run_shell) and read the skill log at .mini-coding-agent/logs/skills.jsonl if skills were involved.
9. Write sdlc/report.md last, from the evidence in step 8.
10. Finish with a short summary that lists the five files and any task left unchecked.

## Templates
intent.md
- `# Intent: <title>`
- `## Problem` (2-4 sentences, in plain words)
- `## Goal` (numbered, what must be true when done)
- `## Success criteria` (checkboxes, each one testable)
- `## Non-goals`
- `## Risks` (risk and mitigation)

spec.md
- `# Spec: <title>`
- `## Behavior` (numbered requirements, each tagged S1, S2, ... and naming the intent criterion it covers)
- `## Interfaces` (files, functions, CLI flags, log fields, with exact names)
- `## Acceptance tests` (input and expected output for each requirement)

plan.md
- `# Plan: <title>`
- `## Steps` (numbered, each says "delivers S1, S2")
- `## Files to create or change`
- `## Order and dependencies`

tasks.md
- `# Tasks`
- one line per task: `- [ ] T1: <action> (verify: <command or file to check>)`

report.md
- `# Report: <title>`
- `## What was built` (files, one line each)
- `## Evidence` (the exact commands run and the key lines of output)
- `## Success criteria` (copy each criterion from intent.md and mark [x] or [ ] with the evidence)
- `## Deviations and open issues` (anything that differs from spec.md, and anything not verified)

## Pitfalls
- Do not write all five files from the first prompt alone. Later stages must use what earlier stages and the real code say.
- A criterion you could not verify stays unchecked in report.md. Say why.
- Keep the stage files consistent: if the code changes the design, patch spec.md and plan.md too.
- Use the XML form of write_file for multi-line markdown.
