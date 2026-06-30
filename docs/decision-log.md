# Decision Log — WREN

Decisions are recorded here in reverse-chronological order.
Format: `### Q{N} — {Short title}` followed by **Decision**, **Alternatives considered**, **Tradeoff accepted**.

<!-- Add decisions below -->

### Q4 — CANON.md rejected; tiered context loading adopted for session prep

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
