#!/usr/bin/env python3
"""Run Breeze-ASR-25 for auxiliary pilot review transcripts.

This project uses Breeze-ASR-25, not Whisper, for current auxiliary ASR.
The transcript is still a warning signal only; human listening owns acceptance.
"""

from __future__ import annotations

import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import torch
from transformers import pipeline


DEFAULT_MODEL = "MediaTek-Research/Breeze-ASR-25"
REPO_ROOT = Path(__file__).resolve().parents[1]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def normalize_result(result: Any) -> tuple[str, list[dict[str, Any]]]:
    if isinstance(result, str):
        return result.strip(), []
    if not isinstance(result, dict):
        return str(result).strip(), []
    text = str(result.get("text", "")).strip()
    chunks = result.get("chunks") or []
    if not isinstance(chunks, list):
        chunks = []
    return text, chunks


def render_timestamp(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (int, float)):
        return f"{float(value):.2f}"
    return str(value)


def write_timestamped_text(path: Path, text: str, chunks: list[dict[str, Any]]) -> None:
    lines: list[str] = []
    for chunk in chunks:
        chunk_text = str(chunk.get("text", "")).strip()
        timestamp = chunk.get("timestamp")
        if isinstance(timestamp, (list, tuple)) and len(timestamp) == 2:
            start, end = timestamp
            lines.append(f"[{render_timestamp(start)} --> {render_timestamp(end)}] {chunk_text}")
        elif chunk_text:
            lines.append(chunk_text)
    if not lines and text:
        lines = [text]
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Breeze-ASR-25 auxiliary ASR.")
    parser.add_argument("--audio", type=Path, required=True)
    parser.add_argument("--output-txt", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-timestamped", type=Path)
    parser.add_argument("--log", type=Path)
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--language", default="zh")
    parser.add_argument("--chunk-length-s", type=float, default=15.0)
    parser.add_argument("--batch-size", type=int, default=1)
    parser.add_argument("--num-beams", type=int, default=1)
    parser.add_argument("--device", default="cuda")
    args = parser.parse_args()

    audio = args.audio.resolve()
    if not audio.exists():
        raise SystemExit(f"Audio not found: {audio}")

    output_txt = args.output_txt.resolve()
    output_json = args.output_json.resolve()
    output_timestamped = args.output_timestamped.resolve() if args.output_timestamped else None
    log_path = args.log.resolve() if args.log else None
    for path in [output_txt, output_json, output_timestamped, log_path]:
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)

    use_cuda = args.device == "cuda" and torch.cuda.is_available()
    device = 0 if use_cuda else -1
    dtype = torch.float16 if use_cuda else torch.float32

    started = time.time()
    pipe = pipeline(
        "automatic-speech-recognition",
        model=args.model,
        torch_dtype=dtype,
        device=device,
    )
    load_elapsed = time.time() - started

    asr_started = time.time()
    result = pipe(
        str(audio),
        chunk_length_s=args.chunk_length_s,
        batch_size=args.batch_size,
        return_timestamps=True,
        generate_kwargs={"language": args.language, "task": "transcribe", "num_beams": args.num_beams},
    )
    asr_elapsed = time.time() - asr_started
    text, chunks = normalize_result(result)

    output_txt.write_text(text.rstrip() + "\n", encoding="utf-8")
    if output_timestamped:
        write_timestamped_text(output_timestamped, text, chunks)

    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "model": args.model,
        "audio": rel(audio),
        "output_txt": rel(output_txt),
        "output_json": rel(output_json),
        "output_timestamped": rel(output_timestamped) if output_timestamped else "",
        "language": args.language,
        "chunk_length_s": args.chunk_length_s,
        "batch_size": args.batch_size,
        "num_beams": args.num_beams,
        "device": "cuda" if use_cuda else "cpu",
        "torch_dtype": str(dtype).replace("torch.", ""),
        "cuda_available": torch.cuda.is_available(),
        "gpu_name": torch.cuda.get_device_name(0) if use_cuda else "",
        "model_load_elapsed_s": round(load_elapsed, 3),
        "asr_elapsed_s": round(asr_elapsed, 3),
        "text_characters": len(text),
        "chunk_count": len(chunks),
        "acceptance_policy": "Auxiliary ASR only; human listening owns TTS gate decisions.",
        "result": result,
    }
    output_json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    summary = {
        "model": args.model,
        "audio": rel(audio),
        "output_txt": rel(output_txt),
        "output_json": rel(output_json),
        "output_timestamped": rel(output_timestamped) if output_timestamped else "",
        "device": payload["device"],
        "gpu_name": payload["gpu_name"],
        "model_load_elapsed_s": payload["model_load_elapsed_s"],
        "asr_elapsed_s": payload["asr_elapsed_s"],
        "text_characters": payload["text_characters"],
        "chunk_count": payload["chunk_count"],
    }
    if log_path:
        log_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
