# Warren — future feature roadmap (parking lot)

**Status: NOT in the current build.** Captured 2026-07-31 at Alex's request so these don't lose visibility while PRD 1–3 ship. Nothing here is committed, scoped, or scheduled — this is an idea register with enough context that picking one up later doesn't mean re-deriving the thinking.

Current build for reference: PRD 1 vault index (done), PRD 2 agent backend (in flight), PRD 2 addendum (identified — browser-facing server surfaces), PRD 3a–3d workbench shell. Post-v1 but already decided: Q15's GM run-mode preset (phase 1) and player-facing companion view (phase 2).

Each item below notes what it likely is, what it depends on, and the one consideration that isn't obvious.

---

## 1. Templates

New-note scaffolding driven by the vault's **existing** `10 Templates/` directory (`Template - Artifact.md`, `- Encounter.md`, `- Era.md`, `- Event.md`, `- Front.md`, and more).

- **Depends on:** PRD 3d's new-note affordance.
- **Consideration:** the templates already exist and are hand-maintained. Warren should *read* them, not invent a parallel template system — otherwise there are two sources of truth for what an NPC note looks like. Template frontmatter is also the natural place to derive the properties strip from.

## 2. Custom instructions

Per-campaign or per-session steering layered on top of Wren's persona (tone, house rules, current arc emphasis, "don't spoil X").

- **Depends on:** nothing structural; the turn-context mechanism from PRD 3's focused-document work is the same plumbing.
- **Consideration:** this must be **config, not memory** — Q16 deliberately rejects a Warren-side memory layer, and instructions that Wren silently rewrites would become exactly that. Likely a vault-side or config file that enters turn context, versioned and visible, with edits flowing through the normal approval gate if it lives in the wren repo.

## 3. Image generation

Generate portraits, item art, scene illustrations, and map assets into the vault's `90 Assets/`.

- **Depends on:** PRD 3d's image handling (display route + insert path) landing first — generation is useless without somewhere to put and show the result.
- **Consideration:** generated files are **agent writes**, so they flow through the approval card like any canon change — which means the card needs to render an image preview, not a text diff. Also introduces a new external API (a second secret under Q13's custody, plus a WebFetch/allowlist question).

## 4. Music generation

Ambience and theme tracks for sessions.

- **Depends on:** nothing in the current build.
- **Consideration:** the least-defined item. Licensing and model availability are open questions, and audio files are large enough that putting them in the vault conflicts with a plain-markdown repo that gets scanned and indexed. Likely an external tool with links stored in notes, rather than in-vault binaries — worth deciding that before any build work.

## 5. Map creator and editor

Region/hex/city maps as first-class, editable objects linked to location notes.

- **Depends on:** image handling; probably its own PRD.
- **Consideration:** the heaviest item on this list by a wide margin, and the one most likely to want a bespoke canvas editor. It has a real head start though: the index already holds **198 typed location nodes** with `parent_location` relationships, so the containment hierarchy a map needs is already extracted. Decide early whether maps are *authored* in Warren or *imported* and annotated — those are different products.

## 6. Combat creator and simulator

Encounter building plus run-time tracking (initiative, HP, conditions, terrain effects).

- **Depends on:** Q15's phase-1 GM run mode (initiative and clocks already live there).
- **Consideration:** the vault has **41 encounter nodes**, but as prose — there is no structured statblock or rules model anywhere, and that model is most of the work. This is where Warren would stop being a knowledge tool and start being a rules engine; worth an explicit decision about whether that's wanted, or whether it should defer to existing tools and only own the narrative side.

## 7. Player-facing notes

Publish or share filtered, spoiler-safe views of canon.

- **Depends on:** Q15 phase 2 already covers the companion *view*; this is the authoring/export side.
- **Consideration:** the data model nominally exists — `visibility` frontmatter plus `12 Player-Facing Packet/` and the `dnd-player-facing-writer` skill — **but it is effectively unpopulated: 800 files are `visibility: gm` and only 8 are `player`/`player-safe`.** So this feature is mostly a *tagging and curation* problem, not a rendering problem. Any build must start by making visibility a trustworthy boundary (Q15 says the same thing), because a leak here spoils the campaign rather than merely breaking a screen.

## 8. Timeline generator

Visual timeline of eras, events, and session history.

- **Depends on:** nothing new — reads what the index already has.
- **Consideration:** the cheapest genuinely useful item here. `eras` frontmatter is on **579 files**, `06 Timeline & Eras/` and `13 Events/` already exist, and the index extracts era attributes today. This is close to a pure view over existing data, which makes it a good early win once the shell exists.

## 9. Calendar generator

In-world calendar with date math (travel time, festival cycles, "what day is it").

- **Depends on:** a defined calendar system for the world (month names, week length, year zero) — which lives in the World Bible, not in code.
- **Consideration:** the sharp edge is that notes carry **two kinds of date**: real-world `created`/`session_date` and in-world era/event dates. Conflating them will produce nonsense. Define the in-world calendar as canon first, then the tool becomes straightforward.

---

## Rough grouping, if these ever get sequenced

- **Cheap, reads existing data:** timeline (8), templates (1), custom instructions (2)
- **Needs the image pipeline first:** image generation (3), then map creator (5)
- **Needs a data model that doesn't exist yet:** combat (6), calendar (9), player-facing curation (7)
- **Needs a scoping decision before any build:** music (4)

Not a commitment to that order — just where the cheap wins and the hidden costs sit.
