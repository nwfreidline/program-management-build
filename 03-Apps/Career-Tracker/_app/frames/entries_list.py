"""Entries List frame — view, search, edit, and delete entries."""
import customtkinter as ctk
from tkinter import messagebox

from config import load_entries, save_entries, MONTH_NAMES


class EntriesListFrame(ctk.CTkFrame):
    """Scrollable list of all entries with search, expand, edit, and delete."""

    def __init__(self, parent, navigate_callback):
        super().__init__(parent, fg_color="transparent")
        self.navigate = navigate_callback
        self._all_entries = []
        self._build_ui()

    def _build_ui(self):
        """Build the entries list layout."""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="All Entries",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(side="left")

        ctk.CTkButton(
            header,
            text="← Back",
            width=80,
            fg_color="transparent",
            border_width=1,
            command=lambda: self.navigate("home"),
        ).pack(side="right")

        # Search bar
        search_frame = ctk.CTkFrame(self, fg_color="transparent")
        search_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search by title...",
            height=35,
            width=300,
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", self._on_search)

        self.count_label = ctk.CTkLabel(
            search_frame,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        )
        self.count_label.pack(side="right")

        # Scrollable entries list
        self.entries_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        self.entries_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 15))

    def _on_search(self, event=None):
        """Filter entries based on search text."""
        query = self.search_entry.get().strip().lower()
        if query:
            filtered = [
                e for e in self._all_entries
                if query in e.get("title", "").lower()
            ]
        else:
            filtered = self._all_entries
        self._render_entries(filtered)

    def _render_entries(self, entries: list):
        """Render the list of entry cards."""
        # Clear existing
        for widget in self.entries_scroll.winfo_children():
            widget.destroy()

        self.count_label.configure(
            text=f"{len(entries)} of {len(self._all_entries)} entries"
        )

        if not entries:
            ctk.CTkLabel(
                self.entries_scroll,
                text="No entries found.",
                font=ctk.CTkFont(size=12),
                text_color=("gray50", "gray60"),
            ).pack(anchor="w", pady=20)
            return

        for entry in entries:
            self._create_entry_card(entry)

    def _create_entry_card(self, entry: dict):
        """Create an expandable card for an entry."""
        card = ctk.CTkFrame(self.entries_scroll, corner_radius=8)
        card.pack(fill="x", pady=(0, 8))

        # Header row (always visible)
        header_row = ctk.CTkFrame(card, fg_color="transparent")
        header_row.pack(fill="x", padx=12, pady=(10, 5))

        # Title
        ctk.CTkLabel(
            header_row,
            text=entry.get("title", "Untitled"),
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
        ).pack(side="left", fill="x", expand=True)

        # Status
        status = entry.get("status", "")
        ctk.CTkLabel(
            header_row,
            text=status,
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        ).pack(side="right", padx=(10, 0))

        # Date row
        date_str = entry.get("date_completed", "")
        if date_str:
            try:
                parts = date_str.split("-")
                month_num = int(parts[1]) if len(parts) > 1 else 0
                month_name = MONTH_NAMES[month_num] if 0 < month_num <= 12 else ""
                display_date = f"{month_name} {parts[0]}"
            except (ValueError, IndexError):
                display_date = date_str

            ctk.CTkLabel(
                card,
                text=f"  {display_date}",
                font=ctk.CTkFont(size=11),
                text_color=("gray50", "gray60"),
            ).pack(anchor="w", padx=12)

        # Detail section (expandable)
        detail_frame = ctk.CTkFrame(card, fg_color="transparent")
        detail_visible = [False]

        def toggle_detail():
            if detail_visible[0]:
                detail_frame.pack_forget()
                expand_btn.configure(text="▸ Details")
                detail_visible[0] = False
            else:
                detail_frame.pack(fill="x", padx=12, pady=(5, 5))
                expand_btn.configure(text="▾ Details")
                detail_visible[0] = True

        # Buttons row
        btn_row = ctk.CTkFrame(card, fg_color="transparent")
        btn_row.pack(fill="x", padx=12, pady=(5, 8))

        expand_btn = ctk.CTkButton(
            btn_row,
            text="▸ Details",
            width=90,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color="transparent",
            border_width=1,
            command=toggle_detail,
        )
        expand_btn.pack(side="left")

        ctk.CTkButton(
            btn_row,
            text="Edit",
            width=60,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color="#1565c0",
            hover_color="#0d47a1",
            command=lambda e=entry: self._edit_entry(e),
        ).pack(side="left", padx=(8, 0))

        ctk.CTkButton(
            btn_row,
            text="Delete",
            width=60,
            height=28,
            font=ctk.CTkFont(size=11),
            fg_color="#c62828",
            hover_color="#b71c1c",
            command=lambda e=entry: self._delete_entry(e),
        ).pack(side="left", padx=(8, 0))

        # Build detail content
        if entry.get("situation"):
            ctk.CTkLabel(
                detail_frame,
                text=f"Situation: {entry['situation']}",
                font=ctk.CTkFont(size=11),
                wraplength=700,
                anchor="w",
                justify="left",
            ).pack(anchor="w", pady=(2, 0))

        if entry.get("task"):
            ctk.CTkLabel(
                detail_frame,
                text=f"Task: {entry['task']}",
                font=ctk.CTkFont(size=11),
                wraplength=700,
                anchor="w",
                justify="left",
            ).pack(anchor="w", pady=(2, 0))

        if entry.get("actions"):
            ctk.CTkLabel(
                detail_frame,
                text="Actions:",
                font=ctk.CTkFont(size=11, weight="bold"),
            ).pack(anchor="w", pady=(4, 0))
            for action in entry["actions"]:
                ctk.CTkLabel(
                    detail_frame,
                    text=f"  • {action}",
                    font=ctk.CTkFont(size=11),
                    wraplength=680,
                    anchor="w",
                    justify="left",
                ).pack(anchor="w")

        if entry.get("result"):
            ctk.CTkLabel(
                detail_frame,
                text=f"Result: {entry['result']}",
                font=ctk.CTkFont(size=11),
                wraplength=700,
                anchor="w",
                justify="left",
            ).pack(anchor="w", pady=(4, 0))

    def _edit_entry(self, entry: dict):
        """Navigate to edit form with entry data pre-filled."""
        # Remove the entry (will be re-saved on edit)
        entries = load_entries()
        entries = [e for e in entries if e.get("id") != entry.get("id")]
        save_entries(entries)

        # Navigate to new entry form with data
        self.navigate("new_entry", edit_data=entry)

    def _delete_entry(self, entry: dict):
        """Delete an entry with confirmation."""
        confirm = messagebox.askyesno(
            "Delete Entry",
            f"Delete '{entry.get('title', 'Untitled')}'?\n\nThis cannot be undone.",
        )
        if confirm:
            entries = load_entries()
            entries = [e for e in entries if e.get("id") != entry.get("id")]
            save_entries(entries)
            self.refresh()

    def refresh(self):
        """Reload entries from disk and re-render."""
        self._all_entries = load_entries()
        # Sort by created_at descending
        self._all_entries.sort(
            key=lambda e: e.get("created_at", ""), reverse=True
        )
        self._on_search()

    def on_show(self):
        """Called when this frame becomes visible."""
        self.search_entry.delete(0, "end")
        self.refresh()
