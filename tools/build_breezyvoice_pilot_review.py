#!/usr/bin/env python3
"""Build a local listening-review package for BreezyVoice pilot outputs."""

from __future__ import annotations

import csv
import json
import wave
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
VERSION = "v1"
PILOT_COMBINED_WAV = LOCAL_ROOT / f"output/{VERSION}/full/cde-2026-breezyvoice-pilot-stitched-v1.wav"
ASR_TXT = LOCAL_ROOT / f"review/{VERSION}/asr/cde-2026-breezyvoice-pilot-stitched-v1.txt"


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


def wav_duration(path: Path) -> float | None:
    if not path.exists():
        return None
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / float(wav.getframerate())


def load_text(path_value: str) -> str:
    path = REPO_ROOT / path_value
    return path.read_text(encoding="utf-8").strip()


def target_seconds(value: str) -> int:
    minutes, seconds = value.split(":")
    return int(minutes) * 60 + int(seconds)


def current_decision(existing: dict[str, str], runtime_seconds: str, subclip_count: int) -> tuple[str, str]:
    decision = existing.get("decision", "")
    notes = existing.get("notes", "")
    if decision not in {"accept", "reject"}:
        return decision, notes

    previous_runtime = existing.get("runtime_seconds", "")
    previous_subclip_count = existing.get("subclip_count", "")
    if previous_runtime == runtime_seconds and previous_subclip_count == str(subclip_count):
        return decision, notes

    stale_note = (
        f"Prior decision `{decision}` invalidated by new render metadata "
        f"(previous runtime={previous_runtime or 'unknown'}, previous subclips={previous_subclip_count or 'unknown'}; "
        f"current runtime={runtime_seconds or 'unknown'}, current subclips={subclip_count}). "
        "Fresh human listening review required."
    )
    if stale_note in notes:
        return "", notes
    return "", f"{notes} | {stale_note}" if notes else stale_note


def main() -> None:
    manifest_rows = read_csv(LOCAL_ROOT / f"manifests/{VERSION}/render_manifest.csv")
    pilot_rows = read_csv(LOCAL_ROOT / f"manifests/{VERSION}/pilot_manifest.csv")
    subclip_rows = read_csv(LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.csv")
    total_subclips = len(subclip_rows)
    stitch_summary_path = LOCAL_ROOT / f"review/{VERSION}/pilot_stitch_summary.json"
    machine_review_path = LOCAL_ROOT / f"review/{VERSION}/pilot_machine_review.json"
    existing_review_path = LOCAL_ROOT / f"review/{VERSION}/pilot_listening_review.csv"

    manifest_by_prefix = {row["output_prefix"]: row for row in manifest_rows}
    subclips_by_prefix: dict[str, list[dict[str, str]]] = {}
    for row in subclip_rows:
        subclips_by_prefix.setdefault(row["parent_output_prefix"], []).append(row)
    for rows in subclips_by_prefix.values():
        rows.sort(key=lambda row: int(row["subclip_index"]))

    stitch_summary = json.loads(stitch_summary_path.read_text(encoding="utf-8")) if stitch_summary_path.exists() else {}
    machine_review = json.loads(machine_review_path.read_text(encoding="utf-8")) if machine_review_path.exists() else {}
    asr_exists = ASR_TXT.exists()
    existing_reviews = {}
    if existing_review_path.exists():
        for row in read_csv(existing_review_path):
            existing_reviews[row["output_prefix"]] = row

    review_rows: list[dict[str, object]] = []
    playlist_lines = ["#EXTM3U"]
    md_lines = [
        "# BreezyVoice Pilot Listening Review",
        "",
        f"Purpose: decide whether the four pilot rows are acceptable before running the full `{total_subclips}` subclip batch.",
        "",
        "Combined pilot WAV:",
        "",
        f"- `{rel(PILOT_COMBINED_WAV)}`",
        "",
        "Machine signals:",
        "",
        f"- ASR transcript exists: `{asr_exists}`",
        f"- Machine review status: `{machine_review.get('status', 'not_available')}`",
        f"- Forbidden markup hits: `{machine_review.get('asr_forbidden_markup_hits', {})}`",
        "",
        "Decision rule:",
        "",
        "- Keep `full_batch_allowed=false` until all four parent rows are accepted by listening.",
        "- If any row fails, fix the smallest affected surface first: punctuation, English spacing, single-term replacement, shorter subclip, preset/pause, then spoken-content edit.",
        "",
        "| Parent | WAV | Runtime | Target | Ratio | Review status |",
        "| --- | --- | ---: | ---: | ---: | --- |",
    ]

    for pilot in pilot_rows:
        prefix = pilot["output_prefix"]
        manifest = manifest_by_prefix[prefix]
        parent_wav = REPO_ROOT / manifest["planned_parent_wav"]
        duration = wav_duration(parent_wav)
        target = target_seconds(manifest["target_duration"])
        ratio = (duration / target) if duration else None
        subclips = subclips_by_prefix[prefix]
        source_preview = load_text(manifest["normalized_text_path"])[:260]
        status = "needs_listening"
        if duration is None:
            status = "missing_parent_wav"
        elif ratio and (ratio < 0.75 or ratio > 1.45):
            status = "needs_pacing_review"
        existing = existing_reviews.get(prefix, {})
        runtime_value = f"{duration:.2f}" if duration is not None else ""
        decision, notes = current_decision(existing, runtime_value, len(subclips))
        if decision == "accept":
            status = "accepted_by_listening"

        review_rows.append(
            {
                "output_prefix": prefix,
                "parent_wav": rel(parent_wav),
                "subclip_count": len(subclips),
                "runtime_seconds": runtime_value,
                "target_seconds": target,
                "runtime_to_target_ratio": f"{ratio:.2f}" if ratio is not None else "",
                "normalized_text_path": manifest["normalized_text_path"],
                "source_preview": source_preview,
                "check_acronyms": existing.get("check_acronyms", ""),
                "check_k8s_524b_channel_file": existing.get("check_k8s_524b_channel_file", ""),
                "check_pacing": existing.get("check_pacing", ""),
                "check_fatigue": existing.get("check_fatigue", ""),
                "check_opening_close_or_handoff": existing.get("check_opening_close_or_handoff", ""),
                "check_no_markup_spoken": existing.get("check_no_markup_spoken", ""),
                "decision": decision,
                "review_status": status,
                "notes": notes,
            }
        )
        playlist_lines.append(f"#EXTINF:{int(duration or 0)},{prefix}")
        playlist_lines.append(rel(parent_wav))
        md_lines.append(
            "| "
            + " | ".join(
                [
                    f"`{prefix}`",
                    f"`{rel(parent_wav)}`",
                    f"{duration:.2f}" if duration is not None else "",
                    str(target),
                    f"{ratio:.2f}" if ratio is not None else "",
                    status,
                ]
            )
            + " |"
        )

    accepted = all(row["decision"] == "accept" for row in review_rows)
    unaccepted = [row["output_prefix"] for row in review_rows if row["decision"] != "accept"]
    full_gate = {
        "full_batch_allowed": accepted,
        "accepted_by_listening": accepted,
        "pilot_parent_count": len(review_rows),
        "review_rows_requiring_decision": sum(1 for row in review_rows if row["decision"] != "accept"),
        "unaccepted_prefixes": unaccepted,
        "pilot_combined_wav": rel(PILOT_COMBINED_WAV),
        "pilot_listening_review_csv": f".local/breezyvoice/review/{VERSION}/pilot_listening_review.csv",
        "pilot_listening_review_md": f".local/breezyvoice/review/{VERSION}/pilot_listening_review.md",
        "pilot_review_playlist": f".local/breezyvoice/review/{VERSION}/pilot_review_playlist.m3u",
        "machine_review_status": machine_review.get("status", "not_available"),
        "reason": "human listening acceptance required before full batch",
    }

    review_dir = LOCAL_ROOT / f"review/{VERSION}"
    write_csv(
        review_dir / "pilot_listening_review.csv",
        review_rows,
        [
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
        ],
    )
    (review_dir / "pilot_listening_review.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")
    (review_dir / "pilot_review_playlist.m3u").write_text("\n".join(playlist_lines) + "\n", encoding="utf-8")
    (review_dir / "full_batch_gate.json").write_text(json.dumps(full_gate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(full_gate, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
