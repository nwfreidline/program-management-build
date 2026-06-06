"""
Template Creator Window — GUI for building custom DocForge templates.

Launched from the main DocForge app via the "Create New" button.
Presents a form for selecting template parameters, optionally uploading
a reference document, then generates the template and refreshes the list.
"""

import os
import customtkinter as ctk
from tkinter import filedialog, messagebox
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

        self.win = ctk.CTkToplevel(parent)
        self.win.title("Create New Template")
        self.win.geometry("560x680")
        self.win.minsize(500, 600)
        self.win.resizable(True, True)
        self.win.grab_set()  # Modal

        self._build_ui()

    def _build_ui(self):
        """Build the template creator form."""
        # Scrollable frame for all content
        scroll = ctk.CTkScrollableFrame(self.win, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=20, pady=15)

        # ── Title ──
        ctk.CTkLabel(
            scroll,
            text="Create New Template",
            font=ctk.CTkFont(size=22, weight="bold"),
        ).pack(anchor="w", pady=(0, 5))

        ctk.CTkLabel(
            scroll,
            text="Configure document formatting for your template.",
            font=ctk.CTkFont(size=12),
            text_color=("gray40", "gray60"),
        ).pack(anchor="w", pady=(0, 20))

        # ── Template Name ──
        self._section_label(scroll, "Template Name")

        self.name_var = ctk.StringVar()
        name_entry = ctk.CTkEntry(
            scroll, textvariable=self.name_var, width=340,
            height=34, font=ctk.CTkFont(size=12),
            placeholder_text="e.g. Project Report, Meeting Notes...",
        )
        name_entry.pack(anchor="w", pady=(0, 16))
        name_entry.focus_set()

        # ── Page Setup ──
        self._section_label(scroll, "Page Setup")

        page_row = ctk.CTkFrame(scroll, fg_color="transparent")
        page_row.pack(anchor="w", fill="x", pady=(0, 12))

        self._field_with_combo(page_row, "Page Size", "page_var", "Letter",
                               list(PAGE_SIZES.keys()), width=120)
        self._field_with_combo(page_row, "Margins", "margins_var", "Normal",
                               list(MARGINS.keys()), width=120)

        # ── Typography ──
        self._section_label(scroll, "Typography")

        type_row1 = ctk.CTkFrame(scroll, fg_color="transparent")
        type_row1.pack(anchor="w", fill="x", pady=(0, 8))

        self._field_with_combo(type_row1, "Font", "font_var", "Calibri",
                               FONTS, width=150)
        self._field_with_combo(type_row1, "Size", "size_var", "11",
                               [str(s) for s in BODY_SIZES], width=80)

        type_row2 = ctk.CTkFrame(scroll, fg_color="transparent")
        type_row2.pack(anchor="w", fill="x", pady=(0, 12))

        self._field_with_combo(type_row2, "Line Spacing", "spacing_var", "Single",
                               list(LINE_SPACING_MAP.keys()), width=120)
        self._field_with_combo(type_row2, "Headings", "heading_var", "Bold only",
                               list(HEADING_STYLES.keys()), width=150)

        # ── Header & Footer ──
        self._section_label(scroll, "Header & Footer")

        header_row = ctk.CTkFrame(scroll, fg_color="transparent")
        header_row.pack(anchor="w", fill="x", pady=(0, 8))

        ctk.CTkLabel(
            header_row, text="Header Text",
            font=ctk.CTkFont(size=12),
        ).pack(side="left", padx=(0, 10))

        self.header_var = ctk.StringVar()
        ctk.CTkEntry(
            header_row, textvariable=self.header_var, width=280, height=32,
            placeholder_text="Optional header text...",
        ).pack(side="left")

        conf_row = ctk.CTkFrame(scroll, fg_color="transparent")
        conf_row.pack(anchor="w", fill="x", pady=(0, 8))

        self._field_with_combo(conf_row, "Confidentiality", "conf_var", "None",
                               ["None", "Amazon Confidential", "Internal Only", "Custom..."],
                               width=180)

        self.page_numbers_var = ctk.BooleanVar(value=True)
        ctk.CTkCheckBox(
            scroll,
            text="Include page numbers (Page X of Y)",
            variable=self.page_numbers_var,
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", pady=(4, 12))

        # ── Reference Document ──
        self._section_label(scroll, "Reference Document (optional)")

        ctk.CTkLabel(
            scroll,
            text="Upload a .docx to extract its formatting as a starting point.",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        ).pack(anchor="w", pady=(0, 8))

        ref_row = ctk.CTkFrame(scroll, fg_color="transparent")
        ref_row.pack(anchor="w", fill="x", pady=(0, 16))

        self.ref_label = ctk.CTkLabel(
            ref_row,
            text="No file selected",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w",
        )
        self.ref_label.pack(side="left", padx=(0, 12))

        ctk.CTkButton(
            ref_row, text="Browse", width=80, height=32,
            fg_color="transparent", border_width=1,
            hover_color=("gray80", "gray30"),
            command=self._browse_reference,
        ).pack(side="left", padx=(0, 6))

        ctk.CTkButton(
            ref_row, text="Clear", width=60, height=32,
            fg_color="transparent", border_width=1,
            hover_color=("gray80", "gray30"),
            command=self._clear_reference,
        ).pack(side="left")

        # ── Action Buttons ──
        btn_frame = ctk.CTkFrame(scroll, fg_color="transparent")
        btn_frame.pack(anchor="w", fill="x", pady=(12, 8))

        ctk.CTkButton(
            btn_frame,
            text="Create Template",
            width=160,
            height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            command=self._create_template,
        ).pack(side="left")

        ctk.CTkButton(
            btn_frame,
            text="Cancel",
            width=90,
            height=42,
            fg_color="gray50",
            hover_color="gray40",
            command=self.win.destroy,
        ).pack(side="left", padx=(12, 0))

        # Status
        self.status_label = ctk.CTkLabel(
            scroll,
            text="",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        )
        self.status_label.pack(anchor="w", pady=(8, 0))

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _section_label(self, parent, text):
        """Create a section header label."""
        ctk.CTkLabel(
            parent,
            text=text,
            font=ctk.CTkFont(size=14, weight="bold"),
        ).pack(anchor="w", pady=(12, 6))

    def _field_with_combo(self, parent, label, var_name, default, values, width=120):
        """Create a label + combobox pair packed side by side."""
        ctk.CTkLabel(
            parent, text=label,
            font=ctk.CTkFont(size=12),
        ).pack(side="left", padx=(0, 8))

        var = ctk.StringVar(value=default)
        setattr(self, var_name, var)

        combo = ctk.CTkComboBox(
            parent, values=values, variable=var,
            width=width, height=32, state="readonly",
        )
        combo.pack(side="left", padx=(0, 20))

    # ------------------------------------------------------------------
    # Reference Document
    # ------------------------------------------------------------------

    def _browse_reference(self):
        """Browse for a reference .docx file."""
        path = filedialog.askopenfilename(
            filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")],
            title="Select Reference Document",
        )
        if path:
            self.reference_path = path
            name = os.path.basename(path)
            display = name if len(name) <= 35 else name[:32] + "..."
            self.ref_label.configure(
                text=f"✅ {display}",
                text_color=("gray10", "white"),
            )

    def _clear_reference(self):
        """Clear the reference document selection."""
        self.reference_path = None
        self.ref_label.configure(
            text="No file selected",
            text_color=("gray50", "gray60"),
        )

    # ------------------------------------------------------------------
    # Create Template
    # ------------------------------------------------------------------

    def _create_template(self):
        """Build the template from form values."""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showwarning(
                "Name Required", "Please enter a template name.", parent=self.win
            )
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

        self.status_label.configure(text="Creating template...")
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
                        f"Could not fully extract styles from reference doc:\n{e}\n\n"
                        "Proceeding with manual selections.",
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

            self.status_label.configure(text=f"✅ Created: {os.path.basename(output_path)}")

            # Notify parent to refresh template list
            if self.on_complete:
                self.on_complete(os.path.basename(output_path))

            messagebox.showinfo(
                "Template Created",
                f"Template saved:\n{os.path.basename(output_path)}\n\n"
                "It's now available in the template dropdown.",
                parent=self.win,
            )
            self.win.destroy()

        except Exception as e:
            self.status_label.configure(text=f"❌ Error: {str(e)[:60]}")
            messagebox.showerror(
                "Error", f"Failed to create template:\n\n{str(e)}", parent=self.win
            )
