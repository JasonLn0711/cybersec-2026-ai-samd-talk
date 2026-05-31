# TTS Text Design Guide

model-facing text 是給模型念的，不是給人閱讀的稿。它的優先目標是穩定發音、穩定節奏、降低重複與吞字，不是版面漂亮。

## 句子

- 每句控制在 15 到 25 個中文字左右。
- 技術長句拆成短句。
- 條列內容改成口語連貫句。
- 每句只承載一個主要動作、概念或因果關係。
- case passage 用短 setup、event path、clinical implication、review takeaway。
- 避免在同一句塞入多個英文縮寫、產品名、法規名與數字。

## 標點

- 逗號處理短停頓。
- 句號處理語意終點。
- 需要較明顯轉折時，用新句，不用過長逗號串。
- 避免括號、斜線、過密標點。
- 避免 Markdown heading、表格符號、項目符號進入 model-facing text。
- 中英邊界需要明確；必要時插入可被 TTS 穩定處理的停頓符號。

## 英文與縮寫

- ASR 固定寫成 A-S-R 或 automatic speech recognition。
- LLM 固定寫成 L-L-M 或 large language model。
- FDA 510(k) 固定寫成 F-D-A five ten k。
- 第一次出現用全名，後面才用縮寫。
- 專有名詞、產品名、標準縮寫可保留英文，但要在 pronunciation lexicon 中固定讀法。
- 非必要英文片語優先改成台灣繁體中文口語。

## 數字

- 2026 改成「二零二六年」或固定英文讀法。
- 15 minutes 改成 fifteen minutes，或改成「十五分鐘」。
- kHz、ms、GB、GPU 要固定讀法。
- 百分比、時間、法規條號、版本號要在同一專案內保持一致。
- 若 ASR 容易誤辨數字，model-facing text 應改成更穩定的口語讀法。

## 術語

- critical terms 必須列入 pronunciation lexicon。
- 會影響研究判讀的術語不可只靠模型自由發音。
- 如果術語在 ASR transcript 中消失、變形或被替換，該 chunk reject。
- 同一術語在同一份音檔中只能有一種預設讀法，除非 experiment card 明確記錄例外。

## Chunk 設計

- chunk 不要從代名詞或不完整因果句開始。
- chunk 結尾不要停在名詞片語、英文縮寫或半句。
- 每個 chunk 開頭給模型足夠語意 context。
- 每個 output_prefix 必須穩定，便於局部重生與 hash 追蹤。
- pilot clips 至少覆蓋開頭、術語密集段與收尾段。

## Repair 順序

1. 修 model-facing text。
2. 修 pronunciation lexicon。
3. 修 chunk boundary。
4. 修 TTS 參數。
5. 修 reference audio 或 voice mode。
6. 最後才做 audio-only edit。

## 常見禁忌

- 直接把人類閱讀稿送進 TTS。
- 把投影片標題、source note、Markdown 表格、speaker cue 留在輸入中。
- 用後製剪輯掩蓋可由文本解決的吞字、重複或術語錯誤。
- 用人工主觀聽感取代 ASR / audio / hash / chunk QA evidence。
