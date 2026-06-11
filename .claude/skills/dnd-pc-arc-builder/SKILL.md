---
name: dnd-pc-arc-builder
model: opus
description: Maps a PC's backstory hooks to active campaign fronts, schedules payoff beats across upcoming sessions, and builds a spotlight queue. Distinct from dnd-npc-arc-builder (NPC revelation structure) and character-arc (internal transformation) — this skill handles scheduling and integration of player-established backstory into living campaign material. Use when deferred spotlights have piled up, when a PC's personal arc has gone dark, or when prepping a session that should pay off a PC's backstory. Triggers on "PC spotlight", "backstory hook", "pay off {PC}'s arc", "what are {PC}'s hooks", "deferred spotlight for {PC}", "when does {PC}'s backstory come up".
metadata:
  codex-compatible: false
---

# dnd-pc-arc-builder

A PC's backstory is a promise the game made to a player. This skill maps that promise to the living campaign — which fronts can honor it, when, and how — so spotlights get scheduled rather than indefinitely deferred.

**Distinct from related skills:**
- `character-arc` — designs the internal transformation arc (want/need/false belief). Run that first; this skill consumes its output or builds toward it.
- `dnd-npc-arc-builder` — revelation structure for NPCs (GM-controlled). PC arcs give the player agency: you create the *opportunity*, not the outcome.

## Contract

Consumes: PC name + backstory, current campaign state (session notes, active fronts, NPC docs, OPEN_THREADS.md)
Produces: hook inventory, front-integration map, spotlight schedule (next 3–5 sessions), vault file updates
Requires: at minimum a PC name and some backstory detail
Side effects: may create or update PC vault files; may add spotlight entries to OPEN_THREADS.md after acceptance
Human gates: user approves integration map before scheduling; user approves vault updates before writing

## Soft Context

Typical workflows: after dnd-session-recap-loop defers a spotlight → dnd-pc-arc-builder (schedule the payoff) → dnd-session-prep (embed the opportunity)
Pairs well with: character-arc (build the internal arc first), dnd-npc-arc-builder (if a PC's backstory NPC needs a revelation arc), dnd-session-prep (embed the scheduled opportunity)

---

## Workflow

### 1. Gather backstory and current state

Read in order:
1. PC's vault file if it exists (check `01 Campaigns/{Campaign}/PCs/` or `NPCs/`)
2. Campaign Dashboard → relevant session notes for PC appearances
3. OPEN_THREADS.md — any existing PC hooks or deferred spotlights
4. Active front docs and NPC docs for potential integration points

Extract from backstory (prompt the user if thin):
- **Wounds** — past events that still shape behavior (loss, betrayal, failure, exile)
- **Relationships** — people from before the campaign (mentors, rivals, family, enemies, debts)
- **Mysteries** — things the PC doesn't know about their own past (sealed memories, unknown lineage, unexplained events)
- **Promises** — things the PC has committed to (vows, oaths, debts, unfinished business)
- **Identity questions** — who are they before the campaign answers? (Koralock's "crushing defeat of my company"; Henry's sealed Celestium memories; Galei's Vigil-uniform reaction)

---

### 2. Classify hooks by readiness

For each hook extracted:

| Status | Meaning | Action |
|--------|---------|--------|
| **Dormant** | Hook exists; no campaign hook-up yet | Map to a front or NPC |
| **Planted** | Seeded in play; players have the thread | Schedule payoff window |
| **Active** | Currently in play; party aware | Prep the encounter |
| **Deferred** | Was scheduled; got pushed | Reprioritize |
| **Paid off** | Resolved | Archive |

Note which hooks are *player-visible* (the player knows about the hook) vs. *GM-only* (a secret the player doesn't know yet that their backstory contains).

---

### 3. Map hooks to existing campaign material

For each hook, find the living campaign element that can honor it. You are looking for *organic integration*, not forced insertion:

**Front/faction integration:**
- Which active fronts could plausibly intersect with this backstory? (Galei → Vigil-uniform shock → Crimson Storm / Vigil is already in the city)
- What does the front's next beat look like if it also pays off this hook?

**NPC integration:**
- Are there existing NPCs who could know the PC's backstory? (Henry's Celestium connection → Celestium operatives in the city)
- Could an existing NPC have a different relationship to the PC than the party knows?

**Location integration:**
- Are there locations on the campaign map that carry backstory resonance? (Henry's Gravedigger's Compound connection)

**Timeline integration:**
- At what campaign beats does the world naturally create space for this hook? (Arrival of Il Tornja Day 2–3 → Vigil presence intensifies → Galei spotlight window opens)

If a hook has no organic hook-up point, note it as *unintegrated* and identify what new material would be needed (a new NPC, a faction connection, a location).

---

### 4. Score each hook

Rate each hook 1–5 on:
- **Player investment** — how much does this player care?
- **Campaign relevance** — how well does it thread into current arcs?
- **Setup completeness** — how much has already been seeded?
- **Urgency** — does deferring this further have a real cost?

---

### 5. Build the spotlight schedule

Schedule payoff windows for the top 3–5 hooks, with specificity:

```md
## Spotlight Schedule

### {PC name} — {Hook name}

**Hook:** {what the backstory promise is}
**Current status:** {dormant / planted / deferred}
**Integration point:** {which front / NPC / location}
**Window:** {session N — what's happening in that session that creates the opening}
**How to surface:** {the concrete thing the GM does — the NPC who appears, the item that triggers recognition, the sight that lands}
**Player agency:** {the choice the player faces when this surfaces — not the outcome, the decision}
**Risk of continued deferral:** {what the player loses if this keeps getting pushed}
```

A window is not "session 83 or 84 sometime." It is "S083 — when Henry walks through the Vigil checkpoint at the Diadem approach — a guard's face triggers the body-memory."

---

### 6. Identify what needs to be built

After mapping, name any gaps: a new NPC to create, a front connection to establish, a location to build out, a piece of lore to lock. Route to the appropriate skill:
- New NPC → create vault file; if revelation arc needed → `dnd-npc-arc-builder`
- New front connection → `dnd-adventure-design` or `dnd-grill`
- Lore question → `dnd-grill (canon mode)` → `dnd-decision-log`

---

### 7. Present and accept

Show the full hook inventory, integration map, and spotlight schedule before writing anything. Get user confirmation before:
- Adding entries to OPEN_THREADS.md
- Creating or updating PC vault files
- Modifying any front or NPC doc

---

### 8. Write to vault

After acceptance:

1. **PC vault file** — create at `01 Campaigns/{Campaign}/PCs/{Name}.md` if none exists; update if it does. Include: backstory summary, hook inventory with status, integration map, key relationships.
2. **OPEN_THREADS.md** — add spotlight queue entries under the relevant status section (Active / Brewing / Ready for Payoff). Format matches existing thread entries.
3. **Session prep stub** — if the next session is being prepped, note the scheduled spotlights as inputs to `dnd-session-prep` step 7 (Spotlight & variety).

---

## Output Format

```md
# PC Arc Builder — {PC name}

## Hook Inventory

| Hook | Status | Score | Integration point |
|------|--------|-------|-------------------|

## Integration Map

### {Hook}: {What existing front/NPC/location picks this up}
- Integration: …
- New material needed: …

## Spotlight Schedule

### Session {N}: {Hook name}
- Window: …
- How to surface: …
- Player agency: …
- Risk of deferral: …

## Gaps to Build

| Gap | Type | Route to |
|-----|------|---------|

## Vault Updates Queued
- {file}: {change}
```

---

## Rules

- PC arcs give the player *opportunities*, not outcomes. The GM creates the pressure; the player makes the choice. Never design an arc that requires the player to respond a specific way.
- A deferred spotlight is a debt. Each session it's pushed, the player feels less seen. Name the deferral cost explicitly.
- Integration must be *organic* — the backstory hook and the active front should be able to coexist naturally, not feel stapled together.
- A hook with no integration point is not a problem; it's a design task. Name it and route it.
- Score determines priority, not attachment. A beloved backstory detail that can't be integrated this arc belongs in the queue, not the schedule.
- Every PC should have at least one hook in Active or Planted status at any given time. If all hooks are Dormant, the player is invisible to the campaign.
