# Project Tracking in Obsidian

All project work is tracked in the Obsidian vault at `Tracking/Projects.md`. This note is the single source of truth for project status and task progress.

## Projects Note Structure

The note uses three sections: `### Backlog`, `### Pending`, `### In Progress`.

Each project entry follows this format:

```markdown
- [ ] Project Name
	- [ ] >>"C:\path\to\project\folder"
	- [x] Completed task or phase
	- [ ] Pending task or phase
```

### Required Elements

1. **First line:** Checkbox + project name
2. **Second line:** Path reference using `>>"<full path>"` format
3. **Subsequent lines:** Task breakdown (phases, individual tasks, sub-tasks)

### Task Granularity

Tasks should capture the **main steps** taken in building — not every micro-action, but enough to tell the story of what was built:
- Major features or components built
- Key decisions made
- Phases of work (if multi-phase)
- Remaining to-do items

## Tracking Rules

### When Starting a New Project
- Add the project to the appropriate section (Backlog, Pending, or In Progress)
- Include the folder path reference on the second line
- Add initial planned tasks/phases

### During Active Work
- Mark tasks as complete (`[x]`) as they're finished
- Add new tasks as they emerge
- Keep the task list current — it should reflect reality at all times

### When a Project is Complete
- All tasks should be marked `[x]`
- Move the project entry to `Tracking/To Growth Tracker.md`

## Automation

**After every work session that modifies a project:**
1. Update the project's task list in `Tracking/Projects.md` with completed work
2. Add any new tasks discovered during the session
3. Mark completed items with `[x]`
