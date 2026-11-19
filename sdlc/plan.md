# Plan: Implement Agent Skills Component for mini-coding-agent

## Overview
This plan outlines the implementation of an "agent skills" component that allows the agent to discover, match, and trigger skill folders based on user prompts.

## Steps

### 1. Create Skill Folder Structure
- Create `skills/` directory in the repo root
- Create a sample skill folder `skills/pr-review/` with:
  - `SKILL.md` containing skill description and instructions
  - Optional helper files if needed

### 2. Implement Skill Discovery Function
- Add a function to scan the `skills/` directory for subdirectories
- Each subdirectory represents a skill
- Parse `SKILL.md` from each skill folder to extract:
  - Skill name/title
  - Description
  - Instructions/prompts to use

### 3. Implement Skill Matching Logic
- Create a function that takes a user prompt and matches it against skill descriptions
- Use similarity-based matching (e.g., keyword matching or simple text similarity)
- Return the best-matching skill or None if no match found

### 4. Integrate Skills into Agent Loop
- Modify the agent's main loop to:
  - Call skill discovery at the start of each turn
  - Match the current prompt against discovered skills
  - If a match is found, inject the skill's instructions into the context before processing

### 5. Add Tests
- Write tests for:
  - Skill discovery (ensure all skill folders are found)
  - Skill matching (test with various prompts)
  - Integration with the agent loop (ensure skills are injected correctly)

## Files to Create/Modify
- `skills/pr-review/SKILL.md` (new)
- `mini_coding_agent.py` (modify: add skill discovery, matching, and integration logic)
- `tests/test_skills.py` (new)

## Dependencies
- No new external dependencies required
- Use existing Python standard library for file operations and text processing
