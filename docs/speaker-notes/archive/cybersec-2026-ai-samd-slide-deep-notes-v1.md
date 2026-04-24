# CYBERSEC 2026 AI SaMD Slide Deep Notes v1 - Legacy zh-TW Baseline

Status: preserved legacy zh-TW deep-note baseline for the generated compact/fallback storyline. The current preferred compact/fallback rehearsal script lives at `../cybersec-2026-ai-samd-slide-deep-notes-v1-positive-progressive-zh-tw.md`; canonical `v1.3` deck prep lives in `../reference/`.

以下以當時的 **14 頁 generated compact fallback target** 為準來精修。這一版的核心不是「把所有資訊塞進投影片」，而是把每一頁背後的知識、案例、趨勢、工作流都準備好，讓你上台時可以講得有層次；投影片本身仍要維持一頁一重點、低文字量、強留白，否則會破壞你目前設計好的 keynote 節奏。你的 Talk Design 已經把這場定義成 30 分鐘、14 頁、28:30 spoken content + 1:30 buffer 的公開資安大會演講，主軸是「AI SaMD 團隊賣的不是模型，而是一個 trustable、patchable、auditable 的臨床產品系統」；Evaluation System 也提醒，投影片漂亮不能救弱敘事，真正評分會看產品尺度、證據鏈、測試策略、Patch SLA 和小團隊 roadmap 能不能被聽眾記住。

先更新最重要的最新趨勢：你所有提到 FDA cybersecurity guidance 的地方，建議統一改成 **FDA 2026 Guidance**。FDA 在 2026 年 2 月 3 日發布新版 *Cybersecurity in Medical Devices: Quality Management System Considerations and Content of Premarket Submissions*，明確取代 2025 年 6 月 27 日版本；FDA 說這份文件提供醫療器材資安設計、標示與上市前送審文件建議，也處理 FD&C Act section 524B。產業評論普遍把 2026 版解讀為「主要是對齊 QMSR / ISO 13485 語言，而不是推翻原本技術要求」，所以你的演講可以講成：**資安不再是外掛文件，而是品質管理系統的一部分。** ([U.S. Food and Drug Administration][1])

---

# Slide 1｜AI 軟體醫材的資安實戰

這一頁的任務不是介紹你有多厲害，而是讓所有人立刻知道：這不是一場 AI hype talk，也不是法規朗讀，更不是工具清單。你要把 FDA 524B、Threat Modeling、Patch SLA 這三個看似分散的主題，收斂成一條產品信任路徑：**產品邊界先被定義，風險才知道在哪；風險被看見，證據鏈才接得起來；finding 被治理，修補能力才被證明。** 你的 slide blueprint 已經把第一頁定位成「product-trust and decision-support talk」，並要求用 Boundary → Evidence → Decision → Repair proof 開場，這個方向是對的。

對一般大眾來說，這頁可以用一句很白的話解釋：「AI 醫療產品不是只要會算答案，它還要在醫院裡安全地被使用。」假設有一個 AI 可以幫忙畫出腦瘤輪廓，它在 demo 場景很漂亮；但醫院真正會問的是：資料從哪來？誰可以用？結果錯了誰確認？系統壞了怎麼恢復？漏洞出現誰修？修完怎麼證明？這些問題一出現，AI 就從一個模型變成一個產品責任。

對工程師來說，這頁要暗示：今天不會只談 model robustness。以附件中的 DeepBT Detector-Plus 文件為例，產品不是只有 Brain Tumor AI Module，而是包含 Web UI、Integration Module、Brain Tumor AI Module、Docker、WSL2、DCMTK、Node.js、Python、PACS/DICOM workflow 等多個組成，SBOM 文件也把元件來源、版本鎖定、provenance、integrity 和 support status 放進管理範圍。這代表工程師要思考的不只是模型權重，而是整個 software supply chain 與 runtime environment。

對主管來說，第一頁真正的管理語言是：「我們不是為了送審而補文件，我們是在建立產品信任能力。」FDA 524B 要求 cyber device 的上市前申請要包含上市後監控、識別、處理漏洞與 exploit 的計畫，也要包含 CVD、postmarket updates and patches、SBOM。這些不是紙上作業，而是上市後營運能力。([U.S. Food and Drug Administration][2])

這頁的工作流可以藏在 speaker notes，不一定放上投影片：產品團隊第一天就要建立四個資料夾。第一個是 Boundary，放 intended use、system boundary、data flow。第二個是 Evidence，放 architecture、threat model、risk assessment、controls、testing。第三個是 Decision，放 finding triage、risk acceptance、compensating control。第四個是 Repair proof，放 patch record、retest evidence、customer advisory、release history。這四個資料夾，就是你整場演講的 operational backbone。

上台時，這頁只要 10 秒。不要補經歷，不要講太多背景。可以講：「各位好，我是林家聖。今天不是背法規，也不是展示工具清單。我想用一個問題串起來：一個 AI model 要變成可信任的醫療產品，中間需要留下哪些證據和決策？」

---

# Slide 2｜Required CYBERSEC Disclaimer

這頁是 compliance beat，不是敘事頁。你的藍圖已經明確指出，Slide 2 是大會 required disclaimer，而且要和主敘事分開；大會信件也明確要求講者把免責聲明頁放在封面下一頁。 

這頁的知識解析很簡單：在醫療、資安、法規這三個領域，邊界感本身就是專業。你不能在公開演講中把內容講成法律意見，也不能保證任何公司照做就一定合規，更不能把私人客戶、醫院拓樸、產品內部細節、學生資料、專利敏感機制放上大螢幕。你的 Talk Design 也明確寫出，public talk 要排除 private hospital/client details、proprietary code、student records、exploit recipes、patent-sensitive implementation mechanics。

對一般大眾來說，這頁只是「講者有把責任邊界講清楚」。對工程師來說，這頁提醒的是：「不要把真實 exploit step 或內部架構細節公開成攻擊指南。」對主管來說，這頁是在降低溝通風險：你後面講 FDA、Patch SLA、incident response 時，講的是治理原則與可落地方法，不是替任何特定產品做公開保證。

最新趨勢也值得注意：CYBERSEC 2026 今年新增 AI 即時翻譯服務。這代表你的語句要更短、更清楚、少用長句，否則即時翻譯會把語意切壞。大會通知提到會提供 AI 即時翻譯，讓不同語言背景的與會者透過 QR Code 選擇語言；所以你後面所有 anchor line 都要盡量像「你賣的不是模型」、「法規要的是證據，不是口號」、「Cyber Safety is Patient Safety」這種可被翻譯、可被記憶的句子。

工作流上，這頁之前你要確認三件事：第一，disclaimer 圖片解析度與比例正確。第二，這頁不加自己的法律詮釋。第三，講完後立刻進入 Slide 3，不要讓聽眾卡在形式頁。上台只說：「這是大會必要的 disclaimer，我在這裡停一下，讓大家看見。接下來我們直接進入今天真正的問題。」

---

# Slide 3｜你賣的不是模型

這頁是整場的第一個大轉念。很多 AI 團隊一開始會說：「我們只是提供模型。」但醫療現場不會這樣看。醫師看到的是結果，病人承受的是後果，公司負責的是整個使用情境。你這頁要讓聽眾從「模型準不準」轉到「產品責任能不能被證明」。你的 Talk Design 把這句列為核心 memory anchor，這是整場最重要的入口句。

對一般大眾來說，可以這樣說：你不是賣一顆很厲害的引擎，你是賣一台真的要上路的車。引擎再強，如果煞車不穩、儀表板亂顯示、保養流程不清楚、召回制度不存在，這台車就不值得信任。AI 醫療產品也是一樣，模型準確率只是引擎；真正被醫院買走的，是整台車能不能安全上路。

用你附件中的產品場景來看，DeepBT Detector-Plus 是協助放射治療計畫流程中產生腦瘤初始 contour 的 AI 軟體，輸入 T1W+C / T2W MRI，輸出 DICOM PR / RTSS，並且明確要求醫療專業人員在治療前必須確認或修改 AI 產出的 contour。這個設定很重要，因為它告訴觀眾：這不是全自動取代醫師，而是放進臨床 workflow 的 decision-support product。

對工程師來說，這頁背後其實是 product boundary。模型只是一個 asset，周圍還有 Web UI、Temporary DICOM Storage、Brain Tumor AI Model、PACS、DICOM Viewer、C-FIND、C-MOVE、C-STORE、log、configuration files。Threat Model 文件已經用 STRIDE 去分析 Spoofing、Tampering、Repudiation、Information Disclosure、Denial of Service、Elevation of Privilege，並對應到系統資產與 cybersecurity requirements。這正是「產品責任」而不是「模型表現」的證據。

對主管來說，這頁要講成：「責任不是從出事那天開始，而是從你把產品放進臨床流程那天開始。」如果 intended use 沒寫清楚，模型限制沒講清楚，使用者角色沒定義，資安更新流程沒設計，客戶事件通報沒有窗口，最後都會回到公司責任。這不是恐嚇，而是醫療器材上市後責任的現實。

真實世界中，AI 醫材正在快速增加。FDA 的 AI-enabled medical device list 是為了讓市場、醫療人員與病人更透明地知道哪些已授權醫療器材使用 AI 技術，FDA 也說這份清單會持續更新。這對你的演講很有幫助：AI 醫材不是未來式，而是現在式；所以產品責任也不是未來問題，而是現在就要處理的問題。([U.S. Food and Drug Administration][3])

虛擬案例可以這樣講：某團隊做出一個腦部 MRI segmentation model，在 validation set 上表現很好。但進醫院後發現，有些使用者用錯影像序列，有些 DICOM metadata 不完整，有些結果被 viewer 顯示在錯誤 context，有些暫存資料沒有清除。這些問題都不是模型分數本身，卻都會影響臨床信任。這就是「你賣的不是模型」的意思。

工作流上，這頁要引出「責任地圖」。產品第一版就要寫清楚：誰用、在哪裡用、輸入是什麼、輸出是什麼、輸出能不能直接用、誰確認、資料暫存多久、異常如何處理、產品如何更新、客戶如何通報事件。這張責任地圖，會變成後面的 architecture view、threat model、risk assessment、testing、labeling、Patch SLA 的共同起點。

---

# Slide 4｜AI 變成基礎設施

這頁要回答「為什麼現在更急」。答案不是因為 AI 很流行，而是因為 AI 正在變成 care infrastructure。2026 年的 AI 不再只是模型檔，它會接 runtime、資料、identity、update chain、support path，最後接到 clinical workflow。你的藍圖把這頁定位成「AI deployment stack → clinical continuity failure path」，這是非常好的設計，因為它把科技趨勢和醫療現場連起來。

最新趨勢很明顯：AI 正在被當作大型基礎設施建置。Roche 在 2026 年 3 月宣布擴建 NVIDIA AI factory，新增 2,176 顆 Blackwell GPUs，整體 on-premise + cloud GPU infrastructure 超過 3,500 顆，用於 diagnostics、therapeutics、clinical trials 和大規模資料洞察。這不是要你在簡報放 Roche logo，而是可以用一句話說：「醫療與生命科學產業正在把 AI 當作 infrastructure，而不是單一模型。」([Roche][4])

台灣脈絡也要補進來，但不能講成第二場國家戰略簡報。行政院 2025 年第七期國家資通安全發展方案提到全社會資安防禦、關鍵基礎設施韌性、國內資安產業、AI 新興資安科技；《國家資通安全戰略2025》也把四大支柱列為全社會防衛韌性、國土防衛與關鍵基礎設施、關鍵產業與供應鏈、AI 應用與安全。你的 Talk Design 已經提醒，國家戰略只能提高戰略高度，不能把主題帶偏。([Executive Yuan][5]) 

對一般大眾來說，可以用「水電」比喻。以前 AI 像一台單獨的小家電，壞了影響有限；現在 AI 開始接到醫院資料流、帳號權限、更新鏈、客服支援、PACS/HIS workflow，就像變成大樓水電的一部分。一旦出事，就不是某個 demo 不能跑，而是臨床流程可能延遲。

對工程師來說，這頁要從三層看：model、runtime、infrastructure。Model 層看 provenance、evaluation、model version、model tampering。Runtime 層看 container、API、secret、log、resource limit、policy enforcement。Infrastructure 層看 identity、network segmentation、host-based firewall、SBOM、update channel、support boundary。你的 Controls 文件已經把 JWT、DICOM-TLS、AES-256、Default-Deny、Nginx single entry point、SIEM forwarding、golden image recovery、signed container image 等控制寫進來，這些都是把 AI 當 infrastructure 治理的具體做法。

真實案例可以用 Change Healthcare。2024 年 Change Healthcare cyberattack 造成美國醫療體系大規模營運干擾，AHA 調查顯示約 1,000 家醫院回覆中，94% 回報財務影響，74% 回報直接病人照護影響。這說明醫療資安事件不一定直接攻擊單一醫療器材，也可能攻擊醫療系統中的第三方基礎設施，最後讓臨床和財務流程一起受影響。([American Hospital Association][6])

台灣也有本地案例。iThome 報導，2025 年 2 月馬偕紀念醫院遭 CrazyHunter 勒索軟體攻擊，已知攻擊路徑涉及 AD 主機派送惡意程式與 BYOVD 手法；衛福部 H-ISAC 發警訊，衛福部與資安署成立快速反應小組進駐協助。這可以讓台灣聽眾知道：醫療資安不是國外新聞，是本地醫療現場已經發生的事。([iThome][7])

工作流上，這頁可以提出「AI infrastructure readiness check」。部署前，團隊要問：模型在哪裡跑？資料從哪裡來？誰能呼叫 API？誰監控 log？誰可以更新？更新失敗怎麼 rollback？醫院端如何 fallback？這些答案如果沒有被寫進 architecture view 和 labeling，所謂 AI infrastructure 就只是口號。

---

# Slide 5｜Risk grows with architecture

這頁是整場的地圖。四層產品尺度是：Model、Viewer、Platform / Database、Connected Medical System。你的藍圖和 Talk Design 都要求這頁不能被刪，因為後面的法規、testing、Patch SLA 都要回到這張地圖。 

這頁的核心知識是：**同一個 AI model，放在不同產品邊界裡，資安責任完全不同。** 如果它只是 model artifact，你要保護的是模型來源、資料 lineage、dependency、SBOM、版本鎖定、更新邊界。如果它加了 viewer，你要處理檔案解析、upload、cache、output interpretation。如果它變成 platform/database，你要處理 identity、API、database、audit log、backup。如果它進入 connected medical system，你要處理 PACS/HIS、hospital network、update server、remote service、downtime fallback。

對一般大眾來說，可以說：「風險不是突然變大，是產品每多接一個東西，責任就跟著長大。」像一台單機電腦只在家裡用，風險比較小；如果它接上學校系統，就要處理帳號；接上全校成績資料庫，就要處理資料權限；接上升學報名平台，就要處理服務不中斷。醫療 AI 也是一樣，每跨一層，證據需求也跨一層。

FDA 2026 Guidance 也支持這個觀點。FDA 說這份 guidance 目的在協助 marketed medical devices 對 cybersecurity threats 具有足夠 resiliency，也處理有 cybersecurity risk 的醫療器材上市前文件。這代表 FDA 看的是 device 在真實系統中的風險，不是 isolated algorithm 的漂亮宣稱。([U.S. Food and Drug Administration][1])

對工程師來說，這頁背後就是 architecture view。你的 Cybersecurity Architecture Views 文件已經把 system workflow 拆成 DICOM query C-FIND、transfer C-MOVE、AI model processing、output C-STORE，也劃分 Internal Protected Boundary 和 External Boundary。這種架構視圖不是為了畫圖好看，而是為了看見 trust boundary、data flow、attack surface 和 shared responsibility。

對主管來說，這頁是資源排序工具。小團隊不可能一開始做所有事情，但至少要知道自己在哪一層。如果還在 model 階段，先把 model release card、SBOM、資料 lineage 做起來；如果已經有 viewer，就必須補 parser/input/cache/output risk；如果已經進 platform，就要補 IAM、API、audit log、backup；如果接醫院網路，就要補 deployment guide、HDO responsibility、incident reporting、downtime fallback。

工作流可以叫「Product Boundary Review」。每次產品新增功能，PM、RD、QA、法規、資安一起問：「我們是不是跨了一層？」新增 viewer，就是跨到 user-facing workflow。新增 database，就是跨到營運責任。新增 PACS/HIS，就是跨到 clinical continuity。每次跨層，都要同步更新 architecture、threat model、risk assessment、testing scope、labeling 和 Patch SLA。

---

# Slide 6｜Evidence, not slogans

這頁是全場知識密度最高的一頁，也是你最容易講太久的一頁。核心句一定要先出來：**法規要的是證據，不是口號。** 你的 Evaluation System 特別說，如果 FDA/TFDA/NIST 只是被命名、沒有被 operational translation，Content Depth 最高只能拿 13/20；所以這頁不能講成法規條文，要翻譯成工程與治理的證據鏈。

FDA 524B 可以壓成幾個義務：monitor、identify、address postmarket cybersecurity vulnerabilities and exploits，包含 coordinated vulnerability disclosure；建立流程以合理確保 device and related systems cybersecure；提供 postmarket updates and patches；提供包含 commercial、open-source、off-the-shelf components 的 SBOM。FDA FAQ 明確列出這些要求。([U.S. Food and Drug Administration][2])

FDA 2026 Guidance 的最新意義是：這些義務要接到 quality management system。FDA 2026 頁面說這份文件提供資安設計、標示和上市前送審文件建議，並取代 2025 年 6 月版本；NSF 的產業評論也指出 2026 更新主要是對齊 QMSR / ISO 13485，核心資安期待如 SPDF、Threat Modeling、Security Architecture、Security Testing、SBOM 仍維持。你的講法可以是：「版本更新不是叫大家重做，而是提醒我們，資安已經進入品質系統語言。」([U.S. Food and Drug Administration][1])

對一般大眾來說，可以用體檢比喻。你說「我很健康」沒有用，你要有檢查數據、醫師判讀、追蹤紀錄。醫療器材資安也一樣，你說「我們很安全」沒有用，你要有 architecture、threat model、risk assessment、controls、testing、finding disposition、patch/retest records。

對工程師來說，這頁要講的是 traceability。你的附件已經有完整證據鏈：Risk Management Report 摘要風險方法、mitigation、testing、residual risks、traceability matrix、post marketing plan；Threat Model 用 STRIDE 找威脅；Controls 把 requirements 對到 design ID；Testing 把 test ID 對到 pass/fail；Metrics 定義 patch completion rate、time-to-remediate、time-to-deploy。這就是 risk → control → test → fix → evidence。    

對主管來說，這頁要講成「可稽核的決策鏈」。Risk 是我們怕什麼，Control 是我們做什麼，Test 是怎麼證明有效，Fix 是發現問題後怎麼處理，Evidence 是這一切如何被保存。這條線接不起來，文件再厚也只是資料夾；這條線接得起來，文件才是產品成熟度。

真實案例可以用 FDA 對 Contec/Epsimed patient monitor 的安全通訊。FDA 2025 年更新指出，Contec 的 patch 會完全移除受影響裝置的 networking functionality，使設備只能做 local monitoring。這是很強的例子：修補不一定是「加功能」，有時候是為了把不可接受風險降下來，必須拿掉某個連線能力。([U.S. Food and Drug Administration][8])

工作流可以用「Evidence Chain Ticket」來說。每個 finding 不能只寫「已修」。它要有 Risk ID、Control ID、Test ID、Finding ID、Decision、Retest Evidence、Archive Location。例如 Web UI 權限問題要對應 Spoofing/Elevation of Privilege，控制可能是 JWT/RBAC/default-deny，測試可能是 unauthorized access 或 black-box pen test，decision 可能是 fix now 或 compensate，最後要有 retest result 和 release record。這就是 FDA 想看到的工程閉環。

---

# Slide 7｜Model, governance, stack

這頁是把 Slide 6 的證據鏈翻成公司內部能溝通的三種語言：model evidence、governance language、AI stack security。你的藍圖明確說，NIST 在這裡是 shared language，不是 checklist；AI RMF 的 Govern、Map、Measure、Manage 與 CSF 2.0 的 Govern、Identify、Protect、Detect、Respond、Recover 要分開講，不要硬塞成一張控制表。 

Model evidence 是給法規、臨床和 AI 團隊看的。它要說清楚 intended use、data、V&V、limits。TFDA 在 2020 年公告「人工智慧/機器學習技術之醫療器材軟體查驗登記技術指引」，目的就是提供 AI/ML 醫療器材軟體申請查驗登記資料準備參考。對台灣團隊來說，這代表 AI 不能只說模型很準，而要說清楚用途、資料、驗證和限制。([Taiwan FDA][9])

FDA 的 AI-enabled device software draft guidance 也強調 total product life cycle。FDA 說這份 draft guidance 針對 AI-enabled device software functions 的 marketing submissions，提供支援 FDA 評估 safety and effectiveness 的文件建議，而且反映整個 device TPLC 的風險管理。這很適合支撐你這頁的觀點：AI SaMD 不是一次性送審，而是生命週期管理。([U.S. Food and Drug Administration][10])

Governance language 是給主管、PM、QA、法規和資安共同使用的。NIST CSF 2.0 已明確擴大到所有組織和產業，並加強 governance 與 supply chain；NIST 也在 2026 年發布 AI RMF Trustworthy AI in Critical Infrastructure Profile 的 concept note，目標是幫助 critical infrastructure operators 把 AI trustworthiness requirements 轉成 actionable practices。這代表 AI 風險管理已經從模型團隊內部問題，變成跨供應鏈、跨生命週期、跨角色的治理問題。([NIST][11])

AI stack security 是給工程師看的。不要只保護模型，還要保護 runtime 和 infrastructure。OWASP LLM Top 10 2025 把 prompt injection、insecure output handling、training data poisoning、model DoS、supply chain vulnerabilities 列為 LLM 應用風險；iThome 的導讀也把 2025 LLM 風險整理成提示詞注入、敏感資訊揭露、供應鏈風險、資料與模型投毒、不當輸出處理、過度代理授權等。即使你的產品不是 LLM，這些趨勢也提醒觀眾：AI security 已經擴展到 input、output、data、model、supply chain、runtime。([OWASP Foundation][12])

對一般大眾來說，這頁可以這樣講：一個可信 AI 團隊要回答三種問題。第一，模型到底能做什麼、不能做什麼。第二，公司誰負責風險決策。第三，模型跑起來的軟體和環境安不安全。這三個少一個，都不是完整的產品安全。

對工程師來說，這頁背後可以接你的 Risk Assessment。文件中用 NIST SP 800-30 的 likelihood、impact、risk matrix 來評估風險，並把 acceptance criteria 設為 High / Very High 必須在 release 前解決，所有 residual risks 要降到 Moderate 或 Low 並持續監控。這就是把技術發現轉成治理決策。

工作流可以叫「三層治理審查」。Model behavior 欄放 intended use、data split、V&V、model limits。Software stack 欄放 SBOM、provenance、isolation、updates、signing、runtime controls。Clinical workflow 欄放 user roles、human-in-the-loop、continuity、fallback、residual risk。每次 design review 都用這三欄問一次，就不會讓模型、工程、法規各講各的。

---

# Slide 8｜Scale 1–2：Model 到 Viewer

這頁要把四層尺度的前兩層講清楚。Scale 1 是 Model，Scale 2 是 Viewer。你的藍圖說得很好：Model 階段要有 artifact、data lineage、SBOM、update boundary；Viewer 階段加入 parser、upload、cache、output interpretation。

Scale 1 的核心是「模型本身就是資產」。一般人可能以為模型只是檔案，但對醫療 AI 來說，model artifact 包含來源、版本、訓練資料脈絡、驗證結果、dependency、hash/signature、更新邊界。只要模型被替換、被竄改、用錯版本，臨床輸出就可能不可信。

你的 SBOM 文件很適合做備稿例子。它記錄 DeepBT Detector-Plus 使用 Python 3.8+、Node.js 20+、Docker、WSL2、DCMTK、JSON，並透過 Docker-based deployment 鎖定 dependency 版本；文件也說外部依賴來自 PyPI、npm 等官方 repositories，內部元件透過版本控制追蹤來源與變更歷史。這些不是文書細節，而是「模型產品如何被追溯」的基本功。

Scale 2 的核心是「viewer 把模型變成使用情境」。一旦有 viewer，就有人上傳檔案、讀取 DICOM、看畫面、理解 AI 輸出。攻擊者不一定要攻擊模型，他可以攻擊 file parser、malformed DICOM、cache、UI error message、output interpretation。

真實案例可以用 MicroDicom DICOM Viewer。NVD 對 CVE-2025-35975 的描述指出，MicroDicom DICOM Viewer 有 out-of-bounds write 漏洞，攻擊者可透過讓使用者開啟惡意 DCM 檔執行任意程式碼；CISA 也發布過相關 medical advisory。這是非常適合 Slide 8 的真實案例，因為它證明 viewer/parser 不是「包裝層」，而是真正攻擊面。([NVD][13])

對一般大眾來說，可以用「考卷和閱卷系統」比喻。模型像老師，viewer 像把考卷拿給老師看的系統。如果有人拿來一份格式怪怪的考卷，閱卷系統一打開就中毒，老師再聰明也沒用。醫療 AI 的 viewer、parser、upload flow 就是這個閱卷系統。

對工程師來說，這頁可以連到你的 Architecture Views 和 Controls。Temporary DICOM Storage 要保護，AI model files 要做 code signing，DICOM transmission 要做 application-level integrity checks，錯誤訊息只能顯示 brief error code，避免 stack trace、internal path、library version 外洩。這些控制直接對應到 viewer / parser / cache / output 的使用情境。 

工作流上，Scale 1 要建立 model release card：model version、training/validation dataset references、performance metrics、known limitations、SBOM、hash/signature、approved intended use。Scale 2 要建立 viewer input safety workflow：DICOM conformance validation、file size/type checks、malformed file testing、fuzzing、temporary data encryption、automatic cache deletion、generic error message、output limitation notice。這樣你就不是只說「viewer 有風險」，而是說出 viewer 的治理路徑。

---

# Slide 9｜Scale 3–4：Platform 到 Connected Medical System

這頁把風險從產品介面推進到公司營運和臨床連續性。Scale 3 是 Platform / Database；Scale 4 是 Connected Medical System。你的藍圖設定這頁要呈現 vendor-owned、shared、hospital-owned risk zones，這很關鍵，因為醫療 AI 的資安不是廠商單方面能完成，也不是醫院單方面能完成。

Scale 3 的核心是：一旦有 platform / database，就開始有身份、權限、API、資料庫、audit log、backup。這時候風險不只是「產品有漏洞」，而是公司營運風險。資料外洩會影響品牌與合規，API 被濫用會影響服務，audit log 不完整會影響事件調查，backup 不可用會影響恢復。

你的 Risk Assessment 文件裡，S2 是 Web UI user accounts 被 valid credentials impersonation 影響，I2 是 sensitive data 透過 insecure storage 外洩，D1 是 local server 被 excessive requests 造成不可用，E1 是 container breakout / privilege escalation。這些都是平台化後必須面對的風險。

Scale 4 的核心是：一旦接入 hospital network、PACS/HIS、update server、remote service，風險就變成 clinical continuity。你的 Architecture Views 明確寫出，DeepBT Detector-Plus 是 standalone software installed on local workstations，直接與 PACS 互動，使用 C-FIND、C-MOVE、C-STORE，且不支援 cloud storage、remote connections 或 external internet access，以限制外部暴露。這個設計可以作為「降低產品邊界風險」的例子，但也要誠實說：只要接醫院 LAN，就仍有內部橫向移動風險。

真實案例可以用 Synnovis。NHS 說 Synnovis cyber incident 後，該公司花了很長時間恢復服務，直到 2024 年 12 月才 fully restored；攻擊者也在 2024 年 6 月發布竊取的資料。這個案例說明醫療供應商被攻擊時，影響的不是單一產品，而是服務恢復、資料風險、臨床 workflow 和公眾信任。([NHS England][14])

另一個本地例子是馬偕事件。iThome 報導指出，2025 年 2 月 11 日馬偕遭 CrazyHunter 攻擊，數百台電腦當機，掛號系統受波及，影響上百名病患；後續確認影響範圍主要是臺北淡水兩區急診室。這很適合在 Slide 9 或 Slide 10 做一句提醒：「醫療資安事件不是抽象，它會碰到急診、掛號、病歷、臨床流程。」([iThome][15])

對主管來說，這頁可以借金融業類比：金融業談交易不中斷，通訊業談連線不中斷，能源談供應不中斷；醫療這裡談的是 clinical continuity。這句已經在你的 talk design 裡，建議保留。它能讓主管一秒理解：資安不是成本中心，而是服務不中斷能力。

工作流上，Scale 3 要建立 platform security baseline：MFA/RBAC、API authz、rate limit、audit log、encryption-at-rest、backup/restore drill。Scale 4 要建立 connected deployment checklist：isolated VLAN、Default-Deny host firewall、allowed PACS IP/AE Title、DICOM-TLS 或 VPN、log forwarding to SIEM/SOC、secure update channel、manual update window、downtime fallback、hospital IT contact、incident reporting route。你的 Labeling 文件已經把 HDO responsibility、isolated VLAN、Default-Deny、port usage、incident reporting、secure update practice 寫進使用者 guidance，這是非常好的落地證據。

---

# Slide 10｜Cyber Safety Is Patient Safety

這頁是全場情緒高點。畫面只要一句話：**Cyber Safety Is Patient Safety。** 你的 Evaluation System 和 Rehearsal Workflow 都暗示這頁不能被稀釋，因為它是 audience impact 的中心。這頁不能放 checklist、不能放 framework、不能放戲劇化醫院照片。 

這句話不是口號。FDA 2026 Guidance 的基本方向就是讓醫療器材面對 cybersecurity threats 有足夠 resiliency，因為器材或醫療系統不可用、不可信、不可修時，會影響安全性與有效性。對你的講法來說，這頁要把 CIA triad 翻成醫療語言：Availability 不是系統 uptime 而已，是醫師能不能在需要時取得結果；Integrity 不是資料沒被改而已，是醫師能不能相信輸出；Repairability 不是工程流程而已，是出事後能不能安全恢復。([U.S. Food and Drug Administration][1])

ECRI 2026 Top Health Technology Hazards 也支撐這個觀點。ECRI 把 healthcare AI chatbots misuse 列為 2026 重要 health technology hazard，並同時提醒「systems outages / digital darkness」等問題；ECRI 說 LLM 工具雖然回答看起來權威，但並非為醫療目的設計或驗證，錯誤建議可能影響 patient safety。這可以作為你在 Slide 10 的補充：「AI 的風險不是只有資安，也包含錯誤信任、錯誤使用、系統中斷。」([ECRI and ISMP][16])

真實世界案例再一次可以串起來。Change Healthcare 顯示第三方醫療基礎設施中斷會影響 patient care 和財務；Synnovis 顯示病理檢驗服務中斷可能拖到數月恢復；馬偕顯示台灣醫院急診系統也會被勒索攻擊干擾；Contec 顯示醫療設備漏洞修補可能直接改變設備功能，例如移除 networking functionality。這些案例共同支持一句話：醫療資安不是 IT 口號，而是照護連續性。([American Hospital Association][6])

對一般大眾來說，可以說：「如果系統不能用，醫師就要改走人工流程；如果資料不可信，醫師就要重做確認；如果漏洞修不了，醫院就要承擔長期風險。」對工程師來說，這句話是在提醒，每個 security finding 都要補 clinical impact。對主管來說，這句話是在提醒，資安預算不是買工具，而是買臨床流程的韌性。

工作流可以叫「Cyber-to-Clinical Translation」。每個 risk register 裡都加一欄 clinical impact：這個漏洞會影響 confidentiality、integrity、availability 哪一項？是否會造成 AI result 不可信？是否會造成臨床流程延遲？是否會造成多病人資料暴露？是否需要 downtime fallback？是否需要 hospital advisory？這一欄會讓醫師、主管、QA、法規、資安真的講同一種語言。

上台這頁要慢。說完「Cyber Safety is Patient Safety」停一拍。不要急著補案例。讓那句話先進到觀眾腦中，再補一句：「不是因為資安人員想把自己講得很重要，而是因為醫療現場已經告訴我們：系統中斷，很快就會變成照護中斷。」

---

# Slide 11｜White-box + Black-box

這頁開始進入實作，但不能變成工具清單。你的新版藍圖其實更精準：標題是「Testing Portfolio: What Question Does Each Test Answer?」也就是每一種測試都要回答一個決策問題。這比單純講 white-box / black-box 更成熟。

對一般大眾來說，white-box 像老師看你的解題過程，black-box 像考官只看你能不能被騙過。White-box 是從內部看：code、config、dependency、container、secret、SBOM。Black-box 是從外部看：登入、API、viewer、upload、network exposure、攻擊路徑能不能串起來。

對工程師來說，這頁的關鍵是每個測試回答不同問題。SBOM / SCA 回答「我用了什麼元件，有沒有已知漏洞」。White-box 回答「release 前有哪些便宜、可修、可追溯的問題」。Fuzz / abuse case 回答「異常輸入會不會打壞流程」。Black-box 回答「外部看得到什麼」。Pen test 回答「漏洞能不能被串成真實攻擊」。Retest 回答「修補是否真的成立」。

你的 Cybersecurity Testing 文件很適合當備稿。CS.T001 測 unauthorized access，CS.T002 測 bcrypt password hashing，CS.T005 測 network isolation、host-based firewall、secure DICOM transmission，CS.T006 測 encryption-at-rest 和 model protection，CS.T009 測 audit logging，CS.T010 測 Docker recovery，CS.T011 測 secure update / version locking，CS.T012 是 external black-box penetration test，CS.T013 是 internal vulnerability scan。這就是 testing portfolio，而不是工具堆疊。

真實案例可以再次用 MicroDicom。DICOM viewer 類漏洞提醒我們：malformed file testing 和 parser robustness 不是 optional。只要使用者開一個惡意 DCM 檔就可能觸發任意程式碼執行，這對任何處理醫療影像的產品都是很具體的威脅。([NVD][13])

對主管來說，這頁的重點是：「測試不是為了報告好看，而是為了產出決策。」如果測試結果沒有 owner、severity、due date、fix decision、retest evidence，它就只是外包報告。你的 Unresolved Anomalies 文件寫到，綜合 Threat Modeling、Risk Assessment、外部 Penetration Testing 後，沒有超過可接受風險門檻的 unresolved anomalies；所有 identified vulnerabilities 已被 remediated 或 mitigated 到 Low residual risk。這就是主管聽得懂的結論：不是測過，而是風險收斂了。

工作流可以是「Testing-to-Finding Pipeline」。先定義 scope：Web UI、API、DICOM port、temporary storage、AI model files、update path。再執行 white-box：SAST、SCA、secret scan、container config、SBOM matching。再執行 black-box：auth bypass、API abuse、DICOM handling、network scan、pen test。接著把 findings 進入 Patch SLA，修補後 retest，最後 archive evidence。這樣 testing 就變成治理的前一站，而不是演講裡的工具名詞。

---

# Slide 12｜Patch SLA

這頁是全場營運高潮。你的 Talk Design 明確把「沒有 decision，就沒有治理；沒有證據，就沒有信任」列為 memory anchor；Rehearsal Workflow 也要求 Slide 12 的 Decision node 必須視覺與語言上都是中心。 

這頁要先講清楚一件事：Patch SLA 不是 FDA 原文裡的一個固定術語，而是你把 FDA 524B 的 updates / patches、reasonable time、CVD、postmarket vulnerability management 翻譯成公司 operating model。這個翻譯很重要，因為主管不一定懂 524B，但一定懂 SLA、owner、severity、due date、decision、evidence。

FDA 524B 要求 cyber device sponsor 提供上市後監控、識別、處理漏洞與 exploit 的計畫，包含 CVD；也要能提供 updates and patches 與 SBOM。這些要求落到公司內部，就會變成：漏洞進來誰收？誰判斷是否適用？誰定嚴重度？誰決定 fix now、compensate、defer、not applicable？誰通知客戶？誰重測？證據放哪？([U.S. Food and Drug Administration][2])

你的 Management Plan 已經把這件事做得很有層次。它採 dual-track：Critical vulnerabilities 走 expedited mitigation，目標是在風險確認後 15 calendar days 內發 Security Advisory 與 validated compensating controls，30 calendar days 內完成 Risk Mitigation Plan；非 critical 或已被 network isolation/default-deny firewall 有效緩解的漏洞，合併到 periodic security update cycle。它也明確寫出 Safety Override：如果 patch 可能影響 AI model accuracy、DICOM structure 或 system stability，patient safety 和 clinical effectiveness 要優先於標準 security SLA。

這一點很有內涵，因為醫療產品不是一般 SaaS。一般 SaaS 可能說「critical patch 立即上」，但醫療 AI 要問：「這個 patch 會不會改變模型輸出？會不會影響 DICOM 結構？會不會破壞臨床驗證？」所以醫療 AI 的 Patch SLA 不是越快越好，而是**越快控制風險，同時不能破壞 patient safety**。

你的 Controls 文件也把這件事落到工程：CS.D014 採 immutable infrastructure，不在 running container 裡 patch individual files，而是替換整個 digitally signed container image；如果 security patch 可能影響 AI model integrity，更新要暫停直到臨床驗證完成，並優先採 compensating controls。

你的 Metrics 文件讓這頁更像主管語言。它定義 Patch Completion Rate、Time-to-Remediate、Time-to-Deploy，並且說 Time-to-Deploy 的 stop point 可以是 update package 透過 secure channel 提供給客戶，或 Security Advisory / compensating control 送達指定窗口；客戶端 change management 造成的延遲不應算成製造商內部績效缺失。這非常務實，因為醫療現場更新常受 HDO 變更管理控制。

真實案例仍然是 Contec/Epsimed patient monitor 最適合。FDA 說 Contec patch 會移除 networking functionality，讓設備只能 local monitoring；同時 FDA 也提醒病患與照護者不要自行安裝，應由 healthcare facility IT/security staff 取得 patch 和安裝說明。這個案例非常精準地說明：Patch SLA 包含安全、臨床、安裝責任、客戶溝通，不是「發一包更新檔」而已。([U.S. Food and Drug Administration][8])

工作流可以講得非常清楚：Intake，漏洞從內部測試、客戶通報、CISA KEV、NVD、供應商公告進來。Triage，判斷是否適用產品、是否可被利用、是否影響臨床安全。Decision，決定 fix now、compensate、defer with timeline、not applicable with rationale。Action，發 Security Advisory、修 patch、補 firewall rule、更新 configuration、或記錄 risk acceptance。Retest，重測控制是否有效。Archive，保存 advisory、risk rationale、test report、release note、customer notification。這就是你的 Patch SLA operating model。

---

# Slide 13｜Small Team 30 / 60 / 90

這頁要把壓力降下來，但不是把標準降低。你的藍圖把 30 / 60 / 90 定義為 adoption scaffold，不是法規要求，也不是固定 SLA 格式。這句很重要，因為你不能讓觀眾誤以為 FDA 要求一定 30/60/90；你是在提供小團隊啟動第一個 evidence loop 的方式。

對一般大眾來說，30 / 60 / 90 可以這樣理解：第一個月先把房子畫出平面圖，第二個月開始裝門鎖和監視器，第三個月找外部人員來測試門有沒有真的鎖上。重點不是三個月變完美，而是三個月後，團隊不再靠口頭記憶做資安，而是開始留下可重複的證據。

30 天的目標是讓產品看得見。小團隊要做 inventory、SBOM、data flow、intended use、known vulnerabilities。你的 SBOM 和 Architecture Views 已經示範應該盤點什麼：產品元件、外部依賴、硬體需求、DICOM workflow、Internal Protected Boundary、External Boundary、PACS connection、Temporary DICOM Storage、AI model、update path。 

60 天的目標是讓風險進流程。做一次 STRIDE threat modeling workshop，建立 CI security gates，定義 finding workflow，寫 customer security note template。你的 Threat Model 用 STRIDE 分成 S/T/R/I/D/E，並把每一類威脅對應到 cybersecurity requirement ID；這可以變成小團隊最簡單的 workshop 模板。

90 天的目標是外部驗證與修補證據。安排 external black-box pen test、internal vulnerability scan、Patch SLA drill、CVD process、retest evidence、release history cleanup。你的 Testing 文件和 Unresolved Anomalies 文件已經展示這個閉環：測試要有 test ID、tool、method、pass/fail criteria、result；剩餘異常要說清楚是否超過 acceptable risk threshold。 

最新趨勢上，CISA KEV 應該成為小團隊 60/90 天的漏洞優先排序輸入。CISA 表示 KEV Catalog 是已在野被利用漏洞的 authoritative source，組織應該把 KEV 作為 vulnerability management prioritization framework 的輸入。你的 Management Plan 已經寫到用內部工具定期 cross-reference device SBOM against CISA KEV，applicable KEV 會自動歸類成 critical vulnerability，72 小時內完成 applicability assessment，然後進 expedited patching SLA。這是很好的小團隊成熟做法。([CISA][17]) 

對主管來說，30/60/90 的成果要講成三個管理里程碑。30 天後，公司知道自己有什麼。60 天後，公司知道風險怎麼進流程。90 天後，公司有外部驗證和修補證據。這比「我們會持續改善」具體太多，也更容易被董事會、投資人、醫院採購、QA、法規接受。

虛擬案例可以這樣講：一個 8 人 AI 醫療團隊，30 天內畫出 data flow，發現 DICOM cache 沒有明確 retention policy；60 天做 STRIDE，發現 AI model tampering 和 unauthorized PACS access 是高優先風險；90 天做 black-box pen test，發現 login interface 的 TLS/限制不足，先用 IP restriction / firewall compensating control 降風險，再安排正式修補與重測。這不是大型企業才做得到，而是小團隊可以開始的 evidence loop。

---

# Slide 14｜先建立信任，再面對稽核

最後一頁要收束，不要再加入新框架。你的藍圖和 Rehearsal Workflow 都提醒，Slide 14 不能新增內容，不能再放 roadmap，也不能放 contact-heavy content。這頁只要讓聽眾記住最後一句：**先把安全做進產品，法規文件才會自然長出來。**  

這頁的知識核心是 secure-by-design。不是產品做完才找資安補洞，不是送審前才補文件，不是客戶問才產 SBOM，而是在產品設計、開發、測試、部署、上市後維護裡，把安全自然放進每個節點。FDA 2026 Guidance 把 cybersecurity 放在 Quality Management System Considerations 裡，正好支持這個收束：安全不是最後一層貼紙，而是品質系統的一部分。([U.S. Food and Drug Administration][1])

對一般大眾來說，可以用大樓消防比喻。逃生梯、消防警報、撒水系統、緊急照明，不是大樓蓋好才想到，而是設計圖一開始就要有。醫療 AI 也是一樣，資安不是最後加上去的，而是從產品邊界、資料流程、使用者角色、修補流程、事件通報開始就要放進設計。

對工程師來說，這頁是提醒：security evidence 不是報告格式，而是平常工程工作留下的痕跡。Threat model 不是審查前趕出來，而是架構設計時就做。SBOM 不是客戶問才整理，而是 build artifact。Testing 不是外部報告而已，而是 release gate。Patch SLA 不是客服話術，而是 finding governance。Retest evidence 不是補洞截圖，而是 repair proof。

對主管來說，這頁的句子要落在責任：成熟團隊不是文件最多，而是每個風險都知道怎麼證明、怎麼修、怎麼追。你的附件其實已經有一套完整 evidence package：Risk Management Report、Threat Model、Risk Assessment、SBOM、Safety/Security Vulnerability Assessment、Unresolved Anomalies、Controls、Architecture Views、Testing、Management Plan、Metrics、Labeling、Software Level of Support。這些文件不應被看成「為了 FDA 補的一堆文件」，而應該被看成「產品信任系統的不同視角」。            

最後可以這樣收：「今天我們從一個 model 開始，走到 connected medical system。每往前一步，產品更有價值，也更需要被信任、被修補、被稽核。所以我想用一句話結束：先把安全做進產品，法規文件才會自然長出來。真正成熟的團隊，不是文件最多的團隊，而是每一個風險都知道怎麼證明、怎麼修、怎麼追的團隊。謝謝大家。」

---

# 全場再升級的三個「有料」角度

第一個升級點是把 **FDA 2026 Guidance** 講成「資安進入品質系統」，不要只說 FDA 更新了文件。產業評論也指出，2026 版主要是 QMSR alignment，核心技術期待並沒有被推翻；這讓你的演講可以更成熟地說：「真正的重點不是追版本，而是把 cybersecurity evidence 放進 QMS。」([Hattrick][18])

第二個升級點是把 **AI lifecycle** 講進來。FDA AI-enabled device draft guidance 強調 TPLC；FDA PCCP guidance 則支持 AI-enabled devices 在已審查的變更計畫內持續迭代，同時維持 safety and effectiveness。這可以和你的 Patch SLA 形成呼應：AI 醫材不是不能改，而是要知道哪些改動能被預先規劃、哪些改動需要安全/臨床驗證、哪些改動會觸發 regulatory review。([U.S. Food and Drug Administration][10])

第三個升級點是把 **韌性語言** 講出來。台灣國家資安戰略、NIST CSF 2.0、NIST AI RMF critical infrastructure profile、CISA KEV、Change Healthcare、Synnovis、馬偕、Contec 這些趨勢與案例都在說同一件事：資安不是單點防護，而是 product boundary、supply chain、clinical continuity、repairability、evidence 的整體治理。([NIST][11])

一句話總結這一版的更強講法：

**AI 軟體醫材的資安，不是保護一個模型，而是在真實醫療世界裡，建立一個能被信任、能被修補、能被證明的產品系統。**

[1]: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-management-system-considerations-and-content-premarket "Cybersecurity in Medical Devices: Quality Management System Considerations and Content of Premarket Submissions | FDA"
[2]: https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity-medical-devices-frequently-asked-questions-faqs "Cybersecurity in Medical Devices Frequently Asked Questions (FAQs) | FDA"
[3]: https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices "Artificial Intelligence-Enabled Medical Devices | FDA"
[4]: https://www.roche.com/media/releases/med-cor-2026-03-16 "Roche launches NVIDIA AI factory to accelerate the development of new therapeutics and diagnostics solutions"
[5]: https://english.ey.gov.tw/Page/61BF20C3E89B856/3cee52d1-96e4-48e0-b0a3-a7a9ba000ee3 "
	National Cybersecurity Development Program enters seventh phase (Executive Yuan, R.O.C. (Taiwan)-Executive Yuan Press Releases Detail)
"
[6]: https://www.aha.org/news/news/2024-03-15-aha-survey-change-healthcare-cyberattack-having-significant-disruptions-patient-care-hospitals-finances "AHA survey: Change Healthcare cyberattack having significant disruptions on patient care, hospitals’ finances | AHA News"
[7]: https://www.ithome.com.tw/news/167327 "2025年2月馬偕醫院遭勒索軟體攻擊事件歷程總整理（持續更新中） | iThome"
[8]: https://www.fda.gov/medical-devices/safety-communications/cybersecurity-vulnerabilities-certain-patient-monitors-contec-and-epsimed-fda-safety-communication "Cybersecurity Vulnerabilities with Certain Patient Monitors from Contec and Epsimed: FDA Safety Communication | FDA"
[9]: https://www.fda.gov.tw/tc/siteListContent.aspx?id=34961&sid=3787&utm_source=chatgpt.com "人工智慧/機器學習技術之醫療器材軟體查驗登記技術指引"
[10]: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing "Artificial Intelligence-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations | FDA"
[11]: https://www.nist.gov/news-events/news/2024/02/nist-releases-version-20-landmark-cybersecurity-framework "NIST Releases Version 2.0 of Landmark Cybersecurity Framework | NIST"
[12]: https://owasp.org/www-project-top-10-for-large-language-model-applications/ "OWASP Top 10 for Large Language Model Applications | OWASP Foundation"
[13]: https://nvd.nist.gov/vuln/detail/cve-2025-35975?utm_source=chatgpt.com "CVE-2025-35975 Detail - NVD"
[14]: https://www.england.nhs.uk/synnovis-cyber-incident/ "NHS England » Synnovis cyber incident"
[15]: https://www.ithome.com.tw/news/167318 "馬偕醫院傳出遭CrazyHunter勒索軟體持續攻擊，衛福部與資安署已成立快速應變小組協助因應 | iThome"
[16]: https://home.ecri.org/blogs/ecri-news/misuse-of-ai-chatbots-tops-annual-list-of-health-technology-hazards "Misuse of AI chatbots tops annual list of health technology hazards"
[17]: https://www.cisa.gov/known-exploited-vulnerabilities-catalog?utm_source=chatgpt.com "Known Exploited Vulnerabilities Catalog"
[18]: https://www.hattrick-it.com/blog/cybersecurityguidanceupdate/ "FDA Cybersecurity Guidance 2026: What Changed?"
