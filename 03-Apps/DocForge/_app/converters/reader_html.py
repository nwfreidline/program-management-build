"""Read HTML files into the internal document model."""

from bs4 import BeautifulSoup


def read_html(filepath):
    """Parse an HTML file into a structured document dict."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    return parse_html_string(content)


def parse_html_string(html_content):
    """Parse an HTML string into a structured document dict."""
    soup = BeautifulSoup(html_content, "html.parser")
    blocks = []
    title = None

    # Try to get title from <title> tag
    title_tag = soup.find("title")
    if title_tag:
        title = title_tag.get_text(strip=True)

    # Process body content (or whole doc if no body)
    body = soup.find("body") or soup

    for element in body.children:
        if not hasattr(element, "name") or element.name is None:
            # Text node
            text = str(element).strip()
            if text:
                blocks.append({"type": "paragraph", "text": text})
            continue

        name = element.name.lower()

        # Headings
        if name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            level = int(name[1])
            text = element.get_text(strip=True)
            if text:
                if level == 1 and title is None:
                    title = text
                blocks.append({"type": "heading", "level": min(level, 4), "text": text})

        # Lists
        elif name in ("ul", "ol"):
            for li in element.find_all("li", recursive=False):
                text = li.get_text(strip=True)
                if text:
                    blocks.append({"type": "bullet", "text": text, "level": 0})

        # Tables
        elif name == "table":
            rows = []
            for tr in element.find_all("tr"):
                cells = []
                for td in tr.find_all(["td", "th"]):
                    cells.append(td.get_text(strip=True))
                if cells:
                    rows.append(cells)
            if rows:
                blocks.append({"type": "table", "rows": rows})

        # Pre/code blocks
        elif name == "pre":
            code = element.find("code")
            text = code.get_text() if code else element.get_text()
            lang = ""
            if code and code.get("class"):
                for cls in code["class"]:
                    if cls.startswith("language-"):
                        lang = cls[9:]
            blocks.append({"type": "code", "text": text, "language": lang or "text"})

        # Paragraphs and divs
        elif name in ("p", "div"):
            text = element.get_text(strip=True)
            if text:
                blocks.append({"type": "paragraph", "text": text})

    return {
        "title": title or "Untitled",
        "blocks": blocks,
    }
