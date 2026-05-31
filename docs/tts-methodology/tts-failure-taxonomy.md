# TTS Failure Taxonomy

## Text-Side Failure

長句、標點錯、縮寫太多、術語堆疊、中英黏在一起。

常見訊號：

- ASR transcript 出現 meaning-changing omission。
- critical term 消失或被替換。
- 同一句重複出現多個技術縮寫後，模型吞字或音節漂移。
- 條列式文字被念成不自然片段。

優先修法：

- 縮短句子。
- 改成台灣繁體中文口語。
- 固定術語讀法。
- 重切 chunk。

## Model-Side Failure

吞字、重複、幻覺音節、聲音飄移、語氣突然改變。

常見訊號：

- ASR transcript 出現 repeated sentence loop。
- audio quality 正常，但文字內容有無來源音節。
- 同一模型在長句或術語密集段失控。

優先修法：

- 降低單一 chunk 長度。
- 減少英文與數字密度。
- 調整 temperature / top-p / speed。
- 換 voice mode 或 checkpoint。

## Reference-Side Failure

reference audio 太吵、太短、語氣不合、音質不穩。

常見訊號：

- 聲音特徵不穩。
- 背景噪音或錄音空間感被帶入生成音。
- 同一文本在 no-reference mode 較穩，在 prompt mode 反而不穩。

優先修法：

- 換乾淨 close-mic reference。
- 記錄 consent / rights。
- 固定 reference SHA-256。
- 回到 default voice 作 baseline。

## Chunk-Side Failure

切段位置不自然、上下文斷裂、段落開頭怪。

常見訊號：

- chunk 開頭缺主詞或承接詞過重。
- chunk 結尾被切斷。
- parent stitch 後段落轉折突兀。

優先修法：

- 讓 chunk 從完整句開始、完整句結束。
- 在 chunk 開頭加一句簡短 context。
- 保留穩定 output_prefix，只重生 failed chunk。

## Stitching-Side Failure

接縫突兀、音量不一致、尾音被切掉。

常見訊號：

- parent chunk duration 正常，但 full master 有接縫跳動。
- silence-ms 太短或太長。
- loudness normalization 前後差異過大。

優先修法：

- 統一 sample rate 與 channel layout。
- 檢查 tail trim。
- 使用一致的 silence-ms。
- full master 做一次 loudnorm，不任意逐段調整。

## Delivery-Side Failure

YouTube 壓縮、手機喇叭聽不清、影片音量太小。

常見訊號：

- local WAV 正常，壓縮後術語不清。
- 手機喇叭播放時 sibilance 或低音不足。
- 影片音量與旁白或背景音不匹配。

優先修法：

- 使用 -16 LUFS around video narration target。
- 產生 M4A / MP3 delivery copy 時保留 WAV master。
- 針對平台壓縮後版本再跑 ASR smoke check。

## Research-Side Failure

TTS artifact 影響研究刺激材料效度。

常見訊號：

- 受試者反應可能來自語音怪異感，而不是研究內容。
- 不同模型語氣差異變成 confound。
- reference voice 權利或 synthetic voice disclosure 不完整。

優先修法：

- 在研究設計中記錄 TTS 作為刺激材料變因。
- 使用同一模型、同一 voice、同一 loudness。
- 以 auto QA 指標證明不同材料可比較。
- 補 IRB / consent / disclosure 記錄。
