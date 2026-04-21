# 01 Talk Design

Purpose: define the public CYBERSEC 2026 talk as one compact, speakable, evidence-driven conference package.

This file combines the former strategy brief, `14`-slide deck spec, and stage-script docs. Use it when deciding what the talk says, shows, and sounds like.

## First-Principles Model

| Question | Decision |
| --- | --- |
| What is the artifact? | A public `30:00` CYBERSEC conference talk, not a research notebook or slide archive. |
| Who must it serve? | Healthcare-security, medical-device, regulatory, QA, product, and security-engineering listeners. |
| What must they leave with? | A product-scale map, evidence-chain logic, testing strategy, Patch SLA model, and small-team roadmap. |
| What is the core thesis? | AI SaMD teams do not sell a model; they sell a trustable, patchable, auditable clinical product system. |
| What is the active deck? | `14` slides, `28:30` spoken content, `1:30` buffer. |
| What is the language policy? | Taiwan Traditional Chinese stage language with English technical terms where they carry shared meaning. |
| What must stay out? | Private hospital/client details, proprietary code, student records, exploit recipes, and patent-sensitive implementation mechanics. |

Operating sequence:

```text
product scale -> evidence chain -> AI stack governance -> testing -> Patch SLA -> 30 / 60 / 90 action
```

## Delivery Promise

The audience should remember one operating model:

`AI SaMD security is not a model-security checklist. It is a product trust system: scope the product, trace the evidence, test the exposure, govern findings, and prove repairability.`

Memory anchors:

- `你賣的不是模型`
- `法規要的是證據，不是口號`
- `Cyber Safety is Patient Safety`
- `沒有 decision，就沒有治理；沒有證據，就沒有信任`
- `先把安全做進產品，法規文件才會自然長出來`

## Audience And Design Response

| Audience | What They Need | Design Response |
| --- | --- | --- |
| Product leads / founders | Know what security work fits their product scale. | Four-scale product map and `30 / 60 / 90` roadmap. |
| Security engineers / consultants | Connect findings to medical-device evidence and repair obligations. | Testing output, finding disposition, retest evidence, Patch SLA. |
| Regulatory / QA teams | Trace architecture, risk, control, test, fix, and evidence. | Evidence-chain slide and submission-oriented language. |
| Healthcare IT leaders | Understand continuity and vendor-risk implications. | `Cyber Safety is Patient Safety` as the ethical peak. |
| Cross-functional managers | Shared ownership language without heroics. | Governance language, decision records, small-team path. |

Common misconceptions to break:

- `AI security = model robustness only`
- `Regulation = documents for submission`
- `Testing = tool list`
- `Small teams cannot start`
- `Cybersecurity is IT, not patient safety`

## Timing Architecture

| Slide | Time | Cumulative | Job |
| ---: | ---: | ---: | --- |
| 1 | `0:10` | `0:10` | Formal opening. |
| 2 | `0:20` | `0:30` | Required disclaimer. |
| 3 | `1:50` | `2:20` | Land thesis. |
| 4 | `2:10` | `4:30` | Make urgency relevant. |
| 5 | `2:00` | `6:30` | Install the four-scale map. |
| 6 | `4:10` | `10:40` | Translate regulation into evidence. |
| 7 | `3:20` | `14:00` | Bridge model evidence, governance, and AI stack. |
| 8 | `2:40` | `16:40` | Explain Scale 1-2. |
| 9 | `2:40` | `19:20` | Explain Scale 3-4. |
| 10 | `1:20` | `20:40` | Patient-safety peak. |
| 11 | `2:20` | `23:00` | Testing strategy. |
| 12 | `2:10` | `25:10` | Patch SLA climax. |
| 13 | `2:30` | `27:40` | Small-team roadmap. |
| 14 | `0:50` | `28:30` | Clean close. |

Timing rule: if slide 7 ends after `14:30`, compress slides 8-9 to one example per side and protect slides 10, 12, 13, and 14.

## Build Path

The structured source is:

`data/presentation_os.json`

Regenerate reports first:

```bash
python3 tools/generate_presentation_outputs.py
```

Build the editable deck when the active Node environment can resolve `@oai/artifact-tool`:

```bash
node tools/build_optimized_deck.mjs
```

Active deck artifact:

`outputs/deck/cybersec-2026-ai-samd-compact-optimized.pptx`

Build rules:

- Exactly `14` slides.
- Exactly `1710` seconds / `28:30` content time.
- Slide 2 may be the official CYBERSEC disclaimer image.
- All other visible talk text should remain editable PowerPoint text/shapes.
- Use generated reports for consistency checks; do not hand-edit generated outputs as independent sources.

## Slide And Script Spine

| Slide | On-Screen Job | Visual Form | Must-Say Line | Cut Rule |
| ---: | --- | --- | --- | --- |
| 1 | `AI 軟體醫材的資安實戰` | Restrained title with product-system outline. | `關鍵字很多，但今天我只想留下三件事：信任、修補、證據。` | Do not add biography. |
| 2 | Required disclaimer | Full-slide organizer disclaimer. | `這是大會必要的 disclaimer，我在這裡停一下，讓大家看見。` | If tight, say only this sentence. |
| 3 | `你賣的不是模型` | Dominant phrase plus `Trust / Patch / Evidence`. | `你賣的是一個在醫療情境中可被信任、可被修補、可被稽核的系統。` | Start at `所以第一個轉念是` if late. |
| 4 | AI infrastructure becomes clinical-continuity risk | AI stack plus continuity break. | `當 AI 進入醫療，cyber incident 可能直接干擾 clinical care。` | Keep only AI infrastructure, workflow, disruption. |
| 5 | Four product scales | Ladder with evidence-growth line. | `每加一層，產品能力變強，攻擊面也變大，證據需求也變大。` | Never cut the four layers. |
| 6 | Evidence chain | `Risk -> Control -> Test -> Fix -> Evidence` plus FDA 524B verbs. | `法規要的是證據，不是口號。` | Keep FDA 524B verbs and evidence chain. |
| 7 | Model / governance / AI stack | Three-column bridge. | `NIST 在這裡是共同語言，不是我要大家背控制項。` | One sentence per column if late. |
| 8 | Scale 1-2: Model to Viewer | Two-panel comparison. | `Model 到 viewer 的差別，是產品從一個 artifact 變成一個使用情境。` | Keep model evidence and viewer attack surface. |
| 9 | Scale 3-4: Platform to Connected System | Platform vs clinical environment map. | `這時候 cyber risk 不只是產品保護，而是 clinical continuity risk。` | Keep identity/API/database and hospital network/update server. |
| 10 | `Cyber Safety Is Patient Safety` | Full-screen phrase with negative space. | `Cyber Safety is Patient Safety.` | Never cut the line or pause. |
| 11 | White-box + black-box testing | Inside-out vs outside-in contrast. | `Testing 的價值，是讓風險變成可以修、可以驗證、可以追蹤的 finding。` | Say only early repair, external exposure, findings, retest evidence. |
| 12 | Patch SLA | Finding journey with dominant `Decision` node. | `沒有 decision，就沒有治理；沒有證據，就沒有信任。` | Never cut the final line. |
| 13 | Small Team `30 / 60 / 90` | Three-step roadmap. | `重點不是三個月變完美，而是三個月後，公司開始自動留下可信證據。` | One output per bucket. |
| 14 | Trust before audit | Quiet closing principle. | `先把安全做進產品，法規文件才會自然長出來。` | If late, say only this and `謝謝大家`. |

## Full Stage Script

### Slide 1. Title

各位好，我是林家聖。今天的題目是 AI 軟體醫材的資安實戰。

`關鍵字很多，但今天我只想留下三件事：信任、修補、證據。`

### Slide 2. Required CYBERSEC Disclaimer

這是大會必要的 disclaimer，我在這裡停一下，讓大家看見。

接下來我們直接進入今天真正的問題。

### Slide 3. 你賣的不是模型

很多 AI 團隊一開始會說：我們只是提供模型。可是醫療現場不會這樣看。

醫師看到的是結果，病人承受的是後果，公司要負責的是整個使用情境。

所以第一個轉念是：

`你賣的不是模型。`

Pause.

你賣的是一個在醫療情境中可被信任、可被修補、可被稽核的系統。

今天所有的 FDA 524B、Threat Modeling、Patch SLA，其實都是從這個轉念開始：產品不是只有準，而是要能被信任；不是只有上線，而是要能被修補；不是只有宣稱安全，而是要拿得出證據。

### Slide 4. AI 變成基礎設施，資安變成照護連續性

2026 年 AI 的語言正在從模型變成基礎設施。

大家不只談模型多大、跑分多高，而是談模型怎麼部署、怎麼更新、怎麼被隔離、怎麼被監控、怎麼接到真實 workflow。

對醫療 AI 來說，這件事更直接。它會接 runtime、資料、使用者、更新鏈，最後接到臨床流程。

所以醫療資安不只是 IT 後台問題。當 AI 進入醫療，cyber incident 可能直接干擾 clinical care，最後變成照護連續性的問題。

### Slide 5. 四種產品尺度

請大家先記四層。

第一層，只有 model。第二層，model 加 viewer。第三層，有 platform 和 database。第四層，進入 connected medical system。

Pause after the four layers.

每加一層，產品能力變強，攻擊面也變大，證據需求也變大。

這張圖很重要，因為等一下我們講法規、testing、Patch SLA，都不是抽象清單，而是要回來問：你的產品到底在哪一層？這一層多了什麼風險？你有沒有相稱的證據？

### Slide 6. 法規要的是一條證據鏈

我用一句話講法規：

`法規要的是證據，不是口號。`

Pause.

FDA 524B 如果用商業語言講，就是：如果你的醫材會連線，上市前就要準備好上市後怎麼 monitor、identify、address cybersecurity issues，怎麼做 coordinated vulnerability disclosure，怎麼提供 updates and patches，以及用 SBOM 說清楚軟體組成。

這件事的重點不是多交一份文件，而是公司在產品設計階段，就要知道上市後漏洞怎麼被看見、誰判斷、誰修補、怎麼通知、怎麼留下紀錄。

FDA 2025 guidance 再往下問的是 traceability。你的 architecture 在哪裡？Threat model 怎麼畫？Controls 對應到哪些風險？Testing 有沒有真的打到攻擊面？每個 finding 最後去哪裡了？

所以我會把它壓成一條線：

`risk、control、test、fix、evidence。`

這條線接不起來，文件再多也只是資料夾；這條線接得起來，法規文件才像是工程工作自然留下來的證據。

### Slide 7. 台灣團隊需要同時說清楚模型、治理與 AI stack

在台灣，AI/ML SaMD 不是黑盒子傳奇。團隊要說清楚 intended use：誰用、在哪裡用、不能怎麼用。

也要說清楚 data 怎麼來，algorithm 怎麼設計，V&V 怎麼做，clinical performance 怎麼證明。

但模型語言還不夠。公司內部還需要管理語言。這裡我建議把 NIST 當成共同語言，而不是控制清單。

如果講 AI 風險，用 AI RMF：Govern、Map、Measure、Manage。意思是先治理，再界定情境，再量測風險，最後管理風險。如果講資安營運，可以再借 CSF 的語言：Govern、Identify、Protect、Detect、Respond、Recover。

今天我只取共同精神：不同角色要用同一套語言討論風險、責任和證據，而不是每個部門各講各的。

最後，AI security 不能只挑 model 做。Model 要看 provenance 和 evaluation；runtime 要看 isolation 和 secrets；infrastructure 要看 identity、updates 和 access boundary。

這三件事接起來，才是醫療 AI team 真正能拿去討論、治理、送審、跟客戶溝通的 security language。

### Slide 8. Scale 1-2：Model 到 Viewer

第一層，如果你真的只有 AI model，範圍最小，但不是沒有資安責任。

至少要說清楚 model artifact 從哪裡來、data lineage 怎麼追、dependency 和 SBOM 有沒有整理、update boundary 在哪裡。

第二層，一旦加上 viewer，世界就變了。攻擊者不一定攻擊模型，他可以攻擊 file parser、upload、cache、output 呈現，甚至攻擊使用者怎麼理解輸出。

所以 model 到 viewer 的差別，是產品從一個 artifact 變成一個使用情境。Security evidence 也要從模型來源，長到檔案、介面、暫存和輸出的安全邊界。

### Slide 9. Scale 3-4：Platform 到 Connected Medical System

第三層，viewer 加上 platform 和 database，資安就變成公司風險。

你開始有 identity、API、database、audit log、backup。這些不是只有 RD 的問題，也是營運、法規、客服和品牌信任的問題。

第四層，當產品進入 connected medical system，事情再升級一次。

它可能接 PACS、HIS、hospital network、update server、remote service。這時候 cyber risk 不只是產品保護，而是 clinical continuity risk。

如果這一層出事，影響的不只是某一次 model output，而可能是多個臨床流程、醫院端營運、供應商責任和病人照護連續性。

### Slide 10. Cyber Safety Is Patient Safety

`Cyber Safety is Patient Safety.`

Pause.

醫療 AI 出事時，受影響的不只是模型績效，而是病人、醫院營運、供應商責任與臨床流程。

這也是為什麼我不建議把資安放到產品最後才補。越晚才補，越像文件；越早放進產品，越像真正的安全設計。

### Slide 11. Testing Strategy

Testing 不是工具名稱競賽。

White-box 的價值，是在 release 前找到便宜、可修、可追溯的問題。看 code、config、dependency、container、cloud setting，也看 AI pipeline 有沒有資料洩漏或更新邊界不清。

Black-box 的價值，是從外部驗證真實暴露：如果我不知道你的原始碼，只從外部看，我能不能打得進來？能不能繞過登入？能不能把幾個小問題串成攻擊路徑？

所以 white-box 是早期修問題，black-box 是 release 或送審前驗證真實暴露。兩個不是互相取代，而是前後接力。最後都要回到同一件事：finding list，加上 retest evidence。

### Slide 12. Patch SLA

如果只能帶走一個營運流程，我會選 Patch SLA。

Pause.

我這裡講的 Patch SLA 是一個 operating model，不是 FDA 原文裡的一個固定名詞。真正的資安不是「沒有漏洞」，而是每個漏洞進來後，公司知道誰負責、多久判斷、多久修補、怎麼通知、怎麼重測、證據放哪裡。

這裡最重要的字是 decision。

Finding 進來之後，不是只有修或不修。可能是 fix now，可能是 compensate，可能是 defer with timeline，也可能是 non-applicable with rationale。

`沒有 decision，就沒有治理；沒有證據，就沒有信任。`

Pause.

### Slide 13. Small Team 30 / 60 / 90

小團隊不需要第一天就蓋大型制度。

30、60、90 不是三個月變完美，而是三個月建立第一個 evidence loop。

30 天，先盤點：assets、SBOM、data flow、intended use、known vulnerabilities。

60 天，建立節奏：threat model、CI security gates、finding workflow、customer security note。

90 天，做外部驗證：penetration test、Patch SLA、CVD process、retest evidence、release history。

重點不是三個月變完美，而是三個月後，公司開始自動留下可信證據。

這就是小團隊比較實際的路徑：先讓風險看得見，再讓 evidence 可以重複產生，最後讓 findings 可以被治理。

### Slide 14. 先建立信任，再面對稽核

今天我們從一個 model 開始，走到 connected medical system。

每往前一步，產品更有價值，也更需要被信任、被修補、被稽核。

所以我想用一句話結束：

`先把安全做進產品，法規文件才會自然長出來。`

Pause.

真正成熟的團隊，不是文件最多的團隊，而是每一個風險都知道怎麼證明、怎麼修、怎麼追的團隊。

謝謝大家。

## Emergency Path

For a `20:00` delivery, keep slides 1, 2, 3, 5, 6, 7, 8-9, 10, 12, 13, and 14. Skip slides 4 and 11 as standalone sections; mention AI infrastructure on slide 5 and testing output on slide 12.

Do not cut:

1. The required disclaimer.
2. The four product scales.
3. `Cyber Safety is Patient Safety`.
4. `沒有 decision，就沒有治理；沒有證據，就沒有信任`.
5. The trust-before-audit closing principle.
