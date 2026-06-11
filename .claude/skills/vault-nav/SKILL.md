---
name: vault-nav
model: sonnet
description: Navigate and search the Chronicles of the Uncrowned King Obsidian vault efficiently. Use before any session work, continuity check, or research task that requires reading campaign state. Handles dashboard-first orientation, grep searches, wiki-link tracing, and graphify integration for deep cross-reference queries.
---

# Vault Nav

Orient Wren in the CotU vault before doing any substantive work. The vault is at `~/Documents/Home/Areas/DnD/GM/Chronicles of the Uncrowned King/` — hereafter `$VAULT`.

## Contract

Consumes: task intent (session prep, continuity check, NPC research, worldbuilding, etc.)
Produces: loaded context from the vault — relevant session notes, active threads, NPC states, faction moves
Requires: filesystem access to `$VAULT`
Side effects: may run graphify on `$VAULT` when `--graph` is passed
Human gates: none

## Vault Root

```
VAULT=~/Documents/Home/Areas/DnD/GM/Chronicles of the Uncrowned King
```

---

## Step 1: Identify scope

What campaign and what task?

| Task | Starting point |
|---|---|
| Session prep (CotAS) | Campaign Dashboard → recent session → Storylines & Fronts |
| Session prep (Echos) | Campaign Dashboard → OPEN_THREADS.md → recent session |
| Session recap | Most recent session note in `Sessions/` |
| NPC research | `NPCs/<name>.md` → trace `[[wiki links]]` |
| Continuity check | OPEN_THREADS.md or Storylines & Fronts → relevant NPCs/Locations |
| Worldbuilding | `02 World Bible/World Bible.md` → relevant subdoc |
| Cross-campaign | `00 World Dashboard/World Dashboard.md` → Shared NPCs/Locations/Factions |
| Deep cross-reference | graphify (see Step 4) |

---

## Step 2: Dashboard-first orientation

Always start with the Campaign Dashboard. It indexes everything live.

```bash
# Children of the Ashen Sky
cat "$VAULT/01 Campaigns/Children of the Ashen Sky/Children of the Ashen Sky - Campaign Dashboard.md"

# Echos of Eternity
cat "$VAULT/01 Campaigns/Echos of Eternity/Echos of Eternity - Campaign Dashboard.md"

# World level
cat "$VAULT/00 World Dashboard/World Dashboard.md"
```

---

## Step 3: Quick searches

### Find the most recent session
```bash
ls "$VAULT/01 Campaigns/Children of the Ashen Sky/Sessions/" | sort | tail -3
ls "$VAULT/01 Campaigns/Echos of Eternity/Sessions/" | sort | tail -3
```

### Find all files referencing an NPC or term
```bash
grep -rl "Carthis Vane" "$VAULT" --include="*.md" | sort
grep -rl "[[House Vane]]" "$VAULT" --include="*.md" | sort
```

### Find files by frontmatter type
```bash
grep -rl "^type: npc" "$VAULT/01 Campaigns/Children of the Ashen Sky" --include="*.md"
grep -rl "^type: front" "$VAULT/01 Campaigns/Children of the Ashen Sky/Storylines & Fronts" --include="*.md"
```

### Find active threads and fronts
```bash
# Echos — structured open threads
cat "$VAULT/01 Campaigns/Echos of Eternity/OPEN_THREADS.md"

# CotAS — fronts directory
ls "$VAULT/01 Campaigns/Children of the Ashen Sky/Storylines & Fronts/"
```

### Find all sessions with a specific NPC
```bash
grep -rl "Vesh'thrael\|Listener" "$VAULT/01 Campaigns/Children of the Ashen Sky/Sessions/" --include="*.md"
```

### Trace wiki links from a file
```bash
grep -o '\[\[[^\]]*\]\]' "$VAULT/01 Campaigns/Children of the Ashen Sky/NPCs/Carthis Vane.md"
```

### Find stubs or needs-review files
```bash
grep -rl "^status: stub\|^status: needs-review" "$VAULT" --include="*.md" | sort
```

---

## Step 4: Graphify (deep cross-reference)

Use graphify when grep isn't enough: tracing an NPC's full relationship web, finding hidden connections across sessions, or running `worldbuilding-council` / `narrative-council` with `--graph`.

### Run graphify on the vault

```bash
graphify "$VAULT" --output "$VAULT/graphify-out"
```

Output lands in `$VAULT/graphify-out/` — this is where `graph-first` detection finds it (matches the `world/graphify-out/` detection path).

### When to use graphify vs grep

| Use grep when | Use graphify when |
|---|---|
| Looking up one NPC or location | Mapping a full relationship network |
| Checking one file for references | Finding all indirect connections to an entity |
| Quick session prep orientation | Running worldbuilding-council or narrative-council |
| Searching for a specific string | Discovering implicit cross-campaign connections |
| Single-hop lookup | Multi-hop traversal |

### After running graphify

Wren's existing skills (`worldbuilding-council`, `narrative-council`, `worldbuilding-deep-dive`, `character-arc`, `story-outline`) will automatically use the graph when invoked — graph-first detection finds `$VAULT/graphify-out/` and loads it. No extra steps needed.

To force graph ingestion in any of those skills: pass `--graph` in the invocation.

---

## Step 5: Following wiki links

Obsidian wiki links use `[[File Name]]` (no path, no extension). To find the target:

```bash
# Search the whole vault for a file by name
find "$VAULT" -name "House Vane.md" 2>/dev/null
find "$VAULT" -name "Lucien Aurelis.md" 2>/dev/null

# Or grep by display name when the file title might differ
find "$VAULT" -name "*.md" | xargs grep -l "^# House Vane" 2>/dev/null
```

---

## Rules

- Always read the Campaign Dashboard before diving into subdirectories.
- Don't read the entire vault — pull only what the task needs.
- For OPEN_THREADS.md, read the Active section first; Brewing/Dormant can wait.
- Graphify is a one-time cost per session when needed — run it once, then all skills use it.
- If graphify-out already exists in `$VAULT`, check its age before re-running: `ls -la "$VAULT/graphify-out/"`.
