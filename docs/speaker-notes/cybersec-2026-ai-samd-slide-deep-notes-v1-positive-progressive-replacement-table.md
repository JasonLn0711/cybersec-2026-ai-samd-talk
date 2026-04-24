# CyberSec 2026 Positive Progressive Replacement Table

Source:

`docs/speaker-notes/cybersec-2026-ai-samd-slide-deep-notes-v1.md`

Revised script:

`docs/speaker-notes/cybersec-2026-ai-samd-slide-deep-notes-v1-positive-progressive-zh-tw.md`

| Original Sentence | Revised Sentence | Transformation Type |
| --- | --- | --- |
| 這一版的核心不是「把所有資訊塞進投影片」，而是把每一頁背後的知識、案例、趨勢、工作流都準備好 | This version uses progressive, question-driven, cause-effect, and decision-support language. It keeps the DeepBT Detector-Plus product evidence examples and the compact 14-slide structure. | progressive |
| 主軸是「AI SaMD 團隊賣的不是模型，而是一個 trustable、patchable、auditable 的臨床產品系統」 | Core path: Boundary -> Evidence -> Decision -> Repair Proof. | progressive |
| 資安不再是外掛文件，而是品質管理系統的一部分。 | cybersecurity evidence 要進入產品設計、標示、上市前文件與上市後維護。 | cause-effect |
| 這一頁的任務不是介紹你有多厲害，而是讓所有人立刻知道... | 第一頁只需要讓觀眾看見今天的路徑：從 AI model，走到可以被醫院使用、被團隊修補、被審查者檢查的醫療軟體產品。 | progressive |
| AI 醫療產品不是只要會算答案，它還要在醫院裡安全地被使用。 | 模型會算答案，是第一層。醫院接著會問：資料從哪裡來？誰可以使用？結果如何確認？系統故障時如何恢復？漏洞出現時誰修？修完後如何證明？ | question |
| 產品不是只有 Brain Tumor AI Module，而是包含 Web UI... | 產品從 Brain Tumor AI Module 延伸到 Web UI、Integration Module、Docker、WSL2、DCMTK、Node.js、Python、PACS / DICOM workflow、SBOM、provenance、integrity、support status。 | progressive |
| 我們不是為了送審而補文件，我們是在建立產品信任能力。 | FDA 524B 的要求會轉化為上市後營運能力。 | decision |
| 今天不是背法規，也不是展示工具清單。 | 今天我想用一個問題串起來：一個 AI model 要變成可信任的醫療產品，中間需要留下哪些證據和決策？ | question |
| 這頁是 compliance beat，不是敘事頁。 | 這頁是大會 required disclaimer。它看起來是形式頁，但在醫療、資安、法規裡，邊界感本身就是專業。 | progressive |
| 你賣的不是模型 | 模型是起點 | progressive |
| 你不是賣一顆很厲害的引擎，你是賣一台真的要上路的車。 | 模型像引擎，SaMD 像一台要上路的車。引擎很強是必要條件；煞車、儀表板、保養紀錄、召回流程、駕駛說明、事故處理，會決定這台車能否被信任。 | progressive |
| 這不是全自動取代醫師，而是放進臨床 workflow 的 decision-support product。 | 這個設定把模型帶進 clinical workflow。它提醒觀眾：這是一個 decision-support product... | progressive |
| 模型只是一個 asset，周圍還有... | 這是一個 decision-support product，要管理 intended use、human-in-the-loop、DICOM viewer、Temporary DICOM Storage、PACS... | progressive |
| 這不是恐嚇，而是醫療器材上市後責任的現實。 | 接下來，臨床使用會帶出更細的問題... | question |
| AI 醫材不是未來式，而是現在式 | AI 醫材正在快速增加，產品責任需要同步建立。 | cause-effect |
| 答案不是因為 AI 很流行，而是因為 AI 正在變成 care infrastructure。 | 2026 年談 AI，要一路看到 runtime、資料、identity、update chain、support path，以及最後連到 clinical workflow 的路徑。 | progressive |
| 這不是要你在簡報放 Roche logo，而是可以用一句話說... | 大型 AI factory 支撐 diagnostics、therapeutics、clinical trials 和資料洞察，這代表 AI 已經開始變成 operating backbone。 | cause-effect |
| 風險不是突然變大，是產品每多接一個東西，責任就跟著長大。 | 風險增加，通常是因為產品能力變強、連接變多、責任變重。 | cause-effect |
| FDA 看的是 device 在真實系統中的風險，不是 isolated algorithm 的漂亮宣稱。 | FDA 2026 Guidance 的意義，是把這些能力接到 quality management system。 | cause-effect |
| 法規要的是證據，不是口號。 | 當邊界被定義，風險位置就會浮現。風險被看見後，證據鏈才能建立。決策被記錄後，修補能力才可被驗證。 | cause-effect |
| NIST 在這裡是 shared language，不是 checklist。 | NIST CSF 2.0 和 AI RMF 的價值，是提供跨角色共同語言，讓不同角色能討論同一個風險。 | decision |
| 不要只保護模型，還要保護 runtime 和 infrastructure。 | AI stack security 包含 SBOM、model integrity、runtime isolation、secrets、API access、logging、update path、software supply chain。 | progressive |
| 這三個少一個，都不是完整的產品安全。 | 一個可信 AI 團隊要能回答三種問題：模型能做什麼、有哪些限制；公司誰負責風險決策；模型跑起來的軟體和環境如何被保護。 | question |
| 這些不是文書細節，而是「模型產品如何被追溯」的基本功。 | 這些紀錄是模型產品可追溯的基本功。 | progressive |
| viewer/parser 不是「包裝層」，而是真正攻擊面。 | 這讓 viewer / parser 從包裝層變成真實 attack surface。 | progressive |
| 醫療 AI 的資安不是廠商單方面能完成，也不是醫院單方面能完成。 | 產品接到 PACS / HIS 後，需要處理內部網路、shared responsibility、downtime fallback。 | decision |
| Availability 不是系統 uptime 而已，是醫師能不能在需要時取得結果。 | Availability 是醫師需要結果時，系統能不能用。 | progressive |
| 不是因為資安人員想把自己講得很重要，而是因為醫療現場... | 醫療現場已經告訴我們，系統中斷很快就會變成照護中斷。 | cause-effect |
| 測試不是為了報告好看，而是為了產出決策。 | 測試結果要能進入 owner、severity、due date、fix decision、retest evidence。這樣測試才會支撐 release judgment。 | decision |
| Patch SLA 不是 FDA 原文裡的一個固定術語，而是... | Patch SLA 是把 FDA 524B 的 updates / patches、reasonable time、CVD、postmarket vulnerability management 翻譯成公司 operating model。 | decision |
| Patch SLA 不是越快越好，而是越快控制風險，同時不能破壞 patient safety。 | 醫療 AI 的 patch 要同時追求兩件事：快速控制風險，並維持 patient safety。 | decision |
| 30 / 60 / 90 不是法規要求，也不是固定 SLA 格式。 | 30 / 60 / 90 是 adoption scaffold。它的用途是讓小團隊啟動第一個 evidence loop；正式時程仍要由產品風險、臨床影響、客戶環境與 QMS 決策定義。 | decision |
| 重點不是三個月變完美，而是三個月後... | 30 天看見產品，60 天讓風險進流程，90 天證明修補能力。 | progressive |
| 不是產品做完才找資安補洞，不是送審前才補文件... | Threat Modeling 在架構設計時進來，SBOM 隨 build artifact 留下，testing 連到 release gate，Patch SLA 連到 finding governance，retest evidence 形成 repair proof。 | progressive |
| 真正成熟的團隊，不是文件最多的團隊，而是... | 成熟團隊會讓每個風險都知道怎麼證明、怎麼修、怎麼追。 | decision |
| AI 軟體醫材的資安，不是保護一個模型，而是在真實醫療世界裡... | 如果我們能說清楚 Boundary、留下 Evidence、做出 Decision、保存 Repair Proof，稽核就會從最後補文件，變成檢查一套已經在運作的產品信任系統。 | cause-effect |

