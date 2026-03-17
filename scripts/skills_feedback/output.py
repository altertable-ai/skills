from __future__ import annotations

import sys


def print_confirmation(action: str, skill: str, proposal_id: str | None = None) -> None:
    if proposal_id:
        print(f"{action}: {skill} [{proposal_id}]")
    else:
        print(f"{action}: {skill}")


def print_warning(message: str) -> None:
    print(f"warning: {message}", file=sys.stderr)
