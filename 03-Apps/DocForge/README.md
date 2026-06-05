# DocForge

A lightweight desktop document converter with a drag-and-drop GUI. Converts between Markdown, Word, PDF, HTML, Email, and Plain Text — with optional template support for styled output.

---

## First-Time Setup

### 1. Make sure Python is installed

Open a terminal (search "cmd" in Start menu) and type:

```
python --version
```

You should see `Python 3.10` or higher. If not, install from https://www.python.org/downloads/ — check "Add Python to PATH" during install.

### 2. Install dependencies

Right-click on the **docforge** folder in File Explorer and select **"Open in Terminal"** (or "Open PowerShell window here"). Then paste this command and press Enter:

```
pip install -r _app\requirements.txt
```

That's it — it downloads the packages DocForge needs. Takes about 1–2 minutes. You only need to do this once (unless an update says otherwise).

> **Tip:** If you don't see "Open in Terminal" when you right-click, you can also:
> 1. Click the address bar at the top of File Explorer (where it shows the folder path)
> 2. Type `cmd` and press Enter — a terminal opens already pointed at this folder
> 3. Paste the command above and press Enter

### 3. (Optional) Install Tesseract OCR

Only needed if you want to convert scanned/image-based PDFs.

Download from: https://github.com/UB-Mannheim/tesseract/wiki

---

## How to Launch

Double-click **docforge.pyw** — the app opens without a console window.

Or from terminal:
```
python docforge.pyw
```

---

## How to Use

1. **Drag and drop** a file onto the app (or click to browse)
2. Select your desired **output format**
3. Optionally select a **template** (for Word/PDF output)
4. Click **Convert**

Output saves alongside the original file (or choose a destination).

---

## Supported Formats

| Format | Read | Write |
|--------|------|-------|
| Markdown (.md) | ✅ | ✅ |
| Word (.docx) | ✅ | ✅ |
| PDF (.pdf) | ✅ | ✅ |
| HTML (.html) | ✅ | ✅ |
| Plain Text (.txt) | ✅ | ✅ |
| Email (.msg/.eml) | ✅ | — |

---

## Templates

Place `.docx` template files in `_app\templates\docx\` to make them available during conversion. Or use the **Create New** button in the app to build one interactively.

---

## Checking for Updates

Run:
```
python update.py
```

This checks the shared folder for a newer version and offers to install it automatically.

---

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `python` not recognized | Python isn't in your PATH. Reinstall with "Add to PATH" checked. |
| `ModuleNotFoundError` | Run `pip install -r _app\requirements.txt` again |
| Drag-and-drop not working | The app still works via the file picker button. |
| Scanned PDF returns blank | Install Tesseract OCR (see setup step 3) |

---

## Questions?

Reach out to Nick.
