# CDE 2026 BreezyVoice pronunciation notes

以下建議以「保留英文技術名詞」為原則。只有容易被 TTS 誤讀，或在台灣醫療資安語境常見多種唸法的詞，才加上建議唸法。若 pilot render 已經穩定，可以不用替換成注音或中文近音。

## 建議保留英文或英文縮寫

| Term | 建議唸法 / 可替代寫法 | 備註 |
| --- | --- | --- |
| CDE | C D E | 不建議唸成一個單字。 |
| TFDA | T F D A | 台灣聽眾熟悉英文縮寫。 |
| FDA | F D A | 保留英文縮寫。 |
| NYCU | N Y C U | 若 TTS 不穩，可寫成「陽明交通大學」。 |
| FDA 510(k) | FDA，五一零 K | 不建議唸成「五百一十括號 k」。 |
| FD&C Act Section 524B | F D and C Act，Section 五二四 B | 若 TTS 卡頓，可在稿內改成「FD&C Act，Section 524B」。 |
| SaMD | S A M D，或 Software as a Medical Device | 第一次可保留全稱，後面用 SaMD。 |
| White-box Testing | white box testing | 可以保留英文；「白箱測試」也可。 |
| black-box testing | black box testing | 可以保留英文；「黑箱測試」也可。 |
| penetration testing | penetration testing | 台灣授課可搭配「滲透測試」。 |
| threat modeling | threat modeling | 台灣華語可讀作「威脅建模」。 |
| SBOM | S B O M | 不建議唸成「斯邦」或單字。 |
| SCA | S C A | Software Composition Analysis。 |
| CVE | C V E | 若提到弱點編號，逐字母唸。 |
| CVSS | C V S S | 不建議唸成一個字。 |
| CVD | C V D | Coordinated Vulnerability Disclosure。 |
| PACS | 派克斯，或 P A C S | 放射科語境常唸「派克斯」；若 TTS 不穩，改 P A C S。 |
| HIS | H I S | 不建議唸成英文單字。 |
| EMR | E M R | 保留縮寫。 |
| RIS | R I S | 放射資訊系統。 |
| LIS | L I S | 檢驗資訊系統。 |
| DICOM | DAI-com；中文提示可寫「戴康」 | 台灣醫療影像語境常見。 |
| HL7 | H L seven | 不建議唸成「hl 七」。 |
| FHIR | fire | 標準唸法接近英文 fire。 |
| API | A P I | 保留縮寫。 |
| VPN | V P N | 保留縮寫。 |
| MFA | M F A | multifactor authentication。 |
| RBAC | R B A C | role-based access control。 |
| IAM | I A M | identity and access management。 |
| K8S | K eight S，或 K 八 S | 若 TTS 誤讀，稿內可改成「K eight S」。 |
| Kubernetes | Kubernetes；中文提示可寫「庫伯內提斯」 | 首次可說「Kubernetes，也就是 K8S」。 |
| Helm charts | Helm charts | K8S 部署檔脈絡使用。 |
| YAML | YAML；必要時可寫「Y A M L」 | TTS 可能讀成一個字；pilot 後決定。 |
| NetworkPolicy | Network Policy | 建議中間加空格，避免 TTS 黏在一起。 |
| SIEM | S I E M | 不建議唸成一個字。 |
| EDR | E D R | endpoint detection and response。 |
| MRI | M R I | 保留縮寫。 |
| CT | C T | 保留縮寫。 |

## 事件與產品名稱

| Term | 建議唸法 / 可替代寫法 | 備註 |
| --- | --- | --- |
| CrazyHunter | Crazy Hunter | 建議中間加空格，TTS 較穩。 |
| Change Healthcare | Change Healthcare | 保留英文名稱。 |
| UnitedHealth | United Health | 若 TTS 黏字，可加空格。 |
| ALPHV BlackCat | A L P H V，Black Cat | 勒索軟體名稱。 |
| Chansn Hospital | Chansn Hospital | 若 TTS 不穩，可在稿內改成中文醫院名稱。 |
| Mackay Memorial Hospital | Mackay Memorial Hospital | 台灣語境可說「馬偕醫院」。 |
| Changhua Christian Hospital | Changhua Christian Hospital | 台灣語境可說「彰化基督教醫院」。 |
| OneBlood | One Blood | 建議加空格。 |
| Stryker | Stryker | 保留英文。 |
| Medibank | Medibank | 保留英文。 |
| Ardent Health Services | Ardent Health Services | 保留英文。 |
| Foxconn | Foxconn | 台灣語境也可說「鴻海」。 |
| Nitrogen | Nitrogen | 勒索軟體名稱，保留英文。 |
| Synnovis | Synnovis | 保留英文。 |
| Qilin | Qilin；中文可讀「麒麟」 | 若 TTS 誤讀，稿內可寫「Qilin，麒麟」。 |
| Signature Healthcare | Signature Healthcare | 保留英文。 |
| Brockton Hospital | Brockton Hospital | 保留英文。 |
| Lurie Children's Hospital | Lurie Children's Hospital | apostrophe 可能造成停頓，必要時寫 Lurie Childrens Hospital。 |
| Contec CMS8000 | Contec C M S eight thousand | 若 TTS 將 8000 唸得過快，可寫「CMS 八千」。 |
| Epsimed MN-120 | Epsimed M N one twenty | 若 TTS 不穩，可寫「MN 一二零」。 |
| Abbott | Abbott | 保留英文。 |
| St. Jude | Saint Jude | 建議寫 Saint Jude，避免 St. 被唸成 street。 |
| Tesla | Tesla | 保留英文。 |
| CrowdStrike | CrowdStrike | 保留英文。 |
| Channel File 291 | Channel File two ninety one | 可寫「Channel File 二九一」讓中文 TTS 更穩。 |
| Log4Shell | Log four Shell | 不建議唸成「log 四殼」；稿內可寫 Log four Shell。 |
| MOVEit Transfer | Move it Transfer | MOVEit 可用「Move it」提示。 |
| DeepBT | Deep B T | 若需要唸產品名，建議拆成 Deep B T。 |
| LIGER AI Manager | Liger A I Manager | LIGER 可唸 Liger，不要逐字母。 |
| Altewan | Altewan | 若 TTS 不穩，可保留不唸或改成公司名稱中文版本。 |

## 建議 pilot render 檢查點

先測一段簡單說明段落：`cde_full_01_opening_positioning_session_fit` 附近的 opening batch。再測一段含英文技術詞段落：搜尋 batch CSV 中含 `Kubernetes`、`K8S`、`RBAC` 的列。再測一段案例密集段落：搜尋含 `Change Healthcare` 或 `Log4Shell` 的列。

Pilot 後如果英文縮寫被連讀，優先做小幅文字替換，例如把 `K8S` 改成 `K eight S`，把 `PACS` 改成 `派克斯`，把 `FD&C` 改成 `F D and C`。不要把所有英文都改成注音，會降低跨領域聽眾的專業辨識度。
