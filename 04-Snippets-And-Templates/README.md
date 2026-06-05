# Layer 4: Snippets & Text Expansion

> Type a short trigger, get a full template instantly. Eliminates repetitive typing for approvals, status updates, vendor communications, and procurement workflows.

---

## What Is Text Expansion?

Text expansion tools let you type a short abbreviation (like `;appreq`) and have it instantly expand into a full paragraph, email template, or form response. For a program manager who sends dozens of similar communications daily, this saves hours per week.

---

## Recommended Tools

| Tool | Platform | Cost | Best For |
|------|----------|------|----------|
| **SprintType** ⭐ | Any browser (Chrome/Firefox/Edge) | Free | Browser-based work, zero install, privacy-first |
| **Espanso** | Windows/Mac/Linux | Free (open source) | System-wide expansion, regex, scripting |
| **AutoHotKey** | Windows only | Free | Windows-native, maximum flexibility |
| **PhraseExpress** | Windows/Mac | Free (personal) | GUI-based, easy setup |
| **TextExpander** | Windows/Mac | $3.33/mo | Team sharing, cloud sync |

**Recommended for this setup: SprintType** — free, works in any browser, no account required, all data stored locally. Uses `//` as the trigger prefix. See [SprintType-Setup.md](SprintType-Setup.md) for full setup guide.

---

## Espanso Quick Setup

### 1. Install

Download from [espanso.org](https://espanso.org/install/) and install.

### 2. Verify

Type `:espanso` anywhere — it should expand to "Hi there!" (default test snippet).

### 3. Load the Snippet Library

Copy `snippets-reference.yml` to your Espanso config directory:

```
%APPDATA%\espanso\match\program-management.yml
```

### 4. Reload

```bash
espanso restart
```

---

## Snippet Library Categories

### Approval & Procurement

| Trigger | Expands To |
|---------|-----------|
| `;appreq` | Approval request template (for expenditures requiring manager sign-off) |
| `;poreq` | Purchase order request template |
| `;quote` | Competing quote requirement notice |
| `;vendor-new` | New vendor onboarding checklist |
| `;vendor-close` | Vendor contract closure notice |

### Status Updates

| Trigger | Expands To |
|---------|-----------|
| `;status-green` | "Status: 🟢 On Track — [details]" |
| `;status-yellow` | "Status: 🟡 At Risk — [reason]. Mitigation: [action]" |
| `;status-red` | "Status: 🔴 Behind — [reason]. Recovery: [plan]" |
| `;weekly` | Weekly status report skeleton |
| `;monthly` | Monthly report skeleton |

### Meeting Management

| Trigger | Expands To |
|---------|-----------|
| `;agenda` | Meeting agenda template |
| `;minutes` | Meeting minutes template |
| `;action` | Action item format: "**Action:** [what] | **Owner:** [who] | **Due:** [when]" |
| `;decision` | Decision record format |
| `;followup` | Follow-up email template |

### Project Communication

| Trigger | Expands To |
|---------|-----------|
| `;kickoff` | Project kickoff email template |
| `;escalate` | Escalation email template |
| `;blockernotice` | Blocker notification to stakeholders |
| `;milestone` | Milestone completion announcement |
| `;closure` | Project closure notification |

### Date/Time Shortcuts

| Trigger | Expands To |
|---------|-----------|
| `;today` | Today's date (YYYY-MM-DD) |
| `;now` | Current date and time |
| `;eow` | End of current week date |
| `;eom` | End of current month date |
| `;eoq` | End of current quarter date |

---

## Creating Custom Snippets

### Espanso Format (YAML)

```yaml
matches:
  - trigger: ";appreq"
    replace: |
      Hi {{recipient}},

      Requesting approval for the following expenditure:

      - **Description:** {{description}}
      - **Amount:** ${{amount}}
      - **Vendor:** {{vendor}}
      - **Budget Line:** {{budget_line}}

      Please confirm approval by replying to this message.

      Thank you.
    vars:
      - name: recipient
        type: form
        params:
          layout: "Recipient: {{value}}"
      - name: description
        type: form
        params:
          layout: "Description: {{value}}"
      - name: amount
        type: form
        params:
          layout: "Amount: {{value}}"
      - name: vendor
        type: form
        params:
          layout: "Vendor: {{value}}"
      - name: budget_line
        type: form
        params:
          layout: "Budget Line: {{value}}"
```

### AutoHotKey Format

```ahk
::;appreq::
(
Hi [Recipient],

Requesting approval for the following expenditure:

- Description: [description]
- Amount: $[amount]
- Vendor: [vendor]
- Budget Line: [budget line]

Please confirm approval by replying to this message.

Thank you.
)
return
```

---

## Tips

- **Use a consistent prefix** — all your snippets should start with the same character (`;` or `:` are common) to avoid accidental triggers
- **Keep triggers short but memorable** — `;appreq` not `;approval-request-email-template`
- **Include variables** — Espanso can prompt you for fill-in fields
- **Review quarterly** — Remove snippets you never use, add new ones for recurring patterns
- **Share with your team** — Export your snippet file and distribute via the team rollout framework
