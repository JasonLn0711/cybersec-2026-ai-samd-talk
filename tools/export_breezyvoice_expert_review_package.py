#!/usr/bin/env python3
"""Export a local BreezyVoice pilot review package for human TTS experts.

The package is intentionally written outside git-tracked paths by default.
It copies only the current pilot audio, traceability text, manifests, review
gates, and expert-facing instructions needed before the full render gate.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import tarfile
import wave
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
VERSION = "v1"
DEFAULT_OUTPUT_DIR = Path.home() / "Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28"

REVIEW_FILES = [
    "pilot_listening_review.md",
    "pilot_listening_review.csv",
    "pilot_review_checklist.md",
    "full_render_acceptance_gate.md",
    "full_batch_gate.json",
    "pilot_machine_review.md",
    "pilot_machine_review.json",
    "pilot_stitch_summary.json",
    "pilot_parent_stitch_inventory.csv",
    "pilot_audio_inventory.csv",
    "pilot_status.json",
    "render_review_log.csv",
    "pilot_correction_matrix.csv",
    "pilot_correction_matrix.md",
    "pilot_correction_matrix.json",
    "orphan_input_inventory.csv",
    "orphan_audio_inventory.csv",
    "full_render_gate_check.json",
    "objective_verification.json",
]

EXPERIMENT_LOG_FILES = [
    REPO_ROOT / "docs/speaker-notes/breezyvoice/cde-2026-breezyvoice-tts-experiment-log-v1.md",
    REPO_ROOT / "docs/speaker-notes/breezyvoice/cde-2026-breezyvoice-tts-experiment-log-v1.jsonl",
    REPO_ROOT / "docs/speaker-notes/breezyvoice/cde-2026-breezyvoice-reference-audio-telemetry-2026-05-28.md",
]

MANIFEST_FILES = [
    "render_manifest.csv",
    "render_manifest.jsonl",
    "subclip_manifest.csv",
    "subclip_manifest.jsonl",
    "pilot_manifest.csv",
    "pilot_manifest.jsonl",
    "package_summary.json",
]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def rel(path: Path, base: Path = REPO_ROOT) -> str:
    return str(path.relative_to(base))


def copy_file(src: Path, dst: Path) -> None:
    if not src.exists():
        raise FileNotFoundError(src)
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / float(wav.getframerate())


def load_state() -> tuple[dict[str, object], dict[str, object], dict[str, object], list[dict[str, str]]]:
    summary = json.loads((LOCAL_ROOT / f"manifests/{VERSION}/package_summary.json").read_text(encoding="utf-8"))
    gate = json.loads((LOCAL_ROOT / f"review/{VERSION}/full_batch_gate.json").read_text(encoding="utf-8"))
    machine = json.loads((LOCAL_ROOT / f"review/{VERSION}/pilot_machine_review.json").read_text(encoding="utf-8"))
    review_rows = read_csv(LOCAL_ROOT / f"review/{VERSION}/pilot_listening_review.csv")
    return summary, gate, machine, refresh_review_rows(review_rows)


def review_subclip_counts() -> dict[str, int]:
    pilot_rows = read_csv(LOCAL_ROOT / f"manifests/{VERSION}/pilot_manifest.csv")
    pilot_prefixes = {row["output_prefix"] for row in pilot_rows}
    counts = {prefix: 0 for prefix in pilot_prefixes}
    for row in read_csv(LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.csv"):
        prefix = row["parent_output_prefix"]
        if prefix in counts:
            counts[prefix] += 1
    return counts


def refresh_review_rows(review_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    counts = review_subclip_counts()
    refreshed: list[dict[str, str]] = []
    for row in review_rows:
        current = dict(row)
        prefix = current["output_prefix"]
        if prefix in counts:
            current["subclip_count"] = str(counts[prefix])
        refreshed.append(current)
    return refreshed


def package_path_from_repo_value(value: str, package: Path, kind: str) -> Path:
    name = Path(value).name
    if kind == "parent_audio":
        return package / "audio/parent_chunks" / name
    if kind == "normalized_text":
        return package / "text/normalized_segments" / name
    raise ValueError(kind)


def copy_package_inputs(package: Path, review_rows: list[dict[str, str]]) -> None:
    full_wav = LOCAL_ROOT / f"output/{VERSION}/full/cde-2026-breezyvoice-pilot-stitched-v1.wav"
    copy_file(full_wav, package / "audio/full" / full_wav.name)
    subclip_rows = read_csv(LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.csv")
    subclips_by_parent: dict[str, list[dict[str, str]]] = {}
    for row in subclip_rows:
        subclips_by_parent.setdefault(row["parent_output_prefix"], []).append(row)
    for rows in subclips_by_parent.values():
        rows.sort(key=lambda item: int(item["subclip_index"]))

    for row in review_rows:
        prefix = row["output_prefix"]
        copy_file(REPO_ROOT / row["parent_wav"], package / "audio/parent_chunks" / Path(row["parent_wav"]).name)
        copy_file(REPO_ROOT / row["normalized_text_path"], package / "text/normalized_segments" / Path(row["normalized_text_path"]).name)
        clean_text = LOCAL_ROOT / f"inputs/{VERSION}/segments/{prefix}.txt"
        copy_file(clean_text, package / "text/segments" / clean_text.name)
        for subclip in subclips_by_parent.get(prefix, []):
            wav_path = REPO_ROOT / subclip["planned_output_wav"]
            text_path = REPO_ROOT / subclip["clean_text_path"]
            copy_file(wav_path, package / "audio/subclips" / wav_path.name)
            copy_file(text_path, package / "text/subclips" / text_path.name)

    review_dir = LOCAL_ROOT / f"review/{VERSION}"
    for filename in REVIEW_FILES:
        copy_file(review_dir / filename, package / "review" / filename)

    for path in EXPERIMENT_LOG_FILES:
        if path.exists():
            copy_file(path, package / "review/experiment_log" / path.name)

    asr_dir = review_dir / "asr"
    copy_file(asr_dir / "cde-2026-breezyvoice-pilot-stitched-v1.txt", package / "review/asr/cde-2026-breezyvoice-pilot-stitched-v1.txt")
    for log_name in [
        "breeze_asr25_after_mixed_gate_repair_final7.log",
        "breeze_asr25_after_mixed_gate_repair_final7.json",
        "breeze_asr25_after_mixed_gate_repair_final7_timestamped.txt",
    ]:
        log_path = asr_dir / log_name
        if log_path.exists():
            copy_file(log_path, package / "review/asr" / log_name)

    runtime_dir = LOCAL_ROOT / f"runtime/{VERSION}"
    for log_name in [
        "pilot_reference_after_mixed_gate_repair_final7.log",
        "tail_trim_20260528-mixed-gate-final7.log",
        "last_render_plan.csv",
    ]:
        log_path = runtime_dir / log_name
        if log_path.exists():
            copy_file(log_path, package / "review/runtime" / log_name)
    telemetry_dir = runtime_dir / "telemetry"
    for telemetry_name in [
        "pilot_reference_after_mixed_gate_repair_final7_summary.json",
        "pilot_reference_after_mixed_gate_repair_final7_gpu.jsonl",
    ]:
        telemetry_path = telemetry_dir / telemetry_name
        if telemetry_path.exists():
            copy_file(telemetry_path, package / "review/runtime/telemetry" / telemetry_name)

    manifest_dir = LOCAL_ROOT / f"manifests/{VERSION}"
    for filename in MANIFEST_FILES:
        copy_file(manifest_dir / filename, package / "manifests" / filename)

    copy_file(
        LOCAL_ROOT / f"inputs/{VERSION}/pronunciation_override_policy.md",
        package / "reference/pronunciation_override_policy.md",
    )
    copy_file(
        REPO_ROOT / "docs/speaker-notes/breezyvoice/model-ready/cde-2026-breezyvoice-pronunciation-notes.md",
        package / "reference/cde-2026-breezyvoice-pronunciation-notes.md",
    )


def expert_rows(package: Path, review_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for row in review_rows:
        parent_audio = package_path_from_repo_value(row["parent_wav"], package, "parent_audio")
        normalized_text = package_path_from_repo_value(row["normalized_text_path"], package, "normalized_text")
        rows.append(
            {
                "output_prefix": row["output_prefix"],
                "package_audio_path": rel(parent_audio, package),
                "subclip_count": row["subclip_count"],
                "runtime_seconds": f"{wav_duration(parent_audio):.2f}",
                "target_seconds": row["target_seconds"],
                "runtime_to_target_ratio": row["runtime_to_target_ratio"],
                "review_status": row["review_status"],
                "normalized_text_path": rel(normalized_text, package),
                "expert_check_acronyms": "",
                "expert_check_key_terms": "",
                "expert_check_pacing": "",
                "expert_check_fatigue": "",
                "expert_check_opening_handoff_close": "",
                "expert_check_no_markup_spoken": "",
                "decision_accept_or_reject": "",
                "pronunciation_issue": "",
                "fix_recommendation": "",
                "notes": "",
            }
        )
    return rows


def write_expert_form(package: Path, rows: list[dict[str, object]]) -> None:
    write_csv(package / "forms/expert_pilot_review_form.csv", rows, list(rows[0].keys()))


def write_playlist(package: Path, rows: list[dict[str, object]]) -> None:
    full = package / "audio/full/cde-2026-breezyvoice-pilot-stitched-v1.wav"
    lines = [
        "#EXTM3U",
        "# Combined pilot first",
        f"#EXTINF:{int(wav_duration(full))},cde-2026-breezyvoice-pilot-stitched-v1",
        "audio/full/cde-2026-breezyvoice-pilot-stitched-v1.wav",
        "",
    ]
    for row in rows:
        lines.append(f"#EXTINF:{int(float(str(row['runtime_seconds'])))},{row['output_prefix']}")
        lines.append(str(row["package_audio_path"]))
    write_text(package / "review/package_relative_playlist.m3u", "\n".join(lines))


def expert_prompt(summary: dict[str, object], pilot_subclip_count: int) -> str:
    return f"""# Prompt For TTS Expert

請協助審查這份 CDE 2026 BreezyVoice pilot TTS 音檔包。目標不是重寫講稿，而是在進入完整 80 分鐘 full render 前，判斷目前四段 pilot 音檔是否已經達到可接受品質，或指出最小必要修正。

## 背景

這是 80 分鐘醫療資安課程的 BreezyVoice TTS pilot review package。完整工程稿已凍結為 v1 source：

- {summary['segments']} 個 chunks
- 80:00 timing plan
- 約 {summary['model_text_characters']} model-text characters
- {summary['subclips']} 個 planned full-render subclips
- 本次 pilot 有 {pilot_subclip_count} 個 subclips
- 本次 pilot 使用 {summary['pilot_execution_mode']}
- full render 目前尚未開放；本包保留已接受的 `cde_full_26`，其餘三段必須等人工聽審通過

請先閱讀：

1. `README_FOR_TTS_EXPERT.md`
2. `review/pilot_listening_review.md`
3. `review/experiment_log/cde-2026-breezyvoice-tts-experiment-log-v1.md`
4. `review/pilot_correction_matrix.md`
5. `forms/expert_pilot_review_form.csv`

## 請優先聽的音檔

請先聽整體連續感：

- `audio/full/cde-2026-breezyvoice-pilot-stitched-v1.wav`

接著逐段審查這四個 parent chunk，這四段是正式 gate decision unit。`cde_full_26` 已由上一輪人工審查標記為接受並保留原音檔，仍放入本包供整體連續感比對；請優先審查其餘三段修正版：

- `audio/parent_chunks/cde_full_01_opening_positioning_crazyhunter_entry_case.wav`
- `audio/parent_chunks/cde_full_16_k8s_review_controls.wav`
- `audio/parent_chunks/cde_full_20_crowdstrike_update_524b.wav`
- `audio/parent_chunks/cde_full_26_shared_close_test_anchors.wav`

如果某段有問題，再用 `audio/subclips/` 內的對應 p01, p02, p03, p04 小段定位問題。

## 審查重點

請針對每個 parent chunk 判斷：

1. 英文縮寫是否可懂且沒有嚴重連讀或亂唸：
   - C D E
   - A I
   - P A C S
   - H I S
   - E M R
   - F D A
   - T F D A
   - S B O M

2. 關鍵術語是否穩定：
   - K 八 S / K8S
   - F D C Act，Section 五二四，英文字母 B 款
   - Channel File 二九一
   - Log four Shell
   - 白箱測試 / 白箱驗證
   - 派克斯停機時間 / 臨床連續性 / evidence chain

3. 語速與 pacing：
   - 是否像 80 分鐘講課，而不是太趕的逐字稿朗讀？
   - 特別注意 `cde_full_16_k8s_review_controls`：前一輪人工審查曾指出 runtime ratio 約 0.73 與語速壓縮；本包已套用更細 subclip 與 post-synthesis pacing override，請以目前音檔實聽結果判斷是否已修復。

4. 長句聽感：
   - 是否疲勞？
   - 是否有明顯喘不過氣、斷句不自然、資訊密度太高的地方？

5. 開場、技術段與結尾：
   - 開場是否穩定可信？
   - K8S / CrowdStrike / 524B 這類技術段是否仍可懂？
   - 結尾是否有 CDE 講課需要的收束感與權威感？

6. 控制標籤安全：
   - 是否聽到 BV26、Markdown、註解、括號、奇怪符號、檔名或其他不應被念出的內容？

## 請回填的檔案

請回填：

- `forms/expert_pilot_review_form.csv`

每一列代表一個 parent chunk。請在 `decision_accept_or_reject` 填：

- `accept`：此段可進入 full render gate
- `reject`：此段需要修正後重跑

如果填 `reject`，請補：

- `pronunciation_issue`：實際聽到的問題
- `fix_recommendation`：建議的最小修正
- `notes`：時間點、subclip filename、或精確問題片語

## 修正建議請依照這個優先順序

請不要直接大改全文。若要修，請優先建議最小改動：

1. 標點與斷句
2. 英文詞 spacing
3. 單一術語替換
4. subclip 切更短
5. 單段 preset / pause 調整
6. 最後才建議改口播內容

## 重要判斷原則

這份 ASR transcript 由 Breeze-ASR-25 產生，只能當輔助，不能當主要判斷依據。請以實際聽感為準。

通過標準是：

- 可懂
- 穩定
- 沒有控制標籤誤讀
- 專有名詞可接受
- 段落不疲勞
- 語氣符合 CDE 醫療資安講課

只要四段 parent chunk 都維持或取得人工審查 `accept`，才會進入完整 80 分鐘 full render。"""


def readme(
    summary: dict[str, object],
    gate: dict[str, object],
    rows: list[dict[str, object]],
    pilot_subclip_count: int,
) -> str:
    table = "\n".join(
        [
            "| Output prefix | Audio | Runtime | Target | Ratio | Current status |",
            "| --- | --- | ---: | ---: | ---: | --- |",
            *[
                f"| `{row['output_prefix']}` | `{row['package_audio_path']}` | {row['runtime_seconds']} | {row['target_seconds']} | {row['runtime_to_target_ratio']} | {row['review_status']} |"
                for row in rows
            ],
        ]
    )
    return f"""# CDE 2026 BreezyVoice Pilot Human Review Package

Prepared for human listening review before any full 80-minute BreezyVoice render. The current gate intentionally keeps full rendering closed until all four pilot parent chunks are accepted by listening.

## Current Machine State

- Source version: v1 80-minute engineering source
- Frozen chunks: {summary['segments']}
- Full planned timing: {summary['duration_seconds']} seconds / 80:00
- Model text characters: {summary['model_text_characters']}
- Planned full subclips: {summary['subclips']}
- Pilot parent chunks: {summary['pilot_segments']}
- Reference audio required: {summary['reference_audio_required']}
- Pilot execution mode: {summary['pilot_execution_mode']}
- Full batch allowed now: {gate['full_batch_allowed']}
- Machine review status: {gate['machine_review_status']}

Important: ASR is generated with Breeze-ASR-25 and is only an auxiliary signal. Judge by listening to the WAV files.

## What To Listen To First

1. `audio/full/cde-2026-breezyvoice-pilot-stitched-v1.wav`
2. The four parent chunks in `audio/parent_chunks/`
3. The {pilot_subclip_count} files in `audio/subclips/` only when a parent chunk needs defect localization

## Required Parent-Chunk Decisions

{table}

Special attention:

- The latest returned human review accepted `cde_full_16_k8s_review_controls`; that audio is preserved and included as the accepted continuity baseline.
- `cde_full_01_opening_positioning_crazyhunter_entry_case`, `cde_full_20_crowdstrike_update_524b`, and `cde_full_26_shared_close_test_anchors` were repaired and rerendered for this package after the mixed gate review.
- The model-facing Chinese white-box terminology is standardized as `白箱`. Listen especially for `白箱測試`, `白箱驗證`, `白箱證據`, and `白箱審查`.
- `cde_full_16_k8s_review_controls` was previously rejected for runtime compression around 0.73 and is currently accepted by human review; use the current WAV and current review CSV rather than older ASR or runtime logs.
- The model-facing text now removes low-confidence fillers such as `這個`, `那個`, `嗯`, `呃`, explicit breath cues, and known hallucination residues before synthesis. Small confident natural vocalization is acceptable; hesitant filler delivery is not.
- The ASR machine check uses Breeze-ASR-25 only. It is an auxiliary signal and can still miss or distort technical terms.

## How To Fill The Review

Fill `forms/expert_pilot_review_form.csv`.

For context on why the current pilot exists and what was already changed, read
`review/experiment_log/cde-2026-breezyvoice-tts-experiment-log-v1.md`. That log
is the authority for previous render attempts, text-conditioning rationale,
machine results, expert feedback, and current stop rules.

For chunk-level repair traceability, read `review/pilot_correction_matrix.md`.
It maps each expert issue to the model-facing conditioning already applied and
the exact listening question that still needs human judgement.

Use `decision_accept_or_reject` values:

- `accept`: usable for full-batch gate
- `reject`: needs a small repair before full render

If rejected, fill `pronunciation_issue`, `fix_recommendation`, and `notes`.

Full render should remain blocked until all four required parent chunks are accepted by human listening.

The package also includes `review/orphan_audio_inventory.csv`. Those WAVs, if
listed, are local artifact-hygiene warnings only and should not be reviewed as
current pilot deliverables unless they also appear in `manifests/subclip_manifest.csv`.

After the form is returned, the local maintainer should ingest it with:

```bash
python3 tools/ingest_breezyvoice_expert_review.py --input /path/to/expert_pilot_review_form.csv
```

The ingester requires explicit `accept` or `reject` values for all four parent
chunks before it updates the full-render gate.
"""


def write_package_summary(package: Path, gate: dict[str, object], summary: dict[str, object], rows: list[dict[str, object]]) -> None:
    payload = {
        "package": str(package),
        "created_for": "CDE 2026 BreezyVoice pilot human review",
        "required_review_units": [row["output_prefix"] for row in rows],
        "full_pilot_audio": "audio/full/cde-2026-breezyvoice-pilot-stitched-v1.wav",
        "expert_prompt": "PROMPT_FOR_TTS_EXPERT.md",
        "expert_form": "forms/expert_pilot_review_form.csv",
        "experiment_log": "review/experiment_log/cde-2026-breezyvoice-tts-experiment-log-v1.md",
        "full_batch_allowed_before_review": gate["full_batch_allowed"],
        "reference_audio_required": summary["reference_audio_required"],
        "pilot_execution_mode": summary["pilot_execution_mode"],
    }
    (package / "PACKAGE_SUMMARY.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def create_archive(package: Path) -> Path:
    archive_path = package.with_suffix(".tar.gz")
    if archive_path.exists():
        archive_path.unlink()
    with tarfile.open(archive_path, "w:gz") as tar:
        tar.add(package, arcname=package.name)
    return archive_path


def validate_package(package: Path, review_rows: list[dict[str, object]]) -> dict[str, object]:
    expected_subclips = sum(int(str(row["subclip_count"])) for row in review_rows)
    counts = {
        "full_wavs": len(list((package / "audio/full").glob("*.wav"))),
        "parent_wavs": len(list((package / "audio/parent_chunks").glob("*.wav"))),
        "subclip_wavs": len(list((package / "audio/subclips").glob("*.wav"))),
        "normalized_segment_txt": len(list((package / "text/normalized_segments").glob("*.txt"))),
        "subclip_txt": len(list((package / "text/subclips").glob("*.txt"))),
        "expert_prompt_exists": (package / "PROMPT_FOR_TTS_EXPERT.md").exists(),
        "expert_readme_exists": (package / "README_FOR_TTS_EXPERT.md").exists(),
        "expert_form_exists": (package / "forms/expert_pilot_review_form.csv").exists(),
    }
    expected = {
        "full_wavs": 1,
        "parent_wavs": 4,
        "subclip_wavs": expected_subclips,
        "normalized_segment_txt": 4,
        "subclip_txt": expected_subclips,
        "expert_prompt_exists": True,
        "expert_readme_exists": True,
        "expert_form_exists": True,
    }
    failures = {key: (counts[key], value) for key, value in expected.items() if counts[key] != value}
    if failures:
        raise RuntimeError(f"Package validation failed: {failures}")
    return counts


def main() -> None:
    parser = argparse.ArgumentParser(description="Export BreezyVoice pilot audio and review files for expert listening.")
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--no-archive", action="store_true")
    args = parser.parse_args()

    package = args.output_dir.expanduser().resolve()
    if package.exists():
        if not args.overwrite:
            raise SystemExit(f"Output directory exists; pass --overwrite: {package}")
        shutil.rmtree(package)
    package.mkdir(parents=True)

    summary, gate, _machine, review_rows = load_state()
    copy_package_inputs(package, review_rows)
    rows = expert_rows(package, review_rows)
    pilot_subclip_count = sum(int(str(row["subclip_count"])) for row in rows)
    write_expert_form(package, rows)
    write_playlist(package, rows)
    write_text(package / "PROMPT_FOR_TTS_EXPERT.md", expert_prompt(summary, pilot_subclip_count))
    write_text(package / "README_FOR_TTS_EXPERT.md", readme(summary, gate, rows, pilot_subclip_count))
    write_package_summary(package, gate, summary, rows)
    counts = validate_package(package, rows)
    archive = None if args.no_archive else create_archive(package)

    print(
        json.dumps(
            {
                "package": str(package),
                "archive": str(archive) if archive else "",
                "counts": counts,
                "full_batch_allowed": gate["full_batch_allowed"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
