# TTS Model Comparison Summary

| model | strength | weakness | accepted use | rejected use | next test |
| --- | --- | --- | --- | --- | --- |
| BreezyVoice / Breeze-ASR-25 QA path | 已有 repo 內完整 provenance、chunk manifest、RTX 5080 runtime、prompt-mode render、global tempo、loudnorm、ASR warning evidence、hash 與 handoff package 紀錄。台灣華語、醫療資安講稿與長音檔 production 經驗最完整。 | mixed Mandarin / English dense sections 仍需要 critical term QA；舊流程曾含人工聽審 gate；部分 QA 指標還未自動產生 CER / WER。 | 可作為目前研究語音 production baseline；可接受 `accepted_with_warnings` 或 `accepted_auto_gate`，前提是補齊 auto QA report。 | 不接受缺少 ASR transcript、term_error_list、audio quality report 或 rights record 的新輸出。 | 建立 `tools/run_tts_auto_qa.py`，對 v3 / v1.1 final package 回填 CER / WER、critical term accuracy、audio quality、chunk consistency。 |
| F5-TTS | 可能適合快速 voice cloning baseline 與跨模型比較。 | 本 repo 目前沒有可驗證的 F5-TTS 生成命令、checkpoint、音檔 hash、ASR transcript 或 QA report。 | 只接受未來重新跑出的實驗，且必須通過本方法論的 auto QA gate。 | 不接受作為目前研究語音材料或比較結論來源。 | 建立 pilot：同一 source text、同一 lexicon、1 到 3 個 pilot clips、ASR 回轉錄、audio QA、hash。 |
| GPT-SoVITS | 可能適合 voice conversion / reference voice comparison。 | 本 repo 目前沒有可驗證的 GPT-SoVITS 生成命令、checkpoint、音檔 hash、ASR transcript 或 QA report。 | 只接受未來重新跑出的實驗，且必須通過本方法論的 auto QA gate。 | 不接受作為目前研究語音材料或比較結論來源。 | 建立 pilot：同一 source text、同一 lexicon、同一 reference rights record、ASR 回轉錄、audio QA、hash。 |

## Interpretation Rule

這張表只比較 repo 內可驗證 evidence。沒有命令、hash、ASR、QA report 的模型嘗試，應標記為 `rejected_provenance_incomplete`，直到重新產生可檢查的 pilot package。
