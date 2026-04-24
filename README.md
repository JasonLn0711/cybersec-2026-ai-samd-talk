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
| What is the active delivery surface? | Owner-approved `v1.3` canonical PDF deck, with the generated compact `14`-slide deck retained as an editable fallback/reference. |
| What should not happen? | Do not mix speech-delivery artifacts with student grading, raw submissions, private hospital/client material, or unrelated course records. |

Routing model:

```text
planning-everything-track = why / when / priority / status / capacity
cybersec-2026-ai-samd-talk = what the talk says / shows / scores / rehearses
```

## Canonical Human Docs

| File | Use It For |
| --- | --- |
| [`docs/01_talk_design.md`](docs/01_talk_design.md) | First-principles talk model, audience promise, current `v1.3` deck routing, generated fallback design, timing, build path, and stage script. |
| [`docs/02_evaluation_system.md`](docs/02_evaluation_system.md) | `100`-point speech rubric, slide hard gates, penalties, multiplier, and generated evaluation outputs. |
| [`docs/03_rehearsal_workflow.md`](docs/03_rehearsal_workflow.md) | Dry-run loop, timing checkpoints, peer-review questions, repair order, and readiness checklist. |
| [`docs/speaker-notes/`](docs/speaker-notes/) | Tracked versioned speaker-prep notes, deeper case material, transcript working copies, audience Q&A prep, and slide-by-slide audience analysis. |

The three numbered docs replace the older split between strategy, deck spec, transcript, scoring rubric, slide constraints, and rehearsal runbook. The speaker-notes folder is supplemental and versioned for rehearsal depth.

## Current Canonical Deck

| Artifact | Role |
| --- | --- |
| `outputs/deck/cybersec-2026-ai-samd-cybersecurity-in-practice-v1.3.pdf` | Current owner-approved canonical deck PDF. No editable source PPTX for `v1.3` is currently present. |
| `docs/speaker-notes/reference/cybersec-2026-ai-samd-v1.3-transcript-audience-plus-deep-notes-zh-tw.md` | Main Taiwan Mandarin rehearsal reader combining talk track, audience analysis, and deep-note companion content slide by slide. |
| `docs/speaker-notes/reference/cybersec-2026-ai-samd-v1.3-transcript-plus-audience-analysis-zh-tw.md` | Lighter slide-by-slide reader combining the `v1.3` talk track and audience analysis. |
| `docs/speaker-notes/reference/cybersec-2026-ai-samd-v1.3-slide-audience-analysis-zh-tw.md` | Current `v1.3` slide-by-slide audience analysis, trend response, and 8 hard-question drill. |
| `docs/speaker-notes/reference/cybersec-2026-ai-samd-audience-qa-v1-zh-tw.md` | Broader role-based Taiwanese Mandarin Q&A prep. |
| `docs/speaker-notes/cybersec-2026-ai-samd-slide-deep-notes-v1-positive-progressive-zh-tw.md` | Current positive-progressive rehearsal script for the generated compact/fallback storyline. |
| `docs/speaker-notes/cybersec_2026_positive_progressive_style.md` | Current speaking-style guide for positive, progressive, non-negation stage language. |
| `docs/speaker-notes/archive/` | Superseded drafts and legacy deep-note baselines retained for traceability. |

The original imported file under `~/Downloads` is not the repo source of truth and should not be modified or deleted by agent work.

## Machine Source And Generated Outputs

Structured source of truth:

`data/presentation_os.json`

This structured source still owns the generated compact fallback package. It is no longer the canonical `v1.3` deck source.

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

## Generated Compact Fallback Deck

Build the optimized compact fallback deck from the same JSON source:

```bash
npm install
npm run build:deck
```

Dependency note: the deck builder uses the public `pptxgenjs` package. PDF export and preview PNG rendering use local LibreOffice and Poppler (`pdftoppm`) when those CLI tools are available.

Fallback editable PPTX:

`outputs/deck/cybersec-2026-ai-samd-compact-optimized.pptx`

Fallback PDF preview / USB backup copy:

`outputs/deck/cybersec-2026-ai-samd-compact-optimized.pdf`

The generated fallback deck uses editable PowerPoint text, shapes, diagrams, and speaker notes. Slide 2 uses the official CYBERSEC disclaimer image from the planning source bundle when that image is available.

## Working Order

1. Use `outputs/deck/cybersec-2026-ai-samd-cybersecurity-in-practice-v1.3.pdf` as the current canonical deck PDF.
2. Read [`docs/01_talk_design.md`](docs/01_talk_design.md) to confirm the thesis, audience promise, slide map, timing, script, and public-safety boundary.
3. Use `docs/speaker-notes/reference/cybersec-2026-ai-samd-v1.3-transcript-audience-plus-deep-notes-zh-tw.md` as the main Taiwan Mandarin slide-by-slide rehearsal reader.
4. Use `docs/speaker-notes/reference/cybersec-2026-ai-samd-v1.3-slide-audience-analysis-zh-tw.md` for per-slide audience challenge prep and the 8 hard-question drill.
5. Use `docs/speaker-notes/reference/cybersec-2026-ai-samd-audience-qa-v1-zh-tw.md` for broader Taiwanese Mandarin audience Q&A prep.
6. Use `docs/speaker-notes/cybersec-2026-ai-samd-slide-deep-notes-v1-positive-progressive-zh-tw.md` and `docs/speaker-notes/cybersec_2026_positive_progressive_style.md` for the generated compact/fallback storyline.
7. Edit `data/presentation_os.json` only when generated fallback reports or fallback deck text need to change.
8. Run `npm run build:reports` or `python3 tools/generate_presentation_outputs.py` only when the generated fallback package needs regeneration.
9. Build the editable fallback PPTX with `npm run build:deck` only when the generated fallback artifact must change.
10. Apply [`docs/02_evaluation_system.md`](docs/02_evaluation_system.md) before timed rehearsal.
11. Rehearse and repair using [`docs/03_rehearsal_workflow.md`](docs/03_rehearsal_workflow.md).
12. Update the planning handoff only with status, links, and workflow changes; do not duplicate this package into the planning repo.

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

## Source Ownership

Keep source detail where it is used:

- Current source-verified `v1.3` slide, transcript, and Q&A references live in `docs/speaker-notes/reference/`.
- Current generated compact/fallback rehearsal script and style guide live at the speaker-notes root.
- Superseded speaker-note drafts and legacy baselines live in `docs/speaker-notes/archive/`; rewrite traceability lives in `docs/speaker-notes/change-log/`.
- Generated compact fallback source anchors live in `data/presentation_os.json` and rebuild into `outputs/current/main_strategy.md`.
- Event and deadline state lives in the planning repo, not in this README.

This README should stay a routing map. Do not duplicate long source lists here unless the repo's source ownership model changes.

Essential stable anchors:

- CYBERSEC session page: <https://cybersec.ithome.com.tw/2026/session/4284>
- FDA 2026 cybersecurity guidance: <https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-management-system-considerations-and-content-premarket>
- FDA cybersecurity FAQ / Section 524B reference: <https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity-medical-devices-frequently-asked-questions-faqs>
- FDA AI-enabled DSF lifecycle draft guidance: <https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing>
- FDA AI PCCP final guidance: <https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence>
- TFDA AI/ML CADe / CADx guidance update: <https://www.fda.gov.tw/tc/siteListContent.aspx?id=49448&sid=310>
- NIST AI RMF playbook: <https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook>
- NIST CSF 2.0: <https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20>

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
