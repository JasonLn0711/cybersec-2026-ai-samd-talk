# TTS Methodology Notes

This folder keeps talk-specific TTS methodology records for the CYBERSEC / CDE
medical-cybersecurity audio-production lane.

The reusable cross-project TTS research-audio methodology now lives in:

```text
../nycu-114-2-smart-biomedicine-final-report/docs/tts-methodology/
```

Use this repo for:

- CDE / CYBERSEC model-facing transcript decisions.
- BreezyVoice runtime, render, stitch, ASR warning, and handoff traceability.
- Talk-specific pronunciation, timing, and local-private audio boundaries.

Use the Smart Biomedicine repo for:

- reusable auto / semi-auto TTS QA methodology.
- `tools/run_tts_auto_qa.py`.
- cross-project reproducibility notes.
- shared templates for experiment cards, rights manifests, lexicons, and runtime
  manifests.

## Current Bridge

- `tts-cybersec-cde-experience-bridge.md`: concise bridge from the CDE
  BreezyVoice production evidence to the reusable research-audio workflow.
- `tts-research-audio-methodology-v1-zh-tw.md`: local methodology snapshot from
  the first TTS documentation pass.
- `tts-auto-qa-rubric.md`: local automated QA rubric snapshot.
- `tts-text-design-guide.md`: local model-facing text design rules.
- `tts-failure-taxonomy.md`: local failure taxonomy.
- `tts-ethics-rights-and-disclosure.md`: local rights/disclosure record shape.
- `tts-model-comparison-summary.md`: CYBERSEC-side model comparison and
  backfill status.

## Local-Only Boundary

Generated audio, prompt audio, reference voice, failed samples, model caches,
and review workbooks stay under `.local/`, `assets/tts-local-only/`, Downloads,
or other private storage. Tracked files should contain methods, commands,
hashes, QA summaries, and repo-safe locator notes only.
