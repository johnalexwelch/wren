---
name: dnd-location-builder
model: opus
description: Designs a playable D&D location — sensory texture, interactive zones, embedded secrets with Three Clue Rule, NPC residents, faction presence, and how the location changes over the campaign timeline. Follows Alexandrian prep conventions (location as situation, not set piece). Use when the party is about to enter a new location that needs to feel real, when session prep calls for a location to be fleshed out, or when a location carries story weight. Triggers on "build out this location", "design the {place}", "what's in the {place}", "make this location playable", "flesh out {place}".
metadata:
  codex-compatible: false
---

# dnd-location-builder

A location is not a backdrop. It's a situation with its own logic — who controls it, who wants it, what secrets it holds, how it changes under pressure. This skill builds locations the way Alexandrian prep builds adventures: as living places that survive player choice.

**Distinct from related skills:**
- `worldbuilding-deep-dive` — general worldbuilding depth (history, culture, sensory texture). Use that for world-level development; use this for a specific playable space.
- `dnd-adventure-design` — designs the full adventure situation (factions, timelines, node map). Use that for adventure architecture; use this to flesh out one location within it.
- `dnd-node-builder` — builds the clue web and investigation paths. This skill feeds `dnd-node-builder` with the location's secrets.

## Contract

Consumes: location name, type, campaign/era, and intended role in the session or arc
Produces: location doc with sensory texture, zones, interactive elements, secrets, NPC residents, faction presence, campaign timeline
Requires: at minimum a location name and its role in the current session or arc
Side effects: creates vault location file after acceptance
Human gates: user approves secrets and faction presence before vault write

## Soft Context

Typical workflows: dnd-session-prep calls for a location → dnd-location-builder → dnd-node-builder (if location carries investigation) → dnd-session-prep
Pairs well with: dnd-node-builder (embed this location's secrets in the clue web), dnd-encounter-design (if a combat/tactical scene happens here), dnd-player-facing-writer (player-safe description or handout for the location)

---

## Workflow

### 1. Establish the location's role

Before building anything, answer: **what is this place *for* in the campaign right now?**

- Is it a one-session location or a recurring anchor?
- What story question does the party come here to answer?
- What front or faction operates here?
- Is it contested, controlled, or neutral?

If the role is unclear, ask. A location without a role is just decoration.

---

### 2. Read campaign context

Pull from the vault:
1. Campaign Dashboard — is this location already referenced?
2. Relevant front or faction docs — who operates here?
3. Timeline — has this location appeared before or been referenced in session notes?
4. OPEN_THREADS.md — are there active threads that touch this location?

---

### 3. Physical orientation

Define three layers — don't over-specify, but give the table enough to navigate:

**Entry impression (what players see first):**
The single image that establishes the location's register. Not a paragraph — the specific thing that lands on arrival. "The staircase descends into water. The water is still."

**Zones:**
Identify 2–5 distinct areas of the location. Each zone should have:
- A name (for GM shorthand)
- A dominant sensory texture
- What's *interactive* here — the objects, surfaces, mechanisms, or people players can engage

Zones are not rooms on a map. They're the meaningful subdivisions the party will naturally move through.

**Depth axis:**
What's visible on entry vs. requires engagement to discover vs. requires investigation to find.

| Layer | Access | Example |
|-------|--------|---------|
| Surface | Just arriving | The carved raven mark on the doorpost |
| Engaged | Talking to someone, interacting with an object | Brogan's Whisperbond scar under his sleeve |
| Investigated | Active search, NPC convincing, skilled check | The hidden channel behind the bar where the Ebon Veil leaves notes |

---

### 4. Sensory texture

For each zone, nail the dominant sensory register — not a list of descriptors, but the *one thing* the player will remember:

- **Smell** (often the most evocative)
- **Sound** (what's always in the background here)
- **Tactile** (what do players touch or feel underfoot)
- **Visual register** (lighting, scale, clutter vs. empty)

At the table, you will use one or two of these per zone. Write them all; choose when you arrive.

---

### 5. Interactive elements

List 3–6 things players can *do* here that aren't encounters. Interactive elements create player investment:

- Objects that can be examined, moved, or used
- NPCs with something to say or give
- Mechanisms that respond to player action
- Hazards that create choice (the unstable floor, the exposed wire, the locked box)
- Atmosphere elements that reward curiosity (the date carved into the wall, the half-empty glass)

For each: what does a player who engages with it *get*? (Information, an item, a relationship change, a complication.)

---

### 6. Embedded secrets (Three Clue Rule)

List 2–4 secrets the location contains. For each, apply the Three Clue Rule — at least three independent ways a player can discover it:

```md
### Secret: {the truth}

**Clue A** ({zone/NPC/method}): {what players find/hear/see and what it points toward}
**Clue B** ({zone/NPC/method}): {independent path to the same truth}
**Clue C** ({zone/NPC/method}): {third path — different sense, different access method}

**Player knowledge gate:** {do players already know any of this?}
**What this unlocks:** {what this secret connects to — front, NPC arc, open thread}
```

Secrets range from location-specific (something about this place's history or current use) to campaign-bearing (something that feeds an active revelation arc or front).

---

### 7. Residents and NPCs

Name everyone who is here — the regulars, the one-time visitors, the hidden occupants.

For each NPC present:

| NPC | Role | What they want here | What they know | What they'll share |
|-----|------|---------------------|----------------|-------------------|
| {Name} | {regular / visitor / hidden} | {goal in this location} | {relevant knowledge} | {conditions under which they share} |

At minimum: one NPC the party can talk to, one who has something to hide.

---

### 8. Faction presence

Who controls or operates in this location, and how?

| Faction | Presence | Goal | What changes if they're found out |
|---------|----------|------|----------------------------------|
| {Name} | {overt / covert / competing} | {what they want here} | {consequence of discovery} |

If a faction controls the location, define their *tells* — the things a perceptive party can notice that reveal the faction's hand.

---

### 9. Campaign timeline

How does this location change as the campaign progresses?

Define at least two states:

**Now (current session):** {what's here, who's present, what's in motion}
**After {front/event X}:** {how the location changes when that front resolves or escalates}
**Endgame:** {what this place looks like after the main arc resolves — if it survives}

A location that never changes isn't really alive. Even a tavern changes if the war reaches the city.

---

### 10. Vault write

Write to `01 Campaigns/{Campaign}/Locations/{Location Name}.md` using `vault-write` conventions. Include standard Location frontmatter.

If the location is shared across campaigns or world-level, write to `03 Shared Locations/`.

---

## Output Format

```md
# {Location Name} *(pronunciation if needed)*

## Role in campaign
{One sentence: what this place is for right now}

## Entry impression
{The single image that lands on arrival}

## Zones

### {Zone name}
- **Texture:** {dominant sensory register}
- **Interactive:** {what players can do here}

## Sensory reference
- Smell: …
- Sound: …
- Tactile: …
- Lighting/scale: …

## Interactive elements
1. {Object/NPC/mechanism}: {what engaging it gets the player}

## Secrets
### Secret: {truth}
- Clue A ({zone/method}): …
- Clue B ({zone/method}): …
- Clue C ({zone/method}): …
- Unlocks: …

## Residents
| NPC | Role | Wants | Knows | Will share if |
|-----|------|-------|-------|--------------|

## Faction presence
| Faction | Presence | Goal | Tell |
|---------|----------|------|------|

## Campaign timeline
- **Now:** …
- **After {event}:** …
- **Endgame:** …

## DM running notes
- Watch for: …
- Don't over-describe: …
```

---

## Rules

- Entry impression is one image, not a paragraph. The table is waiting to play.
- Zones are navigational, not architectural. Players experience them, not the floorplan.
- Every interactive element must *get* the player something — even if it's just flavor that sticks.
- The Three Clue Rule applies to embedded secrets. A secret with only one path is fragile.
- Faction presence needs *tells* — the thing a perceptive party notices. Covert factions don't advertise; but they leave traces.
- Campaign timeline is non-negotiable. A location that never changes is a stage set, not a place.
- Don't build what won't be used. A single-session location needs less than a recurring anchor.
