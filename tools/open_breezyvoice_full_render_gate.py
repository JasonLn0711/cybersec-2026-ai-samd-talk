#!/usr/bin/env python3
"""Record an explicit owner decision to proceed to BreezyVoice full render.

This does not rewrite returned expert-review decisions as human accepts. It
records that the project owner chose to skip another listening-review round
after the latest repair and move to the next concrete production step.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
VERSION = "v1"
OVERRIDE_PATH = LOCAL_ROOT / f"review/{VERSION}/full_render_owner_override.json"


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Open the BreezyVoice full-render gate by owner override.")
    parser.add_argument("--reason", required=True)
    parser.add_argument("--stage", default="final7-owner-release")
    parser.add_argument("--after-experiment-id", default="EXP-20260528-17")
    parser.add_argument("--version", default=VERSION)
    args = parser.parse_args()

    payload = {
        "full_render_allowed": True,
        "accepted_by_owner_override": True,
        "accepted_by_listening": False,
        "stage": args.stage,
        "after_experiment_id": args.after_experiment_id,
        "reason": args.reason,
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "policy": (
            "Proceed to full render without another human listening-review round; "
            "preserve returned review history and record post-render evidence."
        ),
    }
    OVERRIDE_PATH.parent.mkdir(parents=True, exist_ok=True)
    OVERRIDE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    subprocess.run([sys.executable, "tools/build_breezyvoice_pilot_review.py"], cwd=REPO_ROOT, check=True)
    result = subprocess.run(
        [sys.executable, "tools/check_breezyvoice_full_render_gate.py", "--write-report"],
        cwd=REPO_ROOT,
        check=False,
    )
    print(json.dumps({"override": rel(OVERRIDE_PATH), "gate_check_exit": result.returncode}, ensure_ascii=False, indent=2))
    return result.returncode


if __name__ == "__main__":
    sys.exit(main())
