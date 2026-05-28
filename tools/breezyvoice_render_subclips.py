#!/usr/bin/env python3
"""Render prepared BreezyVoice subclips without requiring reference audio.

The default path uses BreezyVoice's built-in SFT/default speaker flow. Prompt
audio remains optional and is used only when explicitly selected.
"""

from __future__ import annotations

import argparse
import csv
import importlib.util
import os
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
DEFAULT_VERSION = "v1"
DEFAULT_MODEL_PATH = "MediaTek-Research/BreezyVoice"


def repo_relative(path: str | Path) -> Path:
    value = Path(path)
    if value.is_absolute():
        return value
    return REPO_ROOT / value


def resolve_breezyvoice_repo(value: str) -> str:
    if value:
        candidates = [Path(value).expanduser()]
    else:
        env_path = os.environ.get("BREEZYVOICE_REPO", "")
        candidates = []
        if env_path:
            candidates.append(Path(env_path).expanduser())
        candidates.extend(
            [
                REPO_ROOT / ".local/BreezyVoice",
                REPO_ROOT.parent / "BreezyVoice",
                Path.cwd(),
            ]
        )

    for candidate in candidates:
        candidate = candidate.resolve()
        if (candidate / "single_inference.py").exists():
            sys.path.insert(0, str(candidate))
            return str(candidate)

    if importlib.util.find_spec("single_inference") is not None:
        return "pythonpath"

    searched = ", ".join(str(path) for path in candidates)
    raise SystemExit(
        "Cannot find BreezyVoice runtime. Set BREEZYVOICE_REPO or pass "
        f"--breezyvoice-repo. Searched: {searched}"
    )


def load_manifest_rows(
    subclip_manifest: Path,
    pilot_manifest: Path,
    selection: str,
) -> list[dict[str, str]]:
    with subclip_manifest.open(encoding="utf-8", newline="") as fh:
        subclip_rows = list(csv.DictReader(fh))

    if selection == "all":
        return subclip_rows

    with pilot_manifest.open(encoding="utf-8", newline="") as fh:
        pilot_prefixes = {row["output_prefix"] for row in csv.DictReader(fh)}

    return [row for row in subclip_rows if row["parent_output_prefix"] in pilot_prefixes]


def read_text(path: str) -> str:
    return repo_relative(path).read_text(encoding="utf-8").strip()


def output_path_for(row: dict[str, str], output_dir: str) -> Path:
    if output_dir:
        return repo_relative(output_dir) / f"{row['subclip_id']}.wav"
    return repo_relative(row["planned_output_wav"])


def display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def import_runtime():
    import torch  # type: ignore
    import torchaudio  # type: ignore

    if not hasattr(torchaudio, "set_audio_backend"):
        torchaudio.set_audio_backend = lambda *_args, **_kwargs: None  # type: ignore[attr-defined]

    import single_inference as single_inference_mod  # type: ignore

    return single_inference_mod, torch, torchaudio


def load_wav_with_soundfile(torch, torchaudio, wav: str, target_sr: int):
    import soundfile as sf  # type: ignore

    data, sample_rate = sf.read(wav, dtype="float32", always_2d=True)
    speech = torch.from_numpy(data.T).float()
    speech = speech.mean(dim=0, keepdim=True)
    if sample_rate != target_sr:
        if sample_rate < target_sr:
            raise ValueError(f"wav sample rate {sample_rate} must be at least {target_sr}")
        speech = torchaudio.transforms.Resample(orig_freq=sample_rate, new_freq=target_sr)(speech)
    return speech


def save_wav_with_soundfile(path: str, waveform, sample_rate: int, **_kwargs) -> None:
    import soundfile as sf  # type: ignore

    audio = waveform.detach().cpu()
    if audio.ndim == 2:
        audio = audio.squeeze(0)
    sf.write(path, audio.numpy(), sample_rate, subtype="PCM_16")


def pick_speaker_id(cosyvoice, requested: str) -> str:
    if not hasattr(cosyvoice, "list_avaliable_spks"):
        raise SystemExit("BreezyVoice runtime does not expose list_avaliable_spks; cannot choose a default speaker.")
    available = list(cosyvoice.list_avaliable_spks())
    if requested != "auto":
        if available and requested not in available:
            raise SystemExit(f"Speaker id `{requested}` is not available. Available speaker ids: {available}")
        return requested
    if not available:
        raise SystemExit(
            "No built-in SFT/default speaker ids are available in this model. "
            "Use a no-reference-capable checkpoint or pass prompt audio explicitly."
        )
    return available[0]


def save_stream(torch, torchaudio, stream, output_path: Path, sample_rate: int) -> None:
    import soundfile as sf  # type: ignore

    chunks = []
    if isinstance(stream, dict):
        chunks.append(stream["tts_speech"])
    else:
        for item in stream:
            chunks.append(item["tts_speech"])
    if not chunks:
        raise RuntimeError(f"No speech chunks returned for {output_path}")
    speech = chunks[0] if len(chunks) == 1 else torch.concat(chunks, dim=1)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    audio = speech.squeeze(0).detach().cpu().numpy()
    sf.write(str(output_path), audio, sample_rate, subtype="PCM_16")


def render_default_voice(cosyvoice, torch, torchaudio, text: str, output_path: Path, speaker_id: str) -> None:
    sample_rate = int(getattr(cosyvoice, "sample_rate", 22050))
    stream = cosyvoice.inference_sft(text, speaker_id)
    save_stream(torch, torchaudio, stream, output_path, sample_rate)


def render_prompt_voice(
    single_inference_mod,
    cosyvoice,
    text: str,
    output_path: Path,
    prompt_audio: str,
    prompt_text_file: str,
) -> None:
    if not prompt_audio:
        raise SystemExit("Prompt voice mode was requested, but --prompt-audio is empty.")
    if not prompt_text_file:
        raise SystemExit("Prompt voice mode was requested, but --prompt-text-file is empty.")
    prompt_audio_path = repo_relative(prompt_audio)
    prompt_text_path = repo_relative(prompt_text_file)
    if not prompt_audio_path.exists():
        raise SystemExit(f"Prompt audio does not exist: {prompt_audio_path}")
    if not prompt_text_path.exists():
        raise SystemExit(f"Prompt transcript does not exist: {prompt_text_path}")

    converter_factory = getattr(single_inference_mod, "G2PWConverter", None)
    converter = converter_factory() if converter_factory else None
    prompt_text = prompt_text_path.read_text(encoding="utf-8").strip()
    single_inference_mod.load_wav = lambda wav, target_sr: load_wav_with_soundfile(
        __import__("torch"),
        __import__("torchaudio"),
        wav,
        target_sr,
    )
    single_inference_mod.torchaudio.save = save_wav_with_soundfile
    output_path.parent.mkdir(parents=True, exist_ok=True)
    single_inference_mod.single_inference(
        str(prompt_audio_path),
        text,
        str(output_path),
        cosyvoice,
        converter,
        prompt_text,
    )


def write_run_log(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "subclip_id",
        "parent_output_prefix",
        "voice_mode",
        "speaker_id",
        "text_characters",
        "output_wav",
        "status",
    ]
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Render local BreezyVoice subclips with no-reference default voice mode."
    )
    parser.add_argument("--version", default=DEFAULT_VERSION)
    parser.add_argument("--selection", choices=["pilot", "all"], default="pilot")
    parser.add_argument("--voice-mode", choices=["default", "prompt", "auto"], default="default")
    parser.add_argument("--speaker-id", default="auto", help="Built-in SFT/default speaker id, or auto.")
    parser.add_argument("--model-path", default=DEFAULT_MODEL_PATH)
    parser.add_argument("--breezyvoice-repo", default="")
    parser.add_argument("--subclip-manifest", default="")
    parser.add_argument("--pilot-manifest", default="")
    parser.add_argument("--output-dir", default="")
    parser.add_argument("--prompt-audio", default="")
    parser.add_argument("--prompt-text-file", default="")
    parser.add_argument("--limit", type=int, default=0)
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    version_root = LOCAL_ROOT / args.version
    subclip_manifest = repo_relative(args.subclip_manifest) if args.subclip_manifest else LOCAL_ROOT / f"manifests/{args.version}/subclip_manifest.csv"
    pilot_manifest = repo_relative(args.pilot_manifest) if args.pilot_manifest else LOCAL_ROOT / f"manifests/{args.version}/pilot_manifest.csv"
    rows = load_manifest_rows(subclip_manifest, pilot_manifest, args.selection)
    if args.limit:
        rows = rows[: args.limit]
    if not rows:
        raise SystemExit("No rows selected for rendering.")

    voice_mode = args.voice_mode
    if voice_mode == "auto":
        voice_mode = "prompt" if args.prompt_audio and repo_relative(args.prompt_audio).exists() else "default"

    log_rows: list[dict[str, str]] = []
    if args.dry_run:
        for row in rows:
            text = read_text(row["clean_text_path"])
            output_path = output_path_for(row, args.output_dir)
            log_rows.append(
                {
                    "subclip_id": row["subclip_id"],
                    "parent_output_prefix": row["parent_output_prefix"],
                    "voice_mode": voice_mode,
                    "speaker_id": args.speaker_id,
                    "text_characters": str(len(text)),
                    "output_wav": display_path(output_path),
                    "status": "dry_run",
                }
            )
        write_run_log(LOCAL_ROOT / f"runtime/{args.version}/last_render_plan.csv", log_rows)
        print(f"Dry run selected {len(rows)} subclips in {voice_mode} mode.")
        return

    runtime_location = resolve_breezyvoice_repo(args.breezyvoice_repo)
    single_inference_mod, torch, torchaudio = import_runtime()
    cosyvoice = single_inference_mod.CustomCosyVoice(args.model_path)
    speaker_id = pick_speaker_id(cosyvoice, args.speaker_id) if voice_mode == "default" else args.speaker_id

    for row in rows:
        text = read_text(row["clean_text_path"])
        output_path = output_path_for(row, args.output_dir)
        if output_path.exists() and not args.overwrite:
            status = "skipped_exists"
        else:
            if voice_mode == "default":
                render_default_voice(cosyvoice, torch, torchaudio, text, output_path, speaker_id)
            else:
                render_prompt_voice(
                    single_inference_mod,
                    cosyvoice,
                    text,
                    output_path,
                    args.prompt_audio,
                    args.prompt_text_file,
                )
            status = "rendered"
        log_rows.append(
            {
                "subclip_id": row["subclip_id"],
                "parent_output_prefix": row["parent_output_prefix"],
                "voice_mode": voice_mode,
                "speaker_id": speaker_id,
                "text_characters": str(len(text)),
                "output_wav": display_path(output_path),
                "status": status,
            }
        )
        print(f"{status}: {row['subclip_id']} -> {display_path(output_path)}")

    write_run_log(LOCAL_ROOT / f"runtime/{args.version}/last_render_plan.csv", log_rows)
    print(f"Runtime: {runtime_location}")
    print(f"Completed {len(log_rows)} selected subclips in {voice_mode} mode.")


if __name__ == "__main__":
    main()
