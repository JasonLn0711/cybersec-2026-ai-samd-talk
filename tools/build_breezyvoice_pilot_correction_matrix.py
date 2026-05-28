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
            "Latest partial-accept review kept this opening chunk rejected for "
            "trust-question looping around whether the system can be trusted "
            "and for hallucinated filler or fragment sounds in the clinical "
            "question sequence."
        ),
        "conditioning_applied": (
            "Converted the trust question into a short declarative checkpoint, "
            "rewrote the clinical question list into cleaner declarative "
            "sentences, removed hesitant fillers, and split the opening into "
            "19 short subclips with an 80-character ceiling. Frozen source "
            "remains unchanged."
        ),
        "next_listener_question": (
            "Does final6/final6b recover a stable CDE opening without trust-loop "
            "repetition or hesitant filler delivery?"
        ),
    },
    "cde_full_16_k8s_review_controls": {
        "expert_issue": (
            "Latest partial-accept review kept this K8S controls chunk rejected "
            "for tight RBAC and CI/CD boundaries, small clipping around the "
            "K8S application interface transition, and mechanical pacing in "
            "the Tesla case."
        ),
        "conditioning_applied": (
            "Inserted stronger punctuation around RBAC, service accounts, "
            "namespace isolation, CI/CD, and application endpoint transitions; "
            "kept the chunk at 9 manifest subclips; then applied a "
            "reproducible post-synthesis atempo=0.88 pacing pass."
        ),
        "next_listener_question": (
            "Does final6/final6b make RBAC, CI/CD, K8S endpoint wording, and "
            "the Tesla credential path intelligible at the corrected 0.89 "
            "runtime ratio?"
        ),
    },
    "cde_full_20_crowdstrike_update_524b": {
        "expert_issue": (
            "Latest partial-accept review kept this CrowdStrike/524B chunk "
            "rejected for SBOM being heard as SDOM, Rollback being heard as "
            "roll-bai, update-channel wording drift, 字母/子母 drift, and "
            "filler or stutter risk in the regulatory bridge."
        ),
        "conditioning_applied": (
            "Replaced rollback with 回滾 where appropriate, kept F D C Act and "
            "五二四/英文字母B款 anchors, retained 白盒 wording, removed filler "
            "pressure, and rerendered cde20-only final6b after ASR auxiliary "
            "warning by expanding SBOM to 軟體物料清單，英文四個字母，S，B，O，M."
        ),
        "next_listener_question": (
            "Does final6b preserve CrowdStrike, supply-chain, 白盒, Section "
            "524B, 回滾, and SBOM credibility without filler-like stumbles?"
        ),
    },
    "cde_full_26_shared_close_test_anchors": {
        "expert_issue": (
            "Latest partial-accept review accepted this closing chunk. The "
            "only note is to confirm whether 百格斯 is intended by the frozen "
            "script context."
        ),
        "conditioning_applied": (
            "Preserved the accepted final5b audio as the continuity baseline. "
            "No final6 rerender was performed for this accepted chunk."
        ),
        "next_listener_question": (
            "Does the accepted cde26 baseline remain suitable when heard "
            "inside the newly stitched final6/final6b pilot package?"
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
