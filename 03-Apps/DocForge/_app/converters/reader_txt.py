"""Read plain text files into the internal document model."""

import os


def read_txt(filepath):
    """Parse a plain text file into a structured document dict.
    
    Treats each paragraph (separated by blank lines) as a block.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    blocks = []
    title = os.path.splitext(os.path.basename(filepath))[0]

    paragraphs = content.split("\n\n")
    for para in paragraphs:
        text = para.strip()
        if text:
            blocks.append({"type": "paragraph", "text": text})

    return {
        "title": title,
        "blocks": blocks,
    }
