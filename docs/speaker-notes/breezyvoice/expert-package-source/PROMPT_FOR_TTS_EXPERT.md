# Prompt For TTS Expert

請協助我把這份 CDE 2026 臨床醫療資安演講資料，整理成 BreezyVoice 可以穩定理解、可分段生成、可人工校對的完整逐字稿與批次輸入。

## 專案背景

這是一場約 `80` 分鐘的 CDE / TFDA 取向課程，題目是：

`臨床端對醫療器材 / 資訊系統之資安要求`

聽眾可能包含醫療器材業者、電子產業、學研單位、RA/QA、法規與醫療系統相關人員。語氣請設定成台灣華語的正式授課風格：清楚、穩定、可信、有技術深度，但不要像銷售簡報、法規朗讀、駭客展示或 AI hype 旁白。

## 我提供的資料

請先看資料包根目錄的：

- `00_README_FOR_TTS_EXPERT.md`
- `MANIFEST.txt`

核心內容在：

- `01_deck/`：靖中最後傳給我的最終 PPT。
- `02_transcripts/cde-2026-full-transcript-source-for-tts-expert.md`：Jason 前半段來源 + 靖中後半段 clean text + shared close 來源。
- `02_transcripts/cde-2026-full-batch-outline.csv`：我建議的全場分段架構。
- `02_transcripts/cde-2026-jingzhong-section-clean.txt`：靖中後半段最接近可朗讀的文字稿。
- `02_transcripts/cde-2026-jingzhong-section-timed-source.txt`：靖中後半段含 slide label / timing 的參考稿。
- `03_original_sources/`：靖中原始 DOCX。
- `04_project_context/`：專案背景與 CDE prep note。

## 請你完成的工作

請產出三個主要檔案：

1. `cde-2026-breezyvoice-merged-transcript-clean.txt`
   - 這是完整、乾淨、可人工審閱的逐字稿。
   - 請把 Jason 前半段、靖中後半段、shared close 合併成一個一致語氣的上課講稿。
   - 請依照 `01_deck/` 裡的最終版本 PPT 來設計逐字稿節奏；PPT 的 slide order、段落切換、案例密度與頁面訊息，是 pacing 的最高依據。
   - 請移除 slide labels、表格、planning notes、source notes、Markdown 標題等不應該被唸出來的文字。

2. `cde-2026-breezyvoice-merged-transcript-batch.csv`
   - 這是給 BreezyVoice 分段生成用的 batch 檔。
   - 請每列放一段適合生成的文字，建議 first pass 每段約 `800-1200` 中文字。
   - 每列請包含：`group`, `segment`, `output_prefix`, `text`, `notes`。
   - 請用穩定檔名前綴，方便單段重生，不要一次產生 80 分鐘音檔。

3. `cde-2026-breezyvoice-pronunciation-notes.md`
   - 請列出建議保留英文的技術名詞、建議唸法、必要時的注音提示。
   - 只有真的容易誤讀的詞再加注音，不要過度標註。

## 合併順序

請用這個順序整理全場逐字稿：

1. Opening / session positioning：說明本場 CDE 課程定位，以及和前兩場不同。
2. Jason 前半段：醫院場域、patient safety、FDA / TFDA lifecycle logic。
3. Jason 中段：attack surface、testing vocabulary、finding anatomy、threat modeling。
4. Handoff：用一小段自然橋接，把外部測試與 threat model 接到 white-box / system review。
5. 靖中後半段：以 `cde-2026-jingzhong-section-clean.txt` 為基底，對齊 PPT 和 timed source。
6. Shared close：用 lifecycle trust、evidence chain、三個 pre/post-test questions 做收尾。

## 節奏設計原則

請先閱讀最終版本 PPT，再設計逐字稿節奏。不要只照文字檔順序機械合併。

每一頁投影片應該先判斷它的工作：

- 如果是 transition slide：講短、講清楚，重點是換段。
- 如果是 concept slide：用一個核心句 + 一個解釋段落。
- 如果是 case slide：先交代 incident path，再說臨床/治理意義，最後收斂成一句 takeaway。
- 如果是 evidence / workflow slide：用流程語言朗讀，不要像念表格。
- 如果是 final close：放慢節奏，讓 lifecycle trust、evidence chain、pre/post-test anchors 清楚留下來。

逐字稿可以依 PPT 做必要調整：

- PPT 有頁面但文字稿沒有自然銜接時，請補 bridge。
- 文字稿內容比該頁投影片承載量大時，請拆成較短的 TTS 段落。
- 文字稿和 PPT 順序不一致時，請以 PPT 順序為準，並在 notes 標記調整原因。
- 技術密度高的頁面請增加停頓與短句，不要讓 TTS 一口氣念完整段。

## 語氣與風格

請使用台灣華語口語授課風格。句子不要太長，適合 TTS 自然停頓。可以保留常見英文技術詞：

`White-box Testing`, `black-box testing`, `penetration testing`, `SBOM`, `K8S`, `DICOM`, `HL7`, `FHIR`, `PACS`, `HIS`, `EMR`, `FDA`, `TFDA`, `524B`, `Log4Shell`, `MOVEit`, `CrowdStrike`, `Change Healthcare`

講稿應該聽起來像一位有醫療資安實務經驗的人，在幫跨領域聽眾建立判斷框架。

請避免：

- 銷售語氣；
- dramatic cyber threat voice；
- exploit cookbook；
- 過多法條朗讀；
- 把 bullet points 直接逐條唸出；
- 把 slide number / Markdown heading / 表格欄位唸出；
- 加入私人醫院、客戶、學生、credential、專利或 exploit-ready 細節。

## BreezyVoice 生成建議

請以「可分段檢查、可重生單段」為原則設計 batch。

建議先做 pilot：

1. 一段簡單說明段落。
2. 一段含英文技術詞的段落。
3. 一段案例密集段落。

聽完 pilot 後，再決定是否需要注音提示、斷句、標點或英文詞替換。

請不要直接輸出一個超長文字欄位給模型。請幫我把它整理成適合逐段生成、逐段校正、逐段重生的形式。

## 最終交付判準

完成時請確認：

- 全文是一份可聽的上課逐字稿，不是資料拼貼。
- Jason 與靖中段落語氣一致，但仍保留自然 handoff。
- 靖中的原稿重點被保留。
- PPT 與講稿順序能對齊。
- 所有批次片段都有穩定輸出檔名前綴。
- 專有名詞有 pronunciation notes。
- 任何 model input 都不包含不該被唸出來的 metadata。
