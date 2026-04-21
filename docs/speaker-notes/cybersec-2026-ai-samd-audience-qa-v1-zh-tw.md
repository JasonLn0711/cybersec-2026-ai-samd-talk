# CYBERSEC 2026 AI SaMD Audience Q&A v1

Date: 2026-04-21
Language: Taiwan Traditional Chinese
Deck basis: `outputs/deck/cybersec-2026-ai-samd-cybersecurity-in-practice-v1.3.pdf`
Speaker-note companion: `docs/speaker-notes/cybersec-2026-ai-samd-slide-deep-notes-v2-en.md`
Slide-by-slide companion: `docs/speaker-notes/cybersec-2026-ai-samd-v1.3-slide-audience-analysis-zh-tw.md`

## 查核基準

這份 Q&A 把 `AI SaMD Cybersecurity In Practice - v1.3` 當成三種觀眾來看：一般民眾、軟體公司、資安工程師。回答目標不是背法規，而是讓上台問答可以把同一個主軸講清楚：

**AI 軟體醫材不是只保護模型，而是建立一套可定義邊界、可產生證據、可治理 finding、可修補、可稽核的產品信任系統。**

查核後的基準如下：

- FDA 醫療器材資安主文件目前應以 **February 2026 Final Guidance** 為主；它取代 June 2025 版本，並把 cybersecurity 放進 Quality Management System Considerations 的語言裡。
- FD&C Act Section 524B 的重點包含上市前提交上市後漏洞監測與處理計畫、CVD、資安設計與維護、上市後更新與修補，以及 SBOM。FDA FAQ 也說明 eSTAR cybersecurity 欄位不完整會造成 Technical Screening hold。
- FDA `Artificial Intelligence-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations` 是 **January 2025 Draft Guidance**，不是 final；它可用來說明 TPLC 方向，但上台不要說成正式最終要求。
- FDA AI-enabled device PCCP guidance 是 **August 2025 Final Guidance**；可用來說明 AI 醫材如何預先定義 planned modifications、validation / implementation methodology 與 impact assessment。
- TFDA 在 2025-08-14 公告修正 AI/ML CADe / CADx 醫療器材查驗登記技術指引；台灣語境應把產品宣稱、適用範圍、使用情境、安全與效能驗證資料講清楚。
- 醫療資安威脅不是抽象議題。AHA 於 2026-04-10 引用 FBI 2025 資料指出 health care and public health 是 2025 年被 ransomware 與其他 cyberthreats 攻擊最多的 sector，包含 460 起 ransomware attacks 與 182 起 data breaches。
- Change Healthcare、Synnovis、Contec/Epsimed、MicroDicom CVE-2025-35975 都可以作為公開案例，但不要講成產品或醫院內部攻擊教學。

## 一般民眾視角：10 題 + 回答

### 1. AI 醫療系統被駭，真的會影響病人安全嗎？

會。原因不是 AI 會「自己變壞」，而是 AI 醫療產品會接到影像、資料、帳號、報告流程、醫院網路和醫師決策。如果這些環節被攻擊，可能造成檢查延誤、結果不可信，或醫師拿不到需要的資訊。

你可以這樣回答：醫療 AI 的資安不是 IT 部門的旁支，而是醫療流程的一部分。Change Healthcare 事件讓許多醫院回報財務與照護流程受影響；Synnovis 事件也讓英國 NHS 病理服務長時間中斷。這些案例提醒我們，資安事故最後可能變成病人等待、醫護改用人工流程、或服務恢復困難。

### 2. 醫師不是最後會看結果嗎？為什麼 AI 被攻擊還危險？

醫師會判斷，但醫師看到的是系統提供的資料。如果影像檔、DICOM viewer、模型版本、報告流程、資料來源或權限被動手腳，醫師可能是在錯誤前提下判斷。

所以 deck 裡的 `Cyber Safety Is Patient Safety` 不是口號。它的意思是：醫療判斷需要可信的輸入、穩定的系統和可追蹤的流程。醫師不是被 AI 取代，但醫師需要一個沒有被污染、沒有被中斷、可以查證的工作環境。

### 3. 一般病人要怎麼知道 AI 醫療產品可信？

一般病人不可能去讀原始碼，所以重點不是自己判斷模型，而是問醫療院所與廠商是否能說清楚：這個產品用在哪裡、不能用在哪裡、結果由誰確認、出錯時怎麼通報、多久可以修補、修完怎麼確認。

可以把它想成：可信任的 AI 醫材，不只是 demo 很漂亮，而是有產品邊界、有驗證資料、有事件處理流程、有修補紀錄。病人不需要懂每個技術細節，但應該期待醫院與廠商能拿得出這些證據。

### 4. 強化資安會不會讓看病變慢？

好的資安不應該讓醫療變慢，而是讓醫療在出事時不要整個停住。真正成熟的設計會包含備援、人工 fallback、事件通報、修補流程、權限管理、日誌和復原演練。

平常看起來像是多做一些準備；出事時，它就是讓醫院能繼續照顧病人的安全網。資安的目標不是讓每個步驟更麻煩，而是讓醫療服務在受到攻擊、更新失敗或外部供應商中斷時，還有路可以走。

### 5. 如果 AI 醫療產品出問題，責任是醫院、公司，還是醫師？

三方都有責任，但責任範圍不同。公司要證明產品設計、更新、漏洞處理、測試和驗證是可靠的；醫院端要確保部署環境、網路隔離、帳號權限、備援流程和使用管理；醫師則是在臨床流程中做專業判斷。

這就是為什麼 deck 一開始要談產品邊界。邊界畫清楚，才知道哪些事情由廠商負責、哪些事情由醫院端負責、哪些事情需要醫師確認。邊界不清楚，出事時就會變成互相猜責任。

### 6. SBOM 是什麼？一般民眾為什麼要在意？

SBOM 可以把它想成「軟體成分表」。就像食品有成分標示，軟體醫材也應該知道自己用了哪些商用、開源、現成軟體元件。

這跟病人有關，因為醫療 AI 不只是一個模型。它可能包含 Python 套件、Node.js、Docker、DICOM viewer、資料庫、API、作業系統套件、更新機制。任何一個元件有漏洞，都可能影響整個產品。SBOM 讓廠商知道自己要追蹤什麼，也讓醫院端在漏洞出現時能快速判斷是否受影響。

### 7. Patch SLA 是什麼？為什麼簡報特別講？

Patch SLA 是把「發現漏洞後怎麼處理」變成明確流程。它回答：誰接收通報？誰判斷嚴重度？多久內要做決策？是修補、暫時控制、延後、還是不適用？修完之後如何重測與留下證據？

上台要補一句：Patch SLA 不是 FDA 原文裡的固定法律名詞，而是把 FDA 524B 的漏洞管理、CVD、更新與修補要求轉成公司可以執行的治理模型。醫療產品不能只說「我們會修」，要能證明什麼時候修、怎麼修、修完如何確認安全。

### 8. 為什麼說「你賣的不是模型」？

因為醫院買的不是一個 `.pt`、`.onnx` 或模型 demo，而是一套會進入臨床流程的產品。它包含影像匯入、viewer、PACS/DICOM、帳號權限、資料暫存、日誌、更新、事件通報和備援。

MicroDicom CVE-2025-35975 是很好的提醒：風險不一定在 AI 模型本身，也可能在 DICOM viewer 或檔案解析器。對病人與醫師來說，他們需要可信任的是整個系統，不只是模型分數。

### 9. FDA 是美國規範，台灣為什麼要在意？

如果產品要進美國市場，當然要在意。就算目前只看台灣市場，FDA、NIST、HSCC 這些文件也代表國際醫材與醫療資安審查越來越重視上市後風險管理、供應鏈透明、修補能力和證據保存。

台灣也不是空白。TFDA 已經有 AI/ML CADe / CADx 醫療器材查驗登記技術指引，而且 2025 年有修正。台灣團隊要面對的是同一個方向：產品宣稱、適用範圍、使用情境、安全與效能驗證資料都要講清楚。

### 10. 一般民眾聽完最該記住什麼？

記住這一句就好：**醫療 AI 不是只要準，而是要能被信任、被修復、被追蹤。**

真正成熟的 AI 醫材，不是只在展示時看起來很聰明，而是在漏洞、更新、資料異常、醫院斷線或供應商中斷時，仍然有清楚流程與證據可以處理。

## 軟體公司視角：10 題 + 回答

### 1. 小團隊要做到這整套，最小可行版本是什麼？

最小可行版本不是買一堆工具，而是建立第一輪 evidence loop。Day 30 先把產品看得見：intended use、user roles、data flow、component inventory、SBOM、known vulnerabilities。Day 60 讓風險進流程：STRIDE workshop、CI security gate、finding triage、customer security note template。Day 90 補外部驗證與修復證據：vulnerability scan、black-box pen test、Patch SLA drill、CVD process、retest record。

要特別說清楚：30 / 60 / 90 是 adoption scaffold，不是 FDA 法定要求。它的價值是讓八人小團隊也能從口頭記憶，走向可重複、可稽核的證據循環。

### 2. 這會不會拖慢上市？

會增加前期工作，但通常比上市前最後一刻補洞便宜很多。真正會拖慢上市的不是資安流程，而是送審或客戶稽核前才發現沒有 SBOM、沒有漏洞處理流程、沒有模型版本證據、沒有 patch decision log。

FDA 524B 已經把 postmarket vulnerability management plan、CVD、updates / patches、SBOM 放進 premarket submission 的期待裡。越早把它做進工程與 QMS，越少最後重工。

### 3. 我們應該先做合規文件，還是先做產品安全？

先做產品安全，再讓文件從實際流程長出來。文件如果只是送審前補出來，審查、客戶稽核、事件復盤時都會露餡。

比較好的順序是：先畫 product boundary 和 data flow，再做 threat model 和 risk assessment，接著把 control、test、finding decision、patch / retest record 串起來。這樣文件不是作文，而是工程證據的不同視角。

### 4. 這套東西應該由哪個團隊負責？

不能只丟給資安，也不能只丟給法規。建議 ownership 放在 Product Security、QMS、Regulatory、Engineering、Clinical / Product 的交界。

工程負責實作和證據，資安負責威脅模型、測試策略和漏洞治理，法規負責查驗登記與 submission 對應，QMS 負責品質系統與紀錄控制，產品/臨床負責 intended use、user role、workflow boundary 與使用風險。AI SaMD 的資安不是單一部門英雄主義，而是跨職能責任鏈。

### 5. Section 524B 什麼情況下會影響我們？

如果你的醫材包含由 sponsor 驗證、安裝或授權的軟體，能連網，而且具有可能受 cyber threats 影響的技術特性，就要認真檢查是否落入 FDA 所說的 cyber device。

一旦落入，510(k)、PMA、De Novo、HDE 等 premarket submissions 就需要處理 524B 相關資料。上台不要把這講成「所有軟體都一樣」，而是講成：只要你的 AI 醫材跨到連網、更新、資料交換或醫院端部署，524B 思維就很可能成為產品治理基本功。

### 6. Patch SLA 要設 15 天合理嗎？

15 天可以當作 critical finding 的內部 operating target，但不要講成 FDA 法定硬期限。FDA 的語言是 postmarket updates / patches within a reasonable time；15 天 advisory / compensating controls、30 天 mitigation plan 是公司把要求轉成可執行治理節奏的做法。

重點不是數字本身，而是你能不能證明：有 intake、applicability assessment、severity、owner、decision、action、retest、archive。沒有 decision，就沒有治理；沒有證據，就沒有信任。

### 7. 如果資安修補會影響模型準確率或醫療安全，怎麼辦？

不能用一般 SaaS 的邏輯硬推。AI 醫材需要 safety override：先判斷 patch 是否影響 model accuracy、DICOM structure、clinical workflow、system stability 或已驗證的使用條件。

如果會影響，就要跑 regression test、clinical performance check，必要時先採 compensating control，例如網段限制、關閉高風險功能、加強監控或 customer advisory。FDA 的 PCCP final guidance 也支持 AI-enabled devices 預先規劃 planned modifications、驗證方法、實施方法與影響評估，讓變更不是臨時拍腦袋。

### 8. SBOM、CVD、Patch SLA 真的能變商業優勢嗎？

能，尤其是賣給醫院、醫療集團、保險、政府或跨國市場時。醫療買方會越來越問：你的 AI 供應鏈透明嗎？第三方元件可追蹤嗎？出事時誰通知？多久能判斷是否受影響？修補之後如何證明？

HSCC / AHA 2026 對 third-party AI risk 與 supply-chain transparency 的討論已經把 data lineage、model auditability、embedded third-party dependencies、post-deployment monitoring 拉到採購與風險治理層級。這代表資安證據會越來越像產品信任賣點，而不是只是成本。

### 9. AI 模型更新要怎麼管理，才不會每次都像重新送審？

先把更新分級：security patch、bug fix、threshold tuning、preprocessing change、model retraining、UI / labeling change、deployment config change。每一類更新要有 impact assessment：會不會影響 intended use、performance、clinical workflow、DICOM output、cybersecurity risk、labeling 或 user training。

PCCP 的精神是事先把可預期變更、驗證方法、實施方法和影響評估寫清楚。不是所有更新都不能做，而是更新要有邊界、有證據、有風險判斷。

### 10. 管理層最該看的 KPI 是什麼？

不要只看「掃出幾個漏洞」。建議看：SBOM coverage、critical vulnerability applicability assessment time、CISA KEV match response time、patch decision lead time、retest completion rate、unresolved high-risk findings、model version traceability、audit log completeness、backup / restore drill pass rate、customer advisory closure rate。

這些 KPI 比「我們很安全」更像董事會、醫院採購、QMS 和法規團隊聽得懂的治理語言。它們回答的是：公司是否知道自己有什麼、風險怎麼進流程、誰做決策、修補是否真的完成。

## 資安工程師視角：10 題 + 回答

### 1. Threat model 用 STRIDE 就夠了嗎？

STRIDE 適合當 baseline，但不應該是全部。AI SaMD 建議用 `STRIDE + architecture boundary + clinical workflow abuse cases + attack tree`。

原因是 scale 不同，攻擊面也不同：Scale 1 看 model artifact、hash、signature、training / validation context；Scale 2 看 viewer、parser、upload、cache、output interpretation；Scale 3 看 identity、API、database、audit log、backup；Scale 4 看 PACS/HIS、hospital LAN、update server、remote service、downtime fallback。Threat model workshop 的主圖應該先是產品邊界，而不是工具清單。

### 2. Model tampering detection 要做到什麼才算夠？

最小基線是 model artifact hash、signature、version pinning、release manifest、deployment allowlist、inference-time version logging。更成熟時再加入 signed container image、build provenance、model registry access control、runtime attestation、rollback record。

核心問題不是只防止模型被換掉，而是能回答：這一次 clinical output 是哪個 model、哪個 build、哪個 pipeline、哪個 input hash、哪個 deployment config 產生的？沒有這條鏈，事件調查與臨床信任都會斷掉。

### 3. SBOM 應該做 build-time 還是 runtime？

兩個都要。Build-time SBOM 回答「我們宣稱放進產品的是什麼」；runtime / deployment inventory 回答「醫院端實際跑的是什麼」。

AI SaMD 常有 Python packages、container base images、Node.js、DCMTK / DICOM libraries、viewer、database、CUDA / cuDNN、OS packages、third-party model 或 cloud service。只做 application SBOM 會漏掉底層與部署元件。FDA 524B 也明確把 commercial、open-source、off-the-shelf software components 納入 SBOM 要求。

### 4. DICOM parser fuzzing 要做到什麼程度？

至少要覆蓋 malformed DICOM、oversized file、invalid tag、nested sequence、compression edge cases、encoding mismatch、metadata abuse cases。若產品真的處理 DICOM，最好能有 coverage-guided fuzzing，並保留 crash triage、reproducer、fix commit、retest evidence。

MicroDicom CVE-2025-35975 是很好的警示：DICOM viewer 的 out-of-bounds write 可能導致 arbitrary code execution，CISA advisory 給出 CVSS v3.1 8.8。這代表 viewer 不是被動包裝，它本身就是攻擊面。

### 5. Risk scoring 用 CVSS 就可以嗎？

不夠。CVSS 可以描述技術嚴重度，但醫療場景還要加 clinical impact、patient safety severity、deployment exposure、exploitability、compensating controls、CISA KEV status、availability impact、data integrity impact、workflow interruption。

一個 CVSS 不高的 finding，如果會造成臨床流程中斷、AI output 不可信、或需要醫院端停用服務，仍然可能要升級處理。反過來，一個高 CVSS finding 如果在該部署完全不適用，也要能留下 not applicable rationale，而不是口頭說明。

### 6. Prompt injection 跟這份 deck 有關嗎？

要看產品有沒有 LLM 或 agentic workflow。如果只是傳統影像 classifier，主要風險通常不是 prompt injection，而是 model tampering、data poisoning、DICOM parser、supply chain、runtime exploit、PACS/HIS integration。

如果產品有 LLM 用於報告生成、客服、triage 或 agent action，就要把 LLM output 當成不可信輸入，不可以讓它直接寫入 clinical decision、SQL、shell、醫囑、PACS 操作或患者通知。OWASP LLM Top 10 2025 把 prompt injection、insecure output handling、training data / model poisoning、supply chain vulnerabilities 都列為重要風險，這些要進 product boundary，而不是只放在 AI research 討論。

### 7. Audit log 要做到 forensic-level traceability，該記什麼？

至少要記 user identity、role、auth method、timestamp、source IP / device、case ID、input file hash、model version、pipeline version、output ID、confidence / score、override action、export / download、admin change、patch action、CVD / incident reference。

Log 本身要防竄改、集中化、保留期限清楚，並能支援事件調查。AI SaMD 的 log 不是只為 debug，而是為了證明 clinical output 的來源、處理鏈、使用者動作與修補歷史。

### 8. Black-box pen test 的範圍該怎麼定？

不要只測 Web UI。範圍至少要包含 external-facing service、auth / RBAC、API authorization、file upload / DICOM handling、PACS integration、update channel、secrets exposure、logging leakage、container boundary、backup / restore、default config、hospital deployment guide。

Pen test 的目的不是「掃弱點」而已，而是驗證漏洞能不能串成 realistic attack path。測完之後，finding 必須進 Patch SLA：owner、severity、due date、decision、action、retest、archive。

### 9. 怎麼證明沒有超過風險門檻的 unresolved anomaly？

要先有 risk acceptance criteria。每個 finding 至少要有 ID、source、affected component、threat scenario、CVSS / clinical severity、applicability decision、mitigation、residual risk、owner、deadline、retest evidence、approval record。

最後用 risk register、test report、retest archive、QMS signoff 證明：沒有 unresolved anomaly 超過 acceptable risk threshold。這正好對應 deck 的 `Evidence, Not Slogans`：不是說「都修好了」，而是每個 finding 都有可追溯的結論。

### 10. AI supply chain 現在最新要補什麼？

要補三件事：data lineage、model auditability、third-party AI dependency visibility。醫療 AI 供應鏈不只看程式套件，也要看資料來源、模型來源、供應商、版本、更新、監測與退場機制。

HSCC / AHA 2026 對 third-party AI risk 的說法，已經把 AI supply chain transparency 拉到 procurement、vendor vetting、deployment、post-deployment monitoring 的層級。工程上不能只說「我們用了某個 API / model」。要能回答：資料哪裡來、模型誰維護、版本怎麼變、供應商出事怎麼替代、醫院端怎麼知道自己受不受影響。

## 上台可用的收斂句

一般民眾版：

> 醫療 AI 不是魔法，它是一套會進入醫療流程的系統。真正重要的不是它看起來多聰明，而是出錯時能不能被發現、被修好、被追蹤。

軟體公司版：

> 不要把 cybersecurity 當成上市前文件。把 SBOM、threat model、testing、Patch SLA、CVD 放進產品開發流程，文件自然會長出來。

資安工程師版：

> 這不是掃完弱點就結案。AI SaMD security 要證明 product boundary、attack surface、evidence chain、residual risk、repair path 都可追溯。

全場版：

> AI SaMD cybersecurity is not about protecting one model. It is about building a product system that can be trusted, repaired, and proven in the real medical world.

## Sources

- FDA, `Cybersecurity in Medical Devices: Quality Management System Considerations and Content of Premarket Submissions`, Final Guidance, February 2026: <https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-management-system-considerations-and-content-premarket>
- FDA, `Cybersecurity in Medical Devices Frequently Asked Questions (FAQs)`: <https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity-medical-devices-frequently-asked-questions-faqs>
- FDA, `Artificial Intelligence-Enabled Medical Devices`: <https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices>
- FDA, `Artificial Intelligence-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations`, Draft Guidance, January 2025: <https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing>
- FDA, `Marketing Submission Recommendations for a Predetermined Change Control Plan for Artificial Intelligence-Enabled Device Software Functions`, Final Guidance, August 2025: <https://www.fda.gov/regulatory-information/search-fda-guidance-documents/marketing-submission-recommendations-predetermined-change-control-plan-artificial-intelligence>
- TFDA 2025-08-14 AI/ML CADe / CADx guidance revision and independent performance assessment FAQ announcement: <https://www.fda.gov.tw/tc/siteListContent.aspx?id=49448&sid=310>
- TFDA, `115年度第1次醫療器材法規及管理溝通討論會議` materials: <https://www.fda.gov.tw/tc/includes/GetFile.ashx?id=f639107213340396020&type=1>
- AHA, `FBI: Health care was top target for ransomware, other cyberthreats in 2025`, 2026-04-10: <https://www.aha.org/news/headline/2026-04-10-fbi-health-care-was-top-target-ransomware-other-cyberthreats-2025>
- AHA, `Change Healthcare Cyberattack Significantly Disrupts Patient Care, Hospitals' Finances`, 2024-03-15: <https://www.aha.org/2024-03-15-aha-survey-change-healthcare-cyberattack-significantly-disrupts-patient-care-hospitals-finances>
- NHS England, `Synnovis cyber incident`: <https://www.england.nhs.uk/synnovis-cyber-incident/>
- CISA, `MicroDicom DICOM Viewer`, ICS Medical Advisory ICSMA-25-121-01: <https://www.cisa.gov/news-events/ics-medical-advisories/icsma-25-121-01>
- NVD, `CVE-2025-35975`: <https://nvd.nist.gov/vuln/detail/cve-2025-35975>
- NIST, `NIST AI RMF Playbook`: <https://www.nist.gov/itl/ai-risk-management-framework/nist-ai-rmf-playbook>
- NIST, `Cybersecurity Framework 2.0`: <https://www.nist.gov/cyberframework>
- CISA, `Known Exploited Vulnerabilities Catalog`: <https://www.cisa.gov/known-exploited-vulnerabilities-catalog>
- CISA, `Secure by Design`: <https://www.cisa.gov/securebydesign>
- OWASP, `Top 10 for Large Language Model Applications`: <https://owasp.org/www-project-top-10-for-large-language-model-applications/>
- AHA, `HSCC releases guide on third-party AI risk, supply chain transparency`, 2026-04-15: <https://www.aha.org/news/headline/2026-04-15-hscc-releases-guide-third-party-ai-risk-supply-chain-transparency>
- Health Sector Coordinating Council, `Third-Party AI Risk and Supply Chain Transparency Guide`: <https://healthsectorcouncil.org/ai-cyber-thirdparty/>
