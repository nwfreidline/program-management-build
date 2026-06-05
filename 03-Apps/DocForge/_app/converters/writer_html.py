"""Write internal document model to HTML."""

import html


def write_html(doc_model, output_path):
    """Convert document model to an HTML file."""
    parts = [
        "<!DOCTYPE html>",
        "<html>",
        "<head>",
        f"  <title>{html.escape(doc_model['title'])}</title>",
        '  <meta charset="utf-8">',
        "  <style>",
        "    body { font-family: Calibri, Arial, sans-serif; font-size: 10pt; max-width: 900px; margin: 40px auto; padding: 0 20px; line-height: 1.15; color: #000; }",
        "    h1 { font-size: 14pt; font-weight: bold; color: #000; margin-top: 10pt; margin-bottom: 2pt; }",
        "    h2 { font-size: 12pt; font-weight: bold; color: #000; margin-top: 10pt; margin-bottom: 2pt; }",
        "    h3 { font-size: 10pt; font-weight: bold; color: #000; margin-top: 8pt; margin-bottom: 2pt; }",
        "    h4 { font-size: 10pt; font-weight: bold; font-style: italic; color: #000; margin-top: 8pt; margin-bottom: 2pt; }",
        "    p { font-size: 10pt; margin-top: 0; margin-bottom: 6pt; color: #000; }",
        "    table { border-collapse: collapse; width: 100%; margin: 6pt 0; font-size: 10pt; }",
        "    th, td { border: 1px solid #BFBFBF; padding: 3pt 5pt; text-align: left; vertical-align: top; color: #000; }",
        "    th { background: #F2F2F2; font-weight: bold; }",
        "    pre { font-family: Consolas, monospace; font-size: 9pt; background: #F8F8F8; padding: 6pt; border: 1px solid #E0E0E0; overflow-x: auto; }",
        "    code { font-family: Consolas, monospace; }",
        "    ul { margin: 0 0 6pt 0; padding-left: 0.25in; }",
        "    li { font-size: 10pt; margin-bottom: 2pt; color: #000; }",
        "  </style>",
        "</head>",
        "<body>",
    ]

    in_list = False
    in_ordered = False

    for block in doc_model["blocks"]:
        btype = block["type"]

        # Close lists if we're leaving list context
        if btype != "bullet" and in_list:
            parts.append("</ul>")
            in_list = False
        if btype != "numbered" and in_ordered:
            parts.append("</ol>")
            in_ordered = False

        if btype == "heading":
            level = min(block.get("level", 1), 6)
            parts.append(f"<h{level}>{html.escape(block['text'])}</h{level}>")

        elif btype == "paragraph":
            text = html.escape(block["text"]).replace("\n", "<br>")
            parts.append(f"<p>{text}</p>")

        elif btype == "bullet":
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"  <li>{html.escape(block['text'])}</li>")

        elif btype == "numbered":
            if not in_ordered:
                parts.append("<ol>")
                in_ordered = True
            parts.append(f"  <li>{html.escape(block['text'])}</li>")

        elif btype == "table":
            rows = block["rows"]
            if not rows:
                continue
            parts.append("<table>")
            # Header row
            parts.append("  <tr>")
            for cell in rows[0]:
                parts.append(f"    <th>{html.escape(cell)}</th>")
            parts.append("  </tr>")
            # Data rows
            for row in rows[1:]:
                parts.append("  <tr>")
                for cell in row:
                    parts.append(f"    <td>{html.escape(cell)}</td>")
                parts.append("  </tr>")
            parts.append("</table>")

        elif btype == "code":
            lang = block.get("language", "")
            escaped = html.escape(block["text"])
            parts.append(f'<pre><code class="language-{lang}">{escaped}</code></pre>')

    if in_list:
        parts.append("</ul>")
    if in_ordered:
        parts.append("</ol>")

    parts.extend(["</body>", "</html>"])

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(parts))
