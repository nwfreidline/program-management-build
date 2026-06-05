"""STAR format generation and past-tense verb conversion engine.

This module provides the core logic for converting action items to past tense
and generating structured STAR (Situation, Task, Action, Result) entries.
"""
import re
import uuid
from datetime import datetime

# ---------------------------------------------------------------------------
# Irregular verbs — comprehensive mapping of present → past tense
# ---------------------------------------------------------------------------
IRREGULAR_VERBS = {
    "arise": "arose",
    "awake": "awoke",
    "be": "was",
    "bear": "bore",
    "beat": "beat",
    "become": "became",
    "begin": "began",
    "bend": "bent",
    "bet": "bet",
    "bid": "bid",
    "bind": "bound",
    "bite": "bit",
    "bleed": "bled",
    "blow": "blew",
    "break": "broke",
    "breed": "bred",
    "bring": "brought",
    "broadcast": "broadcast",
    "build": "built",
    "burn": "burned",
    "burst": "burst",
    "buy": "bought",
    "cast": "cast",
    "catch": "caught",
    "choose": "chose",
    "cling": "clung",
    "come": "came",
    "cost": "cost",
    "creep": "crept",
    "cut": "cut",
    "deal": "dealt",
    "dig": "dug",
    "do": "did",
    "draw": "drew",
    "dream": "dreamed",
    "drink": "drank",
    "drive": "drove",
    "eat": "ate",
    "fall": "fell",
    "feed": "fed",
    "feel": "felt",
    "fight": "fought",
    "find": "found",
    "fit": "fit",
    "flee": "fled",
    "fling": "flung",
    "fly": "flew",
    "forbid": "forbade",
    "forecast": "forecast",
    "forget": "forgot",
    "forgive": "forgave",
    "freeze": "froze",
    "get": "got",
    "give": "gave",
    "go": "went",
    "grind": "ground",
    "grow": "grew",
    "hang": "hung",
    "have": "had",
    "hear": "heard",
    "hide": "hid",
    "hit": "hit",
    "hold": "held",
    "hurt": "hurt",
    "keep": "kept",
    "kneel": "knelt",
    "knit": "knit",
    "know": "knew",
    "lay": "laid",
    "lead": "led",
    "lean": "leaned",
    "leap": "leaped",
    "learn": "learned",
    "leave": "left",
    "lend": "lent",
    "let": "let",
    "lie": "lay",
    "light": "lit",
    "lose": "lost",
    "make": "made",
    "mean": "meant",
    "meet": "met",
    "mow": "mowed",
    "overcome": "overcame",
    "overtake": "overtook",
    "pay": "paid",
    "plead": "pleaded",
    "prove": "proved",
    "put": "put",
    "quit": "quit",
    "read": "read",
    "rebuild": "rebuilt",
    "redo": "redid",
    "repay": "repaid",
    "rewrite": "rewrote",
    "rid": "rid",
    "ride": "rode",
    "ring": "rang",
    "rise": "rose",
    "run": "ran",
    "saw": "sawed",
    "say": "said",
    "see": "saw",
    "seek": "sought",
    "sell": "sold",
    "send": "sent",
    "set": "set",
    "sew": "sewed",
    "shake": "shook",
    "shed": "shed",
    "shine": "shone",
    "shoot": "shot",
    "show": "showed",
    "shrink": "shrank",
    "shut": "shut",
    "sing": "sang",
    "sink": "sank",
    "sit": "sat",
    "sleep": "slept",
    "slide": "slid",
    "sling": "slung",
    "slit": "slit",
    "smell": "smelled",
    "sneak": "sneaked",
    "sow": "sowed",
    "speak": "spoke",
    "speed": "sped",
    "spell": "spelled",
    "spend": "spent",
    "spill": "spilled",
    "spin": "spun",
    "spit": "spat",
    "split": "split",
    "spoil": "spoiled",
    "spread": "spread",
    "spring": "sprang",
    "stand": "stood",
    "steal": "stole",
    "stick": "stuck",
    "sting": "stung",
    "stink": "stank",
    "stride": "strode",
    "strike": "struck",
    "string": "strung",
    "strive": "strove",
    "swear": "swore",
    "sweep": "swept",
    "swim": "swam",
    "swing": "swung",
    "take": "took",
    "teach": "taught",
    "tear": "tore",
    "tell": "told",
    "think": "thought",
    "throw": "threw",
    "thrust": "thrust",
    "tread": "trod",
    "undergo": "underwent",
    "understand": "understood",
    "undertake": "undertook",
    "undo": "undid",
    "unwind": "unwound",
    "uphold": "upheld",
    "upset": "upset",
    "wake": "woke",
    "wear": "wore",
    "weave": "wove",
    "weep": "wept",
    "win": "won",
    "wind": "wound",
    "withdraw": "withdrew",
    "withhold": "withheld",
    "withstand": "withstood",
    "wring": "wrung",
    "write": "wrote",
    # Common workplace/tech verbs that are irregular or special
    "outgrow": "outgrew",
    "outrun": "outran",
    "outsell": "outsold",
    "outdo": "outdid",
    "overrun": "overran",
    "oversee": "oversaw",
    "overthrow": "overthrew",
    "rerun": "reran",
    "resell": "resold",
    "retell": "retold",
    "rethink": "rethought",
}

# Verbs that are already past tense or should not be converted
ALREADY_PAST = {
    "was", "were", "had", "did", "went", "made", "said", "took",
    "came", "gave", "found", "thought", "told", "became", "left",
    "felt", "put", "brought", "began", "showed", "heard", "played",
    "ran", "moved", "lived", "believed", "happened", "wrote", "sat",
    "stood", "lost", "paid", "met", "included", "continued", "set",
    "learned", "changed", "led", "understood", "watched", "followed",
    "stopped", "created", "spoke", "read", "spent", "grew", "opened",
    "walked", "won", "taught", "offered", "remembered", "considered",
    "appeared", "bought", "served", "died", "sent", "built", "stayed",
    "fell", "cut", "reached", "killed", "remained", "suggested",
    "raised", "passed", "sold", "required", "reported", "decided",
    "pulled", "developed", "established", "managed", "coordinated",
    "implemented", "delivered", "achieved", "completed", "launched",
    "designed", "automated", "streamlined", "optimized", "facilitated",
}

# Consonants for doubling rules
CONSONANTS = set("bcdfghjklmnpqrstvwxyz")
VOWELS = set("aeiou")

# Verbs ending in 'e' that just need 'd'
# (Most verbs ending in 'e' follow this rule, but we check explicitly)

# Verbs where final consonant should be doubled before adding -ed
DOUBLE_CONSONANT_VERBS = {
    "admit", "ban", "bar", "bat", "bed", "beg", "bet", "bid",
    "blog", "blot", "blur", "bob", "brag", "brim", "bud", "bug",
    "cap", "chat", "chip", "chop", "clap", "clip", "clog", "clot",
    "club", "commit", "compel", "confer", "control", "cop", "cram",
    "crop", "cup", "dam", "defer", "dim", "dip", "dot", "drag",
    "drip", "drop", "drum", "dub", "emit", "equip", "expel", "fan",
    "fit", "flag", "flap", "flip", "flog", "flop", "fog", "format",
    "fret", "gag", "gap", "grab", "grin", "grip", "gun", "gut",
    "hem", "hop", "hug", "hum", "impel", "incur", "jam", "jar",
    "jet", "jog", "jot", "kid", "knit", "knob", "lag", "lap",
    "log", "lop", "man", "map", "mat", "mob", "mop", "mud", "mug",
    "nab", "nag", "net", "nod", "occur", "omit", "opt", "pad",
    "pan", "pat", "peg", "pen", "permit", "pet", "pin", "pit",
    "plan", "plod", "plot", "plug", "plop", "pop", "pot", "prefer",
    "prep", "prod", "program", "prop", "pub", "pun", "quiz", "ram",
    "rap", "recap", "recur", "refer", "regret", "remit", "repel",
    "rig", "rim", "rip", "rob", "rot", "rub", "rug", "run", "sag",
    "scan", "scar", "scram", "scrap", "scrub", "ship", "shop",
    "shred", "shrug", "shut", "sin", "sip", "sit", "skid", "skim",
    "skip", "slam", "slap", "slim", "slip", "slit", "slog", "slop",
    "slot", "slug", "slum", "snap", "snip", "snob", "snub", "sob",
    "span", "spar", "spin", "spit", "spot", "spur", "stab", "staff",
    "stag", "star", "stem", "step", "stir", "stop", "strap", "strip",
    "strut", "strum", "stud", "stun", "sub", "submit", "sum", "sun",
    "sup", "swap", "swim", "tab", "tag", "tan", "tap", "tar", "thin",
    "throb", "tip", "top", "tot", "transfer", "transmit", "trap",
    "trek", "trim", "trip", "trot", "tug", "unwrap", "up", "upset",
    "vet", "wag", "web", "wed", "wet", "whip", "win", "wit", "wrap",
    "zap", "zip",
}


def _is_past_tense(word: str) -> bool:
    """Check if a word appears to already be in past tense."""
    lower = word.lower()
    if lower in ALREADY_PAST:
        return True
    # Common past tense endings (heuristic)
    if lower.endswith("ed") and len(lower) > 3:
        return True
    return False


def _convert_verb_to_past(verb: str) -> str:
    """Convert a single verb to its past tense form.

    Handles:
    1. Irregular verbs (comprehensive dictionary lookup)
    2. Verbs ending in 'e' (just add 'd')
    3. Verbs ending in consonant + 'y' (change 'y' to 'ied')
    4. Verbs requiring consonant doubling (CVC pattern)
    5. General rule (add 'ed')
    """
    lower = verb.lower()

    # Already past tense?
    if _is_past_tense(lower):
        return verb

    # Check irregular verbs
    if lower in IRREGULAR_VERBS:
        past = IRREGULAR_VERBS[lower]
        # Preserve original capitalization
        if verb[0].isupper():
            return past[0].upper() + past[1:]
        return past

    # Check for prefix + irregular verb (e.g., "re-build", "co-lead")
    for prefix in ("re", "pre", "co", "de", "un", "out", "over", "under", "mis"):
        if lower.startswith(prefix) and lower[len(prefix):] in IRREGULAR_VERBS:
            base_past = IRREGULAR_VERBS[lower[len(prefix):]]
            result = prefix + base_past
            if verb[0].isupper():
                return result[0].upper() + result[1:]
            return result

    # Rule 1: Verbs ending in 'e' — just add 'd'
    if lower.endswith("e"):
        result = lower + "d"
        if verb[0].isupper():
            return result[0].upper() + result[1:]
        return result

    # Rule 2: Verbs ending in consonant + 'y' — change 'y' to 'ied'
    if lower.endswith("y") and len(lower) > 2 and lower[-2] in CONSONANTS:
        result = lower[:-1] + "ied"
        if verb[0].isupper():
            return result[0].upper() + result[1:]
        return result

    # Rule 3: Verbs ending in vowel + 'y' — just add 'ed'
    if lower.endswith("y") and len(lower) > 2 and lower[-2] in VOWELS:
        result = lower + "ed"
        if verb[0].isupper():
            return result[0].upper() + result[1:]
        return result

    # Rule 4: Double consonant verbs (CVC pattern)
    if lower in DOUBLE_CONSONANT_VERBS:
        result = lower + lower[-1] + "ed"
        if verb[0].isupper():
            return result[0].upper() + result[1:]
        return result

    # Rule 4b: Short verbs with CVC pattern (single syllable)
    if (len(lower) >= 3
            and lower[-1] in CONSONANTS
            and lower[-2] in VOWELS
            and lower[-3] in CONSONANTS
            and lower[-1] not in "wxy"):
        # Only double for short words (likely single syllable)
        if len(lower) <= 4:
            result = lower + lower[-1] + "ed"
            if verb[0].isupper():
                return result[0].upper() + result[1:]
            return result

    # Rule 5: Verbs ending in 'c' — add 'ked'
    if lower.endswith("c"):
        result = lower + "ked"
        if verb[0].isupper():
            return result[0].upper() + result[1:]
        return result

    # General rule: add 'ed'
    result = lower + "ed"
    if verb[0].isupper():
        return result[0].upper() + result[1:]
    return result


def convert_to_past_tense(text: str) -> str:
    """Convert the leading verb in a text string to past tense.

    Takes a sentence/phrase and converts only the first word (verb) to past tense,
    preserving the rest of the text unchanged.

    Examples:
        "Create new dashboard" → "Created new dashboard"
        "Build automated pipeline" → "Built automated pipeline"
        "Lead cross-functional team" → "Led cross-functional team"
    """
    if not text or not text.strip():
        return text

    text = text.strip()

    # Split into first word and remainder
    parts = text.split(None, 1)
    if not parts:
        return text

    first_word = parts[0]
    remainder = parts[1] if len(parts) > 1 else ""

    # Remove any leading bullet/number markers
    clean_word = first_word.lstrip("-•*·→►▸")
    prefix = first_word[: len(first_word) - len(clean_word)]

    if not clean_word:
        return text

    # Convert the verb
    past_word = _convert_verb_to_past(clean_word)

    # Reconstruct
    if remainder:
        return f"{prefix}{past_word} {remainder}"
    return f"{prefix}{past_word}"


def convert_items_to_past_tense(items: list) -> list:
    """Convert a list of action items to past tense.

    Each item's leading verb is converted to past tense.
    Empty items are preserved as-is.
    """
    return [convert_to_past_tense(item) if item.strip() else item for item in items]


def generate_star_entry(
    title: str,
    status: str,
    situation: str,
    task: str,
    actions: list,
    result: str,
    date_completed: str,
) -> dict:
    """Create a structured STAR entry dictionary.

    Args:
        title: Project or accomplishment name
        status: Current status (from STATUS_OPTIONS)
        situation: The context/problem that existed
        task: What you were responsible for
        actions: List of specific actions taken (will be converted to past tense)
        result: The measurable outcome or impact
        date_completed: Date in YYYY-MM format

    Returns:
        Dictionary with all STAR fields plus metadata
    """
    # Convert actions to past tense
    past_actions = convert_items_to_past_tense(actions)

    return {
        "id": str(uuid.uuid4()),
        "title": title.strip(),
        "status": status,
        "date_completed": date_completed,
        "situation": situation.strip(),
        "task": task.strip(),
        "actions": past_actions,
        "result": result.strip(),
        "created_at": datetime.now().isoformat(timespec="seconds"),
    }


def format_entry_as_markdown(entry: dict) -> str:
    """Format a single entry as markdown text.

    Returns a formatted markdown block with STAR structure.
    """
    lines = []
    lines.append(f"## {entry['title']}")
    lines.append(f"**Status:** {entry.get('status', 'N/A')}  ")
    lines.append(f"**Date:** {entry.get('date_completed', 'N/A')}")
    lines.append("")
    lines.append(f"**Situation:** {entry.get('situation', '')}")
    lines.append("")
    lines.append(f"**Task:** {entry.get('task', '')}")
    lines.append("")
    lines.append("**Actions:**")
    for action in entry.get("actions", []):
        lines.append(f"- {action}")
    lines.append("")
    lines.append(f"**Result:** {entry.get('result', '')}")
    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def format_entry_as_text(entry: dict) -> str:
    """Format a single entry as plain text.

    Returns a clean plain-text representation of the STAR entry.
    """
    lines = []
    lines.append(entry["title"].upper())
    lines.append(f"Status: {entry.get('status', 'N/A')}")
    lines.append(f"Date: {entry.get('date_completed', 'N/A')}")
    lines.append("")
    lines.append(f"Situation: {entry.get('situation', '')}")
    lines.append("")
    lines.append(f"Task: {entry.get('task', '')}")
    lines.append("")
    lines.append("Actions:")
    for action in entry.get("actions", []):
        lines.append(f"  • {action}")
    lines.append("")
    lines.append(f"Result: {entry.get('result', '')}")
    lines.append("")
    lines.append("=" * 60)
    lines.append("")
    return "\n".join(lines)
