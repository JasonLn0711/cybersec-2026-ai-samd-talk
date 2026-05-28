#!/usr/bin/env python3
"""Append a durable BreezyVoice TTS experiment record.

The tracked Markdown/JSONL log stores decisions, commands, local evidence paths,
results, and stop rules without committing generated audio.
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOG_JSONL = REPO_ROOT / "docs/speaker-notes/breezyvoice/cde-2026-breezyvoice-tts-experiment-log-v1.jsonl"
LOG_MD = REPO_ROOT / "docs/speaker-notes/breezyvoice/cde-2026-breezyvoice-tts-experiment-log-v1.md"

FIELD_ORDER = [
    "experiment_id",
    "timestamp",
    "stage",
    "title",
    "reason",
    "hypothesis",
    "input_version",
    "source_sha256",
    "affected_prefixes",
    "change_summary",
    "commands",
    "logs",
    "outputs",
    "machine_result",
    "human_result",
    "decision",
    "fix_applied",
    "downloads_package",
    "stop_rule",
    "next_action",
    "additional_observations",
]


def split_list(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(";;") if item.strip()]


def load_records() -> list[dict[str, object]]:
    if not LOG_JSONL.exists():
        return []
    records = []
    for line in LOG_JSONL.read_text(encoding="utf-8").splitlines():
        if line.strip():
            records.append(json.loads(line))
    return records


def write_records(records: list[dict[str, object]]) -> None:
    LOG_JSONL.parent.mkdir(parents=True, exist_ok=True)
    with LOG_JSONL.open("w", encoding="utf-8") as fh:
        for record in records:
            fh.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")
    LOG_MD.write_text(render_markdown(records), encoding="utf-8")


def render_list(items: object) -> str:
    if not items:
        return "- none recorded"
    if isinstance(items, list):
        return "\n".join(f"- {item}" for item in items)
    return f"- {items}"


def render_markdown(records: list[dict[str, object]]) -> str:
    lines = [
        "# CDE 2026 BreezyVoice TTS Experiment Log V1",
        "",
        "This is the durable tracked log for every CDE 2026 BreezyVoice TTS",
        "experiment, text-conditioning pass, render attempt, stitch pass, ASR",
        "check, expert-review package, and human-review gate.",
        "",
        "Generated audio, raw runtime caches, prompt WAVs, and large local review",
        "packages remain under `.local/` or `~/Downloads/`; this tracked log keeps",
        "the traceable decision record and local evidence paths.",
        "",
        "## Logging Contract",
        "",
        "- Create or update one experiment record before any new TTS render or",
        "  model-facing text-conditioning pass.",
        "- Record the reason, expected effect, affected prefixes/subclips, exact",
        "  commands, log paths, output paths, machine results, human results, fix",
        "  applied, and next stop rule.",
        "- If human review is required, export a package to `~/Downloads`, record",
        "  both the directory and archive path, and stop before full render until",
        "  human decisions are returned.",
        "- Keep `full_batch_allowed=false` whenever any required pilot parent chunk",
        "  is missing, rejected, undecided, or machine status says",
        "  `needs_human_listening`.",
        "- Do not use stale WAV files that are not listed in the current manifest;",
        "  treat orphan audio as a review-hygiene risk.",
        "",
        "## Current Gate",
        "",
        "- Source version: `v1`",
        "- Current state: determined by the latest experiment record and",
        "  `.local/breezyvoice/review/v1/full_batch_gate.json`.",
        "- Current owner policy: after final7 human-review repairs, the owner",
        "  allowed proceeding to the next concrete step without another listening",
        "  review round, while preserving the returned review history.",
        "- Current auxiliary ASR policy: use `MediaTek-Research/Breeze-ASR-25`",
        "  only; do not use Whisper for current BreezyVoice review gates.",
        "- Generated audio, ASR, telemetry, and review packages remain local-only",
        "  unless explicitly exported.",
        "",
        "## Experiment Index",
        "",
        "| ID | Stage | Title | Decision | Next action |",
        "| --- | --- | --- | --- | --- |",
    ]
    for record in records:
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{record['experiment_id']}`",
                    str(record.get("stage", "")),
                    str(record.get("title", "")).replace("|", "/"),
                    str(record.get("decision", "")).replace("|", "/"),
                    str(record.get("next_action", "")).replace("|", "/"),
                ]
            )
            + " |"
        )
    lines.extend(["", "## Detailed Records", ""])
    for record in records:
        lines.extend(
            [
                f"### {record['experiment_id']} - {record.get('title', '')}",
                "",
                f"- Timestamp: `{record.get('timestamp', '')}`",
                f"- Stage: `{record.get('stage', '')}`",
                f"- Input version: `{record.get('input_version', '')}`",
                f"- Source SHA-256: `{record.get('source_sha256', '')}`",
                f"- Affected prefixes: `{', '.join(record.get('affected_prefixes', []))}`",
                "",
                "Reason:",
                "",
                render_list(record.get("reason")),
                "",
                "Hypothesis:",
                "",
                render_list(record.get("hypothesis")),
                "",
                "Change summary:",
                "",
                render_list(record.get("change_summary")),
                "",
                "Commands:",
                "",
                render_list(record.get("commands")),
                "",
                "Logs:",
                "",
                render_list(record.get("logs")),
                "",
                "Outputs:",
                "",
                render_list(record.get("outputs")),
                "",
                "Machine result:",
                "",
                render_list(record.get("machine_result")),
                "",
                "Human result:",
                "",
                render_list(record.get("human_result")),
                "",
                f"Decision: `{record.get('decision', '')}`",
                "",
                "Fix applied:",
                "",
                render_list(record.get("fix_applied")),
                "",
                "Downloads package:",
                "",
                render_list(record.get("downloads_package")),
                "",
                "Stop rule:",
                "",
                render_list(record.get("stop_rule")),
                "",
                "Next action:",
                "",
                render_list(record.get("next_action")),
                "",
                "Additional observations:",
                "",
                render_list(record.get("additional_observations")),
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Record a BreezyVoice TTS experiment.")
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--stage", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--reason", default="")
    parser.add_argument("--hypothesis", default="")
    parser.add_argument("--input-version", default="v1")
    parser.add_argument("--source-sha256", default="")
    parser.add_argument("--affected-prefixes", default="")
    parser.add_argument("--change-summary", default="")
    parser.add_argument("--commands", default="")
    parser.add_argument("--logs", default="")
    parser.add_argument("--outputs", default="")
    parser.add_argument("--machine-result", default="")
    parser.add_argument("--human-result", default="")
    parser.add_argument("--decision", required=True)
    parser.add_argument("--fix-applied", default="")
    parser.add_argument("--downloads-package", default="")
    parser.add_argument("--stop-rule", default="")
    parser.add_argument("--next-action", default="")
    parser.add_argument("--additional-observations", default="")
    parser.add_argument("--timestamp", default=datetime.now(timezone.utc).isoformat())
    parser.add_argument("--replace", action="store_true")
    args = parser.parse_args()

    records = load_records()
    existing_ids = {str(record["experiment_id"]) for record in records}
    if args.experiment_id in existing_ids and not args.replace:
        raise SystemExit(f"Experiment already exists; pass --replace: {args.experiment_id}")
    records = [record for record in records if record["experiment_id"] != args.experiment_id]

    record = {
        "experiment_id": args.experiment_id,
        "timestamp": args.timestamp,
        "stage": args.stage,
        "title": args.title,
        "reason": split_list(args.reason),
        "hypothesis": split_list(args.hypothesis),
        "input_version": args.input_version,
        "source_sha256": args.source_sha256,
        "affected_prefixes": split_list(args.affected_prefixes),
        "change_summary": split_list(args.change_summary),
        "commands": split_list(args.commands),
        "logs": split_list(args.logs),
        "outputs": split_list(args.outputs),
        "machine_result": split_list(args.machine_result),
        "human_result": split_list(args.human_result),
        "decision": args.decision,
        "fix_applied": split_list(args.fix_applied),
        "downloads_package": split_list(args.downloads_package),
        "stop_rule": split_list(args.stop_rule),
        "next_action": args.next_action,
        "additional_observations": split_list(args.additional_observations),
    }
    ordered_record = {key: record[key] for key in FIELD_ORDER}
    records.append(ordered_record)
    records.sort(key=lambda item: (str(item["timestamp"]), str(item["experiment_id"])))
    write_records(records)
    print(json.dumps({"recorded": args.experiment_id, "records": len(records)}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
