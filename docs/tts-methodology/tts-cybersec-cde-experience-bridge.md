# CYBERSEC / CDE BreezyVoice TTS Experience Bridge

日期：2026-05-31
範圍：CDE / CYBERSEC 醫療資安長篇台灣華語 TTS production 經驗。
Canonical cross-project note：
`../nycu-114-2-smart-biomedicine-final-report/docs/tts-methodology/tts-reproducible-research-notes-cybersec-smart-biomedicine-v1-zh-tw.md`

## Decision

This talk repo keeps the CDE / CYBERSEC evidence trail. The reusable research
audio workflow, runnable auto-QA gate, and cross-project reproducibility note
live in the Smart Biomedicine repo.

The reason is first-principles ownership:

```text
planning-everything-track = why / when / priority / status / capacity
cybersec-2026-ai-samd-talk = what the talk says / shows / scores / rehearses
nycu-114-2-smart-biomedicine-final-report = reusable TTS auto-QA workflow and shared methodology
```

## Evidence Pointers

- Full experiment log:
  `docs/speaker-notes/breezyvoice/cde-2026-breezyvoice-tts-experiment-log-v1.md`
- BreezyVoice working folder:
  `docs/speaker-notes/breezyvoice/README.md`
- Model-ready text package:
  `docs/speaker-notes/breezyvoice/model-ready/README.md`
- Backfilled experiment card:
  `logs/tts-experiments/EXP-20260528-001.md`
- Local methodology snapshot:
  `docs/tts-methodology/tts-research-audio-methodology-v1-zh-tw.md`

## Production Lessons To Carry Forward

1. Text conditioning comes before audio repair.
2. For CJK-English boundaries, insert `、` before rendering so English medical
   and cybersecurity terms do not merge into adjacent Chinese phrasing.
3. Preserve standard technical terms such as `token` and `namespace`; rewrite
   ordinary English phrases into Taiwan Traditional Chinese.
4. Case-study passages should use short setup, event path, clinical
   implication, and review takeaway.
5. Use a single global tempo factor after raw stitching when targeting a full
   session duration. Avoid section-by-section speed changes unless fixing a
   documented defect.
6. Breeze-ASR-25 remains the current warning / back-transcription path for this
   Taiwan Mandarin BreezyVoice workflow. Any replacement ASR must be recorded
   in the experiment card.
7. The legacy CDE route has strong production evidence, but future research use
   should rerun the full auto-QA package before claiming `accepted_auto_gate`.

## Current Research-Grade Status

```text
status: accepted_with_warnings_for_legacy_production_evidence
reason: command, runtime, prompt-mode render, ASR warning pass, hashes, loudnorm,
        pacing, and handoff package are documented; CER / WER, alias-aware
        term_error_list.csv, consolidated audio_quality_report.json, and rights
        manifest are not yet complete for the legacy long-form output.
next_gate: rerun or backfill with the Smart Biomedicine auto-QA schema before
           future research-stimulus reuse.
```

## Privacy Boundary

Do not commit:

- generated WAV / MP3 / M4A / MP4 files
- prompt WAVs
- reference voice
- failed samples
- model cache
- local review packets containing audio

Tracked docs may record:

- method
- command
- model id / revision if known
- output SHA256
- ASR transcript locator
- QA result locator
- rights status
- delivery package locator
