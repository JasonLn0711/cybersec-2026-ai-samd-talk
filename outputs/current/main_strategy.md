# CYBERSEC 2026 Presentation Operating System

Canonical topic: `AI 軟體醫材的資安實戰：從美國 FDA 524B 規範到 Threat Modeling 與 Patch SLA 的完整落地`

This generated strategy file turns the existing compact CYBERSEC talk into a reusable operating system. The macro speech rubric stays at `100` points; the slide constraint layer is a separate pass/fail and penalty gate; the optimization loop repairs the highest-leverage failures before rehearsal.

## 1. Engine Architecture

| Engine | Operating Role |
| --- | --- |
| Design Engine | Convert the CYBERSEC topic into a professional 30-minute conference narrative with timing, authority, and audience cognition built in. |
| Slide Engine | Produce a compact Apple-style 14-slide structure with one message, strong visual dominance, and no decorative security imagery. |
| Evaluation Engine | Score the macro talk with the 100-point rubric before slide penalties are applied. |
| Constraint Engine | Gate every slide with pass/fail slide constraints, anti-AI-feel checks, penalties, and public-safety boundaries. |
| Optimization Engine | Repair the highest-leverage weak points, rewrite weak slides, and simulate a second-pass evaluation. |
| Report Engine | Emit stable Markdown and CSV outputs for rehearsal, peer review, and spreadsheet scoring. |

## 2. Presentation Brief

| Field | Decision |
| --- | --- |
| Recommended title | AI 軟體醫材的資安實戰：從美國 FDA 524B 規範到 Threat Modeling 與 Patch SLA 的完整落地 |
| Positioning | A conference-grade operating model for AI SaMD teams that must translate FDA 524B, FDA 2025 premarket cybersecurity expectations, TFDA-facing AI/ML SaMD evidence, testing, and Patch SLA into product decisions. |
| Core thesis | AI SaMD security is not a model-security checklist. It is a product trust system: scope the product, trace the evidence, test the exposure, govern findings, and prove repairability. |
| Why this matters now | AI medical products are moving from standalone model demonstrations into deployed systems: viewers, cloud runtimes, databases, update mechanisms, hospital integrations, and support workflows. That shift makes cybersecurity a product-continuity and patient-safety issue. |
| Speaker authority angle | The speaker translates regulatory expectations, AI-stack risk, testing practice, and product operations into one implementation model for teams preparing for real CYBERSEC-level scrutiny. |
| Differentiator | The talk does not list regulations or tools. It uses four product scales, one evidence chain, and one Patch SLA decision loop to make cybersecurity operational. |
| Active deck | 14 slides, 28:30 content plus 1:30 buffer |
| Language policy | English for strategy and evaluation; Taiwan Traditional Chinese for stage-language examples. |

### Title Candidates

1. AI 軟體醫材的資安實戰：從 FDA 524B 到 Threat Modeling 與 Patch SLA
2. 你賣的不是模型：AI 醫材資安、證據鏈與 Patch SLA
3. Cyber Safety Is Patient Safety：AI SaMD 的資安治理落地
4. 從模型到醫療系統：AI SaMD 的資安證據鏈
5. 法規要的是證據，不是口號：AI 醫材資安實作路線圖
6. AI SaMD Security Operations：Threat Modeling, Testing, Patch SLA

### Intended Audience

- Medical-device founders and product leaders who need a practical security scope model.
- Security engineers and consultants who need to convert findings into evidence and governance decisions.
- Regulatory, QA, and clinical-risk teams who need traceability from architecture to controls, tests, fixes, and records.
- Hospital and healthcare IT leaders who evaluate vendor trust, service continuity, and patient-safety exposure.
- Cross-functional managers who need a shared language for ownership, evidence, and repair timing.

### Audience Assumptions

- They know AI/ML and medical-device language at different depths, but not everyone has connected it to postmarket vulnerability operations.
- They expect technical seriousness and practical takeaways, not a regulatory reading session.
- They may underestimate how quickly a model demo becomes a product system with identity, data, update, logging, and support obligations.

### Audience Pain Points

- AI security is mistakenly narrowed to model robustness.
- Regulatory work is treated as submission paperwork instead of traceable engineering evidence.
- Testing produces reports but not decisions, retest proof, or Patch SLA governance.
- Small teams assume mature security programs are unreachable and delay minimum evidence work.
- Healthcare stakeholders need a patient-safety explanation that avoids fear-heavy examples.

### Desired Takeaways

- Product scale determines cybersecurity evidence burden.
- FDA 524B and FDA 2025 can be translated into monitor, patch, disclose, SBOM, and traceability work.
- TFDA-facing AI/ML SaMD preparation needs model evidence, governance language, and stack-level security boundaries.
- White-box and black-box testing are valuable when findings become decisions and retest evidence.
- Patch SLA is the operating bridge between vulnerability discovery, product trust, and audit readiness.

### Risk Factors And Mitigations

| Risk Factor | Mitigation |
| --- | --- |
| Regulatory content can become dense and slow. | Compress regulation into evidence-chain logic: Risk -> Control -> Test -> Fix -> Evidence. |
| Technical examples can drift toward tool catalogs. | Use product-scale comparisons instead of vulnerability lists. |
| Slides 6 and 7 can overload the audience if they become control lists. | Make Slide 10 an intentional recovery beat after the dense middle. |
| The ending can be weakened if the speaker spends too long on testing details. | Use cut markers before speaking faster. |
| Any private implementation detail would reduce trust and public-safety readiness. | Keep all examples public-safe and artifact-level. |

## 3. Rubric-To-Design Translation Matrix

| Category | Points | Design Goal | Observable Success | Tactics | Failure Pattern | Avoid | Slide Influence | Speaking Influence |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Structure and Narrative Design | 20 | Make the talk feel inevitable from model to trust system. | Audience can restate the arc: product scale -> evidence -> testing -> Patch SLA -> trust. | Use Slides 3, 5, 6, 12, and 14 as structural anchors. | Sections feel like independent lectures; closing introduces new content. | Agenda-first opening, framework dumping, and late-stage new ideas. | Every slide needs one governing message and a transition reason. | Name why the next section exists before moving. |
| Content Depth and Value | 20 | Deliver technical substance without overwhelming the room. | Security, regulatory, product, and healthcare listeners each hear usable decisions. | Translate FDA 524B, FDA 2025, TFDA-facing AI/ML SaMD evidence, testing, and Patch SLA into artifacts. | Tool-name dumping, regulation name-dropping, or shallow slogans. | Long legal quotes, exploit steps, and vendor-style claims. | Use evidence chains, stack diagrams, contrast panels, and decision flows. | Explain the artifact or decision each concept produces. |
| Stage Rhythm and Time Control | 15 | Vary pace and protect the ending. | Slide 7 ends near 14:00; Slide 14 begins by 27:40; content ends by 28:30. | Slow on memory slides, accelerate through labels, and use Slide 10 as recovery. | Regulatory middle expands; speaker compensates by rushing the close. | Trying to solve density by speaking faster. | Dense slides must use progressive reveal; memory slides must breathe. | Use cut markers before time pressure becomes visible. |
| Delivery Quality | 15 | Sound precise, calm, and executive-technical. | The speaker uses short sentences, consistent terms, and no apologetic hedging. | Preserve the strong lines and deliver them with silence. | Reading slides, overexplaining acronyms, and adding examples after Slide 10. | Passive classroom phrasing and filler transitions. | Slides carry labels, not scripts. | Use Taiwan Traditional Chinese with English terms only where they are domain-standard. |
| Visual Design | 10 | Make meaning visible in three seconds. | Audience sees a phrase, ladder, chain, stack, contrast, flow, or roadmap before explanation. | Use one dominant visual object per slide and semantic color only. | Text blocks, repeated template layout, decorative hacker imagery, or generic AI symbolism. | Stock visuals, random icons, and paragraph slides. | Apple-style restraint, high contrast, and diagram-led meaning. | Refer to the visual only when it advances the decision. |
| Stage Presence | 10 | Project controlled authority. | Stillness and eye contact on Slides 3, 10, 12, and 14. | Use posture changes only for structural transitions and gestures only for diagrams. | Looking back during strong lines, wandering, or visible time panic. | Overmoving during patient-safety and closing moments. | Minimize text that forces the speaker to read. | Pause after the strong lines and stop cleanly. |
| Audience Impact | 10 | Make the talk memorable and useful after the conference. | Audience recalls `你賣的不是模型`, four product scales, Patch SLA, and `30 / 60 / 90`. | Repeat memory anchors and convert them into action. | Interesting content with no operational next step. | Broad best-practice endings and administrative closing clutter. | Preserve visually distinctive memory slides. | End on principle and ownership, not logistics. |

## 4. 30-Minute Time Architecture

Normal target: `28:30` content plus `1:30` buffer.

| Slide Range | Time | Function | Load |
| --- | --- | --- | --- |
| 1-2 | 0:30 | Formal opening and required compliance beat. | Light |
| 3 | 1:50 | Thesis hook and mental-frame reset. | Emotional and conceptual |
| 4-5 | 4:10 | Why-now and product-scale map. | Moderate |
| 6-7 | 7:30 | Regulatory evidence and local governance bridge. | Heavy |
| 8-9 | 5:20 | Concrete product-scale risk comparison. | Moderate |
| 10 | 1:20 | Patient-safety peak and attention recovery. | Emotional reset |
| 11-12 | 4:30 | Testing and Patch SLA operating model. | Technical and operational |
| 13-14 | 3:20 | Practical roadmap and clean close. | Action-oriented |

### Timing Variants

| Mode | Target | Rule |
| --- | --- | --- |
| safe | 27:30 | Remove secondary labels from slides 7, 8, 9, and 11; preserve all memory lines. |
| rushed | 25:00 | Slide 6 becomes evidence chain only; slide 7 one sentence per column; slide 13 one output per bucket. |
| emergency | 20:00 | Skip slides 4 and 11 as standalone sections; mention AI infrastructure in slide 5 and testing output in slide 12. |

### Attention Drop Prediction

| Risk Point | Why Attention Drops | Recovery Strategy |
| --- | --- | --- |
| After Slide 7 | The regulatory/governance section is the heaviest cognitive load. | Move into Slide 8 with the concrete question `第一層和第二層差在哪裡？` |
| Before Slide 12 | Testing can become a tool-list detour. | Use `但 finding 出來以後，真正的治理才開始。` and make Decision the visual center. |
| Final two minutes | The speaker may rush if Slide 11 expands. | Cut testing examples, keep 30 / 60 / 90, and start Slide 14 by 27:40. |

## 5. Narrative Architecture

| Narrative Field | Decision |
| --- | --- |
| Mode | myth -> reality -> operating framework -> implementation |
| Why this mode | The audience likely begins with the false simplification that AI SaMD security is model security or compliance paperwork. This structure breaks that myth, replaces it with product-scale reality, then gives a practical operating model. |
| Opening hook | Start with the stage line `你賣的不是模型` after the required title and disclaimer beats. The line immediately shifts the audience from model performance to product trust. |
| Problem framing | The security problem grows as AI moves from model artifact to viewer, platform, database, connected medical system, update chain, and support workflow. |
| Tension | Regulators, hospitals, and users do not only ask whether the model is accurate. They ask whether the product can be monitored, patched, disclosed, tested, explained, and repaired. |
| Climax | Slide 12: every finding needs a decision. This is where testing, regulation, product ownership, and trust converge. |
| Closing structure | Slide 13 gives the audience a 30 / 60 / 90 implementation path; Slide 14 closes with trust-before-audit and no new material. |
| Final takeaway | 先把安全做進產品，法規文件才會自然長出來。 |

### Development Arc

- Slide 3 breaks the model-only myth.
- Slides 4-5 establish urgency and product scale.
- Slides 6-7 translate regulation and governance into an evidence chain.
- Slides 8-9 apply the model to product-scale risk.
- Slide 10 turns the technical argument into patient-safety significance.
- Slides 11-12 convert testing into Patch SLA decisions.
- Slides 13-14 give an executable path and closing principle.

## 6. Visual Strategy

| Rule | Production Meaning | Rubric Protected |
| --- | --- | --- |
| One dominant object | Each slide must be a phrase, ladder, chain, stack, contrast, flow, or roadmap. | Visual Design |
| Color carries semantics | Use the primary accent for evidence/decision and risk color only for interruption or unresolved exposure. | Visual Design |
| Technical detail becomes labels | Regulatory and testing substance appears as diagram labels; the explanation belongs in stage speech. | Content Depth and Value |
| Memory slides breathe | Slides 3, 10, 12, and 14 use stillness and negative space. | Audience Impact |
| Public-safe examples only | No private, proprietary, exploit, or patent-sensitive content appears on screen. | Stage Presence |

## 7. Audience Impact Design

| Moment | Audience Reaction To Create | Design Action |
| --- | --- | --- |
| First minute | This is not an AI hype talk. | Open on `你賣的不是模型` after the required compliance beat. |
| Slide 5 | I can locate my product on this map. | Use four scales and evidence growth. |
| Slide 6 | Regulation is traceability, not paperwork. | Show the evidence chain instead of legal text. |
| Slide 10 | This connects to patient safety. | Use a standalone phrase and silence. |
| Slide 12 | This is the operating mechanism we need. | Make Decision the largest node. |
| Final minute | I know the next move. | Use 30 / 60 / 90 and close on trust-before-audit. |

## 8. Score Model

| Metric | Value |
| --- | --- |
| Baseline macro score | 84 |
| Baseline slide penalty | 4 |
| Baseline adjusted score | 80 |
| Optimized macro score | 94 |
| Optimized slide penalty | 1 |
| Optimized multiplier | 1.05 |
| Optimized adjusted score | 98 |
| Improvement | +18 |

## 9. Source Anchors

| Source | Anchor |
| --- | --- |
| CYBERSEC session page | https://cybersec.ithome.com.tw/2026/session/4284 |
| CYBERSEC speaker page | https://cybersec.ithome.com.tw/2026/speaker/2060 |
| FDA cybersecurity page | https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity |
| FDA 2025 cybersecurity guidance PDF | https://www.fda.gov/files/guidance%20documents/published/GUI00001825-final-PremarketCybersecurity-2025.pdf |
| Local CYBERSEC source bundle | /Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/planning-everything-track/data/knowledge/personal/sources/2026-04-09-cybersec-2026-speaker-pre-event-notice/source.md |
| v0.9 deck source | /Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-ai-samd-cybersecurity-lin-jia-sheng-organizer-v0.9-20260422.pptx |
| v0.9 speaker notes | /Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-ai-samd-cybersecurity-lin-jia-sheng-speaker-notes-v0.9-20260422.md |
| v0.9 rehearsal runbook | /Users/iKev/Desktop/02_Projects_and_Code/everything_on_git/planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-first-rehearsal-runbook-v0.9-20260422.md |
