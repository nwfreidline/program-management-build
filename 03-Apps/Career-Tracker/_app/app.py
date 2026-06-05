"""Career Tracker — Main application window.

Multi-frame navigation app using customtkinter for tracking
career accomplishments in STAR format.
"""
import customtkinter as ctk

from config import APP_TITLE, APP_SIZE, load_settings, save_settings
from frames import (
    HomeFrame,
    NewEntryFrame,
    ImportFrame,
    EntriesListFrame,
    ExportFrame,
    ProtectionFrame,
)


class CareerTrackerApp(ctk.CTk):
    """Main application window with frame-based navigation."""

    def __init__(self):
        super().__init__()

        # Load settings
        self.settings = load_settings()

        # Configure window
        self.title(APP_TITLE)
        self.geometry(APP_SIZE)
        self.minsize(750, 500)

        # Set theme from settings
        theme = self.settings.get("theme", "dark")
        ctk.set_appearance_mode(theme)
        ctk.set_default_color_theme("blue")

        # Layout: nav bar + content + status bar
        self._build_nav()
        self._build_content()
        self._build_status_bar()

        # Show home frame
        self.navigate("home")

    def _build_nav(self):
        """Build the top navigation bar."""
        self.nav_frame = ctk.CTkFrame(self, height=45, corner_radius=0)
        self.nav_frame.pack(fill="x")
        self.nav_frame.pack_propagate(False)

        # App name
        ctk.CTkLabel(
            self.nav_frame,
            text="⚡ Career Tracker",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left", padx=15)

        # Nav buttons
        nav_buttons = [
            ("Home", "home"),
            ("New Entry", "new_entry"),
            ("Import", "import"),
            ("All Entries", "entries_list"),
            ("Export", "export"),
            ("🛡️", "protection"),
        ]

        for text, target in nav_buttons:
            btn = ctk.CTkButton(
                self.nav_frame,
                text=text,
                width=80 if target != "protection" else 35,
                height=30,
                font=ctk.CTkFont(size=12 if target != "protection" else 14),
                fg_color="transparent",
                hover_color=("gray80", "gray30"),
                command=lambda t=target: self.navigate(t),
            )
            btn.pack(side="left", padx=2)

        # Theme toggle (right side)
        self.theme_btn = ctk.CTkButton(
            self.nav_frame,
            text="🌙" if self.settings.get("theme") == "dark" else "☀️",
            width=35,
            height=30,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            hover_color=("gray80", "gray30"),
            command=self._toggle_theme,
        )
        self.theme_btn.pack(side="right", padx=10)

    def _build_content(self):
        """Build the main content area with all frames."""
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.pack(fill="both", expand=True)

        # Create all frames
        self.frames = {}
        self.frames["home"] = HomeFrame(self.content_frame, self.navigate)
        self.frames["new_entry"] = NewEntryFrame(self.content_frame, self.navigate)
        self.frames["import"] = ImportFrame(self.content_frame, self.navigate)
        self.frames["entries_list"] = EntriesListFrame(self.content_frame, self.navigate)
        self.frames["export"] = ExportFrame(self.content_frame, self.navigate)
        self.frames["protection"] = ProtectionFrame(self.content_frame, self.navigate)

        # Place all frames in same position (stacked)
        for frame in self.frames.values():
            frame.place(relx=0, rely=0, relwidth=1, relheight=1)

    def _build_status_bar(self):
        """Build the bottom status bar."""
        self.status_bar = ctk.CTkFrame(self, height=28, corner_radius=0)
        self.status_bar.pack(fill="x", side="bottom")
        self.status_bar.pack_propagate(False)

        self.status_label = ctk.CTkLabel(
            self.status_bar,
            text="Ready",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        )
        self.status_label.pack(side="left", padx=12)

    def navigate(self, target: str, **kwargs):
        """Navigate to a specific frame.

        Args:
            target: Frame name to show (home, new_entry, import, entries_list, export, protection)
            **kwargs: Additional data to pass to the frame (e.g., edit_data for new_entry)
        """
        if target not in self.frames:
            return

        # Raise the target frame
        frame = self.frames[target]
        frame.tkraise()

        # Call on_show if available
        if hasattr(frame, "on_show"):
            frame.on_show()

        # Handle special kwargs
        if target == "new_entry" and "edit_data" in kwargs:
            frame.load_entry_for_edit(kwargs["edit_data"])

        # Update status bar
        status_map = {
            "home": "Home",
            "new_entry": "New Entry",
            "import": "Import Items",
            "entries_list": "All Entries",
            "export": "Export",
            "protection": "Protection Settings",
        }
        self.status_label.configure(text=status_map.get(target, ""))

    def _toggle_theme(self):
        """Toggle between dark and light theme."""
        current = self.settings.get("theme", "dark")
        new_theme = "light" if current == "dark" else "dark"

        self.settings["theme"] = new_theme
        save_settings(self.settings)

        ctk.set_appearance_mode(new_theme)
        self.theme_btn.configure(text="🌙" if new_theme == "dark" else "☀️")


def run():
    """Launch the Career Tracker application."""
    app = CareerTrackerApp()
    app.mainloop()


if __name__ == "__main__":
    run()
