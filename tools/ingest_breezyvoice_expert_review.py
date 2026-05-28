#!/usr/bin/env python3
"""Ingest returned BreezyVoice expert pilot review decisions.

The script updates the local pilot listening review only when every required
pilot parent chunk has an explicit `accept` or `reject` decision.
"""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
VERSION = "v1"
DEFAULT_EXPERT_FORM = Path.home() / "Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/forms/expert_pilot_review_form.csv"
REQUIRED_PREFIXES = [
    "cde_full_01_opening_positioning_crazyhunter_entry_case",
    "cde_full_16_k8s_review_controls",
    "cde_full_20_crowdstrike_update_524b",
    "cde_full_26_shared_close_test_anchors",
]
LOCAL_REVIEW_FIELDS = [
    "output_prefix",
    "parent_wav",
    "subclip_count",
    "runtime_seconds",
    "target_seconds",
    "runtime_to_target_ratio",
    "normalized_text_path",
    "source_preview",
    "check_acronyms",
    "check_k8s_524b_channel_file",
    "check_pacing",
    "check_fatigue",
    "check_opening_close_or_handoff",
    "check_no_markup_spoken",
    "decision",
    "review_status",
    "notes",
]


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def norm(value: str | None) -> str:
    return (value or "").strip()


def row_prefix(row: dict[str, str]) -> str:
    value = (
        norm(row.get("output_prefix"))
        or norm(row.get("parent_chunk_id"))
        or norm(row.get("parent_chunk"))
        or norm(row.get("chunk_id"))
    )
    if value.endswith(".wav"):
        value = value[:-4]
    return value


def row_decision(row: dict[str, str]) -> str:
    return norm(row.get("decision_accept_or_reject") or row.get("decision")).lower()


def compact_notes(parts: list[str]) -> str:
    return " | ".join(part for part in (part.strip() for part in parts) if part)


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest returned BreezyVoice expert pilot review CSV.")
    parser.add_argument("--input", type=Path, default=DEFAULT_EXPERT_FORM)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--allow-partial", action="store_true", help="Allow a subset of required rows; normally disabled.")
    args = parser.parse_args()

    expert_form = args.input.expanduser().resolve()
    local_review_path = LOCAL_ROOT / f"review/{VERSION}/pilot_listening_review.csv"
    if not expert_form.exists():
        raise SystemExit(f"Missing expert review form: {expert_form}")
    if not local_review_path.exists():
        raise SystemExit(f"Missing local review CSV: {local_review_path}")

    expert_rows = read_csv(expert_form)
    local_rows = read_csv(local_review_path)
    expert_by_prefix = {row_prefix(row): row for row in expert_rows if row_prefix(row)}
    local_by_prefix = {row["output_prefix"]: row for row in local_rows}

    missing_rows = [prefix for prefix in REQUIRED_PREFIXES if prefix not in expert_by_prefix]
    if missing_rows and not args.allow_partial:
        payload = {
            "ingested": False,
            "status": "missing_required_rows",
            "missing_rows": missing_rows,
            "input": str(expert_form),
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2

    invalid_decisions = {}
    for prefix in REQUIRED_PREFIXES:
        if prefix not in expert_by_prefix:
            continue
        decision = row_decision(expert_by_prefix[prefix])
        if decision not in {"accept", "reject"}:
            invalid_decisions[prefix] = decision
    if invalid_decisions:
        payload = {
            "ingested": False,
            "status": "invalid_or_blank_decisions",
            "invalid_decisions": invalid_decisions,
            "input": str(expert_form),
            "required_values": ["accept", "reject"],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2

    updated_rows: list[dict[str, object]] = []
    changed_prefixes: list[str] = []
    accepted: list[str] = []
    rejected: list[str] = []
    for row in local_rows:
        prefix = row["output_prefix"]
        expert = expert_by_prefix.get(prefix)
        if not expert:
            updated_rows.append(row)
            continue

        decision = row_decision(expert)
        if decision == "accept":
            accepted.append(prefix)
        else:
            rejected.append(prefix)

        updated = dict(row)
        updated["check_acronyms"] = norm(expert.get("expert_check_acronyms")) or updated.get("check_acronyms", "")
        updated["check_k8s_524b_channel_file"] = norm(expert.get("expert_check_key_terms")) or updated.get("check_k8s_524b_channel_file", "")
        updated["check_pacing"] = norm(expert.get("expert_check_pacing")) or updated.get("check_pacing", "")
        updated["check_fatigue"] = norm(expert.get("expert_check_fatigue")) or updated.get("check_fatigue", "")
        updated["check_opening_close_or_handoff"] = norm(expert.get("expert_check_opening_handoff_close")) or updated.get("check_opening_close_or_handoff", "")
        updated["check_no_markup_spoken"] = norm(expert.get("expert_check_no_markup_spoken")) or updated.get("check_no_markup_spoken", "")
        updated["decision"] = decision
        updated["review_status"] = "accepted_by_listening" if decision == "accept" else "needs_listening"
        updated["notes"] = compact_notes(
            [
                updated.get("notes", ""),
                f"Expert decision: {decision}",
                f"pronunciation_issue={norm(expert.get('pronunciation_issue'))}",
                f"fix_recommendation={norm(expert.get('fix_recommendation'))}",
                norm(expert.get("notes")),
            ]
        )
        updated_rows.append(updated)
        changed_prefixes.append(prefix)

    payload = {
        "ingested": not args.dry_run,
        "dry_run": args.dry_run,
        "input": str(expert_form),
        "changed_prefixes": changed_prefixes,
        "accepted_prefixes": accepted,
        "rejected_prefixes": rejected,
        "all_required_accepted": len(accepted) == len(REQUIRED_PREFIXES) and not rejected,
        "local_review": rel(local_review_path),
        "checked_at": datetime.now(timezone.utc).isoformat(),
    }

    if not args.dry_run:
        write_csv(local_review_path, updated_rows, LOCAL_REVIEW_FIELDS)
        subprocess.run([sys.executable, "tools/build_breezyvoice_pilot_review.py"], cwd=REPO_ROOT, check=True)
        subprocess.run([sys.executable, "tools/check_breezyvoice_full_render_gate.py", "--write-report"], cwd=REPO_ROOT, check=False)
        ingest_path = LOCAL_ROOT / f"review/{VERSION}/expert_review_ingest_result.json"
        ingest_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
