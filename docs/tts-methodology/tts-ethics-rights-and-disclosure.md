# TTS Ethics, Rights, And Disclosure

只要 reference voice 來自真人，每案都必須填寫本紀錄或同等內容。未完成授權與揭露紀錄時，不得把生成語音作為可公開或可研究使用的 final package。

## Required Record

```text
Voice source:
Whose voice:
Consent obtained:
Allowed use:
Forbidden use:
Can be shared externally:
Can be used in research:
Need synthetic voice disclosure:
IRB relevance:
Storage location:
Deletion / withdrawal mechanism:
```

## Scope Controls

- 真人聲音只能用於已授權範圍。
- reference audio SHA-256 必須記錄，但 reference audio 本體放 local/private storage。
- 若音檔會給外部合作方、學生、受試者或公開觀眾，應標示 synthetic voice。
- 若語音材料會影響研究受試者反應，TTS artifact 必須納入研究限制與 confound 控制。
- 若聲音提供者撤回授權，必須能定位並刪除 reference audio、生成音檔與衍生 package。

## Storage Rule

公開 repo 可保存授權摘要、hash、用途範圍與 QA 結果。不得提交真人 reference audio、生成音檔、失敗樣本或可重建真人聲音的私人資料。
