#!/usr/bin/env python3
"""Solveit PreToolUse hook: block edits over the line cap when in Solveit mode."""
import json
import os
import sys

MAX_LINES = int(os.environ.get("SOLVEIT_MAX_LINES", "50"))

data = json.load(sys.stdin)
cwd = data.get("cwd", os.getcwd())

if not os.path.exists(os.path.join(cwd, ".solveit", "active")):
    sys.exit(0)

tool = data.get("tool_name", "")
ti = data.get("tool_input", {})

if tool == "Edit":
    text = ti.get("new_string", "")
elif tool == "Write":
    text = ti.get("content", "")
elif tool == "MultiEdit":
    text = "\n".join(e.get("new_string", "") for e in ti.get("edits", []))
elif tool == "apply_patch":
    text = ti.get("command", "")
else:
    sys.exit(0)

lines = text.count("\n") + (1 if text and not text.endswith("\n") else 0)

if lines > MAX_LINES:
    print(
        f"Solveit: edit is {lines} lines, exceeds the {MAX_LINES}-line checkpoint cap.\n"
        f"Split this checkpoint into smaller steps. Do not bypass — re-plan in .solveit/session.md.",
        file=sys.stderr,
    )
    sys.exit(2)

sys.exit(0)
