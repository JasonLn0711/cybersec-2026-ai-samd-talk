#!/usr/bin/env python3
"""Apply reproducible post-synthesis tempo overrides to BreezyVoice subclips."""

from __future__ import annotations

import argparse
import csv
import shutil
import subprocess
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


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def atempo_filter(factor: float) -> str:
    if factor <= 0:
        raise ValueError("tempo factor must be positive")
    parts: list[float] = []
    remaining = factor
    while remaining < 0.5:
        parts.append(0.5)
        remaining /= 0.5
    while remaining > 2.0:
        parts.append(2.0)
        remaining /= 2.0
    parts.append(remaining)
    return ",".join(f"atempo={part:.6f}" for part in parts)


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply ffmpeg atempo to selected BreezyVoice subclip WAVs.")
    parser.add_argument("--parent-prefix", required=True)
    parser.add_argument("--tempo", type=float, required=True, help="ffmpeg atempo factor; <1 slows down without changing pitch.")
    parser.add_argument("--manifest", type=Path, default=LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.csv")
    parser.add_argument("--label", default=datetime.now().strftime("%Y%m%d-%H%M%S"))
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    rows = [row for row in read_csv(args.manifest) if row["parent_output_prefix"] == args.parent_prefix]
    if not rows:
        raise SystemExit(f"No subclips found for parent prefix: {args.parent_prefix}")

    archive_dir = LOCAL_ROOT / f"output/{VERSION}/archive/pacing-before-{args.label}/{args.parent_prefix}"
    archive_dir.mkdir(parents=True, exist_ok=True)
    audio_filter = atempo_filter(args.tempo)
    changed = []
    for row in rows:
        wav = repo_path(row["planned_output_wav"])
        if not wav.exists():
            raise FileNotFoundError(wav)
        original = archive_dir / wav.name
        if original.exists() and not args.overwrite:
            raise SystemExit(f"Archived WAV already exists; pass --overwrite: {original}")
        shutil.copy2(wav, original)
        tmp = wav.with_suffix(".tempo.wav")
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-i",
                str(original),
                "-filter:a",
                audio_filter,
                str(tmp),
            ],
            check=True,
        )
        tmp.replace(wav)
        changed.append({"subclip_id": row["subclip_id"], "wav": rel(wav), "archived_original": rel(original)})

    print(
        {
            "parent_prefix": args.parent_prefix,
            "tempo": args.tempo,
            "filter": audio_filter,
            "changed": len(changed),
            "archive_dir": rel(archive_dir),
        }
    )
    for row in changed:
        print(row)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
