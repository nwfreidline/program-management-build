# Dependencies

> Full dependency list for the Program Management Build package.

---

## System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10 | Windows 11 |
| **RAM** | 4 GB | 8 GB+ |
| **Storage** | 500 MB | 2 GB (for vault growth) |
| **Python** | 3.10 | 3.12+ |
| **Display** | 1080p | 1440p+ (for side-by-side Obsidian + editor) |

---

## Software Dependencies

### Tier 1: Required

| Software | Version | Purpose | Download |
|----------|---------|---------|----------|
| Python | 3.10+ | Runtime for all apps and scripts | [python.org](https://www.python.org/downloads/) |
| Obsidian | 1.5+ | Knowledge management backbone | [obsidian.md](https://obsidian.md/) |

### Tier 2: Recommended

| Software | Version | Purpose | Download |
|----------|---------|---------|----------|
| Git | Latest | Version control, repo sync | [git-scm.com](https://git-scm.com/) |
| Espanso | 2.2+ | Text expansion engine | [espanso.org](https://espanso.org/) |
| Node.js | 18+ | MCP server runtime (npx) | [nodejs.org](https://nodejs.org/) |

### Tier 3: Optional

| Software | Version | Purpose | Download |
|----------|---------|---------|----------|
| Kiro | Latest | AI coding assistant | [kiro.dev](https://kiro.dev/) |
| Tesseract OCR | 5.0+ | Scanned PDF text extraction | [GitHub](https://github.com/UB-Mannheim/tesseract/wiki) |
| MS Office | 2019+ | View .docx/.xlsx exports | — |
| VS Code | Latest | Alternative IDE for AI integration | [code.visualstudio.com](https://code.visualstudio.com/) |

---

## Python Package Dependencies

### Combined (all apps)

```
# Core GUI
customtkinter>=5.2.0

# Document processing
python-docx>=0.8.11
openpyxl>=3.1.0
markdown2>=2.4.0
beautifulsoup4>=4.12.0

# PDF (optional — DocForge PDF support)
weasyprint>=60.0
pdfplumber>=0.10.0

# Email parsing (optional — DocForge .msg support)
extract-msg>=0.45.0

# Notifications (MyReminder)
pystray>=0.19.0
Pillow>=10.0.0
windows-toasts>=1.0.0
schedule>=1.2.0
```

### Per-App Breakdown

**MyReminder:**
```
pystray>=0.19.0
Pillow>=10.0.0
windows-toasts>=1.0.0
schedule>=1.2.0
```

**DocForge:**
```
markdown2>=2.4.0
python-docx>=0.8.11
weasyprint>=60.0
beautifulsoup4>=4.12.0
extract-msg>=0.45.0
pdfplumber>=0.10.0
```

**Career Tracker:**
```
customtkinter>=5.2.0
python-docx>=0.8.11
openpyxl>=3.1.0
```

**sync_project_board.py:**
```
(no external dependencies — uses Python stdlib only)
```

---

## Obsidian Plugins

### Required

| Plugin | Purpose |
|--------|---------|
| Kanban | Renders Project Board.md as a visual board |

### Recommended

| Plugin | Purpose |
|--------|---------|
| Calendar | Navigate notes by date |
| Dataview | Query notes as a database |
| Templater | Advanced template insertion with variables |
| Tasks | Enhanced task queries across vault |
| Local REST API | Required for AI (MCP) integration |

### Optional

| Plugin | Purpose |
|--------|---------|
| Periodic Notes | Auto-create daily/weekly notes |
| Excalidraw | Visual diagrams within notes |
| Advanced Tables | Better Markdown table editing |
| Style Settings | Theme customization |

---

## Installation Order

For a fresh machine, install in this order:

1. **Python 3.10+** (check "Add to PATH")
2. **Git** (default options)
3. **Obsidian** (create vault from template)
4. **Run `python _scripts/setup-all.py`** (installs all Python packages)
5. **Espanso** (optional, for text expansion)
6. **Node.js** (optional, for MCP servers)
7. **Kiro or Claude Desktop** (optional, for AI)

Total setup time: ~15-30 minutes.
