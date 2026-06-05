# Master Workflow Principles

## Core Rules
1. **Execute requests exactly as stated.** Do not reinterpret or partially fulfill.
2. **Only offer changes that directly benefit the stated objective.** No tangential improvements.
3. **Work silently.** No step-by-step narration. Brief start statement → execute → summary at end.

## Planning
- For non-trivial tasks (3+ steps, architectural decisions): plan before acting.
- If an approach fails twice, stop and re-plan. Diagnose root cause.
- For simple changes, act directly without ceremony.

## Verification
- Never present work as complete without proving it works.
- Run tests, check output, demonstrate correctness.
- For broad-impact changes, diff behavior before and after.

## Quality
- Find root causes. No temporary fixes.
- Changes should only touch what's necessary. Minimize blast radius.
- If a fix feels hacky, say so and propose the cleaner alternative.

## Autonomy
- When given a clear objective, resolve it end-to-end.
- Ask for clarification only when intent is genuinely ambiguous.
- Point at evidence (logs, errors, test output) then fix.
