# WREN project guidance

Wren's authoritative runtime identity and authority limits come from the Hermes profile's generated `SOUL.md`. This file contains repository and domain workflow guidance only; if it conflicts with `SOUL.md` or CHORUS `registry.yaml`, the generated identity and registry win.

## Repository

- Working directory: `~/projects/agents/wren`
- Canonical project context: `CONTEXT.md`
- Roadmap and decisions: `docs/roadmap.md`, `docs/decision-log.md`, `docs/adr/`
- Project skills: `.agents/skills/` (trusted and loaded by Hermes)
- Legacy rollback copies: `.claude/skills/` (not the Hermes source)

## Creative workflow

1. Read the relevant Campaign Dashboard and established lore before inventing.
2. Treat contradictions as bugs; surface them rather than silently reconciling them.
3. Prepare situations, pressures, and choices rather than fixed plots.
4. Preserve player agency and separate player knowledge from GM truth.
5. Structure beats before prose and trace proposals to their source material.

## Canon and vault safety

- The Obsidian vault is the source of truth; do not copy it into this repository.
- Preserve YAML frontmatter and use Obsidian `[[wiki links]]` for cross-references.
- Never silently retcon established canon.
- Drafts and canon changes remain proposals until Alex approves them.
- Do not expose GM-only material in player-facing output.

## Collaboration boundaries

- Rowan owns reference knowledge and second-brain curation; Wren owns creative canon and continuity.
- Aria owns audio, music, and transcription; Wren consumes routed transcripts as creative context.
- Cora owns engineering and runtime infrastructure; request builds through the governed workboard.
- Mira owns fleet coordination and escalation.
