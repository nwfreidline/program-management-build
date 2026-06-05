"""Export frame — export entries to various formats."""
import customtkinter as ctk
from tkinter import filedialog

from config import load_entries, load_settings
from star_engine import format_entry_as_markdown, format_entry_as_text


class ExportFrame(ctk.CTkFrame):
    """Export entries to Word, Excel, Markdown, or plain text."""

    def __init__(self, parent, navigate_callback):
        super().__init__(parent, fg_color="transparent")
        self.navigate = navigate_callback
        self._build_ui()

    def _build_ui(self):
        """Build the export frame layout."""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="Export Entries",
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

        # Format selection
        format_frame = ctk.CTkFrame(self, fg_color="transparent")
        format_frame.pack(fill="x", padx=20, pady=(10, 10))

        ctk.CTkLabel(
            format_frame,
            text="Export Format:",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(anchor="w", pady=(0, 8))

        formats = [
            "Word Document (.docx)",
            "Excel Spreadsheet (.xlsx)",
            "Markdown (.md)",
            "Plain Text (.txt)",
        ]

        settings = load_settings()
        default_fmt = settings.get("default_export", "docx")
        default_map = {
            "docx": formats[0],
            "xlsx": formats[1],
            "md": formats[2],
            "txt": formats[3],
        }

        self.format_var = ctk.StringVar(value=default_map.get(default_fmt, formats[0]))
        self.format_menu = ctk.CTkOptionMenu(
            format_frame,
            variable=self.format_var,
            values=formats,
            width=250,
        )
        self.format_menu.pack(anchor="w")

        # Entry count info
        self.info_label = ctk.CTkLabel(
            format_frame,
            text="",
            font=ctk.CTkFont(size=12),
            text_color=("gray50", "gray60"),
        )
        self.info_label.pack(anchor="w", pady=(12, 0))

        # Export button
        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=(10, 10))

        self.export_btn = ctk.CTkButton(
            btn_frame,
            text="Export All",
            width=160,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#e65100",
            hover_color="#bf360c",
            command=self._do_export,
        )
        self.export_btn.pack(side="left")

        self.export_status = ctk.CTkLabel(
            btn_frame,
            text="",
            font=ctk.CTkFont(size=12),
        )
        self.export_status.pack(side="left", padx=15)

        # Preview section
        preview_frame = ctk.CTkFrame(self, fg_color="transparent")
        preview_frame.pack(fill="both", expand=True, padx=20, pady=(15, 15))

        ctk.CTkLabel(
            preview_frame,
            text="Preview (first 2 entries):",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", pady=(0, 5))

        self.preview_text = ctk.CTkTextbox(preview_frame, height=250)
        self.preview_text.pack(fill="both", expand=True)

    def _do_export(self):
        """Perform the export based on selected format."""
        entries = load_entries()
        if not entries:
            self.export_status.configure(
                text="⚠ No entries to export.",
                text_color=("#c62828", "#f38ba8"),
            )
            return

        fmt = self.format_var.get()

        # Determine file type and extension
        if "Word" in fmt:
            ext = ".docx"
            filetypes = [("Word Document", "*.docx")]
        elif "Excel" in fmt:
            ext = ".xlsx"
            filetypes = [("Excel Spreadsheet", "*.xlsx")]
        elif "Markdown" in fmt:
            ext = ".md"
            filetypes = [("Markdown", "*.md")]
        else:
            ext = ".txt"
            filetypes = [("Text File", "*.txt")]

        # Open save dialog
        filepath = filedialog.asksaveasfilename(
            defaultextension=ext,
            filetypes=filetypes,
            initialfile=f"Career_Tracker_Export{ext}",
            title="Export Career Entries",
        )

        if not filepath:
            return

        try:
            if ext == ".docx":
                from exporter import export_to_word
                export_to_word(entries, filepath)
            elif ext == ".xlsx":
                from exporter import export_to_excel
                export_to_excel(entries, filepath)
            elif ext == ".md":
                from exporter import export_to_markdown
                export_to_markdown(entries, filepath)
            else:
                from exporter import export_to_text
                export_to_text(entries, filepath)

            self.export_status.configure(
                text=f"✓ Exported {len(entries)} entries!",
                text_color=("#2e7d32", "#a6e3a1"),
            )
        except ImportError as e:
            self.export_status.configure(
                text=f"⚠ {str(e)}",
                text_color=("#c62828", "#f38ba8"),
            )
        except Exception as e:
            self.export_status.configure(
                text=f"⚠ Export failed: {str(e)}",
                text_color=("#c62828", "#f38ba8"),
            )

    def _update_preview(self):
        """Update the preview text with first 2 entries."""
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")

        entries = load_entries()
        if not entries:
            self.preview_text.insert("1.0", "No entries to preview.")
            self.preview_text.configure(state="disabled")
            return

        # Show first 2 entries
        preview_entries = entries[:2]
        fmt = self.format_var.get()

        if "Markdown" in fmt or "Word" in fmt:
            for entry in preview_entries:
                self.preview_text.insert("end", format_entry_as_markdown(entry))
        else:
            for entry in preview_entries:
                self.preview_text.insert("end", format_entry_as_text(entry))

        if len(entries) > 2:
            self.preview_text.insert("end", f"\n... and {len(entries) - 2} more entries")

        self.preview_text.configure(state="disabled")

    def on_show(self):
        """Called when this frame becomes visible."""
        entries = load_entries()
        self.info_label.configure(
            text=f"{len(entries)} {'entry' if len(entries) == 1 else 'entries'} will be exported"
        )
        self.export_status.configure(text="")
        self._update_preview()
