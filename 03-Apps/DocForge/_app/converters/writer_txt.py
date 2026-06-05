"""Write internal document model to plain text."""


def write_txt(doc_model, output_path):
    """Convert document model to a plain text file."""
    lines = []
    num_counter = 0
    prev_was_numbered = False

    for block in doc_model["blocks"]:
        btype = block["type"]

        # Reset number counter when leaving a numbered list
        if btype != "numbered" and prev_was_numbered:
            num_counter = 0
            prev_was_numbered = False

        if btype == "heading":
            text = block["text"]
            lines.append(text.upper())
            lines.append("=" * len(text))
            lines.append("")

        elif btype == "paragraph":
            lines.append(block["text"])
            lines.append("")

        elif btype == "bullet":
            indent = "  " * block.get("level", 0)
            lines.append(f"{indent}* {block['text']}")

        elif btype == "numbered":
            num_counter += 1
            prev_was_numbered = True
            indent = "  " * block.get("level", 0)
            lines.append(f"{indent}{num_counter}. {block['text']}")

        elif btype == "table":
            rows = block["rows"]
            if not rows:
                continue
            # Calculate column widths
            num_cols = max(len(r) for r in rows)
            widths = [0] * num_cols
            for row in rows:
                for i, cell in enumerate(row):
                    widths[i] = max(widths[i], len(cell))

            # Format rows
            for r_idx, row in enumerate(rows):
                padded = []
                for i in range(num_cols):
                    val = row[i] if i < len(row) else ""
                    padded.append(val.ljust(widths[i]))
                lines.append("  ".join(padded))
                if r_idx == 0:
                    lines.append("  ".join("-" * w for w in widths))
            lines.append("")

        elif btype == "code":
            lines.append("---")
            lines.append(block["text"])
            lines.append("---")
            lines.append("")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
