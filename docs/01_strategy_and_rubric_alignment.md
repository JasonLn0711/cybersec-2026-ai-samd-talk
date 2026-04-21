# 01 Strategy And Rubric Alignment

Purpose: define the talk as a professional CYBERSEC conference briefing and translate the `100`-point scoring rubric into design constraints before slides are built.

## 1. Presentation Design Brief

| Field | Decision |
| --- | --- |
| Primary title | `AI 軟體醫材的資安實戰：從美國 FDA 524B 規範到 Threat Modeling 與 Patch SLA 的完整落地` |
| Short title | `AI SaMD Cybersecurity: Evidence, Threat Modeling, Patch SLA` |
| Talk type | `30:00` conference briefing for healthcare security, medical-device, product, and governance audiences |
| Recommended deck length | `14` slides, `28:30` spoken content, `1:30` buffer |
| Core thesis | An AI medical-device team does not sell a model; it sells a clinical product system that must be trustworthy, patchable, and auditable. |
| Audience promise | The audience will leave with a product-scale map, a regulatory evidence chain, a testing strategy, and a practical Patch SLA roadmap. |
| Authority angle | Translate FDA 524B, FDA 2025 guidance, TFDA-facing AI/ML SaMD thinking, NIST-style governance language, and security testing into one operating model for teams. |

## 2. Title Candidates

1. `AI 軟體醫材的資安實戰：從 FDA 524B 到 Threat Modeling 與 Patch SLA`
2. `你賣的不是模型：AI 醫材資安、證據鏈與 Patch SLA`
3. `Cyber Safety Is Patient Safety：AI SaMD 的資安治理落地`
4. `從模型到醫療系統：AI SaMD 的資安證據鏈`
5. `法規要的是證據，不是口號：AI 醫材資安實作路線圖`
6. `AI SaMD Security Operations：Threat Modeling, Testing, Patch SLA`

Recommended conference title: keep the supplied full title for program consistency. Use `你賣的不是模型` as the stage hook, not as the official title.

## 3. Audience Model

| Segment | What They Know | What They Need From This Talk | Design Response |
| --- | --- | --- | --- |
| Medical-device founders and product leads | They understand product pressure and regulatory review, but may under-scope cybersecurity as a late document task. | A practical way to decide what security work fits their product scale. | Use the four-scale product map and `30 / 60 / 90` roadmap. |
| Security engineers and consultants | They know testing and vulnerabilities, but may not connect findings to medical-device evidence and postmarket obligations. | A bridge from testing outputs to regulatory evidence and Patch SLA governance. | Emphasize finding disposition, retest evidence, SBOM, and decision records. |
| Regulatory and QA professionals | They know submission evidence, but may not see where AI/runtime/infrastructure risks enter engineering work. | A clean trace from architecture to threat model, controls, tests, fixes, and records. | Use the evidence-chain slide as the organizing spine. |
| Hospital and healthcare IT leaders | They care about continuity, vendor risk, and clinical operations. | A language for why AI product security affects patient safety and operational continuity. | Preserve `Cyber Safety is Patient Safety` as a standalone peak. |
| Cross-functional managers | They need shared vocabulary, ownership, and time-bounded execution. | A non-heroic operating model that small teams can start. | Use NIST-style governance language and Patch SLA decisions. |

## 4. Audience Pain Points And Misconceptions

| Audience State | Risk If Unaddressed | Talk Move |
| --- | --- | --- |
| `AI security = model robustness only` | The talk sounds narrow and misses product risk. | Slide 3 reframes the product as trust, patch, evidence. |
| `Regulation = documents for submission` | The regulatory section becomes passive compliance. | Slide 6 turns regulation into an evidence chain. |
| `Testing = tool list` | Security content becomes shallow and vendor-like. | Slide 11 defines white-box and black-box by decision output. |
| `Small teams cannot do this` | Audience dismisses the talk as enterprise-only. | Slide 13 gives `30 / 60 / 90` minimum evidence path. |
| `Cybersecurity is IT, not patient safety` | Healthcare relevance weakens. | Slide 10 directly connects cyber safety to patient safety. |

## 5. Desired Takeaways

By the end, the audience should be able to say:

1. `The product scale determines the cybersecurity evidence burden.`
2. `FDA 524B and FDA 2025 can be translated into monitor, patch, disclose, SBOM, and evidence traceability.`
3. `TFDA-facing AI/ML SaMD work needs model evidence, governance language, and stack-level security.`
4. `White-box and black-box testing are valuable only when findings become decisions and retest evidence.`
5. `Patch SLA is the operating bridge between vulnerability discovery, product trust, and audit readiness.`

## 6. Why This Topic Matters Now

AI medical products are moving from standalone model demonstrations into deployed systems: viewers, cloud runtimes, databases, update mechanisms, hospital integrations, and support workflows. That shift changes the security problem. The risk is no longer only whether a model is accurate. The risk is whether the product can be trusted, updated, monitored, fixed, and explained when deployed into clinical operations.

The talk matters because it converts a fragmented discussion into one practical operating sequence:

`product scale -> evidence chain -> AI security stack -> testing -> Patch SLA -> 30 / 60 / 90 execution`

## 7. What Makes This Talk Different

| Common Talk Pattern | This Talk's Replacement |
| --- | --- |
| Lists regulations without operational translation | Converts FDA/TFDA/NIST into evidence and ownership decisions |
| Treats AI security as model-only | Uses model/runtime/infrastructure stack and product-scale growth |
| Treats penetration testing as the climax | Makes Patch SLA and finding decisions the operational climax |
| Ends with broad best practices | Ends with a specific `30 / 60 / 90` small-team path |
| Uses fear-heavy healthcare examples | Uses controlled patient-safety framing without exposing private details |

## 8. Failure Modes And Countermeasures

| Failure Mode | Scoring Damage | Countermeasure |
| --- | --- | --- |
| Too much regulatory detail | Hurts Stage Rhythm and Time Control | Keep slide 6 to five evidence nodes and four FDA 524B verbs. |
| Weak narrative path | Hurts Structure and Narrative Design | Repeat the sequence: scope, evidence, test, decide, prove. |
| Overloaded technical slides | Hurts Visual Design and Delivery Quality | Use diagrams; move detail into speech or Q&A. |
| Not enough practical relevance | Hurts Audience Impact | Preserve Patch SLA and `30 / 60 / 90` as separate slides. |
| Rushed ending | Hurts Stage Presence and Audience Impact | Slide 14 must start by `27:40`; cut slide 11 detail first. |
| Sounds like a classroom report | Hurts Delivery Quality | Use decision verbs: `判斷`, `修補`, `重測`, `留下證據`, `誰負責`. |

## 9. Rubric-To-Design Translation Matrix

| Category | Points | Design Goal | Observable Success Criteria | Tactics | Failure Pattern | Slide Influence | Speaking Influence |
| --- | ---: | --- | --- | --- | --- | --- | --- |
| Structure and Narrative Design | 20 | Make the talk feel inevitable from model to trust system. | Audience can restate the arc in one sentence. | Use four-scale map; make Patch SLA the climax; close with trust-before-audit. | Sections feel like independent mini lectures. | Every slide has one governing message and a transition reason. | Name why the next section exists before moving. |
| Content Depth and Value | 20 | Deliver technical substance without overwhelming the room. | Security, regulatory, and product listeners each hear usable decisions. | Translate FDA 524B, FDA 2025, TFDA, NIST, testing, and Patch SLA into artifacts. | Tool-name dumping or framework name-dropping. | Use evidence chains, risk maps, and decision flows. | Explain what artifact or decision each concept produces. |
| Stage Rhythm and Time Control | 15 | Vary pace and protect the ending. | Speaker reaches slide 14 by `27:40` and finishes by `28:30`. | Heavy slides 6-7 followed by product-scale comparison and patient-safety reset. | Same tempo for all slides or rushing after slide 10. | Dense slides use progressive reveal; memory slides are quiet. | Slow on slides 3, 5, 10, 12, 14; accelerate through lists. |
| Delivery Quality | 15 | Sound precise, calm, and executive-technical. | Short sentences; no filler apology; strong bilingual technical terms. | Use Taiwan Traditional Chinese with standard English terms where useful. | Overexplaining acronyms or reading paragraphs. | Slides carry labels, not scripts. | Emphasize the four strong lines exactly. |
| Visual Design | 10 | Make meaning visible in three seconds. | Audience sees phrase, map, chain, contrast, or decision before explanation. | Use ladders, stacks, chains, side-by-side contrasts, and roadmaps. | Decorative AI/security motifs or paragraph slides. | One dominant visual object per slide. | Refer to diagrams only when they support the spoken decision. |
| Stage Presence | 10 | Project controlled authority. | Eye contact on memory lines; stillness at patient-safety and close. | Stand still for slides 3, 10, 12, 14; gesture only for architecture/process. | Wandering, looking back at slides, weak final posture. | Minimize text that forces speaker to read. | Pause after the strong lines; stop cleanly. |
| Audience Impact | 10 | Make the talk memorable and useful after the session. | Audience remembers `你賣的不是模型`, product scales, Patch SLA, and `30 / 60 / 90`. | Repeat five memory anchors and convert them into action. | Interesting but not actionable. | Preserve standalone memory slides. | End on principle, not administrative clutter. |

## 10. 30-Minute Time Architecture

Normal target: `28:30` content plus `1:30` buffer.

| Slide Range | Time | Cumulative | Function | Load |
| --- | ---: | ---: | --- | --- |
| 1-2 | `0:30` | `0:30` | Formal opening and required disclaimer | Light |
| 3 | `1:50` | `2:20` | Thesis hook | Emotional and conceptual |
| 4-5 | `4:10` | `6:30` | Why-now and product-scale map | Moderate |
| 6-7 | `7:30` | `14:00` | Regulatory evidence and local governance bridge | Heavy |
| 8-9 | `5:20` | `19:20` | Product-scale risk comparison | Moderate |
| 10 | `1:20` | `20:40` | Patient-safety peak and recovery | Emotional reset |
| 11-12 | `4:30` | `25:10` | Testing and Patch SLA | Technical and operational |
| 13-14 | `3:20` | `28:30` | Implementation roadmap and close | Practical and memorable |

Attention drop risk: after slide 7. Recovery move: make slide 8 concrete and phrase it as `第一層和第二層差在哪裡？`.

### Timing Variants

| Mode | Target | Rule |
| --- | ---: | --- |
| Normal | `28:30` | Full compact script; `1:30` buffer. |
| Safe | `27:30` | Remove secondary labels from slides 7, 8, 9, 11; preserve all memory lines. |
| Rushed | `25:00` | Slide 6 becomes evidence chain only; slide 7 one sentence per column; slide 13 one output per bucket. |
| Emergency | `20:00` | Skip slide 4 and slide 11 as standalone sections; mention AI infrastructure in slide 5 and testing output in slide 12. |

## 11. Narrative Architecture

Chosen mode: `myth -> reality -> operating framework -> implementation`.

This is stronger than a simple problem-solution structure because the audience likely begins with a false simplification: `AI SaMD security is mostly about model security or compliance paperwork.` The talk breaks that myth early, replaces it with product-scale reality, then gives an operating framework that feels usable.

| Narrative Beat | Slide | Audience Question | Answer |
| --- | ---: | --- | --- |
| Myth break | 3 | What are we really selling? | Not a model; a trustable, patchable, auditable system. |
| Why now | 4 | Why is this urgent in 2026? | AI is infrastructure; incidents disrupt care. |
| Map | 5 | How should I scope this? | Risk grows with architecture. |
| Evidence | 6 | What do regulators actually want? | A traceable evidence chain. |
| Translation | 7 | How does this work for Taiwan teams? | Model evidence, governance language, stack security. |
| Application | 8-9 | How does risk change by product scale? | Each layer adds attack surface and evidence burden. |
| Peak | 10 | Why does it matter beyond compliance? | Cyber safety is patient safety. |
| Operation | 11-12 | What do we do with findings? | Test, decide, patch, retest, archive. |
| Action | 13 | What can a small team start? | `30 / 60 / 90`. |
| Close | 14 | What should I remember? | Build security into the product before the audit. |

## 12. Visual Strategy

| Rule | Production Requirement | Scoring Link |
| --- | --- | --- |
| One dominant object | Each slide must be a phrase, ladder, chain, stack, contrast, or roadmap. | Visual Design |
| Low word count | Headlines should fit in one line when possible; supporting text must be one short sentence or labels. | Stage Rhythm |
| Color has meaning | Use accent only for risk, evidence, decision, or active layer. | Visual Design |
| No visual filler | Do not use random circuits, dark hacker imagery, glowing AI brains, stock hospital drama, or meaningless gradients. | Stage Presence |
| Technical slides use hierarchy | Put the conclusion in the title; put details in grouped labels. | Content Depth |
| Memory slides breathe | Slides 3, 10, 12, and 14 need negative space and no dense lists. | Audience Impact |

## 13. Audience Impact Design

| Moment | Desired Audience Reaction | Design Action |
| --- | --- | --- |
| First minute | `This is not another AI hype talk.` | Open with `你賣的不是模型`, not an agenda. |
| Slide 5 | `I can locate my product on this map.` | Four-scale ladder with evidence growth. |
| Slide 6 | `Regulation is traceability, not paperwork.` | Evidence chain, not legal text. |
| Slide 10 | `This is connected to patient safety.` | Standalone phrase and pause. |
| Slide 12 | `This is the operating mechanism we need.` | Decision-centered Patch SLA flow. |
| Final minute | `I know what to do next.` | `30 / 60 / 90` then one closing principle. |

## 14. Non-Negotiable Cut Rules

1. Never cut the CYBERSEC disclaimer slide; make it short instead.
2. Never cut the four-scale map.
3. Never cut `Cyber Safety is Patient Safety`.
4. Never cut `沒有 decision，就沒有治理；沒有證據，就沒有信任`.
5. Never add new content on the closing slide.
6. If over time, cut examples before cutting structure.

