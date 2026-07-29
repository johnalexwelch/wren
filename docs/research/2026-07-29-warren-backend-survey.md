# Warren backend survey — serving Wren (persona + skills + vault) to a browser

Resolves wayfinder ticket [wren#7](https://github.com/johnalexwelch/wren/issues/7) (map: [wren#3](https://github.com/johnalexwelch/wren/issues/3)).
Date: 2026-07-29. Method: parallel doc-grounded research (Agent SDK/Claude Code docs; OSS landscape survey) — `/deep-research` was unavailable on this machine (no OpenAI key), so the survey ran via Claude research agents against current documentation and repos.

## Question

What should Warren's backend be — the server-side loop that fronts Wren (persona `CLAUDE.md`/`CONTEXT.md`, `.claude/skills/`, auto-memory, read/write vault access) with streaming chat in a browser — and is there an existing OSS app worth adopting or forking instead of building?

## Constraints carried in

- From [Q9 (Obsidian-optional)](../decision-log.md#warren-obsidian-optional): vault file-watcher for external edits, derived rebuildable index (frontmatter, wiki-link graph, embeddings; files canonical), staleness-checked writes.
- From [Q7 (Chorus fit)](../decision-log.md#wren-workbench-chorus-fit): canon-affecting vault writes need a human approval step in the UI.
- From [Q8 (Warren/Forgejo)](../decision-log.md#warren-code-home-and-name): Warren is a new repo on local Forgejo (`awelch/warren`); CI is Forgejo Actions, not GitHub Actions.
- Ground truth: wren carries **34 skills** in `.claude/skills/`; auto-memory lives under `~/.claude/projects/<encoded-cwd>/memory/`; the vault is **~820 markdown files** — small enough that any watcher/index approach works.

## Option 1 — Claude Agent SDK as a server-side loop (TypeScript or Python)

The Agent SDK is the same engine as Claude Code (it wraps the `claude` runtime), exposed as a library with structured message objects. Everything Warren needs is a documented option:

| Requirement | SDK answer |
|---|---|
| Skill loading | `settingSources: ["user", "project"]` loads `.claude/skills/`, CLAUDE.md, and settings-file hooks from the configured `cwd` — point `cwd` at the wren checkout and the 34 skills load as-is ([docs](https://code.claude.com/docs/en/agent-sdk/skills.md)) |
| Session persistence | `resume: sessionId` / `forkSession`; sessions stored as JSONL under `~/.claude/projects/<encoded-cwd>/` — store session IDs app-side and resume across restarts ([docs](https://code.claude.com/docs/en/agent-sdk/sessions.md)) |
| Streaming | `includePartialMessages: true` yields raw `StreamEvent` deltas (text + incremental tool calls) — relay over WebSocket/SSE ([docs](https://code.claude.com/docs/en/agent-sdk/streaming-output.md)) |
| Vault-write approval | Two layered gates: a `PreToolUse` hook matching `Write\|Edit` on vault paths (runs *before* permission-mode evaluation, so it holds even under permissive modes) plus the `canUseTool` runtime callback to surface the approval in the UI ([permissions](https://code.claude.com/docs/en/agent-sdk/permissions.md), [hooks](https://code.claude.com/docs/en/agent-sdk/hooks.md)) |
| Multi-conversation | Concurrent `query()` calls / `ClaudeSDKClient` instances are isolated; sessions keyed by cwd + id. Same-cwd concurrent writes aren't coordinated — the approval gate + staleness check are the serializer for vault writes |
| Maintenance | First-party Anthropic library, active docs; Warren owns only its own server shell |

**TS vs Python:** TypeScript has the richer hook set (`SessionStart`/`SessionEnd` and other lifecycle hooks are TS-only), the official demos and best OSS plumbing are TS, and one language covers server + React front-end. Python's advantage (embedding-friendly ML ecosystem) doesn't outweigh that; embeddings for the index can call any API from TS.

**Caveats found:** auto-memory loading in SDK sessions is implicit (it rides the same `settingSources` mechanism as CLAUDE.md but isn't explicitly documented) — verify in the first spike; both SDKs are async-only; custom system prompts >~8KB should be passed by file reference in Python.

## Option 2 — Wrapping Claude Code headless (`claude -p`) as a subprocess

Same engine, worse interface for an app: `--output-format stream-json` gives JSON lines but **no `canUseTool` callback** — runtime approval would have to be faked with `--permission-prompt-tool` MCP plumbing or coarse `--allowedTools` lists. Skills, auto-memory, hooks, and `--resume` all work (it's what the SDK does internally), so this remains the quick-hack fallback, but it's strictly dominated by Option 1 for Warren's approval-gate requirement.

## Option 3 — Adopt or fork an existing OSS web UI

Surveyed July 2026; full candidate table in the research transcript. The serious ones:

| Project | Health | Verdict |
|---|---|---|
| [siteboon/claudecodeui](https://github.com/siteboon/claudecodeui) (~13k★, AGPL) | Active | Most complete product (chat, sessions, file tree, git, mobile) but wraps the CLI, has grown multi-CLI bloat (Codex/Cursor abstraction), permission story is per-tool toggles not per-write approval, and AGPL constrains future distribution. Fork = excavating custom panes into someone else's architecture. |
| [sugyan/claude-code-webui](https://github.com/sugyan/claude-code-webui) (MIT) | **Archived May 2026** | Best per-request permission-dialog UX in the space — use as design reference only. |
| [anthropics/claude-agent-sdk-demos](https://github.com/anthropics/claude-agent-sdk-demos) (MIT, official) | Active | Canonical Agent SDK patterns: React + Express + WebSocket streaming chat, session persistence, permission-callback gating. A skeleton, not a product — which fits: Warren's editor + graph panes get built around it, not into it. |
| [JimLiu/claude-agent-kit](https://github.com/JimLiu/claude-agent-kit) (~500★, MIT) | Young, single maintainer | Small TS monorepo on the Agent SDK: SessionManager for concurrent sessions, typed WebSocket bridge, resume from session JSONL. Exactly the plumbing layer Warren needs — treat as vendor/fork material, not a trusted dependency. |
| [getAsterisk/opcode](https://github.com/getAsterisk/opcode), [slopus/happy](https://github.com/slopus/happy) (both ~22k★) | Active | Wrong-shaped: Tauri desktop app / mobile-relay remote control respectively. UX reference only (opcode's checkpoints, happy's remote approvals). |

No candidate ships the campaign-specific surfaces (vault editor honoring frontmatter/wiki-links, semantic graph pane, canon-approval flow) — those are Warren's whole point, and in every fork they'd be fought into a general-purpose codebase. Cross-cutting: all candidates' CI is GitHub Actions but none depend on GitHub at runtime; Forgejo Actions is a non-issue everywhere.

## The Q9-derived services are architecture-independent — but favor one runtime

The vault watcher (chokidar-class), derived index (SQLite + frontmatter/link-graph tables, embeddings column), and staleness-checked writes are **app services beside the agent loop**, not agent features. Any option needs them built. Two integration notes:

- The staleness check belongs in the same choke-point as the approval gate: the `PreToolUse` hook can reject a `Write`/`Edit` whose target changed on disk since the session last read it — one policy gate, two rules.
- The index can double as context plumbing: expose it to Wren as an MCP server (or in-process SDK tool) so chat, editor, and graph all read the same index.

A single Node/TS process (or small process pair) covers agent loop + watcher + index + WebSocket relay; a Python loop would split the runtime or duplicate the stack.

## Recommendation

**Build Warren's backend thin on the Claude Agent SDK (TypeScript), pointed at the wren checkout via `cwd` + `settingSources` — don't fork a product.** Seed the server shell from `anthropics/claude-agent-sdk-demos` patterns and vendor what's useful from `claude-agent-kit` (SessionManager, typed WS events). Gate vault writes with a `PreToolUse` policy hook (path scope + staleness check) surfaced through `canUseTool` as the UI approval step. Keep `sugyan/claude-code-webui`'s archived permission-dialog UX and `opcode`'s checkpoint timeline as design references. First spike should verify the one undocumented assumption: auto-memory loading under SDK `settingSources`.

Why not the alternatives, in one line each: CLI-subprocess wrapping loses the runtime approval callback that Q7 requires; forking claudecodeui buys a week of UI at the cost of AGPL, bloat-stripping, and building the approval flow inside foreign architecture anyway; Python SDK splits the runtime and lacks the TS-only lifecycle hooks.
