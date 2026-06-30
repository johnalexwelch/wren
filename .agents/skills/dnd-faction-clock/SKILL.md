---
name: dnd-faction-clock
model: opus
description: Advances active faction timelines after a session — determines what each faction did while the party wasn't watching, updates their position and resources, surfaces new pressure points and faction-on-faction moves. Use after dnd-session-recap-loop or whenever factions need to be advanced between sessions. Triggers on "advance the factions", "what are the factions doing", "faction clocks", "move the factions forward", "what happened offscreen".
metadata:
  codex-compatible: false
---

# dnd-faction-clock

The world doesn't wait for the party. Every active faction has goals, resources, and timelines that advance whether or not the players engage. This skill advances each faction one beat forward based on what happened in the last session — so the living world feels like it's been moving while the party wasn't watching.

Run this after `dnd-session-recap-loop`, or independently when factions need to catch up with events.

## Contract

Consumes: session summary (what happened), active faction/org docs, front docs, OPEN_THREADS.md  
Produces: faction advancement table, off-screen moves, new pressure points, updated thread entries  
Requires: at minimum a session summary; richer output when faction docs are available  
Side effects: may update faction docs and OPEN_THREADS.md after explicit acceptance  
Human gates: user approves off-screen moves and doc updates before writing

---

## Workflow

### 1. Identify active factions

Pull every faction with a stake in the current arc. For CotU vault:
- **Shared factions**: `05 Shared Factions & Organizations/`
- **Campaign-specific orgs**: `01 Campaigns/{Campaign}/Organizations/`
- **Fronts driving faction behavior**: `Storylines & Fronts/` (CotAS) or faction threads in `OPEN_THREADS.md` (Echos)

A faction is *active* if it has an ongoing goal, a named agent in play, or a clock that's running. Dormant factions (no current agenda) get one line noting they didn't move; don't deep-analyze them.

---

### 2. For each active faction, advance one beat

Answer these questions per faction, drawing from the faction doc's Goals, Timeline, and Resources sections:

**What was the faction trying to do this session?**  
State their active goal at session start.

**What did they accomplish?**  
- *On-screen*: actions the party observed directly  
- *Off-screen*: actions that happened while the party was elsewhere — infer from their established methods, resources, and goals

**What's their position now?**  
How have their resources, leverage, or relationships shifted? Did they gain, lose, or hold?

**What's their next beat if unchecked?**  
Given where they stand now, what do they do next — the concrete action they'd take before the party intervenes?

**Any faction-on-faction moves?**  
Did this faction interact with another? If two factions share a theater of operation, their timelines intersect. Surface conflicts, alliances, and intelligence-gathering that happened without the party.

---

### 3. Determine off-screen consequences

Off-screen faction moves aren't invisible — they leave traces. For each significant off-screen action, name what evidence exists in the world:

- A message the party *could* intercept
- A location that's changed
- An NPC whose behavior has shifted
- A resource that's been depleted or acquired

These are hooks. The party can discover them through investigation, contact, or accident. Not every trace needs to be planted immediately — note which ones should surface in the next session vs. later.

---

### 4. Update pressure on open threads

Cross-reference the faction movements with `OPEN_THREADS.md`:

- Any thread whose faction is now one beat closer to its worst outcome → escalate from Brewing to Active, or update the *Risk if ignored* note
- Any thread that a faction move has resolved (from the party's perspective or not) → flag for retirement or status change
- Any new faction-driven threads (a new NPC sent into play, a new deadline created) → draft a new thread entry

Don't write updates until the user approves the faction advancement in step 5.

---

### 5. Present for acceptance

Show the full faction advancement before writing anything:

```md
## Faction Clock — {Session N+1 setup}

| Faction | What they did (on-screen) | What they did (off-screen) | Position now | Next beat if unchecked |
|---------|--------------------------|---------------------------|--------------|------------------------|
| {Name}  | ...                      | ...                       | ...          | ...                    |

## Faction-on-Faction
- {Faction A} × {Faction B}: ...

## Off-Screen Traces
- {trace}: discoverable via {method} — surface {when}

## Thread Updates Queued
- {Thread}: {status change} — reason: {faction action}
- NEW: {Thread}: {summary}
```

Get user confirmation before writing to any doc.

---

### 6. Write updates

After acceptance:

1. **Faction docs** — update Goals, Timeline, or Resources sections where the advance changed something durable. Use `vault-write` conventions.
2. **OPEN_THREADS.md** — apply the queued thread updates (status changes, new entries, retirements).
3. **Session prep stub (optional)** — if the next session is being prepped now, note the faction positions as context for `dnd-session-prep` step 1.

---

## Output rules

- Off-screen moves must follow from established faction methods and resources. Don't invent behavior that contradicts the faction doc — if a faction is cautious and covert, their off-screen move is not "attack openly."
- The *next beat if unchecked* should be specific and timed, not vague. "They'll try something eventually" is not a clock beat. "Yahlla moves the remaining Eye-Key candidate to the Q11 chamber before the Festival's second night" is.
- Faction-on-faction moves are often more consequential than faction-on-party moves. A faction losing resources to a rival changes the balance of power in ways the party can exploit — surface these.
- Don't advance every faction to a crisis every session. Factions that aren't in play this session hold position. Factions the party directly engaged advance more than factions they ignored.
- If a faction's timeline has run out — their clock hit zero — that's a consequence, not an advancement. Flag it explicitly: the faction's plan has executed, and the world has changed.
