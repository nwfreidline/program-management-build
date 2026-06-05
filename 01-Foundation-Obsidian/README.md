# Layer 1: Obsidian Foundation

> The backbone of the entire system. A local, plain-text knowledge management tool that serves as your single source of truth for all projects, tasks, and career tracking.

---

## What Is Obsidian?

[Obsidian](https://obsidian.md/) is a free, offline-first Markdown editor with:
- Wiki-style linking between notes (`[[note name]]`)
- A plugin ecosystem (kanban boards, calendars, databases, etc.)
- Instant search across thousands of notes
- Full ownership of your data (it's just `.md` files in a folder)

---

## Setup

### 1. Install Obsidian

Download from [obsidian.md](https://obsidian.md/) and install. Free for personal use.

### 2. Open the Vault Template

1. Copy the `Vault-Template/` folder from this section to your preferred location
   - Recommended: `C:\Users\[you]\Documents\PM-Vault\`
   - **Do NOT put it in OneDrive/Dropbox** (sync conflicts with `.obsidian/` folder)
2. Open Obsidian → "Open folder as vault" → select your copied folder
3. Trust the plugins when prompted

### 3. Install Required Community Plugins

Open Settings (⚙️) → Community Plugins → Browse:

| Plugin | Purpose | Required? |
|--------|---------|-----------|
| **Kanban** | Visual board view of Project Board.md | Yes |
| **Calendar** | Day-based navigation | Recommended |
| **Dataview** | Query your notes like a database | Recommended |
| **Templater** | Advanced template insertion | Recommended |
| **Tasks** | Enhanced task queries across vault | Optional |
| **Periodic Notes** | Daily/weekly note generation | Optional |

### 4. Run the Sync Script (First Time)

Open a terminal in the vault's parent folder and run:

```
python sync_project_board.py
```

This generates `Tracking/Project Board.md` from your `Projects.md` and `Tasks.md` files.

---

## Vault Structure

```
PM-Vault/
├── Tracking/
│   ├── Projects.md           ← YOUR MAIN FILE — all projects live here
│   ├── Tasks.md              ← Standalone tasks (not tied to a project)
│   ├── Project Board.md      ← AUTO-GENERATED kanban (don't edit manually)
│   └── To Growth Tracker.md  ← Move completed projects here for career tracking
│
├── Programs/
│   ├── _Template.md          ← Template for recurring program tracking
│   └── (your programs go here)
│
├── Meeting Notes/
│   └── _Template.md          ← Template for meeting notes
│
├── Reference/
│   └── (reference materials, SOPs, contacts)
│
├── Tags/
│   └── Tag-Taxonomy.md       ← Defines your tag structure
│
└── .obsidian/
    ├── plugins/              ← Plugin data (auto-managed)
    └── workspace.json        ← Layout state
```

---

## How to Track Projects

### The Format

Every project in `Projects.md` follows this structure:

```markdown
### In Progress

- [ ] Project Name
	- [ ] >>"C:\path\to\project\folder"
	- [x] Completed task or phase
	- [ ] Pending task
	- [ ] Another pending task
```

**Rules:**
1. First line: Checkbox + project name
2. Second line: Path reference (helps you find the actual files)
3. Subsequent lines: Tasks and phases (check them off as you go)

### Sections

Use three sections to organize:
- `### Backlog` — Ideas and future work
- `### Pending` — Approved but not started
- `### In Progress` — Actively being worked

### Example

```markdown
### In Progress

- [ ] Website Redesign
	- [ ] >>"C:\Projects\website-redesign"
	- [x] Gather requirements from stakeholders
	- [x] Create wireframes
	- [ ] Build prototype
	- [ ] User testing
	- [ ] Launch

- [ ] Vendor Onboarding Process
	- [ ] >>"C:\Projects\vendor-onboarding"
	- [x] Document current process
	- [ ] Identify bottlenecks
	- [ ] Design improved workflow
	- [ ] Pilot with 2 vendors
```

---

## How the Kanban Board Works

The `sync_project_board.py` script reads your `Projects.md` + `Tasks.md` and generates an Obsidian Kanban board with columns:

| Column | How items get here |
|--------|-------------------|
| **To Do** | New items from Backlog/Pending sections |
| **In Progress** | Items from "In Progress" section |
| **On Hold** | Manually moved on the board (preserved across syncs) |
| **Done** | Items with `[x]` at the top level |

**Key behavior:**
- Source files (`Projects.md`, `Tasks.md`) are authoritative for *content*
- The board preserves *column placement* — if you manually move something to "On Hold," it stays there
- Sub-tasks from `Projects.md` appear as card details on the board

### Running the Sync

```bash
python sync_project_board.py
```

Or set it up as an automated hook (see Layer 2: AI Integration).

---

## How to Track Standalone Tasks

`Tasks.md` is for work that isn't part of a larger project:

```markdown
### To Do

- [ ] Schedule Q3 planning meeting
- [ ] Review vendor contract renewals
- [ ] Update team wiki with new procedure

### Done

- [x] Submit expense report
- [x] Complete safety training
```

These appear on the kanban board tagged with `task` to distinguish them from projects.

---

## Growth Tracking Pipeline

When a project is **fully complete** (all sub-tasks checked):

1. Move it from `Projects.md` to `To Growth Tracker.md`
2. The sync script marks it as "Done" on the kanban board
3. Later, import into Career Tracker app (Layer 6) for STAR-format conversion

This creates a permanent record of everything you've delivered — invaluable for performance reviews and promotions.

---

## Tips

- **Keep Projects.md open** — Pin it in Obsidian's left sidebar for quick access
- **Use hotkeys** — `Ctrl+Enter` toggles checkboxes in Obsidian
- **Don't over-structure** — The power is in simplicity. One file, checkboxes, done.
- **Review weekly** — Spend 10 minutes each Friday updating task status
- **Trust the board** — It auto-generates. Don't manually edit `Project Board.md`.

---

## Customizing

### Adding Sections
You can add custom sections to `Projects.md` (e.g., `### Blocked`, `### Waiting on Others`). The sync script places new items in "To Do" by default.

### Changing Board Columns
Edit the column definitions in `sync_project_board.py` if you want different categories.

### Adding Tags
Use Obsidian's `#tag` syntax in your task descriptions for filtering:
```markdown
- [ ] Update vendor contracts #procurement #q3
```
