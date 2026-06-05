"""
Master Setup Script — Program Management Build

Installs Python dependencies for all included apps in one command.
Run from the root of this repository:

    python _scripts/setup-all.py

Options:
    --check     Only verify what's installed (don't install anything)
    --app NAME  Install dependencies for a specific app only
"""

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parent.parent
APPS_DIR = ROOT / "03-Apps"

# Map of app names to their requirements files
APP_REQUIREMENTS = {
    "MyReminder": APPS_DIR / "MyReminder" / "_app" / "requirements.txt",
    "DocForge": APPS_DIR / "DocForge" / "_app" / "requirements.txt",
    "Career-Tracker": APPS_DIR / "Career-Tracker" / "_app" / "requirements.txt",
}

# Combined requirements file
COMBINED_REQUIREMENTS = APPS_DIR / "requirements-all.txt"


def check_python():
    """Verify Python version."""
    version = sys.version_info
    if version < (3, 10):
        print(f"✗ Python 3.10+ required. Found: {version.major}.{version.minor}")
        print("  Download from: https://www.python.org/downloads/")
        return False
    print(f"✓ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_pip():
    """Verify pip is available."""
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "--version"],
            capture_output=True, text=True
        )
        if result.returncode == 0:
            pip_version = result.stdout.strip().split()[1]
            print(f"✓ pip {pip_version}")
            return True
    except Exception:
        pass
    print("✗ pip not found. Install Python with pip included.")
    return False


def install_requirements(requirements_file: Path, app_name: str = ""):
    """Install from a requirements.txt file."""
    if not requirements_file.exists():
        print(f"  ⚠ Requirements file not found: {requirements_file}")
        return False

    label = f" ({app_name})" if app_name else ""
    print(f"\n  Installing from {requirements_file.name}{label}...")

    result = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(requirements_file), "-q"],
        capture_output=True, text=True
    )

    if result.returncode == 0:
        print(f"  ✓ Dependencies installed successfully{label}")
        return True
    else:
        print(f"  ✗ Installation failed{label}")
        if result.stderr:
            print(f"    Error: {result.stderr[:200]}")
        return False


def main():
    print("=" * 60)
    print("  Program Management Build — Setup")
    print("=" * 60)
    print()

    # Check prerequisites
    print("Checking prerequisites...")
    if not check_python():
        sys.exit(1)
    if not check_pip():
        sys.exit(1)

    # Parse arguments
    check_only = "--check" in sys.argv
    specific_app = None
    if "--app" in sys.argv:
        idx = sys.argv.index("--app")
        if idx + 1 < len(sys.argv):
            specific_app = sys.argv[idx + 1]

    if check_only:
        print("\n✓ Prerequisites met. Run without --check to install dependencies.")
        sys.exit(0)

    # Install
    print("\n" + "-" * 60)
    print("Installing dependencies...")
    print("-" * 60)

    if specific_app:
        # Install for specific app
        if specific_app in APP_REQUIREMENTS:
            success = install_requirements(APP_REQUIREMENTS[specific_app], specific_app)
        else:
            print(f"  ✗ Unknown app: {specific_app}")
            print(f"  Available: {', '.join(APP_REQUIREMENTS.keys())}")
            sys.exit(1)
    else:
        # Install all via combined requirements
        if COMBINED_REQUIREMENTS.exists():
            success = install_requirements(COMBINED_REQUIREMENTS, "all apps")
        else:
            # Fallback: install per-app
            success = True
            for app_name, req_file in APP_REQUIREMENTS.items():
                if req_file.exists():
                    if not install_requirements(req_file, app_name):
                        success = False

    # Summary
    print("\n" + "=" * 60)
    if success:
        print("  ✓ Setup complete!")
        print()
        print("  Next steps:")
        print("  1. Install Obsidian from https://obsidian.md/")
        print("  2. Open 01-Foundation-Obsidian/Vault-Template/ as a vault")
        print("  3. Double-click any .pyw file in 03-Apps/ to launch an app")
    else:
        print("  ⚠ Setup completed with warnings. Check errors above.")
    print("=" * 60)


if __name__ == "__main__":
    main()
