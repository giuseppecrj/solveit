# Solveit

A Claude Code plugin that enforces the **Solveit method** for coding sessions: small, verified checkpoints; narrow diffs; human-in-the-loop control. A skill plus three hooks that block (not just warn) when the discipline slips.

Adapted from [Jeremy Howard's Solveit method](https://solveit.fast.ai/) (fast.ai / Answer.AI), itself an adaptation of George Pólya's *How to Solve It* applied to working with LLMs.

## What's in the plugin

- **`/solveit:init`** — a skill that bootstraps a session, scaffolds `.solveit/session.md`, and walks the five-phase loop (Understand → Plan → Execute → Verify → Reflect).
- **Three enforcement hooks** active only inside a session:
  - `session-required.py` (PreToolUse) — blocks edits unless `session.md` is filled out with a current checkpoint.
  - `diff-size.py` (PreToolUse) — blocks edits over 50 lines per checkpoint.
  - `stop-verify.py` (Stop) — blocks end-of-turn until the latest checkpoint records a verification.

The skill has `disable-model-invocation: true`, so Claude can never auto-invoke it. Solveit mode is strictly opt-in.

## Install

From GitHub:

```
/plugin marketplace add https://github.com/giuseppecrj/solveit
/plugin install solveit@solveit
```

Local development:

```
/plugin marketplace add /path/to/this/repo
/plugin install solveit@solveit
```

## Usage

### Start a session

```
/solveit:init
```

This creates two files in the working directory:

- `.solveit/active` — sentinel that arms the hooks. Their absence is a no-op.
- `.solveit/session.md` — the audit trail Claude reads and writes to throughout the session.

Claude enters Phase 1 (Understand). **No code is written yet.**

### The loop

For every checkpoint, all five phases run:

1. **Understand** — restate the problem, list constraints and unknowns.
2. **Plan** — numbered plan; pick the *single smallest* next step.
3. **Execute** — make only that change. Hooks cap edits at 50 lines.
4. **Verify** — run a targeted check; record the command and result in `session.md`.
5. **Reflect** — one or two sentences. Propose the next smallest step. Stop.

### Exit

When done, delete the sentinel:

```
rm .solveit/active
```

`.solveit/session.md` remains as the audit trail.

## How enforcement works

Hooks no-op unless `.solveit/active` exists in the current working directory, so they only fire inside an explicit session. When active:

| Hook | When | What it blocks |
|---|---|---|
| `session-required.py` | before any `Edit`/`Write`/`MultiEdit` | edit attempts when `session.md` is missing, empty, or has no `## Current checkpoint` filled in |
| `diff-size.py` | before any `Edit`/`Write`/`MultiEdit` | edits over `SOLVEIT_MAX_LINES` (default 50) lines |
| `stop-verify.py` | before end-of-turn | ending a turn when the most recent `### Checkpoint` block in `session.md` is missing `- Verification:` or `- Result:` lines |

If a hook blocks, the right move per the skill is to split the checkpoint or fix the underlying cause — not to bypass.

## Configuration

| Env var | Default | Purpose |
|---|---|---|
| `SOLVEIT_MAX_LINES` | `50` | Per-edit line cap. Bumping this is intentionally discouraged; the skill instructs Claude to split rather than raise it. |

## File layout

```
.
├── .claude-plugin/
│   ├── plugin.json
│   └── marketplace.json
├── skills/
│   └── init/
│       └── SKILL.md
└── hooks/
    ├── hooks.json
    ├── session-required.py
    ├── diff-size.py
    └── stop-verify.py
```

## Uninstall

```
/plugin uninstall solveit@solveit
/plugin marketplace remove solveit
```
