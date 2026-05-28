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

