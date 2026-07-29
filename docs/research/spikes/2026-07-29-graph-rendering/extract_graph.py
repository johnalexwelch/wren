#!/usr/bin/env python3
"""Extract a campaign-semantic graph from the CotUK vault -> graph.json.

Nodes: md files with `type:` frontmatter (npc, location, organization, artifact, pc, ...).
Edges:
  - wiki: raw [[wiki links]] between two typed nodes (deduped, unlabeled)
  - rel-section: bullets under a '## Relationships'-style heading: [[Target]] — label
  - ledger: files with type: relationship -> labeled edge between participants
Node attrs: type, campaigns, eras, status, disposition, visibility.
"""
import json, os, re, sys
from pathlib import Path

VAULT = Path("/Users/alexwelch/Documents/Home/Areas/DnD/GM/Chronicles of the Uncrowned King")
OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "graph.json")

FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.S)
LINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")
REL_HEAD_RE = re.compile(r"^#{2,3} .*relationship", re.I)

def parse_fm(text):
    m = FM_RE.match(text)
    if not m:
        return {}, text
    fm, body = {}, text[m.end():]
    key = None
    for line in m.group(1).splitlines():
        if re.match(r"^[A-Za-z_-]+:", line):
            key, _, val = line.partition(":")
            val = val.strip().strip('"')
            fm[key.strip()] = val if val else []
        elif key is not None and line.strip().startswith("- ") and isinstance(fm.get(key), list):
            fm[key].append(line.strip()[2:].strip().strip('"'))
    return fm, body

files = {}
for p in VAULT.rglob("*.md"):
    if "99 Archive" in p.parts or "90 Assets" in p.parts:
        continue
    try:
        text = p.read_text(errors="ignore")
    except OSError:
        continue
    fm, body = parse_fm(text)
    files[p.stem] = (p, fm, body)

KEEP_TYPES = {"npc", "location", "organization", "artifact", "pc", "front", "event", "faction", "relationship"}
nodes, name_ok = {}, set()
for stem, (p, fm, body) in files.items():
    t = (fm.get("type") or "").strip() if isinstance(fm.get("type"), str) else ""
    if t.lower() in KEEP_TYPES and t != "relationship":
        nodes[stem] = {
            "id": stem, "type": t.lower(),
            "campaigns": fm.get("campaigns") if isinstance(fm.get("campaigns"), list) else [],
            "eras": fm.get("eras") if isinstance(fm.get("eras"), list) else [],
            "status": fm.get("status", "") if isinstance(fm.get("status"), str) else "",
            "disposition": fm.get("disposition", "") if isinstance(fm.get("disposition"), str) else "",
            "visibility": fm.get("visibility", "") if isinstance(fm.get("visibility"), str) else "",
        }
        name_ok.add(stem)

edges, seen = [], set()

def add_edge(src, dst, kind, label=""):
    if src not in name_ok or dst not in name_ok or src == dst:
        return
    k = (src, dst, kind, label)
    if k in seen:
        return
    seen.add(k)
    edges.append({"source": src, "target": dst, "kind": kind, "label": label})

for stem, (p, fm, body) in files.items():
    t = (fm.get("type") or "") if isinstance(fm.get("type"), str) else ""
    # ledger relationship files
    if t.strip().lower() == "relationship":
        parts = [LINK_RE.search(x).group(1).strip() for x in (fm.get("participants") or []) if LINK_RE.search(x)]
        label = fm.get("relationship_kind", "") if isinstance(fm.get("relationship_kind"), str) else ""
        if len(parts) >= 2:
            add_edge(parts[0], parts[1], "ledger", label)
        continue
    if stem not in nodes:
        continue
    # relationship-section labeled edges
    in_rel = False
    for line in body.splitlines():
        if line.startswith("#"):
            in_rel = bool(REL_HEAD_RE.match(line))
            continue
        if in_rel and line.strip().startswith("- "):
            m = LINK_RE.search(line)
            if m:
                label = re.split(r"—|--|:", line.split("]]", 1)[-1], 1)[-1].strip(" -–—:") if "]]" in line else ""
                add_edge(stem, m.group(1).strip(), "rel", label[:80])
    # relationship tables: header row with an entity col + a Relationship col
    lines = body.splitlines()
    for i, line in enumerate(lines):
        if not (line.strip().startswith("|") and re.search(r"\|\s*relationship", line, re.I)):
            continue
        cols = [c.strip().lower() for c in line.strip().strip("|").split("|")]
        ent = next((j for j, c in enumerate(cols) if c in ("npc", "character", "name", "who", "pc")), None)
        rel = next((j for j, c in enumerate(cols) if "relationship" in c), None)
        if ent is None or rel is None:
            continue
        for row in lines[i + 2:]:
            if not row.strip().startswith("|"):
                break
            cells = [c.strip() for c in row.strip().strip("|").split("|")]
            if len(cells) <= max(ent, rel):
                continue
            m = LINK_RE.search(cells[ent])
            if m and cells[rel]:
                add_edge(stem, m.group(1).strip(), "rel", cells[rel][:80])
    # plain wiki links
    for m in LINK_RE.finditer(body):
        add_edge(stem, m.group(1).strip(), "wiki")

# drop wiki edges shadowed by a labeled edge on the same pair
labeled = {(e["source"], e["target"]) for e in edges if e["kind"] != "wiki"}
labeled |= {(b, a) for a, b in labeled}
edges = [e for e in edges if e["kind"] != "wiki" or (e["source"], e["target"]) not in labeled]

out = {"nodes": list(nodes.values()), "edges": edges}
OUT.write_text(json.dumps(out, indent=1))
tc = {}
for n in nodes.values():
    tc[n["type"]] = tc.get(n["type"], 0) + 1
kc = {}
for e in edges:
    kc[e["kind"]] = kc.get(e["kind"], 0) + 1
print(f"nodes={len(nodes)} edges={len(edges)} types={tc} edgekinds={kc}")
