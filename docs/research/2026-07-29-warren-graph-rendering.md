# Warren connections graph — data model and rendering survey

Resolves wayfinder ticket [wren#8](https://github.com/johnalexwelch/wren/issues/8) (map: [wren#3](https://github.com/johnalexwelch/wren/issues/3)).
Date: 2026-07-29. Method: vault ground-truth measurement + doc-grounded renderer research (Claude research agent against current npm/GitHub/docs) + a working twin-renderer spike over the real vault data.

## Question

What does the connections graph get built from, and how does it render? Binding inputs from [Q9](../decision-log.md#warren-obsidian-optional) (campaign-semantic bar: typed nodes, campaign/era/status/disposition/visibility filters, labeled edges; acceptance: NPC↔artifact/location links and NPC↔NPC relationship *status* on the edge) and [Q10](../decision-log.md#warren-backend-agent-sdk) (graph reads the derived SQLite-class index in Warren's TS runtime, not the vault; React front-end; ~820 vault files).

## Part 1 — What the vault actually encodes (measured 2026-07-29)

820 markdown files; 810 carry `type:` frontmatter. Entity types worth graphing: **npc 244, location 198, organization 48, artifact 35, front 7, pc 6, event 4** → **~525 graph nodes** after excluding sessions/prep/templates/archive. Filter attributes exist on nearly all of them: `campaigns` (747 files), `eras` (579), `status` (796), `visibility` (807), `disposition` (117, NPCs).

Relationships live in **three layers of decreasing structure**:

| Layer | Where | Volume today | What it gives |
|---|---|---|---|
| **Ledger notes** (`type: relationship`, `11 Relationship Ledger/`) | dedicated file per pair | 8 files | Richest: `relationship_kind`, `current_state`, `reciprocity`, `from_knows`/`to_knows`, `known_to_players`, per-side public labels |
| **Relationship tables/sections** in entity files | `## Relationships` bullets + several table shapes (`\| NPC \| Relationship \|`, `\| Character \| Relationship \|`, `\| NPC \| Relationship \| Disposition \|`, …) | 114 files with headings, 112 with tables → **159 labeled edges** parsed | Labeled edge + free-text status |
| **Raw wiki links** | prose everywhere | 8,888 links, 938 unique targets → **1,672 node-to-node edges** (deduped, typed endpoints only) | Unlabeled co-reference context |

**Data-model decision:** the index materializes an `edges` table from all three layers with a `kind` discriminator (`ledger` > `table` > `wiki`); a wiki edge is shadowed when a labeled edge exists for the same pair. Nodes come from typed frontmatter with the five filter attributes. This is exactly the Q10 derived-index shape — the graph pane is a *view over the index*, and the same edge table doubles as a Wren-queryable tool ("who has an unresolved grudge in Ciradyl?").

Caveats that belong in the PRD, found by actually parsing:

- **Table-format sprawl is the fragile part.** The 159 labeled edges hide behind at least 4 header variants. The index parser needs a tolerant header-sniffing rule (entity column ∈ {NPC, Character, Name, Who, PC} + any column containing "Relationship"); long-term, nudge authoring toward the Ledger (its frontmatter is machine-perfect and already models asymmetry and player knowledge).
- **66 of 525 typed nodes are orphans** (degree 0) — an "unconnected entities" view is a real prep tool, not an error state.
- Alias resolution (`aliases:` frontmatter, per decision Q1) was not exercised by the spike extractor; the index must resolve aliases when matching link targets to nodes.

## Part 2 — Renderer survey (verified July 2026)

Full comparison in the research transcript; the short table (all verified against npm/GitHub this month):

| | Cytoscape.js 3.34 | sigma.js 3.0 + graphology | d3-force + custom | React Flow 12 | G6 v5 |
|---|---|---|---|---|---|
| Rendering | Canvas 2D | **WebGL** + canvas labels | DIY | DOM/SVG | Canvas/WebGL |
| 1–2k nodes / 10k edges | workable, not silky | **excellent** | on you | past its comfort zone | good |
| Labeled edges | **best-in-class** (stylesheet, autorotate) | good (`renderEdgeLabels`, zoom-culled) | DIY | JSX labels but wrong scale | first-class |
| Filtering | selectors, very good | **`nodeReducer`/`edgeReducer` — purpose-built** | DIY | React state | good |
| React | hand-rolled `useEffect` wrapper (`react-cytoscapejs` stale) | **`@react-sigma`** wrapper, hooks | DIY | native | improving |
| Layout | cose built-in, fcose plugin (good) | **ForceAtlas2, web-worker capable** | d3-force | none built-in | strong |
| License / size | MIT / ~110 KB | MIT / ~80 KB total | ISC / tiny | MIT | MIT / 200–500 KB |

Ruled out: React Flow (node-editor, no layout engine, DOM wall at our edge counts), vis-network (dated, janky physics), Reagraph (Three.js baggage for a 2D problem), Cosmograph (CC-BY-NC license; solves a scale we don't have).

**Prior art converges:** Obsidian (custom pixi.js/WebGL), Quartz (d3-force + pixi), Logseq (pixi-graph + graphology) all pair a force layout with WebGL rendering; Dendron and Foam chose Cytoscape.js when they wanted filtering/analysis out of the box. Nobody in this genre uses React Flow or vis-network.

## Part 3 — Twin spike over the real vault (what actually happened)

Both finalists were run over the same extracted dataset — **525 nodes / 1,838 edges (166 labeled)** — as single-file pages with type/campaign/edge-kind filters and click-to-focus. Spike code: [`docs/research/spikes/2026-07-29-graph-rendering/`](spikes/2026-07-29-graph-rendering/) (extractor + page generator; the extracted JSON stays local — it contains GM-only relationship data).

- **sigma.js v3**: ForceAtlas2 (300 iterations) + first render in **176 ms**; filter toggles via reducers refresh in **~7 ms**; click-to-focus dims the rest of the graph cleanly; zooming into a focused NPC (Mirael Duskfern) renders relationship status on every labeled edge — "healer and patient; protective friendship", "former respect; quiet distrust", "Like sisters" — i.e. the Q9 acceptance example, working. Layout quality is clearly the best of the two (hub-and-cluster structure legible at full zoom-out).
- **Cytoscape.js**: functionally equivalent (selectors filtered 1.8k edges in ~3 ms; focus/dim works), but the built-in `cose` layout **blocked the UI for multiple seconds** at 525 nodes (fcose plugin would improve it), always-on edge labels are unreadable noise at full view, and the neighborhood layout is visibly clumpier.
- Practical note: sigma v3 ships **ESM-only** (no UMD/CDN script tag) — irrelevant for Warren's bundled React app, but it made the spike itself need `esm.sh`.

## Recommendation

**sigma.js v3 + graphology + `@react-sigma`**, with edges from the three-layer index model above.

1. **The interaction model fits exactly.** `nodeReducer`/`edgeReducer` implement Warren's two core interactions — attribute filtering and focus-neighborhood dimming — declaratively, without mutating the graph. The spike did each in ~10 lines and ~7 ms.
2. **graphology is not just plumbing.** It's a real in-memory graph model (typed attributes, events, metrics/communities in its standard library) — the natural in-browser materialization of the index's graph tables, and useful for prep queries beyond rendering.
3. **Performance headroom is free.** WebGL keeps 525 nodes trivially smooth and won't blink if the vault doubles or the graph later includes sessions/events (1,600+ nodes). FA2 runs in a web worker for live layout.
4. **Prior-art alignment.** Obsidian-genre tools converged on force layout + WebGL; Warren's graph will *feel* like the graph Alex already knows, then beat it on semantics (typed filters, labeled edges, GM/player visibility — none of which Obsidian's graph has).
5. **Labels-on-zoom is the right UX anyway.** Sigma's one weakness (canvas-drawn edge labels with zoom culling) matches the sane design: relationship labels appear on zoom/hover/focus, not 1,672-at-once.

**Named fallback:** Cytoscape.js (+fcose, layout in a worker) if edge-label typography or stylesheet-grade edge styling ever proves insufficient in sigma — its edge labels are best-in-class and the data model above ports unchanged. G6 v5 is the second fallback if sigma feels too low-level. The renderer is a leaf dependency behind the index; swapping it later strands only the pane component.
