"""Core conversion engine — routes files through reader → model → writer."""

import os
import sys

# Ensure converters package is importable
_converters_dir = os.path.dirname(os.path.abspath(__file__))
_docforge_dir = os.path.dirname(_converters_dir)
if _docforge_dir not in sys.path:
    sys.path.insert(0, _docforge_dir)

# Format detection
FORMAT_EXTENSIONS = {
    ".md": "markdown",
    ".markdown": "markdown",
    ".docx": "docx",
    ".pdf": "pdf",
    ".html": "html",
    ".htm": "html",
    ".txt": "txt",
    ".text": "txt",
    ".msg": "msg",
    ".eml": "eml",
}

OUTPUT_FORMATS = ["markdown", "docx", "pdf", "html", "txt", "eml"]

OUTPUT_EXTENSIONS = {
    "markdown": ".md",
    "docx": ".docx",
    "pdf": ".pdf",
    "html": ".html",
    "txt": ".txt",
    "eml": ".eml",
}


def detect_format(filepath):
    """Detect file format from extension."""
    ext = os.path.splitext(filepath)[1].lower()
    return FORMAT_EXTENSIONS.get(ext)


def read_file(filepath):
    """Read a file into the internal document model."""
    fmt = detect_format(filepath)
    if not fmt:
        raise ValueError(f"Unsupported file format: {filepath}")

    if fmt == "markdown":
        from converters.reader_md import read_markdown
        return read_markdown(filepath)
    elif fmt == "docx":
        from converters.reader_docx import read_docx
        return read_docx(filepath)
    elif fmt == "pdf":
        from converters.reader_pdf import read_pdf
        return read_pdf(filepath)
    elif fmt == "html":
        from converters.reader_html import read_html
        return read_html(filepath)
    elif fmt == "txt":
        from converters.reader_txt import read_txt
        return read_txt(filepath)
    elif fmt == "msg":
        from converters.reader_email import read_msg
        return read_msg(filepath)
    elif fmt == "eml":
        from converters.reader_email import read_eml
        return read_eml(filepath)
    else:
        raise ValueError(f"No reader for format: {fmt}")


def write_file(doc_model, output_path, output_format, template_path=None):
    """Write the internal document model to the specified format."""
    if output_format == "markdown":
        from converters.writer_md import write_markdown
        write_markdown(doc_model, output_path)
    elif output_format == "docx":
        from converters.writer_docx import write_docx
        write_docx(doc_model, output_path, template_path=template_path)
    elif output_format == "pdf":
        from converters.writer_pdf import write_pdf
        write_pdf(doc_model, output_path, template_path=template_path)
    elif output_format == "html":
        from converters.writer_html import write_html
        write_html(doc_model, output_path)
    elif output_format == "txt":
        from converters.writer_txt import write_txt
        write_txt(doc_model, output_path)
    elif output_format == "eml":
        from converters.writer_email import write_eml
        write_eml(doc_model, output_path)
    else:
        raise ValueError(f"No writer for format: {output_format}")


def convert(input_path, output_format, output_dir=None, template_path=None):
    """Full conversion pipeline: read → model → write.
    
    Args:
        input_path: Path to the source file
        output_format: Target format string (e.g., 'docx', 'markdown')
        output_dir: Directory for output file (defaults to same as input)
        template_path: Optional .docx template for Word output
    
    Returns:
        Path to the output file
    """
    # Determine output path
    basename = os.path.splitext(os.path.basename(input_path))[0]
    ext = OUTPUT_EXTENSIONS.get(output_format, f".{output_format}")
    output_filename = f"{basename}{ext}"

    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, output_filename)
    else:
        output_path = os.path.join(os.path.dirname(input_path), output_filename)

    # Check for specialized converters based on template selection
    if template_path and output_format in ("docx", "pdf"):
        template_name = os.path.basename(template_path).lower()

        # Growth Timeline — dedicated converter with STAR-aware parsing
        if "growth_timeline" in template_name:
            from converters.writer_growth_timeline import write_growth_timeline
            write_growth_timeline(input_path, output_path, template_path)
            return output_path

    # Standard pipeline: read → model → write
    doc_model = read_file(input_path)
    write_file(doc_model, output_path, output_format, template_path=template_path)

    return output_path
