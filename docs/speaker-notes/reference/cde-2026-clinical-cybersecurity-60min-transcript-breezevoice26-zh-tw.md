# CDE 2026 臨床端醫材 / 資訊系統資安要求 60 分鐘逐字稿

Source deck:
`/home/jnln3799/Downloads/documents/Clinical-Cybersecurity-Requirements-for-Medical-Devices-and-Healthcare-Information-Systems-TRIMMED-PRIORITY-2025-2026-TAIWAN-NEWS-CASES-20260526-v4.pptx`

Reference markup pattern:
`/home/jnln3799/Downloads/mohw_medical_cybersecurity_breezyvoice_26_50_min_script.md`

Purpose: convert the trimmed CDE deck into a `60` minute Taiwan Mandarin
speech script for later `BreezeVoice 26` / `BreezyVoice` TTS production.

Style boundary: this is an original script. It uses high-level traits such as
Taiwanese conversational Mandarin, dry observational humor, clear contrast,
short rhetorical turns, and a calm but sharp public-speaking rhythm. It does
not imitate any named comedian's exact wording, persona, cadence, catchphrases,
or protected performance style.

Tone policy: spoken transcript sections use affirmative, positive-scope
language. The delivery leads with capability, evidence, governance, scope
control, and next implication, so the talk sounds confident, generous, and
clinically useful.

## A. BreezyVoice 26 / BreezeVoice 26 語音工程設定

> 注意：以下 `[BV26 ...]` 與 `[PAUSE=...]` 是 **Orchestrator Markup**，
> 不是假設 BreezyVoice 26 原生支援所有參數。正確流程是由你的程式先讀取
> 標籤，再轉成切段、reference audio、停頓、語速、注音發音控制與後處理。
> 真正送進 TTS 的文字應該去除控制標籤，避免模型把標籤念出來。

```yaml
voice_engine: BreezyVoice_26_or_BreezyVoice_Taigi_TTS
language_primary: zh-TW
script: Traditional_Chinese
accent: Taiwan_Mandarin
target_duration_minutes: 60
optional_language: Taigi

speaker_reference:
  file: adult_tw_mandarin_calm_medical_cybersecurity_30s.wav
  consent_required: true
  duration_target_sec: 25-45
  recording_style: calm_professional_medical_briefing
  mic_quality: clean_close_mic_no_noise
  avoid:
    - celebrity_voice
    - named_comedian_voice
    - family_member_without_consent
    - dramatic_podcast_voice
    - streamer_voice

global_voice_profile:
  role: clinical_medical_cybersecurity_public_speaker
  perceived_age: 32-45
  gender: neutral_or_mature_professional
  warmth: 0.56
  authority: 0.70
  humor_dryness: 0.34
  emotional_intensity: 0.26
  average_speed_cpm: 175
  max_speed_cpm: 220
  min_speed_cpm: 130
  pitch_shift_semitone: 0
  volume_lufs: -16
  noise_reduction: mild
  post_pause_trim: false

pronunciation_control:
  bopomofo_enabled: true
  english_acronym_mode: letter_by_letter_when_clinical
  mixed_language_style: taiwan_professional
  terms:
    AI: "A-I"
    ASR: "A-S-R"
    TTS: "T-T-S"
    FDA: "F-D-A"
    TFDA: "T-F-D-A"
    CDE: "C-D-E"
    NYCU: "N-Y-C-U"
    SaMD: "Software as a Medical Device；軟體醫材"
    SBOM: "S-B-O-M；軟體物料清單"
    PACS: "P-A-C-S；影像儲傳系統"
    HIS: "H-I-S；醫院資訊系統"
    EMR: "E-M-R；電子病歷"
    EHR: "E-H-R；電子病歷"
    CVD: "Coordinated Vulnerability Disclosure；協調式漏洞揭露"
    VPN: "V-P-N"
    510k: "五一零 K"
    CrazyHunter: "Crazy Hunter 勒索軟體"
    Change_Healthcare: "Change Healthcare；美國醫療支付服務商"

segment_presets:
  OPENING:
    speed_cpm: 162
    warmth: 0.60
    authority: 0.64
    pause_sentence_ms: 560
    pause_after_joke_ms: 850
  DRY_JOKE:
    speed_cpm: 178
    warmth: 0.50
    authority: 0.54
    pause_before_punchline_ms: 550
    pause_after_punchline_ms: 900
  CASE_STORY:
    speed_cpm: 150
    warmth: 0.62
    authority: 0.62
    pause_sentence_ms: 650
  TECH_EXPLAIN:
    speed_cpm: 176
    warmth: 0.50
    authority: 0.73
    pause_sentence_ms: 450
  SAFETY_SLOW:
    speed_cpm: 138
    warmth: 0.54
    authority: 0.82
    pause_sentence_ms: 780
  TRANSITION:
    speed_cpm: 170
    warmth: 0.52
    authority: 0.66
    pause_sentence_ms: 520
  CONCLUSION:
    speed_cpm: 142
    warmth: 0.64
    authority: 0.78
    pause_sentence_ms: 820
```

### 標籤格式

```text
[BV26 preset=OPENING speed=162 pause_after=700ms]
文字內容
[/BV26]
```

常用停頓與語氣標籤：

```text
[PAUSE=300ms] 小停頓
[PAUSE=700ms] 讓觀眾吸收
[PAUSE=1100ms] punchline 後或重大風險句後
[EMPH] 關鍵詞加重，但不要吼
[LOWER] 音量略降，製造嚴肅感
[SMILE] 口氣帶笑，不要誇張
```

### 原生能力與 Orchestrator 分工

BreezyVoice / BreezeVoice 相關公開資料強調台灣華語、voice cloning、注音
發音控制與 code-switching。這份稿件採用保守工程設計：

- BreezyVoice 原生可做：台灣華語語音合成、reference voice cloning、
  code-switching、透過注音輔助處理多音字與專有名詞發音。
- Orchestrator 需要負責：讀取 `[BV26 ...]` 標籤、移除標籤、切段、
  套用 reference audio、插入停頓、控制語速、處理注音發音表、音量正規化、
  串接音檔與後製檢查。
- 不要直接把 `preset=...`、`emotion=...`、`pause_after=...` 這類標籤丟進
  TTS 模型，否則模型可能把控制字串念出來。

建議實際生成流程：

1. Split by `BV26_META.segment_id` 或 `[BV26 ...]` block.
2. Strip metadata and keep only clean spoken text.
3. Generate one audio chunk per block or per paragraph.
4. Review pronunciation and timing.
5. Stitch chunks with `250` ms paragraph gaps and `1.2` to `1.8` second section gaps.

## 60-Minute Transcript

<!-- BV26_META
segment_id: S01
source_slides: 1-2
target_duration: "2:30"
speed: 0.88
tone: "warm_formal_opening"
delivery: "calm, welcoming, lightly witty"
pause_after: "1.6s"
pronunciation_hints:
  - "CDE: C D E"
  - "TFDA: T F D A"
  - "SaMD: software as a medical device；可補中文 軟體醫材"
-->

### S01 Opening - 今天從臨床信任開始

[BV26 preset=OPENING speed=162 pause_after=700ms]
各位先進、各位老師、各位產業界的朋友，大家好。今天這一場，我們要談的是臨床端對醫療器材以及資訊系統的資安要求。
[/BV26]

[BV26 preset=OPENING speed=162 pause_after=700ms]
我先講結論，今天的目標很清楚：把資安轉成臨床現場聽得懂、用得上、可以交接的治理語言。這條路會比背名詞更有價值，也更接近大家每天面對的真實工作。
[/BV26]

[BV26 preset=OPENING speed=162 pause_after=700ms]
今天最重要的事情，是把醫療資安從抽象概念帶回臨床現場。醫院裡的資安會落在很具體的問題上：系統能穩定服務、影像能即時調閱、報告能順利完成、病人照護能依照既定流程持續進行。
[/BV26]

[BV26 preset=OPENING speed=162 pause_after=700ms]
所以這場演講的題目雖然叫做醫療器材和醫療資訊系統的資安要求，我希望大家聽完之後，腦中留下的是一條清楚的線：風險如何被看見，控制如何被設計，測試如何形成證據，修補如何完成，最後證據如何被保存。
[/BV26]

[BV26 preset=OPENING speed=162 pause_after=700ms]
今天我們會從臨床環境開始。醫院和一般企業的差異，會直接影響更新、維護、停機和復原決策。接著我們會看幾個近年的資安事件，包含台灣醫院、國際大型醫療系統、醫療供應鏈，以及影像和檢驗服務中斷。這些案例會幫助大家看到：資安事件的真正影響，會從資料與系統一路延伸到臨床流程。
[/BV26]

[BV26 preset=OPENING speed=162 pause_after=700ms]
接著，我們會談 FDA、TFDA、SBOM、滲透測試、白箱檢測、部署證據，以及生命週期治理。這些名詞聽起來很多，但其實都在回答同一個問題：當一個醫療系統進入真實醫院，它憑什麼被信任？
[/BV26]

<!-- BV26_META
segment_id: S02
source_slides: 3-4
target_duration: "3:40"
speed: 0.89
tone: "observational_contrast"
delivery: "clear contrast, dry humor, composed"
pause_after: "1.4s"
pronunciation_hints:
  - "Change Healthcare: Change Healthcare；後面補 美國醫療支付服務商"
  - "ALPHV BlackCat: A L P H V BlackCat；可簡化成 BlackCat 勒索軟體"
-->

### S02 Cybersecurity Is Clinical Continuity

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=600ms]
我們先看第一個觀念：資安已經進入臨床連續性議題。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=600ms]
以前很多人想到資安，第一個畫面是什麼？防火牆、掃毒軟體、密碼複雜度，然後月底或年底做一份合規檢查表。這些東西重要嗎？重要。但如果我們只停在這裡，就會把醫療資安看得太像一般辦公室 IT。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=600ms]
一般辦公室電腦壞掉，最糟可能是今天報表晚一點交，明天仍有機會補上。醫院的資訊系統角色更直接，它就是臨床流程的一部分。掛號、檢驗、影像、電子病歷、醫囑、藥局、手術排程、急診分流，這些系統只要卡住，臨床就開始改用備援流程。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=600ms]
備援流程可以支撐現場，但它通常比較慢、比較吃人力，也需要更清楚的交接。很多時候，我們口中的「系統中斷」，在臨床現場就變成「大家開始用紙本」、「電話打進護理站」、「影像排隊等待」、「病人重新安排」。所以資安事件會直接進到護理站、檢查室、急診、放射科，甚至病人和家屬的等待時間裡面。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=600ms]
這裡有一個近年的案例。二零二四年，美國 Change Healthcare 遭到 ALPHV BlackCat 勒索軟體攻擊。Change Healthcare 是美國醫療支付和理賠處理非常重要的服務商。事件發生後，醫療理賠、藥局付款、醫療服務收款、甚至部分照護流程都受到影響。美國 CISA、FBI 和 HHS 都有針對這個事件發布聯合通報。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=600ms]
這個案例告訴我們一件事：醫療資安要放在互相依賴的生態系裡理解。醫院、藥局、保險、支付、醫療器材、雲端服務、外包供應商，全部接在一起。任何一個重要節點失效，都可能讓整個臨床和營運流程開始承受壓力。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=600ms]
所以今天我們會用更臨床、更現實的方式定義安全：當某個節點失效時，病人照護如何繼續？當供應商被攻擊時，醫院如何啟動替代路徑？當資料流中斷時，臨床團隊如何接上下一步？
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=600ms]
這些問題一旦回答清楚，資安就會從 IT 任務升級成臨床連續性的治理能力。
[/BV26]

<!-- BV26_META
segment_id: S03
source_slides: 5-6
target_duration: "3:40"
speed: 0.88
tone: "clinical_urgency_without_panic"
delivery: "serious, controlled, grounded"
pause_after: "1.4s"
pronunciation_hints:
  - "PACS: 影像儲傳系統；第一次補 P A C S"
  - "Chansn Hospital: 長生醫院"
-->

### S03 Cyber Incidents Can Become Clinical Incidents

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
第二個重點：資安事件會變成臨床事件。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
我們常常講勒索軟體，講到最後好像主角是加密。檔案被加密，系統被鎖住，螢幕上跳出勒索訊息。這些都是真的；在醫院裡面，真正的重點會落在流程開始停下來。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
想像一下，攻擊者透過醫院影像系統製造中斷。PACS 進入離線或降級狀態，影像即時調閱受到影響，醫師調閱舊片的速度下降，新的檢查排程被延後，報告流程變慢。這時候最直接的影響會落在臨床判斷速度。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
在一般門診，影響可能是病人改期、報告延後。在急診場景，事情更敏感。中風、創傷、手術前評估，很多判斷都依賴影像和資料。當系統進入離線或服務中斷狀態，醫療團隊需要啟動備援流程，以穩健、可追蹤的方式維持照護。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
這也是資安需要同時看資料保護與系統可用性的原因。資料外洩當然嚴重；在醫療場域，系統服務中斷同樣會直接影響照護。Confidentiality、Integrity、Availability，機密性、完整性、可用性，這三個字在教科書上看起來很平等，在醫院裡，可用性常常會直接碰到病人安全。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
台灣二零二五年也有相關案例。長生醫院遭遇勒索軟體攻擊，新聞報導指出可能有超過八萬筆病歷資料受到影響。這件事情同時是個資新聞與臨床營運提醒：各種規模的醫療院所，只要有臨床資料、有資訊系統、有網路連線，就會進入攻擊者的目標清單。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
我們要從這個事件學到的是應變能力：當醫院被攻擊時，資料備份在哪裡？分區隔離如何啟動？資安事件如何通報？演練紀錄如何支援現場？哪些系統需要優先恢復？這些答案越早建立，事件中的判斷就越穩。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
所以，當我們在設計醫療器材或醫療資訊系統時，請優先問更完整的問題：當它被放進醫院之後，它在高壓情境下如何失效？它如何保護其他系統？它如何被隔離？它如何被恢復？它如何留下足夠證據，讓醫院知道發生什麼事？
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
這就是醫療資安的獨特位置：它保護一台機器，也保護一段照護流程。
[/BV26]

<!-- BV26_META
segment_id: S04
source_slides: 7-8
target_duration: "3:15"
speed: 0.89
tone: "systems_thinking"
delivery: "diagram-like explanation, conversational"
pause_after: "1.2s"
pronunciation_hints:
  - "NYC Health + Hospitals: N Y C Health and Hospitals"
-->

### S04 Hospital as a System of Systems

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=550ms]
第三個觀念：醫院是一組互相牽動的系統。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=550ms]
我們平常說「醫院資訊系統」，聽起來好像是一個很大的東西，按一個開關就開，按一個開關就關。真實世界更像一張互相連動的地圖。醫院裡面有 HIS、EMR、PACS、LIS、藥局系統、手術排程、叫號系統、門禁、網路設備、檢驗儀器、影像設備、AI 軟體醫材、雲端服務、供應商維護通道。這些東西有些很新，有些很舊，有些是院內自己管，有些是廠商管，有些介面寫得很漂亮，有些介面則是歷史留下來的。你看著它，心裡會浮現一句話：這就是醫院版的考古現場。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=550ms]
我們要尊重這個現實。醫院系統是長生命週期、高驗證成本、強臨床依賴的基礎設施。很多設備很貴、壽命很長、驗證成本很高，而且還要配合臨床流程。只要某個系統連著另一個系統，它就可能成為風險路徑。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=550ms]
二零二六年，NYC Health and Hospitals 披露一起大型資料外洩事件，報導指出至少一百八十萬人受到影響，資料包含醫療資料甚至指紋。這個案例提醒我們，醫療機構裡的資料具有高度敏感性。它可能包含病史、檢查、身分識別、生物特徵，甚至和多個系統串接後形成更完整的個人輪廓。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=550ms]
所以當我們看醫院資安，要沿著資料流動來看。病人從掛號開始，資料進入 HIS；檢查資料進入 LIS；影像進入 PACS；醫師在 EMR 裡判讀；AI 系統可能讀取影像或文字；結果再回到臨床工作站。每一次傳輸，每一個 API，每一個帳號權限，每一個廠商維護通道，都是信任邊界。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=550ms]
資安的核心是讓連線、資料交換與即時性在可治理的邊界內運作。醫院需要連線，需要資料交換，需要即時性。真正的問題是：哪些地方正在被信任？這些信任如何被驗證？如果其中一個點失效，影響如何被限制？
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=550ms]
如果一個醫療產品只在自己的實驗室裡看起來很安全，下一步就是證明它能在醫院現場維持安全。它要在醫院這種系統中的系統裡仍然安全，才算真的有臨床部署能力。
[/BV26]

<!-- BV26_META
segment_id: S05
source_slides: 9-10
target_duration: "3:40"
speed: 0.88
tone: "practical_governance"
delivery: "firm, explanatory, lightly ironic"
pause_after: "1.3s"
pronunciation_hints:
  - "CrazyHunter: Crazy Hunter 勒索軟體"
  - "Mackay Memorial Hospital: 馬偕醫院"
-->

### S05 Patch Lifecycle in Hospitals

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=650ms]
接下來這一頁很重要，因為它處理醫療資安裡最常見的治理問題：醫院如何安全地完成 patch？
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=650ms]
在一般 IT 環境，如果發現漏洞，大家直覺會說：更新啊，下一步很清楚。到了醫院，事情會變得比較像一部很長的連續劇，而且每一集都會提醒大家：這個系統正在支撐臨床服務。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=650ms]
第一個原因是臨床連續性。很多設備正在服務病人，更新需要配合照護節奏。第二個是廠商驗證。醫療器材常常牽涉原廠支援、版本相容性、法規文件，有些更新需要醫院和廠商共同完成。第三個是系統相容性。HIS、PACS、檢驗系統、影像設備，只要一個元件更新，其他介面可能跟著出問題。第四個是停機窗口。你要找一個影響最小的時間更新，這句話在醫院裡常常約等於找一個大家都很從容的急診。理論上存在，實務上需要高度協調。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=650ms]
所以，patch 在醫院是一個治理流程。要有人判斷風險，要有人確認臨床影響，要有人跟廠商協調，要有人安排停機，要有人測試更新後系統正常，要有人留下紀錄。這些事情事先設計好，漏洞來的時候就能進入既定流程。既定流程會讓修補更穩，讓臨床團隊更有把握。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=650ms]
台灣二零二五年馬偕醫院遭到 CrazyHunter 勒索軟體攻擊，新聞報導指出超過五百台電腦受到影響，醫院啟動緊急應變。這個事件對我們的啟示是，資安事件進入現場時，SOP 會立刻接受實務檢驗。它會直接問你：哪些系統要先恢復？哪些電腦可以隔離？哪些流程要改紙本？哪些資料要確認完整性？哪些對外窗口要通報？
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=650ms]
所以在醫療器材或醫療資訊系統設計階段，我們就應該把 patch lifecycle 想清楚。漏洞怎麼接收？誰評估？誰修？修完怎麼測？醫院怎麼部署？部署失敗怎麼 rollback？臨床端怎麼知道風險已被處理？
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=650ms]
這些聽起來很細，但比起事件發生後才補，成本低很多。資安最有價值的地方，通常是用流程把人力和混亂轉成可預期的行動。
[/BV26]

<!-- BV26_META
segment_id: S06
source_slides: 11-12
target_duration: "3:25"
speed: 0.89
tone: "trust_boundary"
delivery: "controlled, slightly skeptical"
pause_after: "1.2s"
pronunciation_hints:
  - "VPN: V P N"
  - "OneBlood: One Blood"
-->

### S06 Vendor Access Is Also an Attack Surface

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
下一個很容易被低估的風險，是廠商遠端維護。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
醫療環境裡面，廠商遠端維護很常見，也很合理。設備需要更新，系統需要排障，臨床端需要快速支援。於是我們有 VPN、有遠端桌面、有維護帳號、有供應商支援流程。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
從資安角度看，這些便利功能同時也是信任邊界。當你允許廠商從外部進到醫院網路，某種程度上，你就是讓一台由外部管理的設備，接近非常敏感的臨床環境。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
這裡面有幾個常見治理問題。第一，維護帳號如何分派？第二，多因素驗證如何啟用？第三，連線如何收斂到必要系統？第四，時間限制如何設定？第五，紀錄如何保存？第六，廠商端設備如何維持保護？這些問題回答清楚，遠端維護就能從便利通道升級成受控通道。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
我們看一個案例。二零二四年 OneBlood 遭到勒索軟體攻擊，這是一個血液供應機構。事件造成血液供應作業受影響，醫院被迫保守使用血液，部分手術也受到調整。這個案例很適合提醒我們，醫療照護依賴很多外部供應鏈和支援服務。當供應鏈被攻擊，醫院即使維持內部系統完整，仍然會感受到臨床壓力。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
所以我們在談 vendor access 的時候，重點是把廠商連線治理化。每一個維護通道都要回答：誰能進來？從哪裡進來？可以碰什麼？什麼時候可以進來？做了什麼？出事時怎麼停掉？
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
當這些問題都有答案，遠端維護就是受控的服務；答案越完整，信任邊界越清楚。
[/BV26]

<!-- BV26_META
segment_id: S07
source_slides: 13-14
target_duration: "3:45"
speed: 0.88
tone: "regulatory_logic"
delivery: "plain-language translation of regulation"
pause_after: "1.4s"
pronunciation_hints:
  - "FDA: F D A"
  - "TFDA: T F D A"
  - "Stryker: Stryker"
-->

### S07 Why FDA Cybersecurity Requirements Expanded

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=650ms]
接著我們談法規，目標是理解它背後的產品治理邏輯。今天會把 FDA guidance 轉成營運語言，讓大家看見它如何支援產品安全、臨床部署與上市後維護。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=650ms]
FDA 近年把醫療器材資安要求拉高，原因其實很直覺：醫療器材已經從孤立硬體走向連網臨床系統。以前很多設備像一座小島，功能固定、連線少、更新少。現在醫療器材會連醫院網路，會跟雲端交換資料，會接 PACS、HIS、EMR，會做遠端更新，會包含 AI 模型，會有第三方套件，甚至會依賴作業系統、container、API 和網路服務。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=650ms]
換句話說，醫療器材越來越像一台被放在臨床流程裡的電腦。既然它像電腦，它就會有電腦世界的風險：漏洞、更新、身分驗證、權限控管、供應鏈、遠端存取、日誌、復原。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=650ms]
所以 FDA 的要求反映產品現實。當產品變成連網系統，安全會自然進入產品生命週期，從設計、測試、部署一路延伸到上市後維護。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=650ms]
二零二六年，醫療設備大廠 Stryker 發生網路攻擊，報導指出其全球網路受到干擾。這類事件的重點在於醫療供應鏈本身也會成為資安風險。醫療器材公司、軟體供應商、雲端服務、維護廠商，一旦遭遇攻擊，下游醫院和臨床部署都可能受影響。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=650ms]
因此，當 FDA 要求 secure updates、vulnerability disclosure、SBOM、postmarket support，它是在建立製造商的可驗證能力：知道產品裡有什麼；知道漏洞來了誰負責；知道怎麼安全更新；知道上市後怎麼繼續維護。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=650ms]
這就是我們今天要把法規翻譯成營運語言的原因。法規連接產品、證據、責任與持續維護。它要的是可被查核的責任鏈。
[/BV26]

<!-- BV26_META
segment_id: S08
source_slides: 15-16
target_duration: "3:15"
speed: 0.89
tone: "ownership_focus"
delivery: "simple, memorable, slightly humorous"
pause_after: "1.2s"
pronunciation_hints:
  - "SBOM: 第一次念 軟體物料清單；補一句 S B O M"
  - "Medibank: Medibank"
-->

### S08 SBOM Is a Map of Responsibility

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
接下來是 SBOM。SBOM 中文常翻成軟體物料清單。這個翻譯很準，但聽起來有一點像倉庫管理。其實很貼切，因為它真的像在問：你這個產品裡到底用了哪些東西？
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
當我們把 SBOM 當成責任地圖，它的價值會大幅提升。真正重要的是：每個元件出問題時，誰要負責。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
一個醫療軟體可能包含作業系統、runtime、framework、資料庫、影像處理套件、AI 模型依賴、第三方 library、container base image。這些東西大部分來自外部生態系。只要其中一個元件有漏洞，它就可能變成你產品的風險。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
所以 SBOM 的核心價值在於責任地圖。當某個套件爆出漏洞，你要能回答：我們是否使用？在哪個版本？影響哪個產品？誰要評估？誰要修？修補需要多久？醫院需要被通知嗎？修補需要時間時，補償控制如何啟動？
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
二零二二年澳洲 Medibank 發生重大資料外洩事件，攻擊者利用竊取的憑證進入系統，造成大量健康保險客戶敏感資料外洩。這個案例提醒我們一件事：資安很多時候是責任鏈的連續性問題。憑證、系統、資料、供應商、監控、反應，每一段都有 owner，攻擊就會遇到更多阻力。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
所以我們在醫療器材資安裡談 SBOM，是為了上市審查，也為了讓產品上市後能被維護。SBOM 讓團隊知道自己擁有哪些元件，owner 讓每個元件有負責人，更新流程讓負責人能把風險轉成行動。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
好的 SBOM 應該能把焦慮變成行動：哪個元件、哪個版本、哪個漏洞、哪個風險、哪個 owner、哪個時程、哪個證據。
[/BV26]

<!-- BV26_META
segment_id: S09
source_slides: 17-18
target_duration: "3:45"
speed: 0.88
tone: "evidence_chain"
delivery: "measured, persuasive"
pause_after: "1.3s"
pronunciation_hints:
  - "Ardent Health Services: Ardent Health Services"
  - "CVD: coordinated vulnerability disclosure；中文可念 協調式漏洞揭露"
-->

### S09 Trust Requires Evidence

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
這一頁是整場演講的核心之一：信任需要證據。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
在資安領域，最需要被補強的一句話可能是「我們都有做」。這句話非常萬用。你問 threat model 做到哪裡？測試證據在哪裡？漏洞修補如何追蹤？團隊只要把回答轉成文件、紀錄、測試結果和修補證據，信任就會開始成立。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
醫療場域特別重視可追溯證據。醫院要知道：你怎麼設計安全？怎麼測？測出什麼？怎麼修？修完怎麼驗？剩下的風險誰接受？這些都要變成可追溯的 evidence chain。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
我們可以把證據分成幾類。第一是設計證據，例如 threat model、架構審查、資安需求。第二是測試證據，例如滲透測試、弱點掃描、fuzz testing、白箱審查。第三是部署證據，例如設定紀錄、帳號權限、網路區隔。第四是修補和重測證據，例如 change log、retest result、漏洞揭露紀錄。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
這些東西串起來，才會形成可信任的生命週期。團隊可以拿出證據說明安全如何被設計、驗證、修補，以及剩下的風險如何被管理。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
二零二三年 Ardent Health Services 遭到勒索軟體攻擊，網路系統被迫下線，部分可延後手術暫停，後續分階段恢復。這類事件的核心工作，是重新啟動系統，同時確認哪些系統可信、哪些資料完整、哪些流程已恢復、哪些風險仍存在。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
所以證據是事件發生後讓組織恢復判斷力的工具。完整證據能讓團隊靠紀錄、測試結果與決策脈絡行動。這在平常很有價值，在醫療事件裡更關鍵。
[/BV26]

[BV26 preset=SAFETY_SLOW speed=140 pause_after=850ms]
因此，一個好的醫療資安流程，從一開始就要設計證據。每一個 finding 都應該帶著資產、證據、攻擊路徑、臨床影響、owner、修補、重測、殘餘風險。這樣安全會成為可以被追蹤、被討論、被改善的工作。
[/BV26]

<!-- BV26_META
segment_id: S10
source_slides: 19-20
target_duration: "3:25"
speed: 0.89
tone: "attack_path_governance"
delivery: "clear, governance-focused scenario"
pause_after: "1.2s"
pronunciation_hints:
  - "Foxconn: 鴻海；可補 Foxconn"
  - "Nitrogen: Nitrogen 勒索軟體"
-->

### S10 Vendor Maintenance Attack Path

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
我們現在把前面的概念放到一個攻擊路徑裡。這個路徑叫做 vendor maintenance access，也就是廠商維護通道。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
很多醫療設備需要廠商維護，所以會有 VPN、維護帳號、遠端連線。從營運角度，這是必要功能。從攻擊者角度，這是一條很有價值的路。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
假設攻擊者先拿到廠商端的帳號，或者攻擊廠商筆電，再利用維護通道進入醫院網路。如果維護帳號權限太高、多因素驗證需要啟用、連線範圍太大、日誌監控需要到位，那攻擊者就可能從維護通道碰到醫療設備子網段，甚至進一步橫向移動。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
這裡我要特別提醒，今天聚焦治理問題：一個被信任的維護路徑，如何證明它值得被信任？
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
二零二六年，鴻海也就是 Foxconn 的北美相關設施，被 Nitrogen 勒索軟體組織聲稱攻擊，新聞關注供應鏈與資料風險。這個事件很適合拿來提醒醫療產業：供應鏈廠商本身也是攻擊面。當一個重要供應商被攻擊，下游客戶需要快速掌握自己的風險位置。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
醫療器材公司也是一樣。你要保護產品本身，也要保護維護流程。你的工程師怎麼連進客戶環境？連線如何審批？MFA 如何啟用？最小權限如何落實？session recording 如何保存？快速停權如何執行？如果廠商端被入侵，醫院端如何切斷連線？
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
我們常說信任，但在資安裡，信任會落成一組控制。控制讓信任可以被驗證、被追蹤、被交接。希望是一個很好的生活態度；資安架構則把希望轉成可執行的控制。
[/BV26]

<!-- BV26_META
segment_id: S11
source_slides: 21-22
target_duration: "3:35"
speed: 0.88
tone: "clinical_workflow_focus"
delivery: "serious, concrete"
pause_after: "1.2s"
pronunciation_hints:
  - "Synnovis: Synnovis"
  - "Qilin: Qilin 勒索軟體"
  - "NHS: N H S"
-->

### S11 Imaging Systems Are High-Value Targets

[BV26 preset=CASE_STORY speed=150 pause_after=700ms]
接下來看影像系統。影像系統為什麼是高價值目標？因為它同時是資料倉庫，也是臨床決策流程的一部分。
[/BV26]

[BV26 preset=CASE_STORY speed=150 pause_after=700ms]
PACS、影像工作站、modalities、報告系統、影像瀏覽器，這些東西在放射科、急診、手術前評估裡面非常重要。影像要被讀取、被比較、被判讀、被寫進報告、被用來做治療決策。
[/BV26]

[BV26 preset=CASE_STORY speed=150 pause_after=700ms]
所以影像系統的風險至少有三層。第一是可用性，系統進入中斷或降級狀態，檢查和判讀就延遲。第二是完整性，影像或報告如果被竄改，臨床判斷可能被影響。第三是機密性，影像本身也可能包含可辨識的病人資訊。
[/BV26]

[BV26 preset=CASE_STORY speed=150 pause_after=700ms]
二零二四年，英國 Synnovis 遭到 Qilin 勒索軟體攻擊，影響倫敦 NHS 的病理和輸血服務，造成手術取消和檢驗服務中斷。這個案例非常清楚地展示醫療輔助服務中斷的後果。檢驗、影像、血液、病理，這些看起來像背景系統，但臨床其實每天都在依賴它們。
[/BV26]

[BV26 preset=CASE_STORY speed=150 pause_after=700ms]
如果這些系統中斷，醫院會同步啟動臨床、護理、行政與資訊的備援協作。醫師要改判斷流程，護理師要重新安排病人，行政要通知改期，病人要等待。備援流程的效率需要靠事前設計來支撐。
[/BV26]

[BV26 preset=CASE_STORY speed=150 pause_after=700ms]
因此，當我們設計或審查影像相關系統時，要從顯示影像延伸到治理問題：它的網路邊界在哪裡？誰可以上傳？誰可以讀取？DICOM 或 API 介面怎麼驗證？PACS 進入中斷狀態時，替代讀片流程如何啟動？資料延遲時，臨床端如何收到提示？
[/BV26]

[BV26 preset=CASE_STORY speed=150 pause_after=700ms]
攻擊者只要讓關鍵流程停下來，就足以造成壓力。這就是醫療資安的現實：真正承受壓力的常常是一段臨床依賴。
[/BV26]

<!-- BV26_META
segment_id: S12
source_slides: 23-24
target_duration: "3:45"
speed: 0.88
tone: "method_clarity"
delivery: "teacherly, crisp"
pause_after: "1.3s"
pronunciation_hints:
  - "Proofpoint: Proofpoint"
  - "Tom's Hardware: Tom's Hardware"
-->

### S12 Different Testing Methods Prove Different Things

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=550ms]
現在我們來談測試。這一頁很適合拿來建立一個清楚觀念：各類資安測試會證明各自擅長的事情。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=550ms]
弱點掃描、黑箱測試、滲透測試、白箱審查，這些名詞常常被混在一起。結果就是，會議上有人說「我們有掃過了」，另外一個人以為「那就代表安全了」。這中間差很多。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=550ms]
掃描比較像是用已知規則檢查已知問題。它可以找到已知漏洞、錯誤設定、開放服務。它的價值在於快速建立已知風險清單；攻擊路徑、利用性和臨床影響，則需要由其他測試方式補上。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=550ms]
黑箱測試是從外部行為看系統，測試者掌握的是外部可觀察介面。它可以看到外部可達的攻擊面，並把後續 root cause 分析交給白箱審查銜接。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=550ms]
滲透測試更接近攻擊者視角，重點是驗證可被利用的攻擊鏈和實際影響。它在特定範圍和時間內，幫助團隊確認哪些路徑可行、哪些控制有效、哪些風險需要修補。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=550ms]
白箱審查則是往內看。看原始碼、設定、架構、相依套件、權限設計、日誌、部署。它同時回答「外部攻擊路徑如何形成」，以及「風險源頭在哪裡、要從哪裡修」。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=550ms]
二零二五年，台灣半導體供應鏈相關組織遭遇 email-based intrusion 和資安間諜活動的報導。這個案例提醒我們，真實攻擊往往會把社交工程、身分、供應鏈、內部信任、資料存取一路串起來。多種測試方法搭配，才能看見完整風險。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=550ms]
所以對醫療器材來說，安全來自多種測試共同回答完整問題。掃描回答已知問題在哪裡；黑箱回答外部可見攻擊面；滲透測試回答攻擊鏈和影響；白箱審查回答 root cause 和可修補性；部署審查回答進入醫院後如何維持安全。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=176 pause_after=550ms]
這樣組合起來，才比較像真正的 assurance model。
[/BV26]

<!-- BV26_META
segment_id: S13
source_slides: 25-26
target_duration: "4:00"
speed: 0.87
tone: "finding_quality"
delivery: "structured, checklist but human"
pause_after: "1.4s"
pronunciation_hints:
  - "Signature Healthcare: Signature Healthcare"
  - "EHR: 電子病歷；必要時補 E H R"
-->

### S13 A Useful Finding Drives Remediation

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
接下來我們談 finding。好的資安報告會讓 finding 直接推動修補。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
一個成熟度較低的 finding 可能只寫：「系統存在高風險漏洞，建議改善。」這句話提供了方向，但行動性有限。就像醫生跟病人說：「你身體有狀況，建議健康。」病人聽完也只能說，謝謝，這個我大概也知道。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
一個有用的 finding，至少要包含八個元素。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
第一，Asset。受影響的是哪個系統、哪個設備、哪個元件。第二，Evidence。你怎麼證明這個問題存在。第三，Path。攻擊或錯誤使用的路徑是什麼。第四，Impact。它對臨床、營運、病人安全可能造成什麼影響。第五，Owner。誰負責修。第六，Fix。怎麼修。第七，Retest。修完怎麼驗證。第八，Residual Risk。剩下的風險是否接受，為什麼。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
這八個元素的目的，是讓報告能行動。醫院和廠商最需要的是可以分派工作的報告。最後大家把 finding 放進 Excel，顏色改成紅色，再靠 owner、due date、fix、retest 一步一步把它變綠。Excel 本身很努力，真正讓它變綠的是治理流程。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
二零二六年 Signature Healthcare 發生資安事件，Brockton Hospital 在電子病歷系統服務中斷時維持 downtime procedures 和紙本流程。這個案例提醒我們，finding 的價值包含預防事件，也包含事件發生後協助恢復。你要知道哪些資產受影響、哪些系統可信、哪些流程要備援、哪些證據能支持恢復決策。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
所以，在醫療資安裡，我們應該把 finding 當成治理物件。每一個 finding 都應該能進入 workflow：分派 owner、設定時程、追蹤修補、做 retest、紀錄殘餘風險。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
finding 進入修補流程時，它就從資訊升級成治理。
[/BV26]

<!-- BV26_META
segment_id: S14
source_slides: 27-28
target_duration: "3:50"
speed: 0.88
tone: "outside_in_vs_inside_out"
delivery: "analytical, clear baton pass to white-box"
pause_after: "1.3s"
pronunciation_hints:
  - "Lurie Children's Hospital: Lurie Children's Hospital"
-->

### S14 Outside-In Testing Opens the Next Evidence Layer

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
這裡我們進到白箱審查。前面講滲透測試，可能有人會問：如果滲透測試已經可以模擬攻擊者，那為什麼還需要白箱？
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
答案是，滲透測試告訴你「攻擊者可以走到哪裡」。白箱審查告訴你「根本原因在哪裡，以及要怎麼從根本修掉」。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
外部測試很重要，因為它貼近攻擊者視角。它可以驗證 exploitability，驗證攻擊路徑，讓大家知道風險具有現實性。外部測試看到的是結果；白箱審查往內看，可以找到內部架構、權限檢查、設定檔、相依套件與部署設計裡的根本原因。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
白箱審查則是往內部看。看 source code、config、dependency、authentication、authorization、input validation、logging、deployment default。它可以找出 root cause，也可以讓修補比較精準。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
二零二四年 Lurie Children's Hospital 遭到資安攻擊，系統離線數週，電子病歷存取受限。這樣的事件提醒我們，醫療系統需要外部邊界與內部設計一起站穩。身份驗證、權限、日誌、備援、部署設定，每一層都會影響事件發生時的衝擊大小。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
所以，白箱和滲透測試是接力關係。外部測試告訴你攻擊鏈是否可行，白箱告訴你這條鏈為什麼存在。外部測試幫你看到門如何被打開，白箱幫你看到門鎖如何被修正。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=174 pause_after=600ms]
對醫療器材和醫療資訊系統來說，這個差異很重要。因為最終我們要交付的是可維護、可修補、可審查的安全系統。
[/BV26]

<!-- BV26_META
segment_id: S15
source_slides: 29-30
target_duration: "4:00"
speed: 0.87
tone: "deployment_reality"
delivery: "practical, operational, decisive"
pause_after: "1.4s"
pronunciation_hints:
  - "Systex: 精誠資訊；可補 Systex"
-->

### S15 Security Must Survive Deployment

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=650ms]
接下來這句話請大家記得：安全設計要活過部署。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=650ms]
很多產品在設計文件裡都很安全。架構圖很漂亮，控制點很清楚，流程也寫得很完整。進到醫院環境以後，現實會開始問更具體的問題。服務是否收斂到必要範圍？預設帳密如何更新？權限如何最小化？網路放在哪個區段？誰可以遠端維護？日誌送到哪裡？備份誰負責？事件發生誰接手？
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=650ms]
當這些問題都有清楚答案，設計安全就會在部署那一刻延伸成營運安全。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=650ms]
部署安全至少包含幾個面向。第一，secure defaults。產品預設就應該收斂服務範圍、關閉多餘 port、強制強身份驗證。第二，configuration hardening。安全責任要由產品設計、部署文件和現場工程一起承擔。第三，network placement。要說清楚產品應該放在哪個 subnet，允許哪些路徑，限制哪些路徑。第四，credential and key handling。服務帳號、API key、certificate、update-signing key 都要有管理方式。第五，installation evidence。安裝版本、設定、網路規則、權限都要留紀錄。第六，operational handoff。監控、備份、修補、事件應變、重測，誰負責要講清楚。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=650ms]
二零二五年台灣精誠資訊 Systex 通報收到匿名勒索訊息並配合調查。這個案例提醒我們，企業面對勒索或資安威脅時，部署治理和事件應變非常重要。系統如何分區？資料如何備份？權限如何收斂？事件通報和證據保存如何完整？這些能力都適合在平時建立。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=650ms]
對醫療產品來說，部署是工程能力進入臨床現實的交會點。產品在實驗室安全，接著要在醫院安全；產品在 demo 安全，接著要在夜班急診安全；產品在 PowerPoint 安全，接著要在真實網路、真實帳號、真實維護流程裡安全。PowerPoint 很適合溝通，真實部署會負責驗證。
[/BV26]

[BV26 preset=TECH_EXPLAIN speed=172 pause_after=650ms]
真正的安全要在部署環境裡成立。這也是為什麼 FDA-facing evidence 會從設計和測試延伸到部署設定、維護責任、監控與修補流程。
[/BV26]

<!-- BV26_META
segment_id: S16
source_slides: 31-32
target_duration: "4:00"
speed: 0.87
tone: "synthesis_close"
delivery: "confident, constructive, memorable"
pause_after: "1.6s"
pronunciation_hints:
  - "CrazyHunter: Crazy Hunter 勒索軟體"
  - "Changhua Christian Hospital: 彰化基督教醫院"
-->

### S16 From Risk to Lifecycle Trust

[BV26 preset=CONCLUSION speed=142 pause_after=900ms]
最後，我們把今天的內容收回到一張圖：從風險到生命週期信任。
[/BV26]

[BV26 preset=CONCLUSION speed=142 pause_after=900ms]
一個醫療系統要被信任，關鍵在於它能把安全一路做完。第一步是 risk identification，知道哪些資產、流程、資料、介面有風險。第二步是 threat modeling，知道攻擊者可能怎麼走，信任邊界在哪裡。第三步是 security testing，用掃描、黑箱、滲透測試、白箱審查、部署審查去驗證控制。第四步是 vulnerability finding，把問題寫成可行動的 finding。第五步是 remediation and fix，真的修。第六步是 validation and retest，修完要驗。第七步是 compliance evidence，把整個過程留下可追溯證據。最後才是 lifecycle trust，讓產品上市後仍然可以被維護、被更新、被審查、被信任。
[/BV26]

[BV26 preset=CONCLUSION speed=142 pause_after=900ms]
這條鏈裡面任何一段斷掉，資安就會變成口號。
[/BV26]

[BV26 preset=CONCLUSION speed=142 pause_after=900ms]
二零二五年到二零二六年間，台灣 CrazyHunter 勒索軟體攻擊多家醫療院所，包括馬偕、彰化基督教醫院等，引發台灣針對醫院勒索軟體應變 SOP 的討論。這個事件對台灣醫療產業非常重要，因為它把資安議題帶回我們熟悉的醫療環境。它提醒我們，醫療資安已經成為台灣醫療體系共同面對的治理題。
[/BV26]

[BV26 preset=CONCLUSION speed=142 pause_after=900ms]
所以今天如果只帶走一件事，我希望是這個：臨床端的資安要求，是讓醫院能信任這個系統在真實部署、修補、異常與事件交接時仍然可被治理。
[/BV26]

[BV26 preset=CONCLUSION speed=142 pause_after=900ms]
換句話說，安全是一種持續交代責任的能力。
[/BV26]

[BV26 preset=CONCLUSION speed=142 pause_after=900ms]
對醫療器材公司來說，這代表你要知道產品裡有什麼、風險在哪裡、怎麼測、怎麼修、怎麼重測、怎麼跟醫院溝通。對醫院來說，這代表資安報告要能變成行動。對法規和審查來說，這代表證據鏈比口頭保證重要。
[/BV26]

[BV26 preset=CONCLUSION speed=142 pause_after=900ms]
我們今天看到的每一個新聞案例，其實都在講同一件事。Change Healthcare 告訴我們供應鏈會影響醫療營運。長生和馬偕提醒我們台灣醫院也在攻擊範圍內。OneBlood 和 Synnovis 告訴我們支援服務中斷也會影響臨床。Stryker 和 Foxconn 提醒我們供應鏈和設備製造商同樣是風險的一部分。CrazyHunter 則把這一切拉回台灣現場。
[/BV26]

[BV26 preset=CONCLUSION speed=142 pause_after=900ms]
所以，醫療資安真正要做的，是把每個責任都接起來。
[/BV26]

<!-- BV26_META
segment_id: S17
source_slides: "closing bridge"
target_duration: "2:30"
speed: 0.88
tone: "closing_and_handoff"
delivery: "grateful, confident, discussion-ready"
pause_after: "2.0s"
pronunciation_hints:
  - "CDE: C D E"
  - "TFDA: T F D A"
-->

### S17 Closing - 三個帶走的問題

[BV26 preset=CONCLUSION speed=140 pause_after=900ms]
在結束前，我用三個問題幫大家整理。
[/BV26]

[BV26 preset=CONCLUSION speed=140 pause_after=900ms]
第一，這個系統如果今天進入醫院，它依賴哪些臨床流程？如果系統中斷，哪些病人、哪些科別、哪些資料流會受到影響？
[/BV26]

[BV26 preset=CONCLUSION speed=140 pause_after=900ms]
第二，這個系統的安全控制是否有證據？團隊要能拿出 threat model、測試報告、修補紀錄、重測結果、部署設定、殘餘風險說明。
[/BV26]

[BV26 preset=CONCLUSION speed=140 pause_after=900ms]
第三，當風險真的發生時，誰負責？誰修？誰通知？誰決定停機或繼續使用？誰確認恢復？誰保存證據？
[/BV26]

[BV26 preset=CONCLUSION speed=140 pause_after=900ms]
如果這三個問題都能回答，這個系統就比較接近可治理。它代表團隊已經具備面對事件的方向感、責任鏈、證據鏈與恢復路徑。
[/BV26]

[BV26 preset=CONCLUSION speed=140 pause_after=900ms]
最後，我想用一句話收束今天的內容：醫療資安的目的，是讓臨床在面對變動與壓力時，仍然有可以依賴的證據、流程和責任鏈。
[/BV26]

[BV26 preset=CONCLUSION speed=140 pause_after=900ms]
謝謝大家。接下來如果有時間，我們可以針對三個方向討論：第一，醫院端採購時應該怎麼看資安證據；第二，醫療器材公司要怎麼準備 FDA 或 TFDA 相關資安材料；第三，滲透測試、白箱審查和部署審查要怎麼分工，才能讓資源投入更精準，並讓風險治理更連續。
[/BV26]

## B. 60 分鐘語速校正建議

目前 `BV26_META.target_duration` 加總為 `60` 分鐘。實際生成時，請用音檔長度
回推語速與停頓，不要只相信字數。

```yaml
if_actual_time_too_short:
  lower_average_speed_cpm: 165
  extend_pause_after_safety_sentences: +200ms
  extend_pause_after_case_events: +150ms
  add_section_gap_ms: +300
  expand_QA_bridge: true

if_actual_time_too_long:
  raise_average_speed_cpm: 185
  remove_selected_dry_jokes: true
  reduce_case_story_detail: true
  shorten_section_gap_ms: -300
  keep_safety_slow_sections: true
```

建議彩排時計時三次：

1. 只讀 clean text，確認純文字長度。
2. 用 orchestrator 產生分段音檔，確認每段是否接近 `target_duration`。
3. 串接完整音檔後，確認停頓、轉場、投影片切換與 Q&A buffer。

## C. TTS 產線切段設定

建議不要一次把整篇丟給 TTS。這份稿有 `17` 個主要 segment，但實際生成時
可以再依 paragraph 切成 `30` 到 `90` 秒音檔。

```yaml
chunking:
  primary_split:
    - BV26_block
    - paragraph
    - rhetorical_pause
  max_chunk_sec: 90
  preferred_chunk_sec: 45
  preserve_pause_tags: true
  strip_control_tags_before_tts: true
  normalize_punctuation: true

post_processing:
  loudness_normalization: -16_LUFS
  silence_between_paragraph_chunks_ms: 250
  silence_between_sections_ms: 1200-1800
  room_tone: none
  de_esser: mild
  compression: light
  export_format: wav_48k_or_mp3_192k
```

## D. 場景版本建議

```yaml
formal_cde_review_version:
  humor_level: 0.22
  authority: 0.76
  warmth: 0.56
  average_speed_cpm: 165
  pause_after_joke_ms: 950

recording_demo_version:
  humor_level: 0.34
  authority: 0.68
  warmth: 0.60
  average_speed_cpm: 175
  pause_after_joke_ms: 850

prof_wu_handoff_version:
  humor_level: 0.18
  authority: 0.72
  warmth: 0.62
  average_speed_cpm: 158
  add_margin_for_manual_rephrasing: true
```

## E. Post-Generation Audio Review Checklist

Use this after `BreezeVoice 26` / `BreezyVoice` generation:

- [ ] Total stitched audio is close to `60` minutes.
- [ ] Each segment starts cleanly and does not cut off first syllables.
- [ ] Long acronyms are pronounced acceptably: FDA, TFDA, CDE, SBOM, PACS,
      HIS, EMR, VPN, EHR.
- [ ] Taiwan hospital names are pronounced acceptably: 長生醫院、馬偕醫院、
      彰化基督教醫院.
- [ ] Ransomware / company names are not mangled beyond recognition:
      Change Healthcare, BlackCat, CrazyHunter, Qilin, Stryker, Foxconn,
      OneBlood, Synnovis, Medibank, Systex.
- [ ] No metadata block is spoken in the output audio.
- [ ] No private LINE, non-public product, or unpublished company detail is
      included in the audio.
- [ ] If timing is too short, lower speed from `0.88` to `0.84`; if too long,
      raise speed from `0.88` to `0.92`.
