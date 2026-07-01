---
name: dnd-review
model: opus
description: Audits D&D plans and campaign state before the table. Three modes — continuity (contradictions across canon/timeline/NPC/faction/player-knowledge), open-threads (which loose ends to pay off, escalate, preserve, retire), and player-agency (railroading, false choices, brittle clue paths). Use before finalizing sessions/arcs/mysteries, when introducing new lore, between arcs, or to check for railroading.
codex-compatible: false
---

# dnd-review

Catch problems before they reach the table. This skill handles shared setup (scoping + doc retrieval) then dispatches to the appropriate component skill(s). Run one mode for a focused check; run all three for a full pre-session audit.

- **continuity** — "does this contradict", "check continuity", "audit this lore/plan"
- **threads** — "open threads", "loose ends", "what did we forget", "dangling hooks"
- **agency** — "is this railroady", "are these real choices", final gate before the table

## Shared steps (all modes)

1. **Scope** what's under review: session, arc, lore doc, NPC, faction, mystery, handout, or encounter.
2. **Retrieve source of truth** in order: Campaign Dashboard (`{Campaign Name} - Campaign Dashboard.md`), `Decision Log.md` (LOCKED entries — see Decision Log filter in dnd-session-prep Step 1 Tier 2 for how to extract them), `PLAYER_KNOWLEDGE.md`, `OPEN_THREADS.md`, `TIMELINE.md`, relevant NPC/faction/location docs, recent session notes. Load only what exists. Do not look for `CANON.md` — it was rejected (Q4 decision-log); Decision Log is the source of truth for settled decisions.
3. Dispatch to the mode(s) below. Only update docs after explicit acceptance.

---

## Mode: continuity

Load and run `dnd-continuity-check/SKILL.md`.

Pass: the scoped artifact and the docs retrieved in the shared step as the source of truth input. Skip the doc retrieval step inside `dnd-continuity-check` — it was already done here.

---

## Mode: threads

Load and run `dnd-open-thread-review/SKILL.md`.

Pass: `OPEN_THREADS.md` and session notes from the shared retrieval step.

---

## Mode: agency

Load and run `dnd-player-agency-review/SKILL.md`.

Pass: the scoped plan or session from step 1.

---

## Multi-mode runs

When running more than one mode, dispatch in order: continuity → threads → agency. Each uses the docs already loaded in the shared step — do not re-fetch.

After all modes complete, synthesize:

```md
# dnd-review Summary

## Continuity
{findings from dnd-continuity-check — severity counts + top issues}

## Open Threads
{findings from dnd-open-thread-review — status counts + priority actions}

## Player Agency
{findings from dnd-player-agency-review — main risks + brittle paths}

## Combined verdict
Safe to run: {Yes / Yes with changes / No}
Blockers before table: {list or none}
```

## Contract

Consumes: scoped artifact (session plan, arc, lore doc, encounter, etc.), campaign docs when available
Produces: findings from each dispatched mode, combined verdict
Requires: at least one campaign doc or user-provided excerpt; a draft plan for agency review
Side effects: may update `OPEN_THREADS.md` or canon docs only after explicit acceptance
Human gates: user chooses which fixes to apply from each mode
