# CDE 2026 BreezyVoice TTS Expert Brief

## Project Context

This packet supports an `80` minute CDE / TFDA-oriented lecture:

`臨床端對醫療器材 / 資訊系統之資安要求`

The audience is expected to include medical-device, electronic-industry, academic, regulatory, QA/RA, and healthcare-system stakeholders. The talk should sound like a serious clinical cybersecurity lecture, not a commercial voiceover, hacker demo, or AI hype talk.

## Goal For The TTS Expert

Please turn the supplied source material into a BreezyVoice-ready transcript and batch plan.

The current package is a complete source packet, not a final model-ready input. The most important expert work is:

- merge Jason's front-half source into spoken prose;
- align 靖中的 back-half clean transcript with the final PPT;
- design transcript pacing from the final PPT slide order, message density, transitions, and case rhythm;
- add a short natural handoff between Jason and 靖中;
- write a shared close that connects lifecycle trust, evidence, and the three pre/post-test questions;
- split the finished script into small, reviewable BreezyVoice batches;
- add pronunciation notes for English technical terms and any Chinese terms the pilot render misreads.

## Current Material Status

| Material | Status |
| --- | --- |
| Final PPT | Available in `01_deck/`. |
| 靖中 original DOCX files | Available in `03_original_sources/` and already extracted into text. |
| 靖中 clean transcript | Strong first TTS base for the back half. |
| Jason front half | Source notes and speaker lines exist; needs conversion into complete spoken prose. |
| Shared close | Source notes exist; needs final spoken draft. |
| Final BreezyVoice clean transcript | Not created yet. |
| Final BreezyVoice batch CSV | Not created yet. |

## Recommended Output Files

Please produce:

- `cde-2026-breezyvoice-merged-transcript-clean.txt`
- `cde-2026-breezyvoice-merged-transcript-batch.csv`
- `cde-2026-breezyvoice-pronunciation-notes.md`
- optional: `pilot-render-review-notes.md`

## Speaking Style

Use Taiwan Mandarin as the main speaking language. Keep standard English technical terms where natural:

`White-box Testing`, `black-box testing`, `penetration testing`, `SBOM`, `K8S`, `DICOM`, `HL7`, `FHIR`, `PACS`, `HIS`, `EMR`, `FDA`, `TFDA`, `524B`, `Log4Shell`, `MOVEit`, `CrowdStrike`, `Change Healthcare`.

The voice should be:

- professional;
- calm;
- lecture-like;
- technically credible;
- clear for non-cybersecurity healthcare / regulatory listeners.

## Pacing Rule

Use the final PPT in `01_deck/` as the highest-order pacing source. The transcript should follow the slide order, transition logic, case density, and closing structure of that deck.

For each slide, decide whether it is a transition, concept, case, workflow, or close slide. Then shape the spoken text accordingly:

- transition slides should be short and directional;
- concept slides should carry one core sentence and one explanation block;
- case slides should move from incident path to clinical / governance meaning to takeaway;
- workflow slides should sound like a process, not a table being read aloud;
- closing slides should slow down and reinforce lifecycle trust and evidence chain.

Avoid:

- sales pitch tone;
- dramatic threat narration;
- exploit-tutorial language;
- long legal reading;
- dense bullet-list narration;
- putting slide labels into spoken audio.

## BreezyVoice Handling Notes

Recommended workflow:

1. Create one canonical clean transcript for human review.
2. Split into batch rows of roughly `800-1200` Chinese characters for first-pass rendering.
3. Generate pilot clips first:
   - one easy explanatory paragraph;
   - one technical paragraph with English terms;
   - one case-heavy paragraph.
4. Add bopomofo hints only for terms that fail in pilot rendering.
5. Export individual `.wav` clips, not one full `80` minute file.

Generated audio, prompt audio, and model cache should stay local-only.

## Key Boundary

The talk is public-safe. Do not add private hospital, client, student, credential, proprietary implementation, or exploit-ready details.

## Suggested Narrative Order

1. Opening / CDE session positioning.
2. Jason: hospital reality and patient-safety impact.
3. Jason: FDA / TFDA lifecycle evidence logic.
4. Jason: attack surface and testing vocabulary.
5. Jason: finding anatomy and threat-model handoff.
6. Bridge to 靖中.
7. 靖中: white-box, evidence, deployment, K8S, SBOM, remediation, logging, recovery.
8. Shared close: lifecycle trust and three test-question anchors.
