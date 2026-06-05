"""Protection Settings frame — manage entry locks, view versions, and audit trail."""

from datetime import datetime
from pathlib import Path

import customtkinter as ctk

from config import load_entries
from protection import ProtectionStack


class ProtectionFrame(ctk.CTkFrame):
    """Protection settings panel for managing entry locks, versions, and changelog."""

    def __init__(self, parent, navigate_callback):
        super().__init__(parent, fg_color="transparent")
        self.navigate = navigate_callback
        self.protection = ProtectionStack()

        self._lock_vars = {}
        self._build_ui()

    def _build_ui(self):
        """Build the protection settings layout."""
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header_frame,
            text="🛡️  Protection Settings",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(side="left")

        # Scrollable content
        self.scroll_frame = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # --- Entry Locks Section ---
        self._build_locks_section()

        # --- Versions Section ---
        self._build_versions_section()

        # --- Changelog Section ---
        self._build_changelog_section()

    def _build_locks_section(self):
        """Build the entry locks section."""
        ctk.CTkLabel(
            self.scroll_frame,
            text="Entry Locks",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        ).pack(fill="x", pady=(10, 5))

        ctk.CTkLabel(
            self.scroll_frame,
            text="Locked entries cannot be edited or deleted. Use this to protect finalized entries.",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        self.locks_container = ctk.CTkFrame(self.scroll_frame)
        self.locks_container.pack(fill="x", pady=(0, 15))

    def _build_versions_section(self):
        """Build the file versions section."""
        ctk.CTkLabel(
            self.scroll_frame,
            text="File Versions",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        ).pack(fill="x", pady=(15, 5))

        ctk.CTkLabel(
            self.scroll_frame,
            text="Automatic backups created before edits. Last 10 versions retained.",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        self.versions_container = ctk.CTkFrame(self.scroll_frame)
        self.versions_container.pack(fill="x", pady=(0, 15))

    def _build_changelog_section(self):
        """Build the changelog section."""
        ctk.CTkLabel(
            self.scroll_frame,
            text="Recent Activity",
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
        ).pack(fill="x", pady=(15, 5))

        ctk.CTkLabel(
            self.scroll_frame,
            text="Audit trail of all operations — entries created, edited, exported, and deleted.",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w",
        ).pack(fill="x", pady=(0, 10))

        self.changelog_frame = ctk.CTkFrame(self.scroll_frame)
        self.changelog_frame.pack(fill="x", pady=(0, 20))

        self._changelog_text = ctk.CTkTextbox(
            self.changelog_frame,
            height=180,
            font=ctk.CTkFont(size=11, family="Consolas"),
            state="disabled",
        )
        self._changelog_text.pack(fill="x", padx=10, pady=10)

    # -----------------------------------------------------------------------
    # Entry Locks
    # -----------------------------------------------------------------------

    def _load_locks(self):
        """Load entries and display lock toggles."""
        for widget in self.locks_container.winfo_children():
            widget.destroy()
        self._lock_vars.clear()

        entries = load_entries()
        if not entries:
            ctk.CTkLabel(
                self.locks_container,
                text="No entries yet.",
                font=ctk.CTkFont(size=12),
                text_color=("gray50", "gray60"),
            ).pack(pady=15)
            return

        for entry in entries:
            entry_id = entry.get("id", entry.get("title", ""))
            title = entry.get("title", "Untitled")
            is_locked = self.protection.is_locked(entry_id)

            row = ctk.CTkFrame(self.locks_container, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=3)

            var = ctk.BooleanVar(value=is_locked)
            self._lock_vars[entry_id] = var

            switch = ctk.CTkSwitch(
                row,
                text="",
                variable=var,
                width=40,
                onvalue=True,
                offvalue=False,
                command=lambda eid=entry_id, t=title: self._toggle_lock(eid, t),
            )
            switch.pack(side="left", padx=(0, 8))

            icon = "🔒" if is_locked else "🔓"
            icon_label = ctk.CTkLabel(
                row, text=icon, font=ctk.CTkFont(size=13), width=25,
            )
            icon_label.pack(side="left", padx=(0, 5))

            ctk.CTkLabel(
                row,
                text=title,
                font=ctk.CTkFont(size=12),
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

            status = entry.get("status", "")
            if status:
                ctk.CTkLabel(
                    row,
                    text=status,
                    font=ctk.CTkFont(size=10),
                    text_color=("gray50", "gray60"),
                ).pack(side="right")

    def _toggle_lock(self, entry_id: str, title: str):
        """Toggle lock state for an entry."""
        var = self._lock_vars.get(entry_id)
        if not var:
            return

        if var.get():
            self.protection.lock_entry(entry_id, title)
            self.protection.log_action("Lock", f"Locked entry: {title}")
        else:
            self.protection.unlock_entry(entry_id)
            self.protection.log_action("Unlock", f"Unlocked entry: {title}")

        # Refresh to update icons
        self._load_locks()

    # -----------------------------------------------------------------------
    # Versions
    # -----------------------------------------------------------------------

    def _load_versions(self):
        """Load and display available versions."""
        for widget in self.versions_container.winfo_children():
            widget.destroy()

        versions = self.protection.list_versions()

        if not versions:
            ctk.CTkLabel(
                self.versions_container,
                text="No versions yet — backups are created automatically before edits.",
                font=ctk.CTkFont(size=12),
                text_color=("gray50", "gray60"),
            ).pack(pady=15)
            return

        for v in versions[:8]:
            row = ctk.CTkFrame(self.versions_container, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=2)

            ctk.CTkLabel(
                row,
                text=f"📄 {v['name']}",
                font=ctk.CTkFont(size=11),
                anchor="w",
            ).pack(side="left", fill="x", expand=True)

            ctk.CTkLabel(
                row,
                text=f"{v['size_kb']} KB  •  {v['date']}",
                font=ctk.CTkFont(size=10),
                text_color=("gray50", "gray60"),
            ).pack(side="right")

        if len(versions) > 8:
            ctk.CTkLabel(
                self.versions_container,
                text=f"... and {len(versions) - 8} more",
                font=ctk.CTkFont(size=11),
                text_color=("gray50", "gray60"),
            ).pack(pady=(5, 10))

    # -----------------------------------------------------------------------
    # Changelog
    # -----------------------------------------------------------------------

    def _load_changelog(self):
        """Load and display recent changelog entries."""
        changelog_file = self.protection._changelog_file

        self._changelog_text.configure(state="normal")
        self._changelog_text.delete("1.0", "end")

        if not changelog_file.exists():
            self._changelog_text.insert("1.0", "No activity recorded yet.")
        else:
            content = changelog_file.read_text(encoding="utf-8")
            lines = content.strip().split("\n")
            recent = "\n".join(lines[-40:]) if len(lines) > 40 else content
            self._changelog_text.insert("1.0", recent)

        self._changelog_text.configure(state="disabled")

    # -----------------------------------------------------------------------
    # Lifecycle
    # -----------------------------------------------------------------------

    def on_show(self):
        """Called when this frame becomes visible — refresh all data."""
        self.protection = ProtectionStack()
        self._load_locks()
        self._load_versions()
        self._load_changelog()
