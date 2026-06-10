# Memory — WREN

This directory holds the in-repo active memory state for wren.

## Tier 1 — In-Repo Active State

Active working memory that changes frequently and must be version-controlled.

```
memory/
  README.md          # this file — schema and layout guide
  # Add subdirectories here as the agent's memory needs grow:
  # state/           # current task / session state
  # context/         # domain context snapshots
```

**Schema stub**: Add agent-specific subdirectories and files below as needed.
Keep each file focused on one concern. Prefer append-only logs over mutable state.

## Tier 2 — Session Memory Pointer

Claude Code auto-memory lives outside this repo. It is managed automatically by Claude Code across sessions and captures cross-session learnings, decisions, and agent directives.

Session memory path:

```
~/.claude/projects/<repo-path>/memory/MEMORY.md
```

Do not commit session memory — it is machine-managed and user-local.

## Layout Notes

- In-repo memory is for state that agents and humans both need to read/write.
- Session memory is for Claude Code's own cross-session continuity.
- Keep this README updated as the memory schema evolves.
