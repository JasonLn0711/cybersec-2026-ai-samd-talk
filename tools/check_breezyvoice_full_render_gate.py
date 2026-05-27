#!/usr/bin/env python3
"""Check whether BreezyVoice full render is allowed.

This is a machine stop gate. It reads the local pilot listening decision table
and full-batch gate, then exits non-zero unless the four required pilot parent
chunks have accepted human listening decisions.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
VERSION = "v1"
REQUIRED_PREFIXES = [
    "cde_full_01_opening_positioning_crazyhunter_entry_case",
    "cde_full_16_k8s_review_controls",
    "cde_full_20_crowdstrike_update_524b",
    "cde_full_26_shared_close_test_anchors",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def main() -> int:
    parser = argparse.ArgumentParser(description="Check BreezyVoice full-render acceptance gate.")
    parser.add_argument("--write-report", action="store_true", help="Write .local/breezyvoice/review/v1/full_render_gate_check.json")
    args = parser.parse_args()

    review_dir = LOCAL_ROOT / f"review/{VERSION}"
    gate_path = review_dir / "full_batch_gate.json"
    listening_path = review_dir / "pilot_listening_review.csv"
    machine_path = review_dir / "pilot_machine_review.json"
    summary_path = LOCAL_ROOT / f"manifests/{VERSION}/package_summary.json"

    missing_files = [path for path in [gate_path, listening_path, machine_path, summary_path] if not path.exists()]
    if missing_files:
        payload = {
            "allowed": False,
            "status": "missing_gate_files",
            "missing_files": [rel(path) for path in missing_files],
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2

    gate = read_json(gate_path)
    machine = read_json(machine_path)
    summary = read_json(summary_path)
    rows = read_csv(listening_path)
    rows_by_prefix = {row["output_prefix"]: row for row in rows}

    missing_prefixes = [prefix for prefix in REQUIRED_PREFIXES if prefix not in rows_by_prefix]
    unaccepted_prefixes = [
        prefix
        for prefix in REQUIRED_PREFIXES
        if rows_by_prefix.get(prefix, {}).get("decision") != "accept"
    ]
    reject_prefixes = [
        prefix
        for prefix in REQUIRED_PREFIXES
        if rows_by_prefix.get(prefix, {}).get("decision") == "reject"
    ]
    undecided_prefixes = [
        prefix
        for prefix in REQUIRED_PREFIXES
        if rows_by_prefix.get(prefix, {}).get("decision", "") == ""
    ]

    reasons: list[str] = []
    if not gate.get("full_batch_allowed"):
        reasons.append("full_batch_gate.json has full_batch_allowed=false")
    if not gate.get("accepted_by_listening"):
        reasons.append("full_batch_gate.json has accepted_by_listening=false")
    if missing_prefixes:
        reasons.append(f"missing required pilot decision rows: {', '.join(missing_prefixes)}")
    if unaccepted_prefixes:
        reasons.append(f"unaccepted required pilot chunks: {', '.join(unaccepted_prefixes)}")
    if summary.get("full_batch_allowed") is True and gate.get("full_batch_allowed") is not True:
        reasons.append("package_summary and full_batch_gate disagree")

    allowed = not reasons
    payload = {
        "allowed": allowed,
        "status": "full_render_allowed" if allowed else "full_render_blocked",
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "version": VERSION,
        "summary": {
            "segments": summary.get("segments"),
            "subclips": summary.get("subclips"),
            "model_text_characters": summary.get("model_text_characters"),
            "duration_seconds": summary.get("duration_seconds"),
            "reference_audio_required": summary.get("reference_audio_required"),
            "pilot_execution_mode": summary.get("pilot_execution_mode"),
        },
        "full_batch_gate": {
            "full_batch_allowed": gate.get("full_batch_allowed"),
            "accepted_by_listening": gate.get("accepted_by_listening"),
            "machine_review_status": gate.get("machine_review_status"),
        },
        "machine_review_status": machine.get("status"),
        "required_prefixes": REQUIRED_PREFIXES,
        "missing_prefixes": missing_prefixes,
        "reject_prefixes": reject_prefixes,
        "undecided_prefixes": undecided_prefixes,
        "unaccepted_prefixes": unaccepted_prefixes,
        "reasons": reasons,
        "stop_rule": (
            "Do not run full render until full_batch_allowed=true and every required pilot parent chunk has decision=accept."
        ),
        "next_action": (
            "Wait for human listening review or apply only the next expert-specified minimal pilot fix, then re-export a Downloads review package."
            if not allowed
            else "Full render may proceed; keep review logs complete during and after render."
        ),
        "evidence": {
            "gate": rel(gate_path),
            "listening_review": rel(listening_path),
            "machine_review": rel(machine_path),
            "package_summary": rel(summary_path),
        },
    }
    if args.write_report:
        report_path = review_dir / "full_render_gate_check.json"
        report_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if allowed else 2


if __name__ == "__main__":
    sys.exit(main())
