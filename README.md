# CYBERSEC 2026 AI SaMD Talk

Canonical repository for the CYBERSEC 2026 speech-delivery package:

`AI 軟體醫材的資安實戰：從美國 FDA 524B 規範到 Threat Modeling 與 Patch SLA 的完整落地`

This repo owns the presentation design system, compact slide specification, stage script, scoring rubric, slide constraint layer, and rehearsal process. It exists because CYBERSEC talk preparation is a standalone professional delivery project, not a TA grading artifact.

## First-Principles Boundary

| Question | Decision |
| --- | --- |
| What is the artifact? | A public conference talk package for CYBERSEC 2026. |
| Who uses it? | Speaker, deck editor, rehearsal reviewer, and evaluator. |
| What must it optimize? | Clarity, credibility, timing, memorability, and rubric-aligned delivery. |
| Where should it live? | In this dedicated sibling repo, not inside `ns-practice-ta-grading-2026s`. |
| What does the planning repo do? | Holds project context, source anchors, deck artifacts, and a handoff link to this repo. |
| What should not happen? | Do not mix speech-delivery artifacts with student grading, raw submissions, or unrelated course evaluation records. |

Recommended working model:

`planning-everything-track` = project operating context and source anchors.

`cybersec-2026-ai-samd-talk` = canonical talk design, rehearsal, and evaluation package.

## Canonical Files

| File | Use It For | Primary Output |
| --- | --- | --- |
| [`docs/01_strategy_and_rubric_alignment.md`](docs/01_strategy_and_rubric_alignment.md) | Talk positioning, audience promise, narrative, timing, visual strategy, rubric translation | Design decisions |
| [`docs/02_compact_14_slide_deck_spec.md`](docs/02_compact_14_slide_deck_spec.md) | Build-ready slide plan for the recommended compact deck | Exact slide production spec |
| [`docs/03_speaker_script_and_stage_rhythm.md`](docs/03_speaker_script_and_stage_rhythm.md) | Taiwan Traditional Chinese delivery script, rhythm map, cue cards, stage behavior | Rehearsal script |
| [`docs/04_scoring_rubric.md`](docs/04_scoring_rubric.md) | Strict `100`-point evaluator framework and scoring sheet | Evaluation form |
| [`docs/05_rehearsal_and_iteration_runbook.md`](docs/05_rehearsal_and_iteration_runbook.md) | Review passes, dry runs, fix-order by score band, final readiness | Iteration system |
| [`docs/06_slide_design_constraint_system.md`](docs/06_slide_design_constraint_system.md) | Pass/fail slide design gates, penalties, multiplier, and redesign prompt | Slide quality firewall |

## Working Order

1. Lock the audience promise and timing with [`docs/01_strategy_and_rubric_alignment.md`](docs/01_strategy_and_rubric_alignment.md).
2. Build or revise the deck from [`docs/02_compact_14_slide_deck_spec.md`](docs/02_compact_14_slide_deck_spec.md).
3. Run the slide gate in [`docs/06_slide_design_constraint_system.md`](docs/06_slide_design_constraint_system.md) before timed rehearsal.
4. Rehearse from [`docs/03_speaker_script_and_stage_rhythm.md`](docs/03_speaker_script_and_stage_rhythm.md).
5. Score each run with [`docs/04_scoring_rubric.md`](docs/04_scoring_rubric.md).
6. Apply the next repair pass from [`docs/05_rehearsal_and_iteration_runbook.md`](docs/05_rehearsal_and_iteration_runbook.md).

The recommended delivery surface is the compact `14`-slide version. Older `23`-slide materials are source context in the planning repo, not active working files here.

## Evaluation Architecture

```text
Speech Evaluation System
-> 100-point macro score for strategy, content, timing, delivery, visuals, presence, and impact

Slide Design Constraint System
-> pass/fail gates plus penalties for slide-level clarity, density, layout, and AI-feel risk

Optimization Engine
-> rewrite only the worst failed slides
```

Do not merge these layers into one generic checklist. The speech rubric evaluates the talk. The slide constraint system prevents the deck from becoming text-heavy, generic, or visually undisciplined.

## Planning Repo Connection

Planning repo:

`/Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/planning-everything-track/`

Primary planning handoff:

`/Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-presentation-scoring-system-handoff-20260421.md`

Project index:

`/Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck.md`

Connection rule: update the planning handoff when this repo changes its canonical file set or workflow. Do not duplicate the full package into the planning repo.

## Source Anchors

Official anchors:

- CYBERSEC session page: <https://cybersec.ithome.com.tw/2026/session/4284>
- CYBERSEC speaker page: <https://cybersec.ithome.com.tw/2026/speaker/2060>
- FDA cybersecurity page: <https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity>
- FDA 2025 cybersecurity guidance PDF: <https://www.fda.gov/files/guidance%20documents/published/GUI00001825-final-PremarketCybersecurity-2025.pdf>

Local planning anchors:

- v0.9 deck: `/Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-ai-samd-cybersecurity-lin-jia-sheng-organizer-v0.9-20260422.pptx`
- v0.9 PDF: `/Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-ai-samd-cybersecurity-lin-jia-sheng-organizer-v0.9-20260422.pdf`
- v0.9 speaker notes: `/Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-ai-samd-cybersecurity-lin-jia-sheng-speaker-notes-v0.9-20260422.md`
- v0.9 rehearsal runbook: `/Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-first-rehearsal-runbook-v0.9-20260422.md`
- Official event source bundle: `/Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/planning-everything-track/data/knowledge/personal/sources/2026-04-09-cybersec-2026-speaker-pre-event-notice/source.md`

## Design Contract

| Constraint | Package Rule | Rubric Protected |
| --- | --- | --- |
| Serious conference tone | Use product-risk, evidence-chain, and operating-decision language | Content Depth and Value, Stage Presence |
| No classroom report posture | Every slide must answer a decision question: what risk, what evidence, what action | Delivery Quality, Audience Impact |
| No decorative security imagery | Visuals must show architecture, evidence, workflow, comparison, or decision | Visual Design |
| No slide bloat | One dominant message per slide; secondary detail belongs in speaker notes or Q&A | Structure and Narrative Design, Stage Rhythm and Time Control |
| No public sensitive content | Exclude proprietary code, private hospital/client detail, student records, raw submissions, exploit recipes, and patent-sensitive implementation mechanics | Stage Presence, Content Depth and Value |

## Current Delivery Promise

The talk should leave the audience with one operating model:

`AI SaMD security is not a model-security checklist. It is a product trust system: scope the product, trace the evidence, test the exposure, govern findings, and prove repairability.`

Stage-language anchors:

- `你賣的不是模型`
- `法規要的是證據，不是口號`
- `Cyber Safety is Patient Safety`
- `沒有 decision，就沒有治理；沒有證據，就沒有信任`
- `先把安全做進產品，法規文件才會自然長出來`
