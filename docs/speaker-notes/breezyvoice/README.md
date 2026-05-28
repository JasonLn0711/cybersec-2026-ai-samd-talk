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
| `cde-2026-breezyvoice-tts-experiment-log-v1.md` / `.jsonl` | Durable experiment log for every TTS text-conditioning, render, stitch, ASR, review-package, and human-gate decision. |

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

## RTX 5080 Runtime

For local RTX 5080 rendering, use:

```bash
bash tools/setup_breezyvoice_rtx5080_runtime.sh
python3 tools/prepare_breezyvoice_render_package.py
bash .local/breezyvoice/commands/v1/run_pilot_template.sh
python3 tools/stitch_breezyvoice_outputs.py --selection pilot --stitch-full --overwrite
python3 tools/build_breezyvoice_pilot_review.py
python3 tools/build_breezyvoice_render_review_log.py
python3 tools/build_breezyvoice_pilot_correction_matrix.py
```

The setup script keeps the official BreezyVoice clone and Python venv under `.local/`, then replaces the official `torch==2.3.1+cu118` runtime with a CUDA `12.8` PyTorch build that supports RTX 5080 / `sm_120`.

`tools/prepare_breezyvoice_render_package.py` applies model-facing sanitation
before subclip generation: known stage cues, filler tokens, low-confidence
demonstratives such as `這個` / `那個`, hesitant sounds, and hallucination
residue are removed from TTS inputs while the frozen source stays unchanged.
For mixed Mandarin/English output, the model-facing text must insert `、` at
every Chinese-English boundary before rendering. Except for necessary English
proper nouns, product names, event names, and standard acronyms, model-facing
TTS wording should use Taiwan Traditional Chinese customary phrasing rather
than ordinary English phrases. Preserve `token` and `namespace` as English
technical terms. If a clip becomes unstable,
repair the model-facing text first by making the wording simpler, splitting
long sentences, adding clear sentence breaks, and isolating technical terms;
delete duplicated repeated passages before rerendering. Post-synthesis audio
edits are secondary. The full-session delivery target is now approximately
`70` minutes. After raw stitching, compute one global tempo factor from
`raw_duration_seconds / 4200` and apply that factor to the master copy; avoid
per-section speed changes unless a specific defect requires repair. Case-study
passages should be model-conditioned as concise Taiwan Traditional Chinese
storytelling: setup, event path, clinical implication, and review takeaway.
The goal is a confident teacher sharing a concrete case with listeners, not a
dense English technical list.
The generated pilot template overwrites pilot WAVs so revised text cannot be
silently paired with stale audio.

When reference audio is present, the generated templates use prompt mode by
default while keeping no-reference mode available. Prompt-mode experiments
should be run through `tools/run_with_gpu_telemetry.py` so stdout, GPU samples,
wall time, peak memory, and GPU-only Wh estimates are captured with the render.
The current reference-audio telemetry appendix is
`cde-2026-breezyvoice-reference-audio-telemetry-2026-05-28.md`.

Current full-session package is `EXP-20260528-18`. After the final7 repair,
the owner explicitly allowed proceeding without another listening-review round
while preserving the returned expert-review history. The local full-render gate
therefore records `accepted_by_owner_override=true` and
`accepted_by_listening=false`.

The full run rendered `146` prompt-mode subclips on RTX 5080, then stitched all
`26` parent chunks into:

```text
.local/breezyvoice/output/v1/full/cde-2026-breezyvoice-80min-v1.wav
.local/breezyvoice/output/v1/full/cde-2026-breezyvoice-80min-v1.loudnorm-22050.wav
```

The stitched full WAV is `4402.124 s` (`73.37 min`), mono `22050 Hz`, with
SHA-256 `0b7b85f9df3673a56a15143ffa90ddf5a324ad529b5c76aaeacea8c2d4288545`.
The 22.05 kHz loudness-normalized copy has SHA-256
`917592bce31027911509865bb7dd484a4a67bff9ac08a4252f4cc9d8589212f6`.
The `cde_full_16_k8s_review_controls` subclips keep the post-synthesis
`atempo=0.88` pacing override, and the final close subclip keeps the `0.8 s`
tail trim.

Post-render auxiliary ASR used `MediaTek-Research/Breeze-ASR-25` on CUDA only;
no Whisper ASR was used for this release step. The ASR output is an auxiliary
warning signal and does not replace the owner release decision.

All current auxiliary ASR for this project must use
`MediaTek-Research/Breeze-ASR-25`; do not use Whisper for current BreezyVoice
review gates. Breeze-ASR-25 output is still only an auxiliary warning signal
and is not an acceptance source for mixed Mandarin/English medical
cybersecurity audio.

Pilot review artifacts stay local under `.local/breezyvoice/review/v1/`, including `pilot_audio_inventory.csv`, `pilot_parent_stitch_inventory.csv`, `pilot_stitch_summary.json`, `pilot_machine_review.md`, `pilot_listening_review.csv`, `render_review_log.csv`, `pilot_correction_matrix.md`, and `full_batch_gate.json`. Rebuild `render_review_log.csv` and `pilot_correction_matrix.md` after any stitch, expert-review ingestion, or rerender so runtime, issue, fix, accepted status, and stop-gate source stay aligned.

## Experiment Logging Rule

Every TTS experiment must be recorded before the next render or full-batch
decision. Use:

```bash
python3 tools/record_breezyvoice_experiment.py --experiment-id EXP-YYYYMMDD-NN --stage <stage> --title "<title>" --decision "<decision>"
```

The record must explain the reason, expected effect, affected chunks, commands,
log paths, outputs, machine result, human result if any, fix applied, next
action, and stop rule. If human listening is required, export a fresh package to
`~/Downloads` with `python3 tools/export_breezyvoice_expert_review_package.py
--overwrite`, record that directory/archive in the experiment log, and stop
before any full render until the human review returns accepted decisions.

Before any full render attempt, run:

```bash
python3 tools/check_breezyvoice_full_render_gate.py --write-report
```

Only a zero exit code means the full render gate is open. A non-zero exit means
the next action is human listening review or the next expert-specified pilot
repair, not full rendering.

After all four pilot parent chunks are accepted, use the guarded full-render
template generated by `tools/prepare_breezyvoice_render_package.py`:

```bash
bash .local/breezyvoice/commands/v1/run_full_render_template.sh
```

That script runs the full-render gate checker before rendering all subclips,
then stitches parent chunks and the final
`.local/breezyvoice/output/v1/full/cde-2026-breezyvoice-80min-v1.wav`.

## Returned Expert Review

When the expert returns `forms/expert_pilot_review_form.csv`, ingest it with:

```bash
python3 tools/ingest_breezyvoice_expert_review.py --input ~/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/forms/expert_pilot_review_form.csv
```

The ingester refuses blank or partial required decisions by default. It updates
the local pilot listening table, rebuilds `full_batch_gate.json`, and reruns the
machine full-render stop gate. Full rendering may start only if all four parent
chunks have `accept` and `tools/check_breezyvoice_full_render_gate.py` exits
`0`.
