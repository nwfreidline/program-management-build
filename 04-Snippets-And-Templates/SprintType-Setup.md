# SprintType Setup Guide

> SprintType is a free, privacy-first browser extension for text expansion. Type a shortcut like `//approval` in any text field and it instantly expands to the full template. All data stays local on your device.

---

## Install

SprintType is available for all major browsers:

| Browser | Install Link |
|---------|-------------|
| **Firefox** | [addons.mozilla.org/firefox/addon/sprinttype](https://addons.mozilla.org/en-US/firefox/addon/sprinttype/) |
| **Chrome** | Search "SprintType" in the Chrome Web Store |
| **Edge** | Chrome Web Store extensions work in Edge |

After installing, the SprintType icon appears in your browser toolbar.

---

## How It Works

1. You define a **shortcut** (e.g., `//approval`) and an **expansion** (the full text)
2. When you type the shortcut in any text field on any website, it auto-expands
3. All snippets are stored locally in your browser — no cloud, no account needed

### Trigger Prefix

All shortcuts use `//` as the prefix. This prevents accidental triggers during normal typing.

**Examples:**
- `//approval` → full approval request template
- `//DMG` → vendor SPRINT code "DIVMAI"
- `//dmg` → vendor account number "23267836"

---

## Initial Setup

### Option 1: Import the Snippet Library (Recommended)

1. Click the SprintType icon in your toolbar
2. Go to Settings/Import (or the gear icon)
3. Import the `snippets.json` file from this folder
4. All snippets load immediately

### Option 2: Manual Entry

1. Click the SprintType icon → "Add Snippet"
2. Enter the shortcut (e.g., `//weekly`)
3. Enter the expansion text
4. Save — it's live immediately

---

## Snippet Library Included

This package includes two snippet files:

| File | Format | Contents |
|------|--------|----------|
| `sprinttype-snippets.json` | SprintType native JSON | Ready-to-import snippet library for program management |
| `snippets-reference.yml` | Espanso YAML | Same content in Espanso format (alternative tool) |

### Snippet Categories

#### Status & Reporting
| Shortcut | Expands To |
|----------|-----------|
| `//status-green` | On Track status with details placeholder |
| `//status-yellow` | At Risk status with mitigation placeholder |
| `//status-red` | Behind Schedule with recovery plan |
| `//weekly` | Full weekly status report template |
| `//monthly` | Comprehensive monthly report template |

#### Approval & Procurement
| Shortcut | Expands To |
|----------|-----------|
| `//approval` | Approval request with threshold guidance ($500=FM, $10K=AM) |
| `//preferred` | Preferred vendor competing quote requirement notice |
| `//nonpreferred` | Non-preferred vendor quote + justification notice |
| `//PR` | PR submitted notification with PO instructions |
| `//quote` | Generic competing quote request |

#### Meeting Management
| Shortcut | Expands To |
|----------|-----------|
| `//agenda` | Meeting agenda template |
| `//minutes` | Meeting minutes with action items table |
| `//action` | Single action item (what / owner / due) |
| `//decision` | Decision record (what / rationale / who / date) |
| `//followup` | Follow-up email template |

#### Project Communication
| Shortcut | Expands To |
|----------|-----------|
| `//kickoff` | Project kickoff email |
| `//escalate` | Escalation email with issue/impact/ask |
| `//milestone` | Milestone completion announcement |
| `//closure` | Project closure notification |
| `//blocker` | Blocker notification to stakeholders |

#### Vendor Quick Reference
| Shortcut (UPPERCASE) | Expands To | Shortcut (lowercase) | Expands To |
|---------------------|-----------|---------------------|-----------|
| `//Vendor` | SPRINT code (e.g., "DIVMAI") | `//vendor` | Account number (e.g., "23267836") |

*UPPERCASE shortcuts expand to SPRINT vendor codes. Lowercase shortcuts expand to vendor account numbers.*

#### Common Responses
| Shortcut | Expands To |
|----------|-----------|
| `//ack` | "Received, thank you. I'll review and follow up by [date]." |
| `//defer` | Backlog acknowledgment with timeline |
| `//needinfo` | Missing information request with deadline |
| `//delegate` | Routing message to correct owner |

---

## Creating Your Own Snippets

### Best Practices

1. **Always use `//` prefix** — prevents accidental triggers
2. **Keep shortcuts memorable** — use the thing's name or abbreviation
3. **Case sensitivity matters** — `//DMG` and `//dmg` can expand to different things
4. **Multi-line works** — expansions support newlines for full templates
5. **Review quarterly** — remove snippets you never use, add new patterns you notice

### JSON Format

SprintType uses a simple JSON array:

```json
[
  {
    "shortcut": "//mysnippet",
    "expansion": "This is what it expands to.\nThis is line two."
  },
  {
    "shortcut": "//another",
    "expansion": "Another expansion here."
  }
]
```

**Note:** Use `\n` for newlines in JSON. Use `&nbsp;` if you need a visible blank line in HTML-based text fields.

---

## Export & Backup

1. Click SprintType icon → Settings/Export
2. Save the JSON file to a safe location
3. This is your backup — import it on any other browser/machine

**Tip:** Keep your export in this project folder under version control. When you add new snippets, re-export and commit.

---

## Sharing Snippets with Your Team

1. Export your snippets to JSON
2. Remove any personal/sensitive shortcuts (account numbers, internal codes)
3. Share the JSON file — team members import it in one click
4. Each person can then add their own on top of the shared set

---

## Tips

- **Build snippets reactively** — When you catch yourself typing the same thing a third time, make it a snippet
- **Use for emails you send weekly** — Status updates, standup notes, recurring requests
- **HTML awareness** — In rich text editors (Outlook, Gmail), `&nbsp;` creates blank lines; `\n` may not render the same as in plain text fields
- **Vendor codes are case-paired** — UPPERCASE = SPRINT code, lowercase = account number. This is a powerful pattern for quick lookups.
