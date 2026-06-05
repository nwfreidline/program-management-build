# Kiro Remind

A desktop reminder and notification system for Windows with system tray integration, toast notifications, and configurable scheduled actions.

## Features

- **Scheduled reminders** — Daily, weekly, and monthly recurring reminders
- **Windows toast notifications** — Native Windows 10/11 notification popups
- **System tray** — Runs quietly in the background with a tray icon
- **Action triggers** — Reminders can open files, folders, or trigger email templates
- **GUI manager** — Visual interface for creating and managing reminders
- **Grasp integration** — Bridge to Grasp MCP for extended functionality
- **Autostart** — Optional Windows startup registration

## Quick Start

```bash
pip install -r requirements.txt
python run.py
```

Or use the batch launcher:
```
start.bat
```

## Usage

| Entry Point | Description |
|-------------|-------------|
| `run.py` | Start the tray icon + scheduler (background mode) |
| `run_gui.py` | Open the reminder management GUI |
| `run_popup.py` | Show a standalone notification popup |
| `start.bat` | Windows launcher script |
| `start.vbs` | Silent launcher (no console window) |

## Configuration

Reminders are defined in `config/reminders.json`:

```json
{
  "id": "standup-reminder",
  "name": "Daily Standup",
  "enabled": true,
  "schedule": {
    "type": "daily",
    "time": "09:45"
  },
  "notification": {
    "title": "Standup",
    "message": "Team standup in 15 minutes"
  },
  "actions": {
    "open_files": [],
    "open_folders": [],
    "create_calendar_event": false
  }
}
```

App settings live in `config/settings.json` (timezone, notification behavior, tray options).

## Dependencies

- `pystray` — System tray icon
- `Pillow` — Icon image handling
- `windows-toasts` — Native Windows toast notifications
- `schedule` — Lightweight job scheduling

## Project Structure

```
kiro-remind/
├── run.py                # Tray + scheduler entry point
├── run_gui.py            # GUI entry point
├── run_popup.py          # Standalone popup test
├── config/
│   ├── settings.json     # App configuration
│   └── reminders.json    # Reminder definitions
├── src/
│   ├── scheduler.py      # Schedule registration and loop
│   ├── notifier.py       # Toast notifications + action execution
│   ├── tray.py           # System tray icon and menu
│   ├── gui.py            # Reminder management GUI
│   ├── popup.py          # Popup notification window
│   ├── models.py         # Data models (Reminder, Schedule, etc.)
│   ├── config_loader.py  # JSON config reader
│   ├── autostart.py      # Windows startup registration
│   └── grasp_bridge.py   # Grasp MCP integration
└── requirements.txt
```
