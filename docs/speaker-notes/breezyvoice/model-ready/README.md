# CDE 2026 BreezyVoice Model-Ready Delivery

Status: `expert-delivered`

This folder owns the current BreezyVoice-ready text package returned by the TTS expert on `2026-05-27`.

Forward workflow note: this file preserves the historical CDE BreezyVoice
render path. Future research-audio acceptance should follow
`docs/tts-methodology/tts-auto-qa-rubric.md`, using ASR back-transcription,
critical-term checks, audio quality checks, chunk consistency, and
hash/provenance as the gate instead of requiring human listening.

The expert output follows the final PPT order and pacing. It is a rewritten full-session transcript, not a direct paste-up of the source text. Jason's first half, Jingzhong's second half, and the shared close are unified into formal Taiwan Mandarin lecture language with a natural handoff.

## Files

| File | Role | Current check |
| --- | --- | --- |
| `cde-2026-breezyvoice-merged-transcript-clean.txt` | Complete clean transcript for human review before rendering. | `475` lines, `28270` characters. |
| `cde-2026-breezyvoice-merged-transcript-batch.csv` | BreezyVoice batch input with stable `output_prefix` values. | `26` rows, `26` unique output prefixes. |
| `cde-2026-breezyvoice-pronunciation-notes.md` | Focused pronunciation notes for acronyms, technical terms, event names, and product names. | `87` lines. |
| `cde-2026-breezyvoice-80min-engineered-transcript-v1-zh-tw.md` | `80` minute engineering draft that wraps the expert-delivered merged transcript with `BV26` metadata, pacing, pronunciation, pilot-render gates, and positive-scope spoken tuning. | `26` `BV26` chunks, `80:00` timing plan. |

## Batch Contract

The CSV columns are:

```text
group,segment,output_prefix,text,notes
```

Use only the `text` column as the model narration input. It is designed to contain spoken text only, without slide labels, Markdown headings, tables, source notes, or planning notes.

The `output_prefix` column is stable so individual clips can be regenerated without replacing the full audio package.

For an `80` minute controlled render, use `cde-2026-breezyvoice-80min-engineered-transcript-v1-zh-tw.md` as the orchestrator-facing draft. Strip `BV26` / `BV26_META` markup before sending text into the model, and keep the stable `output_prefix` values for per-row regeneration. Reference audio is optional; if no prompt WAV is present, run pilot rendering in no-reference / default-voice mode. The local runner path for that policy is `tools/breezyvoice_render_subclips.py --voice-mode default`.

The render package generator keeps the v1 source frozen and applies only
model-facing sanitation: known stage cues, filler tokens, low-confidence
demonstratives such as `這個` / `那個`, hesitant sounds, and hallucination
residue are removed from generated TTS inputs. It also inserts `、` at every
Chinese-English boundary in model-facing text so mixed Mandarin/English terms
do not merge during synthesis. Except for necessary English proper nouns,
product names, event names, and standard acronyms, model-facing TTS wording
should use Taiwan Traditional Chinese customary phrasing rather than ordinary
English phrases. Preserve `token` and `namespace` as English technical terms.
If a generated clip becomes unstable, first
repair the model-facing text with shorter sentences, clearer sentence breaks,
isolated technical terms, and removal of duplicated repeated passages before
using audio-only fixes. The full-session delivery target is now approximately
`70` minutes. After raw stitching, compute one global tempo factor from
`raw_duration_seconds / 4200` and apply that factor to the master copy; avoid
per-section speed changes unless a specific defect requires repair. Case-study
model-facing text should be written as concise Taiwan Traditional Chinese
storytelling: setup, event path, clinical implication, and review takeaway,
while preserving necessary proper nouns and standard acronyms. After the partial-accept
returned expert review and final6/final6b repair, the plan uses `133`
full-session subclips and `53` pilot subclips: `19` for `cde_full_01`, `9` for
`cde_full_16`, `11` for `cde_full_20`, and `14` for the accepted
`cde_full_26` baseline. The prompt-mode pilot is split into short subclips to
reduce long-sentence attention failures and isolate returned-review defects.
The pilot template overwrites selected pilot WAVs to avoid pairing revised text
with stale audio.

On RTX 5080, run `bash tools/setup_breezyvoice_rtx5080_runtime.sh` before rendering. The official BreezyVoice requirement uses a CUDA `11.8` PyTorch wheel that does not support RTX 5080 / `sm_120`; the local setup script replaces it with a CUDA `12.8` PyTorch runtime and keeps all runtime files under `.local/`.

After pilot rendering, use `tools/stitch_breezyvoice_outputs.py --selection pilot --stitch-full` to verify the subclip-to-parent and parent-to-combined stitch path before any full batch render.

For `cde_full_16_k8s_review_controls`, the returned expert review identified a
runtime-compression failure and later tight RBAC / CI-CD / K8S boundary
problems. The current final6 repair applies safer model-facing technical
anchors, finer boundaries, and
`tools/apply_breezyvoice_audio_pacing.py --tempo 0.88` after synthesis,
bringing the current stitched runtime ratio to about `0.89`. Archive originals
remain local-only under `.local/breezyvoice/output/v1/archive/`.

For `cde_full_26_shared_close_test_anchors`, the latest returned expert review
accepted the chunk. The current package preserves that accepted audio as the
continuity baseline and rerenders only the rejected chunks.

For the historical CDE v1 pilot workflow, `tools/build_breezyvoice_pilot_review.py`,
`tools/build_breezyvoice_render_review_log.py`, and
`tools/build_breezyvoice_pilot_correction_matrix.py` remain as traceability
helpers. For future research-audio workflow, replace the old listening table
with an automated QA summary under `qa/tts-auto-checks/` that records ASR
back-transcription, critical-term accuracy, audio quality, chunk consistency,
and hash/provenance.

The old expert export helper,
`python3 tools/export_breezyvoice_expert_review_package.py --overwrite`, is
retained for historical reproducibility. Future handoff packages should expose
public-safe QA summaries and checksums, while keeping generated audio and
reference audio in local/private storage.

All future BreezyVoice QA for this repo should use
`MediaTek-Research/Breeze-ASR-25` unless a replacement ASR model is explicitly
recorded in the experiment card. Do not use Whisper for the current
BreezyVoice QA path. The historical review workflow treated ASR as a warning
signal; the forward research workflow treats ASR plus lexicon, audio quality,
chunk consistency, and provenance as the auto / semi-auto gate.

Before any new TTS run or text-conditioning change, append a record with
`tools/record_breezyvoice_experiment.py`. The tracked log lives at
`docs/speaker-notes/breezyvoice/cde-2026-breezyvoice-tts-experiment-log-v1.md`
and can be cross-referenced from the public-safe experiment cards under
`logs/tts-experiments/`. Future runs should stop on failed automated QA rather
than wait for human listening decisions.

For the historical CDE v1 full-render template, run
`python3 tools/check_breezyvoice_full_render_gate.py --write-report`. The command
must exit `0`; otherwise the old full render remains closed. For future
research-audio packages, use `docs/tts-methodology/tts-auto-qa-rubric.md`; a
failed or incomplete QA result means text repair, audio repair, chunk repair,
provenance repair, or model rerun before acceptance.

Once the gate opens, run
`bash .local/breezyvoice/commands/v1/run_full_render_template.sh`. The template
checks the gate again before rendering, renders all manifest-listed subclips,
and stitches the final WAV to
`.local/breezyvoice/output/v1/full/cde-2026-breezyvoice-80min-v1.wav`.

Returned expert review CSVs should be ingested with
`tools/ingest_breezyvoice_expert_review.py`. The tool requires explicit
`accept` or `reject` decisions for the four pilot parent chunks before it will
update the local gate.

## Next Gate

Run a pilot render before producing the full set:

1. Render the first row: `cde_full_01_opening_positioning_crazyhunter_entry_case`.
2. Render one acronym-heavy row from the technical middle section.
3. Render the last row: `cde_full_26_shared_close_test_anchors`.
4. Listen for pacing, acronym pronunciation, sentence fatigue, and handoff smoothness.
5. Apply only evidence-backed punctuation or pronunciation adjustments, then regenerate the affected row.

Generated audio stays local under:

```text
.local/breezyvoice/output/
```
