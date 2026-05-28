#!/usr/bin/env python3
"""Run a command while sampling NVIDIA GPU telemetry.

This helper is intentionally local-run oriented. It records observable runtime
evidence for TTS experiments without committing generated audio or raw caches.
"""

from __future__ import annotations

import argparse
import csv
import json
import shutil
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def sample_gpu() -> dict[str, object] | None:
    if shutil.which("nvidia-smi") is None:
        return None
    command = [
        "nvidia-smi",
        "--query-gpu=timestamp,name,power.draw,utilization.gpu,memory.used,memory.total,temperature.gpu",
        "--format=csv,noheader,nounits",
    ]
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
    except (OSError, subprocess.CalledProcessError):
        return None
    first = result.stdout.strip().splitlines()[0] if result.stdout.strip() else ""
    if not first:
        return None
    row = next(csv.reader([first]))
    if len(row) < 7:
        return None
    timestamp, name, power_w, util_pct, mem_used_mb, mem_total_mb, temp_c = [item.strip() for item in row[:7]]
    return {
        "sampled_at": now_iso(),
        "nvidia_timestamp": timestamp,
        "gpu_name": name,
        "power_w": float(power_w),
        "utilization_gpu_pct": float(util_pct),
        "memory_used_mb": float(mem_used_mb),
        "memory_total_mb": float(mem_total_mb),
        "temperature_c": float(temp_c),
    }


def sampler(stop: threading.Event, interval_s: float, jsonl_path: Path, samples: list[dict[str, object]]) -> None:
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)
    with jsonl_path.open("w", encoding="utf-8") as fh:
        while not stop.is_set():
            sample = sample_gpu()
            if sample is not None:
                samples.append(sample)
                fh.write(json.dumps(sample, ensure_ascii=False) + "\n")
                fh.flush()
            stop.wait(interval_s)


def write_summary(
    path: Path,
    *,
    command: list[str],
    exit_code: int,
    started_at: str,
    ended_at: str,
    elapsed_s: float,
    samples: list[dict[str, object]],
    stdout_log: Path,
    telemetry_jsonl: Path,
) -> None:
    power_values = [float(item["power_w"]) for item in samples if "power_w" in item]
    util_values = [float(item["utilization_gpu_pct"]) for item in samples if "utilization_gpu_pct" in item]
    memory_values = [float(item["memory_used_mb"]) for item in samples if "memory_used_mb" in item]
    avg_power_w = sum(power_values) / len(power_values) if power_values else None
    estimated_gpu_wh = (avg_power_w * elapsed_s / 3600.0) if avg_power_w is not None else None
    summary = {
        "started_at": started_at,
        "ended_at": ended_at,
        "elapsed_s": round(elapsed_s, 3),
        "exit_code": exit_code,
        "command": command,
        "stdout_log": str(stdout_log),
        "telemetry_jsonl": str(telemetry_jsonl),
        "sample_count": len(samples),
        "avg_gpu_power_w": round(avg_power_w, 3) if avg_power_w is not None else None,
        "estimated_gpu_energy_wh": round(estimated_gpu_wh, 6) if estimated_gpu_wh is not None else None,
        "avg_gpu_utilization_pct": round(sum(util_values) / len(util_values), 3) if util_values else None,
        "max_gpu_memory_used_mb": max(memory_values) if memory_values else None,
        "energy_scope": "GPU-only estimate from nvidia-smi power.draw samples; excludes CPU, display, storage, PSU loss, and monitor energy.",
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run a command with NVIDIA GPU telemetry sampling.")
    parser.add_argument("--telemetry-jsonl", required=True)
    parser.add_argument("--summary-json", required=True)
    parser.add_argument("--stdout-log", required=True)
    parser.add_argument("--sample-interval-s", type=float, default=1.0)
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    if not args.command or args.command[0] != "--":
        raise SystemExit("Pass the command after `--`.")
    command = args.command[1:]
    if not command:
        raise SystemExit("No command supplied after `--`.")

    telemetry_jsonl = Path(args.telemetry_jsonl)
    summary_json = Path(args.summary_json)
    stdout_log = Path(args.stdout_log)
    stdout_log.parent.mkdir(parents=True, exist_ok=True)

    stop = threading.Event()
    samples: list[dict[str, object]] = []
    thread = threading.Thread(target=sampler, args=(stop, args.sample_interval_s, telemetry_jsonl, samples), daemon=True)
    started_at = now_iso()
    start = time.monotonic()
    thread.start()
    with stdout_log.open("w", encoding="utf-8") as log_fh:
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1)
        assert process.stdout is not None
        for line in process.stdout:
            sys.stdout.write(line)
            sys.stdout.flush()
            log_fh.write(line)
            log_fh.flush()
        exit_code = process.wait()
    elapsed_s = time.monotonic() - start
    ended_at = now_iso()
    stop.set()
    thread.join(timeout=max(args.sample_interval_s * 2, 1.0))
    write_summary(
        summary_json,
        command=command,
        exit_code=exit_code,
        started_at=started_at,
        ended_at=ended_at,
        elapsed_s=elapsed_s,
        samples=samples,
        stdout_log=stdout_log,
        telemetry_jsonl=telemetry_jsonl,
    )
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
