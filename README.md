# Program Management Build

> A complete, exportable program/project/task management methodology and toolkit for Windows.
> Built by a working Program Manager. Battle-tested across 20+ concurrent programs.

---

## What This Is

This repository packages everything you need to run a professional-grade program management operation from a single Windows machine:

- **Obsidian** as the foundational tracking and knowledge management tool
- **AI integration** (Kiro, Claude, or platform of choice) for automation and assistance
- **Desktop apps** for document conversion, reminders, and career tracking
- **Text expansion** for rapid vendor/procurement communications
- **Scheduling tools** for recurring maintenance and program calendars
- **PMI-aligned templates** covering every phase of the project lifecycle
- **Career growth workflow** for tracking accomplishments and building promotion cases

Each layer is independent — adopt one piece or the entire stack.

---

## Quick Start

### Prerequisites

| Requirement | Version | Download |
|-------------|---------|----------|
| Windows | 10 or 11 | — |
| Python | 3.10+ | [python.org](https://www.python.org/downloads/) |
| Obsidian | 1.5+ | [obsidian.md](https://obsidian.md/) |
| Git | Latest | [git-scm.com](https://git-scm.com/) |

### One-Command Setup

After cloning this repo, run:

```
python _scripts\setup-all.py
```

This installs Python dependencies for all included apps. Individual app setup is documented in each section's README.

---

## Structure

```
Program Management Build/
│
├── 01-Foundation-Obsidian/        # The tracking backbone
├── 02-AI-Integration/             # Kiro/Claude/Copilot setup
├── 03-Apps/                       # Desktop tools (Python GUI apps)
├── 04-Snippets-And-Templates/     # Text expansion + document templates
├── 05-Maintenance-Scheduling/     # Recurring work management
├── 06-Career-Growth/              # Accomplishment tracking methodology
├── 07-PMI-Templates/              # PMI/PMBOK-aligned project templates
├── 08-Advanced-Patterns/          # AI agents, automation, team rollout
│
├── Reference/                     # Cross-cutting docs
│   ├── ARCHITECTURE.md            # System architecture + data flows
│   ├── Tool-Comparison-Matrix.md  # All tools at a glance
│   ├── Dependencies.md            # Full dependency list
│   └── Troubleshooting.md         # Common issues
│
├── _scripts/                      # Setup & verification utilities
│   ├── setup-all.py               # Master dependency installer
│   └── verify-setup.py            # Environment verification
│
└── README.md                      # This file
```

---

## Layers (Adopt Incrementally)

### Layer 1: [Obsidian Foundation](01-Foundation-Obsidian/)
The core tracking system. Projects, tasks, kanban board, and growth timeline — all in local Markdown files with automatic sync.

### Layer 2: [AI Integration](02-AI-Integration/)
Connect your tracking system to an AI coding assistant for automated updates, file generation, and workflow orchestration.

### Layer 3: [Desktop Apps](03-Apps/)
Standalone Python tools: document conversion (DocForge), scheduled reminders (MyReminder), and career tracking (Career Tracker).

### Layer 4: [Snippets & Templates](04-Snippets-And-Templates/)
Text expansion shortcuts for rapid communication — vendor codes, procurement templates, approval requests. Plus document templates for recurring deliverables.

### Layer 5: [Maintenance Scheduling](05-Maintenance-Scheduling/)
For managing recurring preventative maintenance, vendor coordination, and compliance-window scheduling. Includes Excel templates and pipeline patterns.

### Layer 6: [Career Growth](06-Career-Growth/)
A methodology for capturing daily work, converting it to STAR-format accomplishments, and building promotion/review documentation over time.

### Layer 7: [PMI Templates](07-PMI-Templates/)
Industry-standard project management templates aligned to the PMBOK Guide. Project charters, risk registers, communication plans, status reports, and more.

### Layer 8: [Advanced Patterns](08-Advanced-Patterns/)
For power users: building domain-specific AI agents, packaging tools for team distribution, MCP server integration, and event-driven automation hooks.

---

## Philosophy

This system is built on three principles:

1. **Local-first.** All data lives on your machine in plain files (Markdown, JSON, Excel). No SaaS lock-in, no subscriptions required for core functionality.

2. **Composable.** Each layer works independently. You don't need AI integration to use the Obsidian tracking, and you don't need Obsidian to use the desktop apps.

3. **Automated where it matters.** Repetitive tracking, status updates, and file generation are automated. Decision-making stays human.

---

## Who This Is For

- Program Managers handling 10+ concurrent workstreams
- Technical PMs who want to integrate AI into their workflow
- Anyone who's been told "you're so organized" and wants to export that system
- PMP candidates looking for a practical template library alongside certification study

---

## License

MIT — use freely, modify as needed, share with your team.

---

## Contributing

Found a bug or want to add a template? Open a PR or issue on [GitHub](https://github.com/nwfreidline/program-management-build).
