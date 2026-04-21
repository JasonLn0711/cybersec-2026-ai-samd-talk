# Slide Constraint Report

This report is the slide-level quality firewall. It does not replace the macro `100`-point speech rubric; it applies pass/fail gates, penalties, and design-risk checks after the macro score is assigned.

## Hard Rules

- Exactly one controlling idea per slide, except the required disclaimer.
- Headline or sentence text stays below 12 words; technical labels are allowed only when they function as diagram labels.
- At least 70% of each slide is visual structure or whitespace.
- No more than two bullets; prefer zero.
- Audience should understand the point in under three seconds.
- No private hospital/client detail, proprietary code, raw student records, exploit recipes, or patent-sensitive implementation mechanics.

## Allowed Layouts

- Big statement
- Full visual
- Contrast
- Diagram
- Progressive build

## Design System

| Axis | Rule |
| --- | --- |
| Style | Dark, clean, high-contrast, diagram-led, and restrained. |
| Fonts | Modern sans: title and label styles only. |
| Colors | One primary accent for evidence/decision and one risk color for interruption or unresolved exposure. |
| Imagery | No hacker hoodies, AI brains, random circuit stock art, or dramatic hospital imagery. |
| Density | One dominant visual object per slide; technical detail belongs in labels, speech, or Q&A. |

## Penalty Model

| Severity | Penalty | Condition |
| --- | --- | --- |
| minor | 1-2 | Small density, spacing, or consistency issue that does not block comprehension. |
| major | 3-5 | Hard-rule failure, AI-feel risk, or important slide losing visual hierarchy. |
| critical | 10 | Text-heavy, no structure, unreadable, or public-safety boundary failure. |

## Baseline Violations Before Optimization

| Slide | Pass/Fail | Violations | Severity | Penalty | Required Redesign |
| --- | --- | --- | --- | --- | --- |
| 6 | FAIL | Risk of legal-text density if FDA evidence is shown as source quotes instead of a chain. | Major | 3 | Keep only Evidence, not slogans; Risk -> Control -> Test -> Fix -> Evidence; Monitor \| CVD \| Patch \| SBOM. |
| 7 | FAIL | Three-column bridge can become a control catalog. | Major | 3 | Reduce each column to one noun phrase plus three labels; speak the rest. |
| 11 | PASS | Minor tool-catalog risk if examples expand. | Minor | 1 | Keep contrast between early repair and external exposure; output strip must say finding list + retest evidence. |
| 12 | PASS | Minor risk that flow competes with Decision node. | Minor | 1 | Make Decision visually dominant and outcomes secondary. |

## Optimized Slide Gate

| Slide | Title | Pass/Fail | Violations | Severity |
| --- | --- | --- | --- | --- |
| 1 | AI SaMD Cybersecurity: From Model Demo to Product Trust | PASS | None | None |
| 2 | Required CYBERSEC Disclaimer | PASS | None | None |
| 3 | 你賣的不是模型，是臨床產品責任 | PASS | None | None |
| 4 | Why Now: AI Is Becoming Care Infrastructure | PASS | None | None |
| 5 | Product Boundary Decides Risk | PASS | None | None |
| 6 | From Obligation to Evidence Chain | PASS | None | None |
| 7 | Three Risk Layers, One Governance Language | PASS | None | None |
| 8 | Scale 1-2: Artifact to User-Facing System | PASS | None | None |
| 9 | Scale 3-4: Platform to Clinical Continuity | PASS | None | None |
| 10 | Security Failure Becomes Safety Risk | PASS | None | None |
| 11 | Testing Portfolio: What Question Does Each Test Answer? | PASS | None | None |
| 12 | Finding Governance: Patch SLA | PASS | None | None |
| 13 | Small Team 30 / 60 / 90 | PASS | None | None |
| 14 | 先建立信任，再面對稽核 | PASS | None | None |

## Redesign Priority

1. Keep Taiwan national strategy and financial resilience as contextual bridges, not standalone sections; rewrite Slide 6 as an evidence chain, not a legal text block.
2. Reduce Slide 7 to three columns with three labels each and move explanation to speech.
3. Make Slide 12's Decision node the largest object in the flow.
4. Use Slide 10 as silence, not content expansion.
5. Rehearse the safe version until Slide 14 reliably starts by 27:40.
