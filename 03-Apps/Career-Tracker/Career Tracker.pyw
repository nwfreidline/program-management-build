"""Career Tracker — Double-click to launch."""
import sys
import os

if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

_this_dir = os.path.dirname(os.path.abspath(__file__))
_app_dir = os.path.join(_this_dir, "_app")
sys.path.insert(0, _app_dir)

from app import run

if __name__ == "__main__":
    run()
