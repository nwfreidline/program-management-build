# Layer 3: Desktop Apps

> Standalone Python GUI tools for document conversion, scheduled reminders, and career tracking. No internet required, no accounts, no API keys.

---

## Overview

| App | What It Does | Key Use Case |
|-----|-------------|--------------|
| **MyReminder** | Scheduled toast notifications with action triggers | Never miss a recurring task |
| **DocForge** | Multi-format document converter (MD↔Word↔PDF↔HTML↔TXT) | Convert deliverables between formats |
| **Career Tracker** | STAR-format accomplishment tracking with import/export | Build your promotion case over time |

---

## Prerequisites (All Apps)

| Requirement | Version | Check |
|-------------|---------|-------|
| Python | 3.10+ | `python --version` |
| pip | Latest | `pip --version` |

### Install All Dependencies at Once

From this folder, run:

```
pip install -r requirements-all.txt
```

Or install per-app from each app's `_app\requirements.txt`.

---

## Quick Start

### MyReminder
```
Double-click: MyReminder\MyReminder.pyw
```
Runs in system tray. Configure reminders in `config/reminders.json`.

### DocForge
```
Double-click: DocForge\docforge.pyw
```
Drag and drop a file, select output format, click Convert.

### Career Tracker
```
Double-click: Career-Tracker\Career Tracker.pyw
```
Create STAR entries, import from files, export to Word/Excel/Markdown.

---

## App Details

Each app folder contains:
- `<App>.pyw` — Double-click launcher (no console window)
- `README.md` — Full setup and usage guide
- `_app/` — Source code and `requirements.txt`
- `config/` — User settings (JSON)

See each app's README for detailed documentation.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| Nothing happens when double-clicking .pyw | Right-click → Open with → Python |
| "Python not recognized" | Reinstall Python with "Add to PATH" checked |
| "No module named X" | Run `pip install -r _app\requirements.txt` in the app folder |
| App opens then immediately closes | Run from terminal (`python <app>.pyw`) to see the error |

---

## Adding Your Own Apps

Follow the project structure standard:

```
My-New-App/
├── My New App.pyw          # Launcher
├── README.md               # Setup + usage
├── _app/
│   ├── requirements.txt
│   ├── app.py              # Main window
│   └── ...
└── config/
    └── settings.json
```

See Layer 8 (Advanced Patterns) for the team distribution framework.
