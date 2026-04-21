# Decision-Grade Deck Upgrade Report

Date: `2026-04-21`

Scope: compact `14`-slide CYBERSEC 2026 AI SaMD cybersecurity deck.

This report is the single deep-upgrade artifact for the compact deck. It does not replace `data/presentation_os.json`; it gives the editorial diagnosis and rewrite target that the structured source should follow.

## SECTION A - Executive Diagnosis

### Overall Judgment

The current deck has a strong skeleton but a weak visible reasoning layer. It has the right arc - product trust, product scale, evidence chain, testing, Patch SLA, and 30 / 60 / 90 roadmap - but too much of the intellectual work is hidden in narration. On screen, several slides still look like labels rather than decision-grade reasoning.

The deck is not fundamentally wrong. It needs a content-density upgrade inside the same `14`-slide envelope:

- Make every major slide answer `why this matters`, `how it works`, and `what decision it supports`.
- Convert framework names into artifacts, workflows, evidence, and ownership decisions.
- Add one realistic failure path so the patient-safety claim feels concrete rather than rhetorical.
- Make technical slides show mechanisms, not just categories.
- Make manager-facing value explicit: risk reduction, resource focus, decision gates, and measurable outputs.

### Why It Currently Feels Shallow

- Many slides use strong slogans but do not show enough mechanism on the slide itself.
- Slides 6 and 7 carry the real intellectual burden, but their visible forms are still framework bridges, not audit-ready evidence logic.
- Slides 8 and 9 are useful product-scale examples, but they need stronger consequences and controls by scale.
- Testing is framed as white-box versus black-box, but the more valuable idea is `which question each testing method answers`.
- Patch SLA is the strongest operational idea, but it should more clearly show owner, decision type, residual-risk rationale, retest, and archive.
- The management layer is implied, not explicit enough: what must a supervisor fund, staff, measure, and decide?

### Biggest Structural Weaknesses

| Weakness | Why It Matters | Fix |
| --- | --- | --- |
| The talk starts with a thesis but not enough real-world consequence. | General audiences may understand the sentence but not feel the operational risk. | Add a simple failure path early: update path or viewer disruption -> clinical workflow delay -> vendor/clinical decision. |
| Product scale is good but under-used. | Engineers need architecture boundaries; managers need scope and prioritization. | Make product boundary the master decision variable for evidence burden, testing depth, and patch operations. |
| Evidence slide is too compressed. | It can sound like compliance vocabulary instead of real engineering traceability. | Translate FDA 524B and FDA 2025 guidance into evidence artifacts: architecture view, threat model, controls, tests, finding disposition, patch/retest record. |
| NIST / governance slide risks name-dropping. | Technical and manager audiences dislike framework recitation when it does not produce decisions. | Reframe as three risk layers: model behavior, software stack, clinical workflow. Use NIST language only to coordinate decisions across roles. |
| Testing slide is still method-centric. | Engineers ask what the tests actually prove; managers ask what the report changes. | Turn testing into a portfolio matrix: method, question answered, output, decision. |
| 30 / 60 / 90 roadmap lacks metrics. | Managers need a way to know whether the plan worked. | Add output metrics: asset inventory coverage, threat-model coverage, finding closure, retest evidence, CVD readiness. |

### Strategy Revision Needed?

Yes. The current strategy is good as a `topic introduction`, but the requested audience needs a `decision-support narrative`.

Revised direction:

> AI SaMD cybersecurity is a clinical product-risk operating system. The team must define the product boundary, trace evidence from architecture to test results, decide findings, and prove repairability over the product lifecycle.

### Slide-Level Diagnostic

| Slide | Current Role | Main Weakness | Why It Matters | Recommended Fix | Priority |
| ---: | --- | --- | --- | --- | --- |
| 1 | Formal title | Subtitle lists topics, not the decision promise. | Audience may expect a regulatory/tool lecture. | Position the talk as `from model demo to product trust`. | Medium |
| 2 | Required disclaimer | Fine as-is. | It should not carry content. | Keep brief and separate. | Low |
| 3 | Thesis hook | Strong line, but it can sound like a slogan unless linked to accountability. | General audience needs plain meaning; managers need consequence. | Add the product-responsibility frame: clinical workflow, repairability, auditability. | High |
| 4 | Why-now urgency | Too abstract: `AI infrastructure` needs a concrete failure path. | Without an example, urgency feels generic. | Show AI stack -> update/support/data path -> workflow interruption. | High |
| 5 | Product-scale map | Useful, but not yet a decision framework. | Engineers need boundary logic; managers need prioritization. | Add the governing question: `what crosses the boundary, who depends on it, what evidence grows?` | High |
| 6 | Regulation to evidence | Correct but dense; visible content may still feel like labels. | This is the credibility core. If shallow, the deck fails. | Map official obligations to evidence artifacts and traceability. | High |
| 7 | Model/governance/stack bridge | Risks framework-name dropping. | Engineers may see it as handwavy; managers may not see decisions. | Reframe as three risk layers plus NIST as shared language. | High |
| 8 | Scale 1-2 example | Good but needs consequence and boundary. | Viewer risk is easy to underestimate. | Explain how wrapper changes the attack surface: parser, upload, cache, output interpretation. | Medium |
| 9 | Scale 3-4 example | Good, but needs operational ownership. | Managers need to know this becomes vendor risk, continuity risk, and support burden. | Add identity/API/database/audit/backup plus hospital integration/update path. | Medium |
| 10 | Patient-safety peak | Strong phrase but under-supported if previous slide lacks failure chain. | It can sound dramatic instead of reasoned. | Make it a conclusion from concrete continuity risk, not a standalone claim. | Medium |
| 11 | Testing strategy | Too binary: white-box vs black-box. | Technical audience needs testing coverage logic. | Convert to testing portfolio: SCA/SBOM, static/dynamic, fuzz, black-box, pen test, retest. | High |
| 12 | Patch SLA climax | Strongest operational slide, but needs decision taxonomy and evidence. | This is what makes the talk manager-useful. | Add owner, severity, decision, due date, compensating control, retest, archive. | High |
| 13 | 30 / 60 / 90 roadmap | Practical but not measurable enough. | Supervisors need resource and progress logic. | Add deliverables, owner, and metric per month. | High |
| 14 | Closing | Good, but could end with a sharper decision checklist. | TA/evaluator should hear a defensible final takeaway. | Close with three questions: boundary, evidence chain, repair proof. | Medium |

## SECTION B - Revised Presentation Strategy

### Target Audience

- General audience: needs a plain explanation of why medical AI cybersecurity affects real clinical work.
- Engineers / technical professionals: need architecture boundaries, mechanisms, testing logic, evidence traceability, and implementation constraints.
- Managers / supervisors / decision-makers: need strategic risk, resource focus, governance points, measurable outcomes, and a small-team path.

### Communication Objective

Move the audience from:

`AI SaMD cybersecurity = model/security/compliance topic`

to:

`AI SaMD cybersecurity = product boundary + evidence chain + testing portfolio + finding governance + repair proof`.

### Revised Narrative Arc

1. Frame: you do not sell only a model; you sell a clinical product responsibility.
2. Urgency: AI is now part of runtime, data, update, and clinical-support infrastructure.
3. Scope: product scale determines attack surface and evidence burden.
4. Evidence: official expectations become traceable artifacts, not slogans.
5. Mechanism: model, software stack, and clinical workflow each create different risks.
6. Application: risk grows from model artifact to viewer, platform, and connected system.
7. Consequence: cyber safety becomes patient-safety and service-continuity risk.
8. Operation: testing turns risk into findings; Patch SLA turns findings into decisions.
9. Action: a small team can start with a 30 / 60 / 90 evidence loop.
10. Close: build security into the product so audit documents become evidence, not theater.

### Core Thesis

AI SaMD cybersecurity is not a model-security checklist. It is a clinical product-risk operating system: define the product boundary, generate traceable evidence, test real exposure, govern findings, and prove repairability.

### What the Audience Should Remember

- Product boundary decides risk.
- Evidence chain decides credibility.
- Testing is useful only when findings become decisions.
- Patch SLA is governance, not ticket hygiene.
- Patient safety includes service continuity and repairability.

### Desired Effect

- Emotional: this topic is serious without being fear-based.
- Intellectual: the audience sees a coherent model instead of disconnected regulations and tools.
- Practical: managers and teams know the next decision and the first 90-day operating loop.

## SECTION C - Improved Outline

| Slide | Revised Title | Slide Objective | Audience Emphasis | Key Message |
| ---: | --- | --- | --- | --- |
| 1 | AI SaMD Cybersecurity: From Model Demo to Product Trust | Set the promise and scope. | Mixed | This talk is about building a trustable clinical product system. |
| 2 | Required CYBERSEC Disclaimer | Satisfy organizer requirement. | Mixed | Separate compliance beat from talk substance. |
| 3 | 你賣的不是模型，是臨床產品責任 | Break the model-only frame. | General / manager | The product responsibility includes trust, repairability, and auditability. |
| 4 | Why Now: AI Is Becoming Care Infrastructure | Make urgency concrete. | General / manager | Security failures can interrupt clinical workflow when AI enters runtime, data, update, and support paths. |
| 5 | Product Boundary Decides Risk | Install the master decision map. | Mixed | The same model creates different obligations depending on product scale. |
| 6 | From Obligation to Evidence Chain | Translate official expectations into artifacts. | Engineer / manager | FDA 524B and FDA 2025 guidance point to lifecycle evidence, not paperwork. |
| 7 | Three Risk Layers, One Governance Language | Avoid framework name-dropping. | Engineer / manager | Model behavior, software stack, and clinical workflow need one shared decision language. |
| 8 | Scale 1-2: Artifact to User-Facing System | Show the first architecture jump. | Engineer | A viewer turns an artifact into an attackable workflow. |
| 9 | Scale 3-4: Platform to Clinical Continuity | Show the second architecture jump. | Engineer / manager | Platform and hospital integration create business, continuity, and patient-safety exposure. |
| 10 | Security Failure Becomes Safety Risk | Create the ethical peak. | General / manager | Cyber safety is patient safety when disruption affects care. |
| 11 | Testing Portfolio: What Question Does Each Test Answer? | Make testing non-generic. | Engineer | Each test method should answer a decision question and produce evidence. |
| 12 | Finding Governance: Patch SLA | Make the operating model explicit. | Manager / engineer | Every finding needs owner, severity, decision, repair, retest, and archived evidence. |
| 13 | 30 / 60 / 90: Minimum Evidence Loop | Convert talk into action. | Manager | A small team can build minimum evidence, workflow, and validation in 90 days. |
| 14 | Trust Before Audit | Close with a decision checklist. | Mixed | If you can define boundary, trace evidence, and prove repairs, the deck has done its job. |

## SECTION D - Slide-by-Slide Rewrite

### Slide 1

Original weakness: The title is accurate but topic-list driven.

Rewrite strategy: Make the deck promise a decision model, not a tour of keywords.

New slide title: `AI SaMD Cybersecurity: From Model Demo to Product Trust`

Revised slide content:

- `AI 軟體醫材的資安實戰`
- `Product boundary -> Evidence chain -> Finding decision -> Repair proof`
- `林家聖 | CYBERSEC 2026`

Suggested narration:

> 各位好，我是林家聖。今天不是要背法規，也不是展示工具清單。我想用一個問題串起來：一個 AI model 要變成可信任的醫療產品，中間需要留下哪些證據和決策？

Optional visual recommendation: Keep restrained title slide, but replace the three-node topic triangle with a four-step operating path.

### Slide 2

Original weakness: None. It is a required compliance slide.

Rewrite strategy: Keep it short so it does not steal cognitive load.

New slide title: `Required CYBERSEC Disclaimer`

Revised slide content:

- Use official organizer disclaimer image.

Suggested narration:

> 這是大會必要的 disclaimer，我在這裡停一下，讓大家看見。接下來直接進入今天真正的問題。

Optional visual recommendation: Full-slide official image only.

### Slide 3

Original weakness: `你賣的不是模型` is memorable, but currently depends too much on the speaker to explain the consequence.

Rewrite strategy: Add the plain-language product-responsibility layer.

New slide title: `你賣的不是模型，是臨床產品責任`

Revised slide content:

- `你賣的不是模型`
- `Clinical workflow`
- `Repairability`
- `Auditability`

Suggested narration:

> 醫師看到的是結果，病人承受的是後果，公司要負責的是整個使用情境。模型準不準只是其中一件事。只要它進入臨床流程，團隊就要能說清楚：誰用、在哪裡用、出問題怎麼修、修完怎麼證明。

General audience takeaway: This is not only about AI accuracy.

Engineer respect point: Scope expands from model artifact to runtime, interface, update, and evidence.

Manager value: The company is selling a risk-bearing clinical product, not only a model component.

Optional visual recommendation: Big phrase plus three small anchors: `Workflow / Repair / Evidence`.

### Slide 4

Original weakness: `AI becomes infrastructure` is true but abstract.

Rewrite strategy: Add a concrete failure path without fear-heavy details.

New slide title: `Why Now: AI Is Becoming Care Infrastructure`

Revised slide content:

- `Model`
- `Runtime`
- `Data / Identity`
- `Update / Support`
- `Clinical continuity`
- `Failure path: update or access issue -> service interruption -> care workflow delay`

Suggested narration:

> 2026 年的醫療 AI 不只是模型檔。它會接 runtime、資料、帳號、更新鏈、客服支援，最後接到臨床流程。這時候資安事件不一定要直接傷害模型才有影響；只要更新路徑、登入、viewer、資料庫或支援服務中斷，就可能讓臨床流程延遲或改走人工 fallback。

General audience takeaway: Cybersecurity can affect whether the tool is available and trustworthy during care.

Engineer respect point: Risk enters through deployment and update/support paths, not only model weights.

Manager value: This is continuity risk and vendor-risk management.

Optional visual recommendation: Left stack, right failure path line with one interruption node.

### Slide 5

Original weakness: The four-scale map is useful but not yet decision-grade.

Rewrite strategy: Make boundary the master variable for risk, evidence, testing, and operations.

New slide title: `Product Boundary Decides Risk`

Revised slide content:

- `1. Model`
- `2. Viewer`
- `3. Platform / Database`
- `4. Connected Medical System`
- `Decision question: what crosses the boundary, who depends on it, what evidence grows?`

Suggested narration:

> 同一個模型，放在不同產品邊界裡，資安責任完全不同。只有 model，要證明來源、依賴、更新邊界。加 viewer，就有 parser、upload、cache、output 呈現。變平台，就有 identity、API、database、audit、backup。進醫院環境，就有 PACS/HIS、網路、更新伺服器、遠端支援和 continuity。

General audience takeaway: Bigger product boundary means bigger responsibility.

Engineer respect point: Architecture determines attack surface.

Manager value: This tells you how much evidence and testing to budget.

Optional visual recommendation: Four-step ladder with a bottom line `Evidence / Testing / Operations grow`.

### Slide 6

Original weakness: Correct but can still sound like compliance terminology.

Rewrite strategy: Translate official requirements into evidence artifacts.

New slide title: `From Obligation to Evidence Chain`

Revised slide content:

- `Architecture view`
- `Threat model`
- `Control`
- `Test`
- `Finding decision`
- `Patch / retest record`
- Side rail: `Monitor / CVD / Patch / SBOM`

Suggested narration:

> FDA 524B 可以壓成幾個生命週期義務：上市後要 monitor、identify、address vulnerability；要有 coordinated vulnerability disclosure；要能提供 updates and patches；也要提供 SBOM。FDA 2025 guidance 往下要求的是安全架構視圖、邊界、角色、介面、threat model、testing evidence，以及 traceability。換成工程語言，就是一條證據鏈：架構怎麼畫、威脅怎麼判斷、控制怎麼設計、測試打到哪裡、finding 怎麼決定、修補和重測怎麼留下紀錄。

General audience takeaway: Regulation asks teams to prove how safety is maintained over time.

Engineer respect point: Traceability must connect architecture, threat model, controls, tests, findings, and retest.

Manager value: This defines what evidence the organization must produce and maintain.

Optional visual recommendation: Evidence chain with artifact labels under each node.

### Slide 7

Original weakness: The current version risks sounding like NIST keyword recitation.

Rewrite strategy: Reframe frameworks as shared language for three risk layers.

New slide title: `Three Risk Layers, One Governance Language`

Revised slide content:

- `Model behavior`
  - `Intended use`
  - `Data / V&V`
  - `Limits`
- `Software stack`
  - `Provenance`
  - `Isolation`
  - `Updates`
- `Clinical workflow`
  - `User roles`
  - `Continuity`
  - `Residual risk`

Suggested narration:

> 我建議不要把 NIST 當成要背的控制項。它比較像共同語言。AI RMF 幫我們問 Govern、Map、Measure、Manage：誰決策、情境是什麼、怎麼量測、怎麼管理。CSF 2.0 幫資安營運補上 Govern、Identify、Protect、Detect、Respond、Recover。真正要講清楚的是三層：模型行為、軟體堆疊、臨床流程。

General audience takeaway: Risk is not only technical; it depends on use context.

Engineer respect point: Model evidence and stack security are separated but connected.

Manager value: Governance language helps assign responsibility and risk tolerance.

Optional visual recommendation: Three columns, with NIST as a small footer `shared language, not checklist`.

### Slide 8

Original weakness: Good comparison, but the mechanism needs to be clearer.

Rewrite strategy: Show how a viewer turns an artifact into a user-facing attack surface.

New slide title: `Scale 1-2: Artifact to User-Facing System`

Revised slide content:

- `Model`
  - `Artifact provenance`
  - `Data lineage`
  - `SBOM`
  - `Update boundary`
- `Viewer`
  - `Parser`
  - `Upload`
  - `Cache`
  - `Output interpretation`

Suggested narration:

> 第一層的風險重點是 artifact：模型從哪裡來，資料怎麼追，依賴怎麼列，更新邊界在哪裡。第二層加了 viewer，就變成使用情境。攻擊者不一定碰模型；他可以碰檔案解析、上傳流程、暫存、輸出呈現，甚至影響使用者怎麼解讀結果。

General audience takeaway: Adding a user interface changes the risk.

Engineer respect point: Parser/upload/cache/output are concrete surfaces.

Manager value: Scope increase means testing and documentation increase.

Optional visual recommendation: Two-panel comparison with `boundary crossed` marker between panels.

### Slide 9

Original weakness: Good but needs sharper operational and management implications.

Rewrite strategy: Make platform/hospital integration visibly about continuity and vendor responsibility.

New slide title: `Scale 3-4: Platform to Clinical Continuity`

Revised slide content:

- `Platform / Database`
  - `Identity`
  - `API`
  - `Database`
  - `Audit log`
  - `Backup`
- `Connected Medical System`
  - `PACS / HIS`
  - `Hospital network`
  - `Update server`
  - `Remote service`
  - `Downtime fallback`

Suggested narration:

> 第三層開始，資安就是公司風險：帳號、權限、API、資料庫、audit log、backup 都會進來。第四層進到醫院環境，問題就不只是產品保護，而是 clinical continuity。你的更新伺服器、遠端支援、PACS/HIS 連接、醫院網路邊界和 downtime fallback，都會影響醫院怎麼信任你這個供應商。

General audience takeaway: Connected medical systems affect operations, not just screens.

Engineer respect point: Integration points and backup/fallback are explicit.

Manager value: This is procurement trust, service continuity, support load, and incident accountability.

Optional visual recommendation: System map with `vendor-owned`, `shared`, and `hospital-owned` zones.

### Slide 10

Original weakness: Strong phrase, but it must feel earned by the previous slides.

Rewrite strategy: Make it the consequence of continuity and repairability.

New slide title: `Security Failure Becomes Safety Risk`

Revised slide content:

- `Cyber Safety Is Patient Safety`
- `Availability`
- `Integrity`
- `Repairability`

Suggested narration:

> Cyber Safety is Patient Safety. 這句話不是口號。當資安問題讓結果不可用、資料不可信、服務無法更新、finding 沒有人決定，最後影響的就是臨床流程和病人照護的連續性。

General audience takeaway: Cyber risk can become care risk.

Engineer respect point: Availability, integrity, and repairability are concrete safety bridges.

Manager value: Security investment protects clinical trust and vendor credibility.

Optional visual recommendation: Full-screen phrase with three small anchors underneath.

### Slide 11

Original weakness: `White-box + black-box` is too narrow for the depth expected.

Rewrite strategy: Present testing as a portfolio of questions.

New slide title: `Testing Portfolio: What Question Does Each Test Answer?`

Revised slide content:

- `SBOM / SCA: what components and known vulnerabilities exist?`
- `White-box: what can we fix before release?`
- `Fuzz / abuse cases: what breaks under malformed input?`
- `Black-box: what is externally exposed?`
- `Pen test: can small issues chain into real risk?`
- `Retest: did the repair work?`

Suggested narration:

> Testing 不是工具名稱競賽。每一種測試都要回答一個決策問題。SBOM/SCA 回答組成和已知漏洞；white-box 回答 release 前可修什麼；fuzz 和 abuse case 回答異常輸入會不會打壞流程；black-box 回答外部看得到什麼；penetration test 回答問題能不能被串成真實風險；retest 回答修補是否成立。

General audience takeaway: Testing is useful because it turns uncertainty into decisions.

Engineer respect point: Coverage questions match FDA-style testing evidence and practical security validation.

Manager value: Testing budget should be tied to decision value, not tool count.

Optional visual recommendation: Six-row matrix: method, question, output, decision.

### Slide 12

Original weakness: Strong but still could look like ticket workflow.

Rewrite strategy: Make governance and residual-risk decision explicit.

New slide title: `Finding Governance: Patch SLA`

Revised slide content:

- `Finding`
- `Owner`
- `Severity`
- `Decision`
- `Due date`
- `Patch / compensate / defer / not applicable`
- `Retest`
- `Evidence archive`

Suggested narration:

> Patch SLA 在這裡不是 FDA 原文裡的固定名詞，而是一個 operating model。真正成熟的團隊不是沒有漏洞，而是每個 finding 進來後，知道 owner 是誰、severity 怎麼判斷、決策是 fix now、compensate、defer 還是 not applicable、期限在哪裡、修完誰重測、證據放哪裡。

General audience takeaway: Security work is a decision process, not only technical repair.

Engineer respect point: Finding disposition and retest evidence close the loop.

Manager value: This is accountability, prioritization, and audit readiness.

Optional visual recommendation: Keep `Decision` as largest node; add owner/severity/due-date tags.

### Slide 13

Original weakness: Practical but too list-like; lacks measurable proof of progress.

Rewrite strategy: Add deliverable, owner, and metric per phase.

New slide title: `30 / 60 / 90: Minimum Evidence Loop`

Revised slide content:

- `30 days: inventory`
  - `assets / SBOM / data flow`
  - `metric: coverage known`
- `60 days: workflow`
  - `threat model / CI gates / finding workflow`
  - `metric: findings routed`
- `90 days: validation`
  - `pen test / CVD / Patch SLA / retest evidence`
  - `metric: repair proof`

Suggested narration:

> 小團隊不要第一天假裝有大型制度。30 天先讓東西看得見；60 天讓風險能進流程；90 天讓外部驗證、CVD、Patch SLA 和 retest evidence 接起來。重點不是三個月完美，而是三個月後公司開始自動留下可信證據。

General audience takeaway: There is a realistic starting path.

Engineer respect point: The plan produces concrete artifacts.

Manager value: The plan has measurable outputs and sequencing.

Optional visual recommendation: Three cards with `output / owner / metric`, not just deliverables.

### Slide 14

Original weakness: Good closing line, but can be sharpened into a final decision checklist.

Rewrite strategy: End with the three tests of maturity.

New slide title: `Trust Before Audit`

Revised slide content:

- `先把安全做進產品`
- `法規文件才會自然長出來`
- `Can we define the boundary?`
- `Can we trace the evidence?`
- `Can we prove the repair?`

Suggested narration:

> 如果今天只留下三個問題，就是：我們能不能定義產品邊界？能不能把 evidence chain 接起來？能不能證明 finding 被修補、被重測、被追蹤？先把安全做進產品，法規文件才會自然長出來。謝謝大家。

General audience takeaway: Mature teams can explain and prove their work.

Engineer respect point: Boundary, traceability, and repair proof are concrete.

Manager value: These three questions are a boardroom-safe readiness test.

Optional visual recommendation: Closing phrase plus three quiet checklist questions.

## SECTION E - Missing Content to Add

### Examples

- A public-safe failure path: update/support/login/viewer interruption causes clinical workflow delay and fallback.
- A public-source example anchor: FDA's Contec/Epsimed patient monitor safety communication shows how connected monitoring, unauthorized control, data exfiltration, and network-scale exposure can become patient/caregiver/facility concerns.
- A realistic AI SaMD example: model-only package versus viewer versus platform versus hospital-integrated service.

### Workflows

- Product boundary workflow: define product scale -> identify interfaces -> assign evidence burden -> choose testing depth.
- Evidence chain workflow: architecture -> threat model -> control -> test -> finding disposition -> patch/retest record.
- Finding governance workflow: intake -> triage -> decision -> repair/compensate/defer -> retest -> evidence archive.

### Comparisons

- Model-only risk versus viewer risk.
- Platform risk versus connected medical system risk.
- Testing as tool list versus testing as decision support.
- Compliance document versus engineering evidence.

### Evidence Types

- Security architecture views.
- Threat model with assumptions and boundaries.
- SBOM and dependency evidence.
- Security control traceability.
- Testing evidence, including abuse/misuse, malformed input, fuzzing, attack surface analysis, vulnerability chaining, SCA, static/dynamic analysis, and penetration testing.
- Finding disposition rationale and retest proof.
- Updateability and patchability process evidence.

### Diagrams

- Four-scale product-boundary ladder.
- Evidence-chain traceability diagram.
- Three risk-layer map: model behavior / software stack / clinical workflow.
- Testing portfolio matrix.
- Patch SLA decision flow.
- 30 / 60 / 90 evidence loop.

### Metrics

- Asset inventory coverage.
- SBOM coverage and freshness.
- Threat-model coverage by product boundary.
- Security gate pass/fail trend.
- Finding age by severity.
- Retest completion rate.
- Deferred-finding rationale coverage.
- Patch/update release-history completeness.
- CVD intake readiness.

### Decision Points

- Which product scale are we actually shipping?
- Which interfaces cross the product boundary?
- Which risks can create clinical workflow disruption?
- Which test method answers which release decision?
- Which findings must be fixed before release?
- Which findings can be compensated or deferred with rationale?
- What evidence must be ready before customer, regulator, or audit discussion?

## SECTION F - Final Quality Check

| Criterion | Judgment | Reason |
| --- | --- | --- |
| Understandable to general audience | Pass if rewritten as above | Uses product responsibility, workflow disruption, and simple examples. |
| Technically respectable | Pass if slide 6, 7, 11, and 12 gain mechanism | Adds architecture boundaries, evidence artifacts, testing coverage, and finding disposition. |
| Strategically meaningful | Pass | Management sees resource focus, ownership, roadmap, and metrics. |
| Logically coherent | Pass | Arc moves from boundary -> evidence -> testing -> governance -> roadmap. |
| Content-rich without bloated | Conditional pass | Keep visible text compact; place depth in narration and speaker notes. |
| Speaker-friendly | Pass | Each slide has one job and a stage line. |
| Decision-useful | Pass | The final model gives readiness questions and 90-day outputs. |

### Remaining Weaknesses

- The compact `14`-slide constraint is useful for delivery but forces compression. If this becomes a longer training session, add separate slides for `testing portfolio matrix`, `evidence artifact glossary`, and `finding severity/SLA table`.
- The PPTX builder now uses public `pptxgenjs`; a full rebuilt editable PPTX, PDF export, and preview PNG set can be regenerated in this Ubuntu environment with `npm run build:deck`.
- TFDA-specific AI/ML SaMD claims should remain conservative unless anchored to a current official TFDA source. Use TFDA-facing language as local preparation framing, not as a precise legal quote, unless separately verified.

### Source Verification Notes

- FDA FAQ on section 524B confirms lifecycle cybersecurity requirements for cyber devices: monitoring, identifying, and addressing postmarket vulnerabilities and exploits; coordinated vulnerability disclosure; update/patch processes; and SBOM. Source: <https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity-medical-devices-frequently-asked-questions-faqs>
- FDA 2025 final premarket cybersecurity guidance supports the evidence-chain framing: security architecture views, product boundaries, user roles, interfaces, traceability, updateability/patchability, and testing evidence. Source: <https://www.fda.gov/files/guidance%20documents/published/GUI00001825-final-PremarketCybersecurity-2025.pdf>
- FDA 2025 guidance also supports testing portfolio language: abuse/misuse cases, malformed inputs, robustness, fuzzing, attack surface analysis, vulnerability chaining, closed-box scanning, software composition analysis, static/dynamic analysis, and penetration testing. Same source as above.
- NIST AI RMF supports the AI governance-language framing with `Govern`, `Map`, `Measure`, and `Manage`; it also emphasizes lifecycle, context, measurement, and management of AI risks. Source: <https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf>
- NIST CSF 2.0 supports the cyber-governance language with `Govern`, `Identify`, `Protect`, `Detect`, `Respond`, and `Recover`, and describes CSF as a high-level taxonomy for understanding, assessing, prioritizing, and communicating cybersecurity outcomes. Source: <https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf>
- FDA's Contec/Epsimed patient monitor safety communication is a public example showing why connected medical-device cybersecurity can become patient, caregiver, healthcare-provider, and facility-level risk. Source: <https://www.fda.gov/medical-devices/safety-communications/cybersecurity-vulnerabilities-certain-patient-monitors-contec-and-epsimed-fda-safety-communication>
