# Decision Log — WREN

Decisions are recorded here in reverse-chronological order.
Format: `### Q{N} — {Short title}` followed by **Decision**, **Alternatives considered**, **Tradeoff accepted**.

<!-- Add decisions below -->

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
