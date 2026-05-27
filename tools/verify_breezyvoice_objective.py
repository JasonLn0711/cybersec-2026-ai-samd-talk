#!/usr/bin/env python3
"""Verify the CDE 2026 BreezyVoice v1 objective against current evidence.

This verifier is intentionally strict: it proves completed setup surfaces,
records human-review gates, and keeps the full objective incomplete until the
required pilot acceptance and full render/stitch artifacts exist.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import wave
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
VERSION = "v1"
REQUIRED_PILOT_PREFIXES = [
    "cde_full_01_opening_positioning_crazyhunter_entry_case",
    "cde_full_16_k8s_review_controls",
    "cde_full_20_crowdstrike_update_524b",
    "cde_full_26_shared_close_test_anchors",
]
FORBIDDEN_MODEL_TOKENS = ["BV26", "[BV26", "[/BV26]", "<!--", "-->", "```", "\n#"]


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def wav_duration(path: Path) -> float | None:
    if not path.exists():
        return None
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / float(wav.getframerate())


def row(requirement: str, status: str, evidence: list[str], notes: list[str] | None = None) -> dict[str, object]:
    return {
        "requirement": requirement,
        "status": status,
        "evidence": evidence,
        "notes": notes or [],
    }


def validate_text_files(paths: list[Path]) -> tuple[bool, list[str]]:
    failures = []
    for path in paths:
        text = path.read_text(encoding="utf-8")
        hits = [token for token in FORBIDDEN_MODEL_TOKENS if token in text]
        if hits:
            failures.append(f"{rel(path)} contains {hits}")
    return not failures, failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the BreezyVoice v1 objective state.")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()

    paths = {
        "freeze": LOCAL_ROOT / f"freeze/{VERSION}/freeze_report.json",
        "summary": LOCAL_ROOT / f"manifests/{VERSION}/package_summary.json",
        "render_manifest": LOCAL_ROOT / f"manifests/{VERSION}/render_manifest.csv",
        "subclip_manifest": LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.csv",
        "pilot_manifest": LOCAL_ROOT / f"manifests/{VERSION}/pilot_manifest.csv",
        "full_gate": LOCAL_ROOT / f"review/{VERSION}/full_batch_gate.json",
        "pilot_review": LOCAL_ROOT / f"review/{VERSION}/pilot_listening_review.csv",
        "gate_check": LOCAL_ROOT / f"review/{VERSION}/full_render_gate_check.json",
        "review_log": LOCAL_ROOT / f"review/{VERSION}/render_review_log.csv",
        "reference_gate": LOCAL_ROOT / f"prompts/{VERSION}/reference_audio_gate.json",
        "audio_spec": LOCAL_ROOT / f"specs/{VERSION}/audio_output_spec.json",
        "experiment_log": REPO_ROOT / "docs/speaker-notes/breezyvoice/cde-2026-breezyvoice-tts-experiment-log-v1.jsonl",
    }
    missing = {name: rel(path) for name, path in paths.items() if not path.exists()}
    if missing:
        payload = {"overall_status": "missing_evidence", "missing": missing}
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 2

    freeze = read_json(paths["freeze"])
    summary = read_json(paths["summary"])
    render_manifest = read_csv(paths["render_manifest"])
    subclip_manifest = read_csv(paths["subclip_manifest"])
    pilot_manifest = read_csv(paths["pilot_manifest"])
    full_gate = read_json(paths["full_gate"])
    pilot_review = read_csv(paths["pilot_review"])
    gate_check = read_json(paths["gate_check"])
    review_log = read_csv(paths["review_log"])
    reference_gate = read_json(paths["reference_gate"])
    audio_spec = read_json(paths["audio_spec"])
    experiment_records = [
        json.loads(line)
        for line in paths["experiment_log"].read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    segment_texts = sorted((LOCAL_ROOT / f"inputs/{VERSION}/segments").glob("*.txt"))
    normalized_segment_texts = sorted((LOCAL_ROOT / f"inputs/{VERSION}/normalized_segments").glob("*.txt"))
    subclip_texts = sorted((LOCAL_ROOT / f"inputs/{VERSION}/subclips").glob("*.txt"))
    segment_texts_ok, segment_text_failures = validate_text_files(segment_texts)
    normalized_texts_ok, normalized_text_failures = validate_text_files(normalized_segment_texts + subclip_texts)

    subclips_by_parent: dict[str, list[dict[str, str]]] = defaultdict(list)
    overlong_subclips = []
    for item in subclip_manifest:
        subclips_by_parent[item["parent_output_prefix"]].append(item)
        if int(item["text_characters"]) > 500:
            overlong_subclips.append(item["subclip_id"])
    bad_parent_counts = {
        prefix: len(items)
        for prefix, items in subclips_by_parent.items()
        if not (2 <= len(items) <= 4)
    }

    pilot_prefixes = [row["output_prefix"] for row in pilot_manifest]
    pilot_review_by_prefix = {row["output_prefix"]: row for row in pilot_review}
    pilot_missing = [prefix for prefix in REQUIRED_PILOT_PREFIXES if prefix not in pilot_prefixes]
    pilot_unaccepted = [
        prefix
        for prefix in REQUIRED_PILOT_PREFIXES
        if pilot_review_by_prefix.get(prefix, {}).get("decision") != "accept"
    ]
    pilot_parent_wavs = [REPO_ROOT / pilot_review_by_prefix[prefix]["parent_wav"] for prefix in REQUIRED_PILOT_PREFIXES if prefix in pilot_review_by_prefix]
    pilot_parent_wavs_exist = [path for path in pilot_parent_wavs if path.exists()]
    full_lecture_wav = LOCAL_ROOT / f"output/{VERSION}/full/cde-2026-breezyvoice-80min-v1.wav"
    full_lecture_duration = wav_duration(full_lecture_wav)
    accepted_review_rows = [row_ for row_ in review_log if row_.get("accepted") == "accept"]

    checks = [
        row(
            "1. freeze v1 source",
            "completed" if freeze.get("segment_count") == 26 and freeze.get("target_total_time") == "80:00" and freeze.get("model_text_characters") == 28053 else "failed",
            [rel(paths["freeze"])],
            [
                f"segment_count={freeze.get('segment_count')}",
                f"target_total_time={freeze.get('target_total_time')}",
                f"model_text_characters={freeze.get('model_text_characters')}",
            ],
        ),
        row(
            "2. render manifest",
            "completed" if len(render_manifest) == 26 and all(key in render_manifest[0] for key in ["output_prefix", "segment_id", "preset", "target_duration", "timeline", "clean_text_path", "pronunciation_hints"]) else "failed",
            [rel(paths["render_manifest"])],
            [f"rows={len(render_manifest)}"],
        ),
        row(
            "3. clean text inputs",
            "completed" if len(segment_texts) == 26 and segment_texts_ok else "failed",
            [rel(LOCAL_ROOT / f"inputs/{VERSION}/segments")],
            [f"files={len(segment_texts)}", *segment_text_failures],
        ),
        row(
            "4. subclip split",
            "completed" if len(subclip_manifest) == 92 and not bad_parent_counts and not overlong_subclips else "failed",
            [rel(paths["subclip_manifest"])],
            [f"subclips={len(subclip_manifest)}", f"bad_parent_counts={bad_parent_counts}", f"overlong_subclips={overlong_subclips}"],
        ),
        row(
            "5. TTS text normalization",
            "completed" if normalized_texts_ok else "failed",
            [rel(LOCAL_ROOT / f"inputs/{VERSION}/normalized_segments"), rel(LOCAL_ROOT / f"inputs/{VERSION}/subclips")],
            normalized_text_failures,
        ),
        row(
            "6. pronunciation override policy",
            "completed" if (LOCAL_ROOT / f"inputs/{VERSION}/pronunciation_override_policy.md").exists() else "failed",
            [rel(LOCAL_ROOT / f"inputs/{VERSION}/pronunciation_override_policy.md")],
            ["policy is pilot-evidence based"],
        ),
        row(
            "7. reference audio policy",
            "completed_no_reference_mode" if reference_gate.get("reference_audio_required") is False else "failed",
            [rel(paths["reference_gate"])],
            [
                "reference audio is optional by current user policy",
                f"audio_exists={reference_gate.get('audio_exists')}",
                f"status={reference_gate.get('status')}",
            ],
        ),
        row(
            "8. audio output spec",
            "completed" if audio_spec.get("format") == "wav" and audio_spec.get("loudness_lufs") == -16 else "failed",
            [rel(paths["audio_spec"])],
            [f"format={audio_spec.get('format')}", f"loudness_lufs={audio_spec.get('loudness_lufs')}"],
        ),
        row(
            "9. pilot render only",
            "completed_pilot_rendered" if len(pilot_manifest) == 4 and len(pilot_parent_wavs_exist) == 4 and not full_lecture_wav.exists() else "failed",
            [rel(paths["pilot_manifest"]), rel(paths["pilot_review"])],
            [f"pilot_rows={len(pilot_manifest)}", f"pilot_parent_wavs={len(pilot_parent_wavs_exist)}", f"full_lecture_exists={full_lecture_wav.exists()}"],
        ),
        row(
            "10. pilot review checklist",
            "completed" if (LOCAL_ROOT / f"review/{VERSION}/pilot_review_checklist.md").exists() else "failed",
            [rel(LOCAL_ROOT / f"review/{VERSION}/pilot_review_checklist.md")],
            [],
        ),
        row(
            "11. correction rules",
            "completed" if (LOCAL_ROOT / f"review/{VERSION}/pilot_review_checklist.md").exists() else "failed",
            [rel(LOCAL_ROOT / f"review/{VERSION}/pilot_review_checklist.md")],
            ["checklist records correction order"],
        ),
        row(
            "12. full render acceptance gate",
            "gated_waiting_human_review" if full_gate.get("full_batch_allowed") is False and gate_check.get("allowed") is False else "completed_open",
            [rel(paths["full_gate"]), rel(paths["gate_check"])],
            [f"pilot_missing={pilot_missing}", f"pilot_unaccepted={pilot_unaccepted}", f"machine_review_status={gate_check.get('machine_review_status')}"],
        ),
        row(
            "13. full render stitch and review log",
            "gated_incomplete" if full_lecture_duration is None else "needs_review_log_completion",
            [rel(paths["review_log"]), rel(full_lecture_wav)],
            [f"full_lecture_duration={full_lecture_duration}", f"accepted_review_rows={len(accepted_review_rows)}"],
        ),
        row(
            "14. TTS experiment log",
            "completed" if len(experiment_records) >= 7 else "failed",
            [rel(paths["experiment_log"])],
            [f"records={len(experiment_records)}"],
        ),
    ]

    hard_failures = [item for item in checks if item["status"] == "failed"]
    gated = [item for item in checks if str(item["status"]).startswith("gated")]
    overall_status = "failed" if hard_failures else "gated_waiting_human_review" if gated else "complete"
    payload = {
        "overall_status": overall_status,
        "completed": overall_status == "complete",
        "checks": checks,
        "stop_rule": "Do not run full render until requirement 12 is completed_open and the full-render gate checker exits 0.",
        "next_action": (
            "Wait for human listening acceptance or apply the next expert-specified minimal pilot fix."
            if overall_status == "gated_waiting_human_review"
            else "Resolve failed checks before proceeding."
            if overall_status == "failed"
            else "Proceed to full render and post-render stitch/log completion."
        ),
    }
    if args.write_report:
        out = LOCAL_ROOT / f"review/{VERSION}/objective_verification.json"
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if overall_status == "complete" else 2


if __name__ == "__main__":
    sys.exit(main())
