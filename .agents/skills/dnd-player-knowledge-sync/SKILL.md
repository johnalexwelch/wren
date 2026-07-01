---
name: dnd-player-knowledge-sync
model: sonnet
description: Post-session extractor. Reads the completed session note and updates PLAYER_KNOWLEDGE.md with what the players now know — NPCs met, locations visited, information learned, rumors heard, secrets revealed. Keeps the GM/player knowledge boundary sharp so session-prep never accidentally hands out a secret the party hasn't earned. Run after every session recap, or trigger from dnd-session-recap-loop Step 11.
metadata:
  codex-compatible: false
---

# dnd-player-knowledge-sync

Maintain the boundary between **GM truth** and **player knowledge**. After each session, extract what crossed that line — what the players actually saw, heard, and learned at the table — and record it in `PLAYER_KNOWLEDGE.md`. This file is the primary guard against prep accidentally re-delivering earned information or leaking unrevealed secrets.

## When to run

- After every session recap (triggered from `dnd-session-recap-loop` Step 11)
- Any time `PLAYER_KNOWLEDGE.md` is missing or clearly stale (e.g. before a prep session where it would matter)
- On demand when the GM asks "what do the players know about X?"

## Bootstrap (first-time setup)

If `PLAYER_KNOWLEDGE.md` doesn’t exist and the campaign has already been running:

- **>5 sessions played:** Do not backfill automatically. Create the file with the header structure, extract from the **most recent 2–3 session notes only**, and add this note at the top: `[BOOTSTRAPPED at S{n} — knowledge before this session not captured. Add early-campaign facts manually if prep surfaces them.]` Then add an OPEN_THREADS entry: “Bootstrap PLAYER_KNOWLEDGE — if prep surfaces a known fact from early campaign not in file, add it.”
- **≤5 sessions played:** Extract all sessions.

**Rationale:** Players already know what they know. This file guards *future* prep, not past. 83 sessions of backfill is error-prone and unnecessary. The bootstrapped marker signals to session-prep that early-campaign knowledge may be missing — fall back to inferring from session notes for pre-bootstrap sessions.

## Maintenance (every 10 sessions)

When session count is a multiple of 10:

1. **Archive old entries** — move sessions older than 20 back to `PLAYER_KNOWLEDGE_ARCHIVE.md`. Exception: secrets revealed are never archived (always live).
2. **Mark superseded facts** — if a confirmed fact contradicts an earlier entry, add `[SUPERSEDED S{n}]` to the old entry.
3. **Consolidate NPC tables** — merge repeated NPC entries into a single cumulative-knowledge row.

Session-prep Tier 2 loads the active file only; archive is reference-only.

## Inputs

1. The session note just written (from `dnd-session-recap-loop`)
2. The previous `PLAYER_KNOWLEDGE.md` (read it; append to it — never overwrite history)
3. The campaign's `Decision Log.md` (LOCKED entries) if available — cross-check that revealed info matches what was intended to be revealed

## The extraction pass

Work through the session note looking for **information that crossed the GM/player boundary this session**. Ask for each item: *did the players witness, hear, or learn this — or does it exist only in GM notes?*

Extract in five categories:

### 1. NPCs encountered (on-screen)

For each NPC the players had direct contact with:

- **Name** as the players know it (might differ from GM file name — note both)
- **What the players know**: role, affiliation, apparent motivation
- **What they don't know**: GM-truth layer that hasn't been revealed
- **Relationship state**: how the party currently stands with this NPC
- **Session ref**: which session this encounter happened

### 2. Locations visited

- Location name and what the players know about it
- Any map/layout information revealed
- Who controls it / what it's used for (player-visible version only)

### 3. Information learned (explicit reveals)

Facts the players were explicitly told, read, or witnessed. Each entry:

- The fact
- Source (who told them / what they found)
- Confidence level from the players' perspective: **confirmed** / **rumor** / **inferred**
- Session ref

### 4. Rumors and unverified leads

Information the players received but can't yet verify. Keep separate from confirmed facts — the distinction matters for prep (a rumor shouldn't be treated as confirmed in future sessions).

### 5. Secrets revealed this session

High-value information that crossed the boundary this session — things that were previously GM-only. Note them here so future prep doesn't re-deliver them.

## PLAYER_KNOWLEDGE.md format

File lives at `{Campaign folder}/PLAYER_KNOWLEDGE.md`. Use append-only updates — add a new session block below existing content. Never rewrite earlier sessions' entries; mark corrections as `[REVISED S{n}]` if something was wrong.

```md
# PLAYER KNOWLEDGE — {Campaign Name}
*What the party actually knows. GM truth layer excluded. Updated after each session.*
*Maintained by: dnd-player-knowledge-sync*

---

## Session {n} — {date or in-game date}

### NPCs Encountered
| NPC (as known) | GM file name | What they know | What they don't | Relationship | First met |
|---|---|---|---|---|---|
| … | … | … | … | neutral/warm/hostile/wary | S{n} |

### Locations Visited
| Location | What they know | Session |
|---|---|---|
| … | … | S{n} |

### Information Learned (Confirmed)
| Fact | Source | Session |
|---|---|---|
| … | … | S{n} |

### Rumors & Unverified Leads
| Rumor | Source | Verified? | Session |
|---|---|---|---|
| … | … | No | S{n} |

### Secrets Revealed This Session
- **{Secret name}**: {what they now know} (S{n})

---
```

## Output rules

- **Player POV only.** Never write GM-truth into PLAYER_KNOWLEDGE.md. If a section requires distinguishing "what they know" from "what's actually true," only write the player-visible version in this file.
- **Append, never overwrite.** Earlier entries are historical record. If something was wrong, add a `[REVISED S{n}]` note; don't delete.
- **Flag gaps.** If the session note is ambiguous about whether something was revealed (GM described a detail but it wasn't clear players noticed), flag it with `[UNCLEAR — confirm with GM]` rather than making a call.
- **Don't extract future prep.** This file is backward-looking (what they know now). Don't include GM plans, upcoming beats, or information the party hasn't received.
- **Cross-check Decision Log.** If a revealed secret contradicts a LOCKED Decision Log entry, note the discrepancy. Don't resolve it silently.

## Pairs with

- `dnd-session-recap-loop` — run this after the recap note is written (Step 11)
- `dnd-session-prep` — reads `PLAYER_KNOWLEDGE.md` in Tier 2 context loading (Step 1 and Step 4)
- `dnd-continuity-check` — uses `PLAYER_KNOWLEDGE.md` to verify clues don't leak unrevealed secrets
