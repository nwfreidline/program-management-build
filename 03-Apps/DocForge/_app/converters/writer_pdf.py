"""Write internal document model to PDF via styled HTML intermediate."""

import os
import tempfile
import html as html_lib


def _build_narrative_html(doc_model):
    """Build HTML that mirrors the narrative template formatting.
    
    Matches: Calibri fonts, narrow margins, compact table styling,
    heading sizes, paragraph spacing — same as the .docx narrative template.
    """
    title = html_lib.escape(doc_model["title"])

    parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        f"  <title>{title}</title>",
        '  <meta charset="utf-8">',
        "  <style>",
        "    body {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 11pt;",
        "      line-height: 1.15;",
        "      color: #000000;",
        "      margin: 0;",
        "      padding: 0;",
        "    }",
        "    h1 {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 16pt;",
        "      font-weight: bold;",
        "      margin-top: 12pt;",
        "      margin-bottom: 0;",
        "      color: #000000;",
        "    }",
        "    h2 {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 13pt;",
        "      font-weight: bold;",
        "      margin-top: 12pt;",
        "      margin-bottom: 0;",
        "      color: #000000;",
        "    }",
        "    h3 {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 11pt;",
        "      font-weight: bold;",
        "      margin-top: 6pt;",
        "      margin-bottom: 0;",
        "      color: #000000;",
        "    }",
        "    h4 {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 11pt;",
        "      font-weight: bold;",
        "      font-style: italic;",
        "      margin-top: 6pt;",
        "      margin-bottom: 0;",
        "      color: #000000;",
        "    }",
        "    p {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 11pt;",
        "      margin-top: 0;",
        "      margin-bottom: 6pt;",
        "      line-height: 1.15;",
        "    }",
        "    ul {",
        "      margin-top: 0;",
        "      margin-bottom: 6pt;",
        "      padding-left: 0.25in;",
        "    }",
        "    li {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 11pt;",
        "      margin-bottom: 2pt;",
        "      line-height: 1.15;",
        "    }",
        "    table {",
        "      border-collapse: collapse;",
        "      width: 100%;",
        "      margin-top: 6pt;",
        "      margin-bottom: 6pt;",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 10pt;",
        "    }",
        "    th, td {",
        "      border: 1px solid #BFBFBF;",
        "      padding: 3pt 5pt;",
        "      text-align: left;",
        "      vertical-align: top;",
        "    }",
        "    th {",
        "      background-color: #F2F2F2;",
        "      font-weight: bold;",
        "    }",
        "    pre {",
        "      font-family: Consolas, monospace;",
        "      font-size: 9.5pt;",
        "      margin-top: 4pt;",
        "      margin-bottom: 4pt;",
        "      padding: 6pt;",
        "      background: #F8F8F8;",
        "      border: 1px solid #E0E0E0;",
        "    }",
        "  </style>",
        "</head>",
        "<body>",
    ]

    in_list = False
    in_ordered = False

    for block in doc_model["blocks"]:
        btype = block["type"]

        # Close lists if leaving list context
        if btype != "bullet" and in_list:
            parts.append("</ul>")
            in_list = False
        if btype != "numbered" and in_ordered:
            parts.append("</ol>")
            in_ordered = False

        if btype == "heading":
            level = min(block.get("level", 1), 4)
            parts.append(f"<h{level}>{html_lib.escape(block['text'])}</h{level}>")

        elif btype == "paragraph":
            text = html_lib.escape(block["text"]).replace("\n", "<br>")
            parts.append(f"<p>{text}</p>")

        elif btype == "bullet":
            if not in_list:
                indent = block.get("level", 0)
                margin_left = 0.25 * indent
                if margin_left > 0:
                    parts.append(f'<ul style="margin-left:{margin_left}in">')
                else:
                    parts.append("<ul>")
                in_list = True
            parts.append(f"  <li>{html_lib.escape(block['text'])}</li>")

        elif btype == "numbered":
            if not in_ordered:
                indent = block.get("level", 0)
                margin_left = 0.25 * indent
                if margin_left > 0:
                    parts.append(f'<ol style="margin-left:{margin_left}in">')
                else:
                    parts.append("<ol>")
                in_ordered = True
            parts.append(f"  <li>{html_lib.escape(block['text'])}</li>")

        elif btype == "table":
            rows = block["rows"]
            if not rows:
                continue
            parts.append("<table>")
            # Header row
            parts.append("  <tr>")
            for cell in rows[0]:
                parts.append(f"    <th>{html_lib.escape(cell)}</th>")
            parts.append("  </tr>")
            # Data rows
            for row in rows[1:]:
                parts.append("  <tr>")
                for cell in row:
                    parts.append(f"    <td>{html_lib.escape(cell)}</td>")
                parts.append("  </tr>")
            parts.append("</table>")

        elif btype == "code":
            escaped = html_lib.escape(block["text"])
            parts.append(f"<pre>{escaped}</pre>")

    if in_list:
        parts.append("</ul>")
    if in_ordered:
        parts.append("</ol>")

    parts.extend(["</body>", "</html>"])
    return "\n".join(parts)


def _build_generic_html(doc_model):
    """Build styled HTML for default (no-template) PDF output.
    
    Matches the default .docx formatting:
    - Calibri 10pt body, black text, single-spaced, 6pt after
    - H1: 14pt bold, H2: 12pt bold, H3: 10pt bold, H4: 10pt bold italic
    - Tables: 10pt, light borders, shaded header, compact padding
    - No colored text
    - 1" margins
    """
    title = html_lib.escape(doc_model["title"])

    parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        f"  <title>{title}</title>",
        '  <meta charset="utf-8">',
        "  <style>",
        "    body {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 10pt;",
        "      line-height: 1.15;",
        "      color: #000000;",
        "      margin: 0;",
        "      padding: 0;",
        "    }",
        "    h1 {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 14pt;",
        "      font-weight: bold;",
        "      margin-top: 10pt;",
        "      margin-bottom: 2pt;",
        "      color: #000000;",
        "    }",
        "    h2 {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 12pt;",
        "      font-weight: bold;",
        "      margin-top: 10pt;",
        "      margin-bottom: 2pt;",
        "      color: #000000;",
        "    }",
        "    h3 {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 10pt;",
        "      font-weight: bold;",
        "      margin-top: 8pt;",
        "      margin-bottom: 2pt;",
        "      color: #000000;",
        "    }",
        "    h4 {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 10pt;",
        "      font-weight: bold;",
        "      font-style: italic;",
        "      margin-top: 8pt;",
        "      margin-bottom: 2pt;",
        "      color: #000000;",
        "    }",
        "    p {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 10pt;",
        "      margin-top: 0;",
        "      margin-bottom: 6pt;",
        "      line-height: 1.15;",
        "      color: #000000;",
        "    }",
        "    ul {",
        "      margin-top: 0;",
        "      margin-bottom: 6pt;",
        "      padding-left: 0.25in;",
        "    }",
        "    li {",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 10pt;",
        "      margin-bottom: 2pt;",
        "      line-height: 1.15;",
        "      color: #000000;",
        "    }",
        "    table {",
        "      border-collapse: collapse;",
        "      width: 100%;",
        "      margin-top: 6pt;",
        "      margin-bottom: 6pt;",
        "      font-family: Calibri, sans-serif;",
        "      font-size: 10pt;",
        "    }",
        "    th, td {",
        "      border: 1px solid #BFBFBF;",
        "      padding: 3pt 5pt;",
        "      text-align: left;",
        "      vertical-align: top;",
        "      color: #000000;",
        "    }",
        "    th {",
        "      background-color: #F2F2F2;",
        "      font-weight: bold;",
        "    }",
        "    pre {",
        "      font-family: Consolas, monospace;",
        "      font-size: 9pt;",
        "      margin-top: 4pt;",
        "      margin-bottom: 4pt;",
        "      padding: 6pt;",
        "      background: #F8F8F8;",
        "      border: 1px solid #E0E0E0;",
        "      color: #000000;",
        "    }",
        "  </style>",
        "</head>",
        "<body>",
    ]

    in_list = False
    in_ordered = False

    for block in doc_model["blocks"]:
        btype = block["type"]

        if btype != "bullet" and in_list:
            parts.append("</ul>")
            in_list = False
        if btype != "numbered" and in_ordered:
            parts.append("</ol>")
            in_ordered = False

        if btype == "heading":
            level = min(block.get("level", 1), 4)
            parts.append(f"<h{level}>{html_lib.escape(block['text'])}</h{level}>")

        elif btype == "paragraph":
            text = html_lib.escape(block["text"]).replace("\n", "<br>")
            parts.append(f"<p>{text}</p>")

        elif btype == "bullet":
            if not in_list:
                indent = block.get("level", 0)
                margin_left = 0.25 * indent
                if margin_left > 0:
                    parts.append(f'<ul style="margin-left:{margin_left}in">')
                else:
                    parts.append("<ul>")
                in_list = True
            parts.append(f"  <li>{html_lib.escape(block['text'])}</li>")

        elif btype == "numbered":
            if not in_ordered:
                indent = block.get("level", 0)
                margin_left = 0.25 * indent
                if margin_left > 0:
                    parts.append(f'<ol style="margin-left:{margin_left}in">')
                else:
                    parts.append("<ol>")
                in_ordered = True
            parts.append(f"  <li>{html_lib.escape(block['text'])}</li>")

        elif btype == "table":
            rows = block["rows"]
            if not rows:
                continue
            parts.append("<table>")
            parts.append("  <tr>")
            for cell in rows[0]:
                parts.append(f"    <th>{html_lib.escape(cell)}</th>")
            parts.append("  </tr>")
            for row in rows[1:]:
                parts.append("  <tr>")
                for cell in row:
                    parts.append(f"    <td>{html_lib.escape(cell)}</td>")
                parts.append("  </tr>")
            parts.append("</table>")

        elif btype == "code":
            escaped = html_lib.escape(block["text"])
            parts.append(f"<pre>{escaped}</pre>")

    if in_list:
        parts.append("</ul>")
    if in_ordered:
        parts.append("</ol>")

    parts.extend(["</body>", "</html>"])
    return "\n".join(parts)


def write_pdf(doc_model, output_path, template_path=None):
    """Convert document model to PDF.
    
    When template_path is provided, uses narrative-styled formatting that
    matches the .docx template (fonts, margins, table styling, header/footer).
    Without a template, uses generic formatting.
    
    Args:
        doc_model: The internal document dict
        output_path: Where to save the PDF
        template_path: Optional template path — triggers narrative styling
    """
    # Build styled HTML based on whether a template is in use
    if template_path:
        html_content = _build_narrative_html(doc_model)
    else:
        html_content = _build_generic_html(doc_model)

    try:
        import fitz

        # Use fitz Story API for HTML-to-PDF rendering
        try:
            story = fitz.Story(html_content)
            writer = fitz.DocumentWriter(output_path)
            mediabox = fitz.paper_rect("letter")

            if template_path:
                # Narrow margins matching the narrative template (0.54" L/R, 0.72" T/B)
                # Leave extra space at top/bottom for header/footer
                margin_lr = 0.54 * 72  # ~38.9 pt
                margin_top = 0.72 * 72 + 14  # content starts below header
                margin_bot = 0.72 * 72 + 14  # content ends above footer
                where = mediabox + fitz.Rect(margin_lr, margin_top, -margin_lr, -margin_bot)
            else:
                # Standard 1-inch margins
                where = mediabox + fitz.Rect(72, 72, -72, -72)

            more = True
            while more:
                dev = writer.begin_page(mediabox)
                more, _ = story.place(where)
                story.draw(dev)
                writer.end_page()
            writer.close()

            # Add header/footer to each page if using template
            if template_path:
                _add_header_footer(output_path, doc_model["title"])

        except AttributeError:
            # Older fitz without Story — fall back to text-based PDF
            _write_pdf_text_fallback(doc_model, output_path)

    except ImportError:
        # No fitz available — fall back to text-based PDF
        _write_pdf_text_fallback(doc_model, output_path)


def _add_header_footer(pdf_path, title):
    """Add header and footer text to each page of an existing PDF.
    
    Header: "DocForge — {title}" centered at top
    Footer: "Amazon Confidential" left, "Page X of Y" right
    """
    import fitz

    doc = fitz.open(pdf_path)
    total_pages = len(doc)
    gray = (0.5, 0.5, 0.5)  # RGB for #808080
    margin_lr = 0.54 * 72
    header_y = 0.5 * 72  # Position header text
    footer_y = 11 * 72 - 0.4 * 72  # Position footer text

    header_text = f"DocForge \u2014 {title}"
    # Truncate long titles
    if len(header_text) > 80:
        header_text = header_text[:77] + "..."

    for page_num in range(total_pages):
        page = doc[page_num]

        # Header — centered
        page.insert_text(
            fitz.Point(margin_lr, header_y),
            header_text,
            fontsize=9,
            fontname="helv",
            color=gray,
        )

        # Footer left — "Amazon Confidential"
        page.insert_text(
            fitz.Point(margin_lr, footer_y),
            "Amazon Confidential",
            fontsize=9,
            fontname="helv",
            color=gray,
        )

        # Footer right — "Page X of Y"
        page_text = f"Page {page_num + 1} of {total_pages}"
        # Right-align: estimate text width (~4.5 pts per char at 9pt)
        text_width = len(page_text) * 4.5
        right_x = 8.5 * 72 - margin_lr - text_width
        page.insert_text(
            fitz.Point(right_x, footer_y),
            page_text,
            fontsize=9,
            fontname="helv",
            color=gray,
        )

    doc.save(pdf_path, incremental=True, encryption=0)
    doc.close()


def _write_pdf_text_fallback(doc_model, output_path):
    """Simple text-based PDF generation as fallback."""
    import fitz

    doc = fitz.open()
    page = doc.new_page(width=612, height=792)  # Letter size
    y = 52  # Start at ~0.72" from top
    margin = 39  # ~0.54" side margins
    page_width = 612
    content_width = page_width - 2 * margin

    fontsize_map = {
        "heading": {1: 16, 2: 13, 3: 11, 4: 11},
        "paragraph": 11,
        "bullet": 11,
        "code": 9.5,
    }

    def new_page():
        nonlocal page, y
        page = doc.new_page(width=612, height=792)
        y = 52

    for block in doc_model["blocks"]:
        btype = block["type"]

        if y > 740:
            new_page()

        if btype == "heading":
            level = block.get("level", 1)
            size = fontsize_map["heading"].get(level, 11)
            y += 12  # space before
            page.insert_text(
                fitz.Point(margin, y),
                block["text"],
                fontsize=size,
                fontname="helv",
            )
            y += size * 1.4

        elif btype == "paragraph":
            text = block["text"]
            words = text.split()
            line = ""
            for word in words:
                test = f"{line} {word}".strip()
                # Approximate character width for Calibri 11pt
                if len(test) * 5.2 > content_width:
                    page.insert_text(
                        fitz.Point(margin, y), line, fontsize=11, fontname="helv"
                    )
                    y += 14
                    if y > 740:
                        new_page()
                    line = word
                else:
                    line = test
            if line:
                page.insert_text(fitz.Point(margin, y), line, fontsize=11, fontname="helv")
                y += 14
            y += 6  # space after paragraph

        elif btype == "bullet":
            indent = block.get("level", 0) * 18
            text = f"\u2022 {block['text']}"
            page.insert_text(
                fitz.Point(margin + 18 + indent, y),
                text,
                fontsize=11,
                fontname="helv",
            )
            y += 14

        elif btype == "numbered":
            indent = block.get("level", 0) * 18
            page.insert_text(
                fitz.Point(margin + 18 + indent, y),
                block["text"],
                fontsize=11,
                fontname="helv",
            )
            y += 14

        elif btype == "code":
            for code_line in block["text"].split("\n"):
                if y > 740:
                    new_page()
                page.insert_text(
                    fitz.Point(margin, y), code_line, fontsize=9.5, fontname="cour"
                )
                y += 12
            y += 6

    doc.save(output_path)
    doc.close()
