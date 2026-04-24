這版我會把你的 CyberSec 2026 簡報升級成：

# **《AI 進入關鍵產業後：模型只是起點，真正要交付的是可被信任、可被修補、可被稽核的系統》**

原本你的筆記主軸是 **AI SaMD 團隊不能只停在 model，最後要交付的是一個 trustable、patchable、auditable 的臨床產品系統**；我會保留這條核心，但把敘事從「醫療 AI 合規與資安」拉高成「AI 變成醫療、金融、關鍵基礎設施的一部分時，防禦者如何建立產品信任」。

語氣會採用 `AI 世代的網路犯罪趨勢與資安防禦革命` 那種 keynote 感：先問一個看似簡單的問題，接著講歷史、講犯罪經濟、講人性，再突然推到未來；中間有冷幽默、反差、真實案例，最後用一個很清楚的決策收束。原講者的強項是把 ransomware、犯罪即服務、三條犯罪者規則、agentic AI 與「cybercrime as a servant」串成一條大敘事，讓聽眾覺得自己不是在聽知識，而是在看威脅世界怎麼演化。

---

# 全場新的大敘事

今天我們先把「AI 醫療產品怎麼補資安文件」這個角度放小一點。

我們要談的是：

> **當 AI 從模型變成基礎設施，誰能證明它值得被信任？**

在醫療產業，這叫 AI SaMD。
在金融產業，這叫交易、詐欺偵測、信用決策、風控自動化。
在關鍵基礎設施，這叫電網、水務、交通、製造、OT 裡的 AI-assisted operation。

名字不同，但真正的問題一樣：

> **如果這個 AI 明天出錯、被攻擊、被誤用、被迫更新、被醫院或銀行要求停機，你能不能說清楚：它在哪裡、誰負責、怎麼修、怎麼證明？**

FDA 2026 medical device cybersecurity guidance 已經把資安拉進 design、labeling、premarket documentation 與 QMS 語言；它不是單純要求多交幾份文件，而是希望上市醫材面對 cybersecurity threats 時有足夠 resiliency。([U.S. Food and Drug Administration][1]) FDA 524B FAQ 也明確說，cyber device sponsor 要有上市後監控、識別與處理漏洞／exploit 的計畫，包含 CVD、postmarket updates and patches，以及 SBOM。([U.S. Food and Drug Administration][2])

但這不只是醫療。NIST 2026 年 4 月發布 AI RMF critical infrastructure profile concept note，直接指出 critical infrastructure 會越來越依賴 AI across IT、OT、ICS，而這些高風險環境採用 AI 的前提是 AI systems must be worthy of trust。([NIST][3]) 金融業也在走同一條路，FS-ISAC 2026 新策略把 supply chain risk、geopolitical shifts、fraud、AI / post-quantum 等 emerging technologies 列為全球金融系統資安韌性的四個重點。([FS-ISAC][4])

所以 AI SaMD 是入口。
這場真正要談的是：

> **AI 產品信任戰爭。**

---

# 全場開場逐字稿

「今天我想先問大家一個很簡單的問題：一個 AI model 要進入醫院、銀行，或關鍵基礎設施，到底要被信任的是什麼？」

「是準確率嗎？是 ROC curve 嗎？是 demo 影片嗎？還是那張投影片上很漂亮的 `99.2% accuracy`？」

「答案當然不是。或者比較精準地說，那只是答案的一小部分。」

「請想像一個病人，明天早上要做放射治療。今天晚上，一個 AI 幫醫師產生腦瘤 contour。模型很準，demo 很漂亮，validation score 也很好。」

「但醫院真正會問你的問題會很殘酷。」

「這個 contour 是哪個 model version 產生的？DICOM 是不是正確解析？影像是不是正確序列？系統最近有沒有被更新？這個版本有沒有已知漏洞？如果明天出現 critical CVE，誰負責判斷？誰通知醫院？多久修？修完怎麼證明？」

「這時候你會發現，醫院真正需要的，是一個可以被信任、可以被修補、可以被稽核的臨床產品系統。」

「同樣的事情也發生在金融業。銀行不會只停在一個 fraud detection model；它需要的是一個在真實交易流裡，能解釋、能追蹤、能停損、能恢復的風控系統。」

「電力公司也不會只停在一個 load forecasting model；它需要的是一個不能因為 AI hallucination、供應鏈漏洞、API 權限錯誤，就讓調度系統做出錯誤決策的基礎設施能力。」

「所以今天這場，我們不談 AI hype。也不背法規。更不會把大家丟進工具清單的地獄，雖然資安人員真的很愛工具清單，這是我們的某種職業病。」

「今天我想用 14 頁回答一件事：當 AI 從模型變成高信任產業的一部分，我們要怎麼建立一條產品信任路徑。」

「Boundary。Evidence。Decision。Repair Proof。」

「先知道產品邊界在哪裡，風險才知道在哪裡。風險被看見，證據鏈才接得起來。finding 被治理，修補能力才被證明。」

「我的第一個賭注是：未來 2 到 3 年，醫院、銀行、關鍵基礎設施單位問 AI vendor 的第一個問題，會從『你的模型多準？』變成『你的產品信任證據在哪裡？』」

---

# Slide 1｜AI 軟體醫材的資安實戰

## 一個問題

**一個 AI model 要進入醫院、銀行或關鍵基礎設施，真正需要被信任的是什麼？**

## 逐字稿

「今天這個題目表面上叫 AI 軟體醫材的資安實戰。但老實說，如果我只講醫療，那其實太小了。」

「因為 AI SaMD 只是第一個讓大家看見問題的場域。醫療只是比較早把問題寫進法規，把責任攤在陽光下。可是同樣的事情正在金融、製造、能源、交通、政府系統發生。」

「所以我們先不要問：AI model 準不準。」

「這是錯的第一個問題。」

「真正的問題是：當這個 AI 被放進真實營運流程，它還能不能被信任？」

「如果它在醫院，它可能影響 contour、triage、diagnosis support、clinical workflow。」

「如果它在銀行，它可能影響詐欺偵測、信用風險、交易阻擋、客戶身份驗證。」

「如果它在電網或水務，它可能影響負載預測、維修排程、異常偵測，甚至 OT 操作建議。」

「不同產業，痛點不一樣。但信任問題很像。」

「AI 原本只是回答問題。現在 AI 開始接資料、接 API、接 workflow、接 decision、接人命、接錢、接國家關鍵服務。」

「這是很棒的事情。也是很可怕的事情。通常科技最有趣的地方就在這裡：它一邊讓你效率暴增，一邊讓你的風險暴增。非常公平，科技沒有偏心。」

「今天我會用 AI SaMD 當主線，因為醫療器材的法規與產品生命週期要求最清楚。但我會一直把它拉回三個高信任產業：醫療、金融、關鍵基礎設施。」

「因為未來真正的 AI 資安，不會只是 prompt injection，也不會只是 model robustness。它會是產品信任、營運韌性、供應鏈、修補治理、證據鏈的組合。」

「如果你今天只能帶走一句話，就是這句：」

「模型只是起點。大家真正想買到的，是可以放心交付責任的系統。」

## 一個決策

**從第一天開始，不要用 model project 管理 AI；要用 product trust system 管理 AI。**

你的產品資料夾應該從四個核心開始：Boundary、Evidence、Decision、Repair Proof。Boundary 放 intended use、system boundary、data flow。Evidence 放 architecture、threat model、risk assessment、testing。Decision 放 finding triage、risk acceptance、compensating control。Repair Proof 放 patch record、retest evidence、customer advisory、release history。

## 未來賭注

**2026–2028 年，AI vendor 的競爭力會從「誰的模型比較強」變成「誰的信任證據比較完整」。**

---

# Slide 2｜Required CYBERSEC Disclaimer

## 一個問題

**在公開資安演講裡，要怎麼講得有用，但不把內容變成攻擊手冊或法律承諾？**

## 逐字稿

「這一頁是大會必要的 disclaimer。我會讓大家看一下。」

「但我想多說一句。Disclaimer 不只是形式。尤其在醫療、金融、關鍵基礎設施和資安這幾個領域，邊界本身就是一種控制。」

「公開演講有兩種危險。」

「第一種，是講得太抽象。大家聽完覺得：嗯，很重要。然後什麼也沒帶走。」

「第二種，是講得太具體。具體到變成 exploit recipe、客戶拓樸、內部流程，或者讓大家誤以為照著做就一定合規。」

「兩種都不好。第一種沒用，第二種太有用了。有時候太有用比沒用還危險，這也是資安世界很微妙的地方。」

「所以今天我會講方法、講決策、講證據鏈、講產品治理。但我不會講私人客戶細節，不會講可直接複製的攻擊步驟，也不會把任何法規要求包裝成法律意見。」

「這其實也呼應今天的第一個主題：Boundary。」

「在產品裡，邊界不清楚，風險就不清楚。在演講裡，邊界不清楚，責任也會不清楚。」

## 一個決策

**公開溝通的第一個安全控制，就是定義揭露邊界。**

這一頁講完立刻轉走，不要停留太久。它的功能不是教育觀眾法務風險，而是建立你的專業邊界感。

## 未來賭注

**未來高信任產業的技術溝通會越來越重視「可驗證但不過度揭露」。**
醫療、金融、關鍵基礎設施都會遇到同一個問題：你要讓審查者、客戶、合作方看見足夠證據，但不能把系統細節暴露成新的攻擊面。

---

# Slide 3｜模型只是起點

## 一個問題

**醫院買 AI 時，買的是模型，還是責任？**

## 逐字稿

「我們先從 AI 團隊最常犯的錯開始。」

「很多團隊會說：我們只是提供模型。」

「這句話在研究裡成立。在產品裡不成立。在醫療裡更不成立。」

「你不會去買一顆很厲害的引擎，然後期待它自己變成一台安全的車。引擎再強，如果煞車不穩、儀表板亂顯示、保養紀錄不存在、召回流程不清楚，沒有人敢讓它上路。」

「AI model 就是引擎。」

「SaMD 是整台車。」

「醫院要的是能上臨床道路的整台車，不是一顆單獨引擎。」

「同樣道理，銀行不會只買一個 fraud model。銀行買的是一套能接真實交易、能追蹤 decision、能處理 false positive、能在模型異常時停損的風控產品。」

「電力公司也不會只停在一個 forecasting model；它需要的是一個在高壓、低容錯、不能亂停的環境裡，能被治理的 operational system。」

「所以當你說『我們只是模型』，其實是在說：我只想對引擎負責，不想對車負責。」

「但客戶不會這樣買。法規也不會這樣看。出事的時候，媒體更不會這樣寫。」

「醫療現場真正會問的是：輸入影像是不是正確？DICOM metadata 有沒有缺漏？輸出結果是否需要醫師確認？使用者有沒有可能誤解 AI 結果？暫存資料多久刪？誰能看？系統壞了怎麼回復？漏洞出現誰修？」

「這些問題大多不在模型準確率裡。」

「但這些問題都會影響產品信任。」

FDA 的 AI-enabled medical device list 也不是在列模型，而是在提高市場、醫療人員與病人對 AI-enabled medical devices 的透明度；FDA 也說未來會探索如何標記 foundation model 與 LLM-based functionality。這代表 AI 醫材已經是產品與市場現實，不只是研究題目。([U.S. Food and Drug Administration][5])

## 一個決策

**每個 AI 團隊都要做一張 Responsibility Map。**

這張圖不是 architecture diagram，而是責任地圖。它要回答：誰使用？在哪個流程使用？輸入是什麼？輸出是什麼？輸出能不能直接用？誰確認？資料暫存多久？異常怎麼處理？誰能更新？漏洞怎麼通報？修補怎麼證明？

## 未來賭注

**未來 AI 產品採購會越來越少只看 benchmark，越來越多看 responsibility evidence。**

你可以把這句講得更重一點：

「Benchmark 會讓客戶對你有興趣。Responsibility evidence 才會讓客戶敢把你放進流程。」

---

# Slide 4｜AI 變成基礎設施

## 一個問題

**當 AI 不再是 demo，而是醫療、金融與關鍵基礎設施的一部分，失敗會長什麼樣子？**

## 逐字稿

「現在我們把視角拉高一點。」

「AI 最早像玩具。然後變成工具。接下來，它正在變成基礎設施。」

「這句話聽起來很大，但我們看一下現實。」

「Roche 在 2026 年 3 月宣布擴建 NVIDIA AI factory，新增 2,176 顆 Blackwell GPUs，總計超過 3,500 顆 GPU，用來支撐 therapeutics、diagnostics、clinical trials 和大規模資料洞察。」([Roche][6])

「這不是一個 AI demo。這是醫療與生命科學產業把 AI 當成 operating backbone。」

「當 AI 變成 backbone，風險就變了。」

「以前 AI model 出錯，可能是一個 prediction 錯。現在 AI infrastructure 出錯，可能是一整個流程停。」

「醫療裡，這叫 clinical workflow disruption。」

「金融裡，這叫 payment、settlement、fraud operation、customer trust disruption。」

「關鍵基礎設施裡，這叫 operation disruption。有時候講白一點，就是燈會不會亮、水會不會流、交通會不會正常。」

「這不是誇張。Change Healthcare 事件就讓我們看到第三方醫療基礎設施中斷可以多嚴重。AHA 調查接近一千家醫院，74% 回報直接病人照護受到影響，94% 回報財務影響。」([American Hospital Association][7])

「Synnovis 事件也讓 NHS 相關服務恢復拖到 2024 年 12 月，攻擊者還公開了竊取的資料。」([NHS England][8])

「台灣也不是局外人。2025 年馬偕紀念醫院遭 CrazyHunter 勒索軟體攻擊，公開報導指出攻擊路徑涉及 AD 主機派送惡意程式與 BYOVD，衛福部 H-ISAC 也發出警訊。」([iThome][9])

「所以我想講一件事：AI 進入醫療，不只是 AI risk。AI 進入金融，不只是 fintech risk。AI 進入 OT，不只是 automation risk。」

「它們都變成 infrastructure risk。」

「一旦 AI 變成基礎設施，問題就不是『模型可不可以跑』，而是『流程能不能活下來』。」

## 一個決策

**把 AI deployment 畫成 infrastructure map，而不是 model pipeline。**

Model pipeline 只會畫 training、validation、inference。Infrastructure map 要畫 model、runtime、identity、API、data storage、logs、update path、SIEM/SOC、customer environment、fallback workflow。醫療要畫 PACS / DICOM / viewer，金融要畫 transaction stream / fraud operation / case management，關鍵基礎設施要畫 IT / OT / ICS boundary 與 human override。

## 未來賭注

**下一波 AI 資安事件，很多不會從 model attack 開始，而會從 connector、identity、update chain、dependency、API、workflow automation 開始。**

這是整場第一個大賭注。

---

# Slide 5｜Risk grows with architecture

## 一個問題

**同一個 AI model，放在不同產品邊界裡，資安責任會一樣嗎？**

## 逐字稿

「我們現在要談一張很重要的地圖。」

「同一個 AI model，放在不同 architecture 裡，風險完全不同。」

「如果它只是 model artifact，風險是 model provenance、version、hash、dependency、training reference。」

「如果它加了一個 viewer，風險突然多了 parser、upload、cache、output rendering、使用者誤解。」

「如果它變成 platform，風險多了 database、API、identity、RBAC、audit log、backup。」

「如果它接進醫院 PACS、銀行 transaction system、工廠 OT network，那風險又變成 shared responsibility 和 continuity。」

「所以風險不是突然變大。」

「是產品長大了。」

「這很像小孩。小孩小的時候，你只要擔心他不要跌倒。長大後他會上網、會交朋友、會刷你的信用卡。你不是突然比較倒楣，是 attack surface 長大了。」

「AI 產品也是一樣。」

「Scale 1：Model。你要問，這個模型從哪裡來，版本是什麼，有沒有被換掉。」

「Scale 2：Viewer。你要問，不可信輸入進來時，parser 會不會爆炸，暫存資料會不會外洩，使用者會不會誤解 output。」

「Scale 3：Platform。你要問，誰能登入，誰能查資料，API 能不能被濫用，log 能不能支撐調查。」

「Scale 4：Connected System。你要問，當它接進醫院、銀行或 OT，它中斷時誰知道，誰能停，誰能復原，誰能通知客戶。」

「很多 AI 團隊痛苦的原因，不是他們不努力，而是他們一直用 Scale 1 的心態在管理 Scale 3 或 Scale 4 的產品。」

「這就像你已經開上高速公路了，還在用腳踏車安全規則。精神可嘉，結果通常不好。」

## 一個決策

**每次產品新增功能，都做一次 Boundary Review。**

你要問：我們是不是跨層了？新增 viewer，就是從 model 跨到 user-facing workflow。新增 database，就是跨到 platform responsibility。新增 PACS / HIS / transaction / OT integration，就是跨到 connected system。每跨一層，就要更新 architecture、threat model、testing scope、labeling、Patch SLA、customer responsibility。

FDA 2026 medical device cybersecurity guidance 也把目標放在 medical devices 對 cybersecurity threats 的 resilience；換句話說，審查者要看的不是單點模型，而是上市產品在真實系統中的設計、標示、文件與韌性證據。([U.S. Food and Drug Administration][1])

## 未來賭注

**未來成熟的 AI 團隊，不是模型分數最高的團隊，而是最清楚知道自己現在在哪一層的團隊。**

---

# Slide 6｜Evidence, not slogans

## 一個問題

**當你說「我們很安全」，你拿什麼證明？**

## 逐字稿

「現在我們進入法規。但先不要緊張，我不會開始朗讀 FDA 文件。公開朗讀法規，是讓一個會場進入集體靈魂出竅最快的方法之一。」

「我們把法規翻成人話。」

「法規真正問的不是：你有沒有文件。」

「法規真正問的是：你有沒有證據鏈。」

「你去做健康檢查，醫師問你身體狀況，你說：我覺得我很健康。」

「這句話沒有用。」

「醫師要看的是血液檢查、影像、病史、追蹤紀錄、異常處理。」

「醫療器材資安也是一樣。你說『我們很安全』沒有用。」

「你要拿得出 architecture、threat model、risk assessment、controls、testing、finding decision、patch record、retest evidence。」

「FDA 524B 的語言看起來像法規，但其實非常合理。它要求 cyber device sponsor 提交計畫，去 monitor、identify、address postmarket cybersecurity vulnerabilities and exploits，包含 coordinated vulnerability disclosure；也要求 device and related systems cybersecure，提供 postmarket updates and patches，以及 SBOM。」([U.S. Food and Drug Administration][2])

「這一點在金融業也一樣。銀行不會只接受你說『我們有資安』。它會問第三方風險、營運韌性、事件通報、供應鏈、復原能力。」

「關鍵基礎設施也是一樣。電網、水務、交通不會只問 AI 準不準。它們會問，這個 AI system 在 high-stakes environment 裡是不是 worthy of trust。NIST 2026 AI RMF critical infrastructure profile 也把這件事講得很清楚：critical infrastructure 會越來越依賴 AI across IT、OT、ICS，採用 AI 的前提是 trustworthiness。」([NIST][3])

「所以這頁我要大家記住一句話：」

「法規要的是證據，不是口號。」

## 一個決策

**每個 finding 都要變成 Evidence Chain Ticket。**

一個 finding 不應該只寫「已修」。它要能串起來：Risk ID → Control ID → Test ID → Finding ID → Decision → Retest Evidence → Archive Location。這樣你才知道這個風險從哪裡來、怎麼控制、怎麼測、怎麼判斷、怎麼修、怎麼證明。

## 未來賭注

**未來 AI 產品審查會越來越像 safety case：不是問你做了多少事，而是問你如何證明這個產品在這個使用情境下值得被信任。**

---

# Slide 7｜Model, governance, stack

## 一個問題

**同一個 AI 風險，模型團隊、資安團隊、法規團隊和主管要怎麼講同一種語言？**

## 逐字稿

「接下來我們談一個很多公司真正卡住的地方。」

「不是模型。不是工具。是語言。」

「同一個 AI risk，在公司裡通常會變成四種完全不同的語言。」

「AI engineer 會說：這可能是 data drift。」

「資安工程師會說：這可能是 input tampering。」

「法規同事會說：這會不會影響 intended use？」

「主管會說：這會不會延後上市？會不會讓客戶不買？」

「四個人都在講同一件事，但他們像在四個不同頻道。這種會議我相信大家多少都開過。你開完會，覺得大家都很專業，但沒有人知道下一步要做什麼。這就是大型組織常見的專業性災難。」

「所以我們需要翻譯。」

「AI 產品風險至少要翻成三種語言。」

「第一種是 model evidence：intended use、dataset、validation、limitation、performance monitoring。」

「第二種是 governance language：owner、severity、acceptance criteria、residual risk、release decision。」

「第三種是 stack security：SBOM、model integrity、runtime isolation、secrets、API access、logging、update path。」

「如果這三種語言接不起來，問題就會漂浮在組織裡。」

「AI 團隊覺得那是資安問題。資安團隊覺得那是產品問題。法規覺得那是送審問題。主管覺得那是工程問題。」

「最後沒有人真的擁有它。」

「而在高信任產業裡，沒有 owner 的 risk，通常會變成事件。」

FDA 的 AI-enabled device software draft guidance 已經採取 total product lifecycle 角度，強調送審資料要支援 FDA 評估 safety and effectiveness，並反映整個 TPLC 的風險管理。([U.S. Food and Drug Administration][10]) NIST CSF 2.0 也把 cybersecurity 擴展成跨組織的 governance 與 enterprise risk 語言；EBA 2025 risk assessment 對銀行業也指出，cyber、ICT-related threats、fraud 和 legal risks 持續推高 operational risk、resilience 和 stability concerns。([European Banking Authority][11])

## 一個決策

**建立 Risk Translation Sheet。**

每個重要風險都要同時寫三欄：Model impact、Security impact、Business / clinical / operational decision。醫療寫 clinical impact，金融寫 customer / transaction / regulatory impact，關鍵基礎設施寫 safety / continuity / OT impact。

## 未來賭注

**未來 AI 產品的最大瓶頸不一定是模型能力，而是跨團隊治理能力。**

很多事故不是沒有人知道風險，而是風險沒有被翻譯成決策。

---

# Slide 8｜Scale 1–2：Model 到 Viewer

## 一個問題

**攻擊者真的需要攻擊你的 AI model 嗎？還是攻擊 viewer、parser、input workflow 就夠了？**

## 逐字稿

「現在我們回到剛剛四層地圖的前兩層：Model 和 Viewer。」

「很多人談 AI 資安，第一反應是 model attack。Data poisoning、model inversion、adversarial example，聽起來很高級，也很適合讓投影片看起來很有學術感。」

「但攻擊者通常沒有那麼浪漫。」

「如果他可以攻擊 parser，他幹嘛攻擊模型？」

「如果他可以偷 API token，他幹嘛研究你的 neural network？」

「如果他可以讓使用者打開一個惡意檔案，他幹嘛花時間理解你的 loss function？」

「攻擊者想要 easy life。這點跟我們大部分人一樣，只是他們選的職涯路線比較有問題。」

「醫療影像是一個很好的例子。」

「你有一個 AI model，可以分析 MRI。很好。但這個 model 前面通常會有 DICOM workflow、viewer、parser、upload、temporary storage。這些東西如果出問題，模型再準也沒有用。」

「NVD 對 CVE-2025-35975 的描述就指出，MicroDicom DICOM Viewer 有 out-of-bounds write vulnerability，使用者只要開啟惡意 DCM 檔，就可能讓攻擊者執行任意程式碼。」([NVD][12])

「這就是我想講的重點。」

「攻擊者不一定要碰 AI。」

「他只要碰 AI 周圍那一圈。」

「金融業也一樣。你可以有很好的 fraud model，但如果 case management system 的權限錯了、API 可以被濫用、第三方 webhook 被竄改，攻擊者不需要打敗模型。」

「關鍵基礎設施也一樣。你可以有很好的 predictive maintenance model，但如果 sensor data pipeline、agent identity、OT gateway、update package 出問題，AI 會很認真地幫你做錯事。」

「這是 AI 產品很殘酷的地方：模型是你最驕傲的地方，但攻擊者通常會從你最無聊的地方進來。」

## 一個決策

**Scale 1 建 model release card；Scale 2 建 input/output safety gate。**

Model release card 要記錄 model version、hash/signature、training/validation reference、intended use、known limitations、dependency、SBOM、release owner。Input/output safety gate 要處理 DICOM conformance、malformed input、file size/type、cache encryption、cache retention、generic error message、output limitation notice、human review reminder。

## 未來賭注

**未來 AI SaMD 最常被低估的攻擊面，不是模型本身，而是資料進出模型的那一圈。**

DICOM、viewer、parser、cache、API、output rendering，這些才是第一波真正會出事的地方。

---

# Slide 9｜Scale 3–4：Platform 到 Connected Medical System

## 一個問題

**當 AI 產品接進醫院、銀行或 OT 系統後，資安事件還只是產品問題嗎？**

## 逐字稿

「現在我們進入 Scale 3 和 Scale 4。」

「Scale 3 是 platform。你開始有帳號、資料庫、API、audit log、backup、admin action。」

「Scale 4 是 connected system。醫療就是 PACS / HIS / hospital network。金融就是 core banking、payment rail、fraud operation、第三方金融科技供應鏈。關鍵基礎設施就是 IT / OT / ICS。」

「這一層開始，資安事件就不只是產品問題。」

「它會變成營運連續性問題。」

「在醫療裡，是 clinical continuity。」

「在金融裡，是 financial operational resilience。」

「在關鍵基礎設施裡，是 service continuity。有時候甚至是 safety。」

「我們看 Synnovis。它不是一個 AI SaMD 事件，但它告訴我們醫療供應商被打，服務恢復可以拖很久，資料調查也可以非常複雜。NHS 說服務到 2024 年 12 月才 fully restored，且被竊資料的調查花了一年以上，因為資料是 unstructured、incomplete、fragmented。」([NHS England][8])

「Change Healthcare 也不是一個 AI 事件，但它告訴我們第三方醫療基礎設施一中斷，醫院、病人、現金流會一起受到影響。AHA 調查顯示 74% 回報 direct patient care impact，94% 回報 financial impact。」([American Hospital Association][7])

「金融業也很清楚這點。FS-ISAC 2026 的策略把 supply chain risk、geopolitical shifts、fraud、emerging technologies 列為全球金融系統 collective risk landscape 的重點。」([FS-ISAC][4])

「這些案例都在講同一件事。」

「當你接進別人的流程，你就進入 shared responsibility。」

「你不能假裝所有事情都是客戶的責任。也不能假裝 vendor 可以控制一切。」

「成熟做法不是甩鍋，也不是全包。」

「成熟做法是把 responsibility boundary 寫清楚。」

## 一個決策

**Scale 3 建 platform security baseline；Scale 4 建 shared responsibility + downtime fallback plan。**

Platform baseline 要包含 MFA、RBAC、API authorization、rate limiting、audit log、encryption-at-rest、backup/restore drill、admin logging、customer data separation。Connected system plan 要包含 network segmentation、allowlist、DICOM-TLS 或 VPN、default-deny firewall、SIEM forwarding、manual update window、downtime fallback、incident contact、customer advisory template。

## 未來賭注

**未來高信任產業採購 AI 時，會越來越問 shared responsibility 和 downtime fallback。**

因為大家已經被事件教育過：連線產品不是只看功能，也要看中斷時怎麼活下來。

---

# Slide 10｜Cyber Safety Is Patient Safety

## 一個問題

**資安什麼時候會變成病人安全、金融穩定或關鍵服務連續性問題？**

## 逐字稿

「這一頁只有一句話。」

「Cyber Safety Is Patient Safety。」

「但我想把它稍微擴大。」

「Cyber Safety Is Operational Safety。」

「在醫療裡，它是 patient safety。」

「在金融裡，它是 market trust 和 customer protection。」

「在關鍵基礎設施裡，它是 public safety 和 service continuity。」

「資安人常常講 CIA：Confidentiality、Integrity、Availability。」

「這些字很正確，也很容易讓非資安人員睡著。它們聽起來像某種很有禮貌的風險分類。」

「所以我們要把它翻譯。」

「Availability 在醫療裡不是 uptime。是醫師需要結果時，系統能不能用。」

「Integrity 在醫療裡不是 hash 沒變。是醫師能不能相信這個 AI output。」

「Confidentiality 不是資料沒有外洩而已。是病人的信任有沒有被破壞。」

「Repairability 不是工程流程。是出事後，產品能不能安全恢復。」

「在金融業，availability 是交易能不能繼續，integrity 是交易與風控 decision 能不能被信任，repairability 是銀行能不能在攻擊後恢復營運。」

「在電網，availability 和 integrity 更殘酷。因為有些錯誤不是報表錯，而是實體世界被影響。」

「所以 Cyber Safety is Patient Safety 不是一句 slogan。」

「這是一個產品責任句。」

「如果你的 AI product 不能被修，不能被追，不能被證明，那它就不應該進入高信任流程。」

FDA 對 Contec / Epsimed patient monitor 的 safety communication 很適合放在這裡。FDA 2025 更新指出，該 patch 會完全移除受影響設備的 networking functionality，讓設備只能 local monitoring；同一頁也指出漏洞可能讓未授權者控制設備、導致設備不如預期運作，或造成資料外流。這說明資安修補在醫療設備裡不是單純 IT 任務，而會直接改變功能、臨床使用方式與現場責任。([U.S. Food and Drug Administration][13])

## 一個決策

**每個 security risk 都要加一欄 clinical / operational impact。**

醫療要問：會不會讓 AI output 不可信？會不會延遲診療？會不會讓醫師拿不到影像或結果？會不會需要 downtime workflow？金融要問：會不會造成交易錯誤、客戶損失、fraud false negative、監管通報？關鍵基礎設施要問：會不會造成 physical process disruption、manual override、safety interlock 壓力？

## 未來賭注

**未來只會講 CVSS 的團隊會被追問：那對臨床、金融營運或關鍵服務的影響是什麼？**

CVSS 是起點，不是決策。

---

# Slide 11｜White-box + Black-box

## 一個問題

**我們做測試，是為了找漏洞，還是為了做決策？**

## 逐字稿

「現在我們來談測試。」

「我先講結論：測試不是為了報告好看。」

「雖然很多測試報告真的長得很像是為了讓人覺得自己花了錢。封面很好看，表格很多，最後大家都很安心。直到下一次事件發生。」

「真正成熟的測試，不是問：我們做了哪些測試？」

「而是問：每一種測試回答了哪一個決策問題？」

「SBOM / SCA 回答：我們用了什麼？有沒有已知漏洞？」

「White-box 回答：release 前有哪些便宜、可修、可追蹤的問題？」

「Secret scan 回答：我們是不是把金鑰、密碼、debug config 帶進產品？」

「Malformed input / fuzz test 回答：異常輸入會不會打壞 viewer、parser、workflow？」

「Black-box 回答：攻擊者從外面看得到什麼？」

「Pen test 回答：這些弱點能不能串成真實攻擊路徑？」

「Retest 回答：我們修完真的有效嗎？」

「測試最重要的不是產生 finding。」

「測試最重要的是產生 decision。」

「如果測試結果沒有 owner、severity、due date、fix decision、retest evidence，那它就只是報告。」

「這一點在醫療、金融、關鍵基礎設施都一樣。」

「金融業現在很重視 resilience，不只是 incident prevention。EBA 2025 risk assessment 也指出，銀行 operational risk 仍高，cyber、ICT-related threats、fraud 和 legal risks 會同時造成直接財務損失與韌性／穩定性疑慮。」([European Banking Authority][11])

「所以 testing portfolio 的目的不是證明你沒有漏洞。」

「這世界上沒有人可以證明自己沒有漏洞。說可以的人通常有兩種：一種是剛入行，一種是正在賣東西。」

「Testing portfolio 的目的，是證明你有能力看見風險、治理風險、修補風險。」

## 一個決策

**把 testing 接到 finding workflow，再接到 Patch SLA。**

每個測試項目都要有 test objective、scope、pass/fail criteria、finding owner、severity criteria、fix decision、retest plan、evidence location。這樣 testing 才會從活動變成治理。

## 未來賭注

**未來 AI 產品資安測試會從 checklist testing 走向 decision-driven testing。**

審查者不只會問「你做過 penetration test 嗎？」
他會問「這個 test 如何支撐你的 release decision？」

---

# Slide 12｜Patch SLA

## 一個問題

**漏洞出現時，你的團隊是靠英雄救火，還是靠決策系統？**

## 逐字稿

「這是我認為今天最重要的一頁。」

「Patch SLA。」

「但我要先講清楚，Patch SLA 不是一個魔法詞。不是你在文件裡寫 critical 30 days、high 60 days，然後產品就變安全。」

「Patch SLA 的核心不是天數。」

「Patch SLA 的核心是 decision。」

「漏洞進來時，你怎麼判斷它跟你有沒有關？它影響哪個版本？它可不可以被利用？它有沒有臨床影響？它有沒有金融營運影響？它有沒有 OT safety 影響？它是不是在 CISA KEV？它是不是有 exploit？你要現在修？先隔離？先發 advisory？先用 compensating control？修完會不會影響模型？」

「這些才是 Patch SLA。」

「NIST 2026 年 4 月說，CVE submissions 從 2020 到 2025 年增加 263%，2026 年前三個月又比去年同期高出近三分之一。NIST 因此調整 NVD enrichment operation，優先處理 CISA KEV、聯邦政府軟體與 critical software 相關 CVE。」([NIST][14])

「這代表什麼？」

「代表漏洞世界已經爆量到連權威資料庫都必須做風險排序。」

「如果 NIST 都需要 prioritization，你的小團隊當然更需要。」

「金融業也開始看見同樣壓力。FS-ISAC 2026 advisory 的摘要指出，AI 可能讓攻擊者更快發現並利用過去未被注意的漏洞，傳統 vulnerability management assumptions no longer hold。」([ABA Banking Journal][15])

「這就是未來。」

「漏洞會更多。AI 會讓 finding 更快。攻擊者會更自動化。Defender 的瓶頸不會只是會不會修，而是會不會判斷。」

「醫療 AI 又更麻煩。」

「因為一個 security patch 可能影響 model runtime。一個 dependency update 可能影響 DICOM output。一個 container rebuild 可能需要重新確認模型輸出一致性。」

「所以醫療 AI 的 patch 不是越快越好。」

「是越快控制風險，同時不能破壞 patient safety。」

「這就是 Patch SLA 真正難的地方。」

## 一個決策

**建立 Patch SLA Decision Tree。**

漏洞進來後先做 intake，來源可能是 internal testing、customer report、CVD、NVD、CISA KEV、vendor advisory、threat intelligence。接著做 applicability：影響我們嗎？影響哪個版本？在產品 boundary 裡嗎？可被利用嗎？接著做 severity + clinical / operational impact。再做 decision：Fix now、Compensating control、Defer with rationale、Not applicable、Customer advisory、Safety validation required。最後是 action、retest、archive。

CISA KEV 可以作為優先排序輸入；CISA 將 KEV catalog 定位為已知在野利用漏洞的 authoritative source，組織應把它作為 vulnerability management prioritization framework 的輸入。([CISA][16])

## 未來賭注

**未來 AI SaMD 團隊的競爭力，不是誰能 build model，而是誰能在漏洞爆炸時做高品質修補決策。**

我會在這裡停一拍，然後說：

「沒有 decision，就沒有 governance。沒有 retest，就沒有 trust。」

---

# Slide 13｜Small Team 30 / 60 / 90

## 一個問題

**如果只有 8 個人、3 個月、沒有大公司資安部門，小團隊要怎麼開始？**

## 逐字稿

「你可能會想：這些聽起來都很棒，但我們公司只有 8 個人。」

「兩個 AI engineer，一個 backend，一個 frontend，一個 DevOps，一個 QA，一個法規，一個 PM。」

「沒有大型資安部門。沒有 compliance office。沒有一整個 GRC team。連會議室都沒有，因為大家都在遠端。」

「那怎麼辦？」

「答案不是放棄。」

「答案也不是假裝自己是大公司。這通常會產出一堆文件，然後大家再也不想碰它。」

「小團隊要做的是第一個 evidence loop。」

「30 天，先知道自己有什麼。」

「產品邊界、intended use、data flow、architecture sketch、asset inventory、SBOM draft、dependency list、model release card draft、known vulnerability check。」

「第一個月的決策問題是：我們現在到底是哪一層？Model？Viewer？Platform？Connected system？」

「60 天，讓風險進流程。」

「做一次 STRIDE workshop，建立 risk register、control mapping、CI security gates、finding workflow、severity criteria、clinical impact column、KEV monitoring、CVD intake、draft Patch SLA。」

「第二個月的決策問題是：哪些風險 release 前必須修？哪些可以 compensating control？誰有權接受 residual risk？」

「90 天，證明修補能力。」

「做 external black-box test、internal vulnerability scan、malformed input test、patch drill、retest evidence、release note template、customer advisory template、incident contact path。」

「第三個月的決策問題是：我們能不能拿一個 finding，完整跑完發現、判斷、修補、重測、留證據？」

「請注意，30/60/90 不是法規要求。不是什麼神聖時程。」

「它是一個小團隊啟動信任系統的方法。」

「三個月後你不會完美。沒有人三個月變完美。除非是簡報上，簡報上的成熟度曲線通常比人生樂觀很多。」

「但三個月後，你會從『我們應該有做吧』，變成『我們知道證據在哪裡』。」

「這差很多。」

IBM 2025 Cost of a Data Breach report 也提醒 AI oversight gap：IBM 指出 AI adoption 正在跑得比 security 和 governance 快，且缺乏 AI access controls 或 AI governance policies 的組織比例很高；同一頁也指出 extensive use of AI in security 可以帶來成本節省，但前提是 AI security 和 governance 要接起來。([IBM][17])

## 一個決策

**不要追求一開始完美；先建立第一個可重複 evidence loop。**

30 天看見產品，60 天讓風險進流程，90 天證明修補能力。這比一開始產出一堆沒有人維護的文件更有價值。

## 未來賭注

**未來小型 AI vendor 能不能被醫院、銀行、關鍵基礎設施客戶信任，關鍵不是「我們之後會補」，而是「我們現在已經有 evidence loop」。**

---

# Slide 14｜先建立信任，再面對稽核

## 一個問題

**法規文件是你最後補出來的，還是產品自然長出來的？**

## 逐字稿

「最後一頁，我們回到今天的核心。」

「AI SaMD 的資安，不能只看成是在保護一個模型。」

「它是在真實醫療世界裡，建立一個能被信任、能被修補、能被證明的產品系統。」

「如果把範圍放大，這件事也適用金融、能源、交通、製造、政府。」

「AI 一旦進入高信任流程，它就不再只是模型能力問題。」

「它是產品責任問題。」

「一棟大樓不會蓋完才說：我們來補逃生梯。」

「逃生梯、灑水系統、消防警報、緊急照明，要在設計圖裡。」

「AI 產品也是一樣。」

「Threat model 不是送審前趕出來的。」

「SBOM 不是客戶問才整理的。」

「Patch SLA 不是出事才建立的。」

「Testing 不是報告封面。」

「Retest evidence 不是補洞截圖。」

「這些東西都應該從產品工作自然長出來。」

「真正成熟的團隊，不一定是文件最多的團隊。」

「是每一個風險都知道怎麼證明、怎麼修、怎麼追的團隊。」

「所以我今天最後的建議是：不要先問我們要補哪些文件。」

「先問四個問題。」

「我們的產品邊界清楚嗎？」

「我們的風險能接到控制與測試嗎？」

「我們的 finding 有決策紀錄嗎？」

「我們能證明修補真的有效嗎？」

「這四題答得出來，你的文件就會長出來。」

「這四題答不出來，文件再多也只是 PDF 森林。看起來很茂密，走進去就迷路。」

「AI 產品的下一個競爭，不只是模型競爭。」

「是信任競爭。」

「模型只是起點。」

「大家真正想從你這裡得到的，是信任。」

## 一個決策

**從今天開始，把安全證據當成產品功能的一部分。**

不要把資安證據當成送審材料。要把它當成產品生命週期的一部分：設計時定義邊界，開發時保留 SBOM，測試時接 finding workflow，修補時留下 decision 和 retest，上市後維持 CVD、KEV monitoring、customer advisory、patch metrics。

## 未來賭注

**未來 AI 高信任產品的勝負，不會只看「誰比較聰明」，而會看「誰比較值得被交付責任」。**

---

# 全場可以反覆使用的三個 anchor line

第一句：

> **模型只是起點。大家真正想買到的，是可以放心交付責任的系統。**

第二句：

> **法規要的是證據，不是口號。**

第三句：

> **沒有 decision，就沒有 governance。沒有 retest，就沒有 trust。**

這三句要分別出現在 Slide 3、Slide 6、Slide 12，最後 Slide 14 全部收回來。

---

# 加強版「未來預測」段落

你可以在 Slide 4 或 Slide 12 前加一段，讓全場更像 AI keynote。

「我今天做三個預測。第一，未來 AI SaMD 的主要資安事件，不會只來自 model attack，而會來自 AI clinical infrastructure：connector、identity、dependency、update chain、viewer、API。第二，金融與關鍵基礎設施對 AI vendor 的問題，會從『你有沒有 AI』變成『你的 AI 怎麼被治理』。第三，漏洞管理會從 CVSS-driven 走向 context-driven，因為漏洞量已經多到連 NVD 都必須優先排序。」

「這三件事合在一起，會把 AI 產品團隊推進一個新時代。」

「以前，我們問 AI：你能不能回答？」

「現在，我們問 AI 產品：你能不能負責？」

Trend Micro 2026 預測也把 agentic AI 描述成會讓網路犯罪從 service model 轉成 AI 作為 operational servant，能以過去難以想像的速度、規模與複雜度協調攻擊；Google Threat Intelligence Group 也在 2026 年 2 月指出，威脅行為者正在把 AI 整合進 reconnaissance、social engineering、malware development 等攻擊生命週期，雖然尚未觀察到根本改變威脅格局的突破性能力，但趨勢已經很明確。([Trend Micro][18])

---

# 可插入的跨產業故事素材

## 醫療故事

「醫療 AI 最可怕的錯誤，不一定是模型答錯。更常見的是流程上下游出問題。影像格式不正確、viewer 有漏洞、暫存資料沒清、輸出被誤解、patch 影響 DICOM output。最後醫師看到的是一個結果，但產品背後其實是一整條信任鏈。」

## 金融故事

「金融業很早就知道一件事：模型不是最後答案。Fraud model 可以很準，但如果 attacker 用 deepfake、BEC、供應鏈帳號、API abuse 改變輸入環境，模型可能會在錯誤世界裡做出很合理的判斷。這就是 AI risk 的難處：AI 常常不是錯在笨，而是錯在太相信它被餵進來的世界。」

## 關鍵基礎設施故事

「在 OT 裡，AI agent 不是多一個 chatbot。它可能接 sensor、接 maintenance ticket、接 procurement、接 dispatch、接 remote operation。當 agent 被賦予行動能力，錯誤就不再停留在螢幕上。它會變成工單、採購、派工、閥門、負載、路線。這就是為什麼 NIST 會開始針對 critical infrastructure 做 Trustworthy AI profile。」

## 犯罪經濟故事

「犯罪者不會因為 AI 很酷就使用 AI。犯罪者使用 AI，是因為它讓犯罪變便宜、變快、變可規模化。這是 AI 世代最重要的威脅變化。不是每個駭客突然變成天才，而是普通攻擊者突然有了自動化助手。就像創業公司有 AI coworker，犯罪集團也會有 AI coworker。只是他們的 OKR 比較糟糕。」

---

# 30 分鐘節奏建議

0:00–2:00
用病人、銀行、電網三個場景開場，建立「AI 產品信任」主題。

2:00–4:00
Slide 1–2，定義今天不是 hype、不是法規朗讀、不是 exploit recipe。

4:00–8:00
Slide 3–4，從「模型只是起點」推到「AI 正在變基礎設施」。

8:00–12:00
Slide 5–7，講產品尺度、證據鏈、三種語言。

12:00–18:00
Slide 8–10，進入前兩層與後兩層風險，再用 Cyber Safety is Patient Safety 做情緒高點。

18:00–25:00
Slide 11–13，講 testing、Patch SLA、30/60/90 小團隊落地。

25:00–28:30
Slide 14 收束，重複三句 anchor line。

28:30–30:00
保留緩衝與 Q&A。

---

# 這版真正升級的地方

舊版是：

> FDA 524B + Threat Modeling + Patch SLA + SBOM + Testing。

新版是：

> **AI 從模型變成高信任產業基礎設施後，產品團隊如何建立 trust evidence、repair capability、governance decision。**

舊版比較像專業工作坊。

新版比較像 keynote。

舊版讓人覺得：「這個人很懂。」

新版要讓人覺得：

> 「糟糕，我們公司現在是不是正在用 Scale 1 的心態管理 Scale 4 的 AI？」

[1]: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/cybersecurity-medical-devices-quality-management-system-considerations-and-content-premarket "Cybersecurity in Medical Devices: Quality Management System Considerations and Content of Premarket Submissions | FDA"
[2]: https://www.fda.gov/medical-devices/digital-health-center-excellence/cybersecurity-medical-devices-frequently-asked-questions-faqs "Cybersecurity in Medical Devices Frequently Asked Questions (FAQs) | FDA"
[3]: https://www.nist.gov/programs-projects/concept-note-ai-rmf-profile-trustworthy-ai-critical-infrastructure "Concept Note: AI RMF Profile on Trustworthy AI in Critical Infrastructure | NIST"
[4]: https://www.fsisac.com/newsroom/fsisac-reveals-new-strategy-for-cybersecurity-resilience-of-the-global-financial-system "FS-ISAC Reveals New Strategy for Cybersecurity & Resilience of the Global Financial System"
[5]: https://www.fda.gov/medical-devices/software-medical-device-samd/artificial-intelligence-enabled-medical-devices "Artificial Intelligence-Enabled Medical Devices | FDA"
[6]: https://www.roche.com/media/releases/med-cor-2026-03-16?utm_source=chatgpt.com "Roche launches NVIDIA AI factory to accelerate the ..."
[7]: https://www.aha.org/2024-03-15-aha-survey-change-healthcare-cyberattack-significantly-disrupts-patient-care-hospitals-finances "AHA Survey: Change Healthcare Cyberattack Significantly Disrupts Patient Care, Hospitals’ Finances | AHA"
[8]: https://www.england.nhs.uk/synnovis-cyber-incident/ "NHS England » Synnovis cyber incident"
[9]: https://www.ithome.com.tw/news/167327 "2025年2月馬偕醫院遭勒索軟體攻擊事件歷程總整理（持續更新中） | iThome"
[10]: https://www.fda.gov/regulatory-information/search-fda-guidance-documents/artificial-intelligence-enabled-device-software-functions-lifecycle-management-and-marketing "Artificial Intelligence-Enabled Device Software Functions: Lifecycle Management and Marketing Submission Recommendations | FDA"
[11]: https://www.eba.europa.eu/publications-and-media/publications/risk-assessment-report-december-2025 "Risk Assessment Report - December 2025 | European Banking Authority"
[12]: https://nvd.nist.gov/vuln/detail/cve-2025-35975 "NVD - cve-2025-35975"
[13]: https://www.fda.gov/medical-devices/safety-communications/cybersecurity-vulnerabilities-certain-patient-monitors-contec-and-epsimed-fda-safety-communication "Cybersecurity Vulnerabilities with Certain Patient Monitors from Contec and Epsimed: FDA Safety Communication | FDA"
[14]: https://www.nist.gov/news-events/news/2026/04/nist-updates-nvd-operations-address-record-cve-growth "NIST Updates NVD Operations to Address Record CVE Growth | NIST"
[15]: https://bankingjournal.aba.com/2026/04/fs-isac-releases-advisory-on-hardening-cybersecurity-from-ai/ "FS-ISAC releases advisory on hardening cybersecurity from AI | ABA Banking Journal"
[16]: https://www.cisa.gov/known-exploited-vulnerabilities-catalog?utm_source=chatgpt.com "Known Exploited Vulnerabilities Catalog"
[17]: https://www.ibm.com/reports/data-breach "Cost of a data breach 2025 | IBM"
[18]: https://documents.trendmicro.com/assets/research-reports/the-ai-fication-of-cyberthreats-trend-micro-security-predictions-for-2026.pdf "The AI-fication of Cyberthreats"
