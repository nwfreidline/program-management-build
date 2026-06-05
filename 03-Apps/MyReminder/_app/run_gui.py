"""Standalone entry point for the MyReminder manager GUI."""
import sys
import os

# _app/run_gui.py — add _app dir to path so src/ is importable
sys.path.insert(0, os.path.dirname(__file__))

from src.gui import open_manager_window

if __name__ == "__main__":
    open_manager_window()
