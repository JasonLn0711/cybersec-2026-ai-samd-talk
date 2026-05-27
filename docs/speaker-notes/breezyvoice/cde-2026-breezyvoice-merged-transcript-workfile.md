# CDE 2026 BreezyVoice Merged Transcript Workfile

Status: `not model-ready yet`

This file tracks the merge path for the full BreezyVoice transcript. The current repo has 靖中的 section extracted and synced, but the full all-session BreezyVoice transcript has not been merged yet.

## Current State

| Segment | Slides / Time | Current source | Model-ready status |
| --- | --- | --- | --- |
| Opening / Prof. Wu framing | `1-5`, about `0-7` min | CDE prep note slide design and speaker lines | Needs spoken draft |
| Jason hospital and regulation section | `6-20`, about `7-31` min | CDE prep note slide design and Jason content spine | Needs spoken draft |
| Jason attack surface and testing section | `21-34`, about `31-55` min | CDE prep note slide design and Jason content spine | Needs spoken draft |
| Handoff to 靖中 | `34-36`, about `55` min | CDE prep note plus 靖中 clean text opening | Needs bridge edit |
| 靖中 white-box / deployment section | source deck says `36-final`; CDE plan maps this to about `55-74` min | `cde-2026-jingzhong-section-clean.txt` and `cde-2026-jingzhong-section-timed-source.txt` | Usable as first TTS base after slide-boundary cleanup |
| Shared close / evidence map | final `4-6` min | CDE prep note slide `45`, draft pre/post-test questions, and 靖中 final summary | Needs spoken draft |

## Recommended Merge Output

Create these files when the merge is ready:

| File | Role |
| --- | --- |
| `cde-2026-breezyvoice-merged-transcript-clean.txt` | Final plain text to review before BreezyVoice batching. |
| `cde-2026-breezyvoice-merged-transcript-batch.csv` | Batch input mapped to output filenames. |
| `cde-2026-breezyvoice-pronunciation-notes.md` | Pronunciation and bopomofo hints discovered during pilot renders. |

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

Do not generate one `80` minute audio file from one transcript. Keep the merged transcript as a single canonical text file for review, then split it into small batch rows for BreezyVoice.

Build the batch rows after checking the final PPT. A concept slide, a case slide, and a closing slide should not use the same spoken rhythm.

First batch structure:

| Group | Segment | Status |
| --- | --- | --- |
| `00` | Opening / session positioning | draft needed |
| `01` | Jason hospital reality | draft needed |
| `02` | Jason FDA / TFDA lifecycle logic | draft needed |
| `03` | Jason attack surface paths | draft needed |
| `04` | Jason testing / finding / threat-model handoff | draft needed |
| `05` | Handoff to 靖中 | draft needed |
| `06` | 靖中 white-box scope | source available |
| `07` | 靖中 device / FDA evidence examples | source available |
| `08` | 靖中 deployment / K8S / Change Healthcare | source available |
| `09` | 靖中 traceability / testing / 524B | source available |
| `10` | 靖中 remediation / SBOM / vulnerability response | source available |
| `11` | 靖中 logging / recovery / close | source available |
| `12` | Shared final close and test-question bridge | draft needed |

## Readiness Gate

The transcript becomes BreezyVoice-ready only when:

- every segment is written as spoken prose;
- slide labels, planning bullets, tables, and source notes are removed from the model input;
- the whole script has one consistent speaking voice;
- English technical terms are intentionally retained or given pronunciation hints;
- batch rows are short enough to regenerate individually;
- the final clean transcript and batch CSV are both tracked in git.
