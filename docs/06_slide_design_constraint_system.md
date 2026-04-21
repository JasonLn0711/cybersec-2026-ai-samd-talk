# 06 Slide Design Constraint System

Purpose: enforce strict slide-level design quality for the CYBERSEC 2026 deck without confusing slide execution with the macro `100`-point speech evaluation rubric.

This file is the second evaluation layer:

```text
Layer 1: Speech Evaluation System
-> 100-point macro score for talk quality

Layer 2: Slide Design Constraint System
-> pass/fail gates, penalties, and redesign priorities for visual execution
```

The key principle:

`Great talks are not only good content. They are content constrained into clarity.`

## 1. First-Principles Separation

| Layer | Evaluates | Method | Output |
| --- | --- | --- | --- |
| Speech Evaluation System | Narrative, substance, timing, delivery, presence, impact | `100`-point rubric | Talk score and rehearsal priorities |
| Slide Design Constraint System | Slide clarity, visual discipline, density, layout, non-generic design | Hard gates plus penalties | Pass/fail list and redesign queue |
| Optimization Engine | Worst-slide repair | Rewrite only failed/high-risk slides | New title, reduced text, visual concept |

Do not let slide rules replace the speech rubric. Slides can make a strong talk stronger, but a beautiful deck cannot compensate for weak narrative, weak technical substance, or poor timing.

## 2. Hard Constraints

These rules are non-negotiable. A slide that fails any hard constraint is not production-ready.

| Constraint | Rule | Applies To | Fail Condition |
| --- | --- | --- | --- |
| One-message rule | Exactly one controlling idea per slide. | Every slide except required disclaimer. | Slide tries to teach two unrelated ideas or carries both a framework and a roadmap. |
| Text limit rule | Max `12` words of headline/sentence text; preferred under `8`. | Titles, subtitles, callouts, footers. | Slide uses a sentence block, explanatory paragraph, or multiple subtitles. |
| Diagram-label exception | Technical labels may exceed the `12`-word headline budget only when they function as visual labels. | Architecture, evidence-chain, testing, Patch SLA slides. | Labels become sentence explanations, dense lists, or require reading instead of seeing. |
| Visual dominance rule | At least `70%` of the slide is visual structure or whitespace. | Every designed slide. | Text occupies the slide or the visual object is decorative. |
| Bullet limit rule | No more than `2` bullets; prefer `0`. | Every slide. | Three or more bullet lines appear. |
| Immediate comprehension rule | The audience should understand the slide's point in under `3` seconds. | Every slide. | Evaluator must read labels line by line before seeing the message. |
| Public-safety rule | No private hospital/client detail, proprietary code, student records, exploit recipes, or patent-sensitive mechanisms. | Every public slide. | Any sensitive detail appears on screen. |

## 3. Design Consistency Rules

These rules prevent the deck from feeling AI-generated or template-heavy.

| Rule | Constraint | Violation Signal |
| --- | --- | --- |
| Typography | Max `2` fonts; one title style, one label/body style. | Mixed font personalities or random emphasis. |
| Accent color | Max `1` primary accent plus one risk color. | Multiple saturated accents with no semantic meaning. |
| Grid | Use a consistent alignment grid. | Elements appear manually scattered. |
| Spacing | Use consistent spacing intervals. | Margins, gaps, and label distances change without reason. |
| Diagram grammar | Same visual meaning uses same shape. | A risk node, process node, and product layer look arbitrary. |

Minor consistency breaks are not automatic redesigns, but repeated inconsistency creates a major AI-feel risk.

## 4. Allowed Layout Types

Each slide must use one of these layout types.

| Type | Use For | CYBERSEC Slides |
| --- | --- | --- |
| Big statement | Memory anchors and emotional peaks. | 3, 10, 14 |
| Full visual | Required disclaimer or single semantic image/diagram. | 2 |
| Contrast | Compare two scopes, test types, or risk states. | 8, 9, 11 |
| Diagram | Architecture, evidence chain, governance stack, finding flow. | 4, 5, 6, 7, 12 |
| Progressive build | Reveal a process or stack one layer at a time. | 4, 5, 6, 7, 12, 13 |

If a slide does not fit one of these five types, it is probably a weak slide concept.

## 5. Anti-AI Detection Rules

Reject or redesign a slide when any of these are true:

| Detection | Why It Hurts | Severity |
| --- | --- | --- |
| Looks like a generic template reuse | Weakens premium conference credibility. | Major |
| Same layout repeats more than `3` slides in a row | Creates visual fatigue and AI-generated feel. | Moderate to major |
| Uses stock-style hacker, AI brain, or dramatic hospital image | Signals decoration instead of expertise. | Major |
| Text-heavy explanation replaces visual structure | Breaks timing and makes speaker read. | Critical |
| No visual concept | Slide becomes a teleprompter. | Major |
| Random icon grid | Looks designed before thinking. | Major |
| Over-polished marketing style | Weakens technical seriousness. | Moderate |

## 6. Slide Penalty Model

The speech score remains the official `100`-point score. Slide constraints modify that score only after the macro evaluation is complete.

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

Cap rule: if more than `4` slides fail hard constraints, the deck is not conference-ready regardless of adjusted score.

## 7. Slide Quality Multiplier

Use the multiplier only after the penalty pass.

| Condition | Multiplier |
| --- | ---: |
| Excellent slides: no hard failures, no more than `2` minor issues, strong visual hierarchy, premium conference feel | `x1.05` |
| Adequate slides: no hard failures, some minor visual inconsistency | `x1.00` |
| Weak slides: `1-3` hard failures or repeated AI-feel risk | `x0.95` |
| Poor slides: `4+` hard failures, repeated text overload, or no visual system | `x0.90` |

Multiplier rule: do not let the multiplier push a score above `100`.

## 8. Compact Deck Constraint Profile

| Slide | Layout Type | Text Budget | Visual Requirement | Failure Risk |
| ---: | --- | --- | --- | --- |
| 1 | Big statement | Title/subtitle only | Quiet authority; no credential clutter | Over-introduction |
| 2 | Full visual | Official image only | Required disclaimer as compliance beat | Added commentary |
| 3 | Big statement | `<8` words preferred | Phrase dominates | Diluting thesis |
| 4 | Diagram | Headline plus stack labels | Stack plus care-disruption line | Trend recap |
| 5 | Diagram / build | Headline plus four layer labels | Four-scale ladder | Threat-list overload |
| 6 | Diagram / build | Headline plus evidence nodes | Evidence chain dominates | Legal text block |
| 7 | Diagram | Three column labels | TFDA / NIST / AI-stack bridge | Control catalog |
| 8 | Contrast | Panel labels only | Model vs Viewer comparison | UI screenshot distraction |
| 9 | Contrast | Panel labels only | Platform vs Connected System | Private topology risk |
| 10 | Big statement | `<6` words | Full-screen phrase | Adding framework |
| 11 | Contrast | One line per side | Inside-out vs outside-in | Tool catalog |
| 12 | Diagram / build | One phrase plus flow labels | `Decision` is dominant | Ticket-system clutter |
| 13 | Progressive build | Three short time buckets | `30 / 60 / 90` roadmap | Unrealistic list |
| 14 | Big statement | One closing sentence | Quiet final principle | New content |

## 9. Evaluation Output Format

Use this format for a deck review:

```text
Deck version:
Evaluator:
Speech score before slide adjustment:

Slide constraint summary:
- Hard failures:
- Minor violations:
- Major violations:
- Critical violations:
- Total penalty:
- Multiplier:
- Final adjusted score:

Redesign priority:
1. Slide / violation / severity / required action
2. Slide / violation / severity / required action
3. Slide / violation / severity / required action
```

Per-slide record:

| Slide | PASS / FAIL | Violations | Severity | Penalty | Redesign Required |
| ---: | --- | --- | --- | ---: | --- |
| 1 |  |  |  |  |  |
| 2 |  |  |  |  |  |
| 3 |  |  |  |  |  |
| 4 |  |  |  |  |  |
| 5 |  |  |  |  |  |
| 6 |  |  |  |  |  |
| 7 |  |  |  |  |  |
| 8 |  |  |  |  |  |
| 9 |  |  |  |  |  |
| 10 |  |  |  |  |  |
| 11 |  |  |  |  |  |
| 12 |  |  |  |  |  |
| 13 |  |  |  |  |  |
| 14 |  |  |  |  |  |

## 10. Optimization Engine Prompt

Use this prompt when reviewing generated or edited slides:

```text
You are a strict slide design evaluator using Apple-style design principles.

Your role is not to give suggestions first.
Your role is to enforce constraints.

For each slide, check:

1. One-message rule
2. Text length rule: max 12 words of headline/sentence text, with technical diagram labels allowed only when they function as visual labels
3. Visual dominance: at least 70% visual structure or whitespace
4. Layout type validity: big statement, full visual, contrast, diagram, or progressive build
5. AI-feel detection: template reuse, repeated structure, generic imagery, text-heavy explanation, no visual concept
6. Public-safety boundary: no private hospital/client detail, proprietary code, student data, exploit recipe, or patent-sensitive mechanism

Output for each slide:
- PASS / FAIL
- Violations
- Severity: minor / major / critical
- Penalty
- Redesign required: yes / no

Then output:
1. Total hard failures
2. Total minor / major / critical violations
3. Total penalty
4. Slide quality multiplier
5. Final adjusted score from the supplied speech score
6. Slides requiring redesign in priority order

Then rewrite only the worst failed slides:
- new title
- reduced text
- allowed layout type
- visual concept
- what to remove
```

