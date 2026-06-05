"""System tray application for MyReminder."""
import logging
import os
import sys
import json
import subprocess
from pathlib import Path

import pystray
from PIL import Image, ImageDraw

from .scheduler import start_scheduler_thread, stop_scheduler, reload_reminders
from .config_loader import load_reminders, get_reminders_path, get_settings_path
from .autostart import is_autostart_enabled, toggle_autostart, enable_autostart, disable_autostart

logger = logging.getLogger("myreminder")

# Resolve paths
CONFIG_DIR = Path(__file__).parent.parent.parent / "config"


def _create_icon_image(size: int = 64) -> Image.Image:
    """Create a simple colored icon for the tray."""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    # Blue circle with white bell shape
    draw.ellipse([2, 2, size - 2, size - 2], fill=(41, 128, 185))
    # Simple bell body
    cx, cy = size // 2, size // 2
    draw.ellipse(
        [cx - 12, cy - 14, cx + 12, cy + 6], fill=(255, 255, 255)
    )
    # Bell base
    draw.rectangle(
        [cx - 14, cy + 2, cx + 14, cy + 8], fill=(255, 255, 255)
    )
    # Clapper
    draw.ellipse(
        [cx - 4, cy + 8, cx + 4, cy + 14], fill=(255, 255, 255)
    )
    return img


def _open_manager(icon=None, item=None):
    """Open the GUI reminder manager as a separate process."""
    import subprocess as sp
    run_py = Path(__file__).parent.parent / "run_gui.py"
    try:
        sp.Popen(
            [sys.executable, str(run_py)],
            creationflags=sp.CREATE_NO_WINDOW if sys.platform == "win32" else 0,
        )
    except Exception as e:
        logger.error(f"Failed to open manager: {e}")


def _open_config_file(icon=None, item=None):
    """Open the reminders config in the default editor."""
    os.startfile(str(get_reminders_path()))


def _open_settings_file(icon=None, item=None):
    """Open the settings config in the default editor."""
    os.startfile(str(get_settings_path()))


def _reload_config(icon=None, item=None):
    """Reload reminders from config."""
    count = reload_reminders()
    icon.notify(f"Reloaded {count} active reminders", "MyReminder")


def _show_status(icon=None, item=None):
    """Show current reminder status."""
    reminders = load_reminders()
    active = sum(1 for r in reminders if r.enabled)
    total = len(reminders)
    icon.notify(f"{active} active / {total} total reminders", "MyReminder")


def _open_reminders_folder(icon=None, item=None):
    """Open the config folder in Explorer."""
    os.startfile(str(CONFIG_DIR))


def _toggle_autostart(icon, item):
    """Toggle start with Windows."""
    new_state = toggle_autostart()
    state_str = "enabled" if new_state else "disabled"
    icon.notify(f"Start with Windows: {state_str}", "MyReminder")


def _quit_app(icon, item):
    """Quit the application."""
    stop_scheduler()
    icon.stop()


def build_menu() -> pystray.Menu:
    """Build the system tray context menu."""
    return pystray.Menu(
        pystray.MenuItem("Manage Reminders", _open_manager, default=True),
        pystray.MenuItem("Status", _show_status),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem(
            "Start with Windows",
            _toggle_autostart,
            checked=lambda item: is_autostart_enabled(),
        ),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Edit Reminders JSON", _open_config_file),
        pystray.MenuItem("Edit Settings", _open_settings_file),
        pystray.MenuItem("Open Config Folder", _open_reminders_folder),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Reload Config", _reload_config),
        pystray.Menu.SEPARATOR,
        pystray.MenuItem("Quit", _quit_app),
    )


def _sync_autostart():
    """Sync the Windows startup registration with the settings file."""
    try:
        from .config_loader import load_settings
        settings = load_settings()
        want_autostart = settings.get("tray", {}).get("startWithWindows", False)
        currently_enabled = is_autostart_enabled()
        if want_autostart and not currently_enabled:
            enable_autostart()
            logger.info("Autostart registered (synced from settings)")
        elif not want_autostart and currently_enabled:
            disable_autostart()
            logger.info("Autostart unregistered (synced from settings)")
    except Exception as e:
        logger.warning(f"Failed to sync autostart state: {e}")


def run_tray():
    """Start the tray icon and scheduler."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(
                CONFIG_DIR.parent / "myreminder.log", encoding="utf-8"
            ),
        ],
    )

    logger.info("Starting MyReminder...")
    _sync_autostart()
    start_scheduler_thread()

    icon = pystray.Icon(
        name="MyReminder",
        icon=_create_icon_image(),
        title="MyReminder",
        menu=build_menu(),
    )
    icon.run()
