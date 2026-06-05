"""MyReminder — Double-click to launch the reminder system tray app."""
import sys
import os

# Hide console window on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Path setup — add _app to path so src/ is importable
_this_dir = os.path.dirname(os.path.abspath(__file__))
_app_dir = os.path.join(_this_dir, "_app")
sys.path.insert(0, _app_dir)

from src.tray import run_tray

if __name__ == "__main__":
    run_tray()
