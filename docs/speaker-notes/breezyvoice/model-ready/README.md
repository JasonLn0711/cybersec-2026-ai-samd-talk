# CDE 2026 BreezyVoice Model-Ready Delivery

Status: `expert-delivered`

This folder owns the current BreezyVoice-ready text package returned by the TTS expert on `2026-05-27`.

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
residue are removed from generated TTS inputs. After the total-reject returned
expert review and final5b repair, the plan uses `127` full-session subclips and
`47` pilot subclips: `12` for `cde_full_01`, `10` for `cde_full_16`, `11` for
`cde_full_20`, and `14` for `cde_full_26`. The prompt-mode pilot is split into
short subclips to reduce long-sentence attention failures and isolate
returned-review defects. The pilot template overwrites pilot WAVs to avoid
pairing revised text with stale audio.

On RTX 5080, run `bash tools/setup_breezyvoice_rtx5080_runtime.sh` before rendering. The official BreezyVoice requirement uses a CUDA `11.8` PyTorch wheel that does not support RTX 5080 / `sm_120`; the local setup script replaces it with a CUDA `12.8` PyTorch runtime and keeps all runtime files under `.local/`.

After pilot rendering, use `tools/stitch_breezyvoice_outputs.py --selection pilot --stitch-full` to verify the subclip-to-parent and parent-to-combined stitch path before any full batch render.

For `cde_full_16_k8s_review_controls`, the returned expert review identified a
runtime-compression failure around `0.73` and follow-up K8S/RBAC/API
terminology collapse. The current final5b repair applies safer model-facing
technical anchors, finer subclip splitting, and
`tools/apply_breezyvoice_audio_pacing.py --tempo 0.82` after synthesis,
improving the current stitched runtime ratio to about `0.91`. Archive originals
remain local-only under `.local/breezyvoice/output/v1/archive/`.

For `cde_full_26_shared_close_test_anchors`, the final5b repair trims `0.8`
seconds from the final thank-you subclip tail after synthesis to reduce the
reported tail-residue risk while preserving the spoken close.

Then run `tools/build_breezyvoice_pilot_review.py` and
`tools/build_breezyvoice_render_review_log.py`, followed by
`tools/build_breezyvoice_pilot_correction_matrix.py`. The first tool creates
the local listening decision table and `full_batch_gate.json`; the second
consolidates manifest rows, parent WAV runtime, pronunciation issue, fix
status, accepted state, and review source into `render_review_log.csv`; the
third gives reviewers a chunk-level issue-to-fix matrix. The full batch stays
blocked until all four pilot parent rows are accepted by listening.

To hand the current pilot outputs to a TTS expert, run `python3 tools/export_breezyvoice_expert_review_package.py --overwrite`. The exporter copies the four required parent WAVs, the stitched pilot WAV, the manifest-listed pilot subclips, matching model text, manifests, ASR notes, runtime logs, GPU telemetry, pacing and tail-trim logs, the expert prompt, experiment log, and a fillable review CSV into `~/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/`, then creates a `.tar.gz` next to it.

Before any new TTS run or text-conditioning change, append a record with
`tools/record_breezyvoice_experiment.py`. The tracked log lives at
`docs/speaker-notes/breezyvoice/cde-2026-breezyvoice-tts-experiment-log-v1.md`
and is included in every expert review export. If a new run produces a human
review gate, export a fresh copy to `~/Downloads` and stop until human decisions
are returned.

Before a full render command, run
`python3 tools/check_breezyvoice_full_render_gate.py --write-report`. The command
must exit `0`; otherwise the full render remains closed and the next action is
human listening review or the next expert-specified pilot repair.

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
