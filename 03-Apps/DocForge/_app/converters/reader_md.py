"""Read Markdown files into the internal document model."""

import re


def _strip_md_inline(text):
    """Remove inline markdown formatting from text.
    
    Strips: **bold**, *italic*, __bold__, _italic_, ~~strikethrough~~,
    `inline code`, [link text](url), [link text][ref], <url>, ![alt](img),
    HTML tags, and escaped characters.
    """
    # First: protect escaped characters by replacing with placeholders
    # \* → placeholder, then restore as literal * at the end
    _escapes = {}
    _counter = [0]
    
    def _protect_escape(m):
        key = f"\x00ESC{_counter[0]}\x00"
        _escapes[key] = m.group(1)
        _counter[0] += 1
        return key
    
    text = re.sub(r"\\([\\`*_{}\[\]()#+\-.!~>|])", _protect_escape, text)
    
    # Images: ![alt](url) → alt
    text = re.sub(r"!\[([^\]]*)\]\([^)]*\)", r"\1", text)
    
    # Links: [text](url) → text
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    
    # Reference links: [text][ref] → text
    text = re.sub(r"\[([^\]]*)\]\[[^\]]*\]", r"\1", text)
    
    # Autolinks and angle-bracket URLs: <url> → url
    text = re.sub(r"<(https?://[^>]+)>", r"\1", text)
    
    # HTML tags: <tag> or </tag> or <br/> (simple tags without attributes)
    text = re.sub(r"</?\s*[a-zA-Z][a-zA-Z0-9]*\s*/?>", "", text)
    
    # Remaining angle brackets: <text> → text
    text = re.sub(r"<([^>]+)>", r"\1", text)
    
    # Inline code: `code` → code
    text = re.sub(r"`([^`]*)`", r"\1", text)
    
    # Bold+italic: ***text*** or ___text___
    text = re.sub(r"\*{3}(.+?)\*{3}", r"\1", text)
    text = re.sub(r"_{3}(.+?)_{3}", r"\1", text)
    
    # Bold: **text** or __text__
    text = re.sub(r"\*{2}(.+?)\*{2}", r"\1", text)
    text = re.sub(r"_{2}(.+?)_{2}", r"\1", text)
    
    # Italic: *text* or _text_ (but not mid-word underscores like file_name)
    text = re.sub(r"(?<!\w)\*(.+?)\*(?!\w)", r"\1", text)
    text = re.sub(r"(?<!\w)_(.+?)_(?!\w)", r"\1", text)
    
    # Strikethrough: ~~text~~
    text = re.sub(r"~~(.+?)~~", r"\1", text)
    
    # Restore escaped characters as their literal values
    for key, char in _escapes.items():
        text = text.replace(key, char)
    
    return text


def read_markdown(filepath):
    """Parse a markdown file into a structured document dict.
    
    Returns:
        dict with keys:
            - title: str (first H1 or filename)
            - blocks: list of dicts, each with:
                - type: 'heading' | 'paragraph' | 'bullet' | 'table' | 'code'
                - level: int (for headings, 1-4)
                - text: str
                - rows: list of lists (for tables)
                - language: str (for code blocks)
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = []
    title = None
    lines = content.split("\n")
    i = 0

    while i < len(lines):
        line = lines[i]

        # Blank line — skip
        if not line.strip():
            i += 1
            continue

        # Fenced code block
        if line.strip().startswith("```"):
            lang = line.strip()[3:].strip()
            code_lines = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i])
                i += 1
            blocks.append({
                "type": "code",
                "text": "\n".join(code_lines),
                "language": lang or "text",
            })
            i += 1
            continue

        # Heading
        heading_match = re.match(r"^(#{1,4})\s+(.+)$", line)
        if heading_match:
            level = len(heading_match.group(1))
            text = _strip_md_inline(heading_match.group(2).strip())
            if level == 1 and title is None:
                title = text
            blocks.append({"type": "heading", "level": level, "text": text})
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^[-*_]{3,}\s*$", line):
            i += 1
            continue

        # Table
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|[-:\s|]+\|\s*$", lines[i + 1]):
            rows = []
            # Header row
            header = [_strip_md_inline(c.strip()) for c in line.strip().strip("|").split("|")]
            rows.append(header)
            i += 2  # skip separator
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                row = [_strip_md_inline(c.strip()) for c in lines[i].strip().strip("|").split("|")]
                rows.append(row)
                i += 1
            blocks.append({"type": "table", "rows": rows})
            continue

        # Bullet / list item
        bullet_match = re.match(r"^(\s*)[*\-+]\s+(.+)$", line)
        if bullet_match:
            indent = len(bullet_match.group(1))
            level = indent // 2
            text = bullet_match.group(2).strip()
            # Collect continuation lines
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(\s*)[*\-+#|]", lines[i]) and not lines[i].strip().startswith("```"):
                text += " " + lines[i].strip()
                i += 1
            blocks.append({"type": "bullet", "text": _strip_md_inline(text), "level": level})
            continue

        # Numbered list
        num_match = re.match(r"^(\s*)\d+[.)]\s+(.+)$", line)
        if num_match:
            indent = len(num_match.group(1))
            level = indent // 2
            text = num_match.group(2).strip()
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(r"^(\s*)[*\-+#|\d]", lines[i]) and not lines[i].strip().startswith("```"):
                text += " " + lines[i].strip()
                i += 1
            blocks.append({"type": "numbered", "text": _strip_md_inline(text), "level": level})
            continue

        # Paragraph — collect consecutive non-special lines
        para_lines = [line.strip()]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^[#|*\-+`]", lines[i]) and not re.match(r"^\d+[.)]\s", lines[i]):
            para_lines.append(lines[i].strip())
            i += 1
        blocks.append({"type": "paragraph", "text": _strip_md_inline(" ".join(para_lines))})

    return {
        "title": title or "Untitled",
        "blocks": blocks,
    }
