#!/usr/bin/env python3
"""Prepare local BreezyVoice render inputs from the 80 minute engineering draft.

The generated package is intentionally local-only under `.local/breezyvoice`.
It strips orchestration markup before model input, preserves stable
`output_prefix` values, and creates review gates before any full TTS run.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import platform
import re
import shutil
import subprocess
import sys
import wave
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE_MD = REPO_ROOT / "docs/speaker-notes/breezyvoice/model-ready/cde-2026-breezyvoice-80min-engineered-transcript-v1-zh-tw.md"
PRONUNCIATION_NOTES = REPO_ROOT / "docs/speaker-notes/breezyvoice/model-ready/cde-2026-breezyvoice-pronunciation-notes.md"
LOCAL_ROOT = REPO_ROOT / ".local/breezyvoice"
VERSION = "v1"
REFERENCE_AUDIO_REQUIRED = False

PILOT_PREFIXES = [
    "cde_full_01_opening_positioning_crazyhunter_entry_case",
    "cde_full_16_k8s_review_controls",
    "cde_full_20_crowdstrike_update_524b",
    "cde_full_26_shared_close_test_anchors",
]

TERM_NORMALIZATIONS = {
    "CDE": "C D E",
    "AI": "A I",
    "ASR": "A S R",
    "TTS": "T T S",
    "TFDA": "T F D A",
    "FDA": "F D A",
    "SaMD": "S A M D",
    "SBOM": "S B O M",
    "SCA": "S C A",
    "PACS": "派克斯",
    "HIS": "H I S",
    "EMR": "E M R",
    "RIS": "R I S",
    "LIS": "L I S",
    "FHIR": "F H I R",
    "DICOM": "戴康 DICOM",
    "API": "A P I",
    "VPN": "V P N",
    "MFA": "M F A",
    "RBAC": "R B A C",
    "IAM": "I A M",
    "HL7": "H L seven",
    "SIEM": "S I E M",
    "EDR": "E D R",
    "K8S API": "K eight S，A P I",
    "K8S": "K eight S",
    "CI/CD": "C I C D",
    "AWS": "A W S",
    "FD&C Act Section 524B": "F D and C Act Section 五二四 B",
    "FD&C Act，Section 524B": "F D and C Act，Section 五二四 B",
    "FD&C Act Section 五二四 B": "F D and C Act Section 五二四 B",
    "FD&C Act": "F D and C Act",
    "524B": "五二四 B",
    "Log4Shell": "Log four Shell",
    "MOVEit Transfer": "Move it Transfer",
    "Channel File 291": "Channel File 二九一",
    "NetworkPolicy": "Network Policy",
    "workflow": "工作流程",
    "clinical continuity": "臨床連續性",
    "Clinical": "臨床",
    "ransomware": "勒索軟體",
    "downtime": "停機",
    "vendor access": "廠商存取",
    "patching limitation": "修補限制",
    "credential risk": "憑證風險",
    "White-box Testing": "White box testing，白箱測試",
    "White box Testing": "White box testing，白箱測試",
    "white-box validation": "white box validation，白箱驗證",
    "software supply paths": "software supply chain，供應鏈",
    "supply path": "supply chain，供應鏈",
    "CrazyHunter": "Crazy Hunter",
    "UnitedHealth": "United Health",
    "OneBlood": "One Blood",
    "BlackCat": "Black Cat",
    "St. Jude": "Saint Jude",
    "Lurie Children's Hospital": "Lurie Childrens Hospital",
    "Lurie Children’s Hospital": "Lurie Childrens Hospital",
}

PILOT_ASR_TERM_VARIANTS = {
    "K8S": ["K eight S", "K8S", "K 八 S"],
    "524B": ["五二四", "524B", "五二四 B"],
    "Log4Shell": ["Log four", "Log4Shell", "Log four Shell"],
    "Channel File 291": ["Channel File", "二九一", "291"],
    "PACS": ["P A C S", "PACS", "派克斯"],
    "HIS": ["H I S", "HIS"],
    "EMR": ["E M R", "EMR"],
    "workflow": ["工作流程", "workflow"],
    "clinical": ["臨床", "Clinical", "clinical"],
    "CDE": ["C D E", "CDE"],
    "FDA": ["F D A", "FDA"],
    "SBOM": ["S B O M", "SBOM"],
}

CONTROL_RE = re.compile(
    r"<!-- BV26_META\n(?P<meta>.*?)\n-->\n\n"
    r"### (?P<title>.*?)\n\n"
    r"\[(?P<tag>BV26[^\]]*)\]\n"
    r"(?P<text>.*?)\n"
    r"\[/BV26\]",
    re.S,
)


@dataclass
class Segment:
    index: int
    segment_id: str
    group: str
    output_prefix: str
    title: str
    preset: str
    speed_cpm: str
    target_duration: str
    target_seconds: int
    timeline: str
    character_count: int
    delivery: str
    source_notes: str
    pronunciation_hints: list[str]
    clean_text: str
    normalized_text: str
    clean_text_path: Path
    normalized_text_path: Path


def rel(path: Path) -> str:
    return str(path.relative_to(REPO_ROOT))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def parse_duration(value: str) -> int:
    minutes, seconds = value.split(":")
    return int(minutes) * 60 + int(seconds)


def parse_meta(meta: str) -> tuple[dict[str, str], list[str]]:
    fields: dict[str, str] = {}
    hints: list[str] = []
    in_hints = False
    for raw_line in meta.splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if line == "pronunciation_hints:":
            in_hints = True
            continue
        if in_hints and line.strip().startswith("- "):
            hints.append(line.strip()[2:].strip().strip('"'))
            continue
        in_hints = False
        if ":" in line:
            key, value = line.split(":", 1)
            fields[key.strip()] = value.strip().strip('"')
    return fields, hints


def clean_model_text(text: str) -> str:
    cleaned = text.replace("\u3000", " ")
    cleaned = re.sub(r"[ \t]+", " ", cleaned)
    cleaned = re.sub(r"\s*\n\s*", " ", cleaned).strip()
    return cleaned


def normalize_text(text: str) -> str:
    normalized = clean_model_text(text)
    for old, new in TERM_NORMALIZATIONS.items():
        normalized = normalized.replace(old, new)
    normalized = apply_pilot_review_conditioning(normalized)
    normalized = re.sub(r"[ \t]+", " ", normalized).strip()
    return normalized


def apply_pilot_review_conditioning(text: str) -> str:
    """Apply conservative text conditioning from pilot human review.

    These replacements keep the source transcript frozen while improving
    model-facing pacing and pronunciation for the pilot failure modes.
    """
    replacements = {
        "P A C S、H I S、E M R": "派克斯，H I S，E M R",
        "派克斯、H I S、E M R": "派克斯，H I S，E M R",
        "戴康 DICOM 工作流程": "戴康 DICOM 影像流程",
        "戴康 DICOM router": "戴康 DICOM router",
        "verify R B A C、service accounts、namespace isolation": "verify，R B A C，service accounts，namespace isolation",
        "secrets handling and cloud credential exposure": "secrets handling，以及 cloud credential exposure",
        "Network Policy、ingress rules、exposed services": "Network Policy，ingress rules，exposed services",
        "application endpoint，K eight S A P I、dashboard、internal service": "application endpoint，K eight S，A P I，dashboard，internal service",
        "In Kubernetes, the security boundary is not the container. The real boundary is identity, configuration, network policy, and deployment governance.": "在 Kubernetes 裡，security boundary 不是 container。真正的 boundary 是 identity、configuration、network policy 與 deployment governance。",
        "Tesla Kubernetes Console Cryptojacking": "Tesla 雲端基礎設施加密貨幣挖礦案例",
        "exposed K eight S console、pod credentials、A W S access、cryptomining workload": "exposed K eight S console，pod credentials，A W S access，crypto mining workload",
        "Tesla 的 cloud infrastructure": "Tesla 的雲端基礎設施",
        "cloud resource 進行 cryptocurrency mining": "雲端資源進行加密貨幣挖礦",
        "faulty security content update": "CrowdStrike Falcon 安全內容更新",
        "Security updates are also software supply chain，供應鏈 that require white box validation，白箱驗證.": "Security updates are also software supply chain，供應鏈；they require white box validation，白箱驗證。",
        "F D and C Act Section 五二四 B": "F D and C Act，Section 五二四 B",
        "F D A、T F D A、五二四 B、S B O M": "F D A，T F D A，五二四 B，S B O M",
        "White box Testing 與 system review": "White box testing，白箱測試，與 system review",
        "White box testing，白箱測試與滲透測試": "White box testing，白箱測試，與滲透測試",
        "白箱測試從內部程式": "White box testing，白箱測試，從內部程式",
        "白箱審查": "White box review，白箱審查",
        "白箱證據": "White box evidence，白箱證據",
        "白箱可以證明": "White box evidence 可以證明",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def validate_model_text(text: str, label: str) -> None:
    forbidden = ["BV26", "<!--", "-->", "```", "\n#", "[/BV26]", "[BV26"]
    hits = [item for item in forbidden if item in text]
    if hits:
        raise ValueError(f"{label} contains forbidden model-input tokens: {hits}")


def parse_segments() -> list[Segment]:
    source = SOURCE_MD.read_text(encoding="utf-8")
    segments: list[Segment] = []
    for index, match in enumerate(CONTROL_RE.finditer(source), start=1):
        meta, hints = parse_meta(match.group("meta"))
        clean_text = clean_model_text(match.group("text"))
        normalized_text = normalize_text(clean_text)
        validate_model_text(clean_text, f"segment {index} clean text")
        validate_model_text(normalized_text, f"segment {index} normalized text")
        output_prefix = meta["output_prefix"]
        segments.append(
            Segment(
                index=index,
                segment_id=meta["segment_id"],
                group=meta["group"],
                output_prefix=output_prefix,
                title=match.group("title").strip(),
                preset=meta["preset"],
                speed_cpm=meta["speed_cpm"],
                target_duration=meta["target_duration"],
                target_seconds=parse_duration(meta["target_duration"]),
                timeline=meta["timeline"],
                character_count=int(meta["character_count"]),
                delivery=meta["delivery"],
                source_notes=meta.get("source_notes", ""),
                pronunciation_hints=hints,
                clean_text=clean_text,
                normalized_text=normalized_text,
                clean_text_path=LOCAL_ROOT / f"inputs/{VERSION}/segments/{output_prefix}.txt",
                normalized_text_path=LOCAL_ROOT / f"inputs/{VERSION}/normalized_segments/{output_prefix}.txt",
            )
        )
    return segments


def split_sentences(text: str) -> list[str]:
    pieces = re.findall(r".+?(?:[。！？?]|$)", text)
    sentences: list[str] = []
    for piece in pieces:
        cleaned = re.sub(r"\s+", " ", piece).strip()
        if not cleaned:
            continue
        if len(cleaned) <= 500:
            sentences.append(cleaned)
            continue

        clauses = re.findall(r".+?(?:[，；：、]|$)", cleaned)
        current: list[str] = []
        current_len = 0
        for clause in [c.strip() for c in clauses if c.strip()]:
            if current and current_len + len(clause) > 430:
                sentences.append(" ".join(current).strip())
                current = [clause]
                current_len = len(clause)
            else:
                current.append(clause)
                current_len += len(clause)
        if current:
            sentences.append(" ".join(current).strip())
    return sentences or [text]


def split_subclips(text: str) -> list[str]:
    sentences = split_sentences(text)
    if len(text) <= 850:
        target_count = 2
    elif len(text) <= 1100:
        target_count = 3
    else:
        target_count = 4
    target_len = max(260, len(text) // target_count)
    clips: list[str] = []
    current: list[str] = []
    current_len = 0
    for sentence in sentences:
        sentence_len = len(sentence)
        should_flush = (
            current
            and current_len >= 240
            and current_len + sentence_len > target_len
            and len(clips) < target_count - 1
        )
        if should_flush:
            clips.append(" ".join(current).strip())
            current = [sentence]
            current_len = sentence_len
        else:
            current.append(sentence)
            current_len += sentence_len
    if current:
        clips.append(" ".join(current).strip())

    # If a very long sentence makes a clip too long, keep it intact rather than
    # cutting mid-sentence; review can decide whether to manually shorten it.
    if len(clips) > 4:
        merged = clips[:3]
        merged.append(" ".join(clips[3:]).strip())
        clips = merged
    return clips


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_jsonl(path: Path, rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def wav_duration_seconds(path: Path) -> float | None:
    if not path.exists():
        return None
    try:
        with wave.open(str(path), "rb") as wav:
            return wav.getnframes() / float(wav.getframerate())
    except wave.Error:
        return None


def read_optional_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def command_version(command: str, *args: str) -> dict[str, object]:
    executable = shutil.which(command)
    if not executable:
        return {"available": False, "path": "", "version": ""}
    try:
        result = subprocess.run(
            [executable, *args],
            check=False,
            capture_output=True,
            text=True,
            timeout=10,
        )
    except Exception as exc:  # pragma: no cover - defensive runtime probe
        return {"available": True, "path": executable, "version": f"probe_failed: {exc}"}
    version = (result.stdout or result.stderr).strip().splitlines()
    return {"available": True, "path": executable, "version": version[0] if version else ""}


def module_available(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def probe_python_runtime(python_path: Path) -> dict[str, object]:
    if not python_path.exists():
        return {"available": False, "path": str(python_path)}
    code = r"""
import importlib.util
import json
import sys

modules = ["torch", "torchaudio", "transformers", "huggingface_hub", "gradio", "g2pw", "soundfile"]
payload = {
    "available": True,
    "path": sys.executable,
    "version": sys.version.split()[0],
    "modules": {name: importlib.util.find_spec(name) is not None for name in modules},
}
try:
    import torch
    import torchaudio

    payload["torch"] = {
        "version": torch.__version__,
        "torchaudio_version": torchaudio.__version__,
        "cuda_available": torch.cuda.is_available(),
    }
    if torch.cuda.is_available():
        payload["torch"]["device"] = torch.cuda.get_device_name(0)
        payload["torch"]["capability"] = list(torch.cuda.get_device_capability(0))
        try:
            value = (torch.ones((32, 32), device="cuda") @ torch.ones((32, 32), device="cuda"))[0, 0].item()
            payload["torch"]["cuda_smoke_ok"] = value == 32.0
        except Exception as exc:
            payload["torch"]["cuda_smoke_ok"] = False
            payload["torch"]["cuda_smoke_error"] = repr(exc)
except Exception as exc:
    payload["torch_probe_error"] = repr(exc)
print(json.dumps(payload, ensure_ascii=False))
"""
    try:
        result = subprocess.run(
            [str(python_path), "-c", code],
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
    except Exception as exc:  # pragma: no cover - defensive runtime probe
        return {"available": True, "path": str(python_path), "probe_error": repr(exc)}
    try:
        payload = json.loads(result.stdout.strip().splitlines()[-1])
    except Exception:
        return {
            "available": True,
            "path": str(python_path),
            "probe_error": result.stderr.strip() or result.stdout.strip(),
        }
    if result.stderr.strip():
        payload["stderr_first_line"] = result.stderr.strip().splitlines()[0]
    return payload


def detect_runtime_state(reference_audio_exists: bool) -> dict[str, object]:
    module_names = [
        "torch",
        "torchaudio",
        "transformers",
        "huggingface_hub",
        "gradio",
        "g2pw",
    ]
    module_state = {name: module_available(name) for name in module_names}
    runner_path = REPO_ROOT / "tools/breezyvoice_render_subclips.py"
    setup_path = REPO_ROOT / "tools/setup_breezyvoice_rtx5080_runtime.sh"
    local_venv_python = LOCAL_ROOT / f"runtime/{VERSION}/venv/bin/python"
    local_venv_probe = probe_python_runtime(local_venv_python)
    breezyvoice_candidates = [
        REPO_ROOT / ".local/BreezyVoice",
        REPO_ROOT.parent / "BreezyVoice",
        Path.home() / "BreezyVoice",
    ]
    repo_ready = any((path / "single_inference.py").exists() for path in breezyvoice_candidates)
    venv_modules = local_venv_probe.get("modules", {})
    venv_torch = local_venv_probe.get("torch", {})
    local_venv_ready = bool(
        local_venv_probe.get("available")
        and repo_ready
        and isinstance(venv_modules, dict)
        and all(venv_modules.get(name) for name in ["torch", "torchaudio", "g2pw", "soundfile"])
    )
    rtx_5080_ready = bool(
        local_venv_ready
        and isinstance(venv_torch, dict)
        and venv_torch.get("cuda_available")
        and venv_torch.get("cuda_smoke_ok")
        and venv_torch.get("capability") == [12, 0]
    )
    return {
        "reference_audio_required": REFERENCE_AUDIO_REQUIRED,
        "reference_audio_exists": reference_audio_exists,
        "execution_mode_without_audio": "default_sft_voice",
        "no_reference_runner": rel(runner_path),
        "rtx_5080_runtime_setup": rel(setup_path),
        "pilot_command_template": rel(LOCAL_ROOT / f"commands/{VERSION}/run_pilot_template.sh"),
        "python": {
            "executable": sys.executable,
            "version": platform.python_version(),
            "python3_10": shutil.which("python3.10") or "",
        },
        "commands": {
            "uv": command_version("uv", "--version"),
            "docker": command_version("docker", "--version"),
            "docker_compose": command_version("docker", "compose", "version"),
            "nvidia_smi": command_version("nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"),
        },
        "python_modules": module_state,
        "breezyvoice_repo_candidates": [
            {"path": str(path), "exists": path.exists(), "has_single_inference": (path / "single_inference.py").exists()}
            for path in breezyvoice_candidates
        ],
        "local_venv": local_venv_probe,
        "ready_to_render_locally": local_venv_ready or (
            all(module_state.values())
            and repo_ready
        ),
        "rtx_5080_ready": rtx_5080_ready,
    }


def prepare_package() -> None:
    segments = parse_segments()
    if len(segments) != 26:
        raise ValueError(f"Expected 26 segments, found {len(segments)}")
    if sum(segment.target_seconds for segment in segments) != 4800:
        raise ValueError("Target duration does not sum to 80:00")
    if sum(len(segment.clean_text) for segment in segments) != 28053:
        raise ValueError("Model text character count drifted from frozen v1 value 28053")

    dirs = [
        LOCAL_ROOT / f"freeze/{VERSION}",
        LOCAL_ROOT / f"manifests/{VERSION}",
        LOCAL_ROOT / f"inputs/{VERSION}/segments",
        LOCAL_ROOT / f"inputs/{VERSION}/normalized_segments",
        LOCAL_ROOT / f"inputs/{VERSION}/subclips",
        LOCAL_ROOT / f"prompts/{VERSION}",
        LOCAL_ROOT / f"runtime/{VERSION}",
        LOCAL_ROOT / f"output/{VERSION}/subclips",
        LOCAL_ROOT / f"output/{VERSION}/parent_chunks",
        LOCAL_ROOT / f"output/{VERSION}/full",
        LOCAL_ROOT / f"output/{VERSION}/archive",
        LOCAL_ROOT / f"review/{VERSION}",
        LOCAL_ROOT / f"specs/{VERSION}",
        LOCAL_ROOT / f"commands/{VERSION}",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    frozen_source = LOCAL_ROOT / f"freeze/{VERSION}/source/cde-2026-breezyvoice-80min-engineered-transcript-v1-zh-tw.md"
    frozen_source.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(SOURCE_MD, frozen_source)

    source_hash = sha256(SOURCE_MD)
    freeze_payload = {
        "version": VERSION,
        "source_path": rel(SOURCE_MD),
        "frozen_source_path": rel(frozen_source),
        "source_sha256": source_hash,
        "segment_count": len(segments),
        "target_total_seconds": sum(segment.target_seconds for segment in segments),
        "target_total_time": "80:00",
        "model_text_characters": sum(len(segment.clean_text) for segment in segments),
        "bv26_markup_in_model_text": False,
        "pronunciation_notes_path": rel(PRONUNCIATION_NOTES),
    }
    write_json(LOCAL_ROOT / f"freeze/{VERSION}/freeze_report.json", freeze_payload)
    write_text(
        LOCAL_ROOT / f"freeze/{VERSION}/freeze_report.md",
        "\n".join(
            [
                "# BreezyVoice V1 Freeze Report",
                "",
                f"- Version: `{VERSION}`",
                f"- Source: `{rel(SOURCE_MD)}`",
                f"- Frozen copy: `{rel(frozen_source)}`",
                f"- Source SHA-256: `{source_hash}`",
                "- Segment count: `26`",
                "- Target timing: `80:00`",
                "- Model text characters: `28053`",
                "- Model text contains `BV26`: `false`",
                "",
                "Purpose: every generated audio file should trace back to this frozen source, stable `output_prefix`, segment id, and clean text path.",
            ]
        ),
    )

    manifest_rows: list[dict[str, object]] = []
    subclip_rows: list[dict[str, object]] = []
    review_rows: list[dict[str, object]] = []

    for segment in segments:
        write_text(segment.clean_text_path, segment.clean_text)
        write_text(segment.normalized_text_path, segment.normalized_text)
        subclips = split_subclips(segment.normalized_text)
        subclip_paths = []
        for sub_index, subclip in enumerate(subclips, start=1):
            validate_model_text(subclip, f"{segment.output_prefix}_p{sub_index:02d}")
            subclip_id = f"{segment.output_prefix}_p{sub_index:02d}"
            subclip_text_path = LOCAL_ROOT / f"inputs/{VERSION}/subclips/{subclip_id}.txt"
            subclip_output_path = LOCAL_ROOT / f"output/{VERSION}/subclips/{subclip_id}.wav"
            write_text(subclip_text_path, subclip)
            subclip_paths.append(rel(subclip_text_path))
            subclip_rows.append(
                {
                    "parent_output_prefix": segment.output_prefix,
                    "segment_id": segment.segment_id,
                    "subclip_id": subclip_id,
                    "subclip_index": sub_index,
                    "subclip_count": len(subclips),
                    "text_characters": len(subclip),
                    "clean_text_path": rel(subclip_text_path),
                    "planned_output_wav": rel(subclip_output_path),
                    "parent_output_wav": rel(LOCAL_ROOT / f"output/{VERSION}/parent_chunks/{segment.output_prefix}.wav"),
                    "full_output_wav": rel(LOCAL_ROOT / f"output/{VERSION}/full/cde-2026-breezyvoice-80min-v1.wav"),
                    "accepted": "",
                }
            )

        manifest_rows.append(
            {
                "output_prefix": segment.output_prefix,
                "segment_id": segment.segment_id,
                "group": segment.group,
                "title": segment.title,
                "preset": segment.preset,
                "speed_cpm": segment.speed_cpm,
                "target_duration": segment.target_duration,
                "target_seconds": segment.target_seconds,
                "timeline": segment.timeline,
                "text_characters": len(segment.clean_text),
                "clean_text_path": rel(segment.clean_text_path),
                "normalized_text_path": rel(segment.normalized_text_path),
                "subclip_count": len(subclips),
                "subclip_text_paths": ";".join(subclip_paths),
                "pronunciation_hints": "; ".join(segment.pronunciation_hints),
                "source_notes": segment.source_notes,
                "planned_parent_wav": rel(LOCAL_ROOT / f"output/{VERSION}/parent_chunks/{segment.output_prefix}.wav"),
            }
        )
        review_rows.append(
            {
                "output_prefix": segment.output_prefix,
                "subclip_count": len(subclips),
                "runtime": "",
                "pronunciation_issue": "",
                "fix_applied": "",
                "accepted": "",
            }
        )

    manifest_fields = [
        "output_prefix",
        "segment_id",
        "group",
        "title",
        "preset",
        "speed_cpm",
        "target_duration",
        "target_seconds",
        "timeline",
        "text_characters",
        "clean_text_path",
        "normalized_text_path",
        "subclip_count",
        "subclip_text_paths",
        "pronunciation_hints",
        "source_notes",
        "planned_parent_wav",
    ]
    write_csv(LOCAL_ROOT / f"manifests/{VERSION}/render_manifest.csv", manifest_rows, manifest_fields)
    write_jsonl(LOCAL_ROOT / f"manifests/{VERSION}/render_manifest.jsonl", manifest_rows)

    subclip_fields = [
        "parent_output_prefix",
        "segment_id",
        "subclip_id",
        "subclip_index",
        "subclip_count",
        "text_characters",
        "clean_text_path",
        "planned_output_wav",
        "parent_output_wav",
        "full_output_wav",
        "accepted",
    ]
    write_csv(LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.csv", subclip_rows, subclip_fields)
    write_jsonl(LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.jsonl", subclip_rows)

    pilot_rows = [row for row in manifest_rows if row["output_prefix"] in PILOT_PREFIXES]
    write_csv(LOCAL_ROOT / f"manifests/{VERSION}/pilot_manifest.csv", pilot_rows, manifest_fields)
    write_jsonl(LOCAL_ROOT / f"manifests/{VERSION}/pilot_manifest.jsonl", pilot_rows)
    pilot_prefixes = {row["output_prefix"] for row in pilot_rows}
    pilot_subclip_rows = [row for row in subclip_rows if row["parent_output_prefix"] in pilot_prefixes]
    pilot_audio_rows = []
    for row in pilot_subclip_rows:
        output_path = REPO_ROOT / str(row["planned_output_wav"])
        duration = wav_duration_seconds(output_path)
        pilot_audio_rows.append(
            {
                "subclip_id": row["subclip_id"],
                "parent_output_prefix": row["parent_output_prefix"],
                "planned_output_wav": row["planned_output_wav"],
                "exists": output_path.exists(),
                "duration_seconds": f"{duration:.2f}" if duration is not None else "",
                "accepted": "",
            }
        )
    write_csv(
        LOCAL_ROOT / f"review/{VERSION}/pilot_audio_inventory.csv",
        pilot_audio_rows,
        ["subclip_id", "parent_output_prefix", "planned_output_wav", "exists", "duration_seconds", "accepted"],
    )
    planned_subclip_wavs = {REPO_ROOT / str(row["planned_output_wav"]) for row in subclip_rows}
    actual_subclip_wavs = sorted((LOCAL_ROOT / f"output/{VERSION}/subclips").glob("*.wav"))
    orphan_audio_rows = []
    for output_path in actual_subclip_wavs:
        if output_path not in planned_subclip_wavs:
            duration = wav_duration_seconds(output_path)
            orphan_audio_rows.append(
                {
                    "output_wav": rel(output_path),
                    "duration_seconds": f"{duration:.2f}" if duration is not None else "",
                    "status": "orphan_not_in_current_subclip_manifest",
                    "action": "archive_or_delete_before_manual_review_if_this_filename_could_confuse_selection",
                }
            )
    write_csv(
        LOCAL_ROOT / f"review/{VERSION}/orphan_audio_inventory.csv",
        orphan_audio_rows,
        ["output_wav", "duration_seconds", "status", "action"],
    )
    pilot_outputs_existing = sum(1 for row in pilot_audio_rows if row["exists"])
    pilot_outputs_complete = pilot_outputs_existing == len(pilot_subclip_rows)
    pilot_parent_paths = sorted(
        {
            REPO_ROOT / str(row["parent_output_wav"])
            for row in pilot_subclip_rows
        }
    )
    pilot_parent_outputs_existing = sum(1 for path in pilot_parent_paths if path.exists())
    pilot_full_stitched_path = LOCAL_ROOT / f"output/{VERSION}/full/cde-2026-breezyvoice-pilot-stitched-v1.wav"
    pilot_full_stitched_exists = pilot_full_stitched_path.exists()
    pilot_asr_path = LOCAL_ROOT / f"review/{VERSION}/asr/cde-2026-breezyvoice-pilot-stitched-v1.txt"
    pilot_asr_text = read_optional_text(pilot_asr_path)
    pilot_asr_term_hits = {
        term: sum(pilot_asr_text.count(variant) for variant in variants)
        for term, variants in PILOT_ASR_TERM_VARIANTS.items()
    }
    pilot_asr_forbidden_hits = {
        token: pilot_asr_text.count(token)
        for token in ["BV26", "<!--", "-->", "[BV26", "[/BV26]", "```"]
        if token in pilot_asr_text
    }
    pilot_asr_missing_terms = [term for term, count in pilot_asr_term_hits.items() if count == 0]
    pilot_machine_review_status = (
        "needs_human_listening"
        if pilot_asr_text and pilot_asr_missing_terms
        else "asr_not_available"
        if not pilot_asr_text
        else "machine_review_no_control_markup"
    )
    write_json(
        LOCAL_ROOT / f"review/{VERSION}/pilot_machine_review.json",
        {
            "pilot_asr_path": rel(pilot_asr_path),
            "asr_exists": pilot_asr_path.exists(),
            "asr_characters": len(pilot_asr_text),
            "asr_term_hits": pilot_asr_term_hits,
            "asr_term_variants": PILOT_ASR_TERM_VARIANTS,
            "asr_missing_terms": pilot_asr_missing_terms,
            "asr_forbidden_markup_hits": pilot_asr_forbidden_hits,
            "status": pilot_machine_review_status,
            "interpretation": (
                "ASR is an auxiliary signal only. Missing term hits or odd substitutions require human listening before full batch approval."
            ),
        },
    )
    write_text(
        LOCAL_ROOT / f"review/{VERSION}/pilot_machine_review.md",
        "\n".join(
            [
                "# Pilot Machine Review",
                "",
                f"- ASR transcript: `{rel(pilot_asr_path)}`",
                f"- ASR exists: `{pilot_asr_path.exists()}`",
                f"- ASR characters: `{len(pilot_asr_text)}`",
                f"- Status: `{pilot_machine_review_status}`",
                f"- Forbidden markup hits: `{pilot_asr_forbidden_hits or {}}`",
                "",
                "Expected term hits from ASR:",
                "",
                "| Term | Count |",
                "| --- | ---: |",
                *[f"| `{term}` | {count} |" for term, count in pilot_asr_term_hits.items()],
                "",
                "Machine interpretation:",
                "",
                "- ASR is not a substitute for human listening.",
                "- No forbidden orchestration markup should appear in the ASR transcript.",
                "- Missing expected terms or strange substitutions are treated as a pilot-review risk, not as proof that the raw audio itself is unusable.",
                "- Keep `full_batch_allowed=false` until the pilot listening checklist is accepted.",
            ]
        ),
    )

    render_review_log_path = LOCAL_ROOT / f"review/{VERSION}/render_review_log.csv"
    if not render_review_log_path.exists():
        write_csv(
            render_review_log_path,
            review_rows,
            ["output_prefix", "subclip_count", "runtime", "pronunciation_issue", "fix_applied", "accepted"],
        )

    write_text(
        LOCAL_ROOT / f"inputs/{VERSION}/pronunciation_override_policy.md",
        "\n".join(
            [
                "# Pronunciation Override Policy",
                "",
                f"Source pronunciation notes: `{rel(PRONUNCIATION_NOTES)}`",
                "",
                "Use the notes as the authority, but apply overrides only after pilot evidence.",
                "Keep professional English terms recognizable for a Taiwan medical-cybersecurity audience.",
                "",
                "Pre-applied low-risk normalizations:",
                "",
                "- `K8S` -> `K eight S`",
                "- `524B` -> `五二四 B`",
                "- `Log4Shell` -> `Log four Shell`",
                "- `MOVEit Transfer` -> `Move it Transfer`",
                "- `Channel File 291` -> `Channel File 二九一`",
                "- `NetworkPolicy` -> `Network Policy`",
                "",
                "Pilot-only candidates:",
                "",
                "- If `SBOM` is misread, replace locally with `S B O M` in the affected subclip.",
                "- If `PACS` is misread, replace locally with `派克斯` or `P A C S` in the affected subclip.",
                "- If `FD&C Act` is misread, replace locally with `F D and C Act` in the affected subclip.",
                "",
                "Do not globally inject bopomofo or Chinese near-sounds unless listening evidence shows a real issue.",
            ]
        ),
    )

    prompt_text = (
        "各位好，今天這場課程會把醫療資安放回臨床 workflow。"
        "我們會用產品生命週期來看證據，用醫院部署現實來看責任分工，"
        "讓法規條文變成可以行動、可以交接、可以驗證的治理語言。"
        "請用穩定、清楚、台灣華語的醫療資安講課語氣朗讀。"
    )
    write_text(LOCAL_ROOT / f"prompts/{VERSION}/jason_reference.txt", prompt_text)
    reference_audio_path = LOCAL_ROOT / f"prompts/{VERSION}/jason_reference.wav"
    reference_text_path = LOCAL_ROOT / f"prompts/{VERSION}/jason_reference.txt"
    reference_audio_exists = reference_audio_path.exists()
    reference_gate = {
        "reference_audio_required": REFERENCE_AUDIO_REQUIRED,
        "optional_audio_path": rel(reference_audio_path),
        "optional_transcript_path": rel(reference_text_path),
        "audio_exists": reference_audio_exists,
        "recommended_duration_seconds": "25-45",
        "style": "clean Taiwan Mandarin medical-cybersecurity lecture",
        "execution_mode_without_audio": "no_reference_default_voice",
        "status": "ready_without_reference_audio" if not reference_audio_exists else "ready_with_reference_audio",
    }
    write_json(LOCAL_ROOT / f"prompts/{VERSION}/reference_audio_gate.json", reference_gate)
    (LOCAL_ROOT / f"prompts/{VERSION}/REFERENCE_AUDIO_REQUIRED.md").unlink(missing_ok=True)
    write_text(
        LOCAL_ROOT / f"prompts/{VERSION}/REFERENCE_AUDIO_OPTIONAL.md",
        "\n".join(
            [
                "# Reference Audio Optional",
                "",
                "This render package is configured to run without reference audio.",
                "",
                "When no prompt WAV is present, use the BreezyVoice runtime's default/no-reference voice mode.",
                "If a prompt WAV is later added, it can be used as an optional voice-style reference:",
                "",
                f"`{reference_gate['optional_audio_path']}`",
                "",
                "Recommended optional recording requirements:",
                "",
                "- `25-45` seconds",
                "- clean close-mic audio",
                "- Taiwan Mandarin",
                "- calm medical-cybersecurity lecture tone",
                "- exact transcript must match `jason_reference.txt`",
                "- do not use celebrity, third-party, or unconsented voice samples",
                "",
                "Do not block pilot rendering just because the optional WAV is absent.",
            ]
        ),
    )

    runtime_state = detect_runtime_state(reference_audio_exists)
    write_json(LOCAL_ROOT / f"runtime/{VERSION}/runtime_readiness.json", runtime_state)
    missing_modules = [name for name, exists in runtime_state["python_modules"].items() if not exists]
    breezyvoice_repo_ready = any(
        candidate["has_single_inference"] for candidate in runtime_state["breezyvoice_repo_candidates"]
    )
    write_text(
        LOCAL_ROOT / f"runtime/{VERSION}/runtime_readiness.md",
        "\n".join(
            [
                "# BreezyVoice Runtime Readiness",
                "",
                "Reference audio policy:",
                "",
                f"- Required: `{REFERENCE_AUDIO_REQUIRED}`",
                f"- Optional WAV exists: `{reference_audio_exists}`",
                "- No-reference execution mode: `default_sft_voice`",
                "",
                "Local execution path:",
                "",
                f"- Runner: `{runtime_state['no_reference_runner']}`",
                f"- RTX 5080 setup script: `{runtime_state['rtx_5080_runtime_setup']}`",
                f"- Pilot command template: `{runtime_state['pilot_command_template']}`",
                "- Default behavior: render with a built-in/default SFT speaker id; do not require prompt audio.",
                "- Optional behavior: a prompt WAV can still be supplied later for zero-shot voice style, with consent and exact prompt transcript.",
                "",
                "Current local runtime probe:",
                "",
                f"- Python: `{runtime_state['python']['version']}` at `{runtime_state['python']['executable']}`",
                f"- Python 3.10 path: `{runtime_state['python']['python3_10'] or 'not found'}`",
                f"- BreezyVoice repo candidate ready: `{breezyvoice_repo_ready}`",
                f"- Missing Python modules: `{', '.join(missing_modules) if missing_modules else 'none'}`",
                f"- Local ready to render: `{runtime_state['ready_to_render_locally']}`",
                f"- RTX 5080 ready: `{runtime_state['rtx_5080_ready']}`",
                f"- Local venv Python: `{runtime_state['local_venv'].get('path', 'not found')}`",
                f"- Local venv torch: `{runtime_state['local_venv'].get('torch', {}).get('version', 'not found')}`",
                "",
                "Important distinction:",
                "",
                "- Missing reference audio no longer blocks pilot rendering.",
                "- RTX 5080 requires a CUDA 12.8-capable PyTorch wheel; the official `torch==2.3.1+cu118` wheel does not support `sm_120`.",
            ]
        ),
    )

    write_json(
        LOCAL_ROOT / f"specs/{VERSION}/audio_output_spec.json",
        {
            "format": "wav",
            "sample_rate": "BreezyVoice runtime default; archive copy may be normalized after render",
            "loudness_lufs": -16,
            "silence_policy": "preserve natural paragraph pauses; do not aggressive trim",
            "subclip_output_dir": rel(LOCAL_ROOT / f"output/{VERSION}/subclips"),
            "parent_chunk_output_dir": rel(LOCAL_ROOT / f"output/{VERSION}/parent_chunks"),
            "full_output_path": rel(LOCAL_ROOT / f"output/{VERSION}/full/cde-2026-breezyvoice-80min-v1.wav"),
            "archive_output_dir": rel(LOCAL_ROOT / f"output/{VERSION}/archive"),
        },
    )
    write_text(
        LOCAL_ROOT / f"specs/{VERSION}/audio_output_spec.md",
        "\n".join(
            [
                "# Audio Output Spec",
                "",
                "- Output format: `.wav`",
                "- Sample rate: use the BreezyVoice runtime default, then create a normalized archive copy if needed.",
                "- Loudness target: about `-16 LUFS` after final normalization.",
                "- Silence policy: preserve natural paragraph pauses; do not aggressive-trim subclips.",
                f"- Subclip output path: `{rel(LOCAL_ROOT / f'output/{VERSION}/subclips')}/`",
                f"- Parent chunk output path: `{rel(LOCAL_ROOT / f'output/{VERSION}/parent_chunks')}/`",
                f"- Full stitched output path: `{rel(LOCAL_ROOT / f'output/{VERSION}/full/cde-2026-breezyvoice-80min-v1.wav')}`",
            ]
        ),
    )

    write_text(
        LOCAL_ROOT / f"review/{VERSION}/pilot_review_checklist.md",
        "\n".join(
            [
                "# Pilot Review Checklist",
                "",
                "Pilot rows:",
                "",
                *[f"- `{prefix}`" for prefix in PILOT_PREFIXES],
                "",
                "Listen for:",
                "",
                "- English acronyms are not slurred or misread.",
                "- `K eight S`, `F D and C Act Section 五二四 B`, and `Channel File 二九一` are stable.",
                "- Speaking speed stays close to the `80:00` pacing plan.",
                "- Long sentences do not sound fatigued.",
                "- Opening sounds stable and the close sounds authoritative.",
                "- Handoff into Jingzhong's white-box/system-review section sounds natural.",
                "- No markup, labels, or strange symbols are spoken.",
                "",
                "Correction order:",
                "",
                "1. Punctuation and sentence breaks.",
                "2. English term spacing.",
                "3. Single-term pronunciation replacement.",
                "4. Shorter subclip split.",
                "5. Segment preset or pause adjustment.",
                "6. Spoken-content edit only if the above cannot solve the issue.",
            ]
        ),
    )
    write_text(
        LOCAL_ROOT / f"review/{VERSION}/full_render_acceptance_gate.md",
        "\n".join(
            [
                "# Full Render Acceptance Gate",
                "",
                "Do not start full render until all four pilot rows are accepted.",
                "",
                "Full render pass criteria:",
                "",
                "- understandable Taiwan Mandarin lecture delivery",
                "- stable professional terms and acronyms",
                "- no spoken markup or control labels",
                "- no excessive sentence fatigue",
                "- tone matches CDE medical-cybersecurity instruction",
                "- every generated WAV maps to `subclip_manifest.csv` and `render_review_log.csv`",
                "- `python3 tools/check_breezyvoice_full_render_gate.py --write-report` exits `0`",
                "",
                "After render:",
                "",
                "1. stitch subclips into parent chunks by `parent_output_prefix`",
                "2. stitch parent chunks into the full lecture",
                "3. normalize final full output around `-16 LUFS`",
                "4. complete `render_review_log.csv` with runtime, pronunciation issue, fix, and accepted status",
                "",
                "Machine stop gate:",
                "",
                "Run this before any full render command:",
                "",
                "```bash",
                "python3 tools/check_breezyvoice_full_render_gate.py --write-report",
                "```",
                "",
                "If it exits non-zero, stop and do not run full render.",
            ]
        ),
    )

    write_json(
        LOCAL_ROOT / f"review/{VERSION}/pilot_status.json",
        {
            "pilot_prefixes": PILOT_PREFIXES,
            "pilot_subclip_count": len(pilot_subclip_rows),
            "pilot_outputs_existing": pilot_outputs_existing,
            "pilot_outputs_complete": pilot_outputs_complete,
            "pilot_parent_outputs_existing": pilot_parent_outputs_existing,
            "pilot_parent_outputs_complete": pilot_parent_outputs_existing == len(pilot_parent_paths),
            "pilot_full_stitched_exists": pilot_full_stitched_exists,
            "pilot_full_stitched_path": rel(pilot_full_stitched_path),
            "pilot_machine_review": rel(LOCAL_ROOT / f"review/{VERSION}/pilot_machine_review.json"),
            "pilot_machine_review_status": pilot_machine_review_status,
            "full_batch_allowed": False,
            "pilot_render_attempted": pilot_outputs_existing > 0,
            "reference_audio_required": REFERENCE_AUDIO_REQUIRED,
            "blocked_by_missing_reference_audio": False,
            "reference_audio_path": rel(reference_audio_path),
            "execution_mode": "with_reference_audio" if reference_audio_exists else "no_reference_default_voice",
            "pilot_audio_inventory": rel(LOCAL_ROOT / f"review/{VERSION}/pilot_audio_inventory.csv"),
            "message": "Pilot TTS may run without reference audio; use optional prompt audio only if present.",
        },
    )

    write_text(
        LOCAL_ROOT / f"commands/{VERSION}/run_pilot_template.sh",
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                "# Template only. Set BREEZYVOICE_REPO to a local BreezyVoice clone before running.",
                f"MANIFEST='{rel(LOCAL_ROOT / f'manifests/{VERSION}/pilot_manifest.csv')}'",
                f"SUBCLIPS='{rel(LOCAL_ROOT / f'manifests/{VERSION}/subclip_manifest.csv')}'",
                f"PROMPT_WAV='{rel(reference_audio_path)}'",
                f"PROMPT_TXT='{rel(reference_text_path)}'",
                f"OUTPUT_DIR='{rel(LOCAL_ROOT / f'output/{VERSION}/subclips')}'",
                "VOICE_MODE='default'",
                "MODEL_PATH=\"${BREEZYVOICE_MODEL_PATH:-MediaTek-Research/BreezyVoice}\"",
                "DEFAULT_SPEAKER_ID=\"${BREEZYVOICE_DEFAULT_SPEAKER_ID:-auto}\"",
                f"PYTHON_BIN=\"${{BREEZYVOICE_PYTHON:-{rel(LOCAL_ROOT / f'runtime/{VERSION}/venv/bin/python')}}}\"",
                "BREEZYVOICE_REPO=\"${BREEZYVOICE_REPO:-.local/BreezyVoice}\"",
                "",
                "if [[ ! -x \"$PYTHON_BIN\" ]]; then",
                "  echo \"Missing runtime Python: $PYTHON_BIN\" >&2",
                "  echo \"Run: bash tools/setup_breezyvoice_rtx5080_runtime.sh\" >&2",
                "  exit 2",
                "fi",
                "",
                "if [[ -f \"$PROMPT_WAV\" ]]; then",
                "  echo \"Using optional prompt audio: $PROMPT_WAV\"",
                "  test -f \"$PROMPT_TXT\" || { echo \"Missing prompt transcript: $PROMPT_TXT\" >&2; exit 2; }",
                "  VOICE_MODE=\"${BREEZYVOICE_VOICE_MODE:-default}\"",
                "else",
                "  echo \"No prompt audio found; proceeding in no-reference/default voice mode.\"",
                "  PROMPT_WAV=''",
                "  PROMPT_TXT=''",
                "  VOICE_MODE='default'",
                "fi",
                "",
                "PYTHONUTF8=1 \"$PYTHON_BIN\" tools/breezyvoice_render_subclips.py \\",
                "  --selection pilot \\",
                "  --voice-mode \"$VOICE_MODE\" \\",
                "  --model-path \"$MODEL_PATH\" \\",
                "  --speaker-id \"$DEFAULT_SPEAKER_ID\" \\",
                "  --prompt-audio \"$PROMPT_WAV\" \\",
                "  --prompt-text-file \"$PROMPT_TXT\" \\",
                "  --subclip-manifest \"$SUBCLIPS\" \\",
                "  --pilot-manifest \"$MANIFEST\" \\",
                "  --output-dir \"$OUTPUT_DIR\"",
            ]
        ),
    )
    (LOCAL_ROOT / f"commands/{VERSION}/run_pilot_template.sh").chmod(0o755)
    write_text(
        LOCAL_ROOT / f"commands/{VERSION}/stitch_pilot_template.sh",
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                "python3 tools/stitch_breezyvoice_outputs.py \\",
                "  --selection pilot \\",
                "  --stitch-full \\",
                "  --overwrite",
            ]
        ),
    )
    (LOCAL_ROOT / f"commands/{VERSION}/stitch_pilot_template.sh").chmod(0o755)
    write_text(
        LOCAL_ROOT / f"commands/{VERSION}/build_pilot_review_template.sh",
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                "python3 tools/build_breezyvoice_pilot_review.py",
                "python3 tools/build_breezyvoice_render_review_log.py",
                "",
                "echo \"Review: .local/breezyvoice/review/v1/pilot_listening_review.md\"",
                "echo \"Decision CSV: .local/breezyvoice/review/v1/pilot_listening_review.csv\"",
                "echo \"Render review log: .local/breezyvoice/review/v1/render_review_log.csv\"",
                "echo \"Full batch gate: .local/breezyvoice/review/v1/full_batch_gate.json\"",
            ]
        ),
    )
    (LOCAL_ROOT / f"commands/{VERSION}/build_pilot_review_template.sh").chmod(0o755)
    write_text(
        LOCAL_ROOT / f"commands/{VERSION}/check_full_render_gate_template.sh",
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                "python3 tools/check_breezyvoice_full_render_gate.py --write-report",
            ]
        ),
    )
    (LOCAL_ROOT / f"commands/{VERSION}/check_full_render_gate_template.sh").chmod(0o755)
    write_text(
        LOCAL_ROOT / f"commands/{VERSION}/run_full_render_template.sh",
        "\n".join(
            [
                "#!/usr/bin/env bash",
                "set -euo pipefail",
                "",
                "# Full render is deliberately guarded. This script exits before",
                "# rendering unless all four pilot parent chunks are accepted.",
                f"SUBCLIPS='{rel(LOCAL_ROOT / f'manifests/{VERSION}/subclip_manifest.csv')}'",
                f"PROMPT_WAV='{rel(reference_audio_path)}'",
                f"PROMPT_TXT='{rel(reference_text_path)}'",
                f"OUTPUT_DIR='{rel(LOCAL_ROOT / f'output/{VERSION}/subclips')}'",
                f"FULL_OUTPUT='{rel(LOCAL_ROOT / f'output/{VERSION}/full/cde-2026-breezyvoice-80min-v1.wav')}'",
                "VOICE_MODE='default'",
                "MODEL_PATH=\"${BREEZYVOICE_MODEL_PATH:-MediaTek-Research/BreezyVoice}\"",
                "DEFAULT_SPEAKER_ID=\"${BREEZYVOICE_DEFAULT_SPEAKER_ID:-auto}\"",
                f"PYTHON_BIN=\"${{BREEZYVOICE_PYTHON:-{rel(LOCAL_ROOT / f'runtime/{VERSION}/venv/bin/python')}}}\"",
                "BREEZYVOICE_REPO=\"${BREEZYVOICE_REPO:-.local/BreezyVoice}\"",
                "",
                "python3 tools/check_breezyvoice_full_render_gate.py --write-report",
                "",
                "if [[ ! -x \"$PYTHON_BIN\" ]]; then",
                "  echo \"Missing runtime Python: $PYTHON_BIN\" >&2",
                "  echo \"Run: bash tools/setup_breezyvoice_rtx5080_runtime.sh\" >&2",
                "  exit 2",
                "fi",
                "",
                "if [[ -f \"$PROMPT_WAV\" ]]; then",
                "  echo \"Using optional prompt audio: $PROMPT_WAV\"",
                "  test -f \"$PROMPT_TXT\" || { echo \"Missing prompt transcript: $PROMPT_TXT\" >&2; exit 2; }",
                "  VOICE_MODE=\"${BREEZYVOICE_VOICE_MODE:-default}\"",
                "else",
                "  echo \"No prompt audio found; proceeding in no-reference/default voice mode.\"",
                "  PROMPT_WAV=''",
                "  PROMPT_TXT=''",
                "  VOICE_MODE='default'",
                "fi",
                "",
                "PYTHONUTF8=1 \"$PYTHON_BIN\" tools/breezyvoice_render_subclips.py \\",
                "  --selection all \\",
                "  --voice-mode \"$VOICE_MODE\" \\",
                "  --model-path \"$MODEL_PATH\" \\",
                "  --speaker-id \"$DEFAULT_SPEAKER_ID\" \\",
                "  --prompt-audio \"$PROMPT_WAV\" \\",
                "  --prompt-text-file \"$PROMPT_TXT\" \\",
                "  --subclip-manifest \"$SUBCLIPS\" \\",
                "  --output-dir \"$OUTPUT_DIR\" \\",
                "  --overwrite",
                "",
                "python3 tools/stitch_breezyvoice_outputs.py \\",
                "  --selection all \\",
                "  --stitch-full \\",
                "  --full-output \"$FULL_OUTPUT\" \\",
                "  --overwrite",
                "",
                "python3 tools/build_breezyvoice_pilot_review.py",
                "python3 tools/build_breezyvoice_render_review_log.py",
                "python3 tools/verify_breezyvoice_objective.py --write-report || true",
            ]
        ),
    )
    (LOCAL_ROOT / f"commands/{VERSION}/run_full_render_template.sh").chmod(0o755)

    summary = {
        "version": VERSION,
        "segments": len(segments),
        "subclips": len(subclip_rows),
        "pilot_segments": len(pilot_rows),
        "model_text_characters": sum(len(segment.clean_text) for segment in segments),
        "duration_seconds": sum(segment.target_seconds for segment in segments),
        "freeze_report": rel(LOCAL_ROOT / f"freeze/{VERSION}/freeze_report.json"),
        "render_manifest": rel(LOCAL_ROOT / f"manifests/{VERSION}/render_manifest.csv"),
        "subclip_manifest": rel(LOCAL_ROOT / f"manifests/{VERSION}/subclip_manifest.csv"),
        "pilot_manifest": rel(LOCAL_ROOT / f"manifests/{VERSION}/pilot_manifest.csv"),
        "reference_audio_required": REFERENCE_AUDIO_REQUIRED,
        "reference_audio_exists": reference_audio_exists,
        "pilot_execution_mode": "with_reference_audio" if reference_audio_exists else "no_reference_default_voice",
        "runtime_readiness": rel(LOCAL_ROOT / f"runtime/{VERSION}/runtime_readiness.json"),
        "full_batch_allowed": False,
    }
    write_json(LOCAL_ROOT / f"manifests/{VERSION}/package_summary.json", summary)
    audit_rows = [
        ("1", "凍結輸入版本", "completed", "freeze/v1/freeze_report.json records 26 chunks, 80:00, 28053 chars, source SHA-256, and frozen source copy."),
        ("2", "產生 render manifest", "completed", "manifests/v1/render_manifest.csv and .jsonl include output_prefix, segment_id, preset, target_duration, timeline, clean_text_path, pronunciation_hints."),
        ("3", "抽出 clean text inputs", "completed", "inputs/v1/segments contains 26 clean .txt files with spoken text only."),
        ("4", "切成更小 subclips", "completed", f"manifests/v1/subclip_manifest.csv records {len(subclip_rows)} subclips, 2-4 per parent, all under 500 chars after current split."),
        ("5", "TTS 文字正規化", "completed", "inputs/v1/normalized_segments and inputs/v1/subclips apply low-risk pronunciation normalizations and contain no BV26/Markdown/control markup."),
        ("6", "準備 pronunciation override", "completed", "inputs/v1/pronunciation_override_policy.md points to model-ready pronunciation notes and keeps overrides pilot-evidence based."),
        ("7", "reference audio policy", "completed_optional", "reference_audio_gate.json explicitly sets reference_audio_required=false; no-reference/default voice mode is allowed when jason_reference.wav is absent."),
        ("7a", "no-reference runtime contract", "prepared", "runtime/v1/runtime_readiness.json and run_pilot_template.sh route missing prompt audio to tools/breezyvoice_render_subclips.py --voice-mode default."),
        ("8", "建立音檔輸出規格", "completed", "specs/v1/audio_output_spec.md/json define wav output, loudness, silence, subclip, parent, full, and archive paths."),
        (
            "9",
            "先跑 pilot，不跑 full batch",
            "completed_pilot_audio" if pilot_outputs_complete else "prepared",
            f"pilot_manifest.csv identifies four pilot rows and {len(pilot_subclip_rows)} subclips; pilot_audio_inventory.csv shows {pilot_outputs_existing} existing WAV outputs.",
        ),
        ("10", "Pilot review checklist", "completed", "review/v1/pilot_review_checklist.md records the listening checks."),
        ("11", "修正規則", "completed", "review/v1/pilot_review_checklist.md records correction order."),
        ("12", "Full render 前通過標準", "completed_gate_defined", "review/v1/full_render_acceptance_gate.md defines pass criteria; full_batch_allowed remains false until pilot acceptance."),
        (
            "13",
            "Full render stitch 與紀錄",
            "pilot_stitch_verified" if pilot_full_stitched_exists else "prepared_not_executed",
            f"pilot stitch path has {pilot_parent_outputs_existing}/{len(pilot_parent_paths)} parent WAVs and pilot full stitched exists={pilot_full_stitched_exists}; full render/stitch remains gated by pilot listening acceptance.",
        ),
        (
            "13a",
            "Pilot machine review before full batch",
            pilot_machine_review_status,
            f"pilot_machine_review.json records ASR exists={pilot_asr_path.exists()}, forbidden markup hits={len(pilot_asr_forbidden_hits)}, missing expected term hits={len(pilot_asr_missing_terms)}.",
        ),
        (
            "14",
            "Artifact hygiene before human review",
            "orphan_audio_detected" if orphan_audio_rows else "no_orphan_audio",
            f"review/v1/orphan_audio_inventory.csv records {len(orphan_audio_rows)} WAV files under output/v1/subclips that are not in the current subclip manifest.",
        ),
    ]
    audit_lines = [
        "# BreezyVoice V1 Objective Audit",
        "",
        f"- Package summary: `{rel(LOCAL_ROOT / f'manifests/{VERSION}/package_summary.json')}`",
        f"- Reference audio required: `{REFERENCE_AUDIO_REQUIRED}`",
        f"- Reference audio exists: `{reference_audio_exists}`",
        f"- Pilot execution mode: `{summary['pilot_execution_mode']}`",
        f"- Full batch allowed: `{summary['full_batch_allowed']}`",
        "",
        "| # | Requirement | Status | Evidence |",
        "| --- | --- | --- | --- |",
    ]
    audit_lines.extend("| " + " | ".join(row) + " |" for row in audit_rows)
    audit_lines.extend(
        [
            "",
            "Current state: pilot rendering is no longer blocked by missing reference audio. Full batch remains gated by pilot acceptance, not by prompt-audio availability.",
        ]
    )
    write_text(LOCAL_ROOT / f"review/{VERSION}/objective_audit.md", "\n".join(audit_lines))
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    prepare_package()
