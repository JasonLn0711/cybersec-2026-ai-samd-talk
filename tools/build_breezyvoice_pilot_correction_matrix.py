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
            "Opening chunk was rejected again for stutters, filler-like vocal "
            "artifacts, acronym instability, and loss of professional authority."
        ),
        "conditioning_applied": (
            "Applied model-facing sanitizer for stage cues, fillers, and known "
            "hallucination residues; kept frozen source unchanged; retained "
            "short opening subclips and PACS/HIS/EMR/DICOM isolation."
        ),
        "next_listener_question": (
            "Does the round-2 rerendered opening recover clinical authority, or "
            "does no-reference/default voice remain unstable for this lecture?"
        ),
    },
    "cde_full_16_k8s_review_controls": {
        "expert_issue": (
            "K8S/RBAC/service-account section was rejected for compressed pacing, "
            "technical acronym collapse, and no-reference hallucination."
        ),
        "conditioning_applied": (
            "Forced this parent chunk to four shorter subclips; increased stitch "
            "silence to 700ms; normalized high-risk K8S phrases toward "
            "Kubernetes API / Kubernetes console where the prior K eight S path "
            "was unstable."
        ),
        "next_listener_question": (
            "Is the round-2 K8S section understandable enough, or should this "
            "workflow switch away from no-reference/default voice before any "
            "further render work?"
        ),
    },
    "cde_full_20_crowdstrike_update_524b": {
        "expert_issue": (
            "CrowdStrike/524B section was rejected for emotional leakage, sighing "
            "artifacts, and hallucination around law and supply-chain terms."
        ),
        "conditioning_applied": (
            "Kept CrowdStrike/Falcon/supply-chain/Section 524B boundaries, forced "
            "four subclips, rebuilt the ASR auxiliary transcript after rerender, "
            "and preserved the frozen source."
        ),
        "next_listener_question": (
            "Does Section 524B now sound steady and professional, or does the "
            "default voice still leak emotion/hallucinated words around this term?"
        ),
    },
    "cde_full_26_shared_close_test_anchors": {
        "expert_issue": (
            "Closing anchors were rejected for tail-end breakdown, fatigue, and "
            "word-salad hallucination."
        ),
        "conditioning_applied": (
            "Split the close into anchor-based subclips around first, second, and "
            "third questions; sanitized model-facing text; added 700ms stitch "
            "silence; kept the closing trust-chain content intact."
        ),
        "next_listener_question": (
            "Does anchor-based rerendering prevent the closing tail collapse, or "
            "does the project need a different voice path before full render?"
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
