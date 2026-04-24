# CYBERSEC 2026 AI SaMD Slide Deep Notes v1 - Positive Progressive zh-TW Rewrite

Status: positive-progressive rewrite of `cybersec-2026-ai-samd-slide-deep-notes-v1.md` for the generated compact/fallback storyline. The legacy v1 baseline remains preserved.

This version uses progressive, question-driven, cause-effect, and decision-support language. It keeps the DeepBT Detector-Plus product evidence examples and the compact 14-slide structure.

Core path:

> **Boundary -> Evidence -> Decision -> Repair Proof**

1. **Boundary**: define intended use, system boundary, users, data flow, integrations, runtime environment.
2. **Evidence**: build architecture evidence, Threat Modeling, SBOM, risk assessment, controls, testing records.
3. **Decision**: turn findings into triage, risk acceptance, mitigation, compensating controls, release decisions.
4. **Repair Proof**: prove repair through patch records, retest evidence, advisories, release history, postmarket monitoring.

---

# Opening｜全場定位

## One Question

**一個 AI model 要變成可信任的醫療軟體產品，中間需要留下哪些證據和決策？**

## Concrete Situation

「今天我們從一個具體場景開始。」

「有一個 AI 可以協助放射治療團隊產生腦瘤初始 contour。模型準確率很好，demo 也漂亮。這是重要起點。」

「接下來，臨床使用會帶出更細的問題：輸入的 T1W+C / T2W MRI 是否正確？DICOM metadata 是否完整？輸出 DICOM PR / RTSS 後，醫療專業人員如何確認或修改？系統在哪個 runtime environment 跑？更新由誰批准？漏洞出現時誰判斷、誰通知、誰修補、誰重測？」

「這些問題會保留模型價值，並把模型帶進醫療產品的責任世界。」

「今天我們會把 FDA 524B、Threat Modeling、SBOM、Patch SLA 連成一條可被團隊執行的產品信任路徑。」

「Boundary。Evidence。Decision。Repair Proof。」

## Decision / Takeaway

**全場所有內容都回到四個資料夾。**

Boundary 放 intended use、system boundary、users、data flow、integrations、runtime environment。Evidence 放 architecture、Threat Modeling、SBOM、risk assessment、controls、testing records。Decision 放 finding triage、risk acceptance、mitigation、compensating controls、release decisions。Repair Proof 放 patch records、retest evidence、customer advisories、release history、postmarket monitoring。

---

# Slide 1｜AI 軟體醫材的資安實戰

## One Question

**AI 醫療產品進入醫院時，第一條產品信任路徑要如何被說清楚？**

## Concrete Situation

「第一頁只需要讓觀眾看見今天的路徑：從 AI model，走到可以被醫院使用、被團隊修補、被審查者檢查的醫療軟體產品。」

「一般觀眾可以先想像：AI 幫醫師畫出腦瘤輪廓。模型會算答案，是第一層。醫院接著會問：資料從哪裡來？誰可以使用？結果如何確認？系統故障時如何恢復？漏洞出現時誰修？修完後如何證明？」

「工程師會看到下一層：產品從 Brain Tumor AI Module 延伸到 Web UI、Integration Module、Docker、WSL2、DCMTK、Node.js、Python、PACS / DICOM workflow、SBOM、provenance、integrity、support status。」

「主管會聽到產品營運能力：FDA 524B 要求 cyber device sponsor 準備上市後監控、識別、處理 vulnerabilities and exploits 的計畫，也要處理 CVD、postmarket updates and patches、SBOM。這些要求會轉化為上市後營運能力。」

## Decision / Takeaway

**第一頁只講產品信任路徑。**

上台可以說：「各位好，我是林家聖。今天我想用一個問題串起來：一個 AI model 要變成可信任的醫療產品，中間需要留下哪些證據和決策？」

---

# Slide 2｜Required CYBERSEC Disclaimer

## One Question

**公開資安演講要如何提供可執行方法，同時維持安全與責任邊界？**

## Concrete Situation

「這頁是大會 required disclaimer。它看起來是形式頁，但在醫療、資安、法規裡，邊界感本身就是專業。」

「今天會談 FDA、Patch SLA、incident response、Threat Modeling；這些內容定位為治理原則與可落地方法，法律判斷仍需要由各組織依照產品、地區與法規責任處理。」

「公開演講也需要安全邊界：私人醫院或客戶細節、內部拓樸、exploit recipe、專利敏感 implementation mechanics，都要留在合適的非公開管道。」

「CYBERSEC 2026 有 AI 即時翻譯，所以這場的 stage language 要短、清楚、少長句。Boundary、Evidence、Decision、Repair Proof 這種結構，對現場觀眾和即時翻譯都比較友善。」

## Decision / Takeaway

**把 disclaimer 當成溝通邊界。**

停一下讓觀眾看見，然後直接進入 Slide 3。這頁的任務是建立安全、法律與專業邊界。

---

# Slide 3｜模型是起點

## One Question

**醫院看到 AI 時，會從模型能力一路問到哪些產品責任？**

## Concrete Situation

「很多 AI 團隊一開始是在做模型。這很合理，因為模型能力讓產品討論有了起點。」

「真正的挑戰會在產品化後出現。模型像引擎，SaMD 像一台要上路的車。引擎很強是必要條件；煞車、儀表板、保養紀錄、召回流程、駕駛說明、事故處理，會決定這台車能否被信任。」

「DeepBT Detector-Plus 的場景很適合說明這一點。它協助放射治療計畫流程產生腦瘤初始 contour，輸入 T1W+C / T2W MRI，輸出 DICOM PR / RTSS，並要求醫療專業人員在治療前確認或修改 AI 產出的 contour。」

「這個設定把模型帶進 clinical workflow。它提醒觀眾：這是一個 decision-support product，要管理 intended use、human-in-the-loop、DICOM viewer、Temporary DICOM Storage、PACS、C-FIND、C-MOVE、C-STORE、log、configuration files。」

「如果一個 segmentation model 在 validation set 上表現很好，但醫院使用時影像序列錯了、DICOM metadata 不完整、viewer 顯示 context 錯了、暫存資料沒有清掉，臨床信任仍然會受到影響。」

## Decision / Takeaway

**建立 Responsibility Map。**

第一版就寫清楚：誰使用、在哪個流程使用、輸入是什麼、輸出是什麼、輸出如何確認、資料暫存多久、異常如何處理、產品如何更新、客戶如何通報事件。這張責任地圖會成為 architecture view、Threat Modeling、risk assessment、testing、labeling、Patch SLA 的起點。

---

# Slide 4｜AI 變成基礎設施

## One Question

**AI 從模型檔進入 care infrastructure 後，風險會如何改變？**

## Concrete Situation

「2026 年談 AI，要一路看到 runtime、資料、identity、update chain、support path，以及最後連到 clinical workflow 的路徑。」

「醫療與生命科學產業正在把 AI 當成 infrastructure 建置。大型 AI factory 支撐 diagnostics、therapeutics、clinical trials 和資料洞察，這代表 AI 已經開始變成 operating backbone。」

「用一般觀眾聽得懂的比喻來說：以前 AI 像一台單獨小家電，壞了影響有限。現在 AI 接到醫院資料流、帳號權限、更新鏈、客服支援、PACS / HIS workflow，就像變成大樓水電的一部分。」

「Change Healthcare 事件讓我們看到第三方醫療基礎設施中斷會影響 patient care 和財務流程。台灣馬偕事件也提醒我們，勒索軟體攻擊會碰到掛號、急診與臨床營運。」

「這些案例帶出 product infrastructure 的現實：AI 一旦進入流程，資安問題會沿著流程變成照護連續性問題。」

## Decision / Takeaway

**做 AI infrastructure readiness check。**

部署前問清楚：模型在哪裡跑？資料從哪裡來？誰能呼叫 API？誰監控 log？誰可以更新？更新失敗如何 rollback？醫院端如何 fallback？答案要寫進 architecture view、labeling、support boundary。

---

# Slide 5｜Risk grows with architecture

## One Question

**同一個 AI model，放在 Model、Viewer、Platform、Connected Medical System 四種尺度裡，證據需求會怎麼變？**

## Concrete Situation

「這頁是整場地圖。後面的法規、testing、Patch SLA 都要回到這張圖。」

「Scale 1 是 Model。團隊要保護 model provenance、data lineage、dependency、SBOM、version locking、update boundary。」

「Scale 2 是 Viewer。產品加入 viewer 後，就有 parser、upload、cache、output interpretation、使用者誤解與暫存資料風險。」

「Scale 3 是 Platform / Database。這一層開始有 identity、API、database、audit log、backup、admin action。」

「Scale 4 是 Connected Medical System。產品接到 PACS / HIS、hospital network、update server、remote service，風險會延伸到 clinical continuity 和 shared responsibility。」

「風險增加，通常是因為產品能力變強、連接變多、責任變重。每跨一層，證據也要跟著跨一層。」

## Decision / Takeaway

**每次新增功能都做 Product Boundary Review。**

PM、RD、QA、法規、資安一起問：我們是否跨層？新增 viewer，要更新 input / parser / cache risk。新增 database，要更新 IAM、API、audit log、backup。新增 PACS / HIS，要更新 deployment guide、HDO responsibility、incident reporting、downtime fallback。

---

# Slide 6｜Evidence Chain

## One Question

**當團隊說產品安全，審查者、醫院和主管需要看見哪一條 evidence chain？**

## Concrete Situation

「這頁是全場知識密度最高的一頁，所以要先把語言翻成人話。」

「FDA 524B 可以被理解成幾個產品能力：monitor、identify、address postmarket cybersecurity vulnerabilities and exploits，包含 CVD；提供 postmarket updates and patches；準備包含 commercial、open-source、off-the-shelf components 的 SBOM。」

「FDA 2026 Guidance 的意義，是把這些能力接到 quality management system。它提醒我們，cybersecurity evidence 要進入產品設計、標示、上市前文件與上市後維護。」

「一般觀眾可以用體檢比喻理解。說自己健康還需要檢查數據、醫師判讀、追蹤紀錄和異常處理。醫療器材資安也是一樣：architecture、Threat Modeling、risk assessment、controls、testing、finding disposition、patch / retest records 要能接成一條線。」

「當邊界被定義，風險位置就會浮現。風險被看見後，證據鏈才能建立。決策被記錄後，修補能力才可被驗證。」

## Decision / Takeaway

**每個 finding 都要開成 Evidence Chain Ticket。**

Ticket 裡要有 Risk ID、Control ID、Test ID、Finding ID、Decision、Retest Evidence、Archive Location。例如 Web UI 權限問題要對應 Spoofing / Elevation of Privilege，控制可能是 JWT / RBAC / default-deny，測試可能是 unauthorized access 或 black-box pen test，decision 可能是 fix now 或 compensating control，最後要有 retest result 和 release record。

---

# Slide 7｜Model, Governance, Stack

## One Question

**模型團隊、資安團隊、法規團隊和主管，如何用同一張表討論 AI 風險？**

## Concrete Situation

「Slide 6 講 evidence chain，Slide 7 要把它翻成公司內部的三種語言。」

「第一種是 model evidence：intended use、data、V&V、limitations、performance monitoring。TFDA AI/ML SaMD 指引和 FDA AI-enabled device software draft guidance 都提醒團隊，AI 產品要說清楚用途、資料、驗證、限制與 total product life cycle。」

「第二種是 governance language：owner、severity、acceptance criteria、residual risk、release decision。NIST CSF 2.0 和 AI RMF 的價值，是提供跨角色共同語言，讓不同角色能討論同一個風險。」

「第三種是 AI stack security：SBOM、model integrity、runtime isolation、secrets、API access、logging、update path、software supply chain。即使產品採用傳統 classifier，OWASP LLM Top 10 仍提醒我們，AI security 已經擴展到 input、output、data、model、supply chain、runtime。」

「一個可信 AI 團隊要能回答三種問題：模型能做什麼、有哪些限制；公司誰負責風險決策；模型跑起來的軟體和環境如何被保護。」

## Decision / Takeaway

**建立三欄 Risk Translation Sheet。**

每個重要風險都要同時寫：Model impact、Security impact、Clinical / business decision。Design review 時用這三欄讓 AI、RD、QA、法規、主管對齊同一個 decision。

---

# Slide 8｜Scale 1-2：Model 到 Viewer

## One Question

**攻擊者會沿著哪一條最容易影響 clinical output 的路徑前進？**

## Concrete Situation

「前兩層是 Model 和 Viewer。」

「Scale 1 的核心是：模型本身就是資產。model artifact 要有來源、版本、訓練資料脈絡、驗證結果、dependency、hash / signature、更新邊界。模型被替換、被竄改、用錯版本，clinical output 就會失去信任基礎。」

「SBOM 文件在這裡很重要。DeepBT Detector-Plus 使用 Python、Node.js、Docker、WSL2、DCMTK、JSON，並透過 Docker-based deployment 鎖定 dependency 版本。這些紀錄是模型產品可追溯的基本功。」

「Scale 2 的核心是：viewer 把模型變成使用情境。一旦有 viewer，就有人上傳檔案、讀取 DICOM、看畫面、理解 AI output。攻擊者可以選擇 file parser、malformed DICOM、cache、UI error message、output interpretation。」

「MicroDicom DICOM Viewer 的 CVE-2025-35975 很適合當案例。NVD 描述它有 out-of-bounds write vulnerability，使用者開啟惡意 DCM 檔後可能導致 arbitrary code execution。這讓 viewer / parser 從包裝層變成真實 attack surface。」

## Decision / Takeaway

**Scale 1 建 model release card；Scale 2 建 viewer input safety workflow。**

Model release card 包含 model version、training / validation dataset references、performance metrics、known limitations、SBOM、hash / signature、approved intended use。Viewer workflow 包含 DICOM conformance validation、file size / type checks、malformed file testing、fuzzing、temporary data encryption、automatic cache deletion、generic error message、output limitation notice。

---

# Slide 9｜Scale 3-4：Platform 到 Connected Medical System

## One Question

**AI 產品接進 platform、database、PACS / HIS 後，責任邊界要如何被寫清楚？**

## Concrete Situation

「Scale 3 把風險推進公司營運。只要有 platform / database，就有身份、權限、API、資料庫、audit log、backup。」

「DeepBT 風險文件中的 Web UI credential impersonation、sensitive data insecure storage、excessive requests、container breakout / privilege escalation，都是平台化後要面對的風險。」

「Scale 4 把風險推進 clinical continuity。DeepBT 是 installed on local workstations、直接與 PACS 互動、使用 C-FIND、C-MOVE、C-STORE，並限制 cloud storage、remote connections、external internet access。這些設計降低外部暴露，但只要接 hospital LAN，就仍然需要處理內部網路、shared responsibility、downtime fallback。」

「Synnovis 事件提醒我們，醫療供應商被攻擊後，影響會擴到服務恢復、資料風險、臨床 workflow、公眾信任。馬偕事件則讓台灣聽眾看見本地脈絡：急診、掛號、病歷、臨床流程都可能受到影響。」

## Decision / Takeaway

**Scale 3 建 platform security baseline；Scale 4 建 connected deployment checklist。**

Platform baseline 包含 MFA / RBAC、API authorization、rate limit、audit log、encryption-at-rest、backup / restore drill。Connected checklist 包含 isolated VLAN、default-deny host firewall、allowed PACS IP / AE Title、DICOM-TLS 或 VPN、SIEM / SOC log forwarding、secure update channel、manual update window、downtime fallback、hospital IT contact、incident reporting route。

---

# Slide 10｜Cyber Safety Is Patient Safety

## One Question

**醫療資安如何從 IT issue 走到 patient safety 和 clinical continuity？**

## Concrete Situation

「這頁是全場情緒高點，畫面可以只留一句：Cyber Safety Is Patient Safety。」

「這句話要被翻成醫療現場語言。Availability 是醫師需要結果時，系統能不能用。Integrity 是醫師能不能相信 AI output。Confidentiality 是病人資料與病人信任是否被保護。Repairability 是出事後產品能不能安全恢復。」

「ECRI 2026 Top Health Technology Hazards 把 healthcare AI chatbots misuse 和 systems outages / digital darkness 放進重要風險，也提醒我們 AI 風險會包含錯誤信任、錯誤使用、系統中斷。」

「Change Healthcare、Synnovis、馬偕、Contec 這些案例共同指向同一件事：醫療系統不可用、資料不可信、漏洞修不了時，臨床流程會受到壓力。」

「這頁上台要慢。先讓 Cyber Safety Is Patient Safety 進到觀眾腦中，再補一句：醫療現場已經告訴我們，系統中斷很快就會變成照護中斷。」

## Decision / Takeaway

**Risk register 裡加一欄 clinical impact。**

每個 security finding 都要問：是否影響 AI result 可信度？是否延遲診療？是否造成多病人資料暴露？是否需要 downtime fallback？是否需要 hospital advisory？這欄會讓醫師、主管、QA、法規、資安能講同一種語言。

---

# Slide 11｜White-box + Black-box

## One Question

**每一種測試回答哪一個 release decision？**

## Concrete Situation

「這頁要用 testing portfolio 的方式講：每一種測試回答一個決策問題。」

「SBOM / SCA 回答：我們用了什麼元件，有沒有已知漏洞？」

「White-box 回答：release 前有哪些便宜、可修、可追溯的問題？」

「Fuzz / abuse case 回答：異常輸入會不會打壞流程？」

「Black-box 回答：外部看得到什麼？」

「Pen test 回答：漏洞能不能被串成真實 attack path？」

「Retest 回答：修補是否真的成立？」

「DeepBT Testing 文件中的 unauthorized access、bcrypt password hashing、network isolation、secure DICOM transmission、encryption-at-rest、audit logging、Docker recovery、secure update、external black-box penetration test、internal vulnerability scan，就是 testing portfolio 的例子。」

「主管要聽到的重點是：測試結果要能進入 owner、severity、due date、fix decision、retest evidence。這樣測試才會支撐 release judgment。」

## Decision / Takeaway

**建立 Testing-to-Finding Pipeline。**

先定義 scope：Web UI、API、DICOM port、temporary storage、AI model files、update path。再執行 white-box：SAST、SCA、secret scan、container config、SBOM matching。再執行 black-box：auth bypass、API abuse、DICOM handling、network scan、pen test。接著 findings 進入 Patch SLA，修補後 retest，最後 archive evidence。

---

# Slide 12｜Patch SLA

## One Question

**漏洞進來後，團隊如何從 vulnerability management 走到可稽核的 repair proof？**

## Concrete Situation

「Patch SLA 是全場營運高潮。」

「這裡要先講清楚：Patch SLA 是把 FDA 524B 的 updates / patches、reasonable time、CVD、postmarket vulnerability management 翻譯成公司 operating model。主管熟悉 SLA、owner、severity、due date、decision、evidence，這些語言可以承接 524B 的產品治理要求。」

「FDA 524B 落到公司內部，會變成一連串問題：漏洞進來誰收？誰判斷是否適用？誰定嚴重度？誰決定 fix now、compensating control、defer、not applicable？誰通知客戶？誰重測？證據放哪？」

「DeepBT Management Plan 的 dual-track 很適合當例子。Critical vulnerabilities 走 expedited mitigation，非 critical 或已被 isolation / default-deny firewall 有效緩解的漏洞，進 periodic security update cycle。Safety Override 也很重要：如果 patch 可能影響 AI model accuracy、DICOM structure 或 system stability，patient safety 和 clinical effectiveness 要優先處理。」

「醫療 AI 的 patch 要同時追求兩件事：快速控制風險，並維持 patient safety。」

## Decision / Takeaway

**建立 Patch SLA operating model。**

Intake：漏洞從 internal testing、customer report、CISA KEV、NVD、vendor advisory 進來。Triage：判斷 applicability、exploitability、clinical impact。Decision：fix now、compensating control、defer with timeline、not applicable with rationale、customer advisory、safety validation required。Action：修 patch、補 firewall rule、更新 configuration、或記錄 risk acceptance。Retest：確認控制有效。Archive：保存 advisory、risk rationale、test report、release note、customer notification。

---

# Slide 13｜Small Team 30 / 60 / 90

## One Question

**小團隊如何在 90 天內建立第一個 evidence loop？**

## Concrete Situation

「這頁要把壓力降下來，同時保留標準。」

「30 / 60 / 90 是 adoption scaffold。它的用途是讓小團隊啟動第一個 evidence loop；正式時程仍要由產品風險、臨床影響、客戶環境與 QMS 決策定義。」

「一般觀眾可以用房子理解：第一個月先畫平面圖，第二個月開始裝門鎖和監視器，第三個月找外部人員測試門有沒有真的鎖上。」

「30 天，讓產品看得見：inventory、SBOM、data flow、intended use、known vulnerabilities、DICOM workflow、Internal Protected Boundary、External Boundary、PACS connection、Temporary DICOM Storage、AI model、update path。」

「60 天，讓風險進流程：做 STRIDE workshop、建立 CI security gates、finding workflow、customer security note template、CISA KEV monitoring、CVD intake。」

「90 天，證明修補能力：external black-box pen test、internal vulnerability scan、Patch SLA drill、CVD process、retest evidence、release history cleanup。」

「一個 8 人 AI 醫療團隊可以這樣跑：30 天發現 DICOM cache 沒有 retention policy；60 天用 STRIDE 找到 model tampering 和 unauthorized PACS access；90 天用 black-box pen test 找到 login interface 的限制不足，先用 IP restriction / firewall compensating control 降風險，再安排正式修補與重測。」

## Decision / Takeaway

**30 天看見產品，60 天讓風險進流程，90 天證明修補能力。**

這三個里程碑比「我們會持續改善」更具體，也更容易被董事會、投資人、醫院採購、QA、法規接受。

---

# Slide 14｜先建立信任，再面對稽核

## One Question

**法規文件如何從產品信任系統自然長出來？**

## Concrete Situation

「最後一頁要收束。」

「secure-by-design 的意思，是在產品設計、開發、測試、部署、上市後維護裡，把安全自然放進每個節點。」

「一般觀眾可以用大樓消防理解。逃生梯、消防警報、撒水系統、緊急照明，要在設計圖一開始就出現。醫療 AI 也是一樣，資安要從產品邊界、資料流程、使用者角色、修補流程、事件通報開始放進設計。」

「工程師要聽到的是：security evidence 是平常工程工作留下的痕跡。Threat Modeling 在架構設計時進來，SBOM 隨 build artifact 留下，testing 連到 release gate，Patch SLA 連到 finding governance，retest evidence 形成 repair proof。」

「主管要聽到的是：成熟團隊會讓每個風險都知道怎麼證明、怎麼修、怎麼追。」

「今天我們從 model 開始，走到 connected medical system。每往前一步，產品更有價值，也更需要被信任、被修補、被稽核。」

## Decision / Takeaway

**先把安全做進產品，法規文件才會自然長出來。**

最後可以收成：「如果我們能說清楚 Boundary、留下 Evidence、做出 Decision、保存 Repair Proof，稽核就會從最後補文件，變成檢查一套已經在運作的產品信任系統。謝謝大家。」

---

# Final Checklist

| 檢查項目 | 狀態 |
| --- | --- |
| Rhetorical negation patterns | 已移除；張力改由 progression、uncertainty、decision pressure 建立。 |
| Slide rhythm | 已符合 question -> scenario -> decision。 |
| Boundary -> Evidence -> Decision -> Repair Proof | 已在 Opening、Slide 1、Slide 6、Slide 12、Slide 14 收回主軸。 |
| Technical terms | 已保留 FDA 524B、Threat Modeling、SBOM、Patch SLA、cyber device、postmarket monitoring、vulnerability management、exploit、CVD、DICOM / PACS、software supply chain、runtime environment。 |
| Tone | 已調整為 guiding、structured、decision-support。 |
| Slogan stacking | 已改成結構、問題與工作流。 |

