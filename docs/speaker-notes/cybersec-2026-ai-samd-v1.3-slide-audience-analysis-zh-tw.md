# CYBERSEC 2026 AI SaMD v1.3 Slide Audience Analysis

Prepared: 2026-04-21

Deck basis: `outputs/deck/cybersec-2026-ai-samd-cybersecurity-in-practice-v1.3.pdf`

Companion files:

- `docs/speaker-notes/cybersec-2026-ai-samd-audience-qa-v1-zh-tw.md`
- `docs/speaker-notes/cybersec-2026-ai-samd-slide-deep-notes-v2-en.md`

## 使用方式

這份文件把 `AI SaMD Cybersecurity In Practice - v1.3` deck 當成逐頁 rehearsal artifact。它不取代既有的 30 題 audience Q&A；兩份文件分工如下：

- `audience-qa-v1-zh-tw.md`：跨全場的 30 題問答，用於會後 Q&A 與主持人追問。
- 本文件：逐頁判斷每張投影片在三種觀眾心中會冒出的問題，以及上台時如何順手接住。

三種觀眾視角：

- **一般民眾**：會問「這跟病人安全有什麼關係？」
- **軟體公司**：會問「我要怎麼做、成本多少、會不會卡上市？」
- **資安工程師**：會問「你這套證據夠不夠硬？」

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

### 頁面訊息

這頁建立定位：這不是一般 AI talk，而是把 FDA Section 524B 作為醫療 AI 產品資安與治理的入口。

### 一般民眾

可能問題：這是不是太法規、太技術？跟我看病有什麼關係？

回答：

**這場不是在講駭客，而是在講當 AI 進入醫院後，病人能不能相信結果、醫師能不能拿到結果、系統出事能不能修回來。**

### 軟體公司

可能問題：我們還不是 FDA 送審階段，現在需要管 524B 嗎？

回答：

不要把 524B 只講成法規門檻，而要講成產品設計語言。越早把 SBOM、漏洞處理、patch、CVD、risk decision 放進開發流程，越不會在上市前才補文件。

### 資安工程師

可能問題：Section 524B 對我實際工作代表什麼？

回答：

直接對應四件事：**威脅模型、SBOM、漏洞監測、修補證據。** 不是寫一份 policy，而是把 evidence chain 做出來。

### 趨勢與因應

FDA AI-enabled medical device list 逐步增加透明度，也提到未來會探索標示 foundation model / LLM-based functionality 的方法。[S4]

因應：第 1 頁可在口語副標加一句：

**From model performance to product accountability.**

## Slide 2｜Disclaimer

### 頁面訊息

這頁是標準 CYBERSEC 免責聲明。用途是避免觀眾把演講內容誤認為醫療建議、法律意見或官方立場。

### 一般民眾

可能問題：所以這些內容是不是不能當成醫療建議？

回答：

**這不是醫療建議，也不是法律意見；這是讓大家理解 AI 醫療產品為什麼需要資安證據與治理流程。**

### 軟體公司

可能問題：我們可以直接把這份簡報當作內部 SOP 或送審文件嗎？

回答：

不行。這份 deck 可以當架構參考，但實際 SOP 要依產品 intended use、架構、風險分級、上市市場、QMS 與 submission pathway 調整。

### 資安工程師

可能問題：Patch SLA、72 小時 KEV assessment、15 天 advisory 是不是 FDA 硬性要求？

回答：

不是。這些是 operating model。FDA FAQ 談的是 postmarket updates / patches、SBOM、變更影響 cybersecurity 時的文件需求；實際期限要由產品風險、臨床影響、客戶環境與 QMS 決策定義。[S2]

### 趨勢與因應

AI 醫療、資安與法規的交界越來越高風險。未來簡報最好標註資料查核日期與法規可能更新。

因應：disclaimer 口頭補一句：

**Regulatory references verified as of 2026-04.**

## Slide 3｜Table of Contents

### 頁面訊息

四段主軸很清楚：Boundary -> Evidence -> Decision -> Repair Proof。這是整份簡報的骨架。

### 一般民眾

可能問題：Boundary、Evidence、Decision、Repair Proof 聽起來很抽象。

回答：

**先知道產品管到哪裡，再知道風險在哪裡；風險看得見，才有證據；證據能被決策，系統才修得回來。**

### 軟體公司

可能問題：這四段可以變成產品開發 roadmap 嗎？

回答：

可以，直接對成四個里程碑：

1. **Boundary**：產品邊界、角色、資料流。
2. **Evidence**：SBOM、threat model、測試紀錄。
3. **Decision**：triage、risk acceptance、patch plan。
4. **Repair Proof**：修補、重測、release history。

### 資安工程師

可能問題：Decision 是誰決策？資安、法規，還是臨床？

回答：

應該是 cross-functional decision：Product Security、Engineering、Regulatory、Clinical Safety、Customer Success 一起進 risk register。沒有 owner 的 decision，就是口頭承諾。

### 趨勢與因應

NIST CSF 2.0 把 Govern 加入核心功能，和 Identify、Protect、Detect、Respond、Recover 並列；NIST AI RMF 則用 Govern、Map、Measure、Manage 管 AI risk。[S8][S9]

因應：這頁可在口語中建立 mapping：

**Boundary = Identify / Map；Evidence = Measure；Decision = Govern / Manage；Repair Proof = Respond / Recover。**

## Slide 4｜You Are Not Selling a Model

### 頁面訊息

這是關鍵頁。它把模型準確率和醫院真正購買的產品責任切開：醫院買的是 intended use、human-in-the-loop、patch、incident reporting，不只是模型。

### 一般民眾

可能問題：AI 不是醫師輔助工具嗎？為什麼講得像一整套系統？

回答：

AI 在醫院不是單獨存在。它要吃資料、產生輸出、給醫師看、接醫院系統、更新版本。任何一段出問題，都會影響醫師能不能安全使用它。

### 軟體公司

可能問題：我們先賣 model API，其他交給醫院整合，這樣可以嗎？

回答：

可以作為商業策略，但責任不能模糊。你要清楚定義：

- intended use 是什麼。
- 使用者是誰。
- AI 結果是否需要人工確認。
- API failure 時誰負責。
- patch / incident 如何通知客戶。

TFDA 2025 AI/ML CADe / CADx 指引要求業者依產品功能、平台、架構、預期用途、使用限制、使用情境、判讀流程與輸出結果解讀等內容準備查驗登記資料。[S6]

### 資安工程師

可能問題：Docker、WSL2、Node.js、Python、DCMTK 都要進 SBOM 嗎？

回答：

如果它們是產品交付、部署、執行或維護所依賴的元件，就應納入 asset inventory / SBOM / vulnerability management。FDA FAQ 也明確提到 SBOM 要涵蓋 commercial、open-source、off-the-shelf components。[S2]

### 趨勢與因應

AI 醫材會從 model-centric 轉向 workflow-centric。

因應：口語補一張產品責任鏈：

**Model -> Viewer -> API -> PACS/DICOM -> Hospital workflow -> Patch / Incident route。**

## Slide 5｜AI Is Becoming Infrastructure

### 頁面訊息

這頁把 AI 拆成 Model Layer、Runtime Layer、Infrastructure Layer，並用 Change Healthcare 事件說明第三方基礎設施失效會擴散到臨床。

### 一般民眾

可能問題：一家公司的系統被攻擊，為什麼會影響醫院看診？

回答：

Change Healthcare 事件就是例子。AHA 對近 1,000 家醫院的調查顯示，74% 回報 direct patient care impact，94% 回報 financial impact。[S10]

重點句：

**醫療不是單一醫院在運作，而是一條供應鏈。供應鏈斷掉，病人的流程就會被拖慢。**

### 軟體公司

可能問題：我們只是 AI vendor，也會被當成醫療基礎設施風險嗎？

回答：

會，尤其是產品碰到資料流、更新機制、身份權限、醫院網路、PACS/DICOM。你的產品如果出問題會卡住臨床流程，就不是單純 SaaS bug。

### 資安工程師

可能問題：這三層要怎麼落控制？

回答：

- Model layer：model provenance、hash / signature、version pinning。
- Runtime layer：container hardening、secret management、API auth、logging。
- Infrastructure layer：IAM、network segmentation、SBOM、update channel、incident route。

### 趨勢與因應

AHA 引用 FBI 2025 Internet Crime Report 指出，health care and public health 是 2025 年 cyberthreats top-targeted sector，包含 460 起 ransomware attacks 與 182 起 data breaches。[S11]

因應：AI SaMD 公司要把供應鏈韌性變成產品能力：deployment guide、downtime fallback、incident contact、customer advisory template。

## Slide 6｜Risk Grows With Architecture

### 頁面訊息

這頁很強：同一個 AI model，因產品邊界不同，資安責任完全不同。Scale 1 是 model；Scale 4 已經是 connected medical system。

### 一般民眾

可能問題：為什麼加一個 viewer 或資料庫，風險就變大？

回答：

**每多一個功能，就多一扇門。門越多，就越需要門鎖、監視器、逃生路線和修理流程。**

### 軟體公司

可能問題：什麼時候我們的責任會從 AI 模型變成醫療系統？

回答：

當你提供 viewer、database、API、update channel、hospital integration、PACS/DICOM workflow 時，就開始跨出模型責任。FDA 2026 guidance 的目標是促進 device design、labeling 與 premarket cybersecurity documentation，並處理有 cybersecurity risk 的 devices。[S1]

### 資安工程師

可能問題：這張 scale diagram 要怎麼變成 threat model？

回答：

把每個 scale 變成 control baseline：

- Scale 1：model artifact integrity。
- Scale 2：file parser / viewer fuzzing。
- Scale 3：IAM、API auth、audit log、backup。
- Scale 4：VLAN、default-deny firewall、DICOM-TLS、downtime fallback。

### 趨勢與因應

FDA 2026 guidance 的趨勢是把 cybersecurity 放入 QMS 語言，而不是最後補一份附錄。[S1]

因應：每次產品架構改版，都要同步更新 threat model、SBOM、risk assessment、deployment guide。

## Slide 7｜Evidence, Not Slogans

### 頁面訊息

這頁是全 deck 的靈魂之一：不要說「我們很安全」，要拿出 Risk -> Control -> Test -> Fix & Prove 的證據。

### 一般民眾

可能問題：我要怎麼知道廠商不是只是在說好聽話？

回答：

**可信任不是靠口號，而是靠可檢查的證據。就像健康檢查不能只說我很健康，要有檢查結果。**

### 軟體公司

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

### 資安工程師

可能問題：STRIDE mapping 夠嗎？

回答：

STRIDE 是起點，不是終點。AI SaMD 應加上：

- clinical abuse cases。
- model tampering scenario。
- data poisoning scenario。
- malicious DICOM file scenario。
- update channel compromise。
- hospital LAN lateral movement。

### 趨勢與因應

Contec / Epsimed patient monitor 案例顯示，降低 unacceptable risk 有時不是加功能，而是拿掉功能；FDA 說該 patch 完全移除 affected devices 的 networking functionality，使裝置只能 local monitoring，且安裝需要專業人員。[S12]

因應：把 **feature removal / degraded mode** 納入 risk mitigation options。

## Slide 8｜Model, Governance, Stack

### 頁面訊息

這頁把可信任 AI 拆成三個學科：Model Evidence、Governance Language、AI Stack Security。

### 一般民眾

可能問題：AI 安全到底是模型準、公司管得好，還是系統不被駭？

回答：

答案是三個都要：

**模型要有證據，組織要能治理，系統要能防護。少一個都不夠。**

### 軟體公司

可能問題：這三塊誰負責？

回答：

建議分工：

- Model Evidence：ML / Clinical / Regulatory。
- Governance Language：QMS / Product / Risk owner。
- AI Stack Security：Security / DevOps / SRE / Engineering。

NIST CSF 2.0 的 Govern 功能涵蓋 strategy、policy、roles、responsibilities、supply chain risk management；NIST AI RMF 則用 Govern、Map、Measure、Manage 管理 AI risk。[S8][S9]

### 資安工程師

可能問題：OWASP LLM Top 10 跟醫療影像 AI 有關嗎？

回答：

如果產品沒有 LLM，不要硬套 prompt injection；但 supply chain、data / model poisoning、insecure output handling 的邏輯仍然 relevant。OWASP LLM Top 10 屬於 broader GenAI security work，適合用來提醒 LLM 或 agentic workflow 的風險邊界。[S13]

### 趨勢與因應

未來 AI security 會從 model security 走向 **AI system security + AI governance**。

因應：在公司內建立一張 crosswalk：FDA / TFDA / NIST CSF / NIST AI RMF / OWASP / internal QMS。

## Slide 9｜Scale 1-2: Model to Viewer

### 頁面訊息

這頁提醒：model artifact 是資產，viewer 是 attack surface。DICOM viewer 不是被動外殼，而是真實攻擊面。

### 一般民眾

可能問題：只是打開一個醫療影像檔，也可能被攻擊？

回答：

是。NVD 的 CVE-2025-35975 顯示 MicroDicom DICOM Viewer 有 out-of-bounds write 漏洞，使用者開啟惡意 DCM file 可能導致任意程式碼執行。[S14]

### 軟體公司

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

### 資安工程師

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

### 趨勢與因應

未來醫療 AI 的攻擊面會越來越偏向周邊元件：viewer、parser、plugin、update channel、container image。

因應：不要只測 model；要把 DICOM parser fuzzing、file upload abuse cases、viewer patch cadence 放進 release gate。

## Slide 10｜Scale 3-4: Platform to Connected Medical System

### 頁面訊息

這頁把風險推到平台與醫院網路：Identity、MFA/RBAC、API authorization、audit log、backup/restore、VLAN、firewall、DICOM-TLS、downtime fallback。

### 一般民眾

可能問題：供應商被駭，真的會讓醫院停擺那麼久？

回答：

Synnovis 事件就是例子。NHS England 說 Synnovis 2024 年 6 月遭 ransomware attack，造成超過 11,000 個 outpatient 與 elective procedure appointments 延誤；服務到 2024 年 12 月才完全恢復，且 2024 年 6 月 20 日攻擊者公布竊取資料。[S15]

### 軟體公司

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

### 資安工程師

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

### 趨勢與因應

HSCC 2026 第三方 AI 風險與供應鏈透明度指南把 data lineage、model auditability、embedded third-party dependencies、post-deployment monitoring 列為醫療 AI 供應鏈最佳實務。[S16]

因應：對醫院客戶提供 AI supply chain disclosure package，而不是只提供產品簡介。

## Slide 11｜Cyber Safety Is Patient Safety

### 頁面訊息

這頁把 Availability、Integrity、Repairability 轉成病人安全語言。

### 一般民眾

可能問題：資安怎麼會等於病人安全？

回答：

三句話即可：

- **Availability**：醫師需要時拿得到結果。
- **Integrity**：醫師拿到的是可信結果。
- **Repairability**：出事後可以安全恢復。

### 軟體公司

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

### 資安工程師

可能問題：這不是 CIA triad 嗎？

回答：

是，但醫療版要重新定義：

**Confidentiality 是隱私，Integrity 是診斷可信度，Availability 是臨床連續性，Repairability 是病人安全恢復能力。**

### 趨勢與因應

醫療資安事件的評估會越來越從「資料有沒有外洩」轉向「照護有沒有中斷」。Change Healthcare 和 Synnovis 都證明 disruption 本身就是病人安全與營運風險。[S10][S15]

因應：security severity scoring 要加入 clinical impact，不要只看 CVSS。

## Slide 12｜Testing Portfolio

### 頁面訊息

這頁把測試從工具清單變成治理問題：每種測試回答不同 decision question。

### 一般民眾

可能問題：為什麼要這麼多測試？不能掃一次就好嗎？

回答：

不能。不同測試抓不同問題：

- SBOM / SCA：知道用了什麼。
- SAST：找開發階段可修問題。
- Fuzz：測異常輸入會不會打壞流程。
- Pen test：測真實攻擊鏈。
- Retest：證明修補有效。

### 軟體公司

可能問題：小公司要做到這些會不會太貴？

回答：

用 risk-based sequencing：

1. 先自動化 SBOM / SCA / SAST。
2. 對 DICOM / file parser 做 abuse cases。
3. 針對 release candidate 做外部 pen test。
4. 所有 high / critical finding 必須 retest。
5. evidence archive 進 QMS。

### 資安工程師

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

### 趨勢與因應

FDA 2026 guidance 已把 cybersecurity documentation 放進 premarket review 與 QMS 思維；CISA KEV 也成為漏洞優先級管理的重要輸入。[S1][S17]

因應：把 testing 變 release gate，而不是上市前外包一份報告。

## Slide 13｜Patch SLA: No Decision, No Governance

### 頁面訊息

這頁是另一個重點：patch 不是工程排程，而是治理決策。Intake -> Triage -> Decision -> Action。

### 一般民眾

可能問題：發現漏洞為什麼不馬上修？拖什麼？

回答：

醫療產品不能像一般 app 一樣亂推更新，因為 patch 可能影響：

- AI model accuracy。
- DICOM structure。
- system stability。
- clinical workflow。
- 醫院部署環境。

所以要先 triage，再決策，再修，再重測。

### 軟體公司

可能問題：Critical 15 天、30 天 mitigation plan 是不是可以寫進 SLA？

回答：

可以作為內部 operating model，但不要宣稱是 FDA 硬性規定。FDA FAQ 的說法是要有 postmarket updates / patches 與相關 lifecycle 計畫；實際時間要依風險定義。[S2]

### 資安工程師

可能問題：72 小時 CISA KEV applicability assessment 合理嗎？

回答：

合理，甚至建議做。CISA KEV 是已知遭實際利用漏洞的權威輸入，可作為 vulnerability management prioritization framework 的一部分。[S17]

但醫療產品要加一層 safety override：如果 patch 會影響臨床安全，就先做 compensating control，再排正式修補與驗證。

### 趨勢與因應

漏洞管理正在從 CVSS 高低走向「是否已被利用 + 是否影響臨床」。Contec / Epsimed 案例顯示，patch 甚至可能移除 networking functionality，讓裝置只保留 local monitoring。[S12]

因應：Patch SLA 裡要同時有 security impact、clinical impact、customer communication。

## Slide 14｜Small Team: 30 / 60 / 90

### 頁面訊息

這頁很實用。它把小團隊如何開始做 evidence loop 具體化。

### 一般民眾

可能問題：小公司真的做得到嗎？

回答：

做得到，但不是一開始就做到完美。重點是 90 天內從口頭記憶變成可重複證據。

### 軟體公司

可能問題：30 / 60 / 90 每階段到底要交什麼？

回答：

- **Day 30**：SBOM、data flow diagram、intended use、user roles、component inventory、known vulnerabilities list。
- **Day 60**：STRIDE workshop、CI security gates、finding triage workflow、customer security note template、CISA KEV cross-reference。
- **Day 90**：black-box pen test、internal vulnerability scan、Patch SLA drill、CVD process、retest records、release history。

### 資安工程師

可能問題：如果資源不夠，哪個先做？

回答：

先做 visibility，再做 governance：

1. 先知道自己有什麼。
2. 再知道風險在哪裡。
3. 再把風險變成 decision。
4. 最後留下 repair evidence。

### 趨勢與因應

TFDA 2026 說明資料提到，AI 醫材可透過獨立性能評估提高驗證效率與靈活度，也鼓勵採用 PCCP 以降低法遵成本。[S7] FDA PCCP guidance 也強調 AI-enabled devices 可在事先規劃的變更範圍內持續改善，同時維持安全與有效性。[S5]

因應：小團隊不要追求一次做滿，要先建立第一個 evidence loop。

## Slide 15｜Build Trust Before the Audit

### 頁面訊息

結論很清楚：成熟團隊不是文件最多，而是每個 risk 都能 prove、repair、track。

### 一般民眾

可能問題：最後我該記住什麼？

回答：

**醫療 AI 不是只要準，而是要能被信任、被修復、被追蹤。**

### 軟體公司

可能問題：這些東西有商業價值嗎？還是只是成本？

回答：

有價值。醫院採購、法規送審、資安稽核、客戶信任都會問同一件事：

**你出事時修得動嗎？你能證明你修好了嗎？**

### 資安工程師

可能問題：Secure-by-design 要落在哪裡？

回答：

落在四個日常動作：

- threat model during architecture。
- SBOM as build artifact。
- testing as release gate。
- Patch SLA as finding governance。

這和 deck 的最後一頁完全一致。

### 趨勢與因應

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
