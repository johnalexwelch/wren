---
name: vault-write
model: sonnet
description: Write or update files in the Chronicles of the Uncrowned King Obsidian vault. Handles session notes, NPC files, prep docs, lore entries, open threads updates, and front/storyline docs. Enforces correct frontmatter, wiki links, directory placement, and naming conventions. Use whenever Wren needs to save content back to the vault.
---

# Vault Write

Write or update files in the CotU vault at `~/Documents/Home/Areas/DnD/GM/Chronicles of the Uncrowned King/` — hereafter `$VAULT`. Always preserve Obsidian conventions: YAML frontmatter, `[[wiki links]]`, and correct directory placement.

## Contract

Consumes: content to write, content type, campaign context
Produces: file(s) written to correct vault location
Requires: filesystem access to `$VAULT`
Side effects: creates or updates vault files
Human gates: confirm before overwriting any existing file

---

## Step 1: Check before writing

Never overwrite without asking.

```bash
[ -f "$TARGET" ] && echo "EXISTS — confirm overwrite or append?" || echo "NEW — safe to create"
```

For appending to `OPEN_THREADS.md` or a session's In-Session Notes, use `>>`.

---

## Step 2: Directory placement

| Content type | Campaign | Directory |
|---|---|---|
| Session note | CotAS | `01 Campaigns/Children of the Ashen Sky/Sessions/` |
| Session note | Echos | `01 Campaigns/Echos of Eternity/Sessions/` |
| Session prep doc | CotAS | `01 Campaigns/Children of the Ashen Sky/Prep/` |
| Session prep doc | Echos | `01 Campaigns/Echos of Eternity/Prep/` |
| NPC | CotAS | `01 Campaigns/Children of the Ashen Sky/NPCs/` |
| NPC | Echos | `01 Campaigns/Echos of Eternity/NPCs/` |
| NPC (shared) | Both | `04 Shared NPCs/` |
| Location | CotAS | `01 Campaigns/Children of the Ashen Sky/Locations/` |
| Location (shared) | Both | `03 Shared Locations/` |
| Front / Storyline | CotAS | `01 Campaigns/Children of the Ashen Sky/Storylines & Fronts/` |
| Encounter | CotAS | `01 Campaigns/Children of the Ashen Sky/Encounters/` |
| Handout (GM) | CotAS | `01 Campaigns/Children of the Ashen Sky/Handouts/` |
| Handout (player) | CotAS | `01 Campaigns/Children of the Ashen Sky/Handouts/Player Safe/` |
| Lore / World Bible | Shared | `02 World Bible/` |
| Faction | CotAS | `01 Campaigns/Children of the Ashen Sky/Factions & Organizations/` |
| Faction (shared) | Both | `05 Shared Factions & Organizations/` |
| Artifact | Shared | `07 Artifacts & Items/` |
| Timeline entry | Shared | `06 Timeline & Eras/` |

---

## Step 3: Naming conventions

Match existing files in the same directory. Common patterns:

| Type | Convention | Example |
|---|---|---|
| Session note | `Session NNN - Title.md` | `Session 005 - The Second Descent.md` |
| Prep doc | `Session NNN - Topic.md` | `Session 005 - Lazy DM Checklist.md` |
| NPC | `First Last.md` or `Name, the Title.md` | `Carthis Vane.md` |
| Location | Proper noun | `The Candlepost Warehouse.md` |
| Front | Descriptive name | `The Hollow Order Advance.md` |

---

## Step 4: Frontmatter templates

### Session note

```yaml
---
created: YYYY-MM-DD
type: session
world: Chronicles of the Uncrowned King
campaigns:
  - <campaign name>
era: <Ashen Sky Era | Echos Era>
session_number: <N>
session_date:
status: <planned | draft | ready | active | played>
visibility: gm
tags: [dnd, session, <campaign-slug>]
---
```

### NPC

```yaml
---
created: YYYY-MM-DD
type: npc
world: Chronicles of the Uncrowned King
campaigns:
  - <campaign name>
eras:
  - <era>
visibility: gm
status: <active | deceased | unknown | missing>
race: <race or TBD>
gender: <male | female | nonbinary | unknown>
class: <class or role>
location: "[[Location Name]]"
organization: "[[Organization Name]]"
disposition: <ally | enemy | neutral | unknown>
tags: [dnd, npc, <campaign-slug>, <relevant-tags>]
---
```

### Front / Storyline

```yaml
---
created: YYYY-MM-DD
type: front
world: Chronicles of the Uncrowned King
campaigns:
  - <campaign name>
era: <era>
visibility: gm
status: <active | brewing | resolved | archived>
threat: <one-line threat statement>
next_move: <what happens next if unchecked>
tags: [dnd, front, <campaign-slug>]
---
```

### Location

```yaml
---
created: YYYY-MM-DD
type: location
world: Chronicles of the Uncrowned King
campaigns:
  - <campaign name>
era: <era>
visibility: <gm | player>
status: <active | destroyed | unknown>
location_type: <city | district | building | region | dungeon | etc.>
parent_location: "[[Parent Location]]"
tags: [dnd, location, <campaign-slug>]
---
```

### Lore / World Bible entry

```yaml
---
created: YYYY-MM-DD
type: lore
world: Chronicles of the Uncrowned King
visibility: gm
status: <canon | candidate | draft>
tags: [dnd, lore, uncrowned-king]
---
```

---

## Step 5: Wiki link rules

- All cross-references use `[[File Name]]` — no path, no extension
- Match the exact filename (case-sensitive in Obsidian)
- When referencing a file not yet created, still use `[[Name]]` — Obsidian tracks unresolved links
- Pronunciation guides go in the heading: `# Carthis Vane *(CAR-this VAYN)*`

---

## Step 6: Write the file

```bash
mkdir -p "$TARGET_DIR" && cat > "$TARGET_FILE" << 'VAULT_EOF'
---
<frontmatter>
---

# Title

Content here...
VAULT_EOF
```

Use `<< 'VAULT_EOF'` (quoted) to prevent shell variable expansion in content.

For appending to an existing file:
```bash
cat >> "$TARGET_FILE" << 'VAULT_EOF'

## New Section

Appended content...
VAULT_EOF
```

---

## Special cases

### Updating OPEN_THREADS.md (Echos)

Read the file first to understand the current thread structure. Match the existing format exactly:
- Status · What the party knows · What the GM knows · Recommended action · Risk if ignored · See (file reference)
- Move resolved threads to the appropriate section (Brewing / Dormant / Ready for Payoff / Retired)
- Never delete retired threads — move them to the Retired section with a resolution note

### Adding to an NPC's Open Questions

Append a new `- [ ]` checkbox under the existing Open Questions section. Do not reorder or remove existing questions unless they are resolved — mark resolved questions `- [x]`.

### Session recap — In-Session Notes

Append to the session note's **In-Session Notes** section after the session plays. Do not overwrite the prep content — add a dated separator:

```markdown
## Post-Session Updates — YYYY-MM-DD

<actual play notes, confirmed canon, divergences from prep>
```

---

## Rules

- Always `mkdir -p` before writing.
- Always check for existing file before writing.
- Never retcon existing content — append or add sections.
- Preserve every `[[wiki link]]` exactly — typos break Obsidian's graph.
- Set `visibility: gm` by default; only set `visibility: player` for handouts explicitly marked safe to share.
- After writing, confirm the file exists: `ls -la "$TARGET_FILE"`.
