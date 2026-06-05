"""Reminder popup window — stays on top until dismissed."""
import tkinter as tk
from tkinter import ttk
import json
import sys
import os
import subprocess
import time
import threading
import logging

logger = logging.getLogger("myreminder")

SNOOZE_OPTIONS = [
    ("5 minutes", 5),
    ("10 minutes", 10),
    ("15 minutes", 15),
    ("30 minutes", 30),
    ("1 hour", 60),
    ("2 hours", 120),
    ("4 hours", 240),
]


class ReminderPopup(tk.Tk):
    """A persistent popup window for a fired reminder."""

    def __init__(self, title: str, message: str, actions: dict):
        super().__init__()
        self._payload_title = title
        self._payload_message = message
        self._payload_actions = actions

        self.wm_title("MyReminder")
        self.attributes("-topmost", True)
        self.resizable(False, False)
        self.configure(bg="#2980b9")

        w, h = 420, 300
        sx = self.winfo_screenwidth() // 2 - w // 2
        sy = self.winfo_screenheight() // 2 - h // 2
        self.geometry(f"{w}x{h}+{sx}+{sy}")

        self.protocol("WM_DELETE_WINDOW", self._dismiss)
        self._build_ui(title, message, actions)
        self.bell()

    def _build_ui(self, title: str, message: str, actions: dict):
        # Header
        header = tk.Frame(self, bg="#2980b9", padx=16, pady=12)
        header.pack(fill="x")
        tk.Label(
            header,
            text="\U0001f514  REMINDER",
            font=("Segoe UI", 10),
            fg="white",
            bg="#2980b9",
        ).pack(anchor="w")
        tk.Label(
            header,
            text=title,
            font=("Segoe UI", 14, "bold"),
            fg="white",
            bg="#2980b9",
            wraplength=380,
        ).pack(anchor="w", pady=(4, 0))

        # Body
        body = tk.Frame(self, bg="white", padx=16, pady=12)
        body.pack(fill="both", expand=True)

        tk.Label(
            body,
            text=message,
            font=("Segoe UI", 10),
            fg="#333",
            bg="white",
            wraplength=380,
            justify="left",
        ).pack(anchor="w")

        # Linked items info
        info_parts = []
        if actions.get("emailTemplate"):
            tmpl = actions["emailTemplate"]
            info_parts.append(
                f"\U0001f4e7 Email: {tmpl.get('folder', '')} / "
                f"{tmpl.get('subjectContains', '')}"
            )
        if actions.get("openFiles"):
            info_parts.append(
                f"\U0001f4c4 {len(actions['openFiles'])} file(s) to open"
            )
        if actions.get("openFolders"):
            info_parts.append(
                f"\U0001f4c1 {len(actions['openFolders'])} folder(s) to open"
            )
        if actions.get("createCalendarEvent"):
            info_parts.append("\U0001f4c5 Calendar event will be created")

        if info_parts:
            tk.Label(
                body,
                text="\n".join(info_parts),
                font=("Segoe UI", 9),
                fg="#666",
                bg="white",
                wraplength=380,
                justify="left",
            ).pack(anchor="w", pady=(8, 0))

        # --- Snooze row ---
        snooze_frame = tk.Frame(body, bg="white")
        snooze_frame.pack(pady=(10, 0), fill="x")

        tk.Label(
            snooze_frame,
            text="Snooze for:",
            font=("Segoe UI", 9),
            fg="#333",
            bg="white",
        ).pack(side="left")

        self._snooze_var = tk.StringVar(value=SNOOZE_OPTIONS[2][0])  # default 15 min
        snooze_combo = ttk.Combobox(
            snooze_frame,
            textvariable=self._snooze_var,
            values=[label for label, _ in SNOOZE_OPTIONS],
            state="readonly",
            width=14,
        )
        snooze_combo.pack(side="left", padx=6)

        ttk.Button(
            snooze_frame,
            text="\U0001f4a4 Snooze",
            command=self._snooze,
        ).pack(side="left", padx=4)

        # --- Action buttons ---
        btn_frame = tk.Frame(body, bg="white")
        btn_frame.pack(pady=(10, 0))

        has_links = actions.get("openFiles") or actions.get("openFolders")
        if has_links:
            ttk.Button(
                btn_frame,
                text="Open Linked Items",
                command=lambda: self._open_links(actions),
            ).pack(side="left", padx=4)

        ttk.Button(
            btn_frame,
            text="Dismiss",
            command=self._dismiss,
        ).pack(side="left", padx=4)

    def _open_links(self, actions: dict):
        for f in actions.get("openFiles", []):
            if os.path.exists(f):
                os.startfile(f)
        for f in actions.get("openFolders", []):
            if os.path.exists(f):
                os.startfile(f)

    def _snooze(self):
        """Snooze: close this popup, wait, then re-launch."""
        label = self._snooze_var.get()
        minutes = next(
            (m for lbl, m in SNOOZE_OPTIONS if lbl == label),
            15,
        )
        # Spawn a background thread that waits then re-launches
        payload = json.dumps({
            "title": self._payload_title,
            "message": self._payload_message,
            "actions": self._payload_actions,
        })
        threading.Thread(
            target=_snooze_worker,
            args=(minutes, payload),
            daemon=True,
        ).start()
        self.destroy()

    def _dismiss(self):
        self.destroy()


def _snooze_worker(minutes: int, payload: str) -> None:
    """Wait for the snooze duration then re-launch the popup."""
    logger.info(f"Snoozing for {minutes} minutes...")
    time.sleep(minutes * 60)
    script = os.path.join(os.path.dirname(__file__), os.pardir, "run_popup.py")
    script = os.path.abspath(script)
    try:
        subprocess.Popen(
            [sys.executable, script, payload],
            creationflags=(
                subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            ),
        )
        logger.info(f"Snooze complete — popup re-launched")
    except Exception as e:
        logger.error(f"Failed to re-launch after snooze: {e}")


def show_popup(title: str, message: str, actions: dict) -> None:
    """Show the popup window (blocks until dismissed or snoozed)."""
    app = ReminderPopup(title, message, actions)
    app.mainloop()


def launch_popup_process(title: str, message: str, actions: dict) -> None:
    """Launch the popup as a separate process (non-blocking)."""
    script = os.path.join(os.path.dirname(__file__), os.pardir, "run_popup.py")
    script = os.path.abspath(script)

    payload = json.dumps({
        "title": title,
        "message": message,
        "actions": actions,
    })

    try:
        subprocess.Popen(
            [sys.executable, script, payload],
            creationflags=(
                subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            ),
        )
    except Exception as e:
        logger.error(f"Failed to launch popup: {e}")


def main():
    if len(sys.argv) < 2:
        print("Usage: popup.py <json_payload>")
        sys.exit(1)

    data = json.loads(sys.argv[1])
    show_popup(
        title=data["title"],
        message=data["message"],
        actions=data.get("actions", {}),
    )


if __name__ == "__main__":
    main()
