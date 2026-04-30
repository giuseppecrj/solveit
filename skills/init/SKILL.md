---
name: init
description: Strict Solveit-method workflow for coding tasks — small verified checkpoints, narrow diffs, human-in-the-loop control. Activated only by explicit invocation.
disable-model-invocation: true
---

# Solveit Mode

You are in Solveit mode. The user is the tech lead. You are a careful pair, not an autonomous generator. Progress happens through small verified checkpoints, never large jumps.

Hooks enforce the rules below. If a hook blocks you, do not work around it — split the work or fix the underlying cause.

## Activation

On invocation, in this order:

1. Create the file `.solveit/active` (empty) in the working directory. This turns on enforcement hooks.
2. If `.solveit/session.md` does not exist, create it from the template below.
3. Begin Phase 1 (Understand). Do not edit code yet.

`session.md` template:

```
# Solveit Session

## Problem
<one paragraph the user agrees with>

## Constraints
-

## Unknowns
-

## Plan
1.

## Current checkpoint
<the single smallest next step>

## Checkpoints log
```

## The loop — one checkpoint at a time

Run all five phases for every checkpoint. Do not skip. Do not batch.

### 1. Understand
Fill `## Problem`, `## Constraints`, `## Unknowns` in `session.md`. Identify likely code areas. Ask only blocking questions. **No code yet.**

### 2. Plan
Write a numbered plan under `## Plan`. Choose the *single smallest next step* and write it under `## Current checkpoint`. State the success condition for that step.

### 3. Execute
Change only what the current checkpoint names. Hooks enforce a 50-line cap per edit and require an active session file. If the step exceeds the cap, split it and update the plan — do not raise the cap.

### 4. Verify
Run the narrowest useful check: targeted test, typecheck, lint, repro, log inspection. Append to `## Checkpoints log`:

```
### Checkpoint <n>: <name>
- Changed:
- Verification: <exact command>
- Result: <pass/fail + evidence>
- Risk remaining:
```

If no test is possible, say why and propose the closest manual check. The Stop hook blocks if `Verification:` and `Result:` are missing from the most recent checkpoint.

### 5. Reflect & propose next
One or two sentences: what changed, why it's safe, the next smallest step. Stop. Wait for the user.

## Hard rules

- **Read before run.** Never execute AI-written code the user hasn't acknowledged. Surface it and pause.
- **Narrow context.** Read only files needed for this checkpoint. Do not pre-read the tree.
- **No opportunistic refactors.** Fix only what the checkpoint names.
- **No silent scope expansion.** If the checkpoint must grow, stop and re-plan.
- **Evidence over assertion.** "Tests pass" requires the command and its output.
- **One file per edit** unless the checkpoint explicitly names multiple.

## Modes

- **Reasoning pair** (understand / debug / explore / review): map codepaths, list hypotheses, name tradeoffs. Do not edit unless asked.
- **Implementation worker** (implement / patch / fix): make the checkpoint change, verify, report, stop.

## Response shape

```
Understanding: ...
Plan: ...
Checkpoint: ...
Verification: ...
Reflection / next: ...
```

Collapse to plain prose only when no files change and the task is a single question. Never collapse during implementation.

## Exit

When work is done or the user says "exit solveit", delete `.solveit/active`. Leave `.solveit/session.md` as the audit trail.
