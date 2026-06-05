# Tool Comparison Matrix

> All tools in this package at a glance — what they do, what they need, and where they fit.

---

## Desktop Apps

| Tool | Purpose | Language | Dependencies | Layer |
|------|---------|----------|--------------|-------|
| **MyReminder** | Scheduled toast notifications with action triggers | Python | pystray, Pillow, windows-toasts, schedule | 3 |
| **DocForge** | Multi-format document converter (MD↔Word↔PDF↔HTML↔TXT) | Python | markdown2, python-docx, weasyprint, beautifulsoup4 | 3 |
| **Career Tracker** | STAR-format accomplishment tracking with import/export | Python | customtkinter, python-docx, openpyxl | 3 |

## Automation Scripts

| Tool | Purpose | Language | Dependencies | Layer |
|------|---------|----------|--------------|-------|
| **sync_project_board.py** | Generate kanban board from Projects.md + Tasks.md | Python | None (stdlib only) | 1 |
| **setup-all.py** | Install all Python dependencies at once | Python | None (stdlib only) | — |
| **verify-setup.py** | Validate environment configuration | Python | None (stdlib only) | — |

## Platforms & Services

| Tool | Purpose | Cost | Required? | Layer |
|------|---------|------|-----------|-------|
| **Obsidian** | Knowledge management and tracking backbone | Free | Yes | 1 |
| **Python 3.10+** | Runtime for all apps and scripts | Free | Yes | All |
| **Git** | Version control | Free | Recommended | All |
| **Espanso** | Text expansion / snippets | Free | Optional | 4 |
| **Kiro** | AI coding assistant with hooks and steering | Free (preview) | Optional | 2 |
| **Node.js** | Required for MCP servers (npx) | Free | Optional (for MCP) | 2 |

## MCP Servers (AI Integration)

| Server | Purpose | Required For | Layer |
|--------|---------|-------------|-------|
| **Obsidian MCP** | AI read/write to Obsidian vault | Vault automation via AI | 2 |
| **Filesystem** | AI file operations in allowed dirs | General file management | 2 |
| **Git** | AI git operations | Automated commits | 2 |
| **Memory** | Persistent AI knowledge graph | Cross-session context | 2 |
| **Sequential Thinking** | Structured problem decomposition | Complex planning | 2 |

## Templates & Reference

| Resource | Format | Count | Layer |
|----------|--------|-------|-------|
| **PMI Templates** | Markdown | 25 templates across 5 phases | 7 |
| **Snippet Library** | YAML (Espanso) | 25+ triggers | 4 |
| **Schedule Templates** | Excel (.xlsx) | 8 templates | 5 |
| **Vault Template** | Markdown + configs | Full starter vault | 1 |
| **Steering Templates** | Markdown | 3 files | 2 |

---

## Dependency Summary

### Required (for core functionality)
- Python 3.10+
- Obsidian

### Recommended (for full experience)
- Git
- Node.js (for MCP servers)
- Espanso (for text expansion)
- Kiro or Claude Desktop (for AI integration)

### Optional (for specific features)
- Tesseract OCR (for DocForge scanned PDF support)
- weasyprint/GTK (for DocForge PDF generation)
- Microsoft Office (for viewing exported .docx/.xlsx files)
