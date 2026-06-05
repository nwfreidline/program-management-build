"""Write internal document model to Markdown."""


def write_markdown(doc_model, output_path):
    """Convert document model to a Markdown file."""
    lines = []

    for block in doc_model["blocks"]:
        btype = block["type"]

        if btype == "heading":
            prefix = "#" * block.get("level", 1)
            lines.append(f"{prefix} {block['text']}")
            lines.append("")

        elif btype == "paragraph":
            lines.append(block["text"])
            lines.append("")

        elif btype == "bullet":
            indent = "  " * block.get("level", 0)
            lines.append(f"{indent}- {block['text']}")

        elif btype == "numbered":
            indent = "  " * block.get("level", 0)
            lines.append(f"{indent}1. {block['text']}")

        elif btype == "table":
            rows = block["rows"]
            if not rows:
                continue
            # Header
            lines.append("| " + " | ".join(rows[0]) + " |")
            lines.append("| " + " | ".join(["---"] * len(rows[0])) + " |")
            for row in rows[1:]:
                # Pad row to match header length
                padded = row + [""] * (len(rows[0]) - len(row))
                lines.append("| " + " | ".join(padded) + " |")
            lines.append("")

        elif btype == "code":
            lang = block.get("language", "")
            lines.append(f"```{lang}")
            lines.append(block["text"])
            lines.append("```")
            lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
