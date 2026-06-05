# System Architecture

---

## High-Level Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        YOUR DAILY WORKFLOW                                │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐    ┌─────────────┐    ┌──────────────┐    ┌───────────┐ │
│  │ Obsidian │───▶│ Sync Script │───▶│ Kanban Board │    │ Reminders │ │
│  │ Vault    │    │ (Python)    │    │ (auto-gen)   │    │ (Toast)   │ │
│  └──────────┘    └─────────────┘    └──────────────┘    └───────────┘ │
│       │                                                                  │
│       │ Completed items                                                  │
│       ▼                                                                  │
│  ┌──────────────┐    ┌─────────────────┐    ┌──────────────────────┐  │
│  │ Growth       │───▶│ Career Tracker  │───▶│ Export (Word/Excel/  │  │
│  │ Tracker      │    │ App (STAR)      │    │ Markdown)            │  │
│  └──────────────┘    └─────────────────┘    └──────────────────────┘  │
│                                                                          │
│  ┌──────────────┐    ┌─────────────────┐    ┌──────────────────────┐  │
│  │ Snippets    │    │ DocForge        │    │ AI Assistant         │  │
│  │ (Text Exp.) │    │ (Converter)     │    │ (Kiro/Claude)        │  │
│  └──────────────┘    └─────────────────┘    └──────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Component Map

### Layer 1: Foundation (Obsidian)

```
Obsidian Vault/
├── Tracking/
│   ├── Projects.md          ← Single source of truth for all projects
│   ├── Tasks.md             ← Standalone tasks (not tied to a project)
│   ├── Project Board.md     ← Auto-generated Kanban (DO NOT EDIT MANUALLY)
│   └── To Growth Tracker.md ← Completed work → career pipeline
├── Programs/                ← Program-level tracking (recurring work)
├── Tags/                    ← Tag definitions and taxonomy
└── .obsidian/               ← Plugin configs, hotkeys, themes
```

**Data flow:** You edit `Projects.md` and `Tasks.md` → `sync_project_board.py` generates `Project Board.md`

### Layer 2: AI Integration

```
AI Platform (Kiro/Claude/Copilot)
├── Steering Files           ← Rules the AI follows for your workflow
├── Hooks                    ← Event triggers (file edit → action)
├── MCP Servers              ← Tool connections (Obsidian, Git, filesystem)
└── Context                  ← Project knowledge the AI can reference
```

**Data flow:** You work in IDE → AI reads steering rules → AI executes with tools → updates files in vault

### Layer 3: Desktop Apps

```
Each App/
├── <App>.pyw                ← Double-click launcher (no console)
├── _app/                    ← Source code + requirements.txt
├── config/                  ← User settings (JSON)
└── README.md                ← Setup + usage
```

**Apps included:**
| App | Input | Output |
|-----|-------|--------|
| MyReminder | `config/reminders.json` | Windows toast notifications |
| DocForge | Any document file | Converted file (MD↔Word↔PDF↔HTML↔TXT) |
| Career Tracker | Manual entry or import | STAR-format exports (Word/Excel/MD) |

### Layer 4: Snippets

```
Snippet Engine (Espanso/AutoHotKey/SprintType)
├── snippets.json            ← Trigger → expansion mappings
└── SprintType config        ← Engine-specific setup
```

**Data flow:** You type a trigger (e.g., `;appreq`) → expands to full approval request template

### Layer 5: Maintenance Scheduling

```
Schedule Templates/
├── Master Schedule.xlsx     ← All programs, all sites, full year
├── 90-Day Outlook.xlsx      ← Rolling 90-day vendor view
├── Per-Vendor Views/        ← Filtered views for vendor coordination
└── Pipeline Pattern/        ← Documentation for building automated pipelines
```

### Layer 6: Career Growth

```
Career Workflow:
  Daily work → Projects.md (check boxes)
       ↓
  Completed projects → To Growth Tracker.md
       ↓
  Growth Timeline (auto-generated monthly summary)
       ↓
  Career Tracker App (convert to STAR format)
       ↓
  Export to Word/Excel for reviews
```

### Layer 7: PMI Templates

```
07-PMI-Templates/
├── Initiating/              ← Project Charter, Business Case, Stakeholder Register
├── Planning/                ← WBS, Schedule, Risk Register, Comm Plan, RACI
├── Executing/               ← Status Reports, Meeting Minutes, Change Requests
├── Monitoring/              ← Earned Value, Quality Metrics, Issue Log
└── Closing/                 ← Lessons Learned, Closeout Checklist, Final Report
```

### Layer 8: Advanced Patterns

```
For power users:
├── AI Agent Patterns        ← How to build domain-specific automation agents
├── Team Rollout Framework   ← Packaging tools for distribution (build_release.py)
├── MCP Server Setup         ← Connecting AI to external tools
└── Automation Hooks         ← Event-driven file triggers
```

---

## Integration Points

| From | To | Mechanism |
|------|----|-----------|
| Projects.md | Project Board.md | `sync_project_board.py` (Python script, manual or hook-triggered) |
| Projects.md | To Growth Tracker | Manual move when project completes |
| To Growth Tracker | Career Tracker App | Manual import or file open |
| AI Assistant | Obsidian Vault | MCP Server (obsidian-mcp-server) |
| AI Assistant | Local Files | Filesystem MCP or direct file operations |
| Snippets Engine | Any text field | System-wide text expansion |
| MyReminder | Windows | Toast notifications via `windows-toasts` |
| DocForge | Any document | Drag-and-drop conversion |

---

## Technology Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| Knowledge base | Obsidian (Markdown) | Local, fast, extensible, plain text |
| Automation scripts | Python 3.10+ | Universal, readable, rich ecosystem |
| Desktop GUIs | CustomTkinter | Native-looking, dark mode, single dependency |
| Notifications | windows-toasts | Native Windows 10/11 toast API |
| AI integration | MCP (Model Context Protocol) | Standard protocol, multiple AI platform support |
| Text expansion | Espanso / SprintType | Cross-app, configurable, fast |
| Version control | Git | Track changes, share via GitHub |
| Distribution | Zip packages | No installer needed, copy and run |

---

## Minimum Viable Setup

If you only have 30 minutes, install this:

1. **Obsidian** + the vault template from `01-Foundation-Obsidian/`
2. **Python 3.10+** (for the sync script)

That gives you: project tracking, task tracking, auto-generated kanban board, and a growth pipeline. Everything else is additive.
