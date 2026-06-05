"""
Verify Setup — Program Management Build

Checks that all prerequisites and dependencies are properly installed.
Run from the root of this repository:

    python _scripts/verify-setup.py
"""

import sys
import subprocess
import importlib
from pathlib import Path


ROOT = Path(__file__).parent.parent
RESULTS = {"pass": [], "warn": [], "fail": []}


def check(label: str, condition: bool, fix: str = ""):
    """Record a check result."""
    if condition:
        RESULTS["pass"].append(label)
        print(f"  ✓ {label}")
    else:
        RESULTS["fail"].append(label)
        print(f"  ✗ {label}")
        if fix:
            print(f"    Fix: {fix}")


def warn(label: str, message: str):
    """Record a warning."""
    RESULTS["warn"].append(label)
    print(f"  ⚠ {label}: {message}")


def check_python_version():
    """Check Python 3.10+."""
    version = sys.version_info
    check(
        f"Python {version.major}.{version.minor}.{version.micro}",
        version >= (3, 10),
        "Install Python 3.10+ from https://www.python.org/downloads/"
    )


def check_module(module_name: str, pip_name: str = None):
    """Check if a Python module is importable."""
    pip_name = pip_name or module_name
    try:
        importlib.import_module(module_name)
        check(f"Module: {module_name}", True)
    except ImportError:
        check(f"Module: {module_name}", False, f"pip install {pip_name}")


def check_command(command: str, label: str, fix: str):
    """Check if a command is available."""
    try:
        result = subprocess.run(
            command.split(), capture_output=True, text=True, timeout=10
        )
        check(label, result.returncode == 0, fix)
    except (FileNotFoundError, subprocess.TimeoutExpired):
        check(label, False, fix)


def check_directory(path: Path, label: str):
    """Check if a directory exists."""
    check(f"Directory: {label}", path.exists())


def check_file(path: Path, label: str):
    """Check if a file exists."""
    check(f"File: {label}", path.exists())


def main():
    print("=" * 60)
    print("  Program Management Build — Verification")
    print("=" * 60)
    print()

    # Prerequisites
    print("Prerequisites:")
    check_python_version()
    check_command("git --version", "Git", "Install from https://git-scm.com/")

    # Check for Obsidian (not a command-line tool, check for common install path)
    obsidian_path = Path.home() / "AppData" / "Local" / "Obsidian"
    if obsidian_path.exists():
        check("Obsidian installed", True)
    else:
        warn("Obsidian", "Not detected. Install from https://obsidian.md/")

    # Python modules (core apps)
    print("\nPython Packages (Layer 3 Apps):")
    check_module("customtkinter")
    check_module("docx", "python-docx")
    check_module("openpyxl")
    check_module("pystray")
    check_module("PIL", "Pillow")

    # Optional modules
    print("\nPython Packages (Optional):")
    try:
        import markdown2
        check("Module: markdown2", True)
    except ImportError:
        warn("markdown2", "Optional — needed for DocForge MD conversion")

    try:
        import weasyprint
        check("Module: weasyprint", True)
    except ImportError:
        warn("weasyprint", "Optional — needed for DocForge PDF output")

    # Directory structure
    print("\nPackage Structure:")
    check_directory(ROOT / "01-Foundation-Obsidian", "01-Foundation-Obsidian")
    check_directory(ROOT / "02-AI-Integration", "02-AI-Integration")
    check_directory(ROOT / "03-Apps", "03-Apps")
    check_directory(ROOT / "04-Snippets-And-Templates", "04-Snippets-And-Templates")
    check_directory(ROOT / "05-Maintenance-Scheduling", "05-Maintenance-Scheduling")
    check_directory(ROOT / "06-Career-Growth", "06-Career-Growth")
    check_directory(ROOT / "07-PMI-Templates", "07-PMI-Templates")
    check_directory(ROOT / "08-Advanced-Patterns", "08-Advanced-Patterns")

    # Key files
    print("\nKey Files:")
    check_file(ROOT / "README.md", "README.md")
    check_file(ROOT / "PHILOSOPHY.md", "PHILOSOPHY.md")
    check_file(ROOT / "01-Foundation-Obsidian" / "sync_project_board.py", "sync_project_board.py")

    # Summary
    print("\n" + "=" * 60)
    total = len(RESULTS["pass"]) + len(RESULTS["warn"]) + len(RESULTS["fail"])
    print(f"  Results: {len(RESULTS['pass'])} passed, "
          f"{len(RESULTS['warn'])} warnings, "
          f"{len(RESULTS['fail'])} failed")
    print(f"  Total checks: {total}")

    if RESULTS["fail"]:
        print("\n  ⚠ Fix the failed items above before using the tools.")
        sys.exit(1)
    elif RESULTS["warn"]:
        print("\n  ✓ Core setup is good! Warnings are optional components.")
    else:
        print("\n  ✓ Everything looks great! You're ready to go.")
    print("=" * 60)


if __name__ == "__main__":
    main()
