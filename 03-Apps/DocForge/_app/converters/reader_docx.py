"""Read Word (.docx) files into the internal document model."""

from docx import Document


def read_docx(filepath):
    """Parse a .docx file into a structured document dict."""
    doc = Document(filepath)
    blocks = []
    title = None

    i = 0
    elements = list(doc.element.body)

    for element in elements:
        tag = element.tag.split("}")[-1] if "}" in element.tag else element.tag

        if tag == "tbl":
            # Process table
            from docx.table import Table
            table = Table(element, doc)
            rows = []
            for row in table.rows:
                cells = [cell.text.strip() for cell in row.cells]
                rows.append(cells)
            if rows:
                blocks.append({"type": "table", "rows": rows})

        elif tag == "p":
            from docx.text.paragraph import Paragraph
            para = Paragraph(element, doc)
            text = para.text.strip()
            style_name = para.style.name if para.style else ""

            if not text:
                continue

            # Detect headings
            if "Heading" in style_name or "AMZN H" in style_name:
                # Extract level
                level = 1
                for ch in style_name:
                    if ch.isdigit():
                        level = int(ch)
                        break
                if title is None and level == 1:
                    title = text
                blocks.append({"type": "heading", "level": level, "text": text})

            # Detect list items
            elif "List" in style_name or "Bullet" in style_name or "Number" in style_name:
                indent = 0
                if para.paragraph_format.left_indent:
                    indent = int(para.paragraph_format.left_indent.inches // 0.5) if para.paragraph_format.left_indent.inches else 0
                blocks.append({"type": "bullet", "text": text, "level": indent})

            # Skip instruction/template text
            elif "Instruction" in style_name:
                continue

            # Regular paragraph
            else:
                blocks.append({"type": "paragraph", "text": text})

    return {
        "title": title or "Untitled",
        "blocks": blocks,
    }
