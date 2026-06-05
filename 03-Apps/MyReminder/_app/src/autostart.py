"""Manage Windows startup registration for MyReminder."""
import os
import sys
import logging
from pathlib import Path

logger = logging.getLogger("myreminder")

APP_NAME = "MyReminder"


def _get_startup_folder() -> Path:
    """Get the Windows Startup folder path."""
    return Path(os.environ["APPDATA"]) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup"


def _get_vbs_path() -> Path:
    """Path to the VBS launcher in the startup folder."""
    return _get_startup_folder() / f"{APP_NAME}.vbs"


def _get_run_script() -> str:
    """Get the full path to run.py."""
    return str(Path(__file__).parent.parent / "run.py")


def _get_pyw_launcher() -> str:
    """Get the full path to MyReminder.pyw (the main launcher)."""
    return str(Path(__file__).parent.parent.parent / "MyReminder.pyw")


def is_autostart_enabled() -> bool:
    """Check if MyReminder is set to start with Windows."""
    return _get_vbs_path().exists()


def enable_autostart() -> bool:
    """Add MyReminder to Windows startup."""
    try:
        vbs_path = _get_vbs_path()
        pyw_launcher = _get_pyw_launcher()

        # Use pythonw to launch the .pyw file silently
        python_exe = sys.executable
        pythonw = python_exe.replace("python.exe", "pythonw.exe")
        if os.path.exists(pythonw):
            python_exe = pythonw

        # If .pyw launcher exists, use it (preferred)
        if os.path.exists(pyw_launcher):
            target_script = pyw_launcher
        else:
            # Fallback to run.py
            target_script = _get_run_script()

        vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
WshShell.Run """{python_exe}"" ""{target_script}""", 0, False
'''
        vbs_path.parent.mkdir(parents=True, exist_ok=True)
        vbs_path.write_text(vbs_content, encoding="utf-8")
        logger.info(f"Autostart enabled: {vbs_path}")
        return True
    except Exception as e:
        logger.error(f"Failed to enable autostart: {e}")
        return False


def disable_autostart() -> bool:
    """Remove MyReminder from Windows startup."""
    try:
        vbs_path = _get_vbs_path()
        if vbs_path.exists():
            vbs_path.unlink()
            logger.info("Autostart disabled")
        return True
    except Exception as e:
        logger.error(f"Failed to disable autostart: {e}")
        return False


def toggle_autostart() -> bool:
    """Toggle autostart on/off. Returns new state."""
    if is_autostart_enabled():
        disable_autostart()
        return False
    else:
        enable_autostart()
        return True
