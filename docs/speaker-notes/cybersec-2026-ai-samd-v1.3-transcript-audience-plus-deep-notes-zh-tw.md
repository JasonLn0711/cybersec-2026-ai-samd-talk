# CYBERSEC 2026 AI SaMD v1.3 台灣華語排練閱讀版：逐字稿 + 觀眾分析 + 深度筆記

準備日期: 2026-04-21

Deck 基準: `outputs/deck/cybersec-2026-ai-samd-cybersecurity-in-practice-v1.3.pdf`

來源檔案:

- 觀眾分析: `docs/speaker-notes/cybersec-2026-ai-samd-v1.3-slide-audience-analysis-zh-tw.md`
- 逐字稿來源素材: `../planning-everything-track/data/projects/2026-04-medical-cybersecurity-tfda-fda-industry-deck/current/cybersec-2026-keynote-style-transcript-v0.9-20260422.md`
- 深度筆記來源: `docs/speaker-notes/cybersec-2026-ai-samd-slide-deep-notes-v2-en.md`；已轉寫成台灣華語並對齊目前 `v1.3` deck
- 搭配 Q&A: `docs/speaker-notes/cybersec-2026-ai-samd-audience-qa-v1-zh-tw.md`

## 閱讀方式

這是一份台灣華語排練閱讀版，將目前 `v1.3` 的上台講法、逐頁觀眾分析，以及英文深度筆記的內容整合在一起。英文深度筆記原本對應 generated compact `14`-slide fallback storyline；這一版已經把深度補充層重新對齊目前 `15` 頁的 `v1.3` deck。

每一頁建議照這個順序讀:

1. **逐字稿 / 上台講法**: 上台時可以怎麼講。
2. **深度補充 / 排練理解**: 從英文深度筆記轉成台灣華語的背景邏輯、案例與工作流。
3. **頁面訊息 / 這頁任務**: 這頁必須完成什麼。
4. **觀眾視角**: 一般民眾、軟體公司、資安工程師可能會怎麼問。
5. **趨勢與因應**: 被追問時可以補充的脈絡。

> 注意：這份逐字稿是為了排練清楚而整理，不是正式上台逐字照念稿。目前 `v1.3` PDF 仍是 deck source of truth。深度補充層是從英文 companion 轉寫成台灣華語後整理，不是逐字貼上原文。

## 查核基準

這份 deck 的核心不是「AI 模型很厲害」，而是：

**AI SaMD 要變成可被信任、可被修復、可被稽核的產品系統。**

外部資訊查核重點：

- FDA `Cybersecurity in Medical Devices: Quality Management System Considerations and Content of Premarket Submissions` 是 **February 2026 Final Guidance**，涵蓋 cybersecurity device design、labeling、premarket submission 文件，並處理 FD&C Act Section 524B；該 guidance 取代 2025 年 6 月版本。[S1]
- FDA Section 524B FAQ 說明 cyber device 的適用對象、postmarket vulnerabilities and exploits plan、CVD、updates / patches、SBOM，以及 device changes 對 cybersecurity 的文件需求。[S2]
- FDA AI-enabled DSF lifecycle guidance 是 **January 2025 Draft Guidance**，不是 final；它強調 AI-enabled devices 的 total product life cycle 思維。[S3]
- FDA AI-enabled medical device list 是透明度工具，FDA 也表示會探索標示 foundation model / LLM-based functionality 的方式。[S4]
- FDA AI PCCP guidance 是 **August 2025 Final Guidance**，要求 PCCP 描述 planned modifications、develop / validate / implement methodology，以及 impact assessment。[S5]
- TFDA 於 2025 年 8 月公告修正 AI/ML CADe / CADx 醫療器材查驗登記技術指引，並新增 AI/ML 醫療器材獨立性能評估常見問答集。[S6]
- TFDA 115 年度第 1 次醫療器材法規及管理溝通討論會議資料提到，AI 醫材可透過獨立性能評估提高驗證效率與靈活度，也鼓勵 AI 醫材業者採用 PCCP 以降低法遵成本。[S7]

## Slide 1｜Title：Designing Cybersecurity for AI in Regulated Environments

### 逐字稿 / 上台講法

各位好，我是林家聖。今天的題目是 AI 軟體醫材的資安實戰。
關鍵字看起來很多：FDA 524B、Threat Modeling、Patch SLA。
但今天我只想留下三件事：信任、修補、證據。

### 深度補充 / 排練理解

這頁的深層任務不是介紹講者，而是讓觀眾立刻知道：這不是 AI hype、不是法規朗讀，也不是工具清單。核心問題是：一個 AI model 要變成可信醫療產品前，需要哪些證據與決策？

可以把全場壓成四個資料夾：`Boundary` 放 intended use、system boundary、data flow；`Evidence` 放 architecture、threat model、risk assessment、controls、testing；`Decision` 放 finding triage、risk acceptance、compensating controls；`Repair proof` 放 patch record、retest evidence、customer advisory、release history。

上台時不要花太多時間鋪背景。用一句話把場打開：今天不是背法規，而是問 AI 醫療產品要如何被信任、被修補、被稽核。

### 頁面訊息 / 這頁任務
這頁建立定位：這不是一般 AI talk，而是把 FDA Section 524B 作為醫療 AI 產品資安與治理的入口。

### 觀眾視角：一般民眾

可能問題：這是不是太法規、太技術？跟我看病有什麼關係？

回答：

**這場不是在講駭客，而是在講當 AI 進入醫院後，病人能不能相信結果、醫師能不能拿到結果、系統出事能不能修回來。**

### 觀眾視角：軟體公司

可能問題：我們還不是 FDA 送審階段，現在需要管 524B 嗎？

回答：

不要把 524B 只講成法規門檻，而要講成產品設計語言。越早把 SBOM、漏洞處理、patch、CVD、risk decision 放進開發流程，越不會在上市前才補文件。

### 觀眾視角：資安工程師

可能問題：Section 524B 對我實際工作代表什麼？

回答：

直接對應四件事：**威脅模型、SBOM、漏洞監測、修補證據。** 不是寫一份 policy，而是把 evidence chain 做出來。

### 趨勢與因應 / 可補充脈絡

FDA AI-enabled medical device list 逐步增加透明度，也提到未來會探索標示 foundation model / LLM-based functionality 的方法。[S4]

因應：第 1 頁可在口語副標加一句：

**From model performance to product accountability.**

## Slide 2｜Disclaimer

### 逐字稿 / 上台講法

這是大會必要的 disclaimer。這裡我停一下，讓大家看見。
接下來我們直接進入今天真正的問題。

### 深度補充 / 排練理解

這頁是 compliance beat，不是敘事頁。它的功能是建立公共演講的責任邊界：不是醫療建議、不是法律意見、不是任何特定公司照抄即可合規的保證。

公開場合也要保護資料邊界。不要在這場露出 private hospital / client details、內部架構、學生資料、patent-sensitive mechanisms，或足以變成攻擊教學的 exploit steps。

CYBERSEC 有 AI 即時翻譯，所以口語要短、清楚、少縮寫。後面的 anchor lines 要讓翻譯也能抓住意思：`你賣的不是模型`、`法規要的是證據，不是口號`、`Cyber Safety is Patient Safety`。

### 頁面訊息 / 這頁任務
這頁是標準 CYBERSEC 免責聲明。用途是避免觀眾把演講內容誤認為醫療建議、法律意見或官方立場。

### 觀眾視角：一般民眾

可能問題：所以這些內容是不是不能當成醫療建議？

回答：

**這不是醫療建議，也不是法律意見；這是讓大家理解 AI 醫療產品為什麼需要資安證據與治理流程。**

### 觀眾視角：軟體公司

可能問題：我們可以直接把這份簡報當作內部 SOP 或送審文件嗎？

回答：

不行。這份 deck 可以當架構參考，但實際 SOP 要依產品 intended use、架構、風險分級、上市市場、QMS 與 submission pathway 調整。

### 觀眾視角：資安工程師

可能問題：Patch SLA、72 小時 KEV assessment、15 天 advisory 是不是 FDA 硬性要求？

回答：

不是。這些是 operating model。FDA FAQ 談的是 postmarket updates / patches、SBOM、變更影響 cybersecurity 時的文件需求；實際期限要由產品風險、臨床影響、客戶環境與 QMS 決策定義。[S2]

### 趨勢與因應 / 可補充脈絡

AI 醫療、資安與法規的交界越來越高風險。未來簡報最好標註資料查核日期與法規可能更新。

因應：disclaimer 口頭補一句：

**Regulatory references verified as of 2026-04.**

## Slide 3｜Table of Contents

### 逐字稿 / 上台講法

這頁我先給大家今天的地圖。

今天不是一堂法規課，也不是工具清單。我們會走四個問題：第一，產品邊界在哪裡；第二，風險怎麼變成證據；第三，finding 進來之後誰做 decision；第四，修補完成後怎麼留下 repair proof。

如果只記一條線，就是：Boundary -> Evidence -> Decision -> Repair Proof。產品先被定義，風險才看得見；風險看得見，證據才接得起來；證據能被決策，系統才修得回來。

### 深度補充 / 排練理解

英文 deep-note companion 沒有獨立的 Table of Contents 頁，因為它原本對應的是 14-slide fallback。這裡要把它轉成 `v1.3` 的導航頁：Boundary -> Evidence -> Decision -> Repair Proof。

這頁不用講深。它的任務是降低觀眾負擔，讓一般民眾知道這不是抽象法規，讓公司知道這可以變 roadmap，讓資安工程師知道後面會談 owner、decision、evidence，而不是只談掃描工具。

最重要的轉場句：產品先被定義，風險才看得見；風險看得見，證據才接得起來；證據能被決策，系統才修得回來。

### 頁面訊息 / 這頁任務
四段主軸很清楚：Boundary -> Evidence -> Decision -> Repair Proof。這是整份簡報的骨架。

### 觀眾視角：一般民眾

可能問題：Boundary、Evidence、Decision、Repair Proof 聽起來很抽象。

回答：

**先知道產品管到哪裡，再知道風險在哪裡；風險看得見，才有證據；證據能被決策，系統才修得回來。**

### 觀眾視角：軟體公司

可能問題：這四段可以變成產品開發 roadmap 嗎？

回答：

可以，直接對成四個里程碑：

1. **Boundary**：產品邊界、角色、資料流。
2. **Evidence**：SBOM、threat model、測試紀錄。
3. **Decision**：triage、risk acceptance、patch plan。
4. **Repair Proof**：修補、重測、release history。

### 觀眾視角：資安工程師

可能問題：Decision 是誰決策？資安、法規，還是臨床？

回答：

應該是 cross-functional decision：Product Security、Engineering、Regulatory、Clinical Safety、Customer Success 一起進 risk register。沒有 owner 的 decision，就是口頭承諾。

### 趨勢與因應 / 可補充脈絡

NIST CSF 2.0 把 Govern 加入核心功能，和 Identify、Protect、Detect、Respond、Recover 並列；NIST AI RMF 則用 Govern、Map、Measure、Manage 管 AI risk。[S8][S9]

因應：這頁可在口語中建立 mapping：

**Boundary = Identify / Map；Evidence = Measure；Decision = Govern / Manage；Repair Proof = Respond / Recover。**

## Slide 4｜You Are Not Selling a Model

### 逐字稿 / 上台講法

很多 AI 團隊一開始會說：我們只是提供模型。
可是醫療現場不會這樣看。醫師看到的是結果，病人承受的是後果，公司要負責的是整個使用情境。
所以第一個轉念是：你賣的不是模型。你賣的是一個在醫療情境中可被信任、可被修補、可被稽核的系統。
這就是今天所有法規、測試和治理的起點。

### 深度補充 / 排練理解

這是第一個真正的 reframing moment。很多團隊說「我們只是提供模型」，但臨床現場看的是完整使用情境：資料從哪裡來、誰可以用、AI 結果誰確認、系統壞掉時怎麼恢復、漏洞誰修、修完怎麼證明。

可以用車子的比喻：模型準確率像引擎，但醫院買的是能上路的車。煞車、儀表板、維修、召回流程都不可信，再強的引擎也不能變成可信產品。

對工程師，這頁要打開 product boundary。模型周圍還有 Web UI、temporary DICOM storage、PACS / DICOM workflow、logs、configuration、deployment dependency。這些都會進入 SBOM、threat model、risk assessment、testing 和 Patch SLA。

這頁的 workflow 是 responsibility map：誰使用、在哪裡使用、輸入輸出是什麼、是否能直接臨床採用、誰確認、資料暫存多久、異常怎麼處理、產品怎麼更新、客戶怎麼通報事件。

### 頁面訊息 / 這頁任務
這是關鍵頁。它把模型準確率和醫院真正購買的產品責任切開：醫院買的是 intended use、human-in-the-loop、patch、incident reporting，不只是模型。

### 觀眾視角：一般民眾

可能問題：AI 不是醫師輔助工具嗎？為什麼講得像一整套系統？

回答：

AI 在醫院不是單獨存在。它要吃資料、產生輸出、給醫師看、接醫院系統、更新版本。任何一段出問題，都會影響醫師能不能安全使用它。

### 觀眾視角：軟體公司

可能問題：我們先賣 model API，其他交給醫院整合，這樣可以嗎？

回答：

可以作為商業策略，但責任不能模糊。你要清楚定義：

- intended use 是什麼。
- 使用者是誰。
- AI 結果是否需要人工確認。
- API failure 時誰負責。
- patch / incident 如何通知客戶。

TFDA 2025 AI/ML CADe / CADx 指引要求業者依產品功能、平台、架構、預期用途、使用限制、使用情境、判讀流程與輸出結果解讀等內容準備查驗登記資料。[S6]

### 觀眾視角：資安工程師

可能問題：Docker、WSL2、Node.js、Python、DCMTK 都要進 SBOM 嗎？

回答：

如果它們是產品交付、部署、執行或維護所依賴的元件，就應納入 asset inventory / SBOM / vulnerability management。FDA FAQ 也明確提到 SBOM 要涵蓋 commercial、open-source、off-the-shelf components。[S2]

### 趨勢與因應 / 可補充脈絡

AI 醫材會從 model-centric 轉向 workflow-centric。

因應：口語補一張產品責任鏈：

**Model -> Viewer -> API -> PACS/DICOM -> Hospital workflow -> Patch / Incident route。**

## Slide 5｜AI Is Becoming Infrastructure

### 逐字稿 / 上台講法

**2026 趨勢：AI 不只是模型，而是基礎設施**

2026 年很有意思。整個 AI 產業的語言正在改變。
大家不只談模型多大、跑分多高，而是談 AI factory、runtime、infrastructure、application，以及這整套東西怎麼被部署、被保護、被更新。
對醫療 AI 來說，這個趨勢更直接。因為醫療不是只把模型放上雲端就結束。它會接資料、接 workflow、接醫院網路，最後接到病人照護。
所以 AI security 也不能停在 model security。它必須往 runtime security、infrastructure security、supply chain security 延伸。

**為什麼是現在：資安事件已經變成照護中斷**

為什麼現在要談這件事？因為醫療資安已經不只是 IT 後台的問題。
在美國，勒索攻擊可以讓診所關閉、手術取消。
在台灣，醫院也已經出現大規模勒索事件，門急診電腦異常，臨床工作被迫降級。
在供應鏈端，醫療產品公司被攻擊，也可能影響全球客戶。
這些案例不是要製造恐慌，而是提醒我們：當 AI 進入醫療，cyber incident 很快就會變成 care disruption。

### 深度補充 / 排練理解

這頁回答：為什麼現在要談？因為 AI 正在從單一 model file 變成 care infrastructure。它會接 runtime、data、identity、update chain、support path，最後接到 clinical workflow。

台灣脈絡要提，但不要讓它變第二場國家戰略簡報。台灣的資安戰略把 AI security、critical infrastructure、key industries、supply chain resilience 放在一起，醫療 AI SaMD 是其中一個很具體的交會點。

案例的用法是支撐 clinical continuity，不是製造恐慌。Change Healthcare 說明第三方醫療基礎設施中斷會影響 patient care 和財務；台灣醫院勒索事件提醒本地觀眾，醫療資安不是國外新聞。

可用的 readiness check：模型在哪裡跑？資料從哪裡來？誰能呼叫 API？誰看 log？誰能更新？更新失敗如何 rollback？醫院端如何 fallback？這些如果沒有寫進 architecture view 和 labeling，AI infrastructure 就只是口號。

### 頁面訊息 / 這頁任務
這頁把 AI 拆成 Model Layer、Runtime Layer、Infrastructure Layer，並用 Change Healthcare 事件說明第三方基礎設施失效會擴散到臨床。

### 觀眾視角：一般民眾

可能問題：一家公司的系統被攻擊，為什麼會影響醫院看診？

回答：

Change Healthcare 事件就是例子。AHA 對近 1,000 家醫院的調查顯示，74% 回報 direct patient care impact，94% 回報 financial impact。[S10]

重點句：

**醫療不是單一醫院在運作，而是一條供應鏈。供應鏈斷掉，病人的流程就會被拖慢。**

### 觀眾視角：軟體公司

可能問題：我們只是 AI vendor，也會被當成醫療基礎設施風險嗎？

回答：

會，尤其是產品碰到資料流、更新機制、身份權限、醫院網路、PACS/DICOM。你的產品如果出問題會卡住臨床流程，就不是單純 SaaS bug。

### 觀眾視角：資安工程師

可能問題：這三層要怎麼落控制？

回答：

- Model layer：model provenance、hash / signature、version pinning。
- Runtime layer：container hardening、secret management、API auth、logging。
- Infrastructure layer：IAM、network segmentation、SBOM、update channel、incident route。

### 趨勢與因應 / 可補充脈絡

AHA 引用 FBI 2025 Internet Crime Report 指出，health care and public health 是 2025 年 cyberthreats top-targeted sector，包含 460 起 ransomware attacks 與 182 起 data breaches。[S11]

因應：AI SaMD 公司要把供應鏈韌性變成產品能力：deployment guide、downtime fallback、incident contact、customer advisory template。

## Slide 6｜Risk Grows With Architecture

### 逐字稿 / 上台講法

這張是今天的地圖。請大家先記四層就好。
第一層，只有 AI model。
第二層，model 加 viewer。
第三層，viewer 加平台和資料庫。
第四層，完整 connected AI medical system。
每加一層，產品能力變強，攻擊面也變大。法規要看的，不是你說自己安全，而是你能不能拿出跟這個尺度相稱的證據。

### 深度補充 / 排練理解

這頁是全場地圖。同一個 AI model，放在不同產品邊界，資安責任完全不同。Model、Viewer、Platform / Database、Connected Medical System 不是裝飾分類，而是 evidence burden 的成長線。

Scale 1 要看 model source、data lineage、dependencies、SBOM、version pinning、update boundary。Scale 2 加上 viewer，就要看 file parser、upload、cache、output interpretation。Scale 3 有 identity、API、database、audit log、backup。Scale 4 進 hospital network，就要看 PACS/HIS、update server、remote service、downtime fallback。

對主管，這頁是資源排序工具。小團隊不可能第一天做完所有 control，但必須知道自己在哪一層。每次產品新增功能，都要做 Product Boundary Review：我們是否跨層？architecture、threat model、risk assessment、testing scope、labeling、Patch SLA 是否同步更新？

### 頁面訊息 / 這頁任務
這頁很強：同一個 AI model，因產品邊界不同，資安責任完全不同。Scale 1 是 model；Scale 4 已經是 connected medical system。

### 觀眾視角：一般民眾

可能問題：為什麼加一個 viewer 或資料庫，風險就變大？

回答：

**每多一個功能，就多一扇門。門越多，就越需要門鎖、監視器、逃生路線和修理流程。**

### 觀眾視角：軟體公司

可能問題：什麼時候我們的責任會從 AI 模型變成醫療系統？

回答：

當你提供 viewer、database、API、update channel、hospital integration、PACS/DICOM workflow 時，就開始跨出模型責任。FDA 2026 guidance 的目標是促進 device design、labeling 與 premarket cybersecurity documentation，並處理有 cybersecurity risk 的 devices。[S1]

### 觀眾視角：資安工程師

可能問題：這張 scale diagram 要怎麼變成 threat model？

回答：

把每個 scale 變成 control baseline：

- Scale 1：model artifact integrity。
- Scale 2：file parser / viewer fuzzing。
- Scale 3：IAM、API auth、audit log、backup。
- Scale 4：VLAN、default-deny firewall、DICOM-TLS、downtime fallback。

### 趨勢與因應 / 可補充脈絡

FDA 2026 guidance 的趨勢是把 cybersecurity 放入 QMS 語言，而不是最後補一份附錄。[S1]

因應：每次產品架構改版，都要同步更新 threat model、SBOM、risk assessment、deployment guide。

## Slide 7｜Evidence, Not Slogans

### 逐字稿 / 上台講法

**法規要的是證據，不是口號**

我用一句話講法規：法規要的是證據，不是口號。
FDA、TFDA、NIST 用的語言不完全一樣，但方向很一致：你要知道風險在哪裡，你要有控制措施，你要測試，你要修補，你要留下紀錄。
對管理者來說，這不是 paperwork。這是一家公司證明自己可靠的方式。

**FDA 524B：一句商業語言**

FDA 524B 可以講得很法律，也可以講得很商業。
商業語言就是：如果你的醫材會連線，上市前就要準備好上市後怎麼監控漏洞、怎麼修補、怎麼告知客戶，以及你的軟體裡到底有哪些元件。
換句話說，產品出貨不是故事的結束。出貨後能不能持續維護，才是醫療產品信任的一部分。

**FDA 2026 Cybersecurity Guidance：審查者會看什麼**

審查者不會只看一份掃描報告。
他們會問：你的 threat model 在哪裡？你的 architecture 怎麼畫？你的控制措施對應到哪些風險？你的測試有沒有真的打到攻擊面？
更重要的是，每個 finding 最後去哪裡了？修掉、補償、延後但有時程，或是有理由判定不適用。
這就是從 risk 到 control，到 test，到 fix 的一條線。這條線接不起來，文件再多也只是資料夾。

### 深度補充 / 排練理解

這是最容易超時、但也最重要的知識頁。第一句要先講出來：`法規要的是證據，不是口號。`

FDA 524B 可以壓成 lifecycle obligations：monitor、identify、address postmarket cybersecurity vulnerabilities and exploits；coordinated vulnerability disclosure；updates and patches；SBOM。FDA 2026 cybersecurity guidance 的新重點，是把這些期待放進 quality management system 的語言，而不是最後補一份附錄。

對一般觀眾，可以用健康檢查比喻：不能只說我很健康，要有檢查結果、判讀和追蹤紀錄。對產品團隊，這條線就是 Risk -> Control -> Test -> Fix -> Evidence。

實作上可以用 Evidence Chain Ticket。每個 finding 不能只寫 fixed，而要有 Risk ID、Control ID、Test ID、Finding ID、Decision、Retest Evidence、Archive Location。這樣法規文件才不是作文，而是工程與治理工作自然留下的證據。

### 頁面訊息 / 這頁任務
這頁是全 deck 的靈魂之一：不要說「我們很安全」，要拿出 Risk -> Control -> Test -> Fix & Prove 的證據。

### 觀眾視角：一般民眾

可能問題：我要怎麼知道廠商不是只是在說好聽話？

回答：

**可信任不是靠口號，而是靠可檢查的證據。就像健康檢查不能只說我很健康，要有檢查結果。**

### 觀眾視角：軟體公司

可能問題：我們到底要準備哪些證據？

回答：

最基本要有：

- Threat model。
- Security requirements。
- SBOM。
- SCA / SAST / fuzz / pen test results。
- Vulnerability triage records。
- Patch / retest evidence。
- CVD process。
- Risk acceptance records。

Section 524B FAQ 提到 patches / updates、SBOM，以及 device change 若影響 cybersecurity，應有相對應文件。[S2]

### 觀眾視角：資安工程師

可能問題：STRIDE mapping 夠嗎？

回答：

STRIDE 是起點，不是終點。AI SaMD 應加上：

- clinical abuse cases。
- model tampering scenario。
- data poisoning scenario。
- malicious DICOM file scenario。
- update channel compromise。
- hospital LAN lateral movement。

### 趨勢與因應 / 可補充脈絡

Contec / Epsimed patient monitor 案例顯示，降低 unacceptable risk 有時不是加功能，而是拿掉功能；FDA 說該 patch 完全移除 affected devices 的 networking functionality，使裝置只能 local monitoring，且安裝需要專業人員。[S12]

因應：把 **feature removal / degraded mode** 納入 risk mitigation options。

## Slide 8｜Model, Governance, Stack

### 逐字稿 / 上台講法

**TFDA 視角：AI/ML SaMD 要說清楚模型與證據**

回到台灣，TFDA 的 AI/ML SaMD 視角提醒我們一件事：AI 模型不是黑盒子傳奇。
你要說清楚 intended use，誰用、在哪裡用、不能怎麼用。
你要說清楚資料怎麼來，訓練、驗證、測試怎麼切，臨床性能怎麼證明。
所以資安不是外掛；它要跟模型文件、軟體確效、臨床證據一起長出來。

**NIST 視角：給老闆聽得懂的管理語言**

NIST 的價值，是把工程問題翻譯成管理語言。
Govern 是誰負責。Identify 是我們有哪些資產和風險。Protect 是怎麼防。Detect 是怎麼知道出事。Respond 是怎麼處理。Recover 是怎麼恢復。
這些字聽起來很基本，但對公司很重要，因為它讓董事會、PM、RD、法規和客服可以講同一種語言。

**AI Security Stack：Model / Runtime / Infrastructure**

接下來我想給大家一個 2026 版本的簡化模型：model、runtime、infrastructure。
Model security 問的是：模型從哪裡來，怎麼評估，怎麼更新，能不能被惡意輸入影響。
Runtime security 問的是：模型執行時，秘密怎麼保護，log 怎麼留，policy 怎麼執行，環境能不能隔離。
Infrastructure security 問的是：身份、容器、雲端設定、網路、更新鏈是否可信。
醫療 AI 要安全，這三層不能只挑一層做。

### 深度補充 / 排練理解

這頁把前一頁的 evidence chain 拆成公司內部聽得懂的三種語言：model evidence、governance language、AI stack security。

Model evidence 給 ML、clinical、regulatory：intended use、data、V&V、limits、clinical performance。Governance language 給管理層、PM、QA、法規、資安：誰負責、如何 map risk、如何 measure、如何 manage。AI stack security 給工程：model provenance、runtime isolation、secrets、logs、identity、network、update path。

NIST CSF 2.0 和 AI RMF 不要硬合併成一張控制表。AI RMF 的 Govern / Map / Measure / Manage 是 AI risk 的共同語言；CSF 的 Govern / Identify / Protect / Detect / Respond / Recover 是資安營運語言。

每次 design review 可以用 Three-Layer Governance Review：Model behavior 欄、Software stack 欄、Clinical workflow 欄。這能避免模型、工程、法規各講各的。

### 頁面訊息 / 這頁任務
這頁把可信任 AI 拆成三個學科：Model Evidence、Governance Language、AI Stack Security。

### 觀眾視角：一般民眾

可能問題：AI 安全到底是模型準、公司管得好，還是系統不被駭？

回答：

答案是三個都要：

**模型要有證據，組織要能治理，系統要能防護。少一個都不夠。**

### 觀眾視角：軟體公司

可能問題：這三塊誰負責？

回答：

建議分工：

- Model Evidence：ML / Clinical / Regulatory。
- Governance Language：QMS / Product / Risk owner。
- AI Stack Security：Security / DevOps / SRE / Engineering。

NIST CSF 2.0 的 Govern 功能涵蓋 strategy、policy、roles、responsibilities、supply chain risk management；NIST AI RMF 則用 Govern、Map、Measure、Manage 管理 AI risk。[S8][S9]

### 觀眾視角：資安工程師

可能問題：OWASP LLM Top 10 跟醫療影像 AI 有關嗎？

回答：

如果產品沒有 LLM，不要硬套 prompt injection；但 supply chain、data / model poisoning、insecure output handling 的邏輯仍然 relevant。OWASP LLM Top 10 屬於 broader GenAI security work，適合用來提醒 LLM 或 agentic workflow 的風險邊界。[S13]

### 趨勢與因應 / 可補充脈絡

未來 AI security 會從 model security 走向 **AI system security + AI governance**。

因應：在公司內建立一張 crosswalk：FDA / TFDA / NIST CSF / NIST AI RMF / OWASP / internal QMS。

## Slide 9｜Scale 1-2: Model to Viewer

### 逐字稿 / 上台講法

**Scale 1：只有 AI Model**

現在回到四種尺度。
如果你真的只有 AI model，恭喜，你的範圍最小，但不是沒有資安。
你要先保護模型 artifact、資料 lineage、dependency、SBOM，以及更新邊界。
小團隊最常犯的錯，是等到要接 viewer 或平台時才補文件。比較聰明的做法，是從第一版 model 就開始留下最小證據。

**Scale 2：AI Model + Viewer**

一旦加上 viewer，世界改變了。
因為攻擊者不一定攻擊你的模型，他可以攻擊檔案解析、upload、暫存資料、UI 呈現，甚至攻擊使用者怎麼理解輸出。
所以這一層要做 DICOM 或 image parser 的檢查，做 malformed file 和 fuzzing，也要確保畫面上的限制說明不會讓醫師誤用。

### 深度補充 / 排練理解

這頁把前半段的 scale map 落到前兩層。Scale 1 的重點是 model 本身就是 asset：來源、版本、training / validation context、hash/signature、dependency、SBOM、update boundary 都要可追。

Scale 2 的重點是 viewer 讓模型進入使用情境。攻擊者不一定攻擊模型，也可能攻擊 file parser、malformed DICOM handling、cache、UI error message、output interpretation。

MicroDicom CVE-2025-35975 是好例子：DICOM viewer 的 out-of-bounds write 可能因開啟惡意 DCM file 而造成 arbitrary code execution。這證明 viewer/parser 不是被動外殼，而是真實 attack surface。

實作上，Scale 1 建 model release card：model version、dataset references、metrics、known limitations、SBOM、hash/signature、approved intended use。Scale 2 建 viewer input safety workflow：DICOM conformance validation、file size/type checks、malformed-file testing、fuzzing、temporary data encryption、cache deletion、generic error message、output limitation notice。

### 頁面訊息 / 這頁任務
這頁提醒：model artifact 是資產，viewer 是 attack surface。DICOM viewer 不是被動外殼，而是真實攻擊面。

### 觀眾視角：一般民眾

可能問題：只是打開一個醫療影像檔，也可能被攻擊？

回答：

是。NVD 的 CVE-2025-35975 顯示 MicroDicom DICOM Viewer 有 out-of-bounds write 漏洞，使用者開啟惡意 DCM file 可能導致任意程式碼執行。[S14]

### 觀眾視角：軟體公司

可能問題：我們用第三方 viewer，是不是就不用負責？

回答：

不能這樣切。你可以用第三方元件，但仍要管理：

- 版本。
- 漏洞。
- 更新。
- SBOM。
- vendor advisory。
- sandboxing。
- file validation。
- fallback workflow。

### 觀眾視角：資安工程師

可能問題：Model asset 和 viewer attack surface 要怎麼控？

回答：

Model asset：

- hash / signature。
- model registry。
- artifact provenance。
- deployment allowlist。
- inference log with model version。

Viewer：

- fuzz malformed DICOM。
- sandbox parser。
- restrict file type / size。
- disable unsafe preview。
- isolate cache。
- monitor crash / exploit signals。

### 趨勢與因應 / 可補充脈絡

未來醫療 AI 的攻擊面會越來越偏向周邊元件：viewer、parser、plugin、update channel、container image。

因應：不要只測 model；要把 DICOM parser fuzzing、file upload abuse cases、viewer patch cadence 放進 release gate。

## Slide 10｜Scale 3-4: Platform to Connected Medical System

### 逐字稿 / 上台講法

**Scale 3：Viewer + Platform + Database**

平台化之後，資安就變成公司風險。
你開始有帳號、角色、API、資料庫、雲端、log、backup。
這時候最重要的問題不是「模型準不準」，而是「錯的人能不能看到資料」、「API 能不能被濫用」、「資料外洩時 blast radius 有多大」。
對老闆來說，這裡開始是營運風險、法規風險，也是品牌信任風險。

**Scale 4：完整 Connected AI Medical System**

當產品進入醫院網路，事情再升級一次。
它可能接 PACS、HIS、醫療設備、遠端服務、更新伺服器。
如果這一層出事，不只是單一使用者不方便，而可能同時影響多名病人和臨床營運。
這就是 cybersecurity 真正變成 patient safety 的時刻。

### 深度補充 / 排練理解

這頁把風險推到公司營運與臨床連續性。Scale 3 有 platform/database 後，identity、permission、API、database、audit log、backup 都會變成公司風險，不只是 RD 風險。

Scale 4 進入 hospital network 後，風險會變成 clinical continuity。供應商、醫院 IT、臨床團隊之間需要 shared responsibility model：vendor-owned zone、shared zone、hospital-owned zone，各自負責什麼要清楚。

Synnovis 和台灣醫院勒索事件都可以用來說明：醫療供應商或醫院系統被攻擊，影響不只是一個功能壞掉，而是服務恢復、資料風險、臨床流程和 public trust。

實作上，Scale 3 要有 platform security baseline：MFA/RBAC、API authorization、rate limit、audit log、encryption-at-rest、backup/restore drill。Scale 4 要有 connected deployment checklist：isolated VLAN、Default-Deny firewall、allowed PACS IP/AE Title、DICOM-TLS 或 VPN、SIEM/SOC log forwarding、secure update channel、manual update window、downtime fallback、hospital IT contact、incident route。

### 頁面訊息 / 這頁任務
這頁把風險推到平台與醫院網路：Identity、MFA/RBAC、API authorization、audit log、backup/restore、VLAN、firewall、DICOM-TLS、downtime fallback。

### 觀眾視角：一般民眾

可能問題：供應商被駭，真的會讓醫院停擺那麼久？

回答：

Synnovis 事件就是例子。NHS England 說 Synnovis 2024 年 6 月遭 ransomware attack，造成超過 11,000 個 outpatient 與 elective procedure appointments 延誤；服務到 2024 年 12 月才完全恢復，且 2024 年 6 月 20 日攻擊者公布竊取資料。[S15]

### 觀眾視角：軟體公司

可能問題：我們交付 deployment guide 就夠了嗎？

回答：

不夠。你需要 shared responsibility model：

- Vendor-owned zone。
- Shared zone。
- Hospital-owned zone。
- 誰負責 VLAN。
- 誰負責 firewall。
- 誰負責 update channel。
- 誰接 incident call。
- downtime fallback 怎麼啟動。

### 觀眾視角：資安工程師

可能問題：接到 hospital LAN 之後，最該怕什麼？

回答：

最該怕 lateral movement 與 clinical continuity failure。控制重點：

- MFA / RBAC。
- API authz。
- audit log completeness。
- network segmentation。
- default-deny firewall。
- DICOM-TLS。
- immutable backup。
- restore drill。
- incident route。

### 趨勢與因應 / 可補充脈絡

HSCC 2026 第三方 AI 風險與供應鏈透明度指南把 data lineage、model auditability、embedded third-party dependencies、post-deployment monitoring 列為醫療 AI 供應鏈最佳實務。[S16]

因應：對醫院客戶提供 AI supply chain disclosure package，而不是只提供產品簡介。

## Slide 11｜Cyber Safety Is Patient Safety

### 逐字稿 / 上台講法

這句話我希望大家帶走：Cyber Safety is Patient Safety。
醫療 AI 出事時，受影響的不只是模型績效，而是病人、醫院營運、供應商責任與臨床流程。
未來的好產品，不會只說「我們的模型很準」。它還要能說：我們知道供應鏈在哪裡，我們知道漏洞怎麼通報，我們知道事件發生時怎麼跟醫院合作，也知道怎麼保護照護不中斷。

### 深度補充 / 排練理解

這是全場 emotional peak。畫面只需要一個清楚句子：`Cyber Safety Is Patient Safety.` 不要把它稀釋成 checklist。

要把 CIA triad 翻成醫療語言：Availability 不是 uptime，而是醫師需要時拿得到結果；Integrity 不是資料沒變，而是醫師能相信輸出；Repairability 不是工程流程，而是事故後能安全恢復。

案例可以回扣，但不要堆太多。Change Healthcare 說明第三方基礎設施中斷會影響照護與財務；Synnovis 說明 pathology service interruption 的恢復成本；Contec/Epsimed 說明有時 mitigation 甚至會移除 networking functionality。

實作上，risk register 要多一欄 clinical impact：這個 vulnerability 是否影響 confidentiality、integrity、availability？是否讓 AI result 不可信？是否延誤 workflow？是否需要 downtime fallback？是否需要 hospital advisory？這一欄會讓醫師、主管、QA、法規、資安開始講同一種語言。

### 頁面訊息 / 這頁任務
這頁把 Availability、Integrity、Repairability 轉成病人安全語言。

### 觀眾視角：一般民眾

可能問題：資安怎麼會等於病人安全？

回答：

三句話即可：

- **Availability**：醫師需要時拿得到結果。
- **Integrity**：醫師拿到的是可信結果。
- **Repairability**：出事後可以安全恢復。

### 觀眾視角：軟體公司

可能問題：這些要怎麼變成 KPI？

回答：

建議 KPI：

- clinical workflow uptime。
- RTO / RPO。
- failed inference recovery time。
- data integrity check pass rate。
- patch retest completion rate。
- incident notification time。
- downtime fallback drill success rate。

### 觀眾視角：資安工程師

可能問題：這不是 CIA triad 嗎？

回答：

是，但醫療版要重新定義：

**Confidentiality 是隱私，Integrity 是診斷可信度，Availability 是臨床連續性，Repairability 是病人安全恢復能力。**

### 趨勢與因應 / 可補充脈絡

醫療資安事件的評估會越來越從「資料有沒有外洩」轉向「照護有沒有中斷」。Change Healthcare 和 Synnovis 都證明 disruption 本身就是病人安全與營運風險。[S10][S15]

因應：security severity scoring 要加入 clinical impact，不要只看 CVSS。

## Slide 12｜Testing Portfolio

### 逐字稿 / 上台講法

**White-Box Testing：從內部看見可修的問題**

接下來進入最實作的部分。
White-box testing 的精神很簡單：在 release 前，從內部把便宜、可修、可追溯的問題找出來。
看 code、看 config、看 secrets、看 dependencies、看 container、看 cloud 設定，也看 AI pipeline 有沒有資料洩漏或更新邊界不清。
白箱的價值不是製造一堆紅字，而是讓工程團隊早一點修掉真正會變成風險的東西。

**Black-Box Testing：從攻擊者視角驗證真實暴露**

Black-box testing 的問題不同。
它問的是：如果我不知道你的原始碼，只從外部看，我能不能打穿產品？
我能不能繞過登入？能不能上傳奇怪檔案讓 viewer 出錯？能不能濫用 API？能不能把幾個小問題串成一條攻擊路徑？
所以 white-box 是早期修問題，black-box 是 release 或送審前驗證真實暴露。兩個不是互相取代，而是前後接力。

### 深度補充 / 排練理解

這頁進入實作，但不能變工具清單。核心句是：每一種測試都要回答一個 decision question。

SBOM / SCA 問：我們用了哪些元件，有哪些 known vulnerabilities？White-box 問：release 前有哪些便宜、可修、可追的問題？Fuzz / abuse case 問：異常輸入會不會打壞 workflow？Black-box 問：外部看得到什麼暴露？Pen test 問：漏洞能不能串成 realistic attack path？Retest 問：修補是否真的有效？

測試的目的不是讓報告好看，而是讓 finding 進治理流程。Testing-to-Finding Pipeline 可以這樣跑：先定 scope，再跑 white-box，再跑 black-box，所有 finding 進 Patch SLA，修補後 retest，最後 archive evidence。

對主管要說：如果測試結果沒有 owner、severity、due date、fix decision、retest evidence，它只是外包報告，不是產品成熟度。

### 頁面訊息 / 這頁任務
這頁把測試從工具清單變成治理問題：每種測試回答不同 decision question。

### 觀眾視角：一般民眾

可能問題：為什麼要這麼多測試？不能掃一次就好嗎？

回答：

不能。不同測試抓不同問題：

- SBOM / SCA：知道用了什麼。
- SAST：找開發階段可修問題。
- Fuzz：測異常輸入會不會打壞流程。
- Pen test：測真實攻擊鏈。
- Retest：證明修補有效。

### 觀眾視角：軟體公司

可能問題：小公司要做到這些會不會太貴？

回答：

用 risk-based sequencing：

1. 先自動化 SBOM / SCA / SAST。
2. 對 DICOM / file parser 做 abuse cases。
3. 針對 release candidate 做外部 pen test。
4. 所有 high / critical finding 必須 retest。
5. evidence archive 進 QMS。

### 觀眾視角：資安工程師

可能問題：怎麼證明 no unresolved anomaly exceeded acceptable risk threshold？

回答：

你需要 risk register，不是口頭判斷。每個 finding 要有：

- ID。
- affected component。
- threat scenario。
- severity。
- clinical impact。
- mitigation。
- residual risk。
- owner。
- due date。
- retest evidence。
- sign-off。

### 趨勢與因應 / 可補充脈絡

FDA 2026 guidance 已把 cybersecurity documentation 放進 premarket review 與 QMS 思維；CISA KEV 也成為漏洞優先級管理的重要輸入。[S1][S17]

因應：把 testing 變 release gate，而不是上市前外包一份報告。

## Slide 13｜Patch SLA: No Decision, No Governance

### 逐字稿 / 上台講法

如果只能帶走一個營運流程，我會選 Patch SLA。
因為真正的資安不是「沒有漏洞」，而是每個漏洞進來後，公司知道誰負責、多久判斷、多久修補、怎麼通知、怎麼重測、證據放哪裡。
這裡的四種結果也很重要：fix now、compensate、defer with timeline、non-applicable with rationale。
沒有 decision，就沒有治理；沒有證據，就沒有信任。

### 深度補充 / 排練理解

這頁是 operational climax。Patch SLA 不是 FDA 原文裡的固定名詞，而是把 FDA 524B 的 updates / patches、CVD、postmarket vulnerability management 翻成公司可以執行的 operating model。

真正的治理不是說「我們會修」，而是每個 finding 進來後都有 intake、applicability assessment、severity、owner、decision、action、retest、archive。

Decision 是這頁最大的一個字。Finding 進來後不是只有修或不修；可能是 fix now、compensate、defer with timeline、non-applicable with rationale。沒有 decision，就沒有治理；沒有證據，就沒有信任。

醫療產品還要加 safety override。Patch 可能影響 model accuracy、DICOM structure、clinical workflow、system stability 或既有驗證條件。如果有影響，就要先做 regression test、clinical performance check，必要時用 compensating control 暫時降低風險。

### 頁面訊息 / 這頁任務
這頁是另一個重點：patch 不是工程排程，而是治理決策。Intake -> Triage -> Decision -> Action。

### 觀眾視角：一般民眾

可能問題：發現漏洞為什麼不馬上修？拖什麼？

回答：

醫療產品不能像一般 app 一樣亂推更新，因為 patch 可能影響：

- AI model accuracy。
- DICOM structure。
- system stability。
- clinical workflow。
- 醫院部署環境。

所以要先 triage，再決策，再修，再重測。

### 觀眾視角：軟體公司

可能問題：Critical 15 天、30 天 mitigation plan 是不是可以寫進 SLA？

回答：

可以作為內部 operating model，但不要宣稱是 FDA 硬性規定。FDA FAQ 的說法是要有 postmarket updates / patches 與相關 lifecycle 計畫；實際時間要依風險定義。[S2]

### 觀眾視角：資安工程師

可能問題：72 小時 CISA KEV applicability assessment 合理嗎？

回答：

合理，甚至建議做。CISA KEV 是已知遭實際利用漏洞的權威輸入，可作為 vulnerability management prioritization framework 的一部分。[S17]

但醫療產品要加一層 safety override：如果 patch 會影響臨床安全，就先做 compensating control，再排正式修補與驗證。

### 趨勢與因應 / 可補充脈絡

漏洞管理正在從 CVSS 高低走向「是否已被利用 + 是否影響臨床」。Contec / Epsimed 案例顯示，patch 甚至可能移除 networking functionality，讓裝置只保留 local monitoring。[S12]

因應：Patch SLA 裡要同時有 security impact、clinical impact、customer communication。

## Slide 14｜Small Team: 30 / 60 / 90

### 逐字稿 / 上台講法

**Small Team Playbook：不要一開始就蓋大型制度**

我知道很多公司聽到 FDA、TFDA、NIST 會覺得壓力很大。
但小團隊不需要第一天就蓋大型制度。
先建立 minimum viable regulatory evidence folder：intended use、architecture、data-flow、SBOM、threat model、test reports、vulnerability log、patch SLA、release history。
然後把便宜的檢查自動化：dependency scan、secret scan、SAST、container scan。
把需要獨立性的事情外包：pen test、regulatory review、高風險架構 review。這樣就夠務實。

**30 / 60 / 90 天落地路線圖**

最後把它變成 30、60、90 天。
30 天，先盤點：資產、SBOM、資料流程、intended use、已知漏洞。
60 天，建立節奏：threat model、CI security gates、finding workflow、customer security note。
90 天，做外部驗證：penetration test、patch SLA、CVD process、retest evidence、release history。
重點不是三個月變完美，而是三個月後，公司已經開始自動留下可信的證據。

### 深度補充 / 排練理解

這頁是降低進場門檻。小團隊不需要第一天建立大型制度，而是先建立第一個 evidence loop。

30 天先 make the product visible：intended use、user roles、data flow、component inventory、SBOM、known vulnerabilities。60 天讓 risk flow into workflow：STRIDE workshop、CI security gate、finding triage、customer security note template。90 天補 validation and repair proof：vulnerability scan、black-box pen test、Patch SLA drill、CVD process、retest record。

`30 / 60 / 90` 不是法規要求，也不是 SLA 固定格式。它是 adoption scaffold，讓主管、PM、RD、QA、資安不用先討論完美制度，而是先對齊第一個 90 天要產生的證據。

如果聽眾是成熟企業，可以改講 `first 90-day evidence loop`；如果是 startup，保留 `30 / 60 / 90`，因為它降低心理成本。

### 頁面訊息 / 這頁任務
這頁很實用。它把小團隊如何開始做 evidence loop 具體化。

### 觀眾視角：一般民眾

可能問題：小公司真的做得到嗎？

回答：

做得到，但不是一開始就做到完美。重點是 90 天內從口頭記憶變成可重複證據。

### 觀眾視角：軟體公司

可能問題：30 / 60 / 90 每階段到底要交什麼？

回答：

- **Day 30**：SBOM、data flow diagram、intended use、user roles、component inventory、known vulnerabilities list。
- **Day 60**：STRIDE workshop、CI security gates、finding triage workflow、customer security note template、CISA KEV cross-reference。
- **Day 90**：black-box pen test、internal vulnerability scan、Patch SLA drill、CVD process、retest records、release history。

### 觀眾視角：資安工程師

可能問題：如果資源不夠，哪個先做？

回答：

先做 visibility，再做 governance：

1. 先知道自己有什麼。
2. 再知道風險在哪裡。
3. 再把風險變成 decision。
4. 最後留下 repair evidence。

### 趨勢與因應 / 可補充脈絡

TFDA 2026 說明資料提到，AI 醫材可透過獨立性能評估提高驗證效率與靈活度，也鼓勵採用 PCCP 以降低法遵成本。[S7] FDA PCCP guidance 也強調 AI-enabled devices 可在事先規劃的變更範圍內持續改善，同時維持安全與有效性。[S5]

因應：小團隊不要追求一次做滿，要先建立第一個 evidence loop。

## Slide 15｜Build Trust Before the Audit

### 逐字稿 / 上台講法

今天我們從一個 model 開始，走到 connected medical system。
每往前一步，產品更有價值，也更需要被信任、被修補、被稽核。
所以我想用一句話結束：先把安全做進產品，法規文件才會自然長出來。
真正成熟的團隊，不是文件最多的團隊，而是每一個風險都知道怎麼證明、怎麼修、怎麼追的團隊。謝謝大家。

## Apple-Like Visual / Pacing Cleanup For Rehearsal

- Slide 3: after saying `你賣的不是模型`, pause for one beat before explaining the system risk.
- Slide 4: do not list every GTC phrase. Say `AI is becoming infrastructure`, then come back to healthcare.
- Slide 6: point to the four scales as the map for the next 20 minutes.
- Slide 9: slow down on `risk -> control -> test -> fix`; this is the regulatory spine.
- Slide 12: use the three stack layers as a clean reveal: model, runtime, infrastructure.
- Slide 17: make `Cyber Safety is Patient Safety` the emotional center.
- Slide 20: treat Patch SLA as the operational climax, not an administrative slide.
- Slide 23: end gently. Do not add new technical points after the closing sentence.

## Musk-Like Narrative Cleanup For Rehearsal

- Keep returning to first principles: `What is the product really responsible for?`
- Raise the stakes without hype: `A cyber event can become a care-disruption event.`
- Name the bottleneck: `The bottleneck is not knowing what to do; it is producing evidence that the company actually did it.`
- Offer an engineering path: `product scale -> threat model -> tests -> patch workflow -> evidence archive.`
- End with an executable future: `30 / 60 / 90 days`.

## Emergency Cut Version

If rehearsal runs over 28:30:

- Slide 5: keep one U.S. incident and one Taiwan incident; cut the vendor example.
- Slide 9: say only `risk -> control -> test -> fix`; skip the detailed document list.
- Slides 13-16: speak only the first sentence plus one risk per scale.
- Slide 18 and 19: keep the contrast; cut the detailed tool names.
- Never cut slides 6, 17, 20, 21, or 22.

### 深度補充 / 排練理解

最後一頁要收束，不要再開新框架。它只要讓觀眾記住：先把安全做進產品，法規文件才會自然長出來。

這裡可以回到三個 readiness questions：我們知道產品邊界嗎？我們能證明風險怎麼被測試和處理嗎？漏洞進來時，我們修得動、證明得了、追得回去嗎？

成熟團隊不是文件最多，而是每一個 risk 都知道如何 prove、repair、track。這也呼應 Secure by Design 和 QMS 的方向：資安責任要前移到產品設計與製造商，而不是 audit 前才補文件。

結尾要停住。說完 trust-before-audit principle 之後，不要再加技術點。

### 頁面訊息 / 這頁任務
結論很清楚：成熟團隊不是文件最多，而是每個 risk 都能 prove、repair、track。

### 觀眾視角：一般民眾

可能問題：最後我該記住什麼？

回答：

**醫療 AI 不是只要準，而是要能被信任、被修復、被追蹤。**

### 觀眾視角：軟體公司

可能問題：這些東西有商業價值嗎？還是只是成本？

回答：

有價值。醫院採購、法規送審、資安稽核、客戶信任都會問同一件事：

**你出事時修得動嗎？你能證明你修好了嗎？**

### 觀眾視角：資安工程師

可能問題：Secure-by-design 要落在哪裡？

回答：

落在四個日常動作：

- threat model during architecture。
- SBOM as build artifact。
- testing as release gate。
- Patch SLA as finding governance。

這和 deck 的最後一頁完全一致。

### 趨勢與因應 / 可補充脈絡

CISA Secure by Design 的方向是把資安責任前移到軟體製造商與設計階段，不是把所有風險丟給使用者。[S18] HSCC 2026 AI supply chain guide 也顯示醫療 AI 未來會更要求 third-party dependency transparency、data lineage、model auditability、post-deployment monitoring。[S16]

因應：把 security 變成 QMS 的一部分，而不是 audit 前才補的文件。

## 這份 Deck 最容易被問倒的 8 個問題

### 1. FDA 2026 Guidance 是硬法規嗎？

回答：它是 FDA guidance，不等同法律條文，但反映 FDA 對 premarket cybersecurity documentation 與 Section 524B 的 current thinking。真正要看產品路徑、device classification、submission type 與是否屬 cyber device。[S1][S2]

### 2. 15 天 Patch SLA 是 FDA 要求嗎？

回答：不是。那是建議的 operating model。FDA 談的是上市後 updates / patches、合理時間、SBOM、CVD、device changes 的 cybersecurity impact。[S2]

### 3. AI model 準確率很高，為什麼還要資安？

回答：因為醫院買的不是單一模型，而是完整 workflow。模型準，不代表資料來源、viewer、API、update channel、log、patch process 都可信。

### 4. 沒有 LLM，OWASP LLM Top 10 還 relevant 嗎？

回答：Prompt injection 不一定 relevant，但 supply chain、data poisoning、model integrity、insecure output handling 的治理邏輯仍然 relevant。使用 OWASP 時要先看產品是否真的有 LLM 或 agentic workflow，不要硬套。[S13]

### 5. 用第三方 viewer / open source 元件，責任算誰的？

回答：法律責任要依合約與產品聲明判斷，但產品風險不能外包。只要元件進到你的產品或部署流程，就要進 SBOM、vulnerability management、patch process。

### 6. CVSS 低就可以慢慢修嗎？

回答：不一定。醫療 AI 要把 clinical impact、availability、integrity、exploitability、KEV status、customer exposure 一起看。

### 7. 小團隊做不到 QMS-grade evidence 怎麼辦？

回答：先做 30 / 60 / 90，不要一開始追求完美。Day 30 visibility，Day 60 workflow，Day 90 repair evidence。

### 8. 未來最大趨勢是什麼？

回答：三個方向：

**AI supply chain transparency、postmarket continuous monitoring、cybersecurity inside QMS。**

## Sources

- [S1] FDA, `Cybersecurity in Medical Devices: Quality Management System Considerations and Content of Premarket Submissions`, Final Guidance, February 2026: <https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-management-system-considerations-and-content-premarket>
- [S2] FDA, `Cybersecurity in Medical Devices Frequently Asked Questions (FAQs)`: <https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity-medical-devices-frequently-asked-questions-faqs>
- [S3] FDA, `Artificial Intelligence-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations`, Draft Guidance, January 2025: <https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing>
- [S4] FDA, `Artificial Intelligence-Enabled Medical Devices`: <https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices>
- [S5] FDA, `Marketing Submission Recommendations for a Predetermined Change Control Plan for Artificial Intelligence-Enabled Device Software Functions`, Final Guidance, August 2025: <https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence>
- [S6] TFDA, 2025-08-14 announcement revising AI/ML CADe / CADx medical device registration technical guidance and publishing independent performance assessment FAQ: <https://www.fda.gov.tw/tc/siteListContent.aspx?id=49448&sid=310>
- [S7] TFDA, `115年度第1次醫療器材法規及管理溝通討論會議` materials, 2026-03-17: <https://www.fda.gov.tw/tc/includes/GetFile.ashx?id=f639107213340396020&type=1>
- [S8] NIST, `The NIST Cybersecurity Framework (CSF) 2.0`: <https://www.nist.gov/publications/nist-cybersecurity-framework-csf-20>
- [S9] NIST, `NIST AI RMF Playbook`: <https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook>
- [S10] AHA, `AHA Survey: Change Healthcare Cyberattack Significantly Disrupts Patient Care, Hospitals' Finances`: <https://www.aha.org/2024-03-15-aha-survey-change-healthcare-cyberattack-significantly-disrupts-patient-care-hospitals-finances>
- [S11] AHA, `FBI: Health care was top target for ransomware, other cyberthreats in 2025`: <https://www.aha.org/news/headline/2026-04-10-fbi-health-care-was-top-target-ransomware-other-cyberthreats-2025>
- [S12] FDA, `Cybersecurity Vulnerabilities with Certain Patient Monitors from Contec and Epsimed: FDA Safety Communication`: <https://www.fda.gov/medical-devices/safety-communications/cybersecurity-vulnerabilities-certain-patient-monitors-contec-and-epsimed-fda-safety-communication>
- [S13] OWASP, `OWASP Top 10 for Large Language Model Applications`: <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- [S14] NVD, `CVE-2025-35975`: <https://nvd.nist.gov/vuln/detail/cve-2025-35975>
- [S15] NHS England, `Synnovis cyber incident`: <https://www.england.nhs.uk/synnovis-cyber-incident/>
- [S16] AHA, `HSCC releases guide on third-party AI risk, supply chain transparency`: <https://www.aha.org/news/headline/2026-04-15-hscc-releases-guide-third-party-ai-risk-supply-chain-transparency>
- [S17] CISA, `Known Exploited Vulnerabilities Catalog`: <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>
- [S18] CISA, `Secure by Design`: <https://www.cisa.gov/securebydesign>
