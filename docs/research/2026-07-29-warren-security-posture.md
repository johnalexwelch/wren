# Warren security posture — locking down a local agent server that writes the vault

Resolves wayfinder ticket [wren#15](https://github.com/johnalexwelch/wren/issues/15) (map: [wren#3](https://github.com/johnalexwelch/wren/issues/3)).
Date: 2026-07-29. Builds on [Q7](../decision-log.md#wren-workbench-chorus-fit) (F13 audit, canon-approval), [Q9](../decision-log.md#warren-obsidian-optional) (staleness-checked writes), and [Q10](../decision-log.md#warren-backend-agent-sdk) (Agent SDK backend, `PreToolUse` + `canUseTool` choke-point).

## Threat model in one paragraph

Warren is a single-user local web app, but "local" is not "safe": the server can **write the vault** (canon corruption), **spend Anthropic API tokens** (money), and **run an agent whose primary input — the vault and session transcripts — is untrusted**. Every note Wren reads is a potential prompt injection (a pasted ChatGPT brainstorm, a garbled auto-transcript, lore imported from anywhere). The attacker classes that matter: (a) a malicious website open in the same browser reaching `localhost` (CSWSH against the WebSocket, DNS rebinding against HTTP); (b) injected instructions in vault/transcript content steering Wren's tool calls; (c) accidental self-harm (an over-permissive agent clobbering canon). There is no multi-user or remote-attacker story — Alex's Mac, Alex's vault.

## 1. Network exposure — localhost bind, per-launch token, origin + Host validation

- **Bind `127.0.0.1` only**, hardcoded — not a config option that can drift to `0.0.0.0`. Remote access, if ever wanted, is a Tailscale/SSH-tunnel problem, not a Warren feature.
- **Per-launch bearer token**: the server generates a random token at startup, prints/opens the UI URL carrying it once (`#token=` fragment, never query string, so it stays out of logs and Referer), and requires it on every HTTP request and on the WebSocket handshake. This is the whole defense against "any local process or rebound page can drive the agent." No accounts, no passwords, no OS-level auth — single-user machine, and the token already gates the two dangerous capabilities (vault writes, token spend).
- **WebSocket `Origin` allowlist**: the upgrade handler rejects any origin other than Warren's own (`http://127.0.0.1:<port>`). Browsers do not apply same-origin policy to WebSocket connects, so without this check any tab Alex has open could hold a live agent channel (CSWSH). Belt and suspenders with the token — the token is the real gate; the origin check makes the failure loud and cheap.
- **`Host` header validation** on all HTTP routes (must be `127.0.0.1:<port>` / `localhost:<port>`) to break DNS rebinding, which defeats origin assumptions on plain HTTP but cannot forge the Host header.
- CORS: no permissive headers at all — same-origin only. The UI is served by the same process; nothing else is a legitimate client.

## 2. Agent write scope — default `permissionMode`, deny-by-default writes, allowlisted read-only Bash

`permissionMode` for Warren sessions is **`default`** — never `acceptEdits` or `bypassPermissions`. The `PreToolUse` policy hook is the authority (it runs before permission-mode evaluation, so it holds even if a mode is misconfigured), with `canUseTool` surfacing decisions in the UI. The surface:

| Surface | Policy |
|---|---|
| Reads (`Read`/`Glob`/`Grep`) | Allow within vault + wren checkout + Warren scratch dir; deny elsewhere (no `~/.ssh`, no `~/.chorus`, no dotfiles) |
| Vault writes (`Write`/`Edit`) | Allow only via the Q7 canon-approval card + Q9 staleness check — every write shows a diff and waits for Alex |
| wren repo writes | **Approval-gated like vault writes**, not free: `CLAUDE.md` and `.claude/skills/` are Wren's own instructions — unattended writes there are a persistence vector for injected content |
| Writes anywhere else | Deny outright (no approval path) — the hook rejects, the UI shows the denial |
| Bash | Allowlist of read-only commands (`rg`, `grep`, `ls`, `cat`, `git log/diff/show`) with arguments path-checked against the read scope; everything else denied. Skills lean on `rg`/`git` for search — the allowlist keeps them working without handing over a shell |
| Network (`WebFetch`/`WebSearch`) | `WebSearch` allowed (queries logged to audit); `WebFetch` allowed against a small persisted domain allowlist, approval-gated for new domains — Wren's research role is real, but an unrestricted fetch tool is the classic injection exfil channel (secret vault content smuggled into a URL) |
| MCP index tool | Allow — read-only over the derived index |

Session budget: cap `maxTurns` per session and log per-session token spend to the audit stream; runaway loops are a cost bug before they are a security bug.

## 3. Secrets — env at server startup, never near the browser

- The Anthropic key (and any embedding-provider key) lives in **`~/.config/warren/env`, mode `0600`, loaded into the server process at startup** — gitignored territory by construction, one obvious place to rotate. macOS Keychain (`security find-generic-password` at boot) is a fine hardening step later; it changes theft-at-rest, not the architecture, so it is not v1-blocking.
- Keys exist **only in the server process**. They are never serialized into WebSocket frames, never embedded in the client bundle, never echoed in error responses. The browser authenticates with the per-launch token only.
- Logging: redact `Authorization`/`x-api-key`-shaped values in any request/response logging; no full-payload logging of Anthropic API traffic. Startup fails fast if the key is missing rather than limping into per-request errors.

## 4. Audit — F13 events with paths and hashes, never content

Warren emits JSONL events to `~/.chorus/audit` (per Q7). Events: **session start/end** (session ID, cwd, model, turn/token totals), **every tool call** (tool name, target path or command name, policy decision `allow`/`deny`/`approval-required`), **every approval outcome** (granted/rejected, target path, content *hash* + byte size of the proposed write), **every policy denial** (rule that fired), and **WebFetch/WebSearch targets** (domain + query). The invariant: **no vault content, no diffs, no chat text** — the vault is GM-secret campaign data and the audit dir is a fleet-shared surface; paths, hashes, sizes, and decisions give Mira full observability of *what Warren did* without leaking *what the campaign contains*. The Q7 Matrix session summary stays the human-readable trace; audit stays the machine-readable one.

## 5. Prompt-injection blast radius — what a compromised Wren can and cannot do

Assume a vault note successfully steers Wren. What it can attempt, and what contains it:

| Attack | Containment |
|---|---|
| Corrupt canon (malicious vault write) | Canon-approval card shows the diff; staleness check blocks races; git history makes any approved mistake reversible |
| Persist itself (edit `CLAUDE.md` / skills) | wren-repo writes are approval-gated — no unattended self-modification |
| Exfiltrate GM secrets via URL | `WebFetch` domain allowlist + approval for new domains; audit logs every fetched domain |
| Escape to the filesystem | Read scope denies everything outside vault/wren/scratch; non-vault writes have no approval path at all |
| Run arbitrary commands | Bash allowlist is read-only and path-checked |
| Burn API budget | `maxTurns` cap + per-session spend in audit |
| Reach the server from a hostile web page | Token + origin + Host checks (§1) — injection in the *browser* channel is closed off separately from injection in the *vault* channel |

The residual risk is honest: **Alex approving a malicious diff**. That is irreducible in a human-in-the-loop design — the mitigations are that the approval card renders the actual diff (not a summary Wren wrote), and everything is one `git revert` away. The posture's shape: the vault is treated as untrusted *input* everywhere, and the approval gate treats Wren as untrusted *output* — nothing Wren produces reaches disk, the network, or another process without either a standing allowlist rule or Alex's click.

## Recommendation

Ship all of §1–§4 in Warren v1 — none of it is deferrable, because the dangerous capabilities (vault writes, API spend) exist from the first spike. The one deliberately thin spot is secrets-at-rest (env file now, Keychain later). Revisit this posture when Warren gains any second network surface (Matrix posting from the server, remote access) — each new egress channel re-opens the exfiltration row of the blast-radius table.
