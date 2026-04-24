# CyberSec 2026 Positive Progressive Style Guide

## 核心原則

用結構引導理解與決策。讓觀眾感覺自己原本理解的一層被自然帶到下一層。

## 舞台稿禁止使用的句型

以下句型會用否定製造對比，舞台稿應改寫成 progression、question、cause-effect 或 decision-support：

| Pattern |
| --- |
| 「不是...」 |
| 「不是...而是...」 |
| 「不是在...而是在...」 |
| 「不只是...」 |
| 「不要...」 used as rhetorical emphasis |
| 「並非...」 used as rhetorical emphasis |
| “not A but B” |
| “not just” |
| “rather than” |

技術事實限制可以保留，例如 `無法存取`、`不支援 cloud storage`、`不可用狀態`，或 vulnerability impact 描述。

## 核准句型

| Pattern Type | Pattern |
| --- | --- |
| Progressive | A 是起點，接下來會延伸到 B。 |
| Progressive | 從 A 開始，問題會自然走到 B。 |
| Progressive | 第一層是 A，下一層會看到 B。 |
| Question-driven | 如果發生 X，系統如何回應？ |
| Question-driven | 當條件改變時，決策如何被做出？ |
| Question-driven | 這樣的系統，如何被驗證與持續維護？ |
| Cause-effect | 當邊界被定義，風險位置就會浮現。 |
| Cause-effect | 風險被看見後，證據鏈才能建立。 |
| Cause-effect | 決策被記錄後，修補能力才可被驗證。 |
| Decision-support | 這裡的重點在於團隊如何做決策。 |
| Decision-support | 這些資訊會影響 release 與 risk acceptance。 |
| Decision-support | 這一步會直接影響是否可以進入臨床場域。 |

## Before / After Examples

| Before | After |
| --- | --- |
| 不是模型，而是產品。 | 模型是起點，接下來會延伸到整個產品系統。 |
| 不是 accuracy，而是 trust。 | Accuracy 會帶出下一個問題：系統如何被信任？ |
| 這不是法規，是產品能力。 | 這些要求會轉化為產品在營運中的能力。 |
| Testing 不是為了報告好看，而是為了產出決策。 | Testing 要回答 release decision：哪些風險已控制、哪些需要修補、哪些需要 compensating control。 |
| Patch SLA 不是越快越好。 | Patch SLA 要同時追求快速控制風險與維持 patient safety。 |

## Slide Rhythm Rules

每一頁都使用：

1. **一個問題**：這頁要處理的 decision pressure。
2. **具體情境**：scenario、product condition、case 或 workflow。
3. **一個決策 / Takeaway**：觀眾要記住的 team action 或 judgment。

建議頁面推進：

1. 從實務問題開始。
2. 說明具體情境。
3. 說清楚 boundary 如何產生 evidence needs。
4. 把 evidence 轉成 decisions。
5. 用 repair proof 或 next action 收束。

## 語氣規則

- 平穩、清楚、有結構。
- 對 engineers 保持技術精準度。
- 對 managers 與非技術觀眾保持可理解性。
- 使用短句，方便 AI live translation。
- 避免 slogan stacking。
- 用 uncertainty 與 decision pressure 建立張力。
- 保留技術詞：FDA 524B, Threat Modeling, SBOM, Patch SLA, cyber device, postmarket monitoring, vulnerability management, exploit, CVD, DICOM / PACS, software supply chain, runtime environment。

## 收束句型

用四段路徑收束：

> Boundary 讓風險被看見。Evidence 讓風險可被檢查。Decision 讓風險可被治理。Repair Proof 讓信任可以被維持。
