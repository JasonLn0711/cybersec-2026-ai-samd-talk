# 03 Speaker Script And Stage Rhythm

Purpose: provide the speakable Taiwan Traditional Chinese path for the compact `14`-slide deck, including rhythm, pauses, authority lines, and cut markers.

## 1. Delivery Contract

| Requirement | Stage Behavior | Rubric Protected |
| --- | --- | --- |
| Preserve memory anchors | Slow down on slides 3, 5, 10, 12, and 14. | Audience Impact, Stage Presence |
| Sound like a conference briefing | Use decision language: `風險在哪裡`, `證據怎麼接`, `finding 最後去哪裡`. | Delivery Quality |
| Keep technical credibility | Explain artifacts, ownership, testing output, and repair evidence. | Content Depth and Value |
| Protect the clock | Use cut markers rather than speaking faster. | Stage Rhythm and Time Control |
| End with control | No new idea after slide 14's closing sentence. | Structure and Narrative Design |

## 2. Energy And Timing Map

| Slide | Timebox | Energy | Voice And Body |
| ---: | --- | --- | --- |
| 1 | `0:00-0:10` | Calm | Centered stance; no biography expansion. |
| 2 | `0:10-0:30` | Neutral | Compliance pause; move on. |
| 3 | `0:30-2:20` | Controlled authority | Slow on `你賣的不是模型`; direct eye contact. |
| 4 | `2:20-4:30` | Alert | Moderate pace; make urgency concrete. |
| 5 | `4:30-6:30` | Slow and clear | Gesture vertically through four scales. |
| 6 | `6:30-10:40` | Authoritative | Slightly slower; use evidence-chain hand movement. |
| 7 | `10:40-14:00` | Practical | Three-column rhythm; no deep detours. |
| 8 | `14:00-16:40` | Efficient | Contrast left/right panels. |
| 9 | `16:40-19:20` | Decisive | Raise consequence level without fear tone. |
| 10 | `19:20-20:40` | Still and slow | Pause after English line. |
| 11 | `20:40-23:00` | Crisp | Faster contrast; output-focused. |
| 12 | `23:00-25:10` | Strong | Slow on `decision`; pause after final line. |
| 13 | `25:10-27:40` | Constructive | Roadmap cadence: 30, 60, 90. |
| 14 | `27:40-28:30` | Final | Still posture; finish and stop. |

## 3. Full Compact Stage Script

### Slide 1. Title

各位好，我是林家聖。今天的題目是 AI 軟體醫材的資安實戰。

`關鍵字很多，但今天我只想留下三件事：信任、修補、證據。`

Cut marker: do not add biography.

### Slide 2. Required CYBERSEC Disclaimer

這是大會必要的 disclaimer，我在這裡停一下，讓大家看見。

接下來我們直接進入今天真正的問題。

Cut marker: if tight, say only the first sentence.

### Slide 3. 你賣的不是模型

很多 AI 團隊一開始會說：我們只是提供模型。可是醫療現場不會這樣看。

醫師看到的是結果，病人承受的是後果，公司要負責的是整個使用情境。

所以第一個轉念是：

`你賣的不是模型。`

Pause.

你賣的是一個在醫療情境中可被信任、可被修補、可被稽核的系統。

今天所有的 FDA 524B、Threat Modeling、Patch SLA，其實都是從這個轉念開始：產品不是只有準，而是要能被信任；不是只有上線，而是要能被修補；不是只有宣稱安全，而是要拿得出證據。

Cut marker: start at `所以第一個轉念是` if late.

### Slide 4. AI 變成基礎設施，資安變成照護連續性

2026 年 AI 的語言正在從模型變成基礎設施。

大家不只談模型多大、跑分多高，而是談模型怎麼部署、怎麼更新、怎麼被隔離、怎麼被監控、怎麼接到真實 workflow。

對醫療 AI 來說，這件事更直接。它會接 runtime、資料、使用者、更新鏈，最後接到臨床流程。

所以醫療資安不只是 IT 後台問題。當 AI 進入醫療，cyber incident 很快就會變成 care disruption。

Cut marker: keep only three sentences: AI is infrastructure; medical AI connects to workflow; incident becomes disruption.

### Slide 5. 四種產品尺度

請大家先記四層。

第一層，只有 model。第二層，model 加 viewer。第三層，有 platform 和 database。第四層，進入 connected medical system。

Pause after the four layers.

每加一層，產品能力變強，攻擊面也變大，證據需求也變大。

這張圖很重要，因為等一下我們講法規、testing、Patch SLA，都不是抽象清單，而是要回來問：你的產品到底在哪一層？這一層多了什麼風險？你有沒有相稱的證據？

Cut marker: never cut the four layers.

### Slide 6. 法規要的是一條證據鏈

我用一句話講法規：

`法規要的是證據，不是口號。`

Pause.

FDA 524B 如果用商業語言講，就是：如果你的醫材會連線，上市前就要準備好上市後怎麼 monitor、怎麼 patch、怎麼 disclose，以及用 SBOM 說清楚軟體組成。

這件事的重點不是多交一份文件，而是公司在產品設計階段，就要知道上市後漏洞怎麼被看見、誰判斷、誰修補、怎麼通知、怎麼留下紀錄。

FDA 2025 guidance 再往下問的是 traceability。你的 architecture 在哪裡？Threat model 怎麼畫？Controls 對應到哪些風險？Testing 有沒有真的打到攻擊面？每個 finding 最後去哪裡了？

所以我會把它壓成一條線：

`risk、control、test、fix、evidence。`

這條線接不起來，文件再多也只是資料夾；這條線接得起來，法規文件才像是工程工作自然留下來的證據。

Cut marker: keep FDA 524B four verbs and the evidence chain; remove the artifact questions if late.

### Slide 7. 台灣團隊需要同時說清楚模型、治理與 AI stack

在台灣，AI/ML SaMD 不是黑盒子傳奇。團隊要說清楚 intended use：誰用、在哪裡用、不能怎麼用。

也要說清楚 data 怎麼來，algorithm 怎麼設計，V&V 怎麼做，clinical performance 怎麼證明。

但模型語言還不夠。公司內部還需要管理語言。NIST 的價值，是讓董事會、PM、RD、法規、客服可以講同一種風險語言：誰 govern，誰 identify，誰 protect，出事時誰 respond、誰 recover。

最後，AI security 不能只挑 model 做。Model 要看 provenance 和 evaluation；runtime 要看 isolation 和 secrets；infrastructure 要看 identity 和 updates。

這三件事接起來，才是醫療 AI team 真正能拿去討論、治理、送審、跟客戶溝通的 security language。

Cut marker: one sentence per column if late.

### Slide 8. Scale 1-2：Model 到 Viewer

第一層，如果你真的只有 AI model，範圍最小，但不是沒有資安責任。

至少要說清楚 model artifact 從哪裡來、data lineage 怎麼追、dependency 和 SBOM 有沒有整理、update boundary 在哪裡。

第二層，一旦加上 viewer，世界就變了。攻擊者不一定攻擊模型，他可以攻擊 file parser、upload、cache、output 呈現，甚至攻擊使用者怎麼理解輸出。

所以 model 到 viewer 的差別，是產品從一個 artifact 變成一個使用情境。Security evidence 也要從模型來源，長到檔案、介面、暫存和輸出的安全邊界。

Cut marker: keep `model evidence` and `viewer attack surface`; remove cache and interpretation detail.

### Slide 9. Scale 3-4：Platform 到 Connected Medical System

第三層，viewer 加上 platform 和 database，資安就變成公司風險。

你開始有 identity、RBAC、API、database、audit log、backup。這些不是只有 RD 的問題，也是營運、法規、客服和品牌信任的問題。

第四層，當產品進入 connected medical system，事情再升級一次。

它可能接 PACS、HIS、hospital network、update server、remote service。這時候 cyber risk 不只是產品保護，而是 clinical continuity risk。

如果這一層出事，影響的不只是某一次 model output，而可能是多個臨床流程、醫院端營運、供應商責任和病人照護連續性。

Cut marker: keep identity/API/database and hospital network/update server.

### Slide 10. Cyber Safety Is Patient Safety

`Cyber Safety is Patient Safety.`

Pause.

醫療 AI 出事時，受影響的不只是模型績效，而是病人、醫院營運、供應商責任與臨床流程。

這也是為什麼我不建議把資安放到產品最後才補。越晚才補，越像文件；越早放進產品，越像真正的安全設計。

Cut marker: never cut the line or the pause.

### Slide 11. Testing Strategy

Testing 不是工具名稱競賽。Testing 的價值，是讓風險變成可以修、可以驗證、可以追蹤的 finding。

White-box testing 是在 release 前，從內部找便宜、可修、可追溯的問題。看 code、config、dependency、container、cloud setting，也看 AI pipeline 有沒有資料洩漏或更新邊界不清。

Black-box testing 問的是另一個問題：如果我不知道你的原始碼，只從外部看，我能不能打得進來？能不能繞過登入？能不能把幾個小問題串成攻擊路徑？

所以 white-box 是早期修問題，black-box 是 release 或送審前驗證真實暴露。兩個不是互相取代，而是前後接力。最後都要回到 finding list 和 retest evidence。

Cut marker: say only white-box early repair, black-box external exposure, both create findings and retest evidence.

### Slide 12. Patch SLA

如果只能帶走一個營運流程，我會選 Patch SLA。

Pause.

真正的資安不是「沒有漏洞」，而是每個漏洞進來後，公司知道誰負責、多久判斷、多久修補、怎麼通知、怎麼重測、證據放哪裡。

這裡最重要的字是 decision。

Finding 進來之後，不是只有修或不修。可能是 fix now，可能是 compensate，可能是 defer with timeline，也可能是 non-applicable with rationale。

`沒有 decision，就沒有治理；沒有證據，就沒有信任。`

Pause.

Cut marker: never cut the final line.

### Slide 13. Small Team 30 / 60 / 90

小團隊不需要第一天就蓋大型制度。

30 天，先盤點：assets、SBOM、data flow、intended use、known vulnerabilities。

60 天，建立節奏：threat model、CI security gates、finding workflow、customer security note。

90 天，做外部驗證：penetration test、Patch SLA、CVD process、retest evidence、release history。

重點不是三個月變完美，而是三個月後，公司開始自動留下可信證據。

這就是小團隊比較實際的路徑：先讓風險看得見，再讓 evidence 可以重複產生，最後讓 findings 可以被治理。

Cut marker: one output per bucket: 30 inventory, 60 workflow, 90 validation.

### Slide 14. 先建立信任，再面對稽核

今天我們從一個 model 開始，走到 connected medical system。

每往前一步，產品更有價值，也更需要被信任、被修補、被稽核。

所以我想用一句話結束：

`先把安全做進產品，法規文件才會自然長出來。`

Pause.

真正成熟的團隊，不是文件最多的團隊，而是每一個風險都知道怎麼證明、怎麼修、怎麼追的團隊。

謝謝大家。

Cut marker: if late, say only the closing sentence and `謝謝大家`.

## 4. Pocket Cue Card

```text
0:00  Title. Calm.
0:10  Disclaimer. Pause, move.
0:30  Not model. Trust / patch / evidence.
2:20  AI infrastructure -> care disruption.
4:30  Four scales. Risk grows, evidence grows.
6:30  FDA evidence chain. Monitor / patch / disclose / SBOM.
10:40 Taiwan model evidence + NIST governance + AI stack.
14:00 Scale 1-2: model evidence -> viewer attack surface.
16:40 Scale 3-4: platform risk -> clinical continuity.
19:20 Cyber Safety is Patient Safety. Pause.
20:40 White-box + black-box -> findings + retest evidence.
23:00 Patch SLA. Every finding needs a decision.
25:10 30 inventory / 60 workflow / 90 validation.
27:40 Trust before audit. Stop.
```

## 5. Rhythm Controls

| Situation | Stage Signal | Correction |
| --- | --- | --- |
| Opening feels slow | Slide 3 begins after `0:45` | Remove setup and start with `你賣的不是模型`. |
| Regulatory section feels dense | Audience stops looking up during slide 6 | Use the evidence chain only; stop naming extra artifacts. |
| Middle feels repetitive | Slides 8-9 sound like lists | Ask: `這一層多了什麼風險？` before each scale pair. |
| Energy drops after slide 9 | Room becomes quiet before patient-safety line | Slow down, step into slide 10, and use silence. |
| Testing runs long | Slide 12 starts after `23:30` | Cut tool examples immediately. |
| Ending is at risk | Slide 14 starts after `28:00` | Use only the closing principle and `謝謝大家`. |

## 6. Lines That Must Land

| Line | Delivery |
| --- | --- |
| `你賣的不是模型` | Say slowly, then pause. |
| `法規要的是證據，不是口號` | Say as a judgment, not a slogan. |
| `Cyber Safety is Patient Safety` | Say in English, pause, then explain in Chinese. |
| `沒有 decision，就沒有治理；沒有證據，就沒有信任` | Slow down on `decision`, `證據`, `信任`. |
| `先把安全做進產品，法規文件才會自然長出來` | Final principle; do not add a new point after it. |

