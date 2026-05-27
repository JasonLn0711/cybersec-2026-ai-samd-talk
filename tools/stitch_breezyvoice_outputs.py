#!/usr/bin/env python3
"""Stitch BreezyVoice subclip WAV files into parent chunks and full lecture WAVs."""

from __future__ import annotations

import argparse
import csv
import json
import wave
from collections import defaultdict
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
DEFAULT_VERSION = "v1"


def repo_relative(path: str | Path) -> Path:
    value = Path(path)
    if value.is_absolute():
        return value
    return REPO_ROOT / value


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def wav_info(path: Path) -> dict[str, object]:
    with wave.open(str(path), "rb") as wav:
        return {
            "channels": wav.getnchannels(),
            "sample_width": wav.getsampwidth(),
            "sample_rate": wav.getframerate(),
            "frames": wav.getnframes(),
            "duration_seconds": wav.getnframes() / float(wav.getframerate()),
            "params": wav.getparams(),
        }


def silence_frames(channels: int, sample_width: int, sample_rate: int, silence_ms: int) -> bytes:
    frame_count = int(sample_rate * silence_ms / 1000)
    return b"\x00" * frame_count * channels * sample_width


def stitch_wavs(input_paths: list[Path], output_path: Path, silence_ms: int) -> dict[str, object]:
    if not input_paths:
        raise ValueError(f"No input WAV files for {output_path}")
    missing = [path for path in input_paths if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing input WAVs: " + ", ".join(display_path(path) for path in missing))

    first_info = wav_info(input_paths[0])
    params = first_info["params"]
    total_input_duration = 0.0
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with wave.open(str(output_path), "wb") as out_wav:
        out_wav.setparams(params)
        for index, input_path in enumerate(input_paths):
            info = wav_info(input_path)
            if info["params"][:3] != params[:3]:
                raise ValueError(
                    f"WAV format mismatch for {display_path(input_path)}: "
                    f"{info['params'][:3]} != {params[:3]}"
                )
            with wave.open(str(input_path), "rb") as in_wav:
                out_wav.writeframes(in_wav.readframes(in_wav.getnframes()))
            total_input_duration += float(info["duration_seconds"])
            if silence_ms and index < len(input_paths) - 1:
                out_wav.writeframes(
                    silence_frames(
                        int(info["channels"]),
                        int(info["sample_width"]),
                        int(info["sample_rate"]),
                        silence_ms,
                    )
                )

    output_info = wav_info(output_path)
    return {
        "output_wav": display_path(output_path),
        "input_count": len(input_paths),
        "input_duration_seconds": round(total_input_duration, 2),
        "output_duration_seconds": round(float(output_info["duration_seconds"]), 2),
        "sample_rate": output_info["sample_rate"],
        "channels": output_info["channels"],
        "silence_ms_between_inputs": silence_ms,
    }


def selected_parent_prefixes(selection: str, pilot_manifest: Path, render_manifest: Path) -> list[str]:
    manifest = pilot_manifest if selection == "pilot" else render_manifest
    id_field = "output_prefix"
    return [row[id_field] for row in read_csv(manifest)]


def group_subclips(subclip_manifest: Path, prefixes: set[str]) -> dict[str, list[dict[str, str]]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in read_csv(subclip_manifest):
        if row["parent_output_prefix"] in prefixes:
            grouped[row["parent_output_prefix"]].append(row)
    for rows in grouped.values():
        rows.sort(key=lambda row: int(row["subclip_index"]))
    return dict(grouped)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Stitch local BreezyVoice WAV outputs.")
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--selection", choices=["pilot", "all"], default="pilot")
    parser.add_argument("--stitch-full", action="store_true", help="Also stitch selected parent chunks into one combined WAV.")
    parser.add_argument("--silence-ms", type=int, default=350, help="Silence inserted between stitched WAVs.")
    parser.add_argument("--subclip-manifest", default="")
    parser.add_argument("--pilot-manifest", default="")
    parser.add_argument("--render-manifest", default="")
    parser.add_argument("--full-output", default="", help="Optional full stitched output WAV path.")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    subclip_manifest = repo_relative(args.subclip_manifest) if args.subclip_manifest else LOCAL_ROOT / f"manifests/{args.version}/subclip_manifest.csv"
    pilot_manifest = repo_relative(args.pilot_manifest) if args.pilot_manifest else LOCAL_ROOT / f"manifests/{args.version}/pilot_manifest.csv"
    render_manifest = repo_relative(args.render_manifest) if args.render_manifest else LOCAL_ROOT / f"manifests/{args.version}/render_manifest.csv"

    prefixes = selected_parent_prefixes(args.selection, pilot_manifest, render_manifest)
    grouped = group_subclips(subclip_manifest, set(prefixes))
    parent_inventory: list[dict[str, object]] = []
    parent_paths: list[Path] = []

    for prefix in prefixes:
        rows = grouped.get(prefix, [])
        if not rows:
            raise SystemExit(f"No subclip rows for parent prefix: {prefix}")
        input_paths = [repo_relative(row["planned_output_wav"]) for row in rows]
        output_path = repo_relative(rows[0]["parent_output_wav"])
        if output_path.exists() and not args.overwrite:
            info = wav_info(output_path)
            result = {
                "output_wav": display_path(output_path),
                "input_count": len(input_paths),
                "input_duration_seconds": "",
                "output_duration_seconds": round(float(info["duration_seconds"]), 2),
                "sample_rate": info["sample_rate"],
                "channels": info["channels"],
                "silence_ms_between_inputs": args.silence_ms,
                "status": "skipped_exists",
            }
        else:
            result = stitch_wavs(input_paths, output_path, args.silence_ms)
            result["status"] = "stitched"
        result["parent_output_prefix"] = prefix
        parent_inventory.append(result)
        parent_paths.append(output_path)
        print(f"{result['status']}: {prefix} -> {result['output_wav']}")

    inventory_path = LOCAL_ROOT / f"review/{args.version}/{args.selection}_parent_stitch_inventory.csv"
    write_csv(
        inventory_path,
        parent_inventory,
        [
            "parent_output_prefix",
            "output_wav",
            "input_count",
            "input_duration_seconds",
            "output_duration_seconds",
            "sample_rate",
            "channels",
            "silence_ms_between_inputs",
            "status",
        ],
    )

    summary = {
        "version": args.version,
        "selection": args.selection,
        "parent_count": len(parent_inventory),
        "inventory": display_path(inventory_path),
        "silence_ms_between_inputs": args.silence_ms,
        "parents": parent_inventory,
    }

    if args.stitch_full:
        if args.full_output:
            full_output = repo_relative(args.full_output)
        elif args.selection == "all":
            full_output = LOCAL_ROOT / f"output/{args.version}/full/cde-2026-breezyvoice-80min-v1.wav"
        else:
            full_output = LOCAL_ROOT / f"output/{args.version}/full/cde-2026-breezyvoice-{args.selection}-stitched-v1.wav"
        full_result = stitch_wavs(parent_paths, full_output, args.silence_ms)
        summary["full_stitch"] = full_result
        print(f"stitched_full: {full_result['output_wav']}")

    summary_path = LOCAL_ROOT / f"review/{args.version}/{args.selection}_stitch_summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"summary: {display_path(summary_path)}")


if __name__ == "__main__":
    main()
