#!/usr/bin/env python3
"""Trim a fixed tail duration from selected local BreezyVoice WAV outputs."""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
import wave
from datetime import datetime
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
VERSION = "v1"


def repo_path(value: str) -> Path:
    path = Path(value)
    return path if path.is_absolute() else REPO_ROOT / path


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))


def wav_duration(path: Path) -> float:
    with wave.open(str(path), "rb") as wav:
        return wav.getnframes() / float(wav.getframerate())


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def main() -> int:
    parser = argparse.ArgumentParser(description="Trim tail audio from selected BreezyVoice subclip WAVs.")
    parser.add_argument("--subclip-id", action="append", required=True)
    parser.add_argument("--tail-seconds", type=float, required=True)
    parser.add_argument("--manifest", type=Path, default=LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.csv")
    parser.add_argument("--label", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    if args.tail_seconds <= 0:
        raise SystemExit("--tail-seconds must be positive")

    rows = {row["subclip_id"]: row for row in read_csv(args.manifest)}
    archive_dir = LOCAL_ROOT / f"output/{VERSION}/archive/tail-before-{args.label}"
    archive_dir.mkdir(parents=True, exist_ok=True)
    changed = []
    for subclip_id in args.subclip_id:
        if subclip_id not in rows:
            raise SystemExit(f"Unknown subclip id: {subclip_id}")
        wav = repo_path(rows[subclip_id]["planned_output_wav"])
        if not wav.exists():
            raise FileNotFoundError(wav)
        original_duration = wav_duration(wav)
        keep_duration = original_duration - args.tail_seconds
        if keep_duration <= 1:
            raise SystemExit(f"Refusing to trim {args.tail_seconds}s from {subclip_id}; duration={original_duration:.3f}s")

        original = archive_dir / wav.name
        if original.exists() and not args.overwrite:
            raise SystemExit(f"Archived WAV already exists; pass --overwrite: {original}")
        shutil.copy2(wav, original)
        tmp = wav.with_suffix(".trim.wav")
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(original),
                "-t",
                f"{keep_duration:.3f}",
                str(tmp),
            ],
            check=True,
        )
        tmp.replace(wav)
        changed.append(
            {
                "subclip_id": subclip_id,
                "wav": rel(wav),
                "archived_original": rel(original),
                "original_duration": f"{original_duration:.3f}",
                "trimmed_tail_seconds": f"{args.tail_seconds:.3f}",
                "new_duration": f"{wav_duration(wav):.3f}",
            }
        )

    print({"trimmed": len(changed), "tail_seconds": args.tail_seconds, "archive_dir": rel(archive_dir)})
    for row in changed:
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
