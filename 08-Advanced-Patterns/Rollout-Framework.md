# Team Rollout Framework

> How to package and distribute your tools to team members as self-contained, installable packages.

---

## Philosophy

Every tool you build should be structured as if it will be shared. Even for personal use, the clean structure makes maintenance easier.

---

## Package Structure

```
<tool-name>/
├── SETUP.md                # Team-facing setup guide (simpler than README)
├── CONTENTS.md             # What's in the folder (file manifest)
├── <Tool Name>.pyw         # Launcher
├── _app/
│   ├── requirements.txt    # Python dependencies
│   ├── update.py           # Self-update checker (injected by build script)
│   ├── VERSION.txt         # Current version (injected by build script)
│   └── <source files>
└── config/
    └── settings.json       # User configuration
```

---

## Distribution: OneDrive Zip Packages

The simplest distribution method for teams without a package registry:

### How It Works
1. You run `build_release.py` → creates a versioned zip
2. Zip goes to a shared OneDrive folder
3. Team members download, extract to a local path, and run
4. Built-in `update.py` checks the shared folder for newer versions

### Folder Layout (Shared OneDrive)
```
Shared Tools/
├── _README - Start Here.md     # What this folder is, how to use it
├── _Changelog.md               # Version history for all tools
├── DocForge/
│   └── DocForge-v1.2.0.zip
├── Career-Tracker/
│   └── Career-Tracker-v1.0.0.zip
└── MyReminder/
    └── MyReminder-v1.1.0.zip
```

---

## Build Script (`build_release.py`)

The build script automates packaging:

```python
"""
Build a release zip for team distribution.

Usage: python build_release.py <project_folder> [--version X.Y.Z]

What it does:
1. Copies the project folder to a temp directory
2. Strips dev/data artifacts (_dev/, _data/, __pycache__/, .git/, .kiro/)
3. Injects VERSION.txt and update.py into _app/
4. Creates a versioned zip file
5. Moves zip to Releases/ folder
"""
```

### What Gets Stripped
- `_dev/` — Development tools and test scripts
- `_data/` — Personal data and outputs
- `__pycache__/` — Python bytecode
- `.git/` — Version control history
- `.obsidian/` — Obsidian workspace state
- `.kiro/` — Kiro configuration
- `.vscode/` — VS Code settings

### What Gets Injected
- `VERSION.txt` — Version string (e.g., "1.2.0")
- `update.py` — Script that checks for newer versions in the shared folder

---

## Update Mechanism

Each package includes `update.py` in the `_app/` folder:

```python
"""
Check for updates by comparing local VERSION.txt to the shared folder.

Usage: python _app/update.py

Behavior:
1. Reads local VERSION.txt
2. Checks shared OneDrive folder for a newer zip
3. If newer version exists: downloads, extracts, replaces _app/ folder
4. User's config/ folder is preserved
"""
```

Team members run `python _app\update.py` whenever they want to check for updates.

---

## Team Prerequisites

Before distributing, ensure your team has:

| Requirement | Install Method |
|-------------|---------------|
| Python 3.10+ | [python.org](https://www.python.org/downloads/) — check "Add to PATH" |
| pip | Included with Python |

For zero-terminal setup, include an `Install Python Packages.bat`:

```batch
@echo off
echo Installing Python packages for all tools...
echo.
pip install -r requirements-all.txt
echo.
echo Done! You can close this window.
pause
```

---

## SETUP.md Template

Each packaged tool should include a SETUP.md with:

```markdown
# [Tool Name] — Setup Guide

## What This Does
[One sentence description]

## Setup (One Time)
1. Extract this folder to `C:\Tools\[tool-name]\` (NOT on OneDrive)
2. Double-click `Install Python Packages.bat`
3. Done!

## How to Run
Double-click `[Tool Name].pyw`

## How to Update
Double-click `_app\update.py` (or run `python _app\update.py`)

## Need Help?
Contact [your name/email]
```

---

## Versioning

Use semantic versioning: `MAJOR.MINOR.PATCH`

| Version Bump | When |
|-------------|------|
| MAJOR (2.0.0) | Breaking changes, redesign |
| MINOR (1.1.0) | New features, non-breaking |
| PATCH (1.0.1) | Bug fixes |

---

## Rollout Checklist

- [ ] Tool is stable and tested on your own machine
- [ ] README/SETUP.md is written for non-technical users
- [ ] All hardcoded paths removed (uses `Path(__file__).parent`)
- [ ] `requirements.txt` is current and complete
- [ ] Build script produces clean zip
- [ ] Install tested on a fresh machine (or colleague's machine)
- [ ] Version and changelog documented
- [ ] Shared folder has the zip + README
- [ ] Team notified of availability
