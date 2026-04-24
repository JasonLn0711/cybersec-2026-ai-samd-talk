# CyberSec 2026 Layered Rewrite Change Log

Source file revised from:

`docs/speaker-notes/cybersec-2026-ai-samd-keynote-expansion-reader-easygoing-zh-tw-2026-04-24.md`

Revised full talk:

`docs/speaker-notes/cybersec-2026-ai-samd-keynote-expansion-reader-layered-zh-tw-2026-04-24.md`

| Original sentence | Revised sentence | Reason for revision |
| --- | --- | --- |
| 「答案當然不是。或者比較精準地說，那只是答案的一小部分。」 | 「準確率當然重要。ROC curve、validation score、benchmark，也都重要。它們讓我們知道模型有沒有資格進入下一階段。」 | 改掉直接否定，先承認觀眾理解，再帶到下一層。 |
| 「所以今天這場，我們不談 AI hype。也不背法規。」 | 「今天這場，我會用 AI SaMD 做主線，因為醫療器材的產品生命週期要求比較清楚。可是我們真正要練習的是一種高信任產業都會需要的思考方式。」 | 從排除式定位改成正向定位，讓開場更成熟。 |
| 「所以我們先不要問：AI model 準不準。這是錯的第一個問題。」 | 「不同產業的痛點不一樣，但信任問題很像：這個 AI 進入真實流程之後，團隊能不能說清楚它在哪裡、誰負責、怎麼修、怎麼證明？」 | 避免說觀眾問題是錯的，改用問題升級。 |
| 「未來真正的 AI 資安，不會只是 prompt injection，也不會只是 model robustness。」 | 「AI 原本回答問題。現在 AI 開始接資料、接 API、接 workflow、接 decision、接人命、接錢、接國家關鍵服務。」 | 用遞進描述建立 tension，避免重複「不只是」。 |
| 「這句話在研究裡成立。在產品裡不成立。在醫療裡更不成立。」 | 「很多團隊一開始是在做模型。這很合理，因為沒有模型能力，就沒有後面的產品。下一層問題會在產品化後出現。」 | 保留原意，但先肯定研究階段，再帶到產品階段。 |
| 「醫院要的是能上臨床道路的整台車，不是一顆單獨引擎。」 | 「醫院要的是能上臨床道路的整台車。它要知道 intended use、human-in-the-loop、輸入資料、輸出限制、patch、incident reporting、downtime workflow。」 | 把 slogan 變成具體採購與治理問題。 |
| 「AI 進入醫療，不只是 AI risk。AI 進入金融，不只是 fintech risk。AI 進入 OT，不只是 automation risk。」 | 「AI 進入高信任流程後，風險會從 AI risk 延伸成 infrastructure risk。」 | 用延伸式語言取代連續否定。 |
| 「問題就不是『模型可不可以跑』，而是『流程能不能活下來』。」 | 「以前 model 出錯，可能是一個 prediction 錯。現在 infrastructure 出錯，可能是一整段流程停。」 | 改成時間與層次推進，保留壓力。 |
| 「風險不是突然變大。是產品長大了。」 | 「風險變大，通常不是因為團隊突然變差，而是產品長大了。」 | 保留少量強對比，但把語氣放柔，避免責備團隊。 |
| 「法規真正問的不是：你有沒有文件。法規真正問的是：你有沒有證據鏈。」 | 「一家公司說自己很安全，這句話本身還不夠。醫師不會只聽病人說『我覺得我很健康』，就完成健康檢查。」 | 用情境比喻帶出 evidence chain，比直接否定更可聽。 |
| 「法規要的是證據，不是口號。」 | 「法規要的是證據，不是口號。」 | 保留為全場唯一強 contrast anchor，因為它短、清楚、有記憶點。 |
| 「不是模型。不是工具。是語言。」 | 「接下來我們談很多公司真正卡住的地方：語言。」 | 移除三連否定，改成直接進入主題。 |
| 「如果這三種語言接不起來，問題就會漂浮在組織裡。」 | 「如果這三種語言接不起來，問題就會漂浮在組織裡。AI 團隊覺得那是資安問題，資安團隊覺得那是產品問題，法規覺得那是送審問題，主管覺得那是工程問題。」 | 保留原句並補足跨團隊情境，使 manager 和 engineer 都能對上。 |
| 「攻擊者不一定要碰 AI。他只要碰 AI 周圍那一圈。」 | 「攻擊者可能不碰 AI 的核心，而是碰 AI 周圍那一圈。」 | 保留必要對比，但降低斷言感。 |
| 「成熟做法不是甩鍋，也不是全包。」 | 「成熟做法是把 responsibility boundary 寫清楚。」 | 用決策語言取代否定語言。 |
| 「Availability 在醫療裡不是 uptime。」 | 「Availability 在醫療裡，是醫師需要結果時，系統能不能用。」 | 改成定義句，降低反駁感。 |
| 「Integrity 在醫療裡不是 hash 沒變。」 | 「Integrity 在醫療裡，是醫師能不能相信這個 AI output。」 | 改成定義句，讓非技術觀眾更容易跟上。 |
| 「Repairability 不是工程流程。」 | 「Repairability 在醫療裡，是出事後產品能不能安全恢復。」 | 改成現場語言，強化 clinical meaning。 |
| 「真正成熟的測試，不是問：我們做了哪些測試？而是問：每一種測試回答了哪一個決策問題？」 | 「成熟的 testing portfolio 會先問：每一種測試回答哪一個決策問題？」 | 保留決策導向，減少口號式對比。 |
| 「測試最重要的不是產生 finding。測試最重要的是產生 decision。」 | 「測試的價值不只在 finding 數量，而在 finding 能不能進入 owner、severity、due date、fix decision、retest evidence。」 | 從 slogan 改成 workflow 說明。 |
| 「Patch SLA 的核心不是天數。Patch SLA 的核心是 decision。」 | 「Patch SLA 很容易被誤解成天數表。Critical 幾天、High 幾天、Medium 幾天。天數有用，但天數只是外層。核心是 decision。」 | 先承認天數有用，再帶到 decision layer。 |
| 「漏洞會更多。AI 會讓 finding 更快。攻擊者會更自動化。Defender 的瓶頸不會只是會不會修，而是會不會判斷。」 | 「漏洞世界已經爆量。CVE 成長、KEV 優先排序、AI 加速攻擊者 reconnaissance 和 exploit development，都讓 vulnerability management 不能只靠記憶與英雄。」 | 用原因與壓力取代重複對比。 |
| 「所以醫療 AI 的 patch 不是越快越好。」 | 「所以醫療 AI 的 patch 要同時追求兩件事：快速控制風險，並維持 patient safety。」 | 用雙目標決策語言取代否定。 |
| 「答案不是放棄。答案也不是假裝自己是大公司。」 | 「小團隊需要的第一步，是建立第一個 evidence loop。」 | 移除連續否定，直接給可執行路徑。 |
| 「請注意，30/60/90 不是法規要求。不是什麼神聖時程。」 | 「30/60/90 是 adoption scaffold。它讓小團隊從口頭記憶，走向可重複、可稽核的證據循環。」 | 從防禦式澄清改成用途說明。 |
| 「AI 一旦進入高信任流程，它就不再只是模型能力問題。」 | 「AI 一旦進入高信任流程，就會承接產品責任。」 | 更短、更平穩，避免「不再只是」。 |
| 「Threat model 不是送審前趕出來的。SBOM 不是客戶問才整理的。Patch SLA 不是出事才建立的。」 | 「Threat Modeling 要在產品邊界形成時進來。SBOM 要在 dependency 被引入時留下。Patch SLA 要在漏洞發生前建立 decision path。」 | 把收尾改成正向行動節奏。 |
| 「文件再多也只是 PDF 森林。」 | 「這四題答不出來，文件再多也很難變成信任。」 | 保留警示，但讓語氣更穩。 |
| 「模型只是起點。」 | 「模型是起點。」 | 「只是」容易形成降格語氣；改成承認模型價值的起點語言。 |

