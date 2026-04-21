# CYBERSEC 2026 AI SaMD Talk

Canonical repository for the CYBERSEC 2026 speech-delivery package:

`AI 軟體醫材的資安實戰：從美國 FDA 524B 規範到 Threat Modeling 與 Patch SLA 的完整落地`

This repo owns what the talk says, shows, scores, and rehearses. It exists because CYBERSEC delivery is a standalone professional talk project, not a TA grading artifact and not a planning dashboard.

Agent-facing working rules live in [`AGENTS.md`](AGENTS.md).

## First-Principles Boundary

| Question | Decision |
| --- | --- |
| What is the artifact? | A public `30:00` CYBERSEC conference talk package. |
| Who uses it? | Speaker, deck editor, rehearsal reviewer, and evaluator. |
| What must it optimize? | Clarity, credibility, timing, memorability, public safety, and delivery readiness. |
| Where should it live? | In this dedicated sibling repo, not inside planning or grading repos. |
| What is the active delivery surface? | Compact `14`-slide deck, `28:30` spoken content, `1:30` buffer. |
| What should not happen? | Do not mix speech-delivery artifacts with student grading, raw submissions, private hospital/client material, or unrelated course records. |

Routing model:

```text
planning-everything-track = why / when / priority / status / capacity
cybersec-2026-ai-samd-talk = what the talk says / shows / scores / rehearses
```

## Canonical Human Docs

| File | Use It For |
| --- | --- |
| [`docs/01_talk_design.md`](docs/01_talk_design.md) | First-principles talk model, audience promise, `14`-slide design, timing, build path, and full stage script. |
| [`docs/02_evaluation_system.md`](docs/02_evaluation_system.md) | `100`-point speech rubric, slide hard gates, penalties, multiplier, and generated evaluation outputs. |
| [`docs/03_rehearsal_workflow.md`](docs/03_rehearsal_workflow.md) | Dry-run loop, timing checkpoints, peer-review questions, repair order, and readiness checklist. |
| [`docs/speaker-notes/`](docs/speaker-notes/) | Tracked versioned speaker-prep notes, deeper case material, and transcript working copies. |

The three numbered docs replace the older split between strategy, deck spec, transcript, scoring rubric, slide constraints, and rehearsal runbook. The speaker-notes folder is supplemental and versioned for rehearsal depth.

## Machine Source And Generated Outputs

Structured source of truth:

`data/presentation_os.json`

Generate current reports:

```bash
python3 tools/generate_presentation_outputs.py
```

Generated files:

| File | Use It For |
| --- | --- |
| `outputs/current/main_strategy.md` | Generated strategy, narrative, timing, source anchors, and rubric translation. |
| `outputs/current/slide_blueprint.md` | Generated slide-by-slide compact `14`-slide blueprint. |
| `outputs/current/evaluation_report.md` | Baseline and optimized scoring with slide-adjusted readiness. |
| `outputs/current/slide_constraint_report.md` | Slide hard-gate report and redesign queue. |
| `outputs/current/optimization_plan.md` | Top failure points and second-pass repair plan. |
| `outputs/current/scoring_report.csv` | Spreadsheet-ready score report. |
| `outputs/current/slide_validation.csv` | Spreadsheet-ready slide gate report. |

The generator enforces exactly `14` slides, exactly `1710` seconds / `28:30` content time, and exactly `100` rubric points.

## Editable PPTX Build

Build the optimized compact deck from the same JSON source:

```bash
npm install
npm run build:deck
```

Dependency note: the deck builder uses the public `pptxgenjs` package. PDF export and preview PNG rendering use local LibreOffice and Poppler (`pdftoppm`) when those CLI tools are available.

Deck artifact:

`outputs/deck/cybersec-2026-ai-samd-compact-optimized.pptx`

PDF preview / USB backup copy:

`outputs/deck/cybersec-2026-ai-samd-compact-optimized.pdf`

The deck uses editable PowerPoint text, shapes, diagrams, and speaker notes. Slide 2 uses the official CYBERSEC disclaimer image from the planning source bundle when that image is available.

## Working Order

1. Read [`docs/01_talk_design.md`](docs/01_talk_design.md) to confirm the thesis, audience promise, slide map, timing, script, and public-safety boundary.
2. Edit `data/presentation_os.json` only when generated reports or deck text need to change.
3. Run `npm run build:reports` or `python3 tools/generate_presentation_outputs.py`.
4. Build the editable PPTX with `npm run build:deck` when the deck artifact must change.
5. Apply [`docs/02_evaluation_system.md`](docs/02_evaluation_system.md) before timed rehearsal.
6. Rehearse and repair using [`docs/03_rehearsal_workflow.md`](docs/03_rehearsal_workflow.md).
7. Update the planning handoff only with status, links, and workflow changes; do not duplicate this package into the planning repo.

## Evaluation Architecture

```text
Speech Evaluation System
-> 100-point macro score for strategy, content, timing, delivery, visuals, presence, and impact

Slide Design Constraint System
-> pass/fail gates plus penalties for slide-level clarity, density, layout, and AI-feel risk

Optimization Engine
-> rewrite only the worst failed slides
```

The speech rubric evaluates the talk. The slide gate protects clarity. The rehearsal loop chooses the next repair.

## Planning Repo Connection

Planning repo local sibling path:

`../planning-everything-track/`

Primary planning handoff local sibling path:

`../planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-presentation-scoring-system-handoff-20260421.md`

Project index local sibling path:

`../planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck.md`

Connection rule: update the planning handoff when this repo changes its canonical file set or workflow.

## Source Anchors

Official anchors:

- CYBERSEC session page: <https://cybersec.ithome.com.tw/2026/session/4284>
- CYBERSEC speaker page: <https://cybersec.ithome.com.tw/2026/speaker/2060>
- FDA cybersecurity page: <https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity>
- FDA 2025 cybersecurity guidance PDF: <https://www.fda.gov/files/guidance%20documents/published/GUI00001825-final-PremarketCybersecurity-2025.pdf>
- Public Law 117-328, section 524B: <https://www.congress.gov/117/plaws/publ328/PLAW-117publ328.pdf>
- NIST AI Risk Management Framework playbook: <https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook>
- NIST Cybersecurity Framework 2.0: <https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20>
- ROC National Cybersecurity Strategy 2025: <https://www.president.gov.tw/File/Doc/9d056651-e4a0-4d51-adeb-5fee5ee71299>
- Executive Yuan National Cybersecurity Development Program, 114-117: <https://www.ey.gov.tw/Page/448DE008087A1971/a954ca38-9dfb-446b-879a-9e7ed88495a4>
- Executive Yuan critical-infrastructure domain reference: <https://digi.nstc.gov.tw/Page/1538F8CF7474AB4E/e262d09b-a434-4f0f-bb89-8015ab70e459>
- FSC Financial Cybersecurity Resilience Blueprint news page: <https://www.fsc.gov.tw/ch/home.jsp?id=96&parentpath=0,2&mcustomize=news_view.jsp&dataserno=202512300002&dtable=News>
- FSC Financial Cybersecurity Resilience Blueprint PDF mirror: <https://www.twsa.org.tw/save/doc/%E9%87%91%E8%9E%8D%E8%B3%87%E5%AE%89%E9%9F%8C%E6%80%A7%E7%99%BC%E5%B1%95%E8%97%8D%E5%9C%96.pdf>

Local planning anchors:

- v0.9 deck source: `../planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-ai-samd-cybersecurity-lin-jia-sheng-organizer-v0.9-20260422.pptx`
- v0.9 PDF source: `../planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-ai-samd-cybersecurity-lin-jia-sheng-organizer-v0.9-20260422.pdf`
- v0.9 speaker notes source: `../planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-ai-samd-cybersecurity-lin-jia-sheng-speaker-notes-v0.9-20260422.md`
- v0.9 rehearsal runbook source: `../planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-first-rehearsal-runbook-v0.9-20260422.md`
- Official event source bundle: `../planning-everything-track/data/knowledge/personal/sources/2026-04-09-cybersec-2026-speaker-pre-event-notice/source.md`

## Design Contract

| Constraint | Package Rule |
| --- | --- |
| Serious conference tone | Use product-risk, evidence-chain, and operating-decision language. |
| No classroom report posture | Every slide must answer: what risk, what evidence, what action. |
| No decorative security imagery | Visuals must show architecture, evidence, workflow, comparison, or decision. |
| No slide bloat | One dominant message per slide; detail belongs in speaker notes or Q&A. |
| No public sensitive content | Exclude proprietary code, private hospital/client detail, student records, raw submissions, exploit recipes, and patent-sensitive implementation mechanics. |

## National And Cross-Sector Context

Use the Taiwan national cybersecurity strategy, critical-infrastructure frame, and financial-sector resilience blueprint as context, not as a second topic. The talk's primary case remains medical AI SaMD.

Placement rule:

- Slide 4 may mention that national strategy now links AI security, critical infrastructure, key industries, and supply-chain resilience.
- Slide 9 may use finance, telecommunications, and energy as one-line continuity analogies before returning to clinical continuity.
- Slides 12-13 may borrow financial-sector language around governance, resilience, drills, backup, supply-chain oversight, and measurable recovery, but only to strengthen Patch SLA and the first `90` days evidence loop.
- Do not add a standalone national-strategy chapter unless the talk length is expanded beyond `30:00`.

## Current Delivery Promise

The talk should leave the audience with one operating model:

`AI SaMD security is not a model-security checklist. It is a product trust system: scope the product, trace the evidence, test the exposure, govern findings, and prove repairability.`

Stage-language anchors:

- `你賣的不是模型`
- `法規要的是證據，不是口號`
- `Cyber Safety is Patient Safety`
- `沒有 decision，就沒有治理；沒有證據，就沒有信任`
- `先把安全做進產品，法規文件才會自然長出來`
