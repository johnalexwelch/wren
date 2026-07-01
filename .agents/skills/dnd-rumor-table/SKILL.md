---
name: dnd-rumor-table
model: sonnet
description: Generates a calibrated set of in-world rumors, overheard conversations, and street-level intelligence for a session — tiered by access, tagged to active fronts, and distinguished by truth value (true / partial / misleading / planted). Follows Three Clue Rule compliance: each rumor is a potential path toward a revelation. Use when session prep needs ambient intelligence for the party to discover through carousing, contacts, or investigation. Triggers on "rumor table", "what's on the street", "what are people saying", "carousing results", "what does {NPC} know", "in-world intelligence for this session", "ambient info".
metadata:
  codex-compatible: false
---

# dnd-rumor-table

Rumors are the ambient intelligence layer of a living world. They give players something to find when they go looking — and something to find even when they aren't. This skill generates rumors that are calibrated to the campaign state, tied to active revelations, and honest about their truth value.

Not random tables. Calibrated intelligence.

## Contract

Consumes: current session state (active fronts, open threads, active NPCs, player knowledge), optionally a specific context (carousing, interrogating an informant, overhearing at a market)
Produces: tiered rumor set — common (freely available), informed (requires a contact or effort), rare (requires investigation or a specific NPC)
Requires: at minimum a sense of where the party is and what fronts are active
Side effects: none unless the user asks to write to session prep or vault
Human gates: user reviews before deploying at the table

## Soft Context

Typical workflows: dnd-session-prep step 4 (secrets/clues/leads) → dnd-rumor-table (ambient layer for those revelations) → embed in prep doc
Pairs well with: dnd-session-prep (embed the rumor set in the session's intel layer), dnd-node-builder (rumors as additional nodes in the clue web), dnd-continuity-check (verify rumors don't contradict established player knowledge)

---

## Workflow

### 1. Read the campaign state

Pull what's active:
1. OPEN_THREADS.md — what revelations are in play?
2. Active front docs — what are factions doing right now?
3. Recent session note — what did the party just learn? (Don't repeat known facts as rumors.)
4. PLAYER_KNOWLEDGE.md if it exists — gate against what the party already knows

Identify the **revelation map** for this session: what truths exist in the world that the party could be pointed toward? Rumors are additional paths to those truths.

---

### 2. Identify the information landscape

Before generating, answer:

- **Where is the party?** (The Mile-End inn / a marketplace / a noble salon — different venues have different information networks)
- **What's the ambient social register?** (Working class, criminal, military, noble, merchant — each hears different things)
- **What factions are actively shaping the narrative?** (They plant disinformation; they suppress true information; they leak useful things)
- **What does the party need more paths toward?** (Check active revelations for thin clue coverage — rumors fill gaps)

---

### 3. Generate tiered rumors

Produce 8–12 rumors across three tiers:

#### Tier 1 — Common (4–5 rumors)
Freely available. Anyone might know this. Players get it from: overhearing conversation, asking a local, carousing casually.

These are the ambient texture of the city/location. Some are true, some are garbled, some are faction-planted.

#### Tier 2 — Informed (2–4 rumors)
Requires a contact, a successful social roll, or deliberately seeking out someone in the know. A merchant's guild contact, an innkeeper with a loose tongue, a guard who's had a drink.

These tend to be more specific and more useful — closer to real revelations.

#### Tier 3 — Rare (2–3 rumors)
Requires real effort: a specific NPC who trusts the party, an investigative action, a successful Insight check on the right person, a bribe. This is intelligence the party earns.

These should be directly useful for an active revelation — the clue that unlocks a thread, the lead that names a person.

---

### 4. Format each rumor

For every rumor:

```md
**{Slug}** [Tier {1/2/3}] [Truth: {True / Partial / Misleading / Planted}]

*"{The rumor as a player would hear it — in a voice, not a GM note}"*

- **Source:** {who typically says this — a dock worker, a festival pilgrim, a Vigil adjutant off-duty}
- **Agenda:** {why this source is saying it — gossip, faction plant, genuine concern, drunk}
- **Truth value:** {what's accurate, what's distorted, what's fabricated}
- **Points toward:** {which revelation, front, or open thread this feeds}
- **Deploy when:** {natural moment to surface this — carousing, asking about X, talking to Y}
```

---

### 5. Truth value taxonomy

| Value | Meaning |
|-------|---------|
| **True** | Accurate. The party can act on this. |
| **Partial** | The kernel is real; the details are garbled, incomplete, or misattributed. |
| **Misleading** | Based on a real event, but points toward the wrong conclusion. Often honest confusion. |
| **Planted** | Deliberately false; circulated by a faction to misdirect. Has an agenda behind it. |

Every set should include at least one Planted rumor — factions shape the information environment. Label it honestly in the GM notes, not in the player-facing text.

---

### 6. Three Clue Rule compliance check

After generating, cross-reference against active revelations:

For each revelation the session needs to be reachable:
- How many rumor-paths now point toward it?
- Is there at least one Tier 1 path (freely available) and one Tier 3 path (earned)?
- Does the party already have enough without these?

Flag any revelation still underserved after the rumor set is built.

---

### 7. Output

Produce a GM-ready table organized by tier, with quick-reference columns for table deployment.

```md
# Rumor Table — {Session / Location / Context}

## Quick Reference

| Slug | Tier | Truth | Points toward |
|------|------|-------|--------------|

---

## Tier 1 — Common

### {Slug}
> "{rumor text}"
- Source: … · Agenda: … · Truth: … · Points toward: … · Deploy when: …

---

## Tier 2 — Informed

…

---

## Tier 3 — Rare

…

---

## Three Clue Rule check

| Revelation | Paths now available | Coverage |
|------------|---------------------|----------|
```

---

## Rules

- **Never repeat known facts as rumors.** Check PLAYER_KNOWLEDGE.md. A rumor that confirms what the party already knows is wasted space.
- **Planted rumors need a source.** A faction that plants disinformation always has an agent doing the planting. Name the vector.
- **Rumors speak in a voice.** A dock worker doesn't say "the Crimson Storm has increased patrols in the Liminal Borgo by 40%." They say "I've seen twice as many Storm cloaks near the Mile-End since the Festival started. Something's got them spooked."
- **Tier determines access, not importance.** A Tier 3 rumor can be mission-critical; a Tier 1 rumor can be flavor. The tier tells the GM how hard the party has to work to find it.
- **Three Clue Rule is a floor.** Every active revelation should have at least one additional rumor-path, even if other paths exist. Redundancy is the point.
- **Don't generate rumors for secrets the party shouldn't touch yet.** If a revelation isn't meant to be reachable this session, don't accidentally create a path to it.
