# Issue tracker: GitHub

Issues and PRDs for this repo live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies.
- **Read an issue**: `gh issue view <number> --comments`, filtering comments by `jq` and also fetching labels.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`

Repo: `johnalexwelch/wren`. Infer from `git remote -v` — `gh` does this automatically when run inside a clone.

## When a skill says "publish to the issue tracker"

Create a GitHub issue.

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.

## Wayfinding operations

Protocol for working wayfinder tickets. The map issue is the parent tracking issue; tickets are its sub-issues.

### Labels

- `wayfinder:map` — the map issue only.
- `wayfinder:research` / `wayfinder:prototype` / `wayfinder:grilling` / `wayfinder:task` — exactly one ticket-type label per ticket.
- `wayfinder:blocked` — on any ticket that is blocked.

### Blocking

- Declare a dependency with a `Blocked by: #N` line in the ticket body. Use native GitHub issue dependencies when available.
- When the blocker clears: remove the `Blocked by:` line and the `wayfinder:blocked` label.

### Frontier

A session may claim a ticket only from the frontier: open + unblocked + `no:assignee`.

### Claiming

1. Verify the ticket is still open and unassigned (concurrent sessions exist): `gh issue view <number> --json state,assignees`.
2. Assign yourself before starting work: `gh issue edit <number> --add-assignee @me`.

### Resolution

1. Post a resolution comment on the ticket.
2. Close the ticket.
3. Append one index line to the map issue's "Decisions so far" section.
4. For decision-type tickets: mirror the decision via `/decision-log`.

### Session discipline

- One ticket per session.
- Exit via `/handoff` into `docs/executions/handoffs/`.
