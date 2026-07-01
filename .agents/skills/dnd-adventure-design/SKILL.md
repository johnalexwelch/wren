---
name: dnd-adventure-design
model: opus
description: Designs a D&D adventure as a living situation — active factions with goals and timelines, revelations with Three Clue Rule, a node map skeleton, and stakes. Produces the adventure architecture that dnd-session-prep and dnd-node-builder build on. Use when designing an adventure, arc, mystery, or intrigue from a premise. Follows Alexandrian prep (situation not plot). Triggers on "design this adventure", "build this arc", "design the situation", "prep an adventure", "structure this mystery", or after dnd-grill approves a premise.
---

# dnd-adventure-design

Build the adventure's architecture — not what will happen, but what *is happening* when the players arrive. This is the structure `dnd-session-prep` runs on and `dnd-node-builder` details. Keep it a situation, not a script.

## Where this sits in the pipeline

```
dnd-grill (premise) → dnd-adventure-design (this skill) → decision-log
  → dnd-node-builder (clue web detail)
  → dnd-review *continuity* + *agency*
  → dnd-session-prep (table execution)
```

## Contract

Consumes: approved premise (from `dnd-grill`), campaign state (canon docs if available)
Produces: structured adventure document with situation, factions, revelation map, timeline, node skeleton, and stakes
Requires: at minimum a premise; richer output when campaign docs are available
Side effects: may update `TIMELINE.md`, `factions/`, `OPEN_THREADS.md` after explicit acceptance
Human gates: faction goals and the adventure timeline accepted before finalizing

---

## Workflow

### 1. Anchor in campaign state

Read available canon in order: `CAMPAIGN_MAP.md` (points to everything live), `TIMELINE.md`, `OPEN_THREADS.md`, relevant `factions/**`, `npcs/**`, `locations/**`. If no campaign docs exist, work from the premise alone and note what needs to be established.

Capture: what's already in motion that this adventure connects to, and what player knowledge already exists that might short-circuit a revelation.

---

### 2. Frame the situation

Write a one-paragraph situation brief: **what is actively happening in the world right now, without the players.** Not "the villain is planning something" — name the plan, the stage it's at, and what happens next if nothing intervenes.

The situation is the adventure. The players' choices change it; they don't trigger it.

> **Example:** *The Pale Compact is two nights from completing the Unbinding. Castellan Vhara has the final component and is en route to the Tomb of Echoes. High Inquisitor Doran knows something is wrong but has the wrong target — he believes House Meren is behind it and will arrest them at dawn. The Compact's street network is actively watching for interference.*

---

### 3. Map active factions

For every faction with agency in this adventure, define:

| Field | What to answer |
|-------|---------------|
| **Goal** | What do they want by the end of this adventure? |
| **Method** | How are they pursuing it right now? |
| **Timeline** | What do they do at each clock beat if unchecked? |
| **Resources** | What do they have — leverage, knowledge, muscle, access? |
| **Obstacle** | What's in their way, including the other factions? |
| **Pressure point** | What could the players exploit to flip, redirect, or break them? |
| **Player knowledge** | What do the players currently know or believe about this faction? |

Factions should be able to succeed without the players. If they can't, they're not factions — they're props.

---

### 4. Define revelations with the Three Clue Rule

List every **revelation** the adventure needs to reach its conclusion — truths the players must be able to discover for the situation to make sense.

For each revelation, provide **at least three independent clues** in different locations, different mediums, and different circumstances. No single point of failure.

```
REVELATION: [The thing that is true]
  Clue A: [What, where, how discovered]
  Clue B: [What, where, how discovered]  
  Clue C: [What, where, how discovered]
  Player knowledge check: [Do they already know any of this?]
```

Distinguish **GM truth** from **in-world belief**. A clue can be a rumor, a lie, or a misreading — as long as three different paths lead to the real answer.

---

### 5. Build the adventure timeline

Map what each faction does at each clock beat if the players don't intervene. Make this concrete — not "the villain advances his plan" but what specifically moves.

```
T+0 (now):     [Situation as established]
T+1 (session 1 end, if unchecked): [Each faction's next move]
T+2:           [...]
T+final:       [How it resolves without player intervention]
```

The timeline is the pressure that makes player choices matter. Update it after each session.

---

### 6. Node map skeleton

Sketch the high-level node map — the locations and NPCs that carry the revelations and faction activity. This is the skeleton; `dnd-node-builder` builds the clue web detail.

For each node, name:
- What's here (location or NPC)
- What revelation(s) it can surface
- Which faction(s) are present or have interest
- Entry conditions (open / gated behind prior discovery / gated behind player action)

Mark any **required nodes** (must be reachable for the adventure to resolve) and **bonus nodes** (enrich but aren't load-bearing). No required node should be gated behind a single prior node — that's a bottleneck, not a network.

---

### 7. Define stakes and consequences

State the answer to: **what does success look like, what does failure look like, and what does partial success look like?**

Stakes should be visible to players before they're fully committed. Consequences should be real — not "the villain escapes to return later" as a default, but something that concretely changes the world state.

---

### 8. Identify encounter situations

Name 3–5 encounter *situations* — not fights, not scenes, but situations the players will need to navigate. Each situation should have:
- A goal at stake (not necessarily combat)
- The faction or force generating pressure
- At least two visible options for how to engage
- A consequence if the players skip or fail it

These are inputs to `dnd-session-prep`, not scripts.

---

## Output format

```md
# Adventure Design: {title}

## Situation brief
{One paragraph: what is actively happening, who's doing it, where it stands}

## Active factions
### {Faction name}
- **Goal:** …  
- **Method:** …  
- **Timeline:** T+0 → T+1 → T+final  
- **Resources:** …  
- **Pressure point:** …  
- **Player knowledge:** …

## Revelations
### Revelation: {truth}
- Clue A ({location/NPC}): …
- Clue B ({location/NPC}): …
- Clue C ({location/NPC}): …

## Adventure timeline
| Beat | World state |
|------|-------------|
| T+0  | …           |
| T+1  | …           |

## Node map (skeleton)
| Node | Revelations | Factions | Entry | Required? |
|------|-------------|----------|-------|-----------|
| …    | …           | …        | open  | yes/no    |

## Stakes
- **Success:** …
- **Failure:** …  
- **Partial:** …

## Encounter situations
1. {Situation}: goal, pressure, options, skip consequence
…
```

---

## Handoffs

- **Feeds into:** `dnd-node-builder` (clue web and discovery path detail), `dnd-session-prep` (table execution)
- **Receives from:** `dnd-grill` (premise validation), campaign state docs
- **After acceptance:** update `TIMELINE.md` with new clocks, create or update `factions/` entries, add new hooks to `OPEN_THREADS.md`
