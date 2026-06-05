"""
Sync Projects.md + Tasks.md + To Growth Tracker.md → Project Board.md

Generates an Obsidian Kanban board that reflects all tracked items.

Logic:
  - Sources (Projects.md, Tasks.md, To Growth Tracker) define WHAT items exist
  - Project Board defines WHERE items sit (column placement is preserved)
  - New items from sources appear in "To Do"
  - Items checked [x] at top level in sources → auto-move to "Done"
  - Items in To Growth Tracker [x] → "Done" (fed to Growth Manager)
  - Manual column moves (In Progress, On Hold) are preserved across syncs
  - Sub-tasks from Projects.md are carried onto board cards

Run manually or triggered via Kiro hook on source file edits.
"""

import re
from pathlib import Path

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

TRACKING_DIR = Path(__file__).parent / "Tracking"
PROJECTS_FILE = TRACKING_DIR / "Projects.md"
TASKS_FILE = TRACKING_DIR / "Tasks.md"
GROWTH_TRACKER_FILE = TRACKING_DIR / "To Growth Tracker.md"
BOARD_FILE = TRACKING_DIR / "Project Board.md"


# ---------------------------------------------------------------------------
# Parsing — Projects.md
# ---------------------------------------------------------------------------

def parse_projects(content: str) -> list[dict]:
    """Parse Projects.md into a list of card dicts.

    Each card: {
        "title": str,
        "checked": bool,
        "subtasks": [{"checked": bool, "text": str}, ...],
        "source": "projects",
        "source_section": str,  # e.g. "Backlog", "In Progress"
    }
    """
    cards = []
    lines = content.strip().splitlines()
    current_card = None
    current_section = ""

    for line in lines:
        # Detect section headers
        section_match = re.match(r'^###\s+(.+)$', line)
        if section_match:
            if current_card is not None:
                cards.append(current_card)
                current_card = None
            current_section = section_match.group(1).strip()
            continue

        top_match = re.match(r'^- \[([ x])\] (.+)$', line)
        sub_match = re.match(r'^\t- \[([ x])\] (.+)$', line)

        if top_match:
            if current_card is not None:
                cards.append(current_card)

            checked = top_match.group(1) == 'x'
            raw_title = top_match.group(2).strip()
            display_title = _clean_display_text(raw_title)

            current_card = {
                "title": display_title,
                "checked": checked,
                "subtasks": [],
                "source": "projects",
                "source_section": current_section,
            }

        elif sub_match and current_card is not None:
            checked = sub_match.group(1) == 'x'
            raw_text = sub_match.group(2).strip()
            # Skip reference-only sub-items (>> "path")
            if re.match(r'^>>\s*[("]*[A-Z]:\\', raw_text):
                continue
            display_text = _clean_display_text(raw_text)
            if display_text:
                current_card["subtasks"].append({
                    "checked": checked,
                    "text": display_text,
                })

    if current_card is not None:
        cards.append(current_card)

    return cards


# ---------------------------------------------------------------------------
# Parsing — Tasks.md
# ---------------------------------------------------------------------------

def parse_tasks(content: str) -> list[dict]:
    """Parse Tasks.md into card dicts.

    Tasks are flat (no sub-tasks). Tagged with source="tasks".
    """
    cards = []
    lines = content.strip().splitlines()
    current_section = ""

    for line in lines:
        section_match = re.match(r'^###\s+(.+)$', line)
        if section_match:
            current_section = section_match.group(1).strip()
            continue

        top_match = re.match(r'^- \[([ x])\] (.+)$', line)
        if top_match:
            checked = top_match.group(1) == 'x'
            raw_title = top_match.group(2).strip()
            if not raw_title:
                continue
            display_title = _clean_display_text(raw_title)
            if display_title:
                cards.append({
                    "title": display_title,
                    "checked": checked,
                    "subtasks": [],
                    "source": "tasks",
                    "source_section": current_section,
                })

    return cards


# ---------------------------------------------------------------------------
# Parsing — To Growth Tracker.md
# ---------------------------------------------------------------------------

def parse_growth_tracker(content: str) -> list[dict]:
    """Parse To Growth Tracker for checked items (fed to Growth Manager).

    These are always treated as "Done" items.
    """
    cards = []
    lines = content.strip().splitlines()
    current_card = None

    for line in lines:
        top_match = re.match(r'^- \[([ x])\] (.+)$', line)
        sub_match = re.match(r'^\t- \[([ x])\] (.+)$', line)

        if top_match:
            if current_card is not None:
                cards.append(current_card)

            checked = top_match.group(1) == 'x'
            raw_title = top_match.group(2).strip()
            display_title = _clean_display_text(raw_title)
            if display_title:
                current_card = {
                    "title": display_title,
                    "checked": checked,
                    "subtasks": [],
                    "source": "growth_tracker",
                    "source_section": "",
                }
            else:
                current_card = None

        elif sub_match and current_card is not None:
            checked = sub_match.group(1) == 'x'
            raw_text = sub_match.group(2).strip()
            if re.match(r'^>>\s*[("]*[A-Z]:\\', raw_text):
                continue
            display_text = _clean_display_text(raw_text)
            if display_text:
                current_card["subtasks"].append({
                    "checked": checked,
                    "text": display_text,
                })

    if current_card is not None:
        cards.append(current_card)

    return cards


# ---------------------------------------------------------------------------
# Parsing — Existing Board
# ---------------------------------------------------------------------------

def parse_board(content: str) -> dict[str, list[dict]]:
    """Parse existing Project Board into columns.

    Returns: {"To Do": [...], "In Progress": [...], "On Hold": [...], "Done": [...]}
    Each item is a card dict with title, checked, subtasks.
    """
    columns = {"To Do": [], "In Progress": [], "On Hold": [], "Done": []}
    current_column = None
    current_card = None
    in_settings = False

    for line in content.splitlines():
        stripped = line.strip()

        # Skip kanban settings block
        if stripped.startswith("%%"):
            in_settings = not in_settings
            continue
        if in_settings or stripped.startswith("```") or stripped.startswith("{\"kanban"):
            continue

        # Skip frontmatter
        if stripped == "---" or stripped.startswith("kanban-plugin"):
            continue

        # Detect column headers
        col_match = re.match(r'^## (.+)$', stripped)
        if col_match:
            # Flush current card
            if current_card is not None and current_column is not None:
                columns[current_column].append(current_card)
                current_card = None

            col_name = col_match.group(1).strip()
            if col_name in columns:
                current_column = col_name
            else:
                current_column = None
            continue

        if current_column is None:
            continue

        # Detect indentation level — tab or spaces
        is_sub = line.startswith("\t") or (line.startswith("  ") and not line.startswith("- "))
        top_match = re.match(r'^- \[([ x])\] (.+)$', stripped)

        if top_match and not is_sub:
            if current_card is not None:
                columns[current_column].append(current_card)

            checked = top_match.group(1) == 'x'
            title = top_match.group(2).strip()
            # Strip completion date markers and source tags
            title = re.sub(r'\s*✅\s*\d{4}-\d{2}-\d{2}\s*$', '', title).strip()
            title = re.sub(r'\s*`task`\s*$', '', title).strip()
            title = re.sub(r'\s*✅→Growth\s*$', '', title).strip()
            current_card = {
                "title": title,
                "checked": checked,
                "subtasks": [],
            }

        elif top_match and is_sub and current_card is not None:
            checked = top_match.group(1) == 'x'
            text = top_match.group(2).strip()
            text = re.sub(r'\s*✅\s*\d{4}-\d{2}-\d{2}\s*$', '', text).strip()
            text = re.sub(r'\s*`task`\s*$', '', text).strip()
            current_card["subtasks"].append({"checked": checked, "text": text})

    # Flush last card
    if current_card is not None and current_column is not None:
        columns[current_column].append(current_card)

    return columns


# ---------------------------------------------------------------------------
# Reconciliation
# ---------------------------------------------------------------------------

def _normalize_title(title: str) -> str:
    """Normalize a title for comparison (lowercase, strip punctuation)."""
    return re.sub(r'[^\w\s]', '', title.lower()).strip()


def reconcile(
    source_cards: list[dict],
    existing_board: dict[str, list[dict]],
) -> dict[str, list[dict]]:
    """Reconcile source items with existing board state.

    Rules:
      1. Items already on the board stay in their current column
         (unless they're now checked [x] in source → move to Done)
      2. New items (in sources but not on board) go to appropriate column
      3. Items from growth_tracker (checked) always go to "Done"
      4. Sub-tasks are updated from source (source is authoritative for content)
      5. Board-only items (not in any source) are preserved in their column
    """
    # Build a lookup of all items currently on the board by normalized title
    board_placement = {}  # normalized_title → column_name
    board_cards = {}      # normalized_title → card dict

    for col_name, cards in existing_board.items():
        for card in cards:
            key = _normalize_title(card["title"])
            if key:  # skip empty
                board_placement[key] = col_name
                board_cards[key] = card

    # Build the new board
    new_board = {"To Do": [], "In Progress": [], "On Hold": [], "Done": []}

    # Track which items we've placed (to avoid duplicates)
    placed_keys = set()

    for source_card in source_cards:
        key = _normalize_title(source_card["title"])
        if not key or key in placed_keys:
            continue
        placed_keys.add(key)

        # Determine target column
        if source_card["source"] == "growth_tracker" and source_card["checked"]:
            target_col = "Done"
        elif source_card["checked"]:
            target_col = "Done"
        elif key in board_placement:
            # Already on board — keep in current column
            current_col = board_placement[key]
            if current_col == "Done" and not source_card["checked"]:
                # Re-opened item — move back to To Do
                target_col = "To Do"
            else:
                target_col = current_col
        else:
            # New item — determine initial placement from source section
            if source_card["source"] == "projects":
                section = source_card["source_section"].lower()
                if "in progress" in section:
                    target_col = "In Progress"
                elif "pending" in section:
                    target_col = "To Do"
                else:
                    target_col = "To Do"
            else:
                target_col = "To Do"

        # Build the card for the board (use source sub-tasks as authoritative)
        board_card = {
            "title": source_card["title"],
            "checked": source_card["checked"],
            "subtasks": source_card["subtasks"],
        }

        # Add source tag for tasks (to distinguish from projects)
        if source_card["source"] == "tasks":
            board_card["source_tag"] = "task"
        elif source_card["source"] == "growth_tracker":
            board_card["source_tag"] = "growth"

        new_board[target_col].append(board_card)

    # Preserve board-only items (manually added to board, not in any source)
    for col_name, cards in existing_board.items():
        for card in cards:
            key = _normalize_title(card["title"])
            if key and key not in placed_keys:
                # Check if this board-only item is actually a sub-task of
                # a source card (old board may have promoted sub-tasks to cards)
                is_subtask = False
                for source_card in source_cards:
                    for sub in source_card.get("subtasks", []):
                        if _normalize_title(sub["text"]) == key:
                            is_subtask = True
                            break
                    if is_subtask:
                        break

                if not is_subtask:
                    placed_keys.add(key)
                    new_board[col_name].append(card)

    return new_board


# ---------------------------------------------------------------------------
# Rendering
# ---------------------------------------------------------------------------

def render_card(card: dict) -> list[str]:
    """Render a card dict into kanban markdown lines."""
    check = "x" if card.get("checked") else " "
    title = card["title"]

    # Add source indicator
    tag = card.get("source_tag")
    if tag == "task":
        title = f"{title} `task`"
    elif tag == "growth":
        title = f"{title} ✅→Growth"

    lines = [f"- [{check}] {title}"]
    for sub in card.get("subtasks", []):
        sub_check = "x" if sub["checked"] else " "
        lines.append(f"\t- [{sub_check}] {sub['text']}")
    return lines


def generate_board(board: dict[str, list[dict]]) -> str:
    """Generate Obsidian Kanban markdown from board dict."""
    lines = [
        "---",
        "",
        "kanban-plugin: board",
        "",
        "---",
        "",
    ]

    for col_name in ["To Do", "In Progress", "On Hold", "Done"]:
        lines.append(f"## {col_name}")
        lines.append("")
        for card in board.get(col_name, []):
            lines.extend(render_card(card))
        lines.append("")

    lines.append("")
    lines.append("%% kanban:settings")
    lines.append("```")
    lines.append('{"kanban-plugin":"board","list-collapse":[false,false,false,false]}')
    lines.append("```")
    lines.append("%%")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Utilities
# ---------------------------------------------------------------------------

def _clean_display_text(raw_text: str) -> str:
    """Strip file paths, markdown links, and reference markers for clean display."""
    text = re.sub(r'\s*\[Markdown File\]\([^)]*\)', '', raw_text)
    text = re.sub(r'\s*\([A-Z]:\\[^)]*\)', '', text)
    text = re.sub(r'\s*>>\s*"?[A-Z]:\\[^"]*"?\s*$', '', text)
    text = re.sub(r'\s*✅\s*\d{4}-\d{2}-\d{2}\s*$', '', text)
    return text.strip()


# ---------------------------------------------------------------------------
# Main Sync
# ---------------------------------------------------------------------------

def sync():
    """Main sync function — reads all sources, reconciles, writes board."""
    # Collect all source cards
    all_cards = []

    if PROJECTS_FILE.exists():
        content = PROJECTS_FILE.read_text(encoding="utf-8")
        all_cards.extend(parse_projects(content))

    if TASKS_FILE.exists():
        content = TASKS_FILE.read_text(encoding="utf-8")
        all_cards.extend(parse_tasks(content))

    if GROWTH_TRACKER_FILE.exists():
        content = GROWTH_TRACKER_FILE.read_text(encoding="utf-8")
        if content.strip():
            all_cards.extend(parse_growth_tracker(content))

    # Parse existing board for column preservation
    existing_board = {"To Do": [], "In Progress": [], "On Hold": [], "Done": []}
    if BOARD_FILE.exists():
        board_content = BOARD_FILE.read_text(encoding="utf-8")
        existing_board = parse_board(board_content)

    # Reconcile sources with board state
    new_board = reconcile(all_cards, existing_board)

    # Count items per column
    counts = {col: len(cards) for col, cards in new_board.items()}

    # Write board
    board_output = generate_board(new_board)
    BOARD_FILE.write_text(board_output, encoding="utf-8")

    print(
        f"✓ Project Board synced: "
        f"{counts['To Do']} to-do, "
        f"{counts['In Progress']} in progress, "
        f"{counts['On Hold']} on hold, "
        f"{counts['Done']} done"
    )


if __name__ == "__main__":
    sync()
