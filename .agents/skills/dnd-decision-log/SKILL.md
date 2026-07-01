---
name: dnd-decision-log
model: sonnet
description: Records an accepted creative decision to the campaign's Decision Log in the CotU vault. Use after any grilling session, design session, or session recap that locks a canon question, resolves a DM open decision, or requires revision of a prior decision. Triggers on "log this decision", "record this", "add to the decision log", "lock this", or when a grill or design workflow accepts a decision.
metadata:
  codex-compatible: false
---

# dnd-decision-log

Records creative decisions to the vault so future prep doesn't rely on chat memory. Decision logs are the authoritative record of why the world is the way it is.

## Vault paths

| Campaign | Decision Log |
|---|---|
| Children of the Ashen Sky | `01 Campaigns/Children of the Ashen Sky/Decision Log.md` |
| Echos of Eternity | `01 Campaigns/Echos of Eternity/Decision Log.md` |

Both files exist and are active. Read the existing log before appending — check the last entry number to continue the sequence correctly.

---

## When to log

Log a decision when:
- A grill or design session **accepts** something that was previously open (naming a faction, defining a corruption, locking a character's backstory)
- A session reveals something at the table that **locks** a canon question
- A prior decision is **revised** — log the revision below the original, don't delete history
- A DM open decision from `OPEN_THREADS.md` or `Story So Far.md` is resolved

Do **not** log:
- Things that are still TBD — those belong in OPEN_THREADS or OPEN_QUESTIONS
- Minor tactical choices (which encounter to run, how to phrase narration)
- Anything that hasn't been explicitly accepted

---

## Entry format

```md
### D-{NNN} · {Short title}

**Decision**: {What was decided — one clear sentence.}

**Alternatives considered**: {What else was on the table.}

**Accepted tradeoff**: {What this gives up or complicates, and why it's worth it.}

**Status**: LOCKED.
```

Group entries under a session or prep heading:

```md
## {Context} — {YYYY-MM-DD}
```

For revisions, append below the original entry:

```md
### D-{NNN} · {Same title} — REVISED {YYYY-MM-DD}

**Revised decision**: {What changed.}

**Reason for revision**: {What happened at the table or in prep that invalidated the original.}

**Status**: REVISED → LOCKED.
```

Never delete the original entry. History is the point.

---

## Workflow

1. **Identify the decision** — what was accepted, by whom, in what context?
2. **Read the existing log** to get the next D-number and confirm no duplicate
3. **Determine the heading** — which session/prep block does this fall under? Add a new heading if needed.
4. **Draft the entry** and show it to the user before writing
5. **Append to the vault file** after acceptance — use `vault-write` conventions
6. **Update OPEN_THREADS.md** — if this decision closes an item in Open Canon to Resolve, mark it Resolved with a pointer to the D-number

---

## Output rules

- One entry per decision. Don't bundle multiple unrelated decisions under one D-number.
- The **decision** line must be specific enough to act on in future prep — "we decided the third eye-key house is House Miren" not "we decided something about the houses."
- The **alternatives** line is required. A decision without recorded alternatives is just a fact, not a decision — the alternatives tell future-you why the other paths weren't taken.
- The **tradeoff** line is required. Every creative decision costs something. Name it.
