# Career Tracker

A standalone desktop app for tracking career accomplishments in **STAR format** (Situation, Task, Action, Result). Built for performance reviews, promotion documents, resume updates, and career growth conversations.

Actions you enter are **automatically converted to past tense** — just type what you did in present tense and the engine handles the rest.

---

## First-Time Setup

### 1. Install Python (if not already installed)

Download Python 3.10+ from [python.org](https://www.python.org/downloads/).

During installation, check **"Add Python to PATH"**.

### 2. Install Dependencies

Open a terminal in this folder and run:

```
pip install -r _app/requirements.txt
```

Or if you prefer to install individually:

```
pip install customtkinter python-docx openpyxl
```

---

## How to Launch

**Double-click `Career Tracker.pyw`** — the app opens without a console window.

Alternatively, from a terminal:

```
python "Career Tracker.pyw"
```

---

## Getting Started

When you first open the app, you have two options on the home screen:

| Button | What it does |
|--------|-------------|
| **📂 Continue from File** | Open an existing career document (Word, Excel, Markdown, Text, or JSON) and work on it directly. Changes save back to that file. |
| **📄 Create New** | Create a fresh career tracker file in any supported format. |

If you don't open a file, the app uses a default `config/entries.json` store — this works fine for getting started quickly.

### Supported File Formats

| Format | Open | Save | Notes |
|--------|------|------|-------|
| `.json` | ✅ | ✅ | Native format — full STAR data preserved |
| `.md` | ✅ | ✅ | Markdown with `####` headers and STAR sections |
| `.docx` | ✅ | ✅ | Word document — paragraphs parsed as items |
| `.xlsx` | ✅ | ✅ | Excel — reads/writes with column headers (Title, Status, etc.) |
| `.txt` | ✅ | ✅ | Plain text — one item per line |

**Tip:** If you already have a Word doc or Excel sheet with your accomplishments, just click "Continue from File" and open it. The app will parse your existing items and let you edit them in STAR format going forward.

---

## How to Use

### Creating Entries

1. Click **+ New Entry** on the home screen
2. Fill in the STAR fields:
   - **Title** — Name of the project or accomplishment
   - **Status** — Completed, In Progress, Launched, etc.
   - **Date** — Month and year completed
   - **Situation** — What problem or gap existed?
   - **Task** — What were you responsible for?
   - **Actions** — What you did (one per line, auto-converted to past tense)
   - **Result** — What was the measurable outcome?
3. Click **Save Entry**

### Importing Items

1. Click **Import Items**
2. Choose a mode:
   - **📋 Paste Text** — Paste a list of accomplishments (one per line)
   - **📁 Import from File** — Browse for a `.txt`, `.md`, `.docx`, or `.xlsx` file
3. Review the preview
4. Click **Save All** to create entries for each item

### Viewing & Editing

- Click **View All** to see all entries
- Use the search bar to filter by title
- Click **Details** to expand an entry
- Click **Edit** to modify or **Delete** to remove

### Exporting

1. Click **Export**
2. Choose a format:
   - **Word (.docx)** — Professional document with headings and bullet points
   - **Excel (.xlsx)** — Spreadsheet with one row per entry
   - **Markdown (.md)** — Formatted text grouped by month
   - **Plain Text (.txt)** — Simple text export
3. Click **Export All** and choose where to save

---

## Data Protection

Career Tracker includes a built-in protection system to prevent accidental data loss. Access it via the **🛡️** button in the navigation bar.

| Feature | What it does |
|---------|-------------|
| **File Versioning** | Automatic timestamped backups before edits (last 10 retained) |
| **Entry Locks** | Lock finalized entries to prevent accidental edits or deletion |
| **Audit Trail** | Changelog of all operations (creates, edits, exports, deletes) |

Backups are stored in `config/_versions/` and the changelog in `config/changelog.md`.

---

## Export Formats

| Format | Best For |
|--------|----------|
| Word (.docx) | Sharing with managers, attaching to reviews |
| Excel (.xlsx) | Sorting, filtering, bulk analysis |
| Markdown (.md) | Obsidian, GitHub, documentation |
| Plain Text (.txt) | Email, quick copy-paste |

---

## Companion: Obsidian Tracking Workflow

Career Tracker works great on its own — but if you want a lightweight daily habit for capturing work as it happens, see **`Obsidian Tracking Guide.md`** in this folder.

It describes a simple system: track project tasks in real time using [Obsidian](https://obsidian.md) (free, offline markdown editor), then periodically convert completed projects into polished STAR entries here. The result: you never have to reconstruct what you did from memory.

---

## Data Storage

All data is stored locally — no cloud services, no API keys, no external dependencies at runtime.

- If you open a file with "Continue from File," changes save directly to that file
- If you don't open a file, data lives in `config/entries.json`
- The app remembers your last-opened file and reloads it on next launch

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| App won't launch | Make sure Python 3.10+ is installed and on PATH |
| "No module named customtkinter" | Run `pip install customtkinter` |
| "No module named docx" | Run `pip install python-docx` |
| "No module named openpyxl" | Run `pip install openpyxl` |
| Export fails | Check that the target folder exists and you have write permission |
| Dark mode looks wrong | Try toggling the theme with the 🌙/☀️ button |
| Entries not saving | Check that the target file isn't open in another program |
| "Continue from File" shows 0 entries | The file format may not match expected structure — try `.json` or `.md` |

---

## Project Structure

```
Career Tracker/
├── Career Tracker.pyw       # Double-click launcher
├── README.md                # This file
├── Obsidian Tracking Guide.md  # Optional companion workflow guide
├── _app/
│   ├── requirements.txt     # Python dependencies
│   ├── app.py               # Main application window
│   ├── config.py            # Settings, file I/O, workspace management
│   ├── star_engine.py       # STAR format + past-tense engine
│   ├── importer.py          # Import from paste/file (txt, md, docx, xlsx)
│   ├── exporter.py          # Export to Word/Excel/MD/TXT
│   ├── protection.py        # Data protection stack
│   └── frames/
│       ├── home.py          # Home screen (Continue/Create New + Quick Actions)
│       ├── new_entry.py     # New entry form
│       ├── import_frame.py  # Import interface (paste or file)
│       ├── entries_list.py  # View/edit all entries
│       ├── export_frame.py  # Export options
│       └── protection_frame.py  # Protection settings panel
└── config/
    ├── settings.json        # User preferences (theme, last opened file)
    ├── entries.json         # Default entry store (if no file opened)
    ├── changelog.md         # Audit trail (auto-generated)
    ├── .protection_state.json  # Lock state (auto-generated)
    └── _versions/           # Timestamped backups (auto-generated)
```

---

## Updates

To update Career Tracker, replace the `_app/` folder with the latest version. Your data in `config/` and any external files you've opened are not affected.

If an `update.py` script is included, you can run it to self-update:

```
python update.py
```
