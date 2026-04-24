# CyberSec 2026 Speaking Style Guide

## Core Principle

> 不推翻觀眾的想法，要把他們帶到下一層。

這場演講的 speaker identity 是：

> 用結構讓人理解的人。

語氣要成熟、平穩、keynote-like；讓 manager 聽得出決策壓力，讓 engineer 聽得出技術精度，讓非技術觀眾聽得懂為什麼這件事重要。

## Discouraged Patterns

這些句型可以偶爾使用，但不能成為主要節奏：

| Pattern | Why to avoid |
| --- | --- |
| 不是 A，而是 B | 容易形成反駁感；用多了像 slogan。 |
| 不是在講 X，而是在講 Y | 容易讓觀眾覺得原本理解被否定。 |
| 不只是 X，而是 Y | 可用，但高頻使用會讓語氣變單調。 |
| 不是模型多強，而是出錯時怎麼辦 | 張力強，但太常用會顯得 aggressive。 |
| not A but B | English contrast pattern; avoid as main rhythm. |
| not just | Use sparingly; prefer expansion language. |
| rather than | Use sparingly; prefer decision language. |

全場最多保留 1-2 個強 contrast anchor。建議保留：

> 法規要的是證據，不是口號。

## Preferred Patterns

### 1. Progressive / Layered Style

Before:

> 不是模型，而是產品。

After:

> 模型是第一步，真正的挑戰會在產品化之後出現。

Use when moving from audience's current understanding to the next layer.

### 2. Expansion Style

Before:

> 不是 accuracy，而是 trust。

After:

> Accuracy 是起點，trust 是整個系統共同產生的結果。

Use when the original idea is valid but incomplete.

### 3. Question-driven Style

Before:

> 不是 AI 強不強，而是能不能被信任。

After:

> 如果 AI 很準，但醫院無法確認它如何被使用、如何被修補、如何被追蹤，那它能不能真正進入臨床？

Use when you want the audience to feel the decision pressure themselves.

### 4. Decision-support Style

Before:

> 這不是法規朗讀，而是產品信任。

After:

> 今天我們會把 FDA 524B、Threat Modeling、Patch SLA 連成一條可以被團隊執行的產品信任路徑。

Use when moving from concept to action.

## Slide-level Rhythm

每一頁都使用三段式：

| Section | Purpose |
| --- | --- |
| One question | 讓觀眾知道這頁要解決什麼決策壓力。 |
| One story or concrete situation | 用醫院、銀行、OT、供應鏈、patch、viewer、DICOM / PACS 等情境讓問題變具體。 |
| One decision / takeaway | 把內容收成團隊明天能做的動作。 |

每頁避免同時講太多 punchline。優先順序是：

1. 問題清楚。
2. 情境具體。
3. 決策可執行。
4. 技術詞準確。
5. Anchor line 短而少。

## Speaker Notes Rules

1. 先承認觀眾已經懂的一層，再帶到下一層。
2. 用「一旦...就...」、「當...之後...」、「下一層問題是...」建立 progression。
3. 用問題製造 tension，例如：「如果模型很準，但修補後無法證明輸出一致，醫院敢不敢繼續用？」
4. 用 cause-and-effect 取代 slogan，例如：「產品接進 PACS 後，risk register 要加入 DICOM workflow、viewer、parser、downtime fallback。」
5. 技術詞保留英文原詞，周圍用台灣繁體中文解釋。
6. FDA 524B、Threat Modeling、SBOM、Patch SLA、cyber device、postmarket monitoring、vulnerability management、exploit、CVD、DICOM / PACS、software supply chain、runtime environment 必須準確。
7. 不做不必要的自我介紹或 credential flexing。
8. 不把內容講成法規朗讀、工具清單、AI marketing copy 或 aggressive contrarian talk。

## Before / After Examples

| Before | After |
| --- | --- |
| 你賣的不是模型。 | 模型是起點；產品化之後，醫院要確認的是整條臨床使用鏈能不能被信任。 |
| 不只是 prompt injection，也不只是 model robustness。 | Prompt injection 和 model robustness 是其中兩層；產品進入醫院後，還會多出 identity、API、viewer、PACS、update chain 和 downtime workflow。 |
| Patch SLA 的核心不是天數，而是 decision。 | Patch SLA 可以從天數開始，但真正決定信任的是 decision path：applicability、severity、clinical impact、action、retest、archive。 |
| Testing 不是為了報告好看。 | Testing 要回答 release decision：哪些風險已控制、哪些需要修、哪些需要 compensating control、哪些需要延後 release。 |
| AI 產品不是只要準，而是要能被信任。 | Accuracy 讓產品有資格被討論；信任來自邊界、證據、決策與修補紀錄。 |

## Closing Rhythm

結尾要回到四個問題：

1. 我們的產品邊界清楚嗎？
2. 我們的風險能接到控制與測試嗎？
3. 我們的 finding 有決策紀錄嗎？
4. 我們能證明修補真的有效嗎？

最後收在：

> 模型是起點。大家真正想從你這裡得到的，是可以被交付責任的信任。

