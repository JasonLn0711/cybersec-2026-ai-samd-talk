# 02 Evaluation System

Purpose: keep talk scoring, slide constraints, and generated evaluation outputs in one place.

First principle: evaluate the delivered talk before evaluating slide polish. A beautiful deck cannot rescue a weak narrative, and a strong narrative still needs slides constrained into clarity.

## Layers

| Layer | Evaluates | Method | Output |
| --- | --- | --- | --- |
| Speech score | Narrative, substance, timing, delivery, presence, and impact. | Strict `100`-point rubric. | Rehearsal score and repair priorities. |
| Slide gate | Slide clarity, density, layout, public safety, and AI-feel risk. | Hard constraints, penalties, and optional multiplier. | Pass/fail list and redesign queue. |
| Optimization loop | The highest-leverage failures. | Rewrite only failed/high-risk slides. | Next deck repair pass. |

Do not merge these layers into one generic checklist.

## 100-Point Speech Rubric

| Category | Points | Excellent Evidence | Deduct When |
| --- | ---: | --- | --- |
| Structure and Narrative Design | 20 | Arc is clear: product scale -> evidence -> governance -> testing -> Patch SLA -> implementation. | Sections feel interchangeable or the close introduces new content. |
| Content Depth and Value | 20 | FDA 524B, FDA 2025, TFDA-facing SaMD thinking, AI stack, testing, and Patch SLA become usable decisions. | Regulations or tools are named without operational translation. |
| Stage Rhythm and Time Control | 15 | Slide 7 ends near `14:00`, slide 14 starts by `27:40`, finish by `28:30`. | The regulatory middle expands and the ending gets rushed. |
| Delivery Quality | 15 | Short sentences, precise terms, no apology for complexity, cut markers used under pressure. | Speaker reads, hedges, or adds examples after slide 10. |
| Visual Design | 10 | Meaning is visible in three seconds; diagrams carry logic. | Slides require paragraph reading or decorative imagery. |
| Stage Presence | 10 | Controlled stance, eye contact on anchor lines, silence used intentionally. | Speaker turns away, wanders, or rushes the memory moments. |
| Audience Impact | 10 | Audience remembers product scale, Patch SLA, `30 / 60 / 90`, and trust-before-audit. | Interesting but not actionable. |

Scoring rule: award points only for observed delivery evidence. Do not score intention, preparation effort, or file completeness unless it is visible in the delivered talk.

## Scoring Caps

| Condition | Maximum |
| --- | ---: |
| Evaluator cannot state the talk arc in one sentence. | Structure <= `14/20` |
| FDA/TFDA/NIST are named without operational translation. | Content <= `13/20` |
| Slide 14 starts after `28:00`. | Rhythm <= `10/15` |
| Speaker reads slide text for more than one major slide. | Delivery <= `10/15` |
| Any major slide requires paragraph reading. | Visual <= `7/10` |
| Speaker turns away during slide 10 or slide 12 anchor line. | Presence <= `7/10` |
| Audience cannot recall product scale, Patch SLA, or `30 / 60 / 90`. | Impact <= `6/10` |

## Score Bands

| Band | Score | Meaning | Required Fix |
| --- | ---: | --- | --- |
| Excellent | `90-100` | Conference-ready. | Polish delivery and slide-level clarity only. |
| Strong | `80-89` | Professional talk with visible weaknesses. | Fix the lowest category before adding content. |
| Acceptable | `70-79` | Understandable but not high-impact. | Repair structure, timing, and slide density first. |
| Weak | `60-69` | Content exists but is not conference-ready. | Simplify deck and rebuild narrative path. |
| Poor | `<60` | Not ready. | Rebuild from thesis, map, evidence chain, and Patch SLA. |

## Slide Hard Constraints

These rules are non-negotiable for the public deck.

| Constraint | Rule | Fail Condition |
| --- | --- | --- |
| One-message rule | Exactly one controlling idea per slide, except the required disclaimer. | Slide tries to teach two unrelated ideas. |
| Text limit rule | Max `12` words of headline/sentence text; preferred under `8`. | Sentence blocks, paragraph subtitles, or multiple explanatory callouts. |
| Diagram-label exception | Technical labels may exceed the headline budget only as visual labels. | Labels become sentence explanations. |
| Visual dominance rule | At least `70%` of each slide is visual structure or whitespace. | Text occupies the slide or the visual object is decorative. |
| Bullet limit rule | No more than `2` bullets; prefer `0`. | Three or more bullet lines. |
| Immediate comprehension rule | Point should be understandable in under `3` seconds. | Evaluator must read line by line before seeing the message. |
| Public-safety rule | No private hospital/client detail, proprietary code, student records, exploit recipes, or patent-sensitive mechanisms. | Any sensitive detail appears on screen. |

Allowed layout types:

- Big statement: slides 3, 10, 14.
- Full visual: required disclaimer.
- Contrast: slides 8, 9, 11.
- Diagram: slides 4, 5, 6, 7, 12.
- Progressive build: slides 4, 5, 6, 7, 12, 13.

If a slide does not fit one of these types, it is probably a weak concept.

## Anti-AI And Public-Safety Checks

Redesign a slide when any of these are true:

- It looks like generic template reuse.
- The same layout repeats more than `3` slides in a row.
- It uses stock-style hacker imagery, AI-brain imagery, or dramatic hospital imagery.
- Text-heavy explanation replaces visual structure.
- Random icon grids appear before the thinking is clear.
- The slide exposes private, proprietary, student, exploit-ready, or patent-sensitive material.

Safety boundary rule: any actual private hospital/client detail, raw student record, proprietary code, exploit recipe, or patent-sensitive implementation mechanic shown in the public deck is at least a major deduction and may be critical.

## Slide Penalty Model

The speech score remains the official `100`-point score. Slide constraints adjust it afterward.

```text
Final Adjusted Score = Speech Score - Slide Penalties
```

| Violation | Penalty |
| --- | ---: |
| Minor visual inconsistency | `-1` |
| Minor density issue on one slide | `-1` to `-2` |
| Hard-rule failure on one non-critical slide | `-3` |
| Major AI-feel / generic-template risk | `-3` to `-5` |
| Major text overload on an important slide | `-5` |
| Critical slide failure: text-heavy, no structure, or unreadable | `-10` |
| Public-safety boundary violation | `-10` minimum and immediate redesign |

Optional multiplier after penalties:

| Condition | Multiplier |
| --- | ---: |
| Excellent slides: no hard failures, no more than `2` minor issues, strong hierarchy. | `x1.05`, capped at `100` |
| Adequate slides: no hard failures, some minor inconsistency. | `x1.00` |
| Weak slides: `1-3` hard failures or repeated AI-feel risk. | `x0.95` |
| Poor slides: `4+` hard failures, repeated text overload, or no visual system. | `x0.90` |

Cap rule: if more than `4` slides fail hard constraints, the deck is not conference-ready regardless of adjusted score.

## Generated Evaluation Outputs

Regenerate from `data/presentation_os.json`:

```bash
python3 tools/generate_presentation_outputs.py
```

| File | Role |
| --- | --- |
| `outputs/current/evaluation_report.md` | Baseline and optimized macro scoring, strengths, weaknesses, and second-pass improvement. |
| `outputs/current/scoring_report.csv` | Spreadsheet-ready score report with `Category,Score,MaxScore,Strengths,Weaknesses,Evidence`. |
| `outputs/current/slide_constraint_report.md` | Hard-rule report, baseline violations, optimized gate status, and redesign priority. |
| `outputs/current/slide_validation.csv` | Spreadsheet-ready gate report with `SlideID,PassFail,Violations,Severity`. |

Interpretation rule: `scoring_report.csv` records the optimized second-pass category scores. Baseline score and adjusted readiness score stay in `evaluation_report.md`.

## Rehearsal Scoring Note

```text
Run date:
Version scored:
Total speech score:
Slide penalty / multiplier:
Final adjusted score:

Top 3 strengths:
1.
2.
3.

Top 3 deductions:
1. Category / slide / evidence / severity / fix:
2. Category / slide / evidence / severity / fix:
3. Category / slide / evidence / severity / fix:

Timing checkpoints:
- Slide 3:
- Slide 7:
- Slide 10:
- Slide 12:
- Slide 14:
- Finish:

Next repair pass:
```
