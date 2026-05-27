# CDE 2026 BreezyVoice Merged Transcript Workfile

Status: `model-ready expert delivery received`

This file tracks the merge path for the full BreezyVoice transcript and records the `2026-05-27` expert delivery now stored under `model-ready/`.

## Current State

| Segment | Slides / Time | Current source | Model-ready status |
| --- | --- | --- | --- |
| Opening / Prof. Wu framing | `1-5`, about `0-7` min | Expert-delivered clean transcript and batch CSV | Model-ready baseline available |
| Jason hospital and regulation section | `6-20`, about `7-31` min | Expert-delivered clean transcript and batch CSV | Model-ready baseline available |
| Jason attack surface and testing section | `21-34`, about `31-55` min | Expert-delivered clean transcript and batch CSV | Model-ready baseline available |
| Handoff to 靖中 | `34-36`, about `55` min | Expert-delivered clean transcript and batch CSV | Model-ready baseline available |
| 靖中 white-box / deployment section | source deck says `36-final`; CDE plan maps this to about `55-74` min | Expert-delivered clean transcript and batch CSV, with original 靖中 source retained for traceability | Model-ready baseline available |
| Shared close / evidence map | final `4-6` min | Expert-delivered clean transcript and batch CSV | Model-ready baseline available |

## 2026-05-27 Expert Delivery Intake

The TTS expert returned three delivery files, now tracked under `model-ready/`:

| File | Role |
| --- | --- |
| `model-ready/cde-2026-breezyvoice-merged-transcript-clean.txt` | Complete clean transcript. |
| `model-ready/cde-2026-breezyvoice-merged-transcript-batch.csv` | Batch CSV with `26` rows and stable `output_prefix` values. |
| `model-ready/cde-2026-breezyvoice-pronunciation-notes.md` | Focused pronunciation notes for likely TTS misreads. |

Expert-return summary:

- The transcript was rebuilt according to the final PPT order and rhythm, not mechanically concatenated from the source files.
- Jason's first half, Jingzhong's second half, and the shared close are unified into formal Taiwan Mandarin lecture style.
- The handoff between speakers is preserved as a natural transition.
- The CSV `text` field contains only BreezyVoice-readable narration, without slide labels, Markdown headings, tables, source notes, or planning notes.
- Pronunciation notes focus on likely TTS failure points: acronyms, technical terms, event names, and product names.

The current working baseline is the expert-delivered `model-ready/` package. Treat the previous sections in this workfile as traceability for how the source packet was prepared.

## Recommended Merge Output

The merge output now exists in `model-ready/`:

| File | Role |
| --- | --- |
| `model-ready/cde-2026-breezyvoice-merged-transcript-clean.txt` | Final plain text to review before BreezyVoice batching. |
| `model-ready/cde-2026-breezyvoice-merged-transcript-batch.csv` | Batch input mapped to output filenames. |
| `model-ready/cde-2026-breezyvoice-pronunciation-notes.md` | Pronunciation notes for pilot renders and correction. |

## Merge Rule

The merged transcript should be one audience-facing spoken script, not a paste-up of planning notes.

The final PPT is the highest-order pacing source. Use its slide order, transition logic, case density, and closing structure to decide how long each spoken segment should be.

Use this order:

1. Opening and positioning: why this CDE session exists and how it differs from earlier sessions.
2. Jason section: hospital reality, FDA / TFDA lifecycle logic, attack surface, testing vocabulary, finding anatomy, threat-model handoff.
3. Handoff: one short bridge from attack paths and threat modeling into white-box and system review.
4. 靖中 section: use `cde-2026-jingzhong-section-clean.txt` as the base, then align boundaries with `cde-2026-jingzhong-section-timed-source.txt`.
5. Shared close: lifecycle trust, three takeaways, and bridge to the pre/post-test questions.

## Practical Recommendation

Do not generate one `80` minute audio file from one transcript. Keep the merged transcript as a single canonical text file for review and render from the batch rows.

The expert batch already follows the final PPT rhythm. A concept slide, a case slide, and a closing slide should still be checked by listening because TTS pacing can shift after synthesis.

Expert-delivered batch structure:

| Check | Value |
| --- | --- |
| CSV rows | `26` |
| Unique `output_prefix` values | `26` |
| First row | `cde_full_01_opening_positioning_crazyhunter_entry_case` |
| Last row | `cde_full_26_shared_close_test_anchors` |
| Model-facing field | `text` |
| Review / regeneration fields | `group`, `segment`, `output_prefix`, `notes` |

## Readiness Gate

The transcript is BreezyVoice-ready as a text baseline. Production readiness now depends on pilot audio review:

- render the opening row, one acronym-heavy middle row, and the shared close row;
- listen for pacing, pronunciation of English terms, and long-sentence fatigue;
- apply focused punctuation or pronunciation-note changes only where listening evidence shows a problem;
- regenerate affected rows by stable `output_prefix`;
- keep generated audio in `.local/breezyvoice/output/`.
