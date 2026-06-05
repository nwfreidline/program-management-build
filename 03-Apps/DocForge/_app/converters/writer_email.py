"""Write internal document model to .eml email format."""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime
import html as html_lib


def write_eml(doc_model, output_path, subject=None, to_addr="", from_addr="", cc_addr=""):
    """Convert document model to an .eml file that Outlook can open.
    
    Args:
        doc_model: The internal document dict
        output_path: Where to save the .eml
        subject: Email subject (defaults to doc title)
        to_addr: Recipient address(es)
        from_addr: Sender address
        cc_addr: CC address(es)
    """
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject or doc_model["title"]
    msg["To"] = to_addr
    msg["From"] = from_addr
    msg["CC"] = cc_addr
    msg["Date"] = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0000")

    # Generate plain text version
    plain_lines = []
    num_counter = 0
    prev_was_numbered = False
    for block in doc_model["blocks"]:
        btype = block["type"]
        if btype != "numbered" and prev_was_numbered:
            num_counter = 0
            prev_was_numbered = False
        if btype == "heading":
            plain_lines.append(f"\n{block['text'].upper()}\n")
        elif btype == "paragraph":
            plain_lines.append(block["text"])
            plain_lines.append("")
        elif btype == "bullet":
            indent = "  " * block.get("level", 0)
            plain_lines.append(f"{indent}• {block['text']}")
        elif btype == "numbered":
            num_counter += 1
            prev_was_numbered = True
            indent = "  " * block.get("level", 0)
            plain_lines.append(f"{indent}{num_counter}. {block['text']}")
        elif btype == "table":
            for row in block["rows"]:
                plain_lines.append(" | ".join(row))
            plain_lines.append("")
        elif btype == "code":
            plain_lines.append(block["text"])
            plain_lines.append("")

    plain_text = "\n".join(plain_lines)

    # Generate HTML version
    html_parts = [
        "<html><body>",
        '<div style="font-family: Calibri, Arial, sans-serif; font-size: 11pt; line-height: 1.5;">',
    ]

    for block in doc_model["blocks"]:
        btype = block["type"]
        if btype == "heading":
            level = min(block.get("level", 1), 4)
            html_parts.append(f"<h{level}>{html_lib.escape(block['text'])}</h{level}>")
        elif btype == "paragraph":
            text = html_lib.escape(block["text"]).replace("\n", "<br>")
            html_parts.append(f"<p>{text}</p>")
        elif btype == "bullet":
            html_parts.append(f"<p style='margin-left:{20 * (block.get('level',0)+1)}px'>\u2022 {html_lib.escape(block['text'])}</p>")
        elif btype == "numbered":
            html_parts.append(f"<p style='margin-left:{20 * (block.get('level',0)+1)}px'>{html_lib.escape(block['text'])}</p>")
        elif btype == "table":
            rows = block["rows"]
            if rows:
                html_parts.append('<table style="border-collapse:collapse;margin:8px 0">')
                html_parts.append("<tr>")
                for cell in rows[0]:
                    html_parts.append(f'<th style="border:1px solid #ccc;padding:6px 10px;background:#f5f5f5">{html_lib.escape(cell)}</th>')
                html_parts.append("</tr>")
                for row in rows[1:]:
                    html_parts.append("<tr>")
                    for cell in row:
                        html_parts.append(f'<td style="border:1px solid #ccc;padding:6px 10px">{html_lib.escape(cell)}</td>')
                    html_parts.append("</tr>")
                html_parts.append("</table>")
        elif btype == "code":
            html_parts.append(f'<pre style="background:#f5f5f5;padding:10px;font-family:Consolas,monospace">{html_lib.escape(block["text"])}</pre>')

    html_parts.extend(["</div>", "</body></html>"])
    html_content = "\n".join(html_parts)

    # Attach both versions — email clients pick the best one
    msg.attach(MIMEText(plain_text, "plain"))
    msg.attach(MIMEText(html_content, "html"))

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(msg.as_string())
