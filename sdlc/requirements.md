# Requirements Specification: mini_coding_agent.py

## 1. Introduction
### 1.1 Purpose
This document defines the functional and non-functional requirements for `mini_coding_agent.py`, an autonomous coding assistant designed to execute code, manage state, and interact with a local development environment.

### 1.2 Scope
The agent will operate within a sandboxed local environment, executing Python scripts via subprocess while maintaining a persistent memory of user commands and project state. It is intended for use by developers requiring rapid prototyping or automated task execution without full IDE overhead.

## 2. User Stories
| ID | User Story | Priority |
|----|------------|----------|
| US-01 | As a developer, I want to issue natural language commands (e.g., "run the script") so that the agent executes the code immediately. | High |
| US-02 | As a developer, I want the agent to remember previous commands and context so I don't have to repeat myself. | Medium |
| US-03 | As a developer, I want to see a list of available skills (tools) so I know what actions the agent can perform. | High |
| US-04 | As a developer, I want to reset the agent's memory and session state so I can start fresh without losing progress elsewhere. | Medium |
| US-05 | As a developer, I want the agent to output clear logs and error messages so I can debug execution failures. | High |

## 3. Functional Requirements
### FR-01: Command Parsing
The agent must parse input strings to identify valid commands from the set defined in `HELP_TEXT`. Invalid commands should trigger an error response.

### FR-02: Skill Execution
The agent must invoke registered skills (from `skills.py`) based on the parsed command. Each skill must be isolated to prevent side effects outside its intended scope.

### FR-03: Memory Management
The agent must maintain a working memory store that persists across sessions, storing key project variables
