# TTS 研究語音製作方法論 v1

## 目的

本方法論用於研究、教學、簡報、臨床前問診模擬、ASR / LLM demo 的合成語音製作。

核心目標是把 TTS production 從「人工感覺可用」推進到「可記錄、可比較、可重現、可自動檢查」。每次生成後，流程必須用 ASR 回轉錄、術語比對、音訊品質檢查、chunk consistency、hash 與 provenance 來判斷是否可接受。人工聽審不作為本流程的必要 gate。

## 適用範圍

- 研究刺激材料與教學語音。
- 簡報、課程、demo、臨床前問診模擬音檔。
- ASR / LLM pipeline 測試資料。
- TTS 模型、reference voice、chunking、文字設計、後製參數的比較實驗。

不適用於未取得授權的真人聲音複製、需要臨床診斷承諾的音檔、或會被誤認成真人即時溝通的高風險使用情境。

## 基本原則

1. source text 與 model-facing text 分開。
2. 先修文字，再修音訊。
3. 先 pilot render，再 full render。
4. ASR back-transcription 作為主要 QA gate。
5. 所有輸出都保存 provenance。
6. 真人 reference voice 必須記錄來源、授權與使用範圍。

## Pipeline

```text
source text
-> model-facing text
-> pronunciation lexicon
-> chunking
-> pilot render
-> ASR back-transcription
-> automated QA
-> local repair
-> full render
-> loudness/stitching
-> final package
-> archive
```

## 標準流程

1. 凍結 source text，記錄來源、版本、SHA-256 與研究用途。
2. 改寫 model-facing text，移除給人看的標題、表格、註解、投影片標籤與 planning note。
3. 建立 pronunciation lexicon，標出 critical terms。
4. 切 chunk，確保每個 output_prefix 穩定、可局部重生。
5. 產生 1 到 3 個 pilot clips，覆蓋開場、術語密集段、結尾或最高風險段。
6. 跑 ASR back-transcription。
7. 計算 CER / WER / keyword accuracy。
8. 檢查 clipping、silence、LUFS、sample rate、channel layout、chunk boundary。
9. 依 failure taxonomy 修文本或參數。
10. full render。
11. loudnorm / stitching，保存 raw、processed、final 的 hash。
12. 再跑一次 automated QA。
13. 填 experiment card。
14. 保存 hash、command、QA result、runtime、device、model checkpoint。
15. 輸出 final package；公開 repo 只放方法、參數、hash、QA 結果與可重現路徑。

## Auto / Semi-Auto QA Gate

每次 TTS 生成後，至少產生以下 evidence：

- ASR transcript。
- CER / WER 或可替代的 normalized text-diff 指標。
- critical term accuracy。
- term_error_list.csv。
- audio quality report：clipping、long silence、loudness、sample rate、channel layout。
- chunk consistency report：缺字、截尾、output_prefix、parent chunk stitch。
- SHA-256：source text、model-facing text、reference audio、raw audio、processed audio、final package。
- provenance：model、checkpoint、device、Python、CUDA、ffmpeg、command、seed、temperature、top-p、speed / tempo。

接受條件由 `tts-auto-qa-rubric.md` 管理。人工主觀聽感可以作為研究備註或 stakeholder feedback，但不能替代自動 QA gate。

## 公開與私有邊界

公開 repo 可以保存：

- 方法論、模板、lexicon 範本。
- experiment card。
- QA 結果摘要。
- hash、command、model version、參數。
- 可公開的 model-facing text 或 teacher-readable transcript。

公開 repo 不保存：

- reference audio。
- generated audio。
- failed samples。
- private voice data。
- 未授權的真人聲音。
- 受試者資料、臨床資料、私人聯絡紀錄。

local/private storage 預設位置：

```text
assets/tts-local-only/
.local/
~/Downloads/<project-specific-package>/
```

## Provenance Minimum

每次實驗最少要記錄：

- Experiment ID。
- project / purpose。
- source text path and SHA-256。
- model-facing text path and SHA-256。
- pronunciation lexicon path。
- TTS model and checkpoint / commit。
- ASR model and checkpoint / commit。
- generation command。
- output_prefix。
- output files and SHA-256。
- ASR transcript path。
- CER / WER。
- critical term accuracy。
- audio quality status。
- accepted / rejected。
- failure type and repair action。

## 對這個 repo 的使用方式

- 方法論放在 `docs/tts-methodology/`。
- 每次實驗卡放在 `logs/tts-experiments/`。
- QA 結果摘要放在 `qa/tts-auto-checks/`。
- 可重用模板放在 `templates/`。
- reference audio、生成音檔、失敗樣本放在 `assets/tts-local-only/` 或 `.local/`，不得提交。

## BreezyVoice 經驗抽象

這次 BreezyVoice 工作提供了幾個可重用規則：

- model-facing text 要比人類閱讀稿更機械、更清楚、更短。
- 中英邊界要明確，避免術語黏在中文句子中。
- dense case passages 應改成故事型敘述：setup、event path、clinical implication、review takeaway。
- full master 優先用單一 global tempo normalization，避免每段任意調速。
- ASR 是主要 gate，但 mixed Mandarin / English 的 ASR drift 要用 critical term list 和 warning regions 管理。
- output_prefix 必須穩定，讓 failed chunk 可以局部重生。

## 下一版應補的自動化

- `tools/run_tts_auto_qa.py`：統一讀取 source text、ASR transcript、lexicon、ffprobe / ffmpeg report。
- `term_error_list.csv` 自動輸出。
- chunk boundary 自動掃描。
- QA JSON schema。
- experiment card 自動產生器。
- model comparison report 自動更新。
