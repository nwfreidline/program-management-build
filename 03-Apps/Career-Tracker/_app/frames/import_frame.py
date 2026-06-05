"""Import frame — paste text, import from files (.txt, .md, .xlsx)."""
import customtkinter as ctk
from tkinter import filedialog
from pathlib import Path

from config import load_entries, save_entries
from importer import parse_pasted_list, import_from_excel, import_from_docx
from star_engine import generate_star_entry


class ImportFrame(ctk.CTkFrame):
    """Import accomplishments from pasted text or files."""

    def __init__(self, parent, navigate_callback):
        super().__init__(parent, fg_color="transparent")
        self.navigate = navigate_callback
        self._imported_items = []
        self._build_ui()

    def _build_ui(self):
        """Build the import frame layout."""
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header,
            text="Import Items",
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

        # Mode selection buttons
        mode_frame = ctk.CTkFrame(self, fg_color="transparent")
        mode_frame.pack(fill="x", padx=20, pady=(5, 10))

        self.paste_mode_btn = ctk.CTkButton(
            mode_frame,
            text="📋  Paste Text",
            width=130,
            height=34,
            fg_color=("#1565c0", "#1565c0"),
            command=self._show_paste_mode,
        )
        self.paste_mode_btn.pack(side="left", padx=(0, 8))

        self.file_mode_btn = ctk.CTkButton(
            mode_frame,
            text="📁  Import from File",
            width=160,
            height=34,
            fg_color="gray50",
            hover_color="gray40",
            command=self._show_file_mode,
        )
        self.file_mode_btn.pack(side="left")

        # ===== Paste Mode Content =====
        self.paste_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.paste_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        ctk.CTkLabel(
            self.paste_frame,
            text="Paste your accomplishments below (one per line):",
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", pady=(0, 5))

        ctk.CTkLabel(
            self.paste_frame,
            text="Supports bullet points, numbered lists, checkboxes, or plain lines.",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        ).pack(anchor="w", pady=(0, 8))

        self.paste_text = ctk.CTkTextbox(self.paste_frame, height=200)
        self.paste_text.pack(fill="both", expand=True, pady=(0, 10))

        # Paste action buttons
        paste_btn_row = ctk.CTkFrame(self.paste_frame, fg_color="transparent")
        paste_btn_row.pack(fill="x")

        self.paste_import_btn = ctk.CTkButton(
            paste_btn_row,
            text="Import Items",
            width=140,
            height=38,
            fg_color="#1565c0",
            hover_color="#0d47a1",
            command=self._do_paste_import,
        )
        self.paste_import_btn.pack(side="left")

        self.paste_status = ctk.CTkLabel(
            paste_btn_row,
            text="",
            font=ctk.CTkFont(size=12),
        )
        self.paste_status.pack(side="left", padx=15)

        # ===== File Mode Content =====
        self.file_frame = ctk.CTkFrame(self, fg_color="transparent")

        ctk.CTkLabel(
            self.file_frame,
            text="Select a file to import items from:",
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", pady=(0, 5))

        ctk.CTkLabel(
            self.file_frame,
            text="Supported: .txt, .md (one item per line)  •  .docx (paragraphs)  •  .xlsx (first column)",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
        ).pack(anchor="w", pady=(0, 15))

        # File selection row
        file_select_row = ctk.CTkFrame(self.file_frame, fg_color="transparent")
        file_select_row.pack(fill="x", pady=(0, 10))

        self.browse_btn = ctk.CTkButton(
            file_select_row,
            text="Browse...",
            width=120,
            height=38,
            fg_color="#1565c0",
            hover_color="#0d47a1",
            command=self._browse_file,
        )
        self.browse_btn.pack(side="left")

        self.file_path_label = ctk.CTkLabel(
            file_select_row,
            text="No file selected",
            font=ctk.CTkFont(size=11),
            text_color=("gray50", "gray60"),
            anchor="w",
        )
        self.file_path_label.pack(side="left", padx=15, fill="x", expand=True)

        # File preview area
        self.file_preview_label = ctk.CTkLabel(
            self.file_frame,
            text="",
            font=ctk.CTkFont(size=12),
            anchor="w",
        )
        self.file_preview_label.pack(anchor="w", pady=(5, 5))

        self.file_preview_text = ctk.CTkTextbox(self.file_frame, height=160, state="disabled")
        self.file_preview_text.pack(fill="both", expand=True, pady=(0, 10))

        # File action buttons
        file_btn_row = ctk.CTkFrame(self.file_frame, fg_color="transparent")
        file_btn_row.pack(fill="x")

        self.file_import_btn = ctk.CTkButton(
            file_btn_row,
            text="Import Items from File",
            width=180,
            height=38,
            fg_color="#1565c0",
            hover_color="#0d47a1",
            state="disabled",
            command=self._do_file_import,
        )
        self.file_import_btn.pack(side="left")

        self.file_status = ctk.CTkLabel(
            file_btn_row,
            text="",
            font=ctk.CTkFont(size=12),
        )
        self.file_status.pack(side="left", padx=15)

        # ===== Preview Frame (shared, shown after import from either mode) =====
        self.preview_frame = ctk.CTkFrame(self, fg_color="transparent")

        self.preview_scroll = ctk.CTkScrollableFrame(
            self.preview_frame, fg_color="transparent"
        )
        self.preview_scroll.pack(fill="both", expand=True, pady=(0, 10))

        preview_btn_row = ctk.CTkFrame(self.preview_frame, fg_color="transparent")
        preview_btn_row.pack(fill="x")

        ctk.CTkButton(
            preview_btn_row,
            text="Save All as Entries",
            width=160,
            height=38,
            fg_color="#2e7d32",
            hover_color="#1b5e20",
            command=self._save_imported,
        ).pack(side="left")

        ctk.CTkButton(
            preview_btn_row,
            text="Cancel",
            width=100,
            height=38,
            fg_color="gray50",
            command=self._cancel_import,
        ).pack(side="left", padx=10)

        self.save_status = ctk.CTkLabel(
            preview_btn_row,
            text="",
            font=ctk.CTkFont(size=12),
        )
        self.save_status.pack(side="left", padx=10)

    # ------------------------------------------------------------------
    # Mode Switching
    # ------------------------------------------------------------------

    def _show_paste_mode(self):
        """Show the paste input mode."""
        self.preview_frame.pack_forget()
        self.file_frame.pack_forget()
        self.paste_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Update button styles
        self.paste_mode_btn.configure(fg_color=("#1565c0", "#1565c0"))
        self.file_mode_btn.configure(fg_color="gray50")

    def _show_file_mode(self):
        """Show the file import mode."""
        self.preview_frame.pack_forget()
        self.paste_frame.pack_forget()
        self.file_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Update button styles
        self.file_mode_btn.configure(fg_color=("#1565c0", "#1565c0"))
        self.paste_mode_btn.configure(fg_color="gray50")

    # ------------------------------------------------------------------
    # Paste Import
    # ------------------------------------------------------------------

    def _do_paste_import(self):
        """Parse pasted text and show preview."""
        raw_text = self.paste_text.get("1.0", "end-1c")
        items = parse_pasted_list(raw_text)

        if not items:
            self.paste_status.configure(
                text="⚠ No items found. Enter one item per line.",
                text_color=("#c62828", "#f38ba8"),
            )
            return

        self._imported_items = items
        self.paste_status.configure(text="")
        self._show_preview()

    # ------------------------------------------------------------------
    # File Import
    # ------------------------------------------------------------------

    def _browse_file(self):
        """Open file dialog to select a file for import."""
        filepath = filedialog.askopenfilename(
            title="Select file to import",
            filetypes=[
                ("All supported", "*.txt *.md *.docx *.xlsx"),
                ("Text files", "*.txt"),
                ("Markdown files", "*.md"),
                ("Word documents", "*.docx"),
                ("Excel files", "*.xlsx"),
            ],
        )

        if not filepath:
            return

        path = Path(filepath)
        self.file_path_label.configure(
            text=f"{path.name}  ({path.parent})",
            text_color=("gray20", "gray80"),
        )

        # Read and preview the file
        try:
            items = self._read_file(path)
        except Exception as e:
            self.file_status.configure(
                text=f"⚠ Error reading file: {e}",
                text_color=("#c62828", "#f38ba8"),
            )
            return

        if not items:
            self.file_status.configure(
                text="⚠ No items found in file.",
                text_color=("#c62828", "#f38ba8"),
            )
            self.file_import_btn.configure(state="disabled")
            return

        # Show preview in the text box
        self.file_preview_label.configure(
            text=f"Found {len(items)} items:",
        )
        self.file_preview_text.configure(state="normal")
        self.file_preview_text.delete("1.0", "end")
        preview_text = "\n".join(f"  {i}. {item}" for i, item in enumerate(items[:20], 1))
        if len(items) > 20:
            preview_text += f"\n  ... and {len(items) - 20} more"
        self.file_preview_text.insert("1.0", preview_text)
        self.file_preview_text.configure(state="disabled")

        # Store items and enable import button
        self._file_items = items
        self.file_import_btn.configure(state="normal")
        self.file_status.configure(text="")

    def _read_file(self, path: Path) -> list[str]:
        """Read items from a file based on its extension."""
        suffix = path.suffix.lower()

        if suffix == ".xlsx":
            return import_from_excel(str(path))
        elif suffix == ".docx":
            return import_from_docx(str(path))
        elif suffix in (".txt", ".md"):
            content = path.read_text(encoding="utf-8")
            return parse_pasted_list(content)
        else:
            raise ValueError(f"Unsupported file type: {suffix}")

    def _do_file_import(self):
        """Import items from the selected file and show preview."""
        if not hasattr(self, "_file_items") or not self._file_items:
            return

        self._imported_items = self._file_items
        self.file_status.configure(text="")
        self._show_preview()

    # ------------------------------------------------------------------
    # Preview & Save (shared by both modes)
    # ------------------------------------------------------------------

    def _show_preview(self):
        """Show the import preview with all parsed items."""
        self.paste_frame.pack_forget()
        self.file_frame.pack_forget()
        self.preview_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Build preview list
        for widget in self.preview_scroll.winfo_children():
            widget.destroy()

        ctk.CTkLabel(
            self.preview_scroll,
            text=f"Preview — {len(self._imported_items)} items to import:",
            font=ctk.CTkFont(size=13, weight="bold"),
        ).pack(anchor="w", pady=(0, 10))

        for i, item in enumerate(self._imported_items, 1):
            item_frame = ctk.CTkFrame(self.preview_scroll, corner_radius=6)
            item_frame.pack(fill="x", pady=(0, 4))

            ctk.CTkLabel(
                item_frame,
                text=f"  {i}. {item}",
                font=ctk.CTkFont(size=12),
                anchor="w",
            ).pack(fill="x", padx=8, pady=6)

    def _save_imported(self):
        """Save all imported items as new entries (title only, STAR details blank)."""
        entries = load_entries()

        from datetime import datetime

        now = datetime.now()
        date_completed = f"{now.year}-{now.month:02d}"

        for item in self._imported_items:
            entry = generate_star_entry(
                title=item,
                status="In Progress",
                situation="",
                task="",
                actions=[],
                result="",
                date_completed=date_completed,
            )
            entries.append(entry)

        save_entries(entries)

        # Log to protection changelog
        try:
            from protection import ProtectionStack
            protection = ProtectionStack()
            protection.create_version(reason="pre-import")
            protection.log_action(
                "Import",
                f"Imported {len(self._imported_items)} items",
                [item[:60] for item in self._imported_items[:5]],
            )
        except Exception:
            pass  # Protection is optional

        self.save_status.configure(
            text=f"✓ {len(self._imported_items)} entries saved!",
            text_color=("#2e7d32", "#a6e3a1"),
        )

        # Reset after delay
        self.after(2000, lambda: self.navigate("home"))

    def _cancel_import(self):
        """Cancel import and go back to paste mode."""
        self._imported_items = []
        self._show_paste_mode()

    def on_show(self):
        """Called when this frame becomes visible."""
        self.paste_status.configure(text="")
        self.file_status.configure(text="")
        self.save_status.configure(text="")
        self._show_paste_mode()
