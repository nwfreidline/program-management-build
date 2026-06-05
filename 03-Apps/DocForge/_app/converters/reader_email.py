"""Read email files (.msg and .eml) into the internal document model."""

import os
import email
from email import policy


def read_msg(filepath):
    """Parse an Outlook .msg file into a structured document dict."""
    import extract_msg

    msg = extract_msg.Message(filepath)
    blocks = []

    # Build metadata header
    meta_lines = []
    if msg.sender:
        meta_lines.append(f"From: {msg.sender}")
    if msg.to:
        meta_lines.append(f"To: {msg.to}")
    if msg.cc:
        meta_lines.append(f"CC: {msg.cc}")
    if msg.date:
        meta_lines.append(f"Date: {msg.date}")
    if msg.subject:
        meta_lines.append(f"Subject: {msg.subject}")

    if meta_lines:
        blocks.append({"type": "paragraph", "text": "\n".join(meta_lines)})

    # Body content
    body = msg.body
    if body:
        paragraphs = body.split("\n\n")
        for para in paragraphs:
            text = para.strip()
            if text:
                blocks.append({"type": "paragraph", "text": text})

    # Note attachments
    if msg.attachments:
        blocks.append({"type": "heading", "level": 2, "text": "Attachments"})
        for att in msg.attachments:
            name = att.longFilename or att.shortFilename or "unnamed"
            blocks.append({"type": "bullet", "text": name, "level": 0})

    title = msg.subject or os.path.splitext(os.path.basename(filepath))[0]
    msg.close()

    return {
        "title": title,
        "blocks": blocks,
    }


def read_eml(filepath):
    """Parse an .eml file into a structured document dict."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        msg = email.message_from_file(f, policy=policy.default)

    blocks = []

    # Metadata
    meta_lines = []
    for header in ("From", "To", "CC", "Date", "Subject"):
        val = msg.get(header)
        if val:
            meta_lines.append(f"{header}: {val}")

    if meta_lines:
        blocks.append({"type": "paragraph", "text": "\n".join(meta_lines)})

    # Body — prefer plain text, fall back to HTML
    body = msg.get_body(preferencelist=("plain", "html"))
    if body:
        content = body.get_content()
        content_type = body.get_content_type()

        if content_type == "text/html":
            # Parse HTML body
            from converters.reader_html import parse_html_string
            html_doc = parse_html_string(content)
            blocks.extend(html_doc["blocks"])
        else:
            paragraphs = content.split("\n\n")
            for para in paragraphs:
                text = para.strip()
                if text:
                    blocks.append({"type": "paragraph", "text": text})

    # Note attachments
    attachments = []
    for part in msg.walk():
        if part.get_content_disposition() == "attachment":
            fname = part.get_filename() or "unnamed"
            attachments.append(fname)
    if attachments:
        blocks.append({"type": "heading", "level": 2, "text": "Attachments"})
        for name in attachments:
            blocks.append({"type": "bullet", "text": name, "level": 0})

    title = msg.get("Subject") or os.path.splitext(os.path.basename(filepath))[0]

    return {
        "title": title,
        "blocks": blocks,
    }
