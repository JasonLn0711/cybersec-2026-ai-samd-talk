# 02 Compact 14-Slide Deck Spec

Purpose: build the recommended compact `14`-slide CYBERSEC deck. This file merges the earlier slide blueprint, compact plan, detailed execution spec, and visual production notes into one build-ready document.

## 1. Production Rules

| Rule | Required Build Behavior | Rubric Protected |
| --- | --- | --- |
| Slide title is a claim | Prefer `Risk grows with architecture` over `Product Scales`. | Structure and Narrative Design |
| One visual object | Each slide has one phrase, ladder, evidence chain, stack, comparison, flow, or roadmap. | Visual Design |
| Labels beat paragraphs | Diagram labels may be technical; paragraphs belong in speaker notes. | Stage Rhythm and Time Control |
| No sensitive examples | No proprietary code, private architecture, private hospital/client detail, raw submission, student record, exploit recipe, or patent-sensitive mechanism. | Stage Presence |
| Build for projection | Large type, high contrast, and enough empty space for a conference room. | Visual Design |
| Preserve five memory anchors | Slides 3, 5, 10, 12, and 14 are the audience's mental anchors. | Audience Impact |

Slide gate: after building these specs into actual slides, run `06_slide_design_constraint_system.md`. This deck spec defines intent and content; the slide gate decides whether the visual execution is production-ready.

Strictness rule: do not force technical diagram labels into decorative minimalism. The hard `12`-word limit applies to headline/sentence text. Diagram labels are allowed only when they behave as labels and remain visually scannable.

## 1.1 Generated Deck Build Path

The active build source is `data/presentation_os.json`. It preserves the compact `14`-slide structure, slide timing, on-screen text, constraint status, and speaker notes in one machine-readable file.

Regenerate the report artifacts first:

```bash
python3 tools/generate_presentation_outputs.py
```

Then build the editable optimized deck:

```bash
/Users/iKev/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/bin/node tools/build_optimized_deck.mjs
```

Output deck:

`outputs/deck/cybersec-2026-ai-samd-compact-optimized.pptx`

Build rule: the PPTX must remain editable PowerPoint text/shapes/diagrams. Slide 2 may use the official CYBERSEC disclaimer image because it is a required organizer source artifact; all other major talk text must remain editable.

## 2. 23-To-14 Consolidation Map

| Compact Slide | New Title | Source Slides | Reason For Merge |
| ---: | --- | --- | --- |
| 1 | AI 軟體醫材的資安實戰 | 1 | Keep formal opening. |
| 2 | Required CYBERSEC Disclaimer | 2 | Required compliance beat. |
| 3 | 你賣的不是模型 | 3 | Preserve thesis hook. |
| 4 | AI 變成基礎設施，資安變成照護連續性 | 4-5 | Merge trend and urgency. |
| 5 | 四種產品尺度：風險會跟架構一起長大 | 6 | Preserve central map. |
| 6 | 法規要的是一條證據鏈 | 7-9 | Merge FDA 524B and FDA 2025 around evidence traceability. |
| 7 | 台灣團隊需要同時說清楚模型、治理與 AI stack | 10-12 | Merge TFDA, NIST, and stack security. |
| 8 | Scale 1-2：Model 到 Viewer | 13-14 | Pair early product scales. |
| 9 | Scale 3-4：Platform 到 Connected Medical System | 15-16 | Pair operating-risk scales. |
| 10 | Cyber Safety Is Patient Safety | 17 | Preserve emotional peak. |
| 11 | Testing Strategy：White-box + Black-box | 18-19 | Merge complementary testing roles. |
| 12 | Patch SLA：Every Finding Needs A Decision | 20 | Preserve operational climax. |
| 13 | Small Team 30 / 60 / 90 | 21-22 | Merge playbook and roadmap. |
| 14 | 先建立信任，再面對稽核 | 23 | Preserve clean close. |

## 3. Timing Plan

| Slide | Time | Cumulative | Timing Job |
| ---: | ---: | ---: | --- |
| 1 | `0:10` | `0:10` | Establish presence. |
| 2 | `0:20` | `0:30` | Clear compliance. |
| 3 | `1:50` | `2:20` | Land thesis. |
| 4 | `2:10` | `4:30` | Make urgency relevant. |
| 5 | `2:00` | `6:30` | Install map. |
| 6 | `4:10` | `10:40` | Deliver regulatory substance. |
| 7 | `3:20` | `14:00` | Bridge local governance and AI stack. |
| 8 | `2:40` | `16:40` | Explain early product-scale risk. |
| 9 | `2:40` | `19:20` | Explain platform and clinical continuity risk. |
| 10 | `1:20` | `20:40` | Emotional reset. |
| 11 | `2:20` | `23:00` | Contrast testing roles. |
| 12 | `2:10` | `25:10` | Deliver Patch SLA climax. |
| 13 | `2:30` | `27:40` | Give executable roadmap. |
| 14 | `0:50` | `28:30` | Close cleanly. |

Checkpoint rule: if slide 7 ends after `14:30`, compress slides 8-9 to one example per side and protect slides 10, 12, 13, and 14.

## 4. Slide Production Specs

### Slide 1. AI 軟體醫材的資安實戰

| Field | Spec |
| --- | --- |
| Objective | Establish formal speaker authority and serious topic frame. |
| One-sentence message | This is a product-trust and medical-device cybersecurity talk, not an AI hype talk. |
| Audience understanding | The speaker will connect FDA 524B, threat modeling, and Patch SLA into one implementation path. |
| Screen copy | `AI 軟體醫材的資安實戰`<br>`從 FDA 524B 到 Threat Modeling 與 Patch SLA`<br>`林家聖 | CYBERSEC 2026 Healthcare Security Forum` |
| Visual form | Restrained title slide with faint product-system outline. |
| Build behavior | None. |
| Speaker note | `各位好，我是林家聖。今天的題目是 AI 軟體醫材的資安實戰。` |
| Do not show | Long biography, credential stack, logos that compete with the title. |
| Transition out | `關鍵字很多，但今天我只想留下三件事：信任、修補、證據。` |
| Rubric support | Stage Presence, Structure and Narrative Design. |

### Slide 2. Required CYBERSEC Disclaimer

| Field | Spec |
| --- | --- |
| Objective | Meet organizer requirement without turning compliance into narrative content. |
| One-sentence message | This is a required compliance beat and should be visually quiet. |
| Audience understanding | The speaker respects the event rule and will move quickly into substance. |
| Screen copy | Official disclaimer image only. |
| Visual form | Full-slide organizer-provided disclaimer. |
| Build behavior | None. |
| Speaker note | `這是大會必要的 disclaimer，我在這裡停一下，讓大家看見。接下來我們直接進入今天真正的問題。` |
| Do not show | Speaker interpretation, extra legal summary, decorative frame. |
| Transition out | Move directly to slide 3. |
| Rubric support | Stage Rhythm and Time Control, Visual Design. |

### Slide 3. 你賣的不是模型

| Field | Spec |
| --- | --- |
| Objective | Break the model-only mental frame. |
| One-sentence message | AI SaMD teams sell a trustable, patchable, auditable system. |
| Audience understanding | The talk is about accountability around the model, not model performance alone. |
| Screen copy | `你賣的不是模型`<br>`Trust` `Patch` `Evidence` |
| Visual form | Dominant phrase with a model cube expanding into clinical-system outline. |
| Build behavior | Phrase first; then the three anchors. |
| Speaker note | `你賣的是一個在醫療情境中可被信任、可被修補、可被稽核的系統。` |
| Do not show | SaMD taxonomy, model-accuracy metrics, architecture detail. |
| Transition out | `如果這是真的，我們就要問：為什麼 2026 年這件事更急？` |
| Rubric support | Structure and Narrative Design, Delivery Quality, Audience Impact. |

### Slide 4. AI 變成基礎設施，資安變成照護連續性

| Field | Spec |
| --- | --- |
| Objective | Connect AI infrastructure growth to healthcare continuity risk. |
| One-sentence message | When AI becomes infrastructure, cyber incidents can become care disruption. |
| Audience understanding | Medical AI security scope grows with deployment scope. |
| Screen copy | `AI is becoming infrastructure`<br>`Model -> Runtime -> Infrastructure`<br>`Cyber incidents become care disruption` |
| Visual form | Left: three-layer AI stack. Right: clinical continuity line with one interruption. |
| Build behavior | Reveal stack, then continuity break. |
| Speaker note | `醫療資安也已經不只是 IT 後台問題；當 AI 進入醫療，cyber incident 很快就會變成 care disruption。` |
| Do not show | News screenshots, vendor logos, fear-heavy patient imagery. |
| Transition out | `所以我們需要一張產品尺度地圖，先決定風險到底長在哪裡。` |
| Rubric support | Content Depth and Value, Audience Impact, Stage Rhythm and Time Control. |

### Slide 5. 四種產品尺度：風險會跟架構一起長大

| Field | Spec |
| --- | --- |
| Objective | Install the talk's navigation map. |
| One-sentence message | Product architecture determines attack surface and evidence burden. |
| Audience understanding | The same AI model creates different cybersecurity obligations depending on product scale. |
| Screen copy | `Risk grows with architecture`<br>`Model`<br>`Viewer`<br>`Platform / Database`<br>`Connected Medical System`<br>`Evidence grows` |
| Visual form | Four-step ladder with an evidence-growth line. |
| Build behavior | Reveal layers bottom to top. |
| Speaker note | `每加一層，產品能力變強，攻擊面也變大，證據需求也變大。` |
| Do not show | Threat list under each layer; this slide is a map, not a catalog. |
| Transition out | `有了這張地圖，我們再看法規到底在要求什麼。` |
| Rubric support | Structure and Narrative Design, Visual Design, Audience Impact. |

### Slide 6. 法規要的是一條證據鏈

| Field | Spec |
| --- | --- |
| Objective | Translate FDA 524B and FDA 2025 into one operational evidence model. |
| One-sentence message | Regulation asks for traceable evidence, not slogans. |
| Audience understanding | Monitor, patch, disclose, SBOM, architecture, threat model, controls, tests, and finding disposition must connect. |
| Screen copy | `Evidence, not slogans`<br>`Risk -> Control -> Test -> Fix -> Evidence`<br>`Monitor | Patch | Disclose | SBOM` |
| Visual form | Horizontal evidence chain with four FDA 524B verbs as side rail. |
| Build behavior | Evidence chain first, then four verbs. |
| Speaker note | `法規要的是證據，不是口號。這條線接不起來，文件再多也只是資料夾。` |
| Do not show | Long legal quotes, section-number clutter, full guidance screenshots. |
| Transition out | `回到台灣和公司內部治理，這條證據鏈還需要兩種語言：模型語言和管理語言。` |
| Rubric support | Content Depth and Value, Delivery Quality, Stage Rhythm and Time Control. |

### Slide 7. 台灣團隊需要同時說清楚模型、治理與 AI stack

| Field | Spec |
| --- | --- |
| Objective | Bridge TFDA-facing AI/ML SaMD evidence, NIST-style governance, and AI-stack security. |
| One-sentence message | A credible team can explain the model, govern risk, and secure the stack. |
| Audience understanding | Model evidence alone is not enough; governance and stack boundaries must be clear. |
| Screen copy | `Model evidence`<br>`Governance language`<br>`Model / Runtime / Infrastructure`<br>`Intended use | Data | V&V | Clinical performance`<br>`Govern | Identify | Protect | Respond | Recover`<br>`Provenance | Isolation | Identity | Updates` |
| Visual form | Three-column bridge. |
| Build behavior | Reveal one column at a time. |
| Speaker note | `這三件事接起來，才是醫療 AI team 真正能拿去討論、治理、送審、跟客戶溝通的 security language。` |
| Do not show | Full control catalog, submission-form detail, cloud architecture export. |
| Transition out | `接下來回到剛才的四層產品尺度，看每一層到底多了什麼風險。` |
| Rubric support | Content Depth and Value, Audience Impact, Visual Design. |

### Slide 8. Scale 1-2：Model 到 Viewer

| Field | Spec |
| --- | --- |
| Objective | Show how responsibility starts with model evidence and grows when a viewer is added. |
| One-sentence message | A wrapper turns a model artifact into an attackable user-facing system. |
| Audience understanding | Scale 1 needs artifact/data/dependency/update evidence; Scale 2 adds parser, upload, cache, and output risk. |
| Screen copy | `Scale 1: Model`<br>`Artifact | Data lineage | Dependency / SBOM | Update boundary`<br>`Scale 2: Viewer`<br>`Parser | Upload | Cache | Output limits` |
| Visual form | Two-panel comparison with same label structure. |
| Build behavior | Model panel first; Viewer panel second; risk labels last. |
| Speaker note | `Model 到 viewer 的差別，是產品從一個 artifact 變成一個使用情境。` |
| Do not show | Real UI screenshots, private file formats, exploit steps. |
| Transition out | `如果再往上長成平台，資安就不只是產品問題，而是公司營運和臨床連續性問題。` |
| Rubric support | Content Depth and Value, Stage Rhythm and Time Control. |

### Slide 9. Scale 3-4：Platform 到 Connected Medical System

| Field | Spec |
| --- | --- |
| Objective | Show when security becomes operating risk and clinical continuity risk. |
| One-sentence message | Platform and hospital integration make cybersecurity a business and patient-safety issue. |
| Audience understanding | Scale 3 introduces identity/API/database/log/backup; Scale 4 introduces hospital network and service continuity. |
| Screen copy | `Scale 3: Platform`<br>`Identity | RBAC | API | Database | Audit log | Backup`<br>`Scale 4: Connected Medical System`<br>`PACS/HIS | Hospital network | Update server | Remote service` |
| Visual form | Two-panel system map: product platform -> connected clinical environment. |
| Build behavior | Platform panel first; connected-system panel second. |
| Speaker note | `這時候 cyber risk 不只是產品保護，而是 clinical continuity risk。` |
| Do not show | Specific hospital topology, customer architecture, internal network detail. |
| Transition out | `所以醫療 AI 的資安，最後不是一句 IT 口號，而是一句病人安全的話。` |
| Rubric support | Content Depth and Value, Audience Impact. |

### Slide 10. Cyber Safety Is Patient Safety

| Field | Spec |
| --- | --- |
| Objective | Deliver the ethical and emotional peak. |
| One-sentence message | Medical-device cybersecurity is part of patient safety. |
| Audience understanding | Security failures can affect patients, hospital operations, supplier responsibility, and clinical workflow. |
| Screen copy | `Cyber Safety Is Patient Safety`<br>Optional footer: `Vendor responsibility | Hospital continuity | Clinical workflow` |
| Visual form | Full-screen phrase with strong negative space. |
| Build behavior | None. |
| Speaker note | `Cyber Safety is Patient Safety.` Pause. |
| Do not show | Framework, checklist, stock hospital drama, extra claims. |
| Transition out | `接下來進入最實作的部分：怎麼測，怎麼修，怎麼留下證據。` |
| Rubric support | Audience Impact, Stage Presence, Delivery Quality. |

### Slide 11. Testing Strategy：White-box + Black-box

| Field | Spec |
| --- | --- |
| Objective | Show complementary testing roles without a tool catalog. |
| One-sentence message | White-box finds repairable problems early; black-box validates external exposure. |
| Audience understanding | Both testing modes must produce findings and retest evidence. |
| Screen copy | `White-box: find repairable problems before release`<br>`Black-box: validate external exposure`<br>`Output: finding list + retest evidence` |
| Visual form | Inside-out vs outside-in contrast. |
| Build behavior | White-box side, black-box side, output strip. |
| Speaker note | `Testing 的價值，是讓風險變成可以修、可以驗證、可以追蹤的 finding。` |
| Do not show | Tool logos, vulnerability screenshots, exploit recipes. |
| Transition out | `但 finding 出來以後，真正的治理才開始。` |
| Rubric support | Content Depth and Value, Delivery Quality, Stage Rhythm and Time Control. |

### Slide 12. Patch SLA：Every Finding Needs A Decision

| Field | Spec |
| --- | --- |
| Objective | Deliver the operational climax. |
| One-sentence message | Every security finding needs ownership, a decision, repair path, retest, and archived evidence. |
| Audience understanding | Patch SLA is governance, not ticket hygiene. |
| Screen copy | `Patch SLA`<br>`Every finding needs a decision`<br>`Intake -> Triage -> Decision -> Patch -> Retest -> Archive`<br>`Fix now | Compensate | Defer | Not applicable` |
| Visual form | Finding journey with `Decision` visually dominant. |
| Build behavior | Flow first; decision outcomes second. |
| Speaker note | `沒有 decision，就沒有治理；沒有證據，就沒有信任。` |
| Do not show | Ticket-system screenshot, long SLA table, customer-specific examples. |
| Transition out | `我知道很多小團隊會覺得這很大，所以最後把它壓成 30、60、90 天。` |
| Rubric support | Content Depth and Value, Structure and Narrative Design, Audience Impact. |

### Slide 13. Small Team 30 / 60 / 90

| Field | Spec |
| --- | --- |
| Objective | Give small teams a credible first implementation path. |
| One-sentence message | Start with minimum evidence, then repeatable workflow, then external validation. |
| Audience understanding | A small team can start without pretending to have a large enterprise program. |
| Screen copy | `30: Inventory / SBOM / data flow`<br>`60: Threat model / CI gates / finding workflow`<br>`90: Pen test / Patch SLA / retest evidence` |
| Visual form | Three-step timeline, equal visual weight. |
| Build behavior | 30, then 60, then 90. |
| Speaker note | `重點不是三個月變完美，而是三個月後，公司開始自動留下可信證據。` |
| Do not show | More than three deliverables per bucket, large enterprise framework. |
| Transition out | `最後，我們回到今天的第一個問題：怎麼在稽核之前先建立信任。` |
| Rubric support | Audience Impact, Stage Rhythm and Time Control. |

### Slide 14. 先建立信任，再面對稽核

| Field | Spec |
| --- | --- |
| Objective | Close with a single durable principle. |
| One-sentence message | Build security into the product so regulatory documents become evidence, not theater. |
| Audience understanding | Mature teams prove, repair, and track risk before audit pressure. |
| Screen copy | `先把安全做進產品，法規文件才會自然長出來。`<br>Optional footer: `Build trust before the audit` |
| Visual form | Large phrase with quiet space. |
| Build behavior | None. |
| Speaker note | `真正成熟的團隊，不是文件最多的團隊，而是每一個風險都知道怎麼證明、怎麼修、怎麼追的團隊。謝謝大家。` |
| Do not show | New framework, contact-heavy content, extra roadmap. |
| Transition out | Stop. |
| Rubric support | Audience Impact, Stage Presence, Delivery Quality. |

## 5. Visual QA Before Export

- [ ] Slides 3, 5, 10, 12, and 14 are visually distinctive.
- [ ] Slide 6 uses an evidence chain, not a legal text block.
- [ ] Slide 7 has three balanced columns and does not become a control catalog.
- [ ] Slides 8-9 use matching comparison structure so product-scale growth is obvious.
- [ ] Slide 12 makes `Decision` the dominant node.
- [ ] No slide contains private architecture, proprietary code, exploit detail, private hospital/client detail, student data, or patent-sensitive implementation mechanics.
- [ ] Every slide can be understood at headline level within three seconds.

## 6. Emergency Cut Path

For a `20:00` delivery:

| Keep | Time | Compression |
| --- | ---: | --- |
| Slides 1-2 | `0:30` | Title and disclaimer only. |
| Slide 3 | `2:00` | Thesis line plus trust/patch/evidence. |
| Slide 5 | `2:00` | Four-scale map; mention AI infrastructure briefly. |
| Slide 6 | `4:00` | Evidence chain plus FDA 524B verbs. |
| Slide 7 | `2:30` | One sentence per column. |
| Slides 8-9 | `3:30` | One example per scale pair. |
| Slide 10 | `1:00` | Patient-safety line and pause. |
| Slide 12 | `2:00` | Patch SLA and decision outcomes; mention testing output here. |
| Slide 13 | `1:30` | One output per bucket. |
| Slide 14 | `0:30` | Closing principle only. |

Skip slides 4 and 11 as standalone sections in the emergency path.
