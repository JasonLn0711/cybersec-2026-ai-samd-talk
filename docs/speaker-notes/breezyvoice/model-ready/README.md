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

## Batch Contract

The CSV columns are:

```text
group,segment,output_prefix,text,notes
```

Use only the `text` column as the model narration input. It is designed to contain spoken text only, without slide labels, Markdown headings, tables, source notes, or planning notes.

The `output_prefix` column is stable so individual clips can be regenerated without replacing the full audio package.

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
