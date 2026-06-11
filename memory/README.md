# Memory — WREN

The Obsidian vault at `~/Documents/Home/Areas/DnD/GM/` is the source of truth for all campaign content. This directory holds lightweight cross-session state that doesn't live in the vault — orientation snapshots, session context, and notes on ongoing work.

---

## Tier 1 — In-Repo Active State

```
memory/
  README.md                    # this file
  campaigns/
    ashen-sky-state.md         # party, active threads, current session — CotAS
    echos-state.md             # party, active threads, current session — Echos
  world/
    cotu-quick-ref.md          # quick-reference world facts (not in vault)
```

### Campaign State Files

Each campaign state file is a lightweight snapshot Wren maintains so she can orient quickly without reading the full vault. Updated after each session.

**Schema:**

```markdown
---
campaign: <name>
updated: YYYY-MM-DD
current_session: <number>
---

# <Campaign> — Active State

## Party
| Character | Player | Status |
|---|---|---|

## Active Threads (top 3-5)
- **Thread name** — one-line status

## Current Focus
<what the party is doing right now / what next session is about>

## Recent Changes
<what shifted in the last session>
```

### World Quick Reference

Facts worth having on hand that aren't easily found in the vault — terminology Wren uses frequently, cross-campaign connections, world-level decisions in progress.

---

## Tier 2 — Session Memory Pointer

Claude Code auto-memory lives outside this repo. It is managed automatically by Claude Code across sessions and captures cross-session learnings, decisions, and agent directives.

Session memory path:

```
~/.claude/projects/<repo-path>/memory/MEMORY.md
```

Do not commit session memory — it is machine-managed and user-local.

---

## Rules

- Keep campaign state files short — they are orientation aids, not duplicates of the vault.
- Update after each session recap. Stale state is worse than no state.
- Vault is authoritative. If a fact lives in the vault, do not duplicate it here — reference the vault file instead.
- Prefer append-only notes over rewriting history.
