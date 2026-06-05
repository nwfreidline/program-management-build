"""Entry point for MyReminder."""
import sys
import os

# _app/run.py — add _app dir to path so src/ is importable
sys.path.insert(0, os.path.dirname(__file__))

from src.tray import run_tray

if __name__ == "__main__":
    run_tray()
