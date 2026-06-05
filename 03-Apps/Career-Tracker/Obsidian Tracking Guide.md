# Obsidian Tracking Guide — Optional Companion Workflow

This guide describes an optional project tracking system using [Obsidian](https://obsidian.md) that pairs well with Career Tracker. It's what I use to log work in real time, then periodically convert completed projects into polished STAR entries.

You don't need this to use Career Tracker — but if you want a lightweight daily tracking habit that makes writing accomplishments easier at review time, this is a proven setup.

---

## Why Obsidian + Career Tracker?

| Problem | How This Solves It |
|---------|-------------------|
| You forget what you worked on 3 months ago | Obsidian captures it as you go |
| Writing STAR entries from scratch is painful | Your task log becomes the raw material |
| You can't remember the "Result" | The log shows what shipped and when |
| You have 20 things in flight and lose track | One note shows all active work at a glance |

**The flow:** Track daily work in Obsidian → Review completed projects monthly → Write them up as STAR entries in Career Tracker → Export for reviews.

---

## What is Obsidian?

[Obsidian](https://obsidian.md) is a free, offline markdown editor. It stores everything as plain `.md` files in a folder on your machine — no cloud account required, no subscription, no sync unless you choose to set it up.

### Install

1. Go to https://obsidian.md/download
2. Download and install for Windows
3. Open Obsidian → **Create new vault**
4. Choose a folder on your local machine (not OneDrive)
5. Name it whatever you want (e.g., "Work Tracking", "PM Notes")

> ⚠️ **Store your vault locally**, not in OneDrive. Obsidian creates small metadata files that sync poorly. If you want backup, use Git or manual copies.

---

## Recommended Vault Structure

You only need one folder and one or two files to get started:

```
Your Vault/
├── Tracking/
│   ├── Projects.md          # All active project work
│   └── To Growth Tracker.md # Completed projects ready for STAR writeup
└── (anything else you want — meeting notes, references, etc.)
```

That's it. Obsidian is flexible — add more structure later if you want. The tracking system works with just these two files.

---

## How Projects.md Works

This is your single source of truth for what you're working on. Each project is a checklist entry with tasks nested underneath.

### Format

```markdown
### In Progress

- [ ] Project Name
	- [ ] Task or phase description
	- [ ] Another task
	- [x] Completed task (check it off as you finish)

- [ ] Another Project
	- [x] Phase 1: Did the thing
	- [ ] Phase 2: Next thing to do
```

### Rules

- **One entry per project** — not per task. The project is the parent, tasks are children.
- **Check things off as you go** — `[x]` for done, `[ ]` for pending.
- **Keep it current** — spend 2 minutes at the end of each day updating what you did.
- **Use phases for large projects** — group related tasks under bold phase headers.

### Example

```markdown
### In Progress

- [ ] Vendor Onboarding Automation
	- [x] Map current manual process (12 steps, 3 handoffs)
	- [x] Build intake form (vendor name, contract type, site list)
	- [x] Create automated email templates for each stage
	- [ ] Test with 2 vendors from next onboarding batch
	- [ ] Get team feedback and iterate

- [ ] Q3 Budget Reconciliation
	- [x] Pull actuals from finance portal
	- [x] Cross-reference against approved OP plan
	- [ ] Flag variances > 10% for manager review
	- [ ] Prepare summary slide for monthly business review
```

---

## When a Project is Done

Once all tasks are checked off:

1. Move the entry from `Projects.md` to `To Growth Tracker.md`
2. That file is your "ready to write up" queue
3. When it's time for a review cycle, open Career Tracker and convert each completed project into a STAR entry

### To Growth Tracker.md — Example

```markdown
- [x] Vendor Onboarding Automation
	- [x] Map current manual process (12 steps, 3 handoffs)
	- [x] Build intake form (vendor name, contract type, site list)
	- [x] Create automated email templates for each stage
	- [x] Test with 2 vendors from next onboarding batch
	- [x] Get team feedback and iterate
```

When you sit down to write a STAR entry, this gives you everything:
- **Situation** → why the project existed (you'll remember from the first task)
- **Task** → what you owned
- **Actions** → the checked-off items are your actions list, already in past tense
- **Result** → the final task usually captures the outcome

---

## The Monthly Review Habit

Set a recurring reminder (first Monday of the month works well):

1. Open `To Growth Tracker.md` — are there completed projects?
2. Open Career Tracker
3. For each completed project, click **+ New Entry** and fill in the STAR fields
4. Your task log from Obsidian is the raw material — paraphrase and quantify
5. Once written up, you can archive the entry from `To Growth Tracker.md`

This takes 15–30 minutes per month and means you never scramble before a review.

---

## Tips

- **Don't overthink task granularity.** Capture the main steps, not every click. If you can't tell the story of what you built from the task list, add more detail.
- **Date your completions if you want.** Some people add `(Jun 2026)` next to completed phases. Optional but helpful for timelines.
- **Use sections to organize.** `### Backlog`, `### In Progress`, `### Pending` (waiting on someone else) is a simple way to separate work states.
- **You don't need plugins.** Obsidian has a huge plugin ecosystem, but this workflow works with zero plugins installed. Plain markdown checkboxes.
- **Kanban view (optional).** If you install the Kanban plugin in Obsidian, you can create a board view of your projects. Nice but not required.

---

## Quick Reference — From Obsidian to STAR Entry

| Obsidian Task Log | STAR Field | How to Translate |
|-------------------|-----------|-----------------|
| Why the project started | **Situation** | What gap or problem existed before you acted? |
| Your role / ownership | **Task** | What were you specifically responsible for? |
| Checked-off tasks | **Actions** | Summarize the key steps (Career Tracker auto-converts to past tense) |
| Final deliverable / outcome | **Result** | Quantify if possible: time saved, people impacted, $ value |

---

## Summary

| Step | Tool | Time |
|------|------|------|
| Track work daily | Obsidian (`Projects.md`) | 2 min/day |
| Move completed projects | Obsidian (`To Growth Tracker.md`) | When done |
| Write STAR entries | Career Tracker | 15–30 min/month |
| Export for reviews | Career Tracker → Word/Excel | 5 min when needed |

This system means your accomplishments are always documented, always current, and always ready to export — whether it's for a promo doc, a 1:1, or a resume update.

---

## Questions?

Reach out to Nick — happy to walk through the setup or share my vault structure as a reference.
