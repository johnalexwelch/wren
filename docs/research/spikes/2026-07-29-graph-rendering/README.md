# Graph-rendering spike (wren#8)

Twin-renderer spike behind [docs/research/2026-07-29-warren-graph-rendering.md](../../2026-07-29-warren-graph-rendering.md).

```bash
python3 extract_graph.py graph.json   # reads the vault (read-only), writes graph.json locally
python3 build_spikes.py               # inlines graph.json into spike-sigma.html + spike-cytoscape.html
python3 -m http.server 8788           # open http://localhost:8788/spike-sigma.html
```

`graph.json` and the generated HTML are **not committed** — they embed vault content including GM-only relationship data (`visibility: gm`, `known_to_players: false`). Regenerate locally.

Measured 2026-07-29: 525 nodes / 1,838 edges (166 labeled). sigma v3: FA2+render 176 ms, reducer filters ~7 ms. Cytoscape `cose`: multi-second synchronous layout at the same size.
