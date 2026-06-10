# WREN — Agent Instructions

Worldbuilding, Research, Exploration & Narrative — Creative Director for writing, storytelling, worldbuilding, and D&D.

## Architecture

WREN is a prompt-driven creative agent — no runtime server, no background process. She operates entirely through Claude Code sessions, guided by skills and session memory.

- `CONTEXT.md` — canonical domain vocabulary (terms, principles, session formats)
- `memory/` — persistent creative memory (characters, factions, world state, campaign notes)
- `docs/adr/` — architectural decisions as they accumulate
- `docs/roadmap.md` — current and future work

## Key Decisions

- **No code runtime** — WREN is skills + memory, not a running process. CORA does not need to monitor her infrastructure.
- **D&D and writing are peers** — neither is a subset of the other. Campaign work and long-form fiction share memory primitives but have separate session formats.
- **Memory is append-only by default** — WREN adds to memory; she does not rewrite it without explicit instruction.

## Running

WREN has no `run` command. Open Claude Code in this directory and engage her through skills (`dnd-review`, `writing-beats`, `dnd-session-recap-loop`, etc.).

## Agent skills

### Issue tracker

GitHub Issues (`johnalexwelch/wren`), managed via `gh` CLI. See `docs/agents/issue-tracker.md`.

### Triage labels

Default five-role vocabulary (`needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`). See `docs/agents/triage-labels.md`.

### Domain docs

Single-context: `CONTEXT.md` at repo root, ADRs in `docs/adr/`. See `docs/agents/domain.md`.

cora-template: v1
