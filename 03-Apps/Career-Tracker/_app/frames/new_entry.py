"""New Entry frame — guided STAR entry form."""
import customtkinter as ctk
from datetime import datetime

from config import (
    STATUS_OPTIONS,
    MONTH_NAMES,
    PLACEHOLDER_SITUATION,
    PLACEHOLDER_TASK,
    PLACEHOLDER_ACTION,
    PLACEHOLDER_RESULT,
    load_entries,
    save_entries,
)
from star_engine import generate_star_entry


class NewEntryFrame(ctk.CTkFrame):
    """Guided STAR entry form for creating new accomplishment entries."""

    def __init__(self, parent, navigate_callback):
        super().__init__(parent, fg_color="transparent")
        self.navigate = navigate_callback
        self._build_ui()

    def _build_ui(self):
        """Build the new entry form layout."""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="New STAR Entry",
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

        # Scrollable form area
        form_scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        form_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Title
        ctk.CTkLabel(
            form_scroll, text="Title", font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", pady=(10, 2))
        self.title_entry = ctk.CTkEntry(
            form_scroll, placeholder_text="Project or accomplishment name", height=35
        )
        self.title_entry.pack(fill="x", pady=(0, 8))

        # Status and Date row
        row_frame = ctk.CTkFrame(form_scroll, fg_color="transparent")
        row_frame.pack(fill="x", pady=(0, 8))

        # Status
        status_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        status_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ctk.CTkLabel(
            status_frame, text="Status", font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", pady=(0, 2))
        self.status_var = ctk.StringVar(value=STATUS_OPTIONS[0])
        self.status_menu = ctk.CTkOptionMenu(
            status_frame, variable=self.status_var, values=STATUS_OPTIONS, width=180
        )
        self.status_menu.pack(anchor="w")

        # Date (month + year)
        date_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        date_frame.pack(side="left", fill="x", expand=True)

        ctk.CTkLabel(
            date_frame, text="Date Completed", font=ctk.CTkFont(size=12, weight="bold")
        ).pack(anchor="w", pady=(0, 2))

        date_pickers = ctk.CTkFrame(date_frame, fg_color="transparent")
        date_pickers.pack(anchor="w")

        months = MONTH_NAMES[1:]  # Skip empty first element
        current_month = datetime.now().month
        self.month_var = ctk.StringVar(value=months[current_month - 1])
        self.month_menu = ctk.CTkOptionMenu(
            date_pickers, variable=self.month_var, values=months, width=130
        )
        self.month_menu.pack(side="left", padx=(0, 8))

        current_year = datetime.now().year
        years = [str(y) for y in range(current_year - 2, current_year + 2)]
        self.year_var = ctk.StringVar(value=str(current_year))
        self.year_menu = ctk.CTkOptionMenu(
            date_pickers, variable=self.year_var, values=years, width=90
        )
        self.year_menu.pack(side="left")

        # Situation
        ctk.CTkLabel(
            form_scroll,
            text="Situation",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", pady=(10, 2))
        ctk.CTkLabel(
            form_scroll,
            text=PLACEHOLDER_SITUATION,
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        ).pack(anchor="w", pady=(0, 2))
        self.situation_text = ctk.CTkTextbox(form_scroll, height=70)
        self.situation_text.pack(fill="x", pady=(0, 8))

        # Task
        ctk.CTkLabel(
            form_scroll,
            text="Task",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", pady=(5, 2))
        ctk.CTkLabel(
            form_scroll,
            text=PLACEHOLDER_TASK,
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        ).pack(anchor="w", pady=(0, 2))
        self.task_text = ctk.CTkTextbox(form_scroll, height=70)
        self.task_text.pack(fill="x", pady=(0, 8))

        # Actions
        ctk.CTkLabel(
            form_scroll,
            text="Actions (one per line — auto-converted to past tense)",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", pady=(5, 2))
        ctk.CTkLabel(
            form_scroll,
            text=PLACEHOLDER_ACTION,
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        ).pack(anchor="w", pady=(0, 2))
        self.actions_text = ctk.CTkTextbox(form_scroll, height=100)
        self.actions_text.pack(fill="x", pady=(0, 8))

        # Result
        ctk.CTkLabel(
            form_scroll,
            text="Result",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", pady=(5, 2))
        ctk.CTkLabel(
            form_scroll,
            text=PLACEHOLDER_RESULT,
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        ).pack(anchor="w", pady=(0, 2))
        self.result_text = ctk.CTkTextbox(form_scroll, height=70)
        self.result_text.pack(fill="x", pady=(0, 8))

        # Save button
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(0, 15))

        self.save_btn = ctk.CTkButton(
            btn_frame,
            text="Save Entry",
            width=160,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            command=self._save_entry,
        )
        self.save_btn.pack(side="left")

        self.status_msg = ctk.CTkLabel(
            btn_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("#2e7d32", "#a6e3a1"),
        )
        self.status_msg.pack(side="left", padx=15)

    def _save_entry(self):
        """Validate and save the entry."""
        title = self.title_entry.get().strip()
        if not title:
            self.status_msg.configure(text="⚠ Title is required", text_color=("#c62828", "#f38ba8"))
            return

        # Get date
        month_name = self.month_var.get()
        month_num = MONTH_NAMES.index(month_name) if month_name in MONTH_NAMES else 1
        year = self.year_var.get()
        date_completed = f"{year}-{month_num:02d}"

        # Get text fields
        situation = self.situation_text.get("1.0", "end-1c").strip()
        task = self.task_text.get("1.0", "end-1c").strip()
        result = self.result_text.get("1.0", "end-1c").strip()

        # Get actions (split by newline, filter empty)
        actions_raw = self.actions_text.get("1.0", "end-1c").strip()
        actions = [a.strip() for a in actions_raw.split("\n") if a.strip()]

        # Generate entry
        entry = generate_star_entry(
            title=title,
            status=self.status_var.get(),
            situation=situation,
            task=task,
            actions=actions,
            result=result,
            date_completed=date_completed,
        )

        # Save
        entries = load_entries()
        entries.append(entry)
        save_entries(entries)

        # Show confirmation
        self.status_msg.configure(
            text="✓ Entry saved!", text_color=("#2e7d32", "#a6e3a1")
        )

        # Clear form after short delay
        self.after(1500, self._clear_form)

    def _clear_form(self):
        """Clear all form fields."""
        self.title_entry.delete(0, "end")
        self.situation_text.delete("1.0", "end")
        self.task_text.delete("1.0", "end")
        self.actions_text.delete("1.0", "end")
        self.result_text.delete("1.0", "end")
        self.status_var.set(STATUS_OPTIONS[0])
        self.status_msg.configure(text="")

    def on_show(self):
        """Called when this frame becomes visible."""
        self.status_msg.configure(text="")

    def load_entry_for_edit(self, entry: dict):
        """Pre-fill the form with an existing entry for editing."""
        self._clear_form()

        self.title_entry.insert(0, entry.get("title", ""))
        self.status_var.set(entry.get("status", STATUS_OPTIONS[0]))

        # Parse date
        date_str = entry.get("date_completed", "")
        if date_str:
            try:
                parts = date_str.split("-")
                year = parts[0]
                month_num = int(parts[1]) if len(parts) > 1 else 1
                self.year_var.set(year)
                if 1 <= month_num <= 12:
                    self.month_var.set(MONTH_NAMES[month_num])
            except (ValueError, IndexError):
                pass

        # Fill text areas
        if entry.get("situation"):
            self.situation_text.insert("1.0", entry["situation"])
        if entry.get("task"):
            self.task_text.insert("1.0", entry["task"])
        if entry.get("actions"):
            self.actions_text.insert("1.0", "\n".join(entry["actions"]))
        if entry.get("result"):
            self.result_text.insert("1.0", entry["result"])
