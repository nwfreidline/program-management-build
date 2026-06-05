"""
DocForge — Lightweight desktop document converter.
Supports: Markdown, Word (.docx), PDF, HTML, Email (.msg/.eml), Plain Text
With template-aware output.
"""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess

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

# Colors
BG = "#1e1e2e"
FG = "#cdd6f4"
ACCENT = "#89b4fa"
SURFACE = "#313244"
BORDER = "#45475a"
MUTED = "#a6adc8"
GREEN = "#a6e3a1"


class DocForgeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DocForge")
        self.root.configure(bg=BG)
        self.root.resizable(True, True)

        # State
        self.input_path = tk.StringVar()
        self.output_format = tk.StringVar(value="docx")
        self.template_choice = tk.StringVar(value="None")
        self.dest_dir = tk.StringVar()
        self.open_after = tk.BooleanVar(value=True)
        self.status_text = tk.StringVar(value="Ready")

        os.makedirs(TEMPLATES_DIR, exist_ok=True)

        self._build_styles()
        self._build_ui()
        self._setup_drag_and_drop()

        # Set initial size — wide and comfortable
        self.root.geometry("960x360")
        self.root.minsize(860, 300)

    def _build_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("TFrame", background=BG)
        style.configure("TLabel", background=BG, foreground=FG, font=("Segoe UI", 9))
        style.configure("Title.TLabel", background=BG, foreground=ACCENT, font=("Segoe UI", 16, "bold"))
        style.configure("Status.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 9))
        style.configure("Step.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 8))
        style.configure("Arrow.TLabel", background=BG, foreground=BORDER, font=("Segoe UI", 22, "bold"))
        style.configure("FmtDesc.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 8))
        style.configure("TButton", font=("Segoe UI", 9), padding=(6, 2))
        style.configure("Convert.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8))
        style.configure("Small.TButton", font=("Segoe UI", 8), padding=(6, 1))
        style.configure("TCheckbutton", background=BG, foreground=FG, font=("Segoe UI", 9))
        style.configure("TCombobox", font=("Segoe UI", 9), justify="center")

    def _build_ui(self):
        # ── Outer container: centers content both axes ──
        outer = ttk.Frame(self.root)
        outer.pack(fill="both", expand=True)
        outer.rowconfigure(0, weight=1)
        outer.rowconfigure(1, weight=0)  # title
        outer.rowconfigure(2, weight=0)  # flow
        outer.rowconfigure(3, weight=0)  # status
        outer.rowconfigure(4, weight=1)
        outer.columnconfigure(0, weight=1)

        # ── Title ──
        ttk.Label(outer, text="DocForge", style="Title.TLabel").grid(
            row=1, column=0, pady=(0, 20))

        # ── Flow: single horizontal row of "cards", each card is a vertical stack ──
        # Each card is its own frame with internal vertical layout,
        # and the cards are packed side-by-side with vertical centering via grid.
        flow = ttk.Frame(outer)
        flow.grid(row=2, column=0)

        # Single row, all items vertically centered
        flow.rowconfigure(0, weight=0)

        col = 0

        # ═══ Card 1: Drop zone ═══
        card1 = ttk.Frame(flow)
        flow.columnconfigure(col, weight=0)
        card1.grid(row=0, column=col, padx=(0, 4))  # no sticky = centered

        ttk.Label(card1, text="DOC TYPE", style="Step.TLabel").pack()

        self.drop_frame = tk.Frame(
            card1, bg=SURFACE, highlightbackground=BORDER,
            highlightthickness=2, cursor="hand2",
            width=120, height=120
        )
        self.drop_frame.pack(pady=(3, 0))
        self.drop_frame.pack_propagate(False)

        self.drop_label = tk.Label(
            self.drop_frame, text="📄 Drop file\nor browse",
            bg=SURFACE, fg=MUTED, font=("Segoe UI", 9),
            cursor="hand2", justify="center"
        )
        self.drop_label.pack(expand=True)
        self.drop_frame.bind("<Button-1>", lambda e: self._browse_file())
        self.drop_label.bind("<Button-1>", lambda e: self._browse_file())

        # ═══ Arrow ═══
        col += 1
        ttk.Label(flow, text="→", style="Arrow.TLabel").grid(
            row=0, column=col, padx=6)

        # ═══ Card 2: Format ═══
        col += 1
        card2 = ttk.Frame(flow)
        card2.grid(row=0, column=col, padx=4)

        ttk.Label(card2, text="FORMAT", style="Step.TLabel").pack()

        self.format_combo = ttk.Combobox(
            card2, textvariable=self.output_format,
            values=list(FORMAT_LABELS.keys()),
            state="readonly", width=14, justify="center"
        )
        self.format_combo.pack(pady=(3, 0))
        self.format_combo.bind("<<ComboboxSelected>>", self._on_format_change)

        self.format_desc = ttk.Label(card2, text="Word (.docx)", style="FmtDesc.TLabel")
        self.format_desc.pack(pady=(3, 0))

        # ═══ Arrow ═══
        col += 1
        ttk.Label(flow, text="→", style="Arrow.TLabel").grid(
            row=0, column=col, padx=6)

        # ═══ Card 3: Template ═══
        col += 1
        card3 = ttk.Frame(flow)
        card3.grid(row=0, column=col, padx=4)

        # Use grid layout for vertical centering within the card
        card3.rowconfigure(0, weight=1)  # top spacer
        card3.rowconfigure(1, weight=0)  # TEMPLATE label
        card3.rowconfigure(2, weight=0)  # dropdown
        card3.rowconfigure(3, weight=0)  # buttons
        card3.rowconfigure(4, weight=1)  # bottom spacer

        ttk.Label(card3, text="TEMPLATE", style="Step.TLabel").grid(row=1, column=0, pady=(0, 3))

        self.template_combo = ttk.Combobox(
            card3, textvariable=self.template_choice,
            state="readonly", width=28, justify="center"
        )
        self.template_combo.grid(row=2, column=0, pady=(0, 3))
        self._refresh_templates()

        btn_frame = ttk.Frame(card3)
        btn_frame.grid(row=3, column=0)
        ttk.Button(btn_frame, text="Add New", style="Small.TButton",
                   command=self._open_templates_dir).pack(side="left", padx=(0, 4))
        ttk.Button(btn_frame, text="Create New", style="Small.TButton",
                   command=self._open_template_creator).pack(side="left")

        # ═══ Arrow ═══
        col += 1
        ttk.Label(flow, text="→", style="Arrow.TLabel").grid(
            row=0, column=col, padx=6)

        # ═══ Card 4: Destination ═══
        col += 1
        card4 = ttk.Frame(flow)
        card4.grid(row=0, column=col, padx=4)

        ttk.Label(card4, text="DESTINATION", style="Step.TLabel").pack()

        self.dest_entry = ttk.Entry(card4, textvariable=self.dest_dir, width=16, justify="center")
        self.dest_entry.pack(pady=(3, 0))
        self.dest_entry.insert(0, "Same as input")
        self.dest_entry.configure(state="readonly")

        ttk.Button(card4, text="Choose", style="Small.TButton",
                   command=self._browse_dest).pack(pady=(3, 0))

        # ═══ Arrow ═══
        col += 1
        ttk.Label(flow, text="→", style="Arrow.TLabel").grid(
            row=0, column=col, padx=6)

        # ═══ Card 5: Convert ═══
        col += 1
        card5 = ttk.Frame(flow)
        card5.grid(row=0, column=col, padx=(4, 0))

        # Invisible spacer label to match the "LABEL" row on other cards
        ttk.Label(card5, text="", style="Step.TLabel").pack()

        self.convert_btn = tk.Frame(card5, bg=SURFACE, highlightbackground=BORDER,
            highlightthickness=2, cursor="hand2", width=120, height=120)
        self.convert_btn.pack(pady=(3, 0))
        self.convert_btn.pack_propagate(False)

        convert_label = tk.Label(
            self.convert_btn, text="Convert",
            bg=SURFACE, fg=FG, font=("Segoe UI", 11, "bold"),
            cursor="hand2"
        )
        convert_label.pack(expand=True)
        self.convert_btn.bind("<Button-1>", lambda e: self._do_convert())
        convert_label.bind("<Button-1>", lambda e: self._do_convert())

        ttk.Checkbutton(
            card5, text="Open after conversion",
            variable=self.open_after
        ).pack(pady=(4, 0))

        # ── Status ──
        ttk.Label(outer, textvariable=self.status_text, style="Status.TLabel").grid(
            row=3, column=0, pady=(16, 10))

    # ── Drag and Drop ────────────────────────────────────────────

    def _setup_drag_and_drop(self):
        try:
            from tkinterdnd2 import DND_FILES
            self.root.drop_target_register(DND_FILES)
            self.root.dnd_bind("<<Drop>>", self._on_drop)
        except Exception:
            self.drop_label.configure(text="📄 Click\nto browse")

    def _on_drop(self, event):
        path = event.data.strip()
        if path.startswith("{") and path.endswith("}"):
            path = path[1:-1]
        if "\n" in path:
            path = path.split("\n")[0].strip()
        self._set_input_file(path)

    # ── File Selection ───────────────────────────────────────────

    def _browse_file(self):
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
        if not os.path.isfile(path):
            self.status_text.set("Error: File not found")
            return

        fmt = detect_format(path)
        if not fmt:
            self.status_text.set("Error: Unsupported file type")
            return

        self.input_path.set(path)
        filename = os.path.basename(path)
        display = filename if len(filename) <= 18 else filename[:15] + "..."
        self.drop_label.configure(text=f"✅ {display}", fg=GREEN)
        self.status_text.set(f"Loaded: {filename} ({fmt})")

        auto_map = {
            "markdown": "docx", "docx": "markdown", "msg": "docx",
            "eml": "docx", "pdf": "docx", "html": "markdown", "txt": "markdown",
        }
        self.output_format.set(auto_map.get(fmt, "docx"))
        self._on_format_change()

    # ── Destination ──────────────────────────────────────────────

    def _browse_dest(self):
        directory = filedialog.askdirectory()
        if directory:
            self.dest_dir.set(directory)
            display = os.path.basename(directory) or directory
            self.dest_entry.configure(state="normal")
            self.dest_entry.delete(0, tk.END)
            self.dest_entry.insert(0, display)
            self.dest_entry.configure(state="readonly")

    # ── Format / Template ────────────────────────────────────────

    def _on_format_change(self, event=None):
        fmt = self.output_format.get()
        self.format_desc.configure(text=FORMAT_LABELS.get(fmt, fmt))
        self._refresh_templates()

    def _refresh_templates(self):
        fmt = self.output_format.get()
        templates = ["None"]

        if fmt in TEMPLATE_FORMATS:
            # PDF uses the same templates as docx (style definitions)
            template_fmt = "docx" if fmt == "pdf" else fmt
            fmt_dir = os.path.join(TEMPLATES_DIR, template_fmt)
            if os.path.isdir(fmt_dir):
                for f in sorted(os.listdir(fmt_dir)):
                    if not f.startswith("."):
                        templates.append(f)
            self.template_combo.configure(state="readonly")
        else:
            self.template_combo.configure(state="disabled")

        self.template_combo["values"] = templates
        self.template_choice.set("None")

    def _open_templates_dir(self):
        fmt = self.output_format.get()
        target = os.path.join(TEMPLATES_DIR, fmt) if fmt in TEMPLATE_FORMATS else TEMPLATES_DIR
        os.makedirs(target, exist_ok=True)

        if sys.platform == "win32":
            os.startfile(target)
        elif sys.platform == "darwin":
            subprocess.run(["open", target])
        else:
            subprocess.run(["xdg-open", target])

        self.root.after(2000, self._refresh_templates)

    def _open_template_creator(self):
        """Open the template creator window."""
        def on_template_created(filename):
            self._refresh_templates()
            # Auto-select the newly created template
            self.template_choice.set(filename)
            self.status_text.set(f"Template created: {filename}")

        TemplateCreatorWindow(self.root, on_complete=on_template_created)

    # ── Conversion ───────────────────────────────────────────────

    def _do_convert(self):
        input_path = self.input_path.get()
        if not input_path or not os.path.isfile(input_path):
            messagebox.showwarning("No File", "Please select a file to convert.")
            return

        output_format = self.output_format.get()

        template_path = None
        if self.template_choice.get() != "None" and output_format in TEMPLATE_FORMATS:
            # PDF uses the same template files as docx (style definitions)
            template_fmt = "docx" if output_format == "pdf" else output_format
            template_path = os.path.join(TEMPLATES_DIR, template_fmt, self.template_choice.get())
            if not os.path.isfile(template_path):
                template_path = None

        dest = self.dest_dir.get()
        output_dir = None if (not dest or dest == "Same as input") else dest

        self.status_text.set("Converting...")
        self.root.update()

        try:
            output_path = convert(
                input_path=input_path,
                output_format=output_format,
                output_dir=output_dir,
                template_path=template_path,
            )
            self.status_text.set(f"✅ Saved: {os.path.basename(output_path)}")

            if self.open_after.get():
                if sys.platform == "win32":
                    os.startfile(output_path)
                elif sys.platform == "darwin":
                    subprocess.run(["open", output_path])
                else:
                    subprocess.run(["xdg-open", output_path])

        except Exception as e:
            self.status_text.set(f"❌ Error: {str(e)[:80]}")
            messagebox.showerror("Conversion Error", f"Failed to convert:\n\n{str(e)}")


def main():
    try:
        from tkinterdnd2 import TkinterDnD
        root = TkinterDnD.Tk()
    except Exception:
        root = tk.Tk()

    DocForgeApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
