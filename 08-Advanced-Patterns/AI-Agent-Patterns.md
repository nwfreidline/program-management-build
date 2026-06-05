# AI Agent Patterns

> How to design and deploy domain-specific AI agents for automating repetitive review, triage, and communication tasks.

---

## What Is an AI Agent?

An AI agent is a configured AI assistant with:
- A **specific domain** (invoices, tickets, schedules, etc.)
- **Decision logic** (rules for approve/reject/flag)
- **Access to data** (documents, systems, APIs)
- **Output actions** (post comments, generate reports, send notifications)

Unlike a general-purpose AI chat, an agent runs on a schedule or trigger and handles routine decisions without your intervention.

---

## When to Build an Agent

Build an agent when you:
1. Make the **same type of decision** more than 10 times/week
2. The decision follows **documented rules** (not gut feeling)
3. The **cost of a wrong decision** is low (or human confirms before action)
4. You spend **>30 minutes/day** on the repetitive task

### Good Agent Candidates
- Invoice review (check rates, PO balance, timeliness)
- Ticket triage (categorize, route, request information)
- Compliance checking (validate against policy documents)
- Report generation (compile data from multiple sources)
- Status update compilation (read tracking files, summarize)

### Bad Agent Candidates
- Negotiation (requires judgment and relationship context)
- Hiring decisions (too consequential for automation)
- Creative strategy (needs human creativity)
- One-off tasks (not worth the setup cost)

---

## Agent Architecture

```
┌────────────────────────────────────────┐
│              AI AGENT                    │
├────────────────────────────────────────┤
│                                          │
│  ┌──────────┐  ┌───────────────────┐   │
│  │  Trigger │  │  Knowledge Base   │   │
│  │(schedule │  │  (policy docs,    │   │
│  │ or event)│  │   contracts,      │   │
│  └──────────┘  │   reference data) │   │
│       │        └───────────────────┘   │
│       ▼                │                │
│  ┌──────────────┐      │                │
│  │  Agent Prompt │◄─────┘                │
│  │  (persona +   │                       │
│  │   decision    │                       │
│  │   logic)      │                       │
│  └──────────────┘                       │
│       │                                  │
│       ▼                                  │
│  ┌──────────────┐  ┌────────────────┐  │
│  │ Tool Access   │  │ Output Actions │  │
│  │ (read tickets,│  │ (post comment, │  │
│  │  check data)  │  │  send email,   │  │
│  └──────────────┘  │  generate doc) │  │
│                     └────────────────┘  │
└────────────────────────────────────────┘
```

---

## Building an Agent: Step by Step

### 1. Define the Scope

Document exactly what the agent should do:
- What inputs does it receive?
- What decisions does it make?
- What rules govern those decisions?
- What actions does it take?
- What are the boundaries (what it should NOT do)?

### 2. Write the Decision Logic

Express your rules as explicit if/then statements:

```
IF invoice amount > $10,000
  AND competing quotes < 2
  THEN flag for human review, post "missing quotes" notice

IF approval comment exists
  AND commenter has required authority level
  THEN mark as approved

IF ticket age > 7 days
  AND no response from requester
  THEN post closure notice
```

### 3. Assemble the Knowledge Base

Gather all reference documents the agent needs:
- Policy documents (what rules to follow)
- Rate cards (what costs are acceptable)
- Contact lists (who to route to)
- Templates (what to say in communications)
- Historical examples (calibration data)

### 4. Write the Agent Prompt

Structure:
```markdown
# Agent Persona
You are a [role] that [does what].

# Decision Rules
[Explicit if/then logic from step 2]

# Knowledge Base
[Reference to loaded documents]

# Output Format
[Exactly how to format the output]

# Constraints
- NEVER [things to avoid]
- ALWAYS [non-negotiable behaviors]
```

### 5. Set Up Tool Access

What systems does the agent need to read/write?
- File system (local documents)
- Ticket system (read tickets, post comments)
- Email (send notifications)
- Database (query records)
- Calendar (check availability)

### 6. Configure the Trigger

How does the agent run?
- **Scheduled** — Every N minutes/hours during business hours
- **Event-driven** — When a file changes, a ticket is created, etc.
- **Manual** — You say "review this" and it runs

### 7. Add Human Oversight

**Critical:** Always include a confirmation step for actions that affect others:
- Comments posted to tickets → require your approval before posting
- Emails sent → show draft and wait for confirmation
- Status changes → report recommendations, don't auto-apply

---

## Example Agent Designs

### Ticket Review Agent
```
Trigger: Every hour, 8am-5pm weekdays
Input: All tickets assigned to me
Logic:
  - New tickets (<24h): post acknowledgment template
  - Aging tickets (>5 days): post follow-up reminder
  - Stale tickets (>7 days): post closure notice
  - Missing information: post info-request template
Output: Activity feed notification with recommendations
```

### Invoice Review Agent
```
Trigger: On demand (user says "review invoice [link]")
Input: Invoice document (PDF or system link)
Logic:
  - Check rates against contract
  - Verify PO has sufficient balance
  - Check timeliness (within 120 days of service)
  - Check supporting documentation
Output: Approve/Reject recommendation + ready-to-post comment
```

### Status Report Generator
```
Trigger: Every Friday at 3pm
Input: Projects.md + Tasks.md from Obsidian vault
Logic:
  - Read all "In Progress" projects
  - Identify items checked off this week
  - Identify blockers (items unchanged >7 days)
  - Calculate completion percentages
Output: Formatted weekly status report (Markdown + email draft)
```

---

## Platform Options for Agents

| Platform | Scheduling | Tool Access | Cost |
|----------|-----------|-------------|------|
| **Kiro Hooks** | File-event or manual trigger | Full tool access | Free |
| **Claude Desktop** | Manual trigger only | MCP servers | Pro subscription |
| **n8n** | Cron, webhook, event | 400+ integrations | Free (self-host) |
| **Make.com** | Schedule, trigger | 1000+ integrations | Free tier available |
| **Custom Python** | `schedule` library | Whatever you code | Free |

---

## Tips

- **Start simple.** Your first agent should do ONE thing well. Add complexity later.
- **Log everything.** Record what the agent decided and why, for debugging and calibration.
- **Expect drift.** Rules change. Review your agent's logic quarterly.
- **Keep humans in the loop.** Approval gates catch errors and build trust.
- **Measure impact.** Track time saved per week. If it's <30 min, the agent isn't worth maintaining.
