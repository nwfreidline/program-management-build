"""
Template Creator Window — GUI for building custom DocForge templates.

Launched from the main DocForge app via the "Create New" button.
Presents a form for selecting template parameters, optionally uploading
a reference document, then generates the template and refreshes the list.
"""

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

# Import the builder
_this_dir = Path(__file__).parent
import sys
if str(_this_dir) not in sys.path:
    sys.path.insert(0, str(_this_dir))

from templates.template_builder import (
    build_template, extract_styles_from_reference,
    FONTS, BODY_SIZES, PAGE_SIZES, MARGINS, LINE_SPACING_MAP, HEADING_STYLES,
)

# Colors (match main app)
BG = "#1e1e2e"
FG = "#cdd6f4"
ACCENT = "#89b4fa"
SURFACE = "#313244"
BORDER = "#45475a"
MUTED = "#a6adc8"
GREEN = "#a6e3a1"


class TemplateCreatorWindow:
    """Toplevel window for creating custom templates."""

    def __init__(self, parent, on_complete=None):
        """
        Args:
            parent: Parent tk widget (root or frame)
            on_complete: Callback function called after template is created.
                         Receives the template filename as argument.
        """
        self.on_complete = on_complete
        self.reference_path = None

        self.win = tk.Toplevel(parent)
        self.win.title("Create New Template")
        self.win.configure(bg=BG)
        self.win.geometry("520x640")
        self.win.minsize(480, 580)
        self.win.resizable(True, True)
        self.win.grab_set()  # Modal

        self._build_styles()
        self._build_ui()

    def _build_styles(self):
        style = ttk.Style()
        style.configure("Creator.TFrame", background=BG)
        style.configure("Creator.TLabel", background=BG, foreground=FG, font=("Segoe UI", 9))
        style.configure("CreatorTitle.TLabel", background=BG, foreground=ACCENT, font=("Segoe UI", 14, "bold"))
        style.configure("CreatorSection.TLabel", background=BG, foreground=ACCENT, font=("Segoe UI", 10, "bold"))
        style.configure("CreatorMuted.TLabel", background=BG, foreground=MUTED, font=("Segoe UI", 8))
        style.configure("Creator.TButton", font=("Segoe UI", 9), padding=(8, 4))
        style.configure("CreatorCreate.TButton", font=("Segoe UI", 11, "bold"), padding=(16, 8))
        style.configure("Creator.TCheckbutton", background=BG, foreground=FG, font=("Segoe UI", 9))
        style.configure("Creator.TCombobox", font=("Segoe UI", 9))
        style.configure("Creator.TEntry", font=("Segoe UI", 9))

    def _build_ui(self):
        # Scrollable container
        canvas = tk.Canvas(self.win, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.win, orient="vertical", command=canvas.yview)
        self.scroll_frame = ttk.Frame(canvas, style="Creator.TFrame")

        self.scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=20, pady=10)
        scrollbar.pack(side="right", fill="y")

        # Bind mousewheel
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        f = self.scroll_frame

        # ── Title ──
        ttk.Label(f, text="Create New Template", style="CreatorTitle.TLabel").pack(anchor="w", pady=(0, 12))

        # ── Template Name ──
        self._section_label(f, "Template Name")
        self.name_var = tk.StringVar()
        name_entry = ttk.Entry(f, textvariable=self.name_var, width=40, font=("Segoe UI", 10))
        name_entry.pack(anchor="w", pady=(0, 12))
        name_entry.focus_set()

        # ── Page Setup ──
        self._section_label(f, "Page Setup")

        row1 = ttk.Frame(f, style="Creator.TFrame")
        row1.pack(anchor="w", fill="x", pady=(0, 8))

        self._field_label(row1, "Page Size")
        self.page_var = tk.StringVar(value="Letter")
        ttk.Combobox(row1, textvariable=self.page_var, values=list(PAGE_SIZES.keys()),
                     state="readonly", width=10).pack(side="left", padx=(0, 20))

        self._field_label(row1, "Margins")
        self.margins_var = tk.StringVar(value="Normal")
        ttk.Combobox(row1, textvariable=self.margins_var, values=list(MARGINS.keys()),
                     state="readonly", width=10).pack(side="left")

        # ── Typography ──
        self._section_label(f, "Typography")

        row2 = ttk.Frame(f, style="Creator.TFrame")
        row2.pack(anchor="w", fill="x", pady=(0, 8))

        self._field_label(row2, "Font")
        self.font_var = tk.StringVar(value="Calibri")
        ttk.Combobox(row2, textvariable=self.font_var, values=FONTS,
                     state="readonly", width=14).pack(side="left", padx=(0, 20))

        self._field_label(row2, "Size")
        self.size_var = tk.StringVar(value="11")
        ttk.Combobox(row2, textvariable=self.size_var, values=[str(s) for s in BODY_SIZES],
                     state="readonly", width=5).pack(side="left")

        row3 = ttk.Frame(f, style="Creator.TFrame")
        row3.pack(anchor="w", fill="x", pady=(0, 8))

        self._field_label(row3, "Line Spacing")
        self.spacing_var = tk.StringVar(value="Single")
        ttk.Combobox(row3, textvariable=self.spacing_var, values=list(LINE_SPACING_MAP.keys()),
                     state="readonly", width=10).pack(side="left", padx=(0, 20))

        self._field_label(row3, "Headings")
        self.heading_var = tk.StringVar(value="Bold only")
        ttk.Combobox(row3, textvariable=self.heading_var, values=list(HEADING_STYLES.keys()),
                     state="readonly", width=14).pack(side="left")

        # ── Header & Footer ──
        self._section_label(f, "Header & Footer")

        row4 = ttk.Frame(f, style="Creator.TFrame")
        row4.pack(anchor="w", fill="x", pady=(0, 8))

        self._field_label(row4, "Header Text")
        self.header_var = tk.StringVar()
        ttk.Entry(row4, textvariable=self.header_var, width=36).pack(side="left")

        row5 = ttk.Frame(f, style="Creator.TFrame")
        row5.pack(anchor="w", fill="x", pady=(0, 8))

        self._field_label(row5, "Confidentiality")
        self.conf_var = tk.StringVar(value="None")
        ttk.Combobox(row5, textvariable=self.conf_var,
                     values=["None", "Amazon Confidential", "Internal Only", "Custom..."],
                     state="readonly", width=20).pack(side="left")

        row5b = ttk.Frame(f, style="Creator.TFrame")
        row5b.pack(anchor="w", fill="x", pady=(0, 8))

        self.page_numbers_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(row5b, text="Include page numbers (Page X of Y)",
                        variable=self.page_numbers_var,
                        style="Creator.TCheckbutton").pack(anchor="w")

        # ── Reference Document ──
        self._section_label(f, "Reference Document (optional)")
        ttk.Label(f, text="Upload a .docx to extract its formatting as a starting point.",
                  style="CreatorMuted.TLabel").pack(anchor="w", pady=(0, 4))

        ref_row = ttk.Frame(f, style="Creator.TFrame")
        ref_row.pack(anchor="w", fill="x", pady=(0, 4))

        self.ref_label = ttk.Label(ref_row, text="No file selected", style="CreatorMuted.TLabel")
        self.ref_label.pack(side="left", padx=(0, 10))

        ttk.Button(ref_row, text="Browse", style="Creator.TButton",
                   command=self._browse_reference).pack(side="left")
        ttk.Button(ref_row, text="Clear", style="Creator.TButton",
                   command=self._clear_reference).pack(side="left", padx=(6, 0))

        # ── Spacer ──
        ttk.Frame(f, height=20, style="Creator.TFrame").pack()

        # ── Create Button ──
        btn_frame = ttk.Frame(f, style="Creator.TFrame")
        btn_frame.pack(anchor="w", fill="x", pady=(8, 12))

        create_btn = tk.Button(
            btn_frame, text="Create Template", font=("Segoe UI", 11, "bold"),
            bg=ACCENT, fg="#1e1e2e", activebackground="#b4d0fb",
            relief="flat", cursor="hand2", padx=20, pady=8,
            command=self._create_template,
        )
        create_btn.pack(side="left")

        ttk.Button(btn_frame, text="Cancel", style="Creator.TButton",
                   command=self.win.destroy).pack(side="left", padx=(12, 0))

        # ── Status ──
        self.status_var = tk.StringVar(value="")
        ttk.Label(f, textvariable=self.status_var, style="CreatorMuted.TLabel").pack(anchor="w", pady=(4, 0))

    # ── Helpers ──

    def _section_label(self, parent, text):
        ttk.Label(parent, text=text, style="CreatorSection.TLabel").pack(anchor="w", pady=(12, 4))

    def _field_label(self, parent, text):
        ttk.Label(parent, text=text, style="Creator.TLabel").pack(side="left", padx=(0, 6))

    # ── Reference doc ──

    def _browse_reference(self):
        path = filedialog.askopenfilename(
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")],
            title="Select Reference Document",
        )
        if path:
            self.reference_path = path
            name = os.path.basename(path)
            display = name if len(name) <= 35 else name[:32] + "..."
            self.ref_label.configure(text=f"✅ {display}")

    def _clear_reference(self):
        self.reference_path = None
        self.ref_label.configure(text="No file selected")

    # ── Create ──

    def _create_template(self):
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning("Name Required", "Please enter a template name.", parent=self.win)
            return

        # Check for duplicate
        safe_name = "".join(c for c in name if c.isalnum() or c in " _-").strip()
        filename = f"{safe_name.replace(' ', '_')}_Template.docx"
        target = Path(__file__).parent / "templates" / "docx" / filename
        if target.exists():
            overwrite = messagebox.askyesno(
                "Template Exists",
                f"A template named '{filename}' already exists.\nOverwrite it?",
                parent=self.win,
            )
            if not overwrite:
                return

        self.status_var.set("Creating template...")
        self.win.update()

        try:
            # Extract reference styles if provided
            ref_params = None
            if self.reference_path:
                try:
                    ref_params = extract_styles_from_reference(self.reference_path)
                except Exception as e:
                    messagebox.showwarning(
                        "Reference Warning",
                        f"Could not fully extract styles from reference doc:\n{e}\n\nProceeding with manual selections.",
                        parent=self.win,
                    )

            # Resolve confidentiality
            conf = self.conf_var.get()
            if conf == "Custom...":
                conf = self.header_var.get() or "Confidential"

            # Build
            output_path = build_template(
                name=name,
                font_name=self.font_var.get(),
                body_size=int(self.size_var.get()),
                page_size=self.page_var.get(),
                margins=self.margins_var.get(),
                line_spacing=self.spacing_var.get(),
                heading_style=self.heading_var.get(),
                header_text=self.header_var.get(),
                footer_text="",
                show_page_numbers=self.page_numbers_var.get(),
                confidentiality=conf,
                reference_params=ref_params,
            )

            self.status_var.set(f"✅ Created: {os.path.basename(output_path)}")

            # Notify parent to refresh template list
            if self.on_complete:
                self.on_complete(os.path.basename(output_path))

            messagebox.showinfo(
                "Template Created",
                f"Template saved:\n{os.path.basename(output_path)}\n\nIt's now available in the template dropdown.",
                parent=self.win,
            )
            self.win.destroy()

        except Exception as e:
            self.status_var.set(f"❌ Error: {str(e)[:60]}")
            messagebox.showerror("Error", f"Failed to create template:\n\n{str(e)}", parent=self.win)
