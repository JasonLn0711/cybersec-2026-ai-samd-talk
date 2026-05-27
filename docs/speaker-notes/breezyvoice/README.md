# BreezyVoice Working Files

This folder owns the tracked, syncable text inputs for BreezyVoice production.

## Boundary

- Tracked in git: source DOCX files, extracted text transcripts, batch plans, pronunciation notes, and command notes.
- Local only: generated audio, prompt audio, model cache, temporary WAV files, and failed render attempts.
- Local-only workspace: `.local/breezyvoice/`.

## Current Files

| File | Role |
| --- | --- |
| `source/講稿.docx` | 靖中的 original speaker-script DOCX with slide labels and timing structure. |
| `source/純文字板.docx` | 靖中的 original clean-text DOCX. |
| `cde-2026-jingzhong-section-clean.txt` | First BreezyVoice text base extracted from `source/純文字板.docx`. |
| `cde-2026-jingzhong-section-timed-source.txt` | Timing and slide-reference text extracted from `source/講稿.docx`. |
| `cde-2026-jingzhong-section-batch-plan.csv` | Planned output groups for batch rendering and review. |
| `cde-2026-breezyvoice-merged-transcript-workfile.md` | Current merge-status file for the all-session BreezyVoice transcript. It is not model-ready yet. |
| `expert-package-source/` | TTS expert handoff notes, full transcript source bundle, and full-session batch outline. |

## Production Rule

Use the clean text as the spoken source. Use the timed source to recover slide boundaries, pacing, and section ownership. Keep the LINE transcript and collaboration notes in the CDE prep note, not in the spoken audio script.

The full BreezyVoice transcript is not merged yet. Build it as `cde-2026-breezyvoice-merged-transcript-clean.txt` after Jason's first-half spoken draft and the shared close are written.

Generated audio should go to:

```text
.local/breezyvoice/output/
```

Prompt audio should go to:

```text
.local/breezyvoice/prompts/
```
