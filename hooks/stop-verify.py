#!/usr/bin/env python3
"""Solveit Stop hook: block end-of-turn until the latest checkpoint is verified."""
import json
import os
import re
import sys

data = json.load(sys.stdin)
cwd = data.get("cwd", os.getcwd())

if not os.path.exists(os.path.join(cwd, ".solveit", "active")):
    sys.exit(0)

# Avoid infinite loops if Claude is already responding to a prior block.
if data.get("stop_hook_active"):
    sys.exit(0)

session = os.path.join(cwd, ".solveit", "session.md")
if not os.path.exists(session):
    sys.exit(0)

with open(session) as f:
    text = f.read()

matches = list(re.finditer(r"^### Checkpoint.*$", text, re.MULTILINE))
if not matches:
    # No checkpoints logged yet — pure planning turn, allow stop.
    sys.exit(0)

last_block = text[matches[-1].start():]

missing = []
if "- Verification:" not in last_block:
    missing.append("- Verification:")
if "- Result:" not in last_block:
    missing.append("- Result:")

if missing:
    out = {
        "decision": "block",
        "reason": (
            "Solveit: the most recent checkpoint in .solveit/session.md is missing "
            f"{', '.join(missing)}. Run a verification (test/typecheck/repro) and "
            "append both lines under the checkpoint before ending the turn. "
            "If no verification is possible, write 'Verification: none — <reason>' "
            "and 'Result: n/a'."
        ),
    }
    print(json.dumps(out))
    sys.exit(0)

sys.exit(0)
