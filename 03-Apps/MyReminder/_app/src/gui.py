"""GUI for managing reminders using tkinter."""
import json
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, Callable

from .models import (
    EmailTemplateRef,
    Notification,
    Reminder,
    ReminderActions,
    Schedule,
)
from .config_loader import load_reminders, save_reminders

# Theme colors
DARK_THEME = {
    "bg": "#1e1e2e",
    "fg": "#cdd6f4",
    "accent": "#89b4fa",
    "surface": "#313244",
    "border": "#45475a",
    "muted": "#a6adc8",
    "select_bg": "#45475a",
    "select_fg": "#cdd6f4",
}

LIGHT_THEME = {
    "bg": "#ffffff",
    "fg": "#1e1e2e",
    "accent": "#1a73e8",
    "surface": "#f5f5f5",
    "border": "#e0e0e0",
    "muted": "#666666",
    "select_bg": "#1a73e8",
    "select_fg": "#ffffff",
}


class ReminderEditorDialog(tk.Toplevel):
    """Dialog for creating or editing a single reminder."""

    def __init__(
        self,
        parent: tk.Tk,
        reminder: Optional[Reminder] = None,
        on_save: Optional[Callable] = None,
    ):
        super().__init__(parent)
        self.result: Optional[Reminder] = None
        self._on_save = on_save
        self._editing = reminder

        self.title("Edit Reminder" if reminder else "New Reminder")
        self.geometry("520x720")
        self.resizable(False, True)
        self.minsize(520, 620)
        self.grab_set()

        self._build_ui(reminder)
        self._apply_editor_theme()
        self.protocol("WM_DELETE_WINDOW", self._on_cancel)

    def _apply_editor_theme(self):
        """Apply the current theme to this editor dialog."""
        from .config_loader import load_settings
        settings = load_settings()
        theme_name = settings.get("theme", "dark")
        colors = DARK_THEME if theme_name == "dark" else LIGHT_THEME

        self.configure(bg=colors["bg"])

        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("TFrame", background=colors["bg"])
        style.configure("TLabel", background=colors["bg"], foreground=colors["fg"])
        style.configure("TButton", background=colors["surface"], foreground=colors["fg"])
        style.configure("TCheckbutton", background=colors["bg"], foreground=colors["fg"])
        style.configure("TSeparator", background=colors["border"])
        style.configure("TSpinbox", fieldbackground=colors["surface"], foreground=colors["fg"])
        style.configure("TCombobox",
                        fieldbackground=colors["surface"],
                        background=colors["surface"],
                        foreground=colors["fg"])

    def _build_ui(self, r: Optional[Reminder]):
        pad = {"padx": 10, "pady": 4}

        # Fixed bottom button bar — always visible
        bottom_bar = ttk.Frame(self, padding=8)
        bottom_bar.pack(side="bottom", fill="x")
        ttk.Button(bottom_bar, text="Save", command=self._on_save_click).pack(
            side="left", padx=8
        )
        ttk.Button(bottom_bar, text="Cancel", command=self._on_cancel).pack(
            side="left", padx=8
        )
        ttk.Separator(self, orient="horizontal").pack(side="bottom", fill="x")

        # Scrollable content area
        frame = ttk.Frame(self, padding=10)
        frame.pack(fill="both", expand=True)

        # --- Basic Info ---
        ttk.Label(frame, text="Reminder Name:", font=("Segoe UI", 9, "bold")).grid(
            row=0, column=0, sticky="w", **pad
        )
        self._name_var = tk.StringVar(value=r.name if r else "")
        ttk.Entry(frame, textvariable=self._name_var, width=45).grid(
            row=0, column=1, columnspan=2, sticky="ew", **pad
        )

        self._enabled_var = tk.BooleanVar(value=r.enabled if r else True)
        ttk.Checkbutton(frame, text="Enabled", variable=self._enabled_var).grid(
            row=1, column=1, sticky="w", **pad
        )

        # --- Schedule ---
        ttk.Separator(frame, orient="horizontal").grid(
            row=2, column=0, columnspan=3, sticky="ew", pady=8
        )
        ttk.Label(frame, text="Schedule", font=("Segoe UI", 10, "bold")).grid(
            row=3, column=0, sticky="w", **pad
        )

        ttk.Label(frame, text="Type:").grid(row=4, column=0, sticky="w", **pad)
        self._type_var = tk.StringVar(value=r.schedule.type if r else "daily")
        type_combo = ttk.Combobox(
            frame,
            textvariable=self._type_var,
            values=["daily", "weekly", "monthly"],
            state="readonly",
            width=15,
        )
        type_combo.grid(row=4, column=1, sticky="w", **pad)
        type_combo.bind("<<ComboboxSelected>>", self._on_type_change)

        ttk.Label(frame, text="Time (HH:MM):").grid(
            row=5, column=0, sticky="w", **pad
        )
        self._time_var = tk.StringVar(value=r.schedule.time if r else "09:00")
        ttk.Entry(frame, textvariable=self._time_var, width=10).grid(
            row=5, column=1, sticky="w", **pad
        )

        # Weekly day picker
        ttk.Label(frame, text="Day of Week:").grid(
            row=6, column=0, sticky="w", **pad
        )
        self._day_var = tk.StringVar(
            value=r.schedule.day if r and r.schedule.day else "monday"
        )
        self._day_combo = ttk.Combobox(
            frame,
            textvariable=self._day_var,
            values=[
                "monday", "tuesday", "wednesday", "thursday",
                "friday", "saturday", "sunday",
            ],
            state="readonly",
            width=15,
        )
        self._day_combo.grid(row=6, column=1, sticky="w", **pad)

        # Monthly day picker
        ttk.Label(frame, text="Day of Month:").grid(
            row=7, column=0, sticky="w", **pad
        )
        self._dom_var = tk.IntVar(
            value=r.schedule.day_of_month if r and r.schedule.day_of_month else 1
        )
        self._dom_spin = ttk.Spinbox(
            frame, from_=1, to=28, textvariable=self._dom_var, width=8
        )
        self._dom_spin.grid(row=7, column=1, sticky="w", **pad)

        self._on_type_change()  # set initial visibility

        # --- Notification ---
        ttk.Separator(frame, orient="horizontal").grid(
            row=8, column=0, columnspan=3, sticky="ew", pady=8
        )
        ttk.Label(frame, text="Notification", font=("Segoe UI", 10, "bold")).grid(
            row=9, column=0, sticky="w", **pad
        )

        ttk.Label(frame, text="Title:").grid(row=10, column=0, sticky="w", **pad)
        self._title_var = tk.StringVar(
            value=r.notification.title if r else ""
        )
        ttk.Entry(frame, textvariable=self._title_var, width=45).grid(
            row=10, column=1, columnspan=2, sticky="ew", **pad
        )

        ttk.Label(frame, text="Message:").grid(row=11, column=0, sticky="w", **pad)
        self._msg_var = tk.StringVar(
            value=r.notification.message if r else ""
        )
        ttk.Entry(frame, textvariable=self._msg_var, width=45).grid(
            row=11, column=1, columnspan=2, sticky="ew", **pad
        )

        # --- Actions ---
        ttk.Separator(frame, orient="horizontal").grid(
            row=12, column=0, columnspan=3, sticky="ew", pady=8
        )
        ttk.Label(frame, text="Actions", font=("Segoe UI", 10, "bold")).grid(
            row=13, column=0, sticky="w", **pad
        )

        # Email template
        ttk.Label(frame, text="Email Folder:").grid(
            row=14, column=0, sticky="w", **pad
        )
        self._email_folder_var = tk.StringVar(
            value=r.actions.email_template.folder
            if r and r.actions.email_template
            else ""
        )
        ttk.Entry(frame, textvariable=self._email_folder_var, width=20).grid(
            row=14, column=1, sticky="w", **pad
        )

        ttk.Label(frame, text="Subject Contains:").grid(
            row=15, column=0, sticky="w", **pad
        )
        self._email_subject_var = tk.StringVar(
            value=r.actions.email_template.subject_contains
            if r and r.actions.email_template
            else ""
        )
        ttk.Entry(frame, textvariable=self._email_subject_var, width=35).grid(
            row=15, column=1, columnspan=2, sticky="ew", **pad
        )

        self._cal_event_var = tk.BooleanVar(
            value=r.actions.create_calendar_event if r else False
        )
        ttk.Checkbutton(
            frame, text="Create calendar event when fired",
            variable=self._cal_event_var,
        ).grid(row=16, column=0, columnspan=3, sticky="w", **pad)

        # --- Files & Folders ---
        ttk.Label(frame, text="Open Files:").grid(
            row=17, column=0, sticky="nw", **pad
        )
        files_frame = ttk.Frame(frame)
        files_frame.grid(row=17, column=1, columnspan=2, sticky="ew", **pad)

        self._files_listbox = tk.Listbox(files_frame, height=3, width=40)
        self._files_listbox.pack(side="left", fill="x", expand=True)
        if r:
            for f in r.actions.open_files:
                self._files_listbox.insert("end", f)

        files_btn_frame = ttk.Frame(files_frame)
        files_btn_frame.pack(side="right", padx=4)
        ttk.Button(files_btn_frame, text="+", width=3, command=self._add_file).pack()
        ttk.Button(
            files_btn_frame, text="-", width=3, command=self._remove_file
        ).pack()

        ttk.Label(frame, text="Open Folders:").grid(
            row=18, column=0, sticky="nw", **pad
        )
        folders_frame = ttk.Frame(frame)
        folders_frame.grid(row=18, column=1, columnspan=2, sticky="ew", **pad)

        self._folders_listbox = tk.Listbox(folders_frame, height=3, width=40)
        self._folders_listbox.pack(side="left", fill="x", expand=True)
        if r:
            for f in r.actions.open_folders:
                self._folders_listbox.insert("end", f)

        folders_btn_frame = ttk.Frame(folders_frame)
        folders_btn_frame.pack(side="right", padx=4)
        ttk.Button(
            folders_btn_frame, text="+", width=3, command=self._add_folder
        ).pack()
        ttk.Button(
            folders_btn_frame, text="-", width=3, command=self._remove_folder
        ).pack()

        # (Save/Cancel buttons are in the fixed bottom bar)

    def _on_type_change(self, event=None):
        stype = self._type_var.get()
        if stype == "weekly":
            self._day_combo.configure(state="readonly")
            self._dom_spin.configure(state="disabled")
        elif stype == "monthly":
            self._day_combo.configure(state="disabled")
            self._dom_spin.configure(state="normal")
        else:
            self._day_combo.configure(state="disabled")
            self._dom_spin.configure(state="disabled")

    def _add_file(self):
        path = filedialog.askopenfilename(parent=self)
        if path:
            self._files_listbox.insert("end", path)

    def _remove_file(self):
        sel = self._files_listbox.curselection()
        if sel:
            self._files_listbox.delete(sel[0])

    def _add_folder(self):
        path = filedialog.askdirectory(parent=self)
        if path:
            self._folders_listbox.insert("end", path)

    def _remove_folder(self):
        sel = self._folders_listbox.curselection()
        if sel:
            self._folders_listbox.delete(sel[0])

    def _on_cancel(self):
        self.result = None
        self.destroy()

    def _on_save_click(self):
        name = self._name_var.get().strip()
        if not name:
            messagebox.showwarning("Missing Name", "Please enter a reminder name.", parent=self)
            return

        time_str = self._time_var.get().strip()
        if not time_str or ":" not in time_str:
            messagebox.showwarning("Invalid Time", "Enter time as HH:MM.", parent=self)
            return

        # Build ID from name if new
        rid = self._editing.id if self._editing else name.lower().replace(" ", "-")

        stype = self._type_var.get()
        schedule = Schedule(
            type=stype,
            time=time_str,
            day=self._day_var.get() if stype == "weekly" else None,
            day_of_month=self._dom_var.get() if stype == "monthly" else None,
        )

        email_folder = self._email_folder_var.get().strip()
        email_subject = self._email_subject_var.get().strip()
        email_template = None
        if email_folder or email_subject:
            email_template = EmailTemplateRef(
                folder=email_folder or "drafts",
                subject_contains=email_subject,
            )

        open_files = list(self._files_listbox.get(0, "end"))
        open_folders = list(self._folders_listbox.get(0, "end"))

        self.result = Reminder(
            id=rid,
            name=name,
            enabled=self._enabled_var.get(),
            schedule=schedule,
            notification=Notification(
                title=self._title_var.get().strip() or name,
                message=self._msg_var.get().strip(),
            ),
            actions=ReminderActions(
                email_template=email_template,
                open_files=open_files,
                open_folders=open_folders,
                create_calendar_event=self._cal_event_var.get(),
            ),
        )
        if self._on_save:
            self._on_save(self.result)
        self.destroy()


class ReminderManagerWindow(tk.Tk):
    """Main window showing all reminders with add/edit/delete."""

    def __init__(self, on_reload: Optional[Callable] = None):
        super().__init__()
        self._on_reload = on_reload
        self._current_theme = "dark"
        self.title("MyReminder")
        self.geometry("650x420")
        self.minsize(550, 350)

        self._reminders: list[Reminder] = []
        self._build_ui()
        self._refresh_list()

        # Apply saved theme
        theme = self._load_theme_preference()
        self._apply_theme(theme)
        btn_text = "☀️ Light" if theme == "dark" else "🌙 Dark"
        self._theme_btn.configure(text=btn_text)

    def _load_theme_preference(self) -> str:
        """Load theme from settings.json. Returns 'dark' or 'light'."""
        from .config_loader import load_settings
        settings = load_settings()
        return settings.get("theme", "dark")

    def _save_theme_preference(self, theme: str):
        """Save theme preference to settings.json."""
        from .config_loader import get_settings_path
        path = get_settings_path()
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                settings = json.load(f)
        else:
            settings = {}
        settings["theme"] = theme
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)

    def _apply_theme(self, theme_name: str):
        """Apply dark or light theme to the window."""
        colors = DARK_THEME if theme_name == "dark" else LIGHT_THEME
        self._current_theme = theme_name

        style = ttk.Style(self)
        style.theme_use("clam")

        self.configure(bg=colors["bg"])

        style.configure("TFrame", background=colors["bg"])
        style.configure("TLabel", background=colors["bg"], foreground=colors["fg"])
        style.configure("TButton", background=colors["surface"], foreground=colors["fg"])
        style.configure("TCheckbutton", background=colors["bg"], foreground=colors["fg"])
        style.configure("Treeview",
                        background=colors["surface"],
                        foreground=colors["fg"],
                        fieldbackground=colors["surface"])
        style.configure("Treeview.Heading",
                        background=colors["border"],
                        foreground=colors["fg"])
        style.map("Treeview",
                  background=[("selected", colors["select_bg"])],
                  foreground=[("selected", colors["select_fg"])])
        style.configure("TCombobox",
                        fieldbackground=colors["surface"],
                        background=colors["surface"],
                        foreground=colors["fg"])
        style.configure("TSeparator", background=colors["border"])

        # Update status bar
        if hasattr(self, "_status_label"):
            self._status_label.configure(background=colors["surface"], foreground=colors["muted"])

    def _toggle_theme(self):
        """Toggle between dark and light theme."""
        new_theme = "light" if self._current_theme == "dark" else "dark"
        self._apply_theme(new_theme)
        self._save_theme_preference(new_theme)
        btn_text = "☀️ Light" if new_theme == "dark" else "🌙 Dark"
        self._theme_btn.configure(text=btn_text)

    def _build_ui(self):
        style = ttk.Style(self)
        style.theme_use("clam")

        # Toolbar
        toolbar = ttk.Frame(self, padding=6)
        toolbar.pack(fill="x")

        ttk.Button(toolbar, text="+ New Reminder", command=self._on_add).pack(
            side="left", padx=4
        )
        ttk.Button(toolbar, text="Edit", command=self._on_edit).pack(
            side="left", padx=4
        )
        ttk.Button(toolbar, text="Delete", command=self._on_delete).pack(
            side="left", padx=4
        )
        ttk.Separator(toolbar, orient="vertical").pack(
            side="left", fill="y", padx=8
        )
        ttk.Button(
            toolbar, text="Toggle On/Off", command=self._on_toggle
        ).pack(side="left", padx=4)
        ttk.Button(toolbar, text="Test Fire", command=self._on_test).pack(
            side="left", padx=4
        )

        # Theme toggle button (right side of toolbar)
        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=8)
        self._theme_btn = ttk.Button(toolbar, text="🌙 Dark", command=self._toggle_theme)
        self._theme_btn.pack(side="right", padx=4)

        # Treeview
        columns = ("name", "schedule", "time", "status")
        self._tree = ttk.Treeview(
            self, columns=columns, show="headings", selectmode="browse"
        )
        self._tree.heading("name", text="Name")
        self._tree.heading("schedule", text="Schedule")
        self._tree.heading("time", text="Time")
        self._tree.heading("status", text="Status")

        self._tree.column("name", width=220, minwidth=150)
        self._tree.column("schedule", width=140, minwidth=100)
        self._tree.column("time", width=80, minwidth=60)
        self._tree.column("status", width=80, minwidth=60)

        scrollbar = ttk.Scrollbar(
            self, orient="vertical", command=self._tree.yview
        )
        self._tree.configure(yscrollcommand=scrollbar.set)

        self._tree.pack(side="left", fill="both", expand=True, padx=(6, 0), pady=6)
        scrollbar.pack(side="right", fill="y", pady=6, padx=(0, 6))

        self._tree.bind("<Double-1>", lambda e: self._on_edit())

        # Status bar
        self._status_var = tk.StringVar(value="")
        self._status_label = ttk.Label(self, textvariable=self._status_var, relief="sunken")
        self._status_label.pack(fill="x", side="bottom", ipady=2)

    def _refresh_list(self):
        self._reminders = load_reminders()
        self._tree.delete(*self._tree.get_children())
        for r in self._reminders:
            sched_desc = r.schedule.type.capitalize()
            if r.schedule.type == "weekly" and r.schedule.day:
                sched_desc += f" ({r.schedule.day.capitalize()})"
            elif r.schedule.type == "monthly" and r.schedule.day_of_month:
                sched_desc += f" (Day {r.schedule.day_of_month})"

            status = "Active" if r.enabled else "Disabled"
            self._tree.insert(
                "", "end", iid=r.id,
                values=(r.name, sched_desc, r.schedule.time, status),
            )
        active = sum(1 for r in self._reminders if r.enabled)
        self._status_var.set(
            f"{active} active / {len(self._reminders)} total reminders"
        )

    def _get_selected(self) -> Optional[Reminder]:
        sel = self._tree.selection()
        if not sel:
            messagebox.showinfo("No Selection", "Select a reminder first.")
            return None
        rid = sel[0]
        return next((r for r in self._reminders if r.id == rid), None)

    def _save_and_refresh(self):
        save_reminders(self._reminders)
        self._refresh_list()
        if self._on_reload:
            self._on_reload()

    def _on_add(self):
        def _handle_save(new_reminder: Reminder):
            self._reminders.append(new_reminder)
            self._save_and_refresh()

        ReminderEditorDialog(self, reminder=None, on_save=_handle_save)

    def _on_edit(self):
        r = self._get_selected()
        if not r:
            return

        def _handle_save(updated: Reminder):
            for i, existing in enumerate(self._reminders):
                if existing.id == updated.id:
                    self._reminders[i] = updated
                    break
            self._save_and_refresh()

        ReminderEditorDialog(self, reminder=r, on_save=_handle_save)

    def _on_delete(self):
        r = self._get_selected()
        if not r:
            return
        if messagebox.askyesno(
            "Delete Reminder",
            f"Delete '{r.name}'?",
            parent=self,
        ):
            self._reminders = [x for x in self._reminders if x.id != r.id]
            self._save_and_refresh()

    def _on_toggle(self):
        r = self._get_selected()
        if not r:
            return
        r.enabled = not r.enabled
        self._save_and_refresh()

    def _on_test(self):
        """Fire the selected reminder immediately for testing."""
        r = self._get_selected()
        if not r:
            return
        self._status_var.set(f"Test firing: {r.name}...")
        self.update_idletasks()

        def _do_test():
            try:
                from .notifier import show_toast, execute_actions, set_powershell_fallback
                # Use PowerShell fallback since tkinter is running
                set_powershell_fallback(True)
                show_toast(r)
                execute_actions(r)
                set_powershell_fallback(False)
                # Update status bar from main thread
                self.after(0, lambda: self._status_var.set(f"Test fired: {r.name}"))
            except Exception as e:
                self.after(
                    0,
                    lambda: self._status_var.set(f"Test fire failed: {e}"),
                )

        import threading
        threading.Thread(target=_do_test, daemon=True).start()


def open_manager_window(on_reload: Optional[Callable] = None):
    """Open the reminder manager as a standalone window."""
    win = ReminderManagerWindow(on_reload=on_reload)
    win.mainloop()
