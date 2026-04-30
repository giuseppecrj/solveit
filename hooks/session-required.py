#!/usr/bin/env python3
"""Solveit PreToolUse hook: require an active session file before any edit."""
import json
import os
import sys

data = json.load(sys.stdin)
cwd = data.get("cwd", os.getcwd())

if not os.path.exists(os.path.join(cwd, ".solveit", "active")):
    sys.exit(0)

session = os.path.join(cwd, ".solveit", "session.md")

if not os.path.exists(session) or os.path.getsize(session) == 0:
    print(
        "Solveit: .solveit/session.md is missing or empty.\n"
        "Complete Phase 1 (Understand) and Phase 2 (Plan) — fill the template — before editing any code.",
        file=sys.stderr,
    )
    sys.exit(2)

with open(session) as f:
    text = f.read()

if "## Current checkpoint" not in text:
    print(
        "Solveit: session.md has no '## Current checkpoint' section.\n"
        "Define the smallest next step before editing.",
        file=sys.stderr,
    )
    sys.exit(2)

# Check the section has non-empty content
after = text.split("## Current checkpoint", 1)[1]
section = after.split("\n## ", 1)[0]
if not section.strip():
    print(
        "Solveit: '## Current checkpoint' is empty.\n"
        "Write the smallest next step before editing.",
        file=sys.stderr,
    )
    sys.exit(2)

sys.exit(0)
