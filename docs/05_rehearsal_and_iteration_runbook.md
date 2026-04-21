# 05 Rehearsal And Iteration Runbook

Purpose: turn the scoring rubric into a practical rehearsal and repair system for the compact `14`-slide CYBERSEC deck.

## 1. Review Sequence

| Pass | When | Goal | Output |
| --- | --- | --- | --- |
| Draft structure review | Before editing slides | Confirm thesis, map, evidence chain, Patch SLA, close. | Structural repair list. |
| Slide constraint review | After first compact deck build | Enforce pass/fail slide constraints and penalties from `06_slide_design_constraint_system.md`. | Redesign queue. |
| Script review | Before first timed rehearsal | Ensure each slide has a speakable point and cut marker. | Cue-card draft. |
| Dry run | First timed run alone | Find timing and language failures. | Rubric score and timing log. |
| Live rehearsal | With peer evaluator | Test audience comprehension and stage presence. | Evidence-based scoring sheet. |
| Final readiness review | Before conference delivery | Confirm no safety boundary issues and no rushed close. | Go/no-go decision. |

## 2. First-Draft Review Checklist

Use this before polishing visual details:

- [ ] Slide 3 says `你賣的不是模型` and makes trust/patch/evidence explicit.
- [ ] Slide 5 clearly shows four product scales.
- [ ] Slide 6 uses `Risk -> Control -> Test -> Fix -> Evidence`.
- [ ] Slide 7 connects model evidence, governance language, and AI stack.
- [ ] Slide 10 remains a standalone patient-safety peak.
- [ ] Slide 12 makes `Decision` visually and verbally central.
- [ ] Slide 13 gives a credible `30 / 60 / 90` path.
- [ ] Slide 14 contains no new framework or extra content.

Rubric gate: if any of these fail, do not spend time on visual polish yet. Repair Structure and Narrative Design first.

## 3. Slide Constraint Review Checklist

- [ ] Run every slide through `06_slide_design_constraint_system.md`.
- [ ] Each slide has exactly one controlling message.
- [ ] Headline/sentence text stays under `12` words unless the slide is the required disclaimer.
- [ ] Technical labels are labels, not sentence explanations.
- [ ] At least `70%` of each slide is visual structure or whitespace.
- [ ] Each slide uses an allowed layout: big statement, full visual, contrast, diagram, or progressive build.
- [ ] No layout pattern repeats more than `3` slides in a row.
- [ ] Slide 12's `Decision` node is visually dominant.
- [ ] No decorative AI/security imagery competes with the message.
- [ ] No sensitive public-safety boundary is violated.

Gate: if any slide has a hard failure, redesign that slide before timed rehearsal. Do not try to solve slide-density problems by speaking faster.

## 4. Dry-Run Checklist

Record slide timestamps:

| Checkpoint | Target | Actual | Action If Late |
| --- | ---: | ---: | --- |
| Slide 3 starts | `0:30` |  | Cut title/disclaimer chatter. |
| Slide 5 starts | `4:30` |  | Cut slide 4 detail. |
| Slide 7 ends | `14:00` |  | Cut slide 7 to one sentence per column. |
| Slide 10 starts | `19:20` |  | Compress slides 8-9. |
| Slide 12 starts | `23:00` |  | Cut slide 11 examples. |
| Slide 14 starts | `27:40` |  | Slide 13 one output per bucket. |
| Finish | `28:30` |  | Use safe version next run. |

After the run, score only these five items first:

1. Can the thesis be remembered?
2. Did the product-scale map become clear?
3. Did regulation become an evidence chain rather than a legal block?
4. Did Patch SLA feel like the climax?
5. Did the close land before the clock pressure became visible?

## 5. Live Rehearsal Checklist

Ask the evaluator to write answers before giving opinions:

| Question | What A Good Answer Contains |
| --- | --- |
| What was the talk's central thesis? | Not model; trustable, patchable, auditable system. |
| What was the map? | Model, Viewer, Platform/Database, Connected Medical System. |
| What does regulation require in this talk? | Evidence chain: risk, control, test, fix, evidence. |
| What is the operational climax? | Patch SLA; every finding needs a decision. |
| What should a small team do next? | 30 inventory, 60 workflow, 90 validation. |

If an evaluator cannot answer one of these, repair the corresponding slide before improving delivery polish.

## 6. Self-Evaluation Worksheet

```text
Run version:
Run length:
Slide 7 end time:
Slide 14 start time:

Which line landed best?
Which slide felt too dense?
Where did I start explaining instead of deciding?
Where did I speak faster instead of cutting?
What is the one repair before the next run?
```

## 7. Peer-Review Worksheet

```text
Evaluator:
Total score:

Strongest slide:
Weakest slide:

Evidence of clarity:
Evidence of confusion:
Evidence of credibility:
Evidence of weak pacing:

Most important fix:
```

## 8. Score-Band Repair Order

### Below 70

Do not polish slides. Repair the talk spine:

1. Rebuild slides 3, 5, 6, 12, and 14 first.
2. Remove secondary examples from slides 7-11.
3. Rehearse only the transition sentences until the arc is clear.
4. Use the `20:00` emergency path once to find the essential talk.

### 70-80

The talk is understandable but not conference-ready:

1. Reduce visual density.
2. Tighten regulatory section to evidence-chain logic.
3. Practice cut markers.
4. Score timing again before adding any detail.

### 80-90

The talk is strong enough to refine:

1. Improve slide 6 and slide 12 wording.
2. Add silence after the major lines.
3. Make visual style more consistent.
4. Improve final minute so it feels intentional, not merely finished.

### 90+

The difference is control:

1. The speaker lands strong lines without rushing.
2. The audience can repeat the map and Patch SLA after the talk.
3. The deck looks serious without looking overloaded.
4. The final slide contains only the principle and a clean stop.

## 9. Timing Variants For Rehearsal

| Version | Target | How To Run It |
| --- | ---: | --- |
| Normal | `28:30` | Full compact script with planned pauses. |
| Safe | `27:30` | Cut secondary examples from slides 7, 8, 9, and 11. |
| Rushed | `25:00` | Slide 6 evidence chain only; slide 13 one output per bucket. |
| Emergency | `20:00` | Skip slides 4 and 11 as standalone sections. |

Rehearsal rule: practice the safe version at least twice before the final normal run. The speaker should know the cuts before needing them.

## 10. Final Readiness Checklist

- [ ] The deck has exactly `14` slides.
- [ ] Slide 2 is the required CYBERSEC disclaimer and is not treated as narrative content.
- [ ] The deck has passed the slide constraint system with no hard failures.
- [ ] The talk finishes by `28:30` in at least two consecutive runs.
- [ ] The speaker can deliver slides 3, 6, 10, 12, and 14 without looking back.
- [ ] The evaluator score is at least `85`.
- [ ] No slide includes private hospital/client detail, student data, proprietary code, exploit recipe, or patent-sensitive implementation mechanics.
- [ ] The final slide ends with the trust-before-audit principle and no new content.

## 11. Post-Rehearsal Repair Log

Use this table after each scored run:

| Date | Version | Score | Timing Issue | Lowest Category | Repair Made | Next Run Target |
| --- | --- | ---: | --- | --- | --- | --- |
|  |  |  |  |  |  |  |
