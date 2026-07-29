# Workbench layout prototype — answer capture

Wayfinder ticket: [wren#9](https://github.com/johnalexwelch/wren/issues/9). HITL session with Alex, 2026-07-29.

## Round 1 — `prototype.html`

**Question:** Which pane arrangement makes Warren feel right for planning work?

Variants (same fake-vault fixture, three renderings):

1. `chat-primary` — chat is home; files + graph slide over from the right
2. `three-pane-studio` — vault tree / editor / chat, all visible; connections strip under the editor
3. `graph-home` — graph is the canvas; chat docked; notes peek from nodes

**Winner: `three-pane-studio`.** Alex: "I like 2 (with the markdown formatted)." Explicit follow-ups: the note must render as formatted markdown (not raw source), and the always-on mini-graph strip failed — "the connections piece isn't very helpful because I can't dive into the visual."

Rejected: chat-primary (buries the vault behind a slide-over), graph-as-home (graph is a tool, not the home).

## Round 2 — `connections.html`

**Question:** What format lets Alex actually dive into connections from the current note?

Same three-pane shell, formatted markdown, three treatments of the connections slot under the editor:

1. `focus-graph` — click a node to re-center the neighborhood on it
2. `linked-panel` — Obsidian-style typed backlink groups
3. `rel-table` — flat relationship table (entity / relationship / type / source layer), click-through

**Winner: `rel-table` + an on-demand full-graph overlay.** Alex: "I like option 3 as well as having the ability to launch the connections graph." A `⤢ open graph` button on the connections header expands a full-screen graph overlay (sigma.js in the real app, per Q11); clicking any entity anywhere — wiki link, table row, graph node — refocuses the whole workspace. Chat stays a right-hand rail: "chat should be on the side so I can interact with everything."

## Final direction (feeds the PRD)

- **Three-pane studio**: vault tree (left) / rendered-markdown editor (center) / chat rail (right)
- **Connections = relationship table** under the editor; typed edges with source layer; click-through refocuses
- **Full graph is launched on demand** as an overlay from the connections header — not an always-on pane
- Editor renders formatted markdown by default with an edit-source toggle; frontmatter as a properties strip
- Staleness banner (Q9), inline tool streams + canon-approval card in chat (Q7/Q10) all fit the shell as prototyped

## How to view

```bash
python3 -m http.server 8931 --directory docs/research/spikes/2026-07-29-workbench-layout
```

Open `http://localhost:8931/prototype.html` (round 1) or `connections.html` (round 2); switch variants with keys 1–3.
