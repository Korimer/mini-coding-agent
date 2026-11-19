# Spec: Implement Agent Skills Component for mini-coding-agent

## Overview
This specification details the implementation of an "agent skills" component that allows the agent to discover, match, and trigger skill folders based on user prompts.

## Requirements

### 1. Skill Discovery
- Scan the `skills/` directory for subdirectories
- Each subdirectory represents a skill
- Parse `SKILL.md` from each skill folder to extract:
  - Skill name/title
  - Description
  - Instructions/prompts to use

### 2. Skill Matching
- Take a user prompt and match it against skill descriptions
- Use keyword-based or simple text similarity matching
- Return the best-matching skill or None if no match found

### 3. Integration with Agent Loop
- Modify the agent's main loop to:
  - Call skill discovery at the start of each turn
  - Match the current prompt against discovered skills
  - If a match is found, inject the skill's instructions into the context before processing

## Implementation Details

### Data Structures
```python
class Skill:
    name: str
    description: str
    instructions: str
    path: str
```

### Functions to Implement
1. `discover_skills()` - Scans skills/ directory and returns list of Skill objects
2. `match_skill(prompt: str) -> Optional[Skill]` - Matches prompt against skills
3. `inject_skill_context(skill: Skill)` - Adds skill instructions to agent context

### Files to Create/Modify
- `skills/pr-review/SKILL.md` (new)
- `mini_coding_agent.py` (modify: add skill discovery, matching, and integration logic)
- `tests/test_skills.py` (new)

## Testing
- Test skill discovery with various folder structures
- Test skill matching with different prompt types
- Test integration with agent loop to ensure skills are injected correctly

## Dependencies
- No new external dependencies required
- Use existing Python standard library for file operations and text processing
