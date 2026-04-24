# AI 進入高信任產業後：從模型能力走向產品信任

這份版本把原本的 keynote expansion reader 改寫成更成熟、較少對抗感的舞台語言。核心原則是：

> 先承認觀眾原本理解的一層，再把他們帶到下一層。

全場主軸保留為：

> **Boundary -> Evidence -> Decision -> Repair Proof**

也就是先定義產品邊界，再產生相稱證據，接著把 finding 變成決策，最後用修補、重測、通知與上市後監測證明產品可以被持續信任。

---

# 全場大敘事

今天我們從 AI SaMD 出發，但問題會一路延伸到金融與關鍵基礎設施。

AI 一開始常被看成模型能力：準確率、ROC curve、benchmark、demo。這些都重要，它們是進入產品討論的第一步。

真正的挑戰會在產品化之後出現。AI 開始接資料、接 API、接 workflow、接醫院 PACS / DICOM、接銀行交易流程、接 OT / ICS runtime environment。當它進入高信任產業，客戶想確認的會從「它會不會回答」，一路延伸到「它能不能被使用、被追蹤、被修補、被稽核」。

FDA 524B 把 cyber device 的上市後漏洞監測、CVD、postmarket updates and patches、SBOM 拉進產品責任。Threat Modeling 讓團隊看見產品邊界裡的攻擊面。Patch SLA 把漏洞處理從口頭承諾變成 decision workflow。postmarket monitoring 則讓上市後的真實世界風險回到產品生命週期。

今天這場會把這些元素接成一條可執行的產品信任路徑：

1. **Boundary**：先定義 intended use、system boundary、users、data flow、integrations、runtime environment。
2. **Evidence**：邊界清楚後，團隊才能建立 architecture evidence、Threat Modeling、SBOM、risk assessment、controls、test records。
3. **Decision**：finding 進來後，要有 triage、risk acceptance、mitigation、compensating controls、release judgment。
4. **Repair Proof**：最後用 patch records、retest evidence、customer advisories、release history、postmarket monitoring 證明信任可以被維持。

這個改寫會保留 tension，只是讓 tension 從問題自然長出來：

> 如果 AI 很準，但醫院無法確認它如何被使用、如何被修補、如何被追蹤，那它能不能真正進入臨床？

---

# 全場開場逐字稿

「今天我想先問大家一個簡單的問題：一個 AI model 要進入醫院、銀行，或關鍵基礎設施，到底需要被信任的是什麼？」

「準確率當然重要。ROC curve、validation score、benchmark，也都重要。它們讓我們知道模型有沒有資格進入下一階段。」

「但請想像一個病人，明天早上要做放射治療。今天晚上，一個 AI 幫醫師產生腦瘤 contour。模型很準，demo 很漂亮，validation score 也很好。」

「醫院接下來會問的問題會更具體。」

「這個 contour 是哪個 model version 產生的？DICOM 是否正確解析？影像序列是否正確？系統最近有沒有更新？這個版本有沒有已知漏洞？如果明天出現 critical CVE，誰判斷影響範圍？誰通知醫院？多久修？修完怎麼證明？」

「這些問題把我們從模型帶到產品。」

「同樣的事情也發生在金融業。銀行可以欣賞一個 fraud detection model，但真正要放進交易流程時，它需要的是能追蹤 decision、能處理 false positive、能停損、能恢復的風控系統。」

「電力公司也一樣。load forecasting model 可以很強，但如果它接到 dispatch、maintenance ticket、remote operation，團隊就要知道資料從哪裡來、誰能修改、錯誤如何被攔下、出事時如何回復。」

「所以今天這場，我會用 AI SaMD 做主線，因為醫療器材的產品生命週期要求比較清楚。可是我們真正要練習的是一種高信任產業都會需要的思考方式。」

「Boundary。Evidence。Decision。Repair Proof。」

「先知道產品邊界在哪裡，風險才有位置。風險被看見，證據鏈才接得起來。finding 進入決策，修補能力才有辦法被證明。」

「我今天的第一個判斷是：未來 2 到 3 年，醫院、銀行、關鍵基礎設施單位問 AI vendor 的第一個問題，會從『你的模型多準？』慢慢走向『你的產品信任證據在哪裡？』」

---

# Slide 1｜AI 軟體醫材的資安實戰

## 一個問題

**一個 AI model 要進入醫院、銀行或關鍵基礎設施，真正需要被信任的是什麼？**

## 一個故事

「今天這個題目是 AI 軟體醫材的資安實戰。我會從醫療開始，因為 AI SaMD 很早就把模型、軟體、使用情境、上市後維護放在同一張桌上。」

「但這張桌子旁邊，其實還坐著金融、製造、能源、交通和政府系統。」

「AI 原本回答問題。現在 AI 開始接資料、接 API、接 workflow、接 decision、接人命、接錢、接國家關鍵服務。」

「在醫院，它可能影響 contour、triage、diagnosis support、clinical workflow。」

「在銀行，它可能影響詐欺偵測、信用風險、交易阻擋、客戶身份驗證。」

「在電網或水務，它可能影響負載預測、維修排程、異常偵測，甚至 OT 操作建議。」

「不同產業的痛點不一樣，但信任問題很像：這個 AI 進入真實流程之後，團隊能不能說清楚它在哪裡、誰負責、怎麼修、怎麼證明？」

「所以今天如果只能帶走一句話，就是這句：模型是起點，產品信任才是交付責任的地方。」

## 一個決策

**從第一天開始，用 product trust system 管理 AI。**

你的產品資料夾應該從四個核心開始：Boundary、Evidence、Decision、Repair Proof。Boundary 放 intended use、system boundary、users、data flow、integrations、runtime environment。Evidence 放 architecture、Threat Modeling、SBOM、risk assessment、controls、testing。Decision 放 finding triage、risk acceptance、mitigation、compensating controls、release judgment。Repair Proof 放 patch records、retest evidence、customer advisories、release history、postmarket monitoring。

---

# Slide 2｜Required CYBERSEC Disclaimer

## 一個問題

**公開資安演講要怎麼講得有用，同時維持安全、法律與專業邊界？**

## 一個故事

「這一頁是大會必要的 disclaimer。我會讓大家看一下，也想補一句：在醫療、金融、關鍵基礎設施和資安裡，邊界本身就是一種控制。」

「公開演講要避開兩個極端。一端太抽象，大家聽完只覺得重要，卻不知道明天怎麼做。另一端太細，細到變成 exploit recipe、客戶拓樸、內部流程，或讓人誤會照著做就一定合規。」

「所以今天我會講方法、決策、證據鏈與產品治理。我會避開私人客戶細節、可直接複製的攻擊步驟，也會避免把任何法規內容包裝成醫療或法律建議。」

「這呼應今天的第一個主題：Boundary。」

「產品裡，邊界清楚，風險才清楚。演講裡，邊界清楚，責任也才清楚。」

## 一個決策

**公開溝通的第一個安全控制，是定義揭露邊界。**

這頁講完立刻轉入主軸。它的功能是建立專業邊界感，讓觀眾知道今天會得到可執行的產品治理方法，而非攻擊教學或法律承諾。

---

# Slide 3｜模型只是起點

## 一個問題

**醫院採購 AI 時，真正承接的是模型能力，還是產品責任？**

## 一個故事

「我們從 AI 團隊最常遇到的轉折開始。」

「很多團隊一開始是在做模型。這很合理，因為沒有模型能力，就沒有後面的產品。」

「下一層問題會在產品化後出現。你不會買一顆很厲害的引擎，然後期待它自己變成一台安全的車。引擎再強，如果煞車不穩、儀表板亂顯示、保養紀錄不存在、召回流程不清楚，沒有人敢讓它上路。」

「AI model 像引擎。SaMD 是整台車。」

「醫院要的是能上臨床道路的整台車。它要知道 intended use、human-in-the-loop、輸入資料、輸出限制、patch、incident reporting、downtime workflow。」

「銀行採購 fraud model 也會走到同樣問題。模型可以很準，但交易流程需要追蹤 decision、處理 false positive、管控 API 權限、保留 audit log。」

「電力公司採用 forecasting model 也一樣。當模型進入 operation，它就需要治理、監控、fallback 和 human override。」

「所以醫療現場會問：輸入影像是否正確？DICOM metadata 有沒有缺漏？輸出結果是否需要醫師確認？使用者有沒有可能誤解 AI 結果？暫存資料多久刪？誰能看？系統壞了怎麼回復？漏洞出現誰修？」

「這些問題大多不在模型準確率裡，但它們都會影響產品信任。」

## 一個決策

**每個 AI 團隊都要做一張 Responsibility Map。**

這張圖要回答：誰使用？在哪個流程使用？輸入是什麼？輸出是什麼？輸出能不能直接用？誰確認？資料暫存多久？異常怎麼處理？誰能更新？漏洞怎麼通報？修補怎麼證明？

---

# Slide 4｜AI 變成基礎設施

## 一個問題

**當 AI 從 demo 進入醫療、金融與關鍵基礎設施，失敗會長什麼樣子？**

## 一個故事

「現在我們把視角拉高一點。」

「AI 最早像玩具，後來變成工具，接下來正在變成基礎設施。」

「這句話聽起來很大，但我們看現實。醫療與生命科學公司已經把 AI factory 當成研發、診斷、臨床試驗和大規模資料洞察的 operating backbone。金融機構把 AI 放進交易、詐欺偵測、身份驗證與風控流程。關鍵基礎設施把 AI 放進異常偵測、維修排程與操作建議。」

「當 AI 變成 backbone，風險就改變了。」

「以前 model 出錯，可能是一個 prediction 錯。現在 infrastructure 出錯，可能是一整段流程停。」

「在醫療裡，這叫 clinical workflow disruption。」

「在金融裡，這叫 payment、settlement、fraud operation、customer trust disruption。」

「在關鍵基礎設施裡，這叫 operation disruption。更白話一點，就是燈會不會亮、水會不會流、交通會不會正常。」

「Change Healthcare 事件讓我們看到第三方醫療基礎設施中斷可以多嚴重。AHA 調查接近一千家醫院，74% 回報直接病人照護受到影響，94% 回報財務影響。」

「Synnovis 事件也提醒我們，醫療供應商被打之後，服務恢復與資料調查可能拖很久。」

「台灣也有自己的提醒。2025 年馬偕紀念醫院遭 CrazyHunter 勒索軟體攻擊，公開報導指出攻擊路徑涉及 AD 主機派送惡意程式與 BYOVD，衛福部 H-ISAC 也發出警訊。」

「這些案例不需要被包裝成恐慌。它們只是告訴我們：AI 進入高信任流程後，風險會從 AI risk 延伸成 infrastructure risk。」

## 一個決策

**把 AI deployment 畫成 infrastructure map。**

這張圖要畫 model、runtime environment、identity、API、data storage、logs、update path、SIEM/SOC、customer environment、fallback workflow。醫療要畫 PACS / DICOM / viewer，金融要畫 transaction stream / fraud operation / case management，關鍵基礎設施要畫 IT / OT / ICS boundary 與 human override。

---

# Slide 5｜Risk grows with architecture

## 一個問題

**同一個 AI model，放在不同產品邊界裡，資安責任會一樣嗎？**

## 一個故事

「我們現在要談一張很重要的地圖。」

「同一個 AI model，放在不同 architecture 裡，風險完全不同。」

「Scale 1 是 Model。你要問：這個模型從哪裡來？版本是什麼？hash 是什麼？有沒有被換掉？dependency 在哪裡？」

「Scale 2 是 Viewer。你要問：不可信輸入進來時，parser 會不會出事？暫存資料會不會外洩？使用者會不會誤解 output？」

「Scale 3 是 Platform。你要問：誰能登入？誰能查資料？API 能不能被濫用？log 能不能支撐調查？」

「Scale 4 是 Connected System。你要問：當它接進醫院、銀行或 OT，它中斷時誰知道？誰能停？誰能復原？誰能通知客戶？」

「風險變大，通常是因為產品長大了，連接更多，責任也更重。」

「很多 AI 團隊痛苦的原因，是他們已經在做 Scale 3 或 Scale 4 的產品，卻還用 Scale 1 的管理方式。」

「這就像車子已經開上高速公路，安全規則還停在停車場練習。問題會在速度變快、連接變多、責任變重之後出現。」

## 一個決策

**每次產品新增功能，都做一次 Boundary Review。**

新增 viewer，就是從 model 跨到 user-facing workflow。新增 database，就是跨到 platform responsibility。新增 PACS / HIS / transaction / OT integration，就是跨到 connected system。每跨一層，就要更新 architecture、Threat Modeling、testing scope、labeling、Patch SLA、customer responsibility。

---

# Slide 6｜Evidence, Not Slogans

## 一個問題

**當團隊說「我們很安全」，可以拿什麼證明？**

## 一個故事

「現在我們進入法規。但先不要緊張，我不會開始朗讀 FDA 文件。公開朗讀法規，是讓會場進入集體靈魂出竅最快的方法之一。」

「我們把 FDA 524B 翻成產品語言。」

「一家公司說自己很安全，這句話本身還不夠。醫師不會只聽病人說『我覺得我很健康』，就完成健康檢查。醫師要看血液檢查、影像、病史、追蹤紀錄、異常處理。」

「醫療器材資安也一樣。團隊要拿得出 architecture、Threat Modeling、risk assessment、controls、testing、finding decision、patch record、retest evidence。」

「FDA 524B 的要求看起來像法規，但背後很務實。cyber device sponsor 要有上市後監控、識別與處理 vulnerabilities and exploits 的計畫，包含 CVD、postmarket updates and patches，以及 SBOM。」

「金融業也走同一條路。銀行會問第三方風險、營運韌性、事件通報、供應鏈、復原能力。」

「關鍵基礎設施也一樣。電網、水務、交通會問：這個 AI system 在 high-stakes environment 裡是否 worthy of trust。」

「所以這頁保留全場唯一一句強 anchor。」

## 一個決策

**每個 finding 都要變成 Evidence Chain Ticket。**

一個 finding 要能串起來：Risk ID -> Control ID -> Test ID -> Finding ID -> Decision -> Retest Evidence -> Archive Location。這樣團隊才知道風險從哪裡來、怎麼控制、怎麼測、怎麼判斷、怎麼修、怎麼證明。

---

# Slide 7｜Model, Governance, Stack

## 一個問題

**同一個 AI 風險，模型團隊、資安團隊、法規團隊和主管要怎麼講同一種語言？**

## 一個故事

「接下來我們談很多公司真正卡住的地方：語言。」

「同一個 AI risk，在公司裡通常會變成四種語言。」

「AI engineer 會說：這可能是 data drift。」

「資安工程師會說：這可能是 input tampering。」

「法規同事會說：這會不會影響 intended use？」

「主管會說：這會不會延後上市？會不會讓客戶不買？」

「四個人可能都在講同一件事，但像在四個頻道。會議開完，大家都很專業，下一步卻不清楚。」

「高信任產業需要翻譯。」

「第一種語言是 model evidence：intended use、dataset、validation、limitation、performance monitoring。」

「第二種語言是 governance language：owner、severity、acceptance criteria、residual risk、release decision。」

「第三種語言是 stack security：SBOM、model integrity、runtime isolation、secrets、API access、logging、update path。」

「如果這三種語言接不起來，問題就會漂浮在組織裡。AI 團隊覺得那是資安問題，資安團隊覺得那是產品問題，法規覺得那是送審問題，主管覺得那是工程問題。」

「高信任產業裡，漂浮的 risk 最後常常會變成事件。」

## 一個決策

**建立 Risk Translation Sheet。**

每個重要風險都要同時寫三欄：Model impact、Security impact、Business / clinical / operational decision。醫療寫 clinical impact，金融寫 customer / transaction / regulatory impact，關鍵基礎設施寫 safety / continuity / OT impact。

---

# Slide 8｜Scale 1-2：Model 到 Viewer

## 一個問題

**攻擊者真的需要攻擊 AI model，還是攻擊 viewer、parser、input workflow 就足夠？**

## 一個故事

「現在我們回到四層地圖的前兩層：Model 和 Viewer。」

「很多人談 AI 資安，第一反應是 model attack。Data poisoning、model inversion、adversarial example，聽起來很高級，也很適合放在投影片上。」

「攻擊者的選擇通常更務實。」

「如果 parser 比 model 好打，攻擊者會選 parser。如果 API token 比 neural network 好偷，攻擊者會選 token。如果一個惡意 DICOM 檔可以讓使用者打開，攻擊者就不需要理解你的 loss function。」

「醫療影像是一個很好的例子。」

「你有一個 AI model，可以分析 MRI。很好。但這個 model 前面通常會有 DICOM workflow、viewer、parser、upload、temporary storage。這些環節出問題，模型再準也無法保護整個產品。」

「NVD 對 CVE-2025-35975 的描述指出，MicroDicom DICOM Viewer 有 out-of-bounds write vulnerability，使用者只要開啟惡意 DCM 檔，就可能讓攻擊者執行任意程式碼。」

「這提醒我們：攻擊者可能繞開 AI 的核心，直接碰 AI 周圍那一圈。」

「金融業也一樣。fraud model 很好，但 case management 權限錯誤、API abuse、第三方 webhook 被竄改，都會讓模型在錯誤環境裡做出看似合理的判斷。」

「關鍵基礎設施也一樣。predictive maintenance model 可以很強，但 sensor data pipeline、agent identity、OT gateway、update package 出問題，AI 可能會很認真地幫你做錯事。」

## 一個決策

**Scale 1 建 model release card；Scale 2 建 input/output safety gate。**

Model release card 要記錄 model version、hash/signature、training/validation reference、intended use、known limitations、dependency、SBOM、release owner。Input/output safety gate 要處理 DICOM conformance、malformed input、file size/type、cache encryption、cache retention、generic error message、output limitation notice、human review reminder。

---

# Slide 9｜Scale 3-4：Platform 到 Connected Medical System

## 一個問題

**當 AI 產品接進醫院、銀行或 OT 系統後，資安事件會如何擴散成營運問題？**

## 一個故事

「現在進入 Scale 3 和 Scale 4。」

「Scale 3 是 platform。你開始有帳號、資料庫、API、audit log、backup、admin action。」

「Scale 4 是 connected system。醫療是 PACS / HIS / hospital network。金融是 core banking、payment rail、fraud operation、第三方金融科技供應鏈。關鍵基礎設施是 IT / OT / ICS。」

「這一層開始，資安事件會沿著連接面擴散。」

「在醫療裡，它會變成 clinical continuity。」

「在金融裡，它會變成 financial operational resilience。」

「在關鍵基礎設施裡，它會變成 service continuity，有時候甚至是 safety。」

「Synnovis 事件提醒我們，醫療供應商被攻擊後，服務恢復可以拖很久，資料調查也可能非常複雜。」

「Change Healthcare 事件提醒我們，第三方醫療基礎設施一中斷，醫院、病人、現金流會一起受到影響。」

「金融業也早就面對同樣壓力。FS-ISAC 把 supply chain risk、geopolitical shifts、fraud、emerging technologies 放在全球金融系統韌性的核心。」

「這些案例都指向同一個結論：當你的產品接進別人的流程，你就進入 shared responsibility。」

「成熟做法是把 responsibility boundary 寫清楚。哪些是 vendor 負責，哪些是 customer 負責，哪些需要共同演練，哪些事件需要通知，哪些情況要啟動 downtime fallback。」

## 一個決策

**Scale 3 建 platform security baseline；Scale 4 建 shared responsibility + downtime fallback plan。**

Platform baseline 要包含 MFA、RBAC、API authorization、rate limiting、audit log、encryption-at-rest、backup/restore drill、admin logging、customer data separation。Connected system plan 要包含 network segmentation、allowlist、DICOM-TLS 或 VPN、default-deny firewall、SIEM forwarding、manual update window、downtime fallback、incident contact、customer advisory template。

---

# Slide 10｜Cyber Safety Is Patient Safety

## 一個問題

**資安什麼時候會變成病人安全、金融穩定或關鍵服務連續性問題？**

## 一個故事

「這一頁只有一句話：Cyber Safety Is Patient Safety。」

「我想把它稍微擴大：Cyber Safety Is Operational Safety。」

「在醫療裡，它是 patient safety。在金融裡，它是 market trust 和 customer protection。在關鍵基礎設施裡，它是 public safety 和 service continuity。」

「資安人常講 CIA：Confidentiality、Integrity、Availability。這些字很正確，但對非資安人員來說，它們需要被翻譯成現場語言。」

「Availability 在醫療裡，是醫師需要結果時，系統能不能用。」

「Integrity 在醫療裡，是醫師能不能相信這個 AI output。」

「Confidentiality 在醫療裡，是病人資料與病人信任能不能被保護。」

「Repairability 在醫療裡，是出事後產品能不能安全恢復。」

「金融業也一樣。availability 是交易能不能繼續，integrity 是交易與風控 decision 能不能被信任，repairability 是銀行能不能在攻擊後恢復營運。」

「電網的 availability 和 integrity 更直接，因為錯誤可能不只停留在報表，而會碰到實體世界。」

「FDA 對 Contec / Epsimed patient monitor 的 safety communication 很適合放在這裡。該 patch 會移除受影響設備的 networking functionality，讓設備只能 local monitoring。這代表資安修補在醫療設備裡會直接改變功能、臨床使用方式與現場責任。」

## 一個決策

**每個 security risk 都要加一欄 clinical / operational impact。**

醫療要問：會不會讓 AI output 不可信？會不會延遲診療？會不會讓醫師拿不到影像或結果？會不會需要 downtime workflow？金融要問：會不會造成交易錯誤、客戶損失、fraud false negative、監管通報？關鍵基礎設施要問：會不會造成 physical process disruption、manual override、safety interlock 壓力？

---

# Slide 11｜White-box + Black-box

## 一個問題

**測試要回答哪一個產品決策？**

## 一個故事

「現在談測試。」

「測試報告常常很漂亮，封面很好看，表格很多，最後大家都很安心。直到下一次事件發生。」

「成熟的 testing portfolio 會先問：每一種測試回答哪一個決策問題？」

「SBOM / SCA 回答：我們用了什麼？有沒有已知漏洞？」

「White-box 回答：release 前有哪些便宜、可修、可追蹤的問題？」

「Secret scan 回答：金鑰、密碼、debug config 有沒有進到產品？」

「Malformed input / fuzz test 回答：異常輸入會不會打壞 viewer、parser、workflow？」

「Black-box 回答：攻擊者從外面看得到什麼？」

「Pen test 回答：這些弱點能不能串成真實 attack path？」

「Retest 回答：修完是否真的有效？」

「測試的價值不只在 finding 數量，而在 finding 能不能進入 owner、severity、due date、fix decision、retest evidence。」

「金融業現在很重視 resilience。EBA 對銀行業的 risk assessment 也指出，cyber、ICT-related threats、fraud 和 legal risks 會同時造成直接財務損失與韌性疑慮。」

「所以 testing portfolio 的目的，是證明團隊有能力看見風險、治理風險、修補風險。」

## 一個決策

**把 testing 接到 finding workflow，再接到 Patch SLA。**

每個測試項目都要有 test objective、scope、pass/fail criteria、finding owner、severity criteria、fix decision、retest plan、evidence location。這樣 testing 才會從一次性活動變成治理能力。

---

# Slide 12｜Patch SLA

## 一個問題

**漏洞出現時，團隊靠英雄救火，還是靠決策系統？**

## 一個故事

「這是今天最重要的一頁：Patch SLA。」

「Patch SLA 很容易被誤解成天數表。Critical 幾天、High 幾天、Medium 幾天。天數有用，但天數只是外層。」

「核心是 decision。」

「漏洞進來時，團隊要判斷：它跟我們有沒有關？影響哪個版本？在產品 boundary 裡嗎？可不可以被利用？有沒有 exploit？是否列在 CISA KEV？有沒有臨床影響？有沒有金融營運影響？有沒有 OT safety 影響？要立即修？先隔離？先發 advisory？先用 compensating control？修完會不會影響模型？」

「漏洞世界已經爆量。CVE 成長、KEV 優先排序、AI 加速攻擊者 reconnaissance 和 exploit development，都讓 vulnerability management 不能只靠記憶與英雄。」

「醫療 AI 又更麻煩。一個 security patch 可能影響 model runtime。一個 dependency update 可能影響 DICOM output。一個 container rebuild 可能需要重新確認模型輸出一致性。」

「所以醫療 AI 的 patch 要同時追求兩件事：快速控制風險，並維持 patient safety。」

「這就是 Patch SLA 真正難、也真正有價值的地方。」

## 一個決策

**建立 Patch SLA Decision Tree。**

漏洞進來後先做 intake，來源可能是 internal testing、customer report、CVD、NVD、CISA KEV、vendor advisory、threat intelligence。接著做 applicability：影響我們嗎？影響哪個版本？在產品 boundary 裡嗎？可被利用嗎？接著做 severity + clinical / operational impact。再做 decision：Fix now、Compensating control、Defer with rationale、Not applicable、Customer advisory、Safety validation required。最後是 action、retest、archive。

最後可以停一拍，收成一句：

> 沒有 decision，就沒有 governance。沒有 retest，就沒有 trust。

---

# Slide 13｜Small Team 30 / 60 / 90

## 一個問題

**如果只有 8 個人、3 個月、沒有大公司資安部門，小團隊要怎麼開始？**

## 一個故事

「你可能會想：這些聽起來都很合理，但我們公司只有 8 個人。」

「兩個 AI engineer，一個 backend，一個 frontend，一個 DevOps，一個 QA，一個法規，一個 PM。」

「沒有大型資安部門。沒有 compliance office。沒有一整個 GRC team。連會議室都沒有，因為大家都在遠端。」

「小團隊需要的第一步，是建立第一個 evidence loop。」

「30 天，先知道自己有什麼。」

「產品邊界、intended use、data flow、architecture sketch、asset inventory、SBOM draft、dependency list、model release card draft、known vulnerability check。」

「第一個月的決策問題是：我們現在到底是哪一層？Model？Viewer？Platform？Connected system？」

「60 天，讓風險進流程。」

「做一次 STRIDE workshop，建立 risk register、control mapping、CI security gates、finding workflow、severity criteria、clinical impact column、KEV monitoring、CVD intake、draft Patch SLA。」

「第二個月的決策問題是：哪些風險 release 前必須修？哪些可以 compensating control？誰有權接受 residual risk？」

「90 天，證明修補能力。」

「做 external black-box test、internal vulnerability scan、malformed input test、patch drill、retest evidence、release note template、customer advisory template、incident contact path。」

「第三個月的決策問題是：我們能不能拿一個 finding，完整跑完發現、判斷、修補、重測、留證據？」

「30/60/90 是 adoption scaffold。它讓小團隊從口頭記憶，走向可重複、可稽核的證據循環。」

「三個月後你不會完美。沒有人三個月變完美。除非在簡報上，簡報上的成熟度曲線通常比人生樂觀很多。」

「但三個月後，你會從『我們應該有做吧』，變成『我們知道證據在哪裡』。」

## 一個決策

**先建立第一個可重複 evidence loop。**

30 天看見產品，60 天讓風險進流程，90 天證明修補能力。這比一開始產出一堆沒有人維護的文件更有價值。

---

# Slide 14｜先建立信任，再面對稽核

## 一個問題

**法規文件是最後補出來的，還是從產品工作自然長出來的？**

## 一個故事

「最後一頁，我們回到今天的核心。」

「AI SaMD 的資安，是在真實醫療世界裡，建立一個能被信任、能被修補、能被證明的產品系統。」

「把範圍放大，這件事也適用金融、能源、交通、製造、政府。」

「AI 一旦進入高信任流程，就會承接產品責任。」

「一棟大樓蓋好後才補逃生梯，通常來不及。逃生梯、灑水系統、消防警報、緊急照明，要在設計圖裡。」

「AI 產品也是一樣。」

「Threat Modeling 要在產品邊界形成時進來。」

「SBOM 要在 dependency 被引入時留下。」

「Patch SLA 要在漏洞發生前建立 decision path。」

「Testing 要回答 release decision。」

「Retest evidence 要證明修補真的有效。」

「成熟團隊不一定是文件最多的團隊。成熟團隊是每一個風險都知道怎麼證明、怎麼修、怎麼追的團隊。」

「所以最後請帶走四個問題。」

「我們的產品邊界清楚嗎？」

「我們的風險能接到控制與測試嗎？」

「我們的 finding 有決策紀錄嗎？」

「我們能證明修補真的有效嗎？」

「這四題答得出來，文件會從產品工作自然長出來。這四題答不出來，文件再多也很難變成信任。」

「AI 產品的下一個競爭，是信任競爭。」

「模型是起點。大家真正想從你這裡得到的，是可以被交付責任的信任。」

## 一個決策

**從今天開始，把安全證據當成產品功能的一部分。**

不要把資安證據只放在送審材料。要把它放進產品生命週期：設計時定義邊界，開發時保留 SBOM，測試時接 finding workflow，修補時留下 decision 和 retest，上市後維持 CVD、KEV monitoring、customer advisory、patch metrics、postmarket monitoring。

---

# 全場三個 anchor line

第一句：

> **模型是起點，產品信任才是交付責任的地方。**

第二句：

> **法規要的是證據，不是口號。**

第三句：

> **沒有 decision，就沒有 governance。沒有 retest，就沒有 trust。**

這三句分別放在 Slide 3、Slide 6、Slide 12，最後 Slide 14 收回來。

---

# 可插入的跨產業故事素材

## 醫療故事

「醫療 AI 最需要被看見的風險，常常在流程上下游。影像格式、viewer、暫存資料、DICOM output、patch 後的模型一致性，都會影響醫師看到的結果。醫師看到的是一個 output，產品背後是一整條信任鏈。」

## 金融故事

「Fraud model 可以很準，但如果 attacker 用 deepfake、BEC、供應鏈帳號、API abuse 改變輸入環境，模型可能會在錯誤世界裡做出合理判斷。AI risk 的難處，是模型常常很認真地相信它被餵進來的世界。」

## 關鍵基礎設施故事

「在 OT 裡，AI agent 可能接 sensor、maintenance ticket、procurement、dispatch、remote operation。當 agent 被賦予行動能力，錯誤就會變成工單、採購、派工、閥門、負載、路線。這也是 critical infrastructure 需要 Trustworthy AI profile 的原因。」

## 犯罪經濟故事

「犯罪者使用 AI，是因為它讓犯罪變便宜、變快、變可規模化。AI 讓普通攻擊者得到自動化助手，也讓 defender 面對更快的 reconnaissance、social engineering、malware development 與 vulnerability exploitation。」

---

# 30 分鐘節奏建議

0:00-2:00  
用病人、銀行、電網三個場景開場，建立「AI 產品信任」主題。

2:00-4:00  
Slide 1-2，定義今天的產品邊界與公開揭露邊界。

4:00-8:00  
Slide 3-4，從「模型是起點」推到「AI 正在變基礎設施」。

8:00-12:00  
Slide 5-7，講產品尺度、證據鏈、三種語言。

12:00-18:00  
Slide 8-10，進入前兩層與後兩層風險，再用 Cyber Safety Is Patient Safety 做情緒高點。

18:00-25:00  
Slide 11-13，講 testing、Patch SLA、30/60/90 小團隊落地。

25:00-28:30  
Slide 14 收束，重複三句 anchor line。

28:30-30:00  
保留緩衝與 Q&A。

---

# Final Checklist

| 檢查項目 | 狀態 |
| --- | --- |
| No excessive contrast patterns | 通過；全場只保留一個強 contrast anchor。 |
| Each slide has one question, one story, one decision | 通過；每頁以「一個問題 / 一個故事 / 一個決策」組織。 |
| Tone is mature and guiding | 通過；以 progression、decision pressure、field example 推進。 |
| Boundary -> Evidence -> Decision -> Repair Proof remains clear | 通過；開場、Slide 1、Slide 14 都收回主軸。 |
| Technical terms are preserved | 通過；保留 FDA 524B、Threat Modeling、SBOM、Patch SLA、cyber device、postmarket monitoring、vulnerability management、exploit、CVD、DICOM / PACS、software supply chain、runtime environment。 |
| No unnecessary self-introduction or credential flexing | 通過；全稿以問題、場景、決策為主。 |
