"""Home screen frame for Career Tracker."""
import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path

from config import (
    load_entries, save_entries, MONTH_NAMES, SUPPORTED_FILE_TYPES,
    get_active_file, set_active_file, get_active_file_display, create_new_file,
)


class HomeFrame(ctk.CTkFrame):
    """Home screen with file actions, quick actions, and recent entries."""

    def __init__(self, parent, navigate_callback):
        super().__init__(parent, fg_color="transparent")
        self.navigate = navigate_callback
        self._build_ui()

    def _build_ui(self):
        """Build the home screen layout."""
        # Title section
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.pack(fill="x", padx=20, pady=(25, 5))

        ctk.CTkLabel(
            title_frame,
            text="Career Tracker",
            font=ctk.CTkFont(size=28, weight="bold"),
        ).pack(anchor="w")

        ctk.CTkLabel(
            title_frame,
            text="Track your accomplishments in STAR format for project tracking, reviews, and career growth.",
            font=ctk.CTkFont(size=13),
            text_color=("gray40", "gray60"),
        ).pack(anchor="w", pady=(4, 0))

        # Active file indicator (bold)
        self.file_indicator = ctk.CTkLabel(
            title_frame,
            text="",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("gray50", "gray50"),
        )
        self.file_indicator.pack(anchor="w", pady=(6, 0))

        # Stats
        self.stats_label = ctk.CTkLabel(
            title_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray50"),
        )
        self.stats_label.pack(anchor="w", pady=(2, 0))

        # --- File Actions (Continue / Create New) ---
        file_frame = ctk.CTkFrame(self, fg_color="transparent")
        file_frame.pack(fill="x", padx=20, pady=(15, 5))

        file_buttons_frame = ctk.CTkFrame(file_frame, fg_color="transparent")
        file_buttons_frame.pack(fill="x")

        self.continue_btn = ctk.CTkButton(
            file_buttons_frame,
            text="Continue from File",
            width=140,
            height=42,
            font=ctk.CTkFont(size=13),
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            command=self._open_file,
        )
        self.continue_btn.pack(side="left", padx=(0, 12))

        self.new_btn = ctk.CTkButton(
            file_buttons_frame,
            text="Create New",
            width=140,
            height=42,
            font=ctk.CTkFont(size=13),
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            command=self._create_new,
        )
        self.new_btn.pack(side="left")

        # --- Quick Actions ---
        actions_frame = ctk.CTkFrame(self, fg_color="transparent")
        actions_frame.pack(fill="x", padx=20, pady=(15, 10))

        ctk.CTkLabel(
            actions_frame,
            text="Quick Actions",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(anchor="w", pady=(0, 10))

        buttons_frame = ctk.CTkFrame(actions_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")

        btn_data = [
            ("New Entry", "new_entry", "#2e7d32"),
            ("Import Items", "import", "#1565c0"),
            ("View All", "entries_list", "#6a1b9a"),
            ("Export", "export", "#e65100"),
        ]

        for i, (text, target, color) in enumerate(btn_data):
            btn = ctk.CTkButton(
                buttons_frame,
                text=text,
                width=140,
                height=40,
                font=ctk.CTkFont(size=13),
                fg_color=color,
                hover_color=color,
                command=lambda t=target: self.navigate(t),
            )
            btn.grid(row=0, column=i, padx=(0, 12), pady=5)

        # --- Recent Entries ---
        recent_frame = ctk.CTkFrame(self, fg_color="transparent")
        recent_frame.pack(fill="both", expand=True, padx=20, pady=(15, 20))

        ctk.CTkLabel(
            recent_frame,
            text="Recent Entries",
            font=ctk.CTkFont(size=15, weight="bold"),
        ).pack(anchor="w", pady=(0, 10))

        self.recent_container = ctk.CTkFrame(recent_frame, fg_color="transparent")
        self.recent_container.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    # File Actions
    # ------------------------------------------------------------------

    def _open_file(self):
        """Open an existing career tracker file."""
        filepath = filedialog.askopenfilename(
            title="Open Career Tracker File",
            filetypes=SUPPORTED_FILE_TYPES,
        )

        if not filepath:
            return

        path = Path(filepath)
        if not path.exists():
            messagebox.showerror("Error", f"File not found:\n{filepath}")
            return

        # Set as active file
        set_active_file(path)

        # Verify it loads
        try:
            entries = load_entries()
            count = len(entries)
            messagebox.showinfo(
                "File Opened",
                f"Loaded {count} {'entry' if count == 1 else 'entries'} from:\n{path.name}",
            )
        except Exception as e:
            messagebox.showerror("Error", f"Could not read file:\n{e}")
            set_active_file(None)
            return

        self.refresh()

    def _create_new(self):
        """Create a new career tracker file."""
        filepath = filedialog.asksaveasfilename(
            title="Create New Career Tracker File",
            defaultextension=".json",
            filetypes=SUPPORTED_FILE_TYPES,
            initialfile="my_career_tracker.json",
        )

        if not filepath:
            return

        path = Path(filepath)

        # Confirm overwrite if file exists
        if path.exists():
            confirm = messagebox.askyesno(
                "File Exists",
                f"{path.name} already exists.\nOverwrite with a new empty tracker?",
            )
            if not confirm:
                return

        # Create the file
        success = create_new_file(path)
        if success:
            messagebox.showinfo(
                "Created",
                f"New tracker created:\n{path.name}\n\nReady to add entries.",
            )
            self.refresh()
        else:
            messagebox.showerror("Error", "Could not create file. Check dependencies.")

    # ------------------------------------------------------------------
    # Refresh
    # ------------------------------------------------------------------

    def refresh(self):
        """Refresh the home screen data."""
        entries = load_entries()

        # Update file indicator (bold)
        active = get_active_file()
        if active:
            self.file_indicator.configure(
                text=f"Current File: {active.name}",
                text_color=("gray10", "white"),
            )
        else:
            self.file_indicator.configure(
                text="Current File: Default (config/entries.json)",
                text_color=("gray10", "white"),
            )

        # Update stats
        count = len(entries)
        self.stats_label.configure(
            text=f"{count} {'entry' if count == 1 else 'entries'} tracked"
        )

        # Clear and rebuild recent entries
        for widget in self.recent_container.winfo_children():
            widget.destroy()

        if not entries:
            ctk.CTkLabel(
                self.recent_container,
                text="No entries yet. Click 'New Entry' to get started!",
                font=ctk.CTkFont(size=12),
                text_color=("gray50", "gray50"),
            ).pack(anchor="w", pady=10)
            return

        # Show last 3 entries
        recent = sorted(
            entries, key=lambda e: e.get("created_at", ""), reverse=True
        )[:3]

        for entry in recent:
            self._create_entry_card(entry)

    def _create_entry_card(self, entry: dict):
        """Create a preview card for a recent entry."""
        card = ctk.CTkFrame(self.recent_container, corner_radius=8)
        card.pack(fill="x", pady=(0, 8))

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=12, pady=10)

        # Title row
        title_row = ctk.CTkFrame(inner, fg_color="transparent")
        title_row.pack(fill="x")

        ctk.CTkLabel(
            title_row,
            text=entry.get("title", "Untitled"),
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(side="left")

        # Status badge
        status = entry.get("status", "")
        if status:
            ctk.CTkLabel(
                title_row,
                text=status,
                font=ctk.CTkFont(size=11),
                text_color=("gray50", "gray60"),
            ).pack(side="right")

        # Date
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
                inner,
                text=display_date,
                font=ctk.CTkFont(size=11),
                text_color=("gray50", "gray60"),
            ).pack(anchor="w")

    def on_show(self):
        """Called when this frame becomes visible."""
        self.refresh()
