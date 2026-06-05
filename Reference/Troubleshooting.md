# Troubleshooting

> Common issues and fixes across all layers of the Program Management Build.

---

## Layer 1: Obsidian

| Issue | Cause | Fix |
|-------|-------|-----|
| Vault won't open | Folder path has special characters or is on a network drive | Move vault to a simple local path (e.g., `C:\Users\you\Documents\PM-Vault`) |
| Kanban board shows raw markdown | Kanban plugin not installed or not enabled | Settings → Community Plugins → Browse → install "Kanban" → Enable |
| `sync_project_board.py` errors on run | Python not in PATH, or wrong working directory | Run from the folder containing the script: `cd PM-Vault && python sync_project_board.py` |
| Board doesn't reflect latest changes | Script hasn't been re-run after editing Projects.md | Run `python sync_project_board.py` again, or set up an automation hook |
| "Failed to load plugin" on vault open | Plugin version incompatible with Obsidian version | Update Obsidian (Help → Check for Updates), then update plugins |
| Sync conflicts (OneDrive/Dropbox) | `.obsidian/workspace.json` changes every time you open | Don't put vault in synced cloud folder. Use Git for versioning instead. |
| Links `[[broken]]` show as plain text | Target note doesn't exist yet | Create the note, or check for typos in the link |

---

## Layer 2: AI Integration (Kiro / MCP)

| Issue | Cause | Fix |
|-------|-------|-----|
| MCP server won't start | `npx` or `uvx` not installed | Install Node.js (for npx) from [nodejs.org](https://nodejs.org) or run `pip install uv` (for uvx) |
| Obsidian MCP "connection refused" | Obsidian not running, or Local REST API plugin not enabled | Open Obsidian, ensure Local REST API plugin is enabled in Settings → Community Plugins |
| Obsidian MCP "unauthorized" | Wrong API key in MCP config | Check the key in Obsidian → Settings → Local REST API → copy the key → paste into your MCP config |
| Kiro doesn't read steering files | Files not in `.kiro/steering/` folder | Verify path: workspace root → `.kiro/steering/your-file.md` |
| Hook doesn't trigger | File pattern doesn't match, or hook has a syntax error | Check the `patterns` array uses glob syntax (e.g., `**/*.md`). Validate JSON syntax. |
| "Module not found" for MCP server | Package not downloaded yet | Run the MCP command manually once in terminal to let npx/uvx download it |
| GitHub MCP auth fails | No token or expired token | Create a Personal Access Token at github.com/settings/tokens → set as `GITHUB_TOKEN` env variable |

---

## Layer 3: Desktop Apps (Python)

| Issue | Cause | Fix |
|-------|-------|-----|
| Nothing happens when double-clicking `.pyw` | Python not associated with `.pyw` files | Right-click → "Open with" → Choose Python. Or run from terminal: `python "App Name.pyw"` |
| `python` not recognized | Python not in system PATH | Reinstall Python from [python.org](https://python.org) — check "Add Python to PATH" during install |
| `ModuleNotFoundError: No module named 'customtkinter'` | Dependencies not installed | Run `pip install -r _app\requirements.txt` from the app's folder |
| `ModuleNotFoundError: No module named 'docx'` | Package name mismatch | Run `pip install python-docx` (not `pip install docx`) |
| App opens then immediately closes | Runtime error with no console to show it | Run from terminal: `python "App Name.pyw"` to see the error message |
| App looks blurry on high-DPI display | Windows scaling issue with tkinter | Right-click the `.pyw` → Properties → Compatibility → "Override high DPI scaling" → System (Enhanced) |
| Dark mode looks wrong | System theme conflict | Toggle theme with the 🌙/☀️ button in the app, or edit `config/settings.json` → `"theme": "dark"` |
| Export fails with permission error | Target folder doesn't exist or file is open in another program | Create the target folder first. Close the file in other programs (Excel, Word). |
| "Windows cannot access the specified device" | OneDrive blocking `.pyw` execution | Move the app folder out of OneDrive to a local path. This is why we use `.pyw` not `.bat`. |

### MyReminder Specific

| Issue | Cause | Fix |
|-------|-------|-----|
| No toast notifications appearing | Windows notification permissions | Settings → System → Notifications → ensure Python/MyReminder is allowed |
| Tray icon doesn't appear | `pystray` issue on some Windows builds | Run as administrator, or check if another app is hiding the tray icon |
| Reminders don't fire at the right time | Timezone mismatch in `config/settings.json` | Set `"timezone": "America/Los_Angeles"` (or your timezone) in settings |

### DocForge Specific

| Issue | Cause | Fix |
|-------|-------|-----|
| PDF output blank or missing | `weasyprint` requires GTK libraries on Windows | Install GTK3 runtime: [github.com/nickvdyck/weasyprint-win/releases](https://github.com/nickvdyck/weasyprint-win) or use the `pdfkit` alternative |
| Scanned PDF returns blank text | No OCR engine installed | Install Tesseract OCR from [github.com/UB-Mannheim/tesseract/wiki](https://github.com/UB-Mannheim/tesseract/wiki) |
| Drag-and-drop not working | Windows focus/permission issue | Use the file picker button instead. Drag-and-drop requires the app window to have focus. |

### Career Tracker Specific

| Issue | Cause | Fix |
|-------|-------|-----|
| "Continue from File" shows 0 entries | File format doesn't match expected structure | Try importing as `.json` (native format) or `.md` with `####` headers and STAR sections |
| Past-tense conversion produces odd results | Complex sentence structure confuses the engine | Edit the action text manually after auto-conversion |

---

## Layer 4: SprintType (Text Expansion)

| Issue | Cause | Fix |
|-------|-------|-----|
| Snippets don't expand | Extension not active on the current site | Click the SprintType icon to verify it's enabled. Some sites block extensions in certain fields. |
| Expansion triggers in the middle of typing | Shortcut accidentally typed | Use `//` prefix consistently — two slashes are unlikely to occur in normal typing |
| Import fails | JSON file has syntax errors | Validate your JSON at [jsonlint.com](https://jsonlint.com) before importing |
| Snippets lost after browser update | Extension data was cleared | Re-import from your backup `snippets.json`. Keep backups in this project folder. |
| Multi-line expansion appears as single line | Rich text field handling varies by site | Use `\n` in JSON for newlines. In HTML-heavy fields, try `&nbsp;\n` for visible line breaks. |
| Wrong snippet expands | Case sensitivity — `//DMG` ≠ `//dmg` | SprintType is case-sensitive. Check exact casing of your shortcut. |
| Extension not available in private/incognito | Browser privacy settings | Firefox: `about:addons` → SprintType → "Allow in Private Windows". Chrome: Extensions → SprintType → "Allow in Incognito" |

---

## Layer 5: Maintenance Scheduling

| Issue | Cause | Fix |
|-------|-------|-----|
| Excel formulas show `#REF!` errors | Columns were moved or deleted | Don't rearrange columns — formulas reference specific column letters. Restore from template. |
| Compliance window dates look wrong | Frequency code not matching the buffer table | Check that your frequency code (1M, 3M, 6M, 12M) exactly matches the lookup table |
| 90-Day Outlook is empty | Filter is set to a past date range | Update the "today" reference cell to current date, or remove the date filter |

---

## Layer 7: PMI Templates

| Issue | Cause | Fix |
|-------|-------|-----|
| Tables render broken in Obsidian | Pipe characters not aligned | Ensure each `|` column separator has a space on both sides |
| Template won't convert to Word via DocForge | Complex Markdown table formatting | Simplify tables or export to HTML first, then convert to Word |

---

## General / Environment

| Issue | Cause | Fix |
|-------|-------|-----|
| `pip` not recognized | Python installed without pip, or PATH issue | Run `python -m ensurepip --upgrade` then restart terminal |
| `git` not recognized | Git not installed or not in PATH | Download from [git-scm.com](https://git-scm.com) and install with default options |
| Scripts run in wrong directory | Terminal opened in wrong location | Use `cd "C:\path\to\folder"` first, or right-click the folder → "Open in Terminal" |
| Permission denied on file write | File open in another application | Close the file in Excel/Word/etc. before running scripts that write to it |
| Antivirus blocks `.pyw` execution | Some AV flags Python scripts | Add an exception for your tools folder in your antivirus settings |
| `setup-all.py` fails mid-install | Network issue or package conflict | Run again — pip will skip already-installed packages. For specific failures, install that package individually. |

---

## Getting Help

1. **Check this file first** — most common issues are covered above
2. **Run `python _scripts\verify-setup.py`** — it'll tell you what's missing
3. **Search the error message** — paste the exact error into Google/Stack Overflow
4. **Open an issue** — [github.com/nwfreidline/program-management-build/issues](https://github.com/nwfreidline/program-management-build/issues)
