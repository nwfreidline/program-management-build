"""
protection.py -- Data Protection for Career Tracker

Provides layered protection against data loss:

    Layer 1: File Versioning
        - Creates timestamped backups before destructive operations
        - Configurable retention policy (default: keep last 10 versions)

    Layer 4: Entry-Level Locks
        - Lock specific entries to prevent edits or deletion
        - Stored in protection state file (not in the entries themselves)

    Layer 5: Change Log / Audit Trail
        - Appends a timestamped entry to changelog for every operation
        - Records what was changed, exported, imported, or deleted

Usage:
    from protection import ProtectionStack

    protection = ProtectionStack()

    # Before modifying entries:
    protection.create_version()

    # Check if an entry is locked:
    if protection.is_locked(entry_id):
        print("Cannot modify -- entry is locked")

    # Lock/unlock:
    protection.lock_entry(entry_id, entry_title)
    protection.unlock_entry(entry_id)

    # Log an action:
    protection.log_action("export", "Exported 5 entries to DOCX")
"""

import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional


class ProtectionStack:
    """Data protection for Career Tracker entries."""

    def __init__(self, max_versions: int = 10):
        self._app_dir = Path(__file__).parent.resolve()
        self._project_dir = self._app_dir.parent
        self._config_dir = self._project_dir / "config"
        self._entries_file = self._config_dir / "entries.json"

        self.max_versions = max_versions

        # Protection state file
        self._state_file = self._config_dir / ".protection_state.json"

        # Changelog file
        self._changelog_file = self._project_dir / "config" / "changelog.md"

        # Versions directory
        self._versions_dir = self._project_dir / "config" / "_versions"

        # Load state
        self._state = self._load_state()

    # -----------------------------------------------------------------------
    # State Management
    # -----------------------------------------------------------------------

    def _load_state(self) -> dict:
        """Load protection state from disk."""
        if self._state_file.exists():
            try:
                return json.loads(self._state_file.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        return {
            "locked_entries": {},
            "version_counter": {},
        }

    def save_state(self) -> None:
        """Persist protection state to disk."""
        self._config_dir.mkdir(parents=True, exist_ok=True)
        self._state_file.write_text(
            json.dumps(self._state, indent=2, default=str),
            encoding="utf-8",
        )

    # -----------------------------------------------------------------------
    # Layer 1: File Versioning
    # -----------------------------------------------------------------------

    def create_version(self, reason: str = "pre-edit") -> Optional[Path]:
        """Create a versioned backup of the entries file before modification.

        Returns the path to the version file, or None if the source doesn't exist.
        """
        if not self._entries_file.exists():
            return None

        self._versions_dir.mkdir(parents=True, exist_ok=True)

        # Build version filename: entries_YYYY-MM-DD_vN.json
        date_str = datetime.now().strftime("%Y-%m-%d")
        counter_key = f"entries_{date_str}"
        current_count = self._state.get("version_counter", {}).get(counter_key, 0)
        next_version = current_count + 1

        version_name = f"entries_{date_str}_v{next_version}.json"
        version_path = self._versions_dir / version_name

        # Copy the file
        shutil.copy2(self._entries_file, version_path)

        # Update counter
        if "version_counter" not in self._state:
            self._state["version_counter"] = {}
        self._state["version_counter"][counter_key] = next_version

        # Enforce retention policy
        self._enforce_retention()

        self.save_state()
        return version_path

    def _enforce_retention(self) -> None:
        """Remove old versions beyond the retention limit."""
        if not self._versions_dir.exists():
            return

        versions = sorted(
            self._versions_dir.glob("entries_*_v*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        for old_version in versions[self.max_versions:]:
            old_version.unlink(missing_ok=True)

    def list_versions(self) -> list[dict]:
        """List all available versions, newest first.

        Returns list of dicts with 'path', 'name', 'size_kb', 'date'.
        """
        if not self._versions_dir.exists():
            return []

        versions = sorted(
            self._versions_dir.glob("entries_*_v*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        result = []
        for v in versions:
            result.append({
                "path": v,
                "name": v.name,
                "size_kb": round(v.stat().st_size / 1024, 1),
                "date": datetime.fromtimestamp(v.stat().st_mtime).strftime("%Y-%m-%d %H:%M"),
            })
        return result

    def restore_version(self, version_path: Path) -> bool:
        """Restore entries from a specific version file.

        Creates a backup of current state before restoring.
        """
        version_path = Path(version_path)
        if not version_path.exists():
            return False

        # Backup current before restoring
        self.create_version(reason="pre-restore")

        # Restore
        shutil.copy2(version_path, self._entries_file)
        self.log_action("Restore", f"Restored entries from {version_path.name}")
        return True

    # -----------------------------------------------------------------------
    # Layer 4: Entry-Level Locks
    # -----------------------------------------------------------------------

    def lock_entry(self, entry_id: str, entry_title: str = "") -> None:
        """Lock an entry to prevent modification or deletion."""
        if "locked_entries" not in self._state:
            self._state["locked_entries"] = {}

        self._state["locked_entries"][entry_id] = {
            "title": entry_title,
            "locked_at": datetime.now().isoformat(),
        }
        self.save_state()

    def unlock_entry(self, entry_id: str) -> None:
        """Unlock a previously locked entry."""
        locked = self._state.get("locked_entries", {})
        if entry_id in locked:
            del locked[entry_id]
            self.save_state()

    def is_locked(self, entry_id: str) -> bool:
        """Check if an entry is locked."""
        return entry_id in self._state.get("locked_entries", {})

    def get_locked_entries(self) -> dict:
        """Get all locked entries."""
        return self._state.get("locked_entries", {})

    # -----------------------------------------------------------------------
    # Layer 5: Change Log / Audit Trail
    # -----------------------------------------------------------------------

    def log_action(self, operation: str, message: str, details: list[str] = None) -> None:
        """Append an entry to the changelog."""
        self._config_dir.mkdir(parents=True, exist_ok=True)

        now = datetime.now().strftime("%Y-%m-%d %H:%M")
        entry_lines = [f"\n## {now} — {operation}\n"]
        entry_lines.append(f"- {message}")

        if details:
            for detail in details:
                entry_lines.append(f"  - {detail}")

        entry_lines.append("")
        entry_text = "\n".join(entry_lines)

        if self._changelog_file.exists():
            existing = self._changelog_file.read_text(encoding="utf-8")
            self._changelog_file.write_text(
                existing + entry_text, encoding="utf-8"
            )
        else:
            header = (
                "# Career Tracker Changelog\n\n"
                "Audit trail of all operations performed in Career Tracker.\n\n"
                "---\n"
            )
            self._changelog_file.write_text(header + entry_text, encoding="utf-8")
