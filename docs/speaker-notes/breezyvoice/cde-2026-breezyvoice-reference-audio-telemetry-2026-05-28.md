# CDE 2026 BreezyVoice Reference-Audio Telemetry - 2026-05-28

This note is the research appendix for `EXP-20260528-13`. It records the
observable engineering chronology, runtime evidence, failure modes, timing, and
GPU-energy estimates for the reference-audio pilot experiment.

## Scope

- Input audio: local-only `/home/jnln3799/Downloads/260528_0839_record.mp3`.
- Input transcript: local-only `/home/jnln3799/Downloads/260528_0839_record_final.txt`.
- Prompt WAV used by BreezyVoice: `.local/breezyvoice/prompts/v1/jason_reference.wav`.
- Prompt transcript used by BreezyVoice: `.local/breezyvoice/prompts/v1/jason_reference.txt`.
- Prompt duration: `20` seconds, extracted from the formal opening, not the recording-test lead-in.
- Render policy: reference audio is allowed and used; it remains optional and does not reopen the old reference-audio hard requirement.
- Full render policy: still blocked until all required pilot parent chunks pass human listening review.

## Engineering Chronology

| Step | Observation | Decision / Fix | Result |
| --- | --- | --- | --- |
| Reference intake | MP3 existed in Downloads, `16 kHz`, mono, about `702.864 s`. | Use only a short formal-opening prompt to avoid conditioning the model on recording-test speech or long noisy context. | Created local-only `jason_reference.wav` and transcript. |
| Transcript source | Whisper tiny prompt transcript included recording-test text. | Use user-supplied `260528_0839_record_final.txt` and hand-align the `08:39:55` opening segment. | Prompt transcript became stable formal lecture text. |
| Prompt-mode first run | BreezyVoice prompt path failed at `torchaudio.load`; `torchcodec` missing. | Patch local runner to override BreezyVoice `load_wav` with a `soundfile` reader. | Prompt WAV load succeeded. |
| Prompt-mode second run | Synthesis completed but `torchaudio.save` failed on `torchcodec`. | Patch local runner to override BreezyVoice `torchaudio.save` with a `soundfile` writer. | Prompt-mode WAV output succeeded. |
| GPU audit | PyTorch used RTX 5080, but ONNX Runtime reported only CPU/Azure providers. | Replace shadowing CPU `onnxruntime` with `onnxruntime-gpu==1.23.2`. | Provider list became `TensorrtExecutionProvider`, `CUDAExecutionProvider`, `CPUExecutionProvider`. |
| ABI regression | Installing ORT GPU upgraded NumPy to `2.2.6`, breaking Matplotlib / compiled extensions. | Pin `numpy==1.26.4`, `protobuf==4.25.0`, `packaging==24.2`. | Runtime imports and BreezyVoice initialization recovered. |
| Closing failure 1 | `cde_full_26` long summary failed with tensor mismatch: `5002` vs `2`. | Split close into more subclips. | Reduced but did not eliminate the failure. |
| Closing failure 2 | A `168` character compound sentence still triggered the same attention mismatch. | Split `cde_full_26` to conservative clause-level subclips around `90` characters. | Full pilot render completed: `25/25` subclips. |
| Telemetry | Prior runs had only stdout logs and spot `nvidia-smi` checks. | Add `tools/run_with_gpu_telemetry.py`. | Each render can now capture stdout, GPU samples, elapsed time, peak memory, and GPU-only Wh estimate. |

## Runtime Evidence

| Check | Result |
| --- | --- |
| GPU | `NVIDIA GeForce RTX 5080` |
| PyTorch CUDA | available; capability `(12, 0)` |
| PyTorch / torchaudio | `2.11.0+cu128` / `2.11.0+cu128` |
| ONNX Runtime before repair | `['AzureExecutionProvider', 'CPUExecutionProvider']` |
| ONNX Runtime after repair | `['TensorrtExecutionProvider', 'CUDAExecutionProvider', 'CPUExecutionProvider']` |
| ORT warning after repair | Some nodes remain on CPU; ORT reports this as normal for shape-related ops. |
| Local cache handling | `G2PWModel/` is local-only and ignored. |

## Telemetry Runs

| Run | Exit | Rendered | Wall time | Avg GPU power | GPU Wh estimate | Avg GPU util | Peak GPU memory | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `pilot_reference_cuda_ort_after_clause_split` | `1` | `14` | `390.217 s` | `231.341 W` | `25.075873 Wh` | `81.066%` | `15720 MB` | Failed on `cde_full_26` long sentence tensor mismatch. |
| `pilot_reference_cuda_ort_after_clause90` | `0` | `25` | `443.357 s` | `213.898 W` | `26.342492 Wh` | `75.074%` | `13673 MB` | Completed all pilot subclips with clause-level close split. |

Energy scope: GPU-only estimate from `nvidia-smi power.draw` samples. It excludes
CPU, motherboard, storage, display, PSU loss, and room power. Treat it as a
comparative render-efficiency metric, not a facility-grade energy measurement.

## Successful Per-Subclip Timing

| # | subclip_id | render_s | audio_s | audio/render |
| ---: | --- | ---: | ---: | ---: |
| 1 | `cde_full_01_opening_positioning_crazyhunter_entry_case_p01` | `28.307` | `55.205` | `1.950` |
| 2 | `cde_full_01_opening_positioning_crazyhunter_entry_case_p02` | `33.128` | `55.322` | `1.670` |
| 3 | `cde_full_01_opening_positioning_crazyhunter_entry_case_p03` | `23.173` | `46.846` | `2.022` |
| 4 | `cde_full_01_opening_positioning_crazyhunter_entry_case_p04` | `30.975` | `61.603` | `1.989` |
| 5 | `cde_full_16_k8s_review_controls_p01` | `19.362` | `33.994` | `1.756` |
| 6 | `cde_full_16_k8s_review_controls_p02` | `15.603` | `28.781` | `1.845` |
| 7 | `cde_full_16_k8s_review_controls_p03` | `13.569` | `27.318` | `2.013` |
| 8 | `cde_full_16_k8s_review_controls_p04` | `21.005` | `42.353` | `2.016` |
| 9 | `cde_full_20_crowdstrike_update_524b_p01` | `21.798` | `43.073` | `1.976` |
| 10 | `cde_full_20_crowdstrike_update_524b_p02` | `18.145` | `34.482` | `1.900` |
| 11 | `cde_full_20_crowdstrike_update_524b_p03` | `17.305` | `33.483` | `1.935` |
| 12 | `cde_full_20_crowdstrike_update_524b_p04` | `22.451` | `43.595` | `1.942` |
| 13 | `cde_full_26_shared_close_test_anchors_p01` | `7.306` | `13.282` | `1.818` |
| 14 | `cde_full_26_shared_close_test_anchors_p02` | `6.731` | `12.759` | `1.896` |
| 15 | `cde_full_26_shared_close_test_anchors_p03` | `3.489` | `6.861` | `1.966` |
| 16 | `cde_full_26_shared_close_test_anchors_p04` | `8.123` | `15.116` | `1.861` |
| 17 | `cde_full_26_shared_close_test_anchors_p05` | `6.690` | `12.562` | `1.878` |
| 18 | `cde_full_26_shared_close_test_anchors_p06` | `7.275` | `14.443` | `1.985` |
| 19 | `cde_full_26_shared_close_test_anchors_p07` | `7.941` | `15.813` | `1.991` |
| 20 | `cde_full_26_shared_close_test_anchors_p08` | `2.320` | `3.820` | `1.647` |
| 21 | `cde_full_26_shared_close_test_anchors_p09` | `6.725` | `13.444` | `1.999` |
| 22 | `cde_full_26_shared_close_test_anchors_p10` | `4.219` | `8.440` | `2.001` |
| 23 | `cde_full_26_shared_close_test_anchors_p11` | `3.314` | `6.420` | `1.937` |
| 24 | `cde_full_26_shared_close_test_anchors_p12` | `7.630` | `15.430` | `2.022` |
| 25 | `cde_full_26_shared_close_test_anchors_p13` | `10.493` | `21.060` | `2.007` |

Aggregate subclip render time: `347.077 s`; average `13.883 s`; min `2.320 s`;
max `33.128 s`.

## Stitch Result

| Parent chunk | Subclips | Input audio | Stitched audio |
| --- | ---: | ---: | ---: |
| `cde_full_01_opening_positioning_crazyhunter_entry_case` | `4` | `218.98 s` | `221.08 s` |
| `cde_full_16_k8s_review_controls` | `4` | `132.45 s` | `134.55 s` |
| `cde_full_20_crowdstrike_update_524b` | `4` | `154.63 s` | `156.73 s` |
| `cde_full_26_shared_close_test_anchors` | `13` | `159.45 s` | `167.85 s` |
| Full pilot stitch | `4 parent WAVs` | `680.21 s` | `682.31 s` |

## Research Notes

- Reference audio improves voice identity control, but it does not remove the
  need for short subclips. Zero-shot prompt mode is sensitive to long compound
  sentences in the LLM attention path.
- ONNX Runtime CUDA provider is materially important for throughput. After the
  provider repair, pilot subclips generated at roughly `1.65x` to `2.02x` audio
  duration per render second in the successful telemetry run.
- Tiny ASR remains a weak proxy for clinical quality. It still misrecognizes
  technical English and some Chinese terms, so it is useful only as a warning
  signal and cannot replace expert listening.
- The full render remains closed. The correct next gate is human listening
  review of the prompt-mode pilot package.
- Future full-length attempts should use telemetry by default and should keep
  prompt-mode subclip limits tighter than no-reference/default mode.

## Returned-Review Repair Addendum

`EXP-20260528-14` supersedes the earlier `25`-subclip pilot for the next human
listening gate. It responds to the returned expert review and the added
confident-speech rule: the model-facing text now removes low-confidence fillers
such as `這個`, `那個`, `嗯`, `呃`, explicit breath cues, laughter strings,
`吱吱嗚嗚` / `支支吾吾`, and known hallucination residues before synthesis.

The final4 prompt-mode run used the local reference audio and RTX 5080:

| Run | Exit | Rendered | Wall time | Avg GPU power | GPU Wh estimate | Avg GPU util | Peak GPU memory | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `pilot_reference_after_confident_speech_final4` | `0` | `38` | `494.384 s` | `203.473 W` | `27.942732 Wh` | `70.164%` | `14016 MB` | Completed all current pilot subclips in prompt mode after returned-review conditioning. |

The current pilot split is:

| Parent chunk | Subclips | Stitched audio | Target | Ratio | Notes |
| --- | ---: | ---: | ---: | ---: | --- |
| `cde_full_01_opening_positioning_crazyhunter_entry_case` | `8` | `233.84 s` | `185 s` | `1.26` | Slower opening is acceptable only if expert listening confirms authority and no looping. |
| `cde_full_16_k8s_review_controls` | `7` | `182.67 s` | `190 s` | `0.96` | Includes local-only post-synthesis `atempo=0.76` pacing override after synthesis. |
| `cde_full_20_crowdstrike_update_524b` | `9` | `168.85 s` | `190 s` | `0.89` | Still requires expert listening for CrowdStrike, malformed input, supply-chain, and 524B boundaries. |
| `cde_full_26_shared_close_test_anchors` | `14` | `169.72 s` | `155 s` | `1.09` | Short split protects against close-section fatigue; expert should judge stitch naturalness. |

Interrupted or superseded repair attempts are retained in the experiment log:

- `pilot_reference_after_returned_review_repair`: interrupted when stdout
  showed `FDA 510(k)` could become `五百一十(k)`; fixed by mapping `510(k)` /
  `510(K)` to `五一零 K`.
- `pilot_reference_after_returned_review_repair_rerun`: interrupted when
  whitespace-only `五 二 四 B` collapsed toward `五二四B`; fixed with
  punctuation mapping `五、二、四，B`.
- `pilot_reference_after_returned_review_final`: completed but was superseded
  because the close split still relied on a fallback path.
- `pilot_reference_after_confident_speech_final3`: interrupted conservatively
  after runtime printed internal zhuyin annotations; follow-up verified these
  annotations were not present in normalized model inputs.

`tools/verify_breezyvoice_objective.py --write-report` exits `2` with
`overall_status=gated_waiting_human_review`, and
`tools/check_breezyvoice_full_render_gate.py --write-report` exits `2` with
`status=full_render_blocked`. The current human-review package is:

```text
/home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/
/home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz
```

Package validation: `1` full WAV, `4` parent WAVs, `38` subclip WAVs, `4`
normalized segment text files, `38` subclip text files, expert prompt, README,
and expert CSV form. The full 80-minute render remains blocked until all four
parent chunks receive explicit human `accept` decisions.

## Total-Reject Repair Addendum

`EXP-20260528-15` supersedes final4 for the next listening gate. It responds to
the returned expert decision that all four parent chunks must remain rejected
until the pilot is repaired and relistened.

The repair keeps the v1 source frozen and changes only the model-facing render
inputs and local audio post-processing:

- `cde_full_01`: removes trust-question pressure, keeps filler cleanup, uses a
  safer `戴康` reading for DICOM, and splits the opening into `12` subclips.
- `cde_full_16`: localizes K8S/API/RBAC pressure, removes dash/slash leakage
  risk, rewrites the Tesla exposed-console path, splits to `10` subclips, and
  applies `atempo=0.82` after synthesis.
- `cde_full_20`: replaces ambiguous FD&C/524B/SBOM/white-box strings with
  explicit spoken anchors and splits to `11` subclips.
- `cde_full_26`: replaces risky homophones, uses `根本原因` / `白箱` anchors,
  preserves the `14` short closing subclips, and trims `0.8 s` from the final
  thank-you subclip tail.

The final5 attempt was intentionally interrupted when stdout showed a stale
Tesla console phrase. The final5b run completed:

| Run | Exit | Rendered | Wall time | Avg GPU power | GPU Wh estimate | Avg GPU util | Peak GPU memory | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `pilot_reference_after_total_reject_repair_final5` | interrupted | partial | logged locally | n/a | n/a | n/a | n/a | Stopped after stale `exposed K八S console` wording appeared in runtime stdout. |
| `pilot_reference_after_total_reject_repair_final5b` | `0` | `47` | `507.566 s` | `197.054 W` | `27.782796 Wh` | `65.497%` | `14346 MB` | Completed all final5b prompt-mode pilot subclips on RTX 5080. |

Current final5b stitched pilot metrics:

| Parent chunk | Subclips | Stitched audio | Target | Ratio | Post-processing |
| --- | ---: | ---: | ---: | ---: | --- |
| `cde_full_01_opening_positioning_crazyhunter_entry_case` | `12` | `232.49 s` | `185 s` | `1.26` | none |
| `cde_full_16_k8s_review_controls` | `10` | `172.19 s` | `190 s` | `0.91` | `atempo=0.82` |
| `cde_full_20_crowdstrike_update_524b` | `11` | `168.97 s` | `190 s` | `0.89` | none |
| `cde_full_26_shared_close_test_anchors` | `14` | `172.23 s` | `155 s` | `1.11` | final subclip tail trimmed by `0.8 s` |
| Full pilot stitch | `4 parent WAVs` | `747.99 s` | n/a | n/a | `700 ms` parent silence |

ASR tiny was regenerated only as an auxiliary warning signal. It remains weak
for mixed Mandarin/English medical cybersecurity terms and must not override
expert listening. In this pass it still produced severe technical-term
recognition errors, so the gate stays conservative.

`tools/verify_breezyvoice_objective.py --write-report` exits `2` with
`overall_status=gated_waiting_human_review`, and
`tools/check_breezyvoice_full_render_gate.py --write-report` exits `2` with
`status=full_render_blocked`. The refreshed package is:

```text
/home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/
/home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz
```

Package validation: `1` full WAV, `4` parent WAVs, `47` subclip WAVs, `4`
normalized segment text files, `47` subclip text files, expert prompt, README,
and expert CSV form. The full 80-minute render remains blocked until all four
final5b parent chunks receive explicit human `accept` decisions.

## Partial-Accept Repair And Breeze-ASR-25 Addendum

`EXP-20260528-16` supersedes final5b for the next listening gate. The returned
review accepted `cde_full_26_shared_close_test_anchors` and kept
`cde_full_01`, `cde_full_16`, and `cde_full_20` in repair status. The current
package preserves the accepted close as the continuity baseline and rerenders
only the three rejected parent chunks.

Current final6/final6b telemetry:

| Run | Exit | Rendered | Wall time | Avg GPU power | GPU Wh estimate | Avg GPU util | Peak GPU memory | Notes |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| `pilot_reference_after_partial_accept_repair_final6` | `0` | `39` | `407.155 s` | `192.923 W` | `21.819338 Wh` | `65.404%` | `15474 MB` | Rerendered `cde01`, `cde16`, and initial `cde20` repair in prompt mode. |
| `pilot_reference_after_partial_accept_repair_final6b_cde20` | `0` | `11` | `126.252 s` | `186.973 W` | `6.557122 Wh` | `65.350%` | `15683 MB` | Rerendered only `cde20` after the SBOM phrase was expanded to `軟體物料清單，英文四個字母，S，B，O，M`. |

Current final6/final6b stitched pilot metrics:

| Parent chunk | Subclips | Stitched audio | Target | Ratio | Status |
| --- | ---: | ---: | ---: | ---: | --- |
| `cde_full_01_opening_positioning_crazyhunter_entry_case` | `19` | `232.09 s` | `185 s` | `1.25` | repaired; needs human relisten |
| `cde_full_16_k8s_review_controls` | `9` | `168.96 s` | `190 s` | `0.89` | repaired with `atempo=0.88`; needs human relisten |
| `cde_full_20_crowdstrike_update_524b` | `11` | `168.19 s` | `190 s` | `0.89` | final6b repaired; needs human relisten |
| `cde_full_26_shared_close_test_anchors` | `14` | `172.23 s` | `155 s` | `1.11` | accepted baseline preserved |
| Full pilot stitch | `4 parent WAVs` | `743.57 s` | n/a | n/a | full render still blocked |

Current auxiliary ASR policy: use `MediaTek-Research/Breeze-ASR-25` only. Do
not use Whisper for current BreezyVoice review gates. A Whisper tiny command was
run before this policy correction during final6b handling; that output is
archived as superseded and is not used for the current package.

Breeze-ASR-25 auxiliary run:

| Model | Device | Model load | ASR time | Text chars | Timestamp chunks | Output |
| --- | --- | ---: | ---: | ---: | ---: | --- |
| `MediaTek-Research/Breeze-ASR-25` | RTX 5080 CUDA | `3.111 s` | `41.487 s` | `3692` | `216` | `.local/breezyvoice/review/v1/asr/cde-2026-breezyvoice-pilot-stitched-v1.txt` |

Breeze-ASR-25 remains an auxiliary warning signal. It can surface possible term
drift and repeated phrases, but it does not replace human listening for CDE TTS
acceptance.
