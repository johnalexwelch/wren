# Handoff — LiteLLM + WireGuard on Mac mini for pi

Exit: manual
Target: cora
Generated: 2026-06-30

## Where we are

Alex wants to replace OpenRouter with a self-hosted LiteLLM proxy running on his Mac mini. Pi connects to it via the `pi-provider-litellm` extension. Since Alex travels and won't always be on the home network, we need remote access. Tailscale conflicts with his work setup, Cloudflare Tunnel felt too public. Decision: WireGuard for secure private remote access — only one UDP port exposed, no public URL, all traffic encrypted.

Nothing has been installed yet. This is greenfield.

## What was done this session

- Evaluated OpenRouter → LiteLLM migration path
- Found `pi-provider-litellm` official extension (auto-discovers models, `/login litellm`, `/litellm-refresh`)
- Ruled out Tailscale (conflicts with work Tailscale tailnet)
- Ruled out bare Cloudflare Tunnel (public URL concern)
- Decided on: **WireGuard on Mac mini** + LiteLLM as launchd service + `pi-provider-litellm` extension on MacBook

## What is NOT done

- WireGuard not installed or configured on Mac mini or MacBook
- LiteLLM not installed on Mac mini
- `config.yaml` for LiteLLM not written (providers/models not confirmed)
- launchd plist for LiteLLM not created
- `pi-provider-litellm` extension not installed on MacBook
- Router UDP port 51820 not forwarded to Mac mini

## Blockers requiring human input

- **Which LLM providers + API keys** should LiteLLM route? (e.g. Anthropic, OpenAI, others) — needed before writing `config.yaml`
- **Mac mini hostname or local IP** on home network — needed for WireGuard peer config
- **Router access** — Alex needs to forward UDP 51820 → Mac mini himself (Cora can't do this)

## Key decisions made

- Self-hosted LiteLLM on Mac mini, not OpenRouter
- WireGuard for remote access (not Tailscale, not Cloudflare Tunnel)
- `pi-provider-litellm` npm extension (not manual `models.json` approach)
- LiteLLM runs as persistent launchd service (starts on boot)

## Next steps

1. **Ask Alex** which providers/API keys go in `config.yaml` and confirm Mac mini local IP
2. Install WireGuard on Mac mini + generate server keypair + write `wg0.conf`
3. Install WireGuard on MacBook + generate client keypair + write peer config
4. Forward UDP 51820 on router → Mac mini (human step, flag for Alex)
5. Install LiteLLM on Mac mini via `uv tool install 'litellm[proxy]'`
6. Write `~/litellm/config.yaml` with confirmed providers
7. Write and load `~/Library/LaunchAgents/com.litellm.proxy.plist`
8. Install `pi-provider-litellm` on MacBook: `pi install npm:pi-provider-litellm`
9. `/login litellm` in pi with WireGuard IP of Mac mini + master key
10. Test from home network, then test via WireGuard from outside

## Ready-to-use prompt

```
You are Cora, execution agent. Set up a self-hosted LiteLLM proxy on Alex's Mac mini with WireGuard for secure remote access, then connect pi on his MacBook to it via the pi-provider-litellm extension.

Architecture decided:
- Mac mini: WireGuard server + LiteLLM proxy (launchd service, port 4000)
- MacBook: WireGuard client + pi with pi-provider-litellm extension
- Remote access: WireGuard only (one UDP 51820 port on router, no public URL)

Before starting, ask Alex:
1. Which LLM providers + API keys for LiteLLM config.yaml (e.g. Anthropic, OpenAI)?
2. Mac mini local IP or hostname on home network
3. Confirm he can forward UDP 51820 on his router to Mac mini

Steps:
1. WireGuard on Mac mini (brew install wireguard-tools, generate keypair, wg0.conf)
2. WireGuard on MacBook (generate client keypair, add as peer on server)
3. LiteLLM on Mac mini (uv tool install 'litellm[proxy]', config.yaml, launchd plist)
4. pi-provider-litellm on MacBook (pi install npm:pi-provider-litellm)
5. /login litellm in pi pointing at WireGuard IP:4000
6. Test end-to-end

Router port forward (UDP 51820 → Mac mini) is a human step — flag it clearly for Alex.

Read this handoff for full context: docs/executions/handoffs/2026-06-30-litellm-wireguard-setup.md
```

## Files to read first

- `docs/executions/handoffs/2026-06-30-litellm-wireguard-setup.md` (this file)
