# CyberSec 2026 Slide Deep Notes v1 Layered Rewrite Change Log

Source file revised from:

`docs/speaker-notes/cybersec-2026-ai-samd-slide-deep-notes-v1.md`

Revised full talk:

`docs/speaker-notes/cybersec-2026-ai-samd-slide-deep-notes-v1-layered-zh-tw.md`

| Original sentence | Revised sentence | Reason for revision |
| --- | --- | --- |
| 這一版的核心不是「把所有資訊塞進投影片」，而是把每一頁背後的知識、案例、趨勢、工作流都準備好 | 這一版保留原本的 14 頁 generated compact fallback target、DeepBT Detector-Plus 產品情境、FDA 524B / Threat Modeling / SBOM / Patch SLA / testing / 30-60-90 roadmap 等核心內容，但把語氣從反覆對比改成「把觀眾帶到下一層」。 | 把開場從否定式說明改成改寫目標與保留範圍。 |
| 主軸是「AI SaMD 團隊賣的不是模型，而是一個 trustable、patchable、auditable 的臨床產品系統」 | 全場主軸：Boundary -> Evidence -> Decision -> Repair Proof。 | 用結構主軸取代 slogan 型 contrast。 |
| 資安不再是外掛文件，而是品質管理系統的一部分。 | cybersecurity evidence 要進入產品設計、標示、上市前文件與上市後維護。 | 改成 cause-and-effect 與 QMS 語言。 |
| 這一頁的任務不是介紹你有多厲害，而是讓所有人立刻知道... | 第一頁不用急著證明講者多懂，也不用把所有框架塞進來。這頁只要讓觀眾知道... | 保留提醒，但語氣更平穩。 |
| AI 醫療產品不是只要會算答案，它還要在醫院裡安全地被使用。 | 模型會算答案，是第一層。醫院接著會問：資料從哪來？誰可以用？結果錯了誰確認？ | 以層次推進取代「不只是」。 |
| 產品不是只有 Brain Tumor AI Module，而是包含 Web UI... | 產品包含 Brain Tumor AI Module，也包含 Web UI、Integration Module、Docker、WSL2、DCMTK、Node.js、Python、PACS / DICOM workflow... | 直接擴展產品範圍，避免否定模型。 |
| 我們不是為了送審而補文件，我們是在建立產品信任能力。 | FDA 524B 要求...這些要求其實是在建立上市後營運能力。 | 從對比句改成法規到營運能力的翻譯。 |
| 今天不是背法規，也不是展示工具清單。 | 今天我想用一個問題串起來：一個 AI model 要變成可信任的醫療產品，中間需要留下哪些證據和決策？ | 開場改成問題導向，降低反駁感。 |
| 這頁是 compliance beat，不是敘事頁。 | 這頁是大會 required disclaimer。它看起來是形式頁，但在醫療、資安、法規裡，邊界感本身就是專業。 | 先說功能，再帶出專業意義。 |
| 你賣的不是模型 | 模型是起點 | 將強對比標題改成 progressive anchor。 |
| 你不是賣一顆很厲害的引擎，你是賣一台真的要上路的車。 | 模型像引擎，SaMD 像一台要上路的車。引擎很強是必要條件... | 先承認模型價值，再擴展到產品責任。 |
| 這不是全自動取代醫師，而是放進臨床 workflow 的 decision-support product。 | 這個設定把模型帶進 clinical workflow。它提醒觀眾：這是一個 decision-support product... | 用說明式語氣取代否定式定位。 |
| 模型只是一個 asset，周圍還有... | 它提醒觀眾...要管理 intended use、human-in-the-loop、DICOM viewer... | 避免降低模型，改成產品管理清單。 |
| 這不是恐嚇，而是醫療器材上市後責任的現實。 | 下一層問題會在臨床使用時出現... | 用情境壓力製造 tension。 |
| AI 醫材不是未來式，而是現在式；所以產品責任也不是未來問題 | AI 醫材正在快速增加...模型進入臨床流程後，產品責任需要同步建立。 | 減少重複否定，改成趨勢到責任的推論。 |
| 答案不是因為 AI 很流行，而是因為 AI 正在變成 care infrastructure。 | 2026 年談 AI，已經不能只停在模型檔。AI 會接 runtime、資料、identity、update chain、support path... | 改成層次擴展。 |
| 這不是要你在簡報放 Roche logo，而是可以用一句話說... | 大型 AI factory 支撐 diagnostics、therapeutics、clinical trials 和資料洞察，這代表 AI 已經開始變成 operating backbone。 | 移除防禦式說法，直接講結論。 |
| 風險不是突然變大，是產品每多接一個東西，責任就跟著長大。 | 風險增加，通常是因為產品能力變強、連接變多、責任變重。 | 語氣更穩，也保留 tension。 |
| FDA 看的是 device 在真實系統中的風險，不是 isolated algorithm 的漂亮宣稱。 | FDA 2026 Guidance 的意義，是把這些能力接到 quality management system。 | 聚焦 QMS 與 evidence，不用反駁 algorithm。 |
| 法規要的是證據，不是口號。 | 法規要的是證據，不是口號。 | 保留為全稿唯一強 contrast anchor。 |
| NIST 在這裡是 shared language，不是 checklist。 | NIST CSF 2.0 和 AI RMF 的價值，是提供跨角色共同語言。 | 用正向定義取代否定。 |
| 不要只保護模型，還要保護 runtime 和 infrastructure。 | AI stack security 包含 SBOM、model integrity、runtime isolation、secrets、API access、logging、update path、software supply chain。 | 用清單與擴展取代命令式對比。 |
| 這三個少一個，都不是完整的產品安全。 | 一個可信 AI 團隊要能回答三種問題... | 改成能力描述。 |
| 這些不是文書細節，而是「模型產品如何被追溯」的基本功。 | 這不是文書細節，而是模型產品可追溯的基本功。 | 保留一個輕對比，但不形成主節奏。 |
| viewer/parser 不是「包裝層」，而是真正攻擊面。 | 這讓 viewer / parser 從包裝層變成真實 attack surface。 | 用轉變語言取代對比語言。 |
| 醫療 AI 的資安不是廠商單方面能完成，也不是醫院單方面能完成。 | 產品接到 PACS / HIS 後，需要處理內部網路、shared responsibility、downtime fallback。 | 用責任項目取代雙重否定。 |
| Availability 不是系統 uptime 而已，是醫師能不能在需要時取得結果。 | Availability 是醫師需要結果時，系統能不能用。 | 改成定義句。 |
| 不是因為資安人員想把自己講得很重要，而是因為醫療現場... | 醫療現場已經告訴我們，系統中斷很快就會變成照護中斷。 | 去掉自我防禦，保留現場壓力。 |
| 測試不是為了報告好看，而是為了產出決策。 | 測試結果要能進入 owner、severity、due date、fix decision、retest evidence。 | 改成 decision workflow。 |
| Patch SLA 不是 FDA 原文裡的一個固定術語，而是... | Patch SLA 是把 FDA 524B 的 updates / patches、reasonable time、CVD、postmarket vulnerability management 翻譯成公司 operating model。 | 用正向定義取代否定。 |
| Patch SLA 不是越快越好，而是越快控制風險，同時不能破壞 patient safety。 | 醫療 AI 的 patch 要同時追求兩件事：快速控制風險，並維持 patient safety。 | 改成雙目標決策語言。 |
| 30 / 60 / 90 不是法規要求，也不是固定 SLA 格式。 | 30 / 60 / 90 是 adoption scaffold...讓小團隊啟動第一個 evidence loop 的方法。 | 先說用途，降低防禦語氣。 |
| 重點不是三個月變完美，而是三個月後... | 30 天看見產品，60 天讓風險進流程，90 天證明修補能力。 | 改成管理里程碑。 |
| 不是產品做完才找資安補洞，不是送審前才補文件... | Threat Modeling 在架構設計時進來，SBOM 隨 build artifact 留下，testing 連到 release gate... | 用正向工作流取代連續否定。 |
| 真正成熟的團隊，不是文件最多的團隊，而是... | 成熟團隊不一定是文件最多的團隊。成熟團隊是每個風險都知道怎麼證明、怎麼修、怎麼追的團隊。 | 保留核心張力，但語氣較柔。 |
| AI 軟體醫材的資安，不是保護一個模型，而是在真實醫療世界裡... | 如果我們能說清楚 Boundary、留下 Evidence、做出 Decision、保存 Repair Proof，稽核就不是最後補文件，而是檢查一套已經在運作的產品信任系統。 | 收束到四步路徑，避免再用反覆對比作結。 |

