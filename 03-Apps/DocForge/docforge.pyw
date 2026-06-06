"""
DocForge — Lightweight desktop document converter.
Supports: Markdown, Word (.docx), PDF, HTML, Email (.msg/.eml), Plain Text
With template-aware output.
"""

import os
import sys
import subprocess
import customtkinter as ctk
from tkinter import filedialog, messagebox

# Hide the background console window on Windows
if sys.platform == "win32":
    import ctypes
    ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# Path setup
_this_dir = os.path.dirname(os.path.abspath(__file__))
_app_dir = os.path.join(_this_dir, "_app")
_parent_dir = os.path.dirname(_this_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)
if _app_dir not in sys.path:
    sys.path.insert(0, _app_dir)
if _this_dir not in sys.path:
    sys.path.insert(0, _this_dir)

from converters.engine import (
    convert, detect_format, OUTPUT_FORMATS, OUTPUT_EXTENSIONS, FORMAT_EXTENSIONS
)
from template_creator_ui import TemplateCreatorWindow

TEMPLATES_DIR = os.path.join(_app_dir, "templates")

FORMAT_LABELS = {
    "markdown": "Markdown (.md)",
    "docx": "Word (.docx)",
    "pdf": "PDF (.pdf)",
    "html": "HTML (.html)",
    "txt": "Plain Text (.txt)",
    "eml": "Email (.eml)",
}

TEMPLATE_FORMATS = {"docx", "pdf"}


class DocForgeApp(ctk.CTk):
    """Main DocForge application window."""

    def __init__(self):
        super().__init__()

        # Configure window
        self.title("DocForge")
        self.geometry("960x400")
        self.minsize(900, 360)

        # Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # State
        self.input_path = ""
        self.output_format_var = ctk.StringVar(value="docx")
        self.template_choice_var = ctk.StringVar(value="None")
        self.dest_dir = ""

        os.makedirs(TEMPLATES_DIR, exist_ok=True)

        # Build UI
        self._build_nav()
        self._build_content()
        self._build_status_bar()

    # ------------------------------------------------------------------
    # Navigation Bar
    # ------------------------------------------------------------------

    def _build_nav(self):
        """Build the top navigation bar."""
        self.nav_frame = ctk.CTkFrame(self, height=45, corner_radius=0)
        self.nav_frame.pack(fill="x")
        self.nav_frame.pack_propagate(False)

        ctk.CTkLabel(
            self.nav_frame,
            text="⚡ DocForge",
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(side="left", padx=15)

        # Theme toggle (right side)
        self.theme_btn = ctk.CTkButton(
            self.nav_frame,
            text="🌙",
            width=35,
            height=30,
            font=ctk.CTkFont(size=14),
            fg_color="transparent",
            text_color=("gray20", "gray90"),
            hover_color=("gray80", "gray30"),
            command=self._toggle_theme,
        )
        self.theme_btn.pack(side="right", padx=10)

    # ------------------------------------------------------------------
    # Main Content — Horizontal Pipeline Flow
    # ------------------------------------------------------------------

    def _build_content(self):
        """Build the main content area with horizontal card flow."""
        content = ctk.CTkFrame(self, fg_color="transparent")
        content.pack(fill="both", expand=True)

        # Center the flow vertically and horizontally
        content.grid_rowconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=0)  # title
        content.grid_rowconfigure(2, weight=0)  # flow
        content.grid_rowconfigure(3, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            content,
            text="DocForge",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).grid(row=1, column=0, pady=(0, 20))

        # ── Horizontal flow container using grid rows for alignment ──
        # Row 0: headers (FORMAT, TEMPLATE, DESTINATION)
        # Row 1: main controls (Browse, dropdown, dropdown, Choose, Convert) — all aligned
        # Row 2: sub-labels (No file selected, Word (.docx), Add/Create, Same as input)
        flow = ctk.CTkFrame(content, fg_color="transparent")
        flow.grid(row=2, column=0)

        col = 0

        # ═══ Card 1: Browse ═══
        # Row 0: empty header spacer
        # Row 1: Browse button
        # Row 2: "No file selected"
        ctk.CTkLabel(flow, text="", font=ctk.CTkFont(size=10)).grid(row=0, column=col)

        ctk.CTkButton(
            flow,
            text="Browse",
            width=100,
            height=34,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#1565c0",
            hover_color="#0d47a1",
            command=self._browse_file,
        ).grid(row=1, column=col, padx=(0, 4))

        self.source_label = ctk.CTkLabel(
            flow,
            text="No file selected",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
        )
        self.source_label.grid(row=2, column=col, padx=(0, 4), pady=(4, 0))

        # ═══ Arrow 1 ═══
        col += 1
        ctk.CTkLabel(
            flow, text="→",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("gray70", "gray40"),
        ).grid(row=1, column=col, padx=6)

        # ═══ Card 2: Format ═══
        col += 1
        ctk.CTkLabel(
            flow,
            text="FORMAT",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=("gray40", "gray60"),
        ).grid(row=0, column=col, pady=(0, 6))

        self.format_combo = ctk.CTkComboBox(
            flow,
            values=list(FORMAT_LABELS.keys()),
            variable=self.output_format_var,
            width=120,
            height=34,
            state="readonly",
            command=self._on_format_change,
        )
        self.format_combo.grid(row=1, column=col, padx=4)

        self.format_desc_label = ctk.CTkLabel(
            flow,
            text="Word (.docx)",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
        )
        self.format_desc_label.grid(row=2, column=col, padx=4, pady=(4, 0))

        # ═══ Arrow 2 ═══
        col += 1
        ctk.CTkLabel(
            flow, text="→",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("gray70", "gray40"),
        ).grid(row=1, column=col, padx=6)

        # ═══ Card 3: Template ═══
        col += 1
        ctk.CTkLabel(
            flow,
            text="TEMPLATE",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=("gray40", "gray60"),
        ).grid(row=0, column=col, pady=(0, 6))

        self.template_combo = ctk.CTkComboBox(
            flow,
            values=["None"],
            variable=self.template_choice_var,
            width=190,
            height=34,
            state="readonly",
        )
        self.template_combo.grid(row=1, column=col, padx=4)

        btn_row = ctk.CTkFrame(flow, fg_color="transparent")
        btn_row.grid(row=2, column=col, padx=4, pady=(4, 0))

        ctk.CTkButton(
            btn_row,
            text="Add New",
            width=70,
            height=26,
            font=ctk.CTkFont(size=10),
            fg_color="transparent",
            text_color=("gray20", "gray90"),
            border_width=1,
            hover_color=("gray80", "gray30"),
            command=self._open_templates_dir,
        ).pack(side="left", padx=(0, 4))

        ctk.CTkButton(
            btn_row,
            text="Create New",
            width=80,
            height=26,
            font=ctk.CTkFont(size=10),
            fg_color="transparent",
            text_color=("gray20", "gray90"),
            border_width=1,
            hover_color=("gray80", "gray30"),
            command=self._open_template_creator,
        ).pack(side="left")

        # ═══ Arrow 3 ═══
        col += 1
        ctk.CTkLabel(
            flow, text="→",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("gray70", "gray40"),
        ).grid(row=1, column=col, padx=6)

        # ═══ Card 4: Destination ═══
        col += 1
        ctk.CTkLabel(
            flow,
            text="DESTINATION",
            font=ctk.CTkFont(size=10, weight="bold"),
            text_color=("gray40", "gray60"),
        ).grid(row=0, column=col, pady=(0, 6))

        ctk.CTkButton(
            flow,
            text="Choose",
            width=120,
            height=34,
            font=ctk.CTkFont(size=11),
            fg_color="transparent",
            text_color=("gray20", "gray90"),
            border_width=1,
            hover_color=("gray80", "gray30"),
            command=self._browse_dest,
        ).grid(row=1, column=col, padx=4)

        self.dest_label = ctk.CTkLabel(
            flow,
            text="Same as input",
            font=ctk.CTkFont(size=10),
            text_color=("gray50", "gray60"),
        )
        self.dest_label.grid(row=2, column=col, padx=4, pady=(4, 0))

        # ═══ Arrow 4 ═══
        col += 1
        ctk.CTkLabel(
            flow, text="→",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=("gray70", "gray40"),
        ).grid(row=1, column=col, padx=6)

        # ═══ Card 5: Convert ═══
        col += 1
        ctk.CTkLabel(flow, text="", font=ctk.CTkFont(size=10)).grid(row=0, column=col)

        ctk.CTkButton(
            flow,
            text="Convert",
            width=100,
            height=34,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            command=self._do_convert,
        ).grid(row=1, column=col, padx=(4, 0))

        # Refresh templates on load
        self._refresh_templates()
        self._setup_drag_and_drop()

    # ------------------------------------------------------------------
    # Status Bar
    # ------------------------------------------------------------------

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

    # ------------------------------------------------------------------
    # Theme Toggle
    # ------------------------------------------------------------------

    def _toggle_theme(self):
        """Toggle between dark and light theme."""
        current = ctk.get_appearance_mode().lower()
        new_theme = "light" if current == "dark" else "dark"
        ctk.set_appearance_mode(new_theme)
        self.theme_btn.configure(text="🌙" if new_theme == "dark" else "☀️")

    # ------------------------------------------------------------------
    # Drag and Drop
    # ------------------------------------------------------------------

    def _setup_drag_and_drop(self):
        """Set up drag and drop support if tkinterdnd2 is available."""
        try:
            from tkinterdnd2 import DND_FILES
            self.drop_target_register(DND_FILES)
            self.dnd_bind("<<Drop>>", self._on_drop)
        except Exception:
            pass

    def _on_drop(self, event):
        """Handle dropped file."""
        path = event.data.strip()
        if path.startswith("{") and path.endswith("}"):
            path = path[1:-1]
        if "\n" in path:
            path = path.split("\n")[0].strip()
        self._set_input_file(path)

    # ------------------------------------------------------------------
    # File Selection
    # ------------------------------------------------------------------

    def _browse_file(self):
        """Open file dialog to select input file."""
        filetypes = [
            ("All Supported", "*.md *.markdown *.docx *.pdf *.html *.htm *.txt *.msg *.eml"),
            ("Markdown", "*.md *.markdown"),
            ("Word", "*.docx"),
            ("PDF", "*.pdf"),
            ("HTML", "*.html *.htm"),
            ("Plain Text", "*.txt"),
            ("Email", "*.msg *.eml"),
            ("All Files", "*.*"),
        ]
        path = filedialog.askopenfilename(filetypes=filetypes)
        if path:
            self._set_input_file(path)

    def _set_input_file(self, path):
        """Set the input file and update the UI."""
        if not os.path.isfile(path):
            self.status_label.configure(text="Error: File not found")
            return

        fmt = detect_format(path)
        if not fmt:
            self.status_label.configure(text="Error: Unsupported file type")
            return

        self.input_path = path
        filename = os.path.basename(path)
        display = filename if len(filename) <= 18 else filename[:15] + "..."
        self.source_label.configure(
            text=f"✅ {display}",
            text_color=("gray10", "white"),
        )
        self.status_label.configure(text=f"Loaded: {filename} ({fmt})")

        # Auto-select format
        auto_map = {
            "markdown": "docx", "docx": "markdown", "msg": "docx",
            "eml": "docx", "pdf": "docx", "html": "markdown", "txt": "markdown",
        }
        self.output_format_var.set(auto_map.get(fmt, "docx"))
        self._on_format_change(auto_map.get(fmt, "docx"))

    # ------------------------------------------------------------------
    # Destination
    # ------------------------------------------------------------------

    def _browse_dest(self):
        """Open directory dialog for output destination."""
        directory = filedialog.askdirectory()
        if directory:
            self.dest_dir = directory
            display = os.path.basename(directory) or directory
            self.dest_label.configure(
                text=display,
                text_color=("gray10", "white"),
            )

    # ------------------------------------------------------------------
    # Format / Template
    # ------------------------------------------------------------------

    def _on_format_change(self, choice=None):
        """Handle format selection change."""
        fmt = self.output_format_var.get()
        self.format_desc_label.configure(text=FORMAT_LABELS.get(fmt, fmt))
        self._refresh_templates()

    def _refresh_templates(self):
        """Refresh the template dropdown based on selected format."""
        fmt = self.output_format_var.get()
        templates = ["None"]

        if fmt in TEMPLATE_FORMATS:
            template_fmt = "docx" if fmt == "pdf" else fmt
            fmt_dir = os.path.join(TEMPLATES_DIR, template_fmt)
            if os.path.isdir(fmt_dir):
                for f in sorted(os.listdir(fmt_dir)):
                    if not f.startswith("."):
                        templates.append(f)
            self.template_combo.configure(state="readonly")
        else:
            self.template_combo.configure(state="disabled")

        self.template_combo.configure(values=templates)
        self.template_choice_var.set("None")

    def _open_templates_dir(self):
        """Import a .docx file as a new template."""
        fmt = self.output_format_var.get()
        template_fmt = "docx" if fmt == "pdf" else fmt

        if fmt not in TEMPLATE_FORMATS:
            messagebox.showinfo("Templates", "Templates are only available for Word and PDF output.")
            return

        path = filedialog.askopenfilename(
            title="Select a template file to import",
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")],
        )
        if not path:
            return

        import shutil

        target_dir = os.path.join(TEMPLATES_DIR, template_fmt)
        os.makedirs(target_dir, exist_ok=True)

        filename = os.path.basename(path)
        dest = os.path.join(target_dir, filename)

        if os.path.exists(dest):
            overwrite = messagebox.askyesno(
                "Template Exists",
                f"A template named '{filename}' already exists.\nOverwrite it?",
            )
            if not overwrite:
                return

        try:
            shutil.copy2(path, dest)
            self._refresh_templates()
            self.template_choice_var.set(filename)
            self.status_label.configure(text=f"Template added: {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not import template:\n\n{str(e)}")

    def _open_template_creator(self):
        """Open the template creator window."""
        def on_template_created(filename):
            self._refresh_templates()
            self.template_choice_var.set(filename)
            self.status_label.configure(text=f"Template created: {filename}")

        TemplateCreatorWindow(self, on_complete=on_template_created)

    # ------------------------------------------------------------------
    # Conversion
    # ------------------------------------------------------------------

    def _do_convert(self):
        """Perform the document conversion."""
        if not self.input_path or not os.path.isfile(self.input_path):
            messagebox.showwarning("No File", "Please select a file to convert.")
            return

        output_format = self.output_format_var.get()

        template_path = None
        if self.template_choice_var.get() != "None" and output_format in TEMPLATE_FORMATS:
            template_fmt = "docx" if output_format == "pdf" else output_format
            template_path = os.path.join(
                TEMPLATES_DIR, template_fmt, self.template_choice_var.get()
            )
            if not os.path.isfile(template_path):
                template_path = None

        output_dir = None if (not self.dest_dir or self.dest_dir == "Same as input") else self.dest_dir

        self.status_label.configure(text="Converting...")
        self.update()

        try:
            output_path = convert(
                input_path=self.input_path,
                output_format=output_format,
                output_dir=output_dir,
                template_path=template_path,
            )
            self.status_label.configure(
                text=f"✅ Saved: {os.path.basename(output_path)}"
            )

            # Always open after conversion
            if sys.platform == "win32":
                os.startfile(output_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", output_path])
            else:
                subprocess.run(["xdg-open", output_path])

        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {str(e)[:80]}")
            messagebox.showerror("Conversion Error", f"Failed to convert:\n\n{str(e)}")


def main():
    app = DocForgeApp()
    app.mainloop()


if __name__ == "__main__":
    main()
