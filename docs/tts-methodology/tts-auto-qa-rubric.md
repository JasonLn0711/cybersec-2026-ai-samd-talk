# TTS Automated QA Rubric

本 rubric 定義 TTS 研究語音材料的 auto / semi-auto QA gate。接受判斷以 ASR 回轉錄、術語比對、音訊品質、chunk consistency、hash / provenance 為主，不納入人工聽審作為必要 gate。

## Acceptance Gate

```text
CER <= 8%
WER <= 12%
Critical term accuracy = 100%
No clipping
No broken chunk boundary
No meaning-changing omission
```

任一 critical condition 失敗，該 clip 或 full package reject。可局部重生 failed chunk，不需要重跑整份音檔。

## ASR Back-Transcription

- CER <= 8%。
- WER <= 12%。
- Critical term accuracy = 100%。
- No meaning-changing omission。
- No repeated sentence loop。
- ASR model、checkpoint、device、command 必須記錄。
- ASR transcript 必須保存路徑與 SHA-256。

## Pronunciation Lexicon Check

- 所有 critical terms 必須出現在 ASR transcript。
- 錯誤術語列入 `term_error_list.csv`。
- critical term 錯誤即 reject。
- non-critical term 錯誤可標記為 warning，但必須在 experiment card 說明是否影響研究用途。

`term_error_list.csv` 建議欄位：

```csv
experiment_id,chunk_id,term,preferred_reading,asr_observed,error_type,critical,decision,repair_action
```

## Audio Quality Check

- No clipping。
- No abnormal long silence > 2.0 sec。
- No sudden loudness jump > 6 dB。
- Integrated loudness target: around -16 LUFS for video narration。
- Same sample rate and channel layout across chunks。
- Final package 應記錄 sample rate、channel、duration、LUFS、bitrate、SHA-256。

建議檢查項目：

- ffprobe：duration、sample_rate、channels、bit_rate。
- ffmpeg astats：peak level、clipping 風險。
- ffmpeg silencedetect：長靜音。
- loudnorm：integrated loudness、true peak、LRA。

## Chunk Consistency

- chunk 開頭不得缺字。
- chunk 結尾不得被切斷。
- output_prefix 必須穩定。
- failed chunk 可以局部重生。
- parent chunk stitch 必須保留 chunk order。
- full stitch 必須記錄 silence-ms、stitch command、parent list、final hash。

## Provenance Check

每個 accepted output 必須能回溯到：

- source text path / SHA-256。
- model-facing text path / SHA-256。
- pronunciation lexicon path / SHA-256。
- TTS model / checkpoint / commit。
- ASR model / checkpoint / commit。
- generation command。
- device / Python / CUDA / ffmpeg。
- output_prefix。
- raw output hash。
- processed output hash。
- final package hash。

## Decision Labels

- `accepted_auto_gate`：所有 required checks pass。
- `accepted_with_warnings`：critical checks pass，但有 non-critical warnings。
- `rejected_text_repair_required`：文本或術語造成失敗。
- `rejected_audio_repair_required`：clipping、silence、LUFS、stitching 失敗。
- `rejected_provenance_incomplete`：缺少 hash、command、model 或來源記錄。
- `research_use_blocked`：授權、IRB、voice rights 或刺激材料效度不成立。

## Semi-Auto Use

半自動 gate 允許人工解讀 ASR drift 的原因，但必須留下可檢查的 evidence：

- ASR warning region。
- source text 對照。
- critical term list。
- decision rationale。
- repair action 或 accepted_with_warnings reason。

人工聽感只能補充 context，不能替代 gate 指標。
