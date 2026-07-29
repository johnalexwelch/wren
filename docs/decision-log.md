# Decision Log — WREN

Decisions are recorded here in reverse-chronological order.
Format: `### Q{N} — {Short title}` followed by **Decision**, **Alternatives considered**, **Tradeoff accepted**.

<!-- Add decisions below -->

### Q8 — The workbench is named Warren and lives in its own repo, on local Forgejo <a id="warren-code-home-and-name"></a>

**Decision:** The Wren Workbench app is named **Warren**, and its code lives in a **new dedicated repo on Alex's local Forgejo instance** (`awelch/warren`) rather than inside `wren` or on GitHub. The name hides *wren* inside a word for a network of connected passages — the vault's link graph the app exists to navigate. Hosting follows the pergamon cutover (tracker guidance is forgejo-primary): Warren is born on Forgejo, and its delivery-funnel issues/PRs live there via the Forgejo API/`tea` (not `gh`). `wren` stays a persona/skills/canon repo; Warren points at the `wren` checkout (persona `CLAUDE.md`, `.claude/skills/`, auto-memory) and the Obsidian vault by configured paths, so the coupling is path config, not code. Scope is Warren only: the wayfinder map and `wren` itself stay on GitHub until this effort completes — wren's migration belongs to pergamon's cutover backlog. The repo is not created until the funnel builds it (plan, don't do); scaffold/template choices are delivery decisions informed by the backend survey. Wayfinder ticket: [wren#6](https://github.com/johnalexwelch/wren/issues/6) (see amendment comment).
**Alternatives considered:** Inside `wren` as an `apps/` subdir (one repo and tracker, no path config — but node_modules, builds, and app CI change the repo's character, and PRD issue volume would drown the D&D/skill work); GitHub `johnalexwelch/warren` (the initial pick this session — reversed because pergamon's whole purpose is moving off GitHub, and a repo that doesn't exist yet migrates for free); also migrating the wren map to Forgejo now (rejected: mid-effort tracker migration friction, GitHub sub-issue relations don't port 1:1); other names — Wren Workbench (descriptive but flat), Bower, Scriptorium, Drafting Table, Roost, Perch.
**Tradeoff accepted:** Two repos on two forges during the transition (map + decisions on GitHub `wren`, code + delivery issues on Forgejo `warren`), agent tooling for Warren must use the Forgejo API/`tea` instead of the `gh`-based skill conventions, and availability depends on the local instance — in exchange for keeping `wren` a pure persona/canon repo, giving the app a real delivery home, and advancing the off-GitHub cutover instead of against it.

### Q7 — Wren Workbench chat is a work surface, not fleet chat; bridged to Matrix by session summary <a id="wren-workbench-chorus-fit"></a>

**Decision:** The Wren Workbench (local web app: chat with Wren, vault browse/edit, connections graph) is a hybrid. Its chat is a **work session surface** — the Claude Code pattern with a better face: transcripts are session artifacts; tool calls, file edits, and skill runs stream inline. This sits outside Chorus F9's "no custom chat" rule, which governs *fleet conversation*; that plane is untouched — quick conversational asks to Wren stay on Matrix (`@wren`, Element), and the workbench does not replace or proxy Matrix. The bridge: on session end, Wren posts a short summary (work done, files touched, decisions) to her Matrix room, and the workbench emits standard F13 audit events to `~/.chorus/audit`, preserving Mira's observability. Wren's charter constraint (canon writes require Alex approval) must surface as an approval step in the workbench UI. Wayfinder ticket: [wren#4](https://github.com/johnalexwelch/wren/issues/4).
**Alternatives considered:** Treat workbench chat as fleet conversation and build it as a Matrix client (F9-pure, but Element/Matrix can't render tool streams, diffs, or skill runs — the actual content of a work session); full transcript mirroring to Matrix (maximum fidelity, but noisy and duplicates the session artifact); audit events only with no Matrix trace (clean, but work sessions become invisible to the fleet conversation record).
**Tradeoff accepted:** A second conversational surface for Wren exists (workbench + Element), in exchange for a work surface that can actually render agent work; the summary-plus-audit bridge keeps the fleet record whole. The "work surfaces are not chat" interpretation should also be noted fleet-side in chorus's decision log so F9's boundary is written down.

### Q6 — Cross-campaign world facts: deferred; WORLD_DECISIONS.md approach tracked

**Decision:** Skip for now. The immediate fix is session-prep Tier 2 filtering by NPC/faction names, which will surface cross-campaign-relevant entries if the GM happens to read them. A proper `WORLD_DECISIONS.md` (cross-campaign locked decisions) and per-session cross-grep would be cleaner but requires vault restructuring.
**Alternatives considered:** Grep other campaign's Decision Log for shared entity names at prep time (fragile, slow); fold cross-campaign facts into each campaign's own Decision Log (duplicates, rots); create `02 World Bible/WORLD_DECISIONS.md` with world-level LOCKED entries (right answer, requires migration work).
**Tradeoff accepted:** Deferred until a cross-campaign prep failure actually occurs and motivates the migration.

### Q5 — CANON.md rejected; tiered context loading adopted for session prep

**Decision:** Skip CANON.md as a manually-maintained artifact. Root cause of AI re-litigating settled decisions is that `dnd-session-prep` never reads `Decision Log.md` or `Story So Far.md`. Fix the actual gap: add Decision Log (LOCKED entries, filtered by relevance), Story So Far, and Storylines & Fronts (active fronts only) as Tier 2 mandatory reads in session prep. No new file to maintain. CANON.md would have required a sixth manual post-session update, compressed 39.9K of Decision Log to 3-4K with lossy results, and become poisonous when stale.
**Alternatives considered:** CANON.md as always-read dense summary (Karpathy-style, ~3-4K words) — rejected: maintenance burden, compression loss on long campaigns, staleness worse than no summary; AI-generated CANON.md regenerated each session — plausible but adds latency and creates a derived artifact; RAG/embeddings — overkill for a single-GM creative domain at this scale.
**Tradeoff accepted:** Tier 2 reads can be heavier per session than a single CANON.md read, in exchange for no maintenance artifact, no staleness risk, and Decision Log remaining the single source of truth.

### Q5 — PLAYER_KNOWLEDGE.md gap closed with new dnd-player-knowledge-sync skill

**Decision:** `PLAYER_KNOWLEDGE.md` was listed in `dnd-session-prep` as a context source but didn't exist and had no creation mechanism. Add `dnd-player-knowledge-sync` skill: runs post-session (triggered from recap-loop Step 11), extracts player-visible information from the session note (NPCs met, facts learned, rumors heard, secrets revealed), appends to `PLAYER_KNOWLEDGE.md`. Append-only; never overwrites history. Session-prep reads it in Tier 2 to prevent clues from re-delivering already-known information or leaking unrevealed secrets.
**Alternatives considered:** Infer player knowledge from session notes during prep (fragile, slow, inconsistent); skip it entirely (perpetuates the GM-knowledge-leak risk).
**Tradeoff accepted:** One additional post-session pass, in exchange for a durable player/GM knowledge boundary that survives across prep sessions.

### Q1 — Two buckets for name reconciliation, split by "would this resolve silently, everywhere?"

**Decision:** Two mechanisms. (1) Strings you always want to resolve to an entity → Obsidian native `aliases:` frontmatter (spelling variants, typos, in-world short forms). (2) Context-dependent transcription garble that must NOT resolve globally (e.g. "silver"→Ciradyl, "half-orc"→Veylar) → a small ingestion-only garble list, consulted only during transcript ingestion.
**Alternatives considered:** Single central alias-map file (duplicates Obsidian's native behavior, rots out of sync); pure-native only with no garble list (loses the catches that actually corrupted canon).
**Tradeoff accepted:** Two mechanisms instead of one, in exchange for not polluting the global namespace with transcription noise and not rebuilding what Obsidian does natively.

### Q2 — Native aliases auto-resolve; garble list flags for confirmation; consumption wired into ingestion skills

**Decision:** Native `aliases:` resolve silently (safe by definition). The garble list is flag-for-confirmation during ingestion, never auto-substituted. Make the behavior durable in `dnd-session-recap-loop` and `dnd-lore-ingestion` rather than leaving it in a WREN memory note that no skill reads.
**Alternatives considered:** Auto-substitute garbles (launders transcription noise into canon); leave consumption in the memory note (keeps not firing).
**Tradeoff accepted:** A confirmation step during ingestion, in exchange for never silently fusing conflicting entities (see the Osborn/Oswald D'emon split).

### Q3 — Scope is error-correction (garbles + spelling variants); diegetic aliases kept separate

**Decision:** The reconciliation system covers transcription garbles and spelling/typo variants only. In-world epithets/titles ("the Uncrowned King," "the Sapphire City") remain legitimate `aliases:` entries but are treated as worldbuilding, not error-correction; the garble list stays error-only.
**Alternatives considered:** One unified alias concept (loses the "is this noise?" signal); fold epithets in now (muddies the test).
**Tradeoff accepted:** Two conceptual categories sharing one frontmatter field, in exchange for keeping the garble list's intent clear.
