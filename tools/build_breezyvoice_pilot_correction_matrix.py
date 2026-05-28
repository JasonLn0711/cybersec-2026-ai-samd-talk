#!/usr/bin/env python3
"""Build the pilot correction matrix for the BreezyVoice human gate.

This matrix explains what was reported by expert review, what narrow
conditioning has already been applied, and what the next listener still needs
to decide. It does not open the full-render gate.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
VERSION = "v1"

CORRECTIONS = {
    "cde_full_01_opening_positioning_crazyhunter_entry_case": {
        "expert_issue": (
            "Opening chunk was returned as total-reject for trust-question "
            "looping, bracket/control-like wording leakage, DICOM/PACS "
            "instability, and ASR-like filler residue."
        ),
        "conditioning_applied": (
            "Removed repeated trust-question pressure in model-facing text, "
            "replaced DICOM with a safer Chinese reading, normalized fillers "
            "and hesitant phrasing, and increased the opening split to 12 "
            "shorter subclips. Frozen source remains unchanged."
        ),
        "next_listener_question": (
            "Does final5b recover a stable CDE opening without loop, bracket "
            "leakage, or hesitant filler delivery?"
        ),
    },
    "cde_full_16_k8s_review_controls": {
        "expert_issue": (
            "K8S/RBAC/API and Tesla case section was returned as total-reject "
            "for K8S/Kubernetes collapse, robotic acronym spelling, API "
            "repetition, symbol leakage risk, and runtime compression."
        ),
        "conditioning_applied": (
            "Localized high-risk K8S/API passages, rewrote RBAC with a Chinese "
            "role-control anchor, removed dash/slash symbol risks, localized "
            "the Tesla exposed-console phrase, split to 10 subclips, and "
            "applied a reproducible 0.82 tempo pacing pass."
        ),
        "next_listener_question": (
            "Does final5b make RBAC, K8S, service accounts, API calls, and the "
            "Tesla credential path intelligible at the corrected 0.91 runtime "
            "ratio?"
        ),
    },
    "cde_full_20_crowdstrike_update_524b": {
        "expert_issue": (
            "CrowdStrike/524B section was returned as total-reject for FD&C "
            "symbol misreading, white-box homophone drift, threat/update drift, "
            "and filler-like phrasing in the regulatory bridge."
        ),
        "conditioning_applied": (
            "Replaced FD&C with an explicit F D C Act reading, replaced 524B "
            "with a Chinese/letter anchor, moved white-box wording to 白盒, "
            "localized interpreter and threat-update pressure, and split to 11 "
            "subclips."
        ),
        "next_listener_question": (
            "Does final5b preserve CrowdStrike, Falcon, supply-chain, 白盒, "
            "Section 524B, and SBOM credibility without filler-like stumbles?"
        ),
    },
    "cde_full_26_shared_close_test_anchors": {
        "expert_issue": (
            "Closing anchors were returned as total-reject for homophone drift "
            "around PACS downtime, internal program, vulnerability/governance "
            "phrasing, laughter-like hallucination, 524B/SBOM/root-cause drift, "
            "and tail residue after thanks."
        ),
        "conditioning_applied": (
            "Replaced risky homophones with safer Chinese technical wording, "
            "used 五二四/英文字母B款 and S B O M anchors, replaced root cause "
            "with 根本原因/根因, preserved 14 fine-grained subclips, and "
            "trimmed 0.8 seconds from the final thank-you subclip tail."
        ),
        "next_listener_question": (
            "Does final5b close with stable question anchors, no laughter-like "
            "artifact, correct 524B/SBOM/root-cause terms, and no tail residue?"
        ),
    },
}


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


def render_markdown(rows: list[dict[str, object]]) -> str:
    lines = [
        "# BreezyVoice Pilot Correction Matrix",
        "",
        "Purpose: preserve the expert-review-to-fix trace before any full 80-minute render.",
        "",
        "This is a listening-gate aid, not an acceptance decision. The full render",
        "remains closed until all four pilot parent chunks are accepted by human",
        "listening and the machine full-render gate exits `0`.",
        "",
        "| Chunk | Runtime / target | Gate | Expert issue | Conditioning applied | Next listener question |",
        "| --- | ---: | --- | --- | --- | --- |",
    ]
    for row in rows:
        runtime = row["runtime_seconds"] or "not rendered"
        ratio = row["runtime_to_target_ratio"] or "n/a"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{row['output_prefix']}`",
                    f"{runtime} / {row['target_seconds']} ({ratio})",
                    f"`{row['gate_decision']}` / `{row['review_status']}`",
                    str(row["expert_issue"]),
                    str(row["conditioning_applied"]),
                    str(row["next_listener_question"]),
                ]
            )
            + " |"
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    review_dir = LOCAL_ROOT / f"review/{VERSION}"
    render_review = {row["output_prefix"]: row for row in read_csv(review_dir / "render_review_log.csv")}
    pilot_review = {row["output_prefix"]: row for row in read_csv(review_dir / "pilot_listening_review.csv")}

    rows: list[dict[str, object]] = []
    for prefix, correction in CORRECTIONS.items():
        render_row = render_review.get(prefix, {})
        pilot_row = pilot_review.get(prefix, {})
        rows.append(
            {
                "output_prefix": prefix,
                "parent_wav": render_row.get("parent_wav", ""),
                "target_seconds": render_row.get("target_seconds", ""),
                "runtime_seconds": render_row.get("runtime_seconds", ""),
                "runtime_to_target_ratio": render_row.get("runtime_to_target_ratio", ""),
                "gate_decision": pilot_row.get("decision", ""),
                "review_status": render_row.get("review_status", pilot_row.get("review_status", "")),
                "expert_issue": correction["expert_issue"],
                "conditioning_applied": correction["conditioning_applied"],
                "current_fix_status": "model_facing_conditioning_applied_needs_human_relisten",
                "next_listener_question": correction["next_listener_question"],
                "evidence_paths": "; ".join(
                    item
                    for item in [
                        render_row.get("normalized_text_path", ""),
                        render_row.get("parent_wav", ""),
                        ".local/breezyvoice/review/v1/pilot_listening_review.csv",
                        ".local/breezyvoice/review/v1/render_review_log.csv",
                    ]
                    if item
                ),
                "stop_rule": "full_render_blocked_until_all_four_pilot_chunks_accept",
            }
        )

    fieldnames = [
        "output_prefix",
        "parent_wav",
        "target_seconds",
        "runtime_seconds",
        "runtime_to_target_ratio",
        "gate_decision",
        "review_status",
        "expert_issue",
        "conditioning_applied",
        "current_fix_status",
        "next_listener_question",
        "evidence_paths",
        "stop_rule",
    ]
    csv_path = review_dir / "pilot_correction_matrix.csv"
    md_path = review_dir / "pilot_correction_matrix.md"
    json_path = review_dir / "pilot_correction_matrix.json"
    write_csv(csv_path, rows, fieldnames)
    md_path.write_text(render_markdown(rows), encoding="utf-8")
    json_path.write_text(json.dumps(rows, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"rows": len(rows), "csv": rel(csv_path), "md": rel(md_path)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
