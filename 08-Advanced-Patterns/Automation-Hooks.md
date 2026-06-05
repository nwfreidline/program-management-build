# Automation Hooks

> Event-driven automation: trigger actions automatically when files change, tasks complete, or the AI finishes work.

---

## What Are Hooks?

Hooks are event→action mappings. When something happens (event), something else executes automatically (action).

```
Event (file saved, task done, timer fires)
        ↓
Action (run script, notify AI, send notification)
```

---

## Hook Types

### File-Based Hooks

| Event | Triggers When | Example Use |
|-------|--------------|-------------|
| `fileEdited` | A file is saved | Re-sync kanban board when Projects.md changes |
| `fileCreated` | A new file appears | Auto-format new Markdown files |
| `fileDeleted` | A file is removed | Update tracking when project folder deleted |

### AI Workflow Hooks

| Event | Triggers When | Example Use |
|-------|--------------|-------------|
| `agentStop` | AI finishes a task | Update Obsidian tracking with completed work |
| `promptSubmit` | You send a message to AI | Log interactions for context |
| `preToolUse` | Before AI runs a tool | Validate write operations |
| `postToolUse` | After AI runs a tool | Verify output quality |

### Task Hooks

| Event | Triggers When | Example Use |
|-------|--------------|-------------|
| `preTaskExecution` | Before a spec task starts | Load relevant context |
| `postTaskExecution` | After a spec task completes | Run tests, update docs |

### Manual Hooks

| Event | Triggers When | Example Use |
|-------|--------------|-------------|
| `userTriggered` | You click a button | Run build script, deploy, sync |

---

## Hook Configuration

Hooks are JSON files stored in `.kiro/hooks/`:

```json
{
  "name": "Sync Kanban on Edit",
  "version": "1.0.0",
  "description": "Regenerate Project Board when tracking files change",
  "when": {
    "type": "fileEdited",
    "patterns": ["**/Tracking/Projects.md", "**/Tracking/Tasks.md"]
  },
  "then": {
    "type": "runCommand",
    "command": "python sync_project_board.py"
  }
}
```

---

## Practical Hook Recipes

### 1. Auto-Sync Kanban Board

When you edit Projects.md or Tasks.md, automatically regenerate the kanban board:

```json
{
  "name": "Sync Kanban Board",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["**/Tracking/Projects.md", "**/Tracking/Tasks.md"]
  },
  "then": {
    "type": "runCommand",
    "command": "python sync_project_board.py"
  }
}
```

### 2. Update Tracking After AI Work

When the AI finishes a task, remind it to update your project tracking:

```json
{
  "name": "Update Tracking",
  "version": "1.0.0",
  "when": {
    "type": "agentStop"
  },
  "then": {
    "type": "askAgent",
    "prompt": "Review what was accomplished. If project work was done, update Tracking/Projects.md."
  }
}
```

### 3. Lint on Save

Run a linter when Python files are saved:

```json
{
  "name": "Lint Python",
  "version": "1.0.0",
  "when": {
    "type": "fileEdited",
    "patterns": ["**/*.py"]
  },
  "then": {
    "type": "runCommand",
    "command": "python -m flake8 --max-line-length 120"
  }
}
```

### 4. Run Tests After Task Completion

After a spec task is marked complete, run the test suite:

```json
{
  "name": "Post-Task Tests",
  "version": "1.0.0",
  "when": {
    "type": "postTaskExecution"
  },
  "then": {
    "type": "runCommand",
    "command": "python -m pytest"
  }
}
```

### 5. Safety Gate for Write Operations

Before the AI writes a file, verify it follows coding standards:

```json
{
  "name": "Write Safety Check",
  "version": "1.0.0",
  "when": {
    "type": "preToolUse",
    "toolTypes": ["write"]
  },
  "then": {
    "type": "askAgent",
    "prompt": "Before writing, verify: no hardcoded paths, proper error handling, and consistent style."
  }
}
```

---

## Designing Your Own Hooks

### Questions to Ask
1. **What repetitive action do I take after [event]?** → Automate it
2. **What do I always forget to do?** → Hook it to the triggering event
3. **What should happen before/after AI actions?** → Pre/post hooks

### Best Practices
- Keep hook actions fast (<5 seconds for `runCommand`)
- Use `askAgent` for complex logic, `runCommand` for simple scripts
- Don't chain too many hooks — circular triggers will cause loops
- Test hooks on non-critical files first
- Document your hooks in a central location

---

## Without Kiro

If you're using a different AI platform, you can achieve similar automation with:

| Platform | Equivalent |
|----------|-----------|
| VS Code | Tasks (`tasks.json`) + file watchers |
| Generic | `watchdog` Python library for file monitoring |
| Windows | Task Scheduler for time-based triggers |
| Git | Git hooks (pre-commit, post-commit) |
