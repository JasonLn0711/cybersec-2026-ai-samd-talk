# 03 Rehearsal Workflow

Purpose: turn the compact deck, script, and evaluation system into a low-friction rehearsal loop.

First principle: rehearse to find the next constraint, not to keep polishing everything. Each run should produce one repair target.

## Operating Loop

| Step | When | Action | Output |
| ---: | --- | --- | --- |
| 1 | Before slide edits | Read `docs/01_talk_design.md` and confirm the promise, memory anchors, timing, and public-safety boundary. | Talk spine locked. |
| 2 | Before rebuilding outputs | Edit `data/presentation_os.json` only when generated reports or deck text need to change. | Single source updated. |
| 3 | After JSON edits | Run `python3 tools/generate_presentation_outputs.py`. | Reports and CSVs aligned. |
| 4 | When the deck must change | Run `node tools/build_optimized_deck.mjs` if `@oai/artifact-tool` is available. | Editable `14`-slide PPTX. |
| 5 | Before timed rehearsal | Apply `docs/02_evaluation_system.md` slide gates. | Redesign queue or pass. |
| 6 | First timed run | Speak the deck with cut markers, record checkpoints. | Timing log and weak spots. |
| 7 | After each run | Score using `docs/02_evaluation_system.md`. | One next repair target. |
| 8 | Final pass | Confirm no public-safety issue, no rushed close, and no hard slide failures. | Go/no-go decision. |

## First-Draft Gate

Do this before visual polish:

- [ ] Slide 3 says `你賣的不是模型` and makes trust/patch/evidence explicit.
- [ ] Slide 5 clearly shows four product scales.
- [ ] Slide 6 uses `Risk -> Control -> Test -> Fix -> Evidence`.
- [ ] Slide 7 connects model evidence, governance language, and AI stack.
- [ ] Slide 10 remains a standalone patient-safety peak.
- [ ] Slide 12 makes `Decision` visually and verbally central.
- [ ] Slide 13 gives a credible `30 / 60 / 90` path.
- [ ] Slide 14 contains no new framework or extra content.

Gate: if any item fails, repair structure before improving visual style.

## Slide-Gate Checklist

- [ ] Exactly one controlling message per slide.
- [ ] Headline/sentence text stays under `12` words, except required disclaimer.
- [ ] Technical labels are labels, not sentence explanations.
- [ ] At least `70%` of each slide is visual structure or whitespace.
- [ ] Each slide uses an allowed layout: big statement, full visual, contrast, diagram, or progressive build.
- [ ] No layout pattern repeats more than `3` slides in a row.
- [ ] Slide 12's `Decision` node is visually dominant.
- [ ] No decorative AI/security imagery competes with the message.
- [ ] No public-safety boundary is violated.
- [ ] Slide 6 says `Monitor / CVD / Patch / SBOM`, while the speaker explains FDA 524B as monitor, identify, address, coordinated vulnerability disclosure, updates/patches, and SBOM.
- [ ] Slide 7 keeps AI RMF language separate from CSF 2.0 language; do not collapse both into an incomplete NIST function list.
- [ ] Slide 12 treats `Patch SLA` as this talk's operating model, not as a quoted FDA term.

Gate: if any slide has a hard failure, redesign that slide before timed rehearsal. Do not solve slide-density problems by speaking faster.

## Dry-Run Checkpoints

| Checkpoint | Target | Actual | Action If Late |
| --- | ---: | ---: | --- |
| Slide 3 starts | `0:30` |  | Cut title/disclaimer chatter. |
| Slide 5 starts | `4:30` |  | Cut slide 4 detail. |
| Slide 7 ends | `14:00` |  | Cut slide 7 to one sentence per column. |
| Slide 10 starts | `19:20` |  | Compress slides 8-9. |
| Slide 12 starts | `23:00` |  | Cut slide 11 examples. |
| Slide 14 starts | `27:40` |  | Slide 13 becomes one output per bucket. |
| Finish | `28:30` |  | Use safe version next run. |

After the run, answer only five questions first:

1. Can the thesis be remembered?
2. Did the product-scale map become clear?
3. Did regulation become an evidence chain rather than a legal block?
4. Did Patch SLA feel like the climax?
5. Did the close land before clock pressure became visible?

## Peer-Review Questions

Ask the evaluator to answer these before giving opinions:

| Question | Good Answer Contains |
| --- | --- |
| What was the talk's central thesis? | Not model; trustable, patchable, auditable system. |
| What was the map? | Model, Viewer, Platform/Database, Connected Medical System. |
| What does regulation require in this talk? | Evidence chain: risk, control, test, fix, evidence. |
| What is the operational climax? | Patch SLA; every finding needs a decision. |
| What should a small team do next? | 30 inventory, 60 workflow, 90 validation. |

If an evaluator cannot answer one of these, repair the corresponding slide before polishing delivery.

## Self-Evaluation Note

```text
Run version:
Run length:
Slide 7 end time:
Slide 14 start time:

Which line landed best?
Which slide felt too dense?
Where did I explain instead of deciding?
Where did I speak faster instead of cutting?
What is the one repair before the next run?
```

## Repair Order By Score

### Below 70

Do not polish slides. Repair the talk spine:

1. Rebuild slides 3, 5, 6, 12, and 14.
2. Remove secondary examples from slides 7-11.
3. Rehearse transition sentences until the arc is clear.
4. Run the `20:00` emergency path once to find the essential talk.

### 70-80

The talk is understandable but not conference-ready:

1. Reduce visual density.
2. Tighten regulatory section to evidence-chain logic.
3. Practice cut markers.
4. Score timing again before adding detail.

### 80-90

The talk is strong enough to refine:

1. Improve slide 6 and slide 12 wording.
2. Add silence after major lines.
3. Make visual style more consistent.
4. Improve the final minute so it feels intentional.

### 90+

The difference is control:

1. Land strong lines without rushing.
2. Make the audience able to repeat the map and Patch SLA.
3. Keep the deck serious without overload.
4. End on the principle and stop.

## Timing Variants

| Version | Target | Rule |
| --- | ---: | --- |
| Normal | `28:30` | Full compact script with planned pauses. |
| Safe | `27:30` | Cut secondary examples from slides 7, 8, 9, and 11. |
| Rushed | `25:00` | Slide 6 evidence chain only; slide 13 one output per bucket. |
| Emergency | `20:00` | Skip slides 4 and 11 as standalone sections. |

Rehearsal rule: practice the safe version at least twice before the final normal run.

## Final Readiness

- [ ] The deck has exactly `14` slides.
- [ ] Slide 2 is the required CYBERSEC disclaimer and is not treated as narrative content.
- [ ] The deck has passed the slide gate with no hard failures.
- [ ] The talk finishes by `28:30` in at least two consecutive runs.
- [ ] The speaker can deliver slides 3, 6, 10, 12, and 14 without looking back.
- [ ] Evaluator score is at least `85`.
- [ ] No slide includes private hospital/client detail, student data, proprietary code, exploit recipe, or patent-sensitive implementation mechanics.
- [ ] The final slide ends with the trust-before-audit principle and no new content.

## Repair Log

| Date | Version | Score | Timing Issue | Lowest Category | Repair Made | Next Run Target |
| --- | --- | ---: | --- | --- | --- | --- |
|  |  |  |  |  |  |  |
