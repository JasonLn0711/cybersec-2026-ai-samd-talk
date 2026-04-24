# CyberSec 2026 Positive Progressive Style Guide

## Core Principle

用結構引導理解與決策。讓觀眾感覺自己原本理解的一層被自然帶到下一層。

## Banned Patterns For Stage Script

These patterns create contrast through negation and should be removed from the script:

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

Factual constraints are allowed when technically necessary, such as `無法存取`, `不支援 cloud storage`, `不可用狀態`, or vulnerability impact descriptions.

## Approved Patterns

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

Every slide uses:

1. **One Question**: The decision pressure for the slide.
2. **Concrete Situation**: A scenario, product condition, case, or workflow.
3. **Decision / Takeaway**: The team action or judgment the audience should remember.

Preferred slide movement:

1. Start with a practical question.
2. Explain the concrete situation.
3. Show how boundary creates evidence needs.
4. Translate evidence into decisions.
5. Close with repair proof or next action.

## Speaking Tone Rules

- Calm and structured.
- Precise enough for engineers.
- Clear enough for managers and non-technical audiences.
- Use short spoken sentences for AI live translation.
- Avoid slogan stacking.
- Build tension through uncertainty and decision pressure.
- Preserve technical terms: FDA 524B, Threat Modeling, SBOM, Patch SLA, cyber device, postmarket monitoring, vulnerability management, exploit, CVD, DICOM / PACS, software supply chain, runtime environment.

## Closing Pattern

End with the four-part path:

> Boundary makes risk visible. Evidence makes risk inspectable. Decision makes risk governable. Repair Proof makes trust maintainable.

