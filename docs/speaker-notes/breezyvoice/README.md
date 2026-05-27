# BreezyVoice Working Files

This folder owns the tracked, syncable text inputs for BreezyVoice production.

## Boundary

- Tracked in git: source DOCX files, extracted text transcripts, batch plans, pronunciation notes, and command notes.
- Local only: generated audio, prompt audio, model cache, temporary WAV files, and failed render attempts.
- Local-only workspace: `.local/breezyvoice/`.

## Current Files

| File | Role |
| --- | --- |
| `model-ready/` | Current expert-delivered full-session BreezyVoice transcript, batch CSV, and pronunciation notes. This is the baseline for pilot rendering. |
| `source/講稿.docx` | 靖中的 original speaker-script DOCX with slide labels and timing structure. |
| `source/純文字板.docx` | 靖中的 original clean-text DOCX. |
| `cde-2026-jingzhong-section-clean.txt` | First BreezyVoice text base extracted from `source/純文字板.docx`. |
| `cde-2026-jingzhong-section-timed-source.txt` | Timing and slide-reference text extracted from `source/講稿.docx`. |
| `cde-2026-jingzhong-section-batch-plan.csv` | Planned output groups for batch rendering and review. |
| `cde-2026-breezyvoice-merged-transcript-workfile.md` | Merge-status and delivery-intake file for the all-session BreezyVoice transcript. |
| `expert-package-source/` | TTS expert handoff notes, full transcript source bundle, and full-session batch outline. |

## Production Rule

Use `model-ready/cde-2026-breezyvoice-merged-transcript-batch.csv` as the clean rendering baseline. Use the `text` column as BreezyVoice input and keep metadata columns for review, routing, and regeneration.

Use `model-ready/cde-2026-breezyvoice-80min-engineered-transcript-v1-zh-tw.md` when the render needs the richer `BV26` control layer from the earlier `60` minute script: `80:00` pacing, per-segment preset, pronunciation hints, pilot-render gates, and post-generation review checks. Reference audio is optional; absence of a prompt WAV should use no-reference / default-voice mode rather than block pilot rendering. The prepared local runner is `tools/breezyvoice_render_subclips.py --voice-mode default`.

Use the earlier clean and timed source files as traceability companions. Keep the LINE transcript and collaboration notes in the CDE prep note, not in the spoken audio script.

Generated audio should go to:

```text
.local/breezyvoice/output/
```

Prompt audio should go to:

```text
.local/breezyvoice/prompts/
```
