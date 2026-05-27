#!/usr/bin/env python3
"""Build the BreezyVoice render review log from current manifest evidence.

The log is intentionally conservative. Pilot rows inherit human listening
decisions from `pilot_listening_review.csv`; non-pilot rows remain pending
until the full-render gate opens and audio exists.
"""

from __future__ import annotations

import csv
import wave
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
VERSION = "v1"

PILOT_REVIEW_COLUMNS = [
    "check_acronyms",
    "check_k8s_524b_channel_file",
    "check_pacing",
    "check_fatigue",
    "check_opening_close_or_handoff",
    "check_no_markup_spoken",
]

MANUAL_FIELDS = ["pronunciation_issue", "fix_applied", "accepted", "notes"]


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def wav_duration(path: Path) -> float | None:
    if not path.exists():
        return None
    try:
        with wave.open(str(path), "rb") as wav:
            return wav.getnframes() / float(wav.getframerate())
    except wave.Error:
        return None


def format_seconds(value: float | None) -> str:
    return f"{value:.2f}" if value is not None else ""


def review_issue(row: dict[str, str]) -> str:
    notes = row.get("notes", "").strip()
    checks = [
        f"{column}={row[column]}"
        for column in PILOT_REVIEW_COLUMNS
        if row.get(column, "").strip() and row.get(column, "").strip() not in {"ok", "pass"}
    ]
    if notes and checks:
        return f"{notes} Checks: " + "; ".join(checks)
    if notes:
        return notes
    return "; ".join(checks)


def fix_summary(row: dict[str, str]) -> str:
    decision = row.get("decision", "").strip()
    if decision == "accept":
        return "No further pilot fix required by current listening decision."
    if decision == "reject":
        return (
            "Reject retained in pilot gate; apply the next minimal text, pacing, "
            "or rerender fix from expert review before full render."
        )
    if row:
        return "Human listening decision still required before full render."
    return ""


def review_status(prefix: str, audio_exists: bool, decision: str, in_pilot_review: bool) -> str:
    if in_pilot_review and decision == "accept":
        return "accepted_by_listening"
    if in_pilot_review and decision == "reject":
        return "rejected_by_listening_gate"
    if in_pilot_review:
        return "needs_listening"
    if audio_exists:
        return "needs_post_render_review"
    return "not_rendered_full_batch_gated"


def main() -> None:
    manifest_path = LOCAL_ROOT / f"manifests/{VERSION}/render_manifest.csv"
    subclip_path = LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.csv"
    pilot_review_path = LOCAL_ROOT / f"review/{VERSION}/pilot_listening_review.csv"
    review_log_path = LOCAL_ROOT / f"review/{VERSION}/render_review_log.csv"

    manifest_rows = read_csv(manifest_path)
    subclip_rows = read_csv(subclip_path)
    pilot_reviews = {row["output_prefix"]: row for row in read_csv(pilot_review_path)}
    existing_rows = {row["output_prefix"]: row for row in read_csv(review_log_path)}

    subclip_counts: dict[str, int] = {}
    for row in subclip_rows:
        prefix = row["parent_output_prefix"]
        subclip_counts[prefix] = subclip_counts.get(prefix, 0) + 1

    rows: list[dict[str, object]] = []
    for manifest in manifest_rows:
        prefix = manifest["output_prefix"]
        parent_wav = REPO_ROOT / manifest["planned_parent_wav"]
        duration = wav_duration(parent_wav)
        target_seconds = int(manifest["target_seconds"])
        ratio = duration / target_seconds if duration is not None and target_seconds else None
        pilot_review = pilot_reviews.get(prefix, {})
        existing = existing_rows.get(prefix, {})
        decision = pilot_review.get("decision", "").strip()
        audio_exists = parent_wav.exists()

        pronunciation_issue = review_issue(pilot_review) if pilot_review else ""
        fix_applied = fix_summary(pilot_review) if pilot_review else ""
        accepted = decision if pilot_review else ""
        notes = pilot_review.get("notes", "").strip() if pilot_review else ""

        for field in MANUAL_FIELDS:
            if existing.get(field, "").strip() and not pilot_review:
                if field == "accepted":
                    accepted = existing[field].strip()
                elif field == "pronunciation_issue":
                    pronunciation_issue = existing[field].strip()
                elif field == "fix_applied":
                    fix_applied = existing[field].strip()
                elif field == "notes":
                    notes = existing[field].strip()

        rows.append(
            {
                "output_prefix": prefix,
                "parent_wav": rel(parent_wav),
                "subclip_count": subclip_counts.get(prefix, manifest.get("subclip_count", "")),
                "target_seconds": target_seconds,
                "runtime": format_seconds(duration),
                "runtime_seconds": format_seconds(duration),
                "runtime_to_target_ratio": f"{ratio:.2f}" if ratio is not None else "",
                "audio_exists": str(audio_exists).lower(),
                "normalized_text_path": manifest["normalized_text_path"],
                "pronunciation_issue": pronunciation_issue,
                "fix_applied": fix_applied,
                "accepted": accepted,
                "review_status": review_status(prefix, audio_exists, decision, bool(pilot_review)),
                "review_source": "pilot_listening_review.csv" if pilot_review else "render_manifest.csv",
                "notes": notes,
            }
        )

    write_csv(
        review_log_path,
        rows,
        [
            "output_prefix",
            "parent_wav",
            "subclip_count",
            "target_seconds",
            "runtime",
            "runtime_seconds",
            "runtime_to_target_ratio",
            "audio_exists",
            "normalized_text_path",
            "pronunciation_issue",
            "fix_applied",
            "accepted",
            "review_status",
            "review_source",
            "notes",
        ],
    )
    print(f"wrote {rel(review_log_path)} rows={len(rows)}")


if __name__ == "__main__":
    main()
