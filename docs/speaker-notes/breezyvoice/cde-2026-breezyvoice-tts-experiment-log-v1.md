# CDE 2026 BreezyVoice TTS Experiment Log V1

This is the durable tracked log for every CDE 2026 BreezyVoice TTS
experiment, text-conditioning pass, render attempt, stitch pass, ASR
check, expert-review package, and human-review gate.

Generated audio, raw runtime caches, prompt WAVs, and large local review
packages remain under `.local/` or `~/Downloads/`; this tracked log keeps
the traceable decision record and local evidence paths.

## Logging Contract

- Create or update one experiment record before any new TTS render or
  model-facing text-conditioning pass.
- Record the reason, expected effect, affected prefixes/subclips, exact
  commands, log paths, output paths, machine results, human results, fix
  applied, and next stop rule.
- If human review is required, export a package to `~/Downloads`, record
  both the directory and archive path, and stop before full render until
  human decisions are returned.
- Keep `full_batch_allowed=false` whenever any required pilot parent chunk
  is missing, rejected, undecided, or machine status says
  `needs_human_listening`.
- Do not use stale WAV files that are not listed in the current manifest;
  treat orphan audio as a review-hygiene risk.

## Current Gate

- Source version: `v1`
- Current state: determined by the latest experiment record and
  `.local/breezyvoice/review/v1/full_batch_gate.json`.
- Current owner policy: after final7 human-review repairs, the owner
  allowed proceeding to the next concrete step without another listening
  review round, while preserving the returned review history.
- Current auxiliary ASR policy: use `MediaTek-Research/Breeze-ASR-25`
  only; do not use Whisper for current BreezyVoice review gates.
- Generated audio, ASR, telemetry, and review packages remain local-only
  unless explicitly exported.

## Experiment Index

| ID | Stage | Title | Decision | Next action |
| --- | --- | --- | --- | --- |
| `EXP-20260527-01` | source-intake | Source-complete TTS expert packet intake | proceed_to_model_ready_package | Build v1 model-ready render package |
| `EXP-20260528-01` | freeze-manifest-inputs | Freeze v1 source and generate no-reference render package | proceed_to_runtime_and_pilot_only | Prepare RTX 5080 runtime and render pilot only |
| `EXP-20260528-02` | runtime | Enable BreezyVoice inference on RTX 5080 | runtime_ready_for_pilot | Render only pilot subclips |
| `EXP-20260528-03` | pilot-render-review | Initial no-reference pilot render, stitch, and machine review | full_render_blocked_pending_human_review | Use expert/human review to decide minimal text conditioning |
| `EXP-20260528-04` | term-conditioning | Pilot term-normalization pass after machine/listening risk | continue_to_expert_conditioning_not_full_render | Apply only expert-identified minimal corrections and rerender pilot |
| `EXP-20260528-05` | expert-conditioning-human-gate | Expert pilot review conditioning and refreshed Downloads package | stop_for_human_review_before_full_render | Wait for human listening review; if rejected again, record the review, apply smallest fix, export a new Downloads package, and stop again |
| `EXP-20260528-06` | full-render-stop-gate | Machine-enforced full-render gate check before any next TTS run | stop_for_human_review_enforced_by_machine_gate | Wait for human listening review; if rejected again, record the review and apply only the next minimal pilot fix |
| `EXP-20260528-07` | artifact-hygiene | Quarantine stale orphan pilot WAV before next human package | orphan_audio_quarantined_no_render | Refresh metadata, gate reports, objective verification, and Downloads package without rendering |
| `EXP-20260528-08` | expert-review-ingestion | Add guarded expert-review ingestion path | ingestion_path_ready_gate_still_closed | Wait for completed expert review CSV; ingest it when returned |
| `EXP-20260528-09` | guarded-full-render-template | Add guarded full-render template without running TTS | full_render_template_ready_but_gate_closed | Wait for returned expert review CSV; ingest it, then rerun the gate checker |
| `EXP-20260528-10` | review-log-traceability | Build consolidated render review log before next human gate | render_review_log_builder_ready_gate_still_closed | Export refreshed Downloads review package and wait for completed expert review CSV or specific minimal pilot-fix instruction |
| `EXP-20260528-11` | human-review-traceability | Add pilot correction matrix to human review package | correction_matrix_ready_gate_still_closed | Wait for completed expert review CSV or a specific minimal pilot-fix instruction; do not run full render |
| `EXP-20260528-14` | returned-review-repair | Reference-audio pilot repair with confident-speech sanitization | full_render_blocked_pending_human_listening | Send the Downloads package and PROMPT_FOR_TTS_EXPERT.md to the expert; after returned form, ingest with tools/ingest_breezyvoice_expert_review.py and only then decide the next minimal repair or full-render release |
| `EXP-20260528-12` | pilot-repair-rerender | Round-2 pilot rerender after all-reject contamination review | round2_pilot_rendered_stop_for_human_review | Export refreshed Downloads package and wait for round-2 human listening review |
| `EXP-20260528-19` | text-conditioning | v3 ConvNet reference CJK-English boundary rule | restart v3 render after regenerating manifests with CJK-English boundary punctuation | Regenerate BreezyVoice local render package, rebuild v3 manifests against .local/breezyvoice/output/v3, run one smoke subclip, then restart full v3 render with 80-minute global pacing post-process. |
| `EXP-20260528-20` | pacing-policy | Uniform 0.9x full-session TTS pacing and repeat-removal rule | continue current raw render, then produce 0.9x full-session master | Monitor current v3 render to completion, stitch raw full WAV, apply ffmpeg atempo=0.9 to the full master, then loudness-normalize the 0.9x copy. |
| `EXP-20260528-21` | text-conditioning | Taiwan Traditional Chinese preferred TTS wording | restart v3 render after regenerating manifests with Taiwan Traditional Chinese preferred model-facing text | Regenerate BreezyVoice local render package, rebuild v3 manifests, smoke test, then restart full v3 render; after stitching, produce uniform 0.9x pacing master. |
| `EXP-20260528-22` | text-conditioning | Preserve token and namespace in TTS wording | regenerate manifests before restarting v3 render | Regenerate BreezyVoice local render package, rebuild v3 manifests, smoke test one subclip, restart full v3 render, then produce 0.9x master. |
| `EXP-20260528-13` | reference-audio-cuda-telemetry | Reference-audio pilot render with ONNX CUDA telemetry | reference_prompt_pilot_rendered_stop_for_human_review | Export refreshed Downloads review package with telemetry and wait for expert listening review. |
| `EXP-20260528-15` | final4-human-reject-repair | Total-reject pilot repair with jargon-safe substitutions | final5b_exported_full_render_blocked_for_human_review | Send the refreshed Downloads package to the TTS expert; ingest the returned forms/expert_pilot_review_form.csv; if any row is reject, apply only the next minimal expert-specified pilot fix and rerender affected pilot chunks. |
| `EXP-20260528-16` | final5b-partial-review-repair | Partial-accept pilot repair for cde01 cde16 cde20 with Breeze-ASR-25 auxiliary check | final6b_exported_full_render_blocked_for_human_review | Send refreshed Downloads review package to expert, ingest returned form, and either open the full-render gate or apply the next minimal repair. |
| `EXP-20260528-17` | final6b-human-review-repair-final7 | Mixed-gate final7 pilot repair with 白箱 terminology | final7_exported_full_render_blocked_for_human_review | Send the refreshed Downloads package to the expert; ingest the returned review CSV; only if every required pilot chunk is accepted should the full render gate open. |
| `EXP-20260528-18` | owner-release-full-render-final7 | Owner-overridden full render after final7 repair | full_render_completed_owner_release_post_render_logging | Prepare the deliverable package or handoff copy from the full WAV and loudnorm copy; use Breeze-ASR-25 transcript only to prioritize future repair candidates. |
| `EXP-20260528-23` | v3-text-conditioning-policy | Set v3 delivery target to 70 minutes and story-condition case passages | proceed_to_v3_smoke_then_full_render | Run v3 prompt-mode smoke on RTX 5080, then full render, stitch, normalize to approximately 70 minutes, loudness normalize, and run Breeze-ASR-25. |
| `EXP-20260528-24` | v3-full-render-70min-final | v3 70-minute full render with ConvNet prompt and Breeze-ASR-25 final check | completed_local_70min_master_with_asr_warning_notes | Package the 70-minute audio and model-facing transcript for stakeholder handoff when requested. |
| `EXP-20260528-25` | v3-wu-teacher-handoff-package | Wu teacher reference package with M4A and transcript | downloads_handoff_package_created | Share the Downloads folder or tar.gz package with Wu teacher; keep auxiliary ASR as warning signal only. |
| `EXP-20260528-26` | v3-wu-teacher-handoff-postprocess | Wu teacher package 0.9x M4A listening copy | downloads_handoff_package_updated | Use the 0.9x M4A when a slower reference-listening copy is preferred; original M4A remains preserved. |

## Detailed Records

### EXP-20260527-01 - Source-complete TTS expert packet intake

- Timestamp: `2026-05-27T17:15:48+08:00`
- Stage: `source-intake`
- Input version: `v1`
- Source SHA-256: `pre-v1-source-packet`
- Affected prefixes: `all`

Reason:

- Jingzhong final PPT and source DOCX became the pacing source for the full CDE TTS workflow
- Need a stable source packet before model-ready transcript and render planning

Hypothesis:

- A source-complete expert packet gives traceability from final PPT to Jason section, Jingzhong section, shared close, and TTS expert instructions

Change summary:

- Created source/expert handoff packet under docs/speaker-notes/breezyvoice and copied portable package to Downloads on the prior workstation path recorded in planning

Commands:

- tracked by existing repo commit history and planning handoff
- no TTS render executed in this step

Logs:

- docs/speaker-notes/breezyvoice/expert-package-source/README_FOR_TTS_EXPERT.md
- docs/speaker-notes/breezyvoice/expert-package-source/PROMPT_FOR_TTS_EXPERT.md

Outputs:

- docs/speaker-notes/breezyvoice/expert-package-source/cde-2026-full-transcript-source-for-tts-expert.md
- docs/speaker-notes/breezyvoice/expert-package-source/cde-2026-full-batch-outline.csv

Machine result:

- not applicable; source intake only

Human result:

- not yet reviewed as audio

Decision: `proceed_to_model_ready_package`

Fix applied:

- none; source packet prepared

Downloads package:

- none recorded

Stop rule:

- Do not render until a model-ready transcript, stable output_prefix values, pronunciation notes, and pilot gate exist

Next action:

- Build v1 model-ready render package

Additional observations:

- Keep collaboration notes out of model input; only spoken lecture text should enter TTS

### EXP-20260528-01 - Freeze v1 source and generate no-reference render package

- Timestamp: `2026-05-28T00:01:00+08:00`
- Stage: `freeze-manifest-inputs`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `all`

Reason:

- The 80 minute engineering transcript needed traceable audio-to-text provenance before any TTS batch
- User explicitly changed policy so reference audio must not block execution

Hypothesis:

- Freezing v1, extracting clean text, splitting subclips, and allowing default/no-reference voice will make pilot rendering reproducible on local hardware

Change summary:

- Generated freeze report, render manifest, subclip manifest, clean segment inputs, normalized subclip inputs, pronunciation policy, runtime readiness, audio spec, pilot checklist, and full-render gate

Commands:

- python3 tools/prepare_breezyvoice_render_package.py

Logs:

- .local/breezyvoice/freeze/v1/freeze_report.md
- .local/breezyvoice/review/v1/objective_audit.md
- .local/breezyvoice/runtime/v1/runtime_readiness.md

Outputs:

- .local/breezyvoice/manifests/v1/package_summary.json
- .local/breezyvoice/manifests/v1/render_manifest.csv
- .local/breezyvoice/manifests/v1/subclip_manifest.csv
- .local/breezyvoice/inputs/v1/subclips/

Machine result:

- 26 chunks
- 92 planned subclips
- 80:00 target
- 28053 model-text characters
- reference_audio_required=false
- full_batch_allowed=false

Human result:

- not applicable before pilot audio

Decision: `proceed_to_runtime_and_pilot_only`

Fix applied:

- Configured no-reference/default voice mode and kept reference WAV optional

Downloads package:

- none recorded

Stop rule:

- Do not run full render until four pilot parent chunks pass listening review

Next action:

- Prepare RTX 5080 runtime and render pilot only

Additional observations:

- Generated audio remains local-only; tracked docs store source, rules, and reproducibility surfaces

### EXP-20260528-02 - Enable BreezyVoice inference on RTX 5080

- Timestamp: `2026-05-28T00:05:00+08:00`
- Stage: `runtime`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `all`

Reason:

- The official BreezyVoice torch cu118 runtime does not support RTX 5080 sm_120
- Local pilot render needed a CUDA 12.8 capable PyTorch environment

Hypothesis:

- A local venv with cu128 PyTorch can run BreezyVoice inference while keeping runtime files under .local

Change summary:

- Added RTX 5080 setup script and local runtime readiness check; no source transcript change

Commands:

- bash tools/setup_breezyvoice_rtx5080_runtime.sh
- python3 tools/prepare_breezyvoice_render_package.py

Logs:

- .local/breezyvoice/runtime/v1/torch_cu128_upgrade.log
- .local/breezyvoice/runtime/v1/dependency_install.log
- .local/breezyvoice/runtime/v1/runtime_readiness.json

Outputs:

- .local/breezyvoice/runtime/v1/venv/
- .local/BreezyVoice/

Machine result:

- runtime_readiness records local venv torch and ready_to_render status; missing reference audio does not block default voice

Human result:

- not applicable; runtime only

Decision: `runtime_ready_for_pilot`

Fix applied:

- Replaced unsupported cu118 torch path with CUDA 12.8-capable local runtime

Downloads package:

- none recorded

Stop rule:

- If CUDA runtime fails again, record the exact error and do not alter transcript to mask runtime failure

Next action:

- Render only pilot subclips

Additional observations:

- onnxruntime CUDA provider warning appears in logs, but pilot render still completes through available runtime path

### EXP-20260528-03 - Initial no-reference pilot render, stitch, and machine review

- Timestamp: `2026-05-28T00:12:00+08:00`
- Stage: `pilot-render-review`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `cde_full_01_opening_positioning_crazyhunter_entry_case, cde_full_16_k8s_review_controls, cde_full_20_crowdstrike_update_524b, cde_full_26_shared_close_test_anchors`

Reason:

- Full render must not start until representative opening, dense technical, regulatory, and closing chunks are checked
- Need audio evidence for pacing, acronym stability, and label-safety

Hypothesis:

- Four pilot parent chunks can reveal most TTS risks before spending GPU time on all 92 subclips

Change summary:

- Rendered pilot subclips in no-reference/default mode, stitched parent chunks, stitched combined pilot WAV, ran ASR auxiliary check, and built listening review gate

Commands:

- bash .local/breezyvoice/commands/v1/run_pilot_template.sh
- python3 tools/stitch_breezyvoice_outputs.py --selection pilot --stitch-full --overwrite
- python3 tools/build_breezyvoice_pilot_review.py

Logs:

- .local/breezyvoice/runtime/v1/pilot_gpu_render.log
- .local/breezyvoice/review/v1/pilot_stitch_summary.json
- .local/breezyvoice/review/v1/pilot_machine_review.json
- .local/breezyvoice/review/v1/pilot_listening_review.md

Outputs:

- .local/breezyvoice/output/v1/subclips/
- .local/breezyvoice/output/v1/parent_chunks/
- .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav

Machine result:

- Pilot audio rendered and stitched; ASR had no forbidden BV26/markup hits but status remained needs_human_listening due mixed technical term misses

Human result:

- Human listening not yet accepted

Decision: `full_render_blocked_pending_human_review`

Fix applied:

- none at this stage; generated pilot evidence only

Downloads package:

- none recorded

Stop rule:

- If any pilot parent chunk is undecided or rejected, do not run full batch

Next action:

- Use expert/human review to decide minimal text conditioning

Additional observations:

- ASR is too weak for mixed Taiwan Mandarin technical English; it can catch spoken markup but cannot replace listening

### EXP-20260528-04 - Pilot term-normalization pass after machine/listening risk

- Timestamp: `2026-05-28T00:18:00+08:00`
- Stage: `term-conditioning`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `all; pilot-sensitive terms in cde_full_16 and cde_full_20`

Reason:

- Pilot review exposed risk around acronym spacing and high-risk mixed English terms
- Need low-risk model-facing changes without modifying frozen source

Hypothesis:

- Conservative replacements such as K8S to K eight S, 524B to 五二四 B, and Channel File 291 to Channel File 二九一 reduce misreads while preserving professional term recognition

Change summary:

- Added low-risk term normalization in model-facing text only; preserved v1 source and stable output_prefix traceability

Commands:

- python3 tools/prepare_breezyvoice_render_package.py
- bash .local/breezyvoice/commands/v1/run_pilot_template.sh
- python3 tools/stitch_breezyvoice_outputs.py --selection pilot --stitch-full --overwrite
- python3 tools/build_breezyvoice_pilot_review.py

Logs:

- .local/breezyvoice/runtime/v1/pilot_gpu_render_after_term_normalization.log
- .local/breezyvoice/review/v1/asr/pilot_whisper_tiny_after_term_normalization.log
- .local/breezyvoice/review/v1/asr/archive/pilot-before-term-normalization/

Outputs:

- .local/breezyvoice/inputs/v1/normalized_segments/
- .local/breezyvoice/inputs/v1/subclips/
- .local/breezyvoice/output/v1/

Machine result:

- Pilot rerender completed; machine ASR still insufficient for acceptance and full_batch_allowed remained false

Human result:

- No accepted human review yet

Decision: `continue_to_expert_conditioning_not_full_render`

Fix applied:

- Acronym spacing and high-risk term normalizations only

Downloads package:

- none recorded

Stop rule:

- Do not add broad phonetic rewriting unless human listening identifies a specific term failure

Next action:

- Apply only expert-identified minimal corrections and rerender pilot

Additional observations:

- Term normalization can change subclip counts, so stale WAVs must be audited against current manifest before packaging

### EXP-20260528-05 - Expert pilot review conditioning and refreshed Downloads package

- Timestamp: `2026-05-28T00:24:00+08:00`
- Stage: `expert-conditioning-human-gate`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `cde_full_01_opening_positioning_crazyhunter_entry_case, cde_full_16_k8s_review_controls, cde_full_20_crowdstrike_update_524b, cde_full_26_shared_close_test_anchors`

Reason:

- User-pasted expert review rejected pilot chunks for breath artifacts, pacing collapse, stumbles, and critical term errors
- Conflicting review sections disagreed on cde_full_26, so conservative gate treats all four parent chunks as rejected until re-listening

Hypothesis:

- Applying only punctuation, spacing, single-term, and narrow phrase conditioning can improve the no-reference pilot while preserving frozen v1 source and professional English recognizability

Change summary:

- Applied conservative pilot-review conditioning for PACS/DICOM, K8S/RBAC/API pacing, Tesla cloud cryptomining phrase, CrowdStrike Falcon update, supply chain, 524B, and white-box terminology; rerendered and stitched current pilot

Commands:

- python3 tools/prepare_breezyvoice_render_package.py
- bash .local/breezyvoice/commands/v1/run_pilot_template.sh
- python3 tools/stitch_breezyvoice_outputs.py --selection pilot --stitch-full --overwrite
- python3 tools/build_breezyvoice_pilot_review.py
- python3 tools/export_breezyvoice_expert_review_package.py --overwrite

Logs:

- .local/breezyvoice/review/v1/expert_review_decision_2026-05-28.json
- .local/breezyvoice/runtime/v1/pilot_gpu_render_after_expert_conditioning.log
- .local/breezyvoice/review/v1/asr/pilot_whisper_tiny_after_expert_conditioning.log
- .local/breezyvoice/review/v1/pilot_stitch_summary.json
- .local/breezyvoice/review/v1/full_batch_gate.json

Outputs:

- .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Machine result:

- Current package summary: 26 chunks, 92 planned subclips, 14 pilot subclips, 80:00, 28053 chars, no-reference default voice, full_batch_allowed=false; parent runtimes 222.53s, 145.78s, 160.15s, 171.70s; ASR forbidden markup hits=0 and status=needs_human_listening

Human result:

- Expert review requires rejection/re-listening; no accepted pilot decisions yet

Decision: `stop_for_human_review_before_full_render`

Fix applied:

- Minimal text conditioning only; no frozen-source rewrite and no broad phonetic conversion

Downloads package:

- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Stop rule:

- Stop here unless human review returns accept for all four pilot parent chunks or gives specific minimal fixes for another pilot rerender

Next action:

- Wait for human listening review; if rejected again, record the review, apply smallest fix, export a new Downloads package, and stop again

Additional observations:

- Current local output directory can contain stale WAVs from prior manifests; artifact hygiene should be audited and only manifest-listed files should enter review packages
- Machine ASR is useful for forbidden markup, but not reliable enough for professional-term acceptance

### EXP-20260528-06 - Machine-enforced full-render gate check before any next TTS run

- Timestamp: `2026-05-28T00:43:30+08:00`
- Stage: `full-render-stop-gate`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `cde_full_01_opening_positioning_crazyhunter_entry_case, cde_full_16_k8s_review_controls, cde_full_20_crowdstrike_update_524b, cde_full_26_shared_close_test_anchors`

Reason:

- The workflow needs a hard stop so full render cannot proceed while human listening decisions are reject or undecided
- User instructed that when human review is required, work should stop and wait rather than continue generation

Hypothesis:

- A dedicated gate checker that exits non-zero when pilot decisions are not all accept will prevent accidental full-batch rendering and produce auditable evidence for reviewers

Change summary:

- Added check_breezyvoice_full_render_gate.py, generated full_render_gate_check.json, updated docs and review package export to include the gate report

Commands:

- python3 tools/prepare_breezyvoice_render_package.py
- python3 tools/build_breezyvoice_pilot_review.py
- python3 tools/check_breezyvoice_full_render_gate.py --write-report
- python3 tools/export_breezyvoice_expert_review_package.py --overwrite

Logs:

- .local/breezyvoice/review/v1/full_render_gate_check.json
- .local/breezyvoice/review/v1/full_batch_gate.json
- .local/breezyvoice/review/v1/pilot_listening_review.csv

Outputs:

- tools/check_breezyvoice_full_render_gate.py
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/review/full_render_gate_check.json
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Machine result:

- Gate checker exited 2 as expected: allowed=false, full_batch_allowed=false, accepted_by_listening=false, four required pilot chunks unaccepted

Human result:

- No new human review received

Decision: `stop_for_human_review_enforced_by_machine_gate`

Fix applied:

- No TTS text or audio change; added gate enforcement and package evidence

Downloads package:

- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Stop rule:

- Do not run full render unless check_breezyvoice_full_render_gate.py exits 0 after all four pilot decisions are accept

Next action:

- Wait for human listening review; if rejected again, record the review and apply only the next minimal pilot fix

Additional observations:

- This gate should be run in any future full-render command template or manual runbook
- The review package now includes the gate report so experts see why generation is stopped

### EXP-20260528-07 - Quarantine stale orphan pilot WAV before next human package

- Timestamp: `2026-05-28T00:47:00+08:00`
- Stage: `artifact-hygiene`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `cde_full_16_k8s_review_controls`

Reason:

- The verifier and orphan inventory showed one local subclip WAV from a prior manifest that was no longer listed in the current subclip manifest
- Keeping stale audio beside current pilot files can confuse human review and future package assembly

Hypothesis:

- Moving the orphan WAV into an archive folder preserves evidence while preventing it from being mistaken for a current pilot deliverable

Change summary:

- Moved cde_full_16_k8s_review_controls_p04.wav from output/v1/subclips to output/v1/archive/orphan-audio-2026-05-28

Commands:

- mkdir -p .local/breezyvoice/output/v1/archive/orphan-audio-2026-05-28
- mv .local/breezyvoice/output/v1/subclips/cde_full_16_k8s_review_controls_p04.wav .local/breezyvoice/output/v1/archive/orphan-audio-2026-05-28/

Logs:

- .local/breezyvoice/review/v1/orphan_audio_inventory.csv
- docs/speaker-notes/breezyvoice/cde-2026-breezyvoice-tts-experiment-log-v1.md

Outputs:

- .local/breezyvoice/output/v1/archive/orphan-audio-2026-05-28/cde_full_16_k8s_review_controls_p04.wav

Machine result:

- Artifact moved; no TTS render executed

Human result:

- No new human review received

Decision: `orphan_audio_quarantined_no_render`

Fix applied:

- Local artifact hygiene only; no text, manifest, or accepted-review change

Downloads package:

- none recorded

Stop rule:

- Rebuild metadata and export package; full render remains blocked unless gate checker exits 0

Next action:

- Refresh metadata, gate reports, objective verification, and Downloads package without rendering

Additional observations:

- Quarantining stale audio is safer than deleting it because prior experiment logs can still trace the earlier render attempt

### EXP-20260528-08 - Add guarded expert-review ingestion path

- Timestamp: `2026-05-28T00:52:00+08:00`
- Stage: `expert-review-ingestion`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `cde_full_01_opening_positioning_crazyhunter_entry_case, cde_full_16_k8s_review_controls, cde_full_20_crowdstrike_update_524b, cde_full_26_shared_close_test_anchors`

Reason:

- The workflow needs a safe way to turn returned human review CSV decisions into local gate state
- Manual editing of pilot_listening_review.csv or full_batch_gate.json risks opening full render with blank or partial decisions

Hypothesis:

- A guarded ingester that rejects blank or partial forms will preserve the human-review boundary while allowing accepted reviews to open the gate reproducibly

Change summary:

- Added ingest_breezyvoice_expert_review.py and documented the returned-review workflow in BreezyVoice README files and expert package instructions

Commands:

- python3 tools/ingest_breezyvoice_expert_review.py --input /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/forms/expert_pilot_review_form.csv --dry-run

Logs:

- docs/speaker-notes/breezyvoice/README.md
- docs/speaker-notes/breezyvoice/model-ready/README.md

Outputs:

- tools/ingest_breezyvoice_expert_review.py

Machine result:

- Dry-run against blank Downloads form exited 2 as expected with invalid_or_blank_decisions for all four required prefixes

Human result:

- No new human review received

Decision: `ingestion_path_ready_gate_still_closed`

Fix applied:

- No TTS text or audio change; added guarded review-ingestion workflow only

Downloads package:

- none recorded

Stop rule:

- Do not run full render until ingested expert review has accept for all four chunks and check_breezyvoice_full_render_gate.py exits 0

Next action:

- Wait for completed expert review CSV; ingest it when returned

Additional observations:

- This closes a process gap: the return path from human review now has the same rigor as export and rendering gates

### EXP-20260528-09 - Add guarded full-render template without running TTS

- Timestamp: `2026-05-28T00:55:00+08:00`
- Stage: `guarded-full-render-template`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `all`

Reason:

- After human review accepts all pilot chunks, the workflow needs a single safe command for full render
- The command must not allow manual full-batch rendering while full_batch_allowed=false

Hypothesis:

- A generated run_full_render_template.sh that calls the full-render gate checker before rendering all subclips will preserve the human-review boundary and standardize the final stitch path

Change summary:

- Added guarded full-render command template generation and aligned all-selection stitch output to cde-2026-breezyvoice-80min-v1.wav

Commands:

- python3 tools/prepare_breezyvoice_render_package.py
- bash .local/breezyvoice/commands/v1/run_full_render_template.sh

Logs:

- .local/breezyvoice/review/v1/full_render_gate_check.json
- .local/breezyvoice/commands/v1/run_full_render_template.sh

Outputs:

- tools/prepare_breezyvoice_render_package.py
- tools/stitch_breezyvoice_outputs.py
- docs/speaker-notes/breezyvoice/README.md
- docs/speaker-notes/breezyvoice/model-ready/README.md

Machine result:

- Guarded full-render template exited 2 at the gate checker; no full TTS render ran and cde-2026-breezyvoice-80min-v1.wav was not created

Human result:

- No new human review received

Decision: `full_render_template_ready_but_gate_closed`

Fix applied:

- No TTS text or audio change; added guarded future command path

Downloads package:

- none recorded

Stop rule:

- Do not run full render unless run_full_render_template.sh reaches rendering after check_breezyvoice_full_render_gate.py exits 0

Next action:

- Wait for returned expert review CSV; ingest it, then rerun the gate checker

Additional observations:

- The final full WAV path is now explicit and matches audio_output_spec.json, reducing post-accept command ambiguity

### EXP-20260528-10 - Build consolidated render review log before next human gate

- Timestamp: `2026-05-28T01:02:00+08:00`
- Stage: `review-log-traceability`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `all, cde_full_01_opening_positioning_crazyhunter_entry_case, cde_full_16_k8s_review_controls, cde_full_20_crowdstrike_update_524b, cde_full_26_shared_close_test_anchors`

Reason:

- The previous render_review_log.csv was a blank template even though pilot parent WAVs, runtime ratios, and reject decisions already existed

Hypothesis:

- A manifest-driven render review log will make every TTS attempt auditable without running additional TTS or opening the full-render gate

Change summary:

- Added tools/build_breezyvoice_render_review_log.py to merge render_manifest, subclip_manifest, parent WAV duration, and pilot listening review decisions
- Updated generated command templates and README docs to rebuild render_review_log.csv after pilot review and full render stitch
- Preserved prepare_breezyvoice_render_package.py from wiping an existing enriched render review log

Commands:

- python3 tools/prepare_breezyvoice_render_package.py
- python3 tools/build_breezyvoice_pilot_review.py
- python3 tools/build_breezyvoice_render_review_log.py
- python3 tools/check_breezyvoice_full_render_gate.py --write-report
- python3 tools/verify_breezyvoice_objective.py --write-report

Logs:

- .local/breezyvoice/review/v1/render_review_log.csv
- .local/breezyvoice/review/v1/full_render_gate_check.json
- .local/breezyvoice/review/v1/objective_verification.json

Outputs:

- tools/build_breezyvoice_render_review_log.py
- docs/speaker-notes/breezyvoice/cde-2026-breezyvoice-tts-experiment-log-v1.md
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/

Machine result:

- render_review_log.csv now has 26 rows; four pilot parent chunks include runtime_seconds and reject status; non-pilot rows remain not_rendered_full_batch_gated
- Full-render gate checker exited 2 as expected with allowed=false and four unaccepted pilot chunks
- Objective verifier exited 2 as expected with overall_status=gated_waiting_human_review

Human result:

- No new human listening review received in this step

Decision: `render_review_log_builder_ready_gate_still_closed`

Fix applied:

- Traceability/logging fix only; no TTS text, no audio render, no full batch run

Downloads package:

- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Stop rule:

- Do not run full render until all four pilot parent chunks are accepted by human listening and check_breezyvoice_full_render_gate.py exits 0

Next action:

- Export refreshed Downloads review package and wait for completed expert review CSV or specific minimal pilot-fix instruction

Additional observations:

- FIRST PRINCIPLE: audio generation is a controlled manufacturing step; the review log is the batch record that binds source, chunk, runtime, defect, fix, and gate decision before scale-up

### EXP-20260528-11 - Add pilot correction matrix to human review package

- Timestamp: `2026-05-28T01:06:00+08:00`
- Stage: `human-review-traceability`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `cde_full_01_opening_positioning_crazyhunter_entry_case, cde_full_16_k8s_review_controls, cde_full_20_crowdstrike_update_524b, cde_full_26_shared_close_test_anchors`

Reason:

- The gate package needed a compact per-chunk map from expert-reported issue to already-applied text conditioning and the remaining listening question

Hypothesis:

- A correction matrix will reduce review ambiguity while preserving the stop rule that human listening must accept all four pilot chunks before full render

Change summary:

- Added tools/build_breezyvoice_pilot_correction_matrix.py
- Generated pilot_correction_matrix.csv, .md, and .json under local review evidence
- Updated expert package export and README instructions so reviewers see the issue-to-fix matrix

Commands:

- python3 tools/prepare_breezyvoice_render_package.py
- python3 tools/build_breezyvoice_pilot_review.py
- python3 tools/build_breezyvoice_render_review_log.py
- python3 tools/build_breezyvoice_pilot_correction_matrix.py
- python3 tools/check_breezyvoice_full_render_gate.py --write-report
- python3 tools/verify_breezyvoice_objective.py --write-report
- python3 tools/export_breezyvoice_expert_review_package.py --overwrite

Logs:

- .local/breezyvoice/review/v1/pilot_correction_matrix.md
- .local/breezyvoice/review/v1/pilot_correction_matrix.csv
- .local/breezyvoice/review/v1/objective_verification.json

Outputs:

- tools/build_breezyvoice_pilot_correction_matrix.py
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/review/pilot_correction_matrix.md
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Machine result:

- Correction matrix generated four pilot rows with runtime, gate decision, expert issue, applied conditioning, fix status, next listener question, and stop rule
- Objective verifier now reports pilot correction matrix completed while overall status remains gated_waiting_human_review
- Full-render gate checker still exits 2 with allowed=false, as expected

Human result:

- No new human listening review received in this step

Decision: `correction_matrix_ready_gate_still_closed`

Fix applied:

- Review traceability only; no model-facing text change, no TTS render, no full batch run

Downloads package:

- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Stop rule:

- If human listening is required, keep the package in Downloads and stop until accept/reject decisions or specific minimal pilot fixes return

Next action:

- Wait for completed expert review CSV or a specific minimal pilot-fix instruction; do not run full render

Additional observations:

- FIRST PRINCIPLE: the pilot gate is a quality-control batch record; reviewers need to know whether they are judging an unresolved defect or a fix that still needs acceptance

### EXP-20260528-14 - Reference-audio pilot repair with confident-speech sanitization

- Timestamp: `2026-05-28T03:08:48.658384+00:00`
- Stage: `returned-review-repair`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `cde_full_01_opening_positioning_crazyhunter_entry_case, cde_full_16_k8s_review_controls, cde_full_20_crowdstrike_update_524b, cde_full_26_shared_close_test_anchors`

Reason:

- Returned expert audit conservatively rejected all four parent chunks; user additionally required no hesitant TTS fillers such as 這個, 那個, or 吱吱嗚嗚 in generated audio
- Full 80-minute render must remain blocked until renewed human listening accepts all four parent chunks
- Research log must capture runtime, GPU/energy telemetry, failed/interrupted attempts, cause, resolution, and remaining observations

Hypothesis:

- Reference audio can preserve a more suitable lecturer identity if model-facing text removes stage cues, known hallucination residues, low-confidence fillers, and high-risk English/Chinese boundary pressure
- Fine subclip splitting plus post-synthesis atempo=0.76 for cde_full_16 should move the technical chunk out of the prior 0.73 compressed pacing band
- ASR tiny is useful only as a weak risk signal for gross breakdowns, not as a substitute for human listening

Change summary:

- Conditioned model-facing text for AI, PACS/DICOM workflow wording, RBAC/service-account/Kubernetes/Tesla console wording, CrowdStrike malformed-input and 524B punctuation, closing white-box/logging/recovery anchors
- Added generic sanitization for low-confidence fillers: 這個, 那個, 嗯, 呃, 對啊, 阿哈, laughter strings, 吱吱嗚嗚, 支支吾吾, and known hallucination residues
- Prepared 119 full-session subclips and 38 pilot subclips; pilot split is cde01=8, cde16=7, cde20=9, cde26=14
- Added reproducible post-synthesis audio pacing tool and applied atempo=0.76 to the seven cde_full_16 subclips after final4 render

Commands:

- python3 tools/prepare_breezyvoice_render_package.py
- python3 tools/run_with_gpu_telemetry.py --telemetry-jsonl .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_confident_speech_final4_gpu.jsonl --summary-json .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_confident_speech_final4_summary.json --stdout-log .local/breezyvoice/runtime/v1/pilot_reference_after_confident_speech_final4.log --sample-interval-s 1 -- .local/breezyvoice/runtime/v1/venv/bin/python tools/breezyvoice_render_subclips.py --selection pilot --voice-mode prompt --model-path MediaTek-Research/BreezyVoice --speaker-id auto --prompt-audio .local/breezyvoice/prompts/v1/jason_reference.wav --prompt-text-file .local/breezyvoice/prompts/v1/jason_reference.txt --subclip-manifest .local/breezyvoice/manifests/v1/subclip_manifest.csv --pilot-manifest .local/breezyvoice/manifests/v1/pilot_manifest.csv --output-dir .local/breezyvoice/output/v1/subclips --overwrite
- python3 tools/apply_breezyvoice_audio_pacing.py --parent-prefix cde_full_16_k8s_review_controls --tempo 0.76 --label 20260528-confident-speech-final4 --overwrite
- python3 tools/stitch_breezyvoice_outputs.py --selection pilot --stitch-full --overwrite --silence-ms 700
- python3 tools/build_breezyvoice_pilot_review.py
- python3 tools/build_breezyvoice_render_review_log.py
- python3 tools/build_breezyvoice_pilot_correction_matrix.py
- .local/breezyvoice/runtime/v1/venv/bin/python -m whisper .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav --model tiny --language zh --output_format txt --output_dir .local/breezyvoice/review/v1/asr
- python3 tools/verify_breezyvoice_objective.py --write-report
- python3 tools/check_breezyvoice_full_render_gate.py --write-report
- python3 tools/export_breezyvoice_expert_review_package.py --overwrite

Logs:

- .local/breezyvoice/runtime/v1/pilot_reference_after_returned_review_repair.log: interrupted after stdout showed FDA 510(k) would synthesize as 五百一十(k); fixed by mapping 510(k)/510(K) to 五一零 K
- .local/breezyvoice/runtime/v1/pilot_reference_after_returned_review_repair_rerun.log: interrupted after stdout showed 五 二 四 B spacing collapsed to 五二四B; fixed by punctuation mapping 五、二、四，B
- .local/breezyvoice/runtime/v1/pilot_reference_after_returned_review_final.log: completed 37 subclips but was superseded because cde26 split fallback was still too coarse
- .local/breezyvoice/runtime/v1/pilot_reference_after_confident_speech_final3.log: interrupted conservatively when runtime printed internal zhuyin annotations; follow-up confirmed annotations were BreezyVoice internal frontend output and not present in normalized inputs
- .local/breezyvoice/runtime/v1/pilot_reference_after_confident_speech_final4.log: completed 38 selected subclips in prompt mode
- .local/breezyvoice/runtime/v1/pacing_confident_speech_final4.log
- .local/breezyvoice/review/v1/asr/pilot_whisper_tiny_after_confident_speech_final4.log
- .local/breezyvoice/review/v1/objective_verification.json
- .local/breezyvoice/review/v1/full_render_gate_check.json

Outputs:

- .local/breezyvoice/output/v1/subclips/: 38 current pilot WAV files
- .local/breezyvoice/output/v1/parent_chunks/: 4 stitched parent WAV files
- .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav sha256=f6c98568fa2b210bbf6b6b3105205712ea2af2852a91648628985f1d2bc20a69
- .local/breezyvoice/review/v1/pilot_listening_review.csv
- .local/breezyvoice/review/v1/pilot_stitch_summary.json
- .local/breezyvoice/review/v1/pilot_correction_matrix.md
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Machine result:

- RTX 5080 used successfully; torch CUDA reports NVIDIA GeForce RTX 5080 and ONNX Runtime providers include TensorRTExecutionProvider, CUDAExecutionProvider, CPUExecutionProvider
- final4 render elapsed_s=494.384, avg_gpu_power_w=203.473, estimated_gpu_energy_wh=27.942732, avg_gpu_utilization_pct=70.164, max_gpu_memory_used_mb=14016.0, sample_count=481
- post-pacing cde_full_16 runtime=182.67s, target=190s, ratio=0.96; prior returned-review failure band was about 0.73
- current parent runtimes: cde01=233.84/185 ratio=1.26, cde16=182.67/190 ratio=0.96, cde20=168.85/190 ratio=0.89, cde26=169.72/155 ratio=1.09
- normalized text scan found no 這個, 那個, 吱吱嗚嗚, 支支吾吾, 對啊, 阿哈, 媽媽, 這老能, x console, or x公顯 residues
- objective verifier exited 2 with overall_status=gated_waiting_human_review; full-render gate checker exited 2 with status=full_render_blocked
- Downloads review package validation passed with 1 full WAV, 4 parent WAVs, 38 subclip WAVs, 4 normalized segment text files, 38 subclip text files, expert prompt, README, and expert form
- Whisper tiny ASR remains noisy and flags possible repeated/garbled regions; treat it as auxiliary evidence requiring expert listening, not as an automatic reject/accept decision

Human result:

- Returned expert audit before this rerender was conservatively interpreted as reject for all four pilot parent chunks; no human acceptance exists for final4 yet; Downloads package is ready for expert listening

Decision: `full_render_blocked_pending_human_listening`

Fix applied:

- No-reference requirement remains supported, but this experiment intentionally used the Downloads reference audio and transcript in prompt mode for comparison
- Removed low-confidence filler wording from model-facing text; confident natural vocalization is allowed, hesitant filler delivery is not
- Applied post-synthesis atempo=0.76 only to cde_full_16 and archived originals under .local/breezyvoice/output/v1/archive/pacing-before-20260528-confident-speech-final4/

Downloads package:

- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Stop rule:

- Stop before any 80-minute full render; wait for human expert review of the exported final4 package; proceed only after all four parent chunks are accepted

Next action:

- Send the Downloads package and PROMPT_FOR_TTS_EXPERT.md to the expert; after returned form, ingest with tools/ingest_breezyvoice_expert_review.py and only then decide the next minimal repair or full-render release

Additional observations:

- BreezyVoice runtime prints internal zhuyin annotations such as 稽[:ㄐㄧ1]核 after frontend conversion; these are not present in normalized input text and should be monitored in listening review for possible leakage
- The closing chunk cde26 now has 14 very short subclips, which protects autoregressive fatigue but may create a slightly segmented delivery; expert should judge stitch naturalness
- The biggest unresolved research risk is not GPU capability but mixed-language decoder stability under technical acronym clusters; future iterations may need a domain lexicon or stronger Chinese paraphrase policy for high-risk English lists

### EXP-20260528-12 - Round-2 pilot rerender after all-reject contamination review

- Timestamp: `2026-05-28T08:46:00+08:00`
- Stage: `pilot-repair-rerender`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `cde_full_01_opening_positioning_crazyhunter_entry_case, cde_full_16_k8s_review_controls, cde_full_20_crowdstrike_update_524b, cde_full_26_shared_close_test_anchors`

Reason:

- Returned expert review rejected all four pilot parent chunks for text-cleaning contamination symptoms, no-reference hallucination, pacing collapse, and tail-end fatigue

Hypothesis:

- Model-facing sanitizer, stale input quarantine, finer pilot splitting, 700ms stitch silence, and pilot-only overwrite rerender can reduce decoder instability before another human listening gate

Change summary:

- Ingested the returned all-reject expert review
- Added model-facing stage-cue, filler, and hallucination-residue sanitizer
- Forced cde_full_16/cde_full_20 to four subclips and cde_full_26 to anchor-based subclips
- Archived stale generated subclip text that no longer appears in the current manifest
- Overwrote and rerendered all 16 current pilot subclips only

Commands:

- python3 tools/prepare_breezyvoice_render_package.py
- python3 tools/ingest_breezyvoice_expert_review.py --input .local/breezyvoice/review/v1/returned_expert_review_2026-05-28_round2.csv
- PYTHONUTF8=1 .local/breezyvoice/runtime/v1/venv/bin/python tools/breezyvoice_render_subclips.py --selection pilot --voice-mode default --subclip-manifest .local/breezyvoice/manifests/v1/subclip_manifest.csv --pilot-manifest .local/breezyvoice/manifests/v1/pilot_manifest.csv --output-dir .local/breezyvoice/output/v1/subclips --overwrite
- python3 tools/stitch_breezyvoice_outputs.py --selection pilot --stitch-full --overwrite --silence-ms 700
- .local/breezyvoice/runtime/v1/venv/bin/python -m whisper .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav --model tiny --language zh --output_format txt --output_dir .local/breezyvoice/review/v1/asr
- python3 tools/verify_breezyvoice_objective.py --write-report

Logs:

- .local/breezyvoice/review/v1/returned_expert_review_2026-05-28_round2.csv
- .local/breezyvoice/review/v1/orphan_input_inventory.csv
- .local/breezyvoice/runtime/v1/pilot_gpu_render_after_round2_repair.log
- .local/breezyvoice/review/v1/asr/pilot_whisper_tiny_after_round2_repair.log
- .local/breezyvoice/review/v1/objective_verification.json

Outputs:

- .local/breezyvoice/manifests/v1/subclip_manifest.csv
- .local/breezyvoice/output/v1/subclips/
- .local/breezyvoice/output/v1/parent_chunks/
- .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/

Machine result:

- Round-2 manifest has 97 planned full subclips and 16 current pilot subclips
- All 16 pilot subclips were overwritten and rendered in no-reference/default mode
- Pilot was stitched with 700ms silence; parent runtimes are about 223.47s, 145.63s, 159.25s, and 166.93s
- Tiny ASR was regenerated as an auxiliary signal; it still shows poor mixed technical-term recognition, so human listening remains required
- Full-render gate remains allowed=false

Human result:

- Returned review is all reject; no round-2 acceptance yet

Decision: `round2_pilot_rendered_stop_for_human_review`

Fix applied:

- Pilot-only model-facing preprocessing, stale input quarantine, finer subclip split, and overwrite rerender; frozen source unchanged; no full render

Downloads package:

- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Stop rule:

- Stop after exporting the round-2 pilot package; do not run full render until human review accepts all four required pilot chunks

Next action:

- Export refreshed Downloads package and wait for round-2 human listening review

Additional observations:

- FIRST PRINCIPLE: no-reference/default voice may be the underlying instability; round-2 review should decide whether to continue with this voice path or switch voice strategy before full render

### EXP-20260528-19 - v3 ConvNet reference CJK-English boundary rule

- Timestamp: `2026-05-28T09:02:28.404428+00:00`
- Stage: `text-conditioning`
- Input version: `v3-convnet-reference`
- Source SHA-256: ``
- Affected prefixes: `all CDE BreezyVoice v3 subclips`

Reason:

- Owner required every Chinese-English boundary in TTS model-facing text to use an ideographic comma so Mandarin and English do not merge in speech.

Hypothesis:

- Adding audible boundary punctuation before synthesis will reduce code-switching blur, acronym merging, and pacing instability more reliably than audio-only post-processing.

Change summary:

- Stopped the in-progress v3 raw render, added enforce_cjk_latin_breaks() to prepare_breezyvoice_render_package.py, documented the rule in AGENTS.md and BreezyVoice READMEs, and added a global memory note for future TTS work.

Commands:

- kill -TERM -1273502; python3 -m py_compile tools/prepare_breezyvoice_render_package.py; inline normalize_text smoke test

Logs:

- .local/breezyvoice/runtime/v3/full_convnet_reference_global_28s_v3.log; .local/breezyvoice/runtime/v3/telemetry/full_convnet_reference_global_28s_v3_summary.json

Outputs:

- Updated preprocessing and documentation; previous partial v3 subclips remain local-only evidence and are not the main delivery.

Machine result:

- py_compile passed; normalize_text now inserts ideographic comma at CJK/Latin boundaries.

Human result:

- Owner rule: Chinese and English must be separated by ideographic comma; unstable TTS should be repaired by simpler model-facing text with clear phrase breaks.

Decision: `restart v3 render after regenerating manifests with CJK-English boundary punctuation`

Fix applied:

- Repo rule, global memory note, and preprocessing implementation added.

Downloads package:

- none recorded

Stop rule:

- No additional human review gate requested after this repair; proceed to the next concrete render step unless GPU/runtime fails.

Next action:

- Regenerate BreezyVoice local render package, rebuild v3 manifests against .local/breezyvoice/output/v3, run one smoke subclip, then restart full v3 render with 80-minute global pacing post-process.

Additional observations:

- BreezyVoice runtime G2P stdout annotations such as [:ㄌㄜ4] are internal annotations, not source-script pollution. Use Breeze-ASR-25 only for auxiliary ASR; do not use Whisper.

### EXP-20260528-20 - Uniform 0.9x full-session TTS pacing and repeat-removal rule

- Timestamp: `2026-05-28T09:15:13.014527+00:00`
- Stage: `pacing-policy`
- Input version: `v3-convnet-reference-cjk-breaks`
- Source SHA-256: ``
- Affected prefixes: `full-session v3 master audio and any affected repeated subclips`

Reason:

- Owner requested the overall TTS pacing speed be adjusted to 0.9x and repeated passages be deleted or repaired through clearer model-facing text before rerendering.

Hypothesis:

- A uniform 0.9x post-synthesis full-session master will make pacing more consistent and bring the v3 course closer to the intended 80-minute delivery, while repeat-removal/model-text repair prevents attention-loop artifacts from becoming final audio.

Change summary:

- Documented uniform 0.9x master pacing and repeated-passage repair in AGENTS.md, BreezyVoice README files, and global memory note.

Commands:

- apply_patch AGENTS.md docs/speaker-notes/breezyvoice/README.md docs/speaker-notes/breezyvoice/model-ready/README.md; add memory note 20260528-171441-breezyvoice-pacing-and-repeat-rule.md

Logs:

- .local/breezyvoice/runtime/v3/full_convnet_cjk_breaks_v3.log; .local/breezyvoice/runtime/v3/telemetry/full_convnet_cjk_breaks_v3_summary.json

Outputs:

- Pending after current v3 render: raw stitched WAV plus uniform atempo=0.9 full-session pacing master and loudness-normalized copy.

Machine result:

- Rule recorded while v3 full render continues; post-synthesis atempo=0.9 will be applied after stitching.

Human result:

- Owner requested 0.9x overall pacing and duplicate-repeat removal or clearer segmented model-facing text before rerendering unstable clips.

Decision: `continue current raw render, then produce 0.9x full-session master`

Fix applied:

- Policy added to repo docs and global memory note.

Downloads package:

- none recorded

Stop rule:

- If repeated same-passage audio is detected, remove the duplicated repeated portion or revise and rerender affected model-facing text before treating the master as final.

Next action:

- Monitor current v3 render to completion, stitch raw full WAV, apply ffmpeg atempo=0.9 to the full master, then loudness-normalize the 0.9x copy.

Additional observations:

- The 0.9x rule supersedes the earlier variable-duration normalization plan unless owner explicitly requests a different target duration.

### EXP-20260528-21 - Taiwan Traditional Chinese preferred TTS wording

- Timestamp: `2026-05-28T09:41:46.054127+00:00`
- Stage: `text-conditioning`
- Input version: `v3-convnet-reference-cjk-breaks`
- Source SHA-256: ``
- Affected prefixes: `all CDE BreezyVoice v3 subclips`

Reason:

- Owner requested TTS model-facing text use Taiwan Traditional Chinese customary wording for all non-proper English, preserving only necessary English proper nouns, product names, event names, and standard acronyms.

Hypothesis:

- Replacing ordinary English phrases with Taiwan Traditional Chinese while preserving proper nouns/acronyms will reduce mixed-language instability and improve learner comprehension without losing technical identity anchors.

Change summary:

- Stopped the active v3 render, added NON_PROPER_ENGLISH_ZHTW_NORMALIZATIONS and SPOKEN_ENGLISH_SENTENCE_REWRITES, documented the rule in AGENTS.md and BreezyVoice READMEs, and added a global memory note.

Commands:

- kill -TERM -1327013; python3 -m py_compile tools/prepare_breezyvoice_render_package.py; inline normalize_text smoke tests

Logs:

- .local/breezyvoice/runtime/v3/full_convnet_cjk_breaks_v3.log; .local/breezyvoice/runtime/v3/telemetry/full_convnet_cjk_breaks_v3_summary.json

Outputs:

- Updated preprocessing and documentation; current partial v3 subclips remain local-only interrupted-run evidence and are not the main delivery.

Machine result:

- py_compile passed; smoke tests converted non-proper English phrases such as story map, lifecycle, patient safety, evidence chain, deployment evidence, and credential handling into Taiwan Traditional Chinese while preserving CrowdStrike and Tesla.

Human result:

- Owner rule: except for English proper nouns, rewrite TTS wording into Taiwan Traditional Chinese customary phrasing.

Decision: `restart v3 render after regenerating manifests with Taiwan Traditional Chinese preferred model-facing text`

Fix applied:

- Repo rule, global memory note, and preprocessing dictionary/sentence rewrites added.

Downloads package:

- none recorded

Stop rule:

- If remaining non-proper English causes unstable TTS, add a targeted Taiwan Traditional Chinese rewrite and rerender the affected subclip.

Next action:

- Regenerate BreezyVoice local render package, rebuild v3 manifests, smoke test, then restart full v3 render; after stitching, produce uniform 0.9x pacing master.

Additional observations:

- Use Breeze-ASR-25 only for auxiliary ASR; do not use Whisper. Keep CJK-English ideographic comma boundary rule active for preserved English names/acronyms.

### EXP-20260528-22 - Preserve token and namespace in TTS wording

- Timestamp: `2026-05-28T09:45:17.077688+00:00`
- Stage: `text-conditioning`
- Input version: `v3-convnet-reference-zh-tw-preferred`
- Source SHA-256: ``
- Affected prefixes: `all CDE BreezyVoice v3 subclips containing token or namespace`

Reason:

- Owner clarified that token and namespace should remain English technical terms and should not be translated under the Taiwan Traditional Chinese preferred wording rule.

Hypothesis:

- Preserving token and namespace will keep Kubernetes/security terminology recognizable while the surrounding non-proper English remains Taiwan Traditional Chinese.

Change summary:

- Removed token and namespace from non-proper-English translation; changed service account token to service account token preserving token as English; documented preserved terms in AGENTS.md, BreezyVoice READMEs, and global memory note.

Commands:

- apply_patch; python3 -m py_compile tools/prepare_breezyvoice_render_package.py; inline normalize_text smoke test

Logs:

- .local/breezyvoice/runtime/v3/prepare_for_v3_convnet_zh_tw_preferred_r2.log

Outputs:

- Updated preprocessing and documentation; render not yet restarted after this correction.

Machine result:

- py_compile passed; smoke test emits 服務帳號、token、與、namespace、隔離 while converting deployment evidence and credential handling.

Human result:

- Owner exception: token, namespace should not be translated.

Decision: `regenerate manifests before restarting v3 render`

Fix applied:

- token/namespace preservation added to repo docs and global memory note; service-account-token phrase fixed to preserve token.

Downloads package:

- none recorded

Stop rule:

- Do not translate token or namespace in future TTS model-facing text.

Next action:

- Regenerate BreezyVoice local render package, rebuild v3 manifests, smoke test one subclip, restart full v3 render, then produce 0.9x master.

Additional observations:

- This is an exception to the broader Taiwan Traditional Chinese preferred wording rule.

### EXP-20260528-13 - Reference-audio pilot render with ONNX CUDA telemetry

- Timestamp: `2026-05-28T09:55:00+08:00`
- Stage: `reference-audio-cuda-telemetry`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `cde_full_01_opening_positioning_crazyhunter_entry_case,cde_full_16_k8s_review_controls,cde_full_20_crowdstrike_update_524b,cde_full_26_shared_close_test_anchors`

Reason:

- User supplied 260528_0839_record.mp3 and 260528_0839_record_final.txt as reference audio material; no-reference pilot had repeated hallucination and pacing failures; user requested RTX 5080 GPU usage and ONNX Runtime CUDA provider repair; user requested complete research-grade logging including time and energy.

Hypothesis:

- A short formal-opening reference prompt plus ONNX Runtime CUDA provider and clause-level closing split can render the pilot in prompt mode on RTX 5080 while avoiding zero-shot long-sentence attention failure.

Change summary:

- Copied local-only reference MP3 into .local prompt area; extracted 20s formal-opening WAV from 260528_0839_record.mp3; used transcript from 260528_0839_record_final.txt; preserved reference audio as optional rather than mandatory; patched prompt runner to use soundfile for prompt WAV load/save to bypass torchaudio torchcodec requirement; replaced CPU onnxruntime with onnxruntime-gpu 1.23.2 while pinning numpy 1.26.4 protobuf 4.25.0 packaging 24.2; added GPU telemetry wrapper; split cde_full_26 to clause-level subclips after repeated zero-shot tensor mismatch; ignored local G2PWModel cache.

Commands:

- ffmpeg -ss 10 -t 20 -i /home/jnln3799/Downloads/260528_0839_record.mp3 -ac 1 -ar 16000 .local/breezyvoice/prompts/v1/jason_reference.wav; uv pip uninstall onnxruntime onnxruntime-gpu; uv pip install onnxruntime-gpu==1.23.2 numpy==1.26.4 protobuf==4.25.0 packaging==24.2; python3 tools/prepare_breezyvoice_render_package.py; python3 tools/run_with_gpu_telemetry.py --telemetry-jsonl .local/breezyvoice/runtime/v1/telemetry/pilot_reference_cuda_ort_after_clause90_gpu.jsonl --summary-json .local/breezyvoice/runtime/v1/telemetry/pilot_reference_cuda_ort_after_clause90_summary.json --stdout-log .local/breezyvoice/runtime/v1/pilot_reference_cuda_ort_after_clause90.log -- .local/breezyvoice/runtime/v1/venv/bin/python tools/breezyvoice_render_subclips.py --selection pilot --voice-mode prompt --overwrite; python3 tools/stitch_breezyvoice_outputs.py --selection pilot --stitch-full --overwrite --silence-ms 700; .local/breezyvoice/runtime/v1/venv/bin/python -m whisper .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav --model tiny --language zh --output_format txt

Logs:

- .local/breezyvoice/runtime/v1/pilot_reference_cuda_provider_smoke.log,.local/breezyvoice/runtime/v1/pilot_reference_cuda_ort_after_clause_split.log,.local/breezyvoice/runtime/v1/telemetry/pilot_reference_cuda_ort_after_clause_split_summary.json,.local/breezyvoice/runtime/v1/pilot_reference_cuda_ort_after_clause90.log,.local/breezyvoice/runtime/v1/telemetry/pilot_reference_cuda_ort_after_clause90_summary.json,.local/breezyvoice/runtime/v1/telemetry/pilot_reference_cuda_ort_after_clause90_gpu.jsonl,.local/breezyvoice/review/v1/asr/pilot_whisper_tiny_after_reference_cuda_ort_clause90.log,.local/breezyvoice/review/v1/objective_verification.json

Outputs:

- .local/breezyvoice/prompts/v1/jason_reference.wav,.local/breezyvoice/prompts/v1/jason_reference.txt,.local/breezyvoice/manifests/v1/subclip_manifest.csv,.local/breezyvoice/output/v1/subclips,.local/breezyvoice/output/v1/parent_chunks,.local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav,.local/breezyvoice/review/v1/pilot_stitch_summary.json

Machine result:

- ONNX Runtime provider list changed from AzureExecutionProvider/CPUExecutionProvider to TensorRTExecutionProvider/CUDAExecutionProvider/CPUExecutionProvider; GPU smoke render completed; failed clause-split run rendered 14 subclips then failed on cde_full_26 long sentence with tensor size mismatch; failed telemetry elapsed_s=390.217 avg_gpu_power_w=231.341 estimated_gpu_energy_wh=25.075873 max_gpu_memory_used_mb=15720; successful clause90 run rendered 25/25 subclips exit_code=0 elapsed_s=443.357 avg_gpu_power_w=213.898 estimated_gpu_energy_wh=26.342492 avg_gpu_utilization_pct=75.074 max_gpu_memory_used_mb=13673; subclip elapsed sum=347.077s avg=13.883s min=2.320s max=33.128s; stitched pilot duration=682.31s; full render gate remains blocked.

Human result:

- No human listening acceptance yet; tiny ASR remains auxiliary and shows severe recognition errors, so human listening is still mandatory.

Decision: `reference_prompt_pilot_rendered_stop_for_human_review`

Fix applied:

- Reference-audio prompt mode, ONNX Runtime CUDA provider repair, soundfile prompt I/O fallback, 90-character clause-level close split, GPU telemetry capture, pilot-only render and stitch; no full render.

Downloads package:

- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/,/home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Stop rule:

- Do not run full render until all four required pilot parent chunks are accepted by human listening review.

Next action:

- Export refreshed Downloads review package with telemetry and wait for expert listening review.

Additional observations:

- Energy figures are GPU-only nvidia-smi power.draw estimates and exclude CPU/system/display/PSU energy; thinking time is recorded as observable engineering intervention chronology rather than hidden model reasoning; ONNX CUDA improved prompt-mode runtime substantially but ASR proxy still suggests clinical listening review is non-negotiable; future renders should always run through tools/run_with_gpu_telemetry.py.

### EXP-20260528-15 - Total-reject pilot repair with jargon-safe substitutions

- Timestamp: `2026-05-28T11:50:00+08:00`
- Stage: `final4-human-reject-repair`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `cde_full_01_opening_positioning_crazyhunter_entry_case, cde_full_16_k8s_review_controls, cde_full_20_crowdstrike_update_524b, cde_full_26_shared_close_test_anchors`

Reason:

- Returned expert review marked all four parent chunks reject: cde01 loop/bracket/DICOM/filler issues; cde16 K8S/RBAC/API/Tesla collapse and runtime compression; cde20 FD&C/white-box/threat drift; cde26 homophone drift/laughter-like risk/524B/SBOM/root-cause/tail residue.

Hypothesis:

- A model-facing-only repair can reduce decoder pressure without changing the frozen v1 source: safer Chinese anchors for risky jargon, finer pilot splits, cde16 post-synthesis pacing, and cde26 tail trimming should create a better human-review candidate while keeping full render closed.

Change summary:

- Removed low-confidence filler/demonstrative phrasing such as 這個/那個/嗯/呃 from model-facing text only
- Changed DICOM to 戴康 and PACS downtime to 派克斯停機時間
- Localized K8S/API/RBAC pressure with Chinese anchors and K 八 S wording
- Replaced FD&C/524B/SBOM/white-box/root-cause paths with explicit F D C Act, 五二四英文字母B款, S B O M, 白箱, 根本原因 anchors
- Split pilot to 47 subclips: cde01=12 cde16=10 cde20=11 cde26=14
- Applied cde16 atempo=0.82 after synthesis and trimmed 0.8s from cde26 p14 tail

Commands:

- python3 tools/ingest_breezyvoice_expert_review.py --input .local/breezyvoice/review/v1/expert_review_returned_20260528_final4_total_reject.csv
- python3 tools/prepare_breezyvoice_render_package.py
- python3 tools/run_with_gpu_telemetry.py --telemetry-jsonl .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_total_reject_repair_final5b_gpu.jsonl --summary-json .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_total_reject_repair_final5b_summary.json --stdout-log .local/breezyvoice/runtime/v1/pilot_reference_after_total_reject_repair_final5b.log --sample-interval-s 1 -- .local/breezyvoice/runtime/v1/venv/bin/python tools/breezyvoice_render_subclips.py --selection pilot --voice-mode prompt --model-path MediaTek-Research/BreezyVoice --speaker-id auto --prompt-audio .local/breezyvoice/prompts/v1/jason_reference.wav --prompt-text-file .local/breezyvoice/prompts/v1/jason_reference.txt --subclip-manifest .local/breezyvoice/manifests/v1/subclip_manifest.csv --pilot-manifest .local/breezyvoice/manifests/v1/pilot_manifest.csv --output-dir .local/breezyvoice/output/v1/subclips --overwrite
- python3 tools/apply_breezyvoice_audio_pacing.py --parent-prefix cde_full_16_k8s_review_controls --tempo 0.82 --label 20260528-total-reject-repair-final5b --overwrite
- python3 tools/trim_breezyvoice_audio_tail.py --subclip-id cde_full_26_shared_close_test_anchors_p14 --tail-seconds 0.8 --label 20260528-total-reject-repair-final5b --overwrite
- python3 tools/stitch_breezyvoice_outputs.py --selection pilot --stitch-full --overwrite --silence-ms 700
- python3 tools/build_breezyvoice_pilot_review.py
- python3 tools/build_breezyvoice_render_review_log.py
- python3 tools/build_breezyvoice_pilot_correction_matrix.py
- .local/breezyvoice/runtime/v1/venv/bin/python -m whisper .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav --model tiny --language zh --output_format txt --output_dir .local/breezyvoice/review/v1/asr
- python3 tools/verify_breezyvoice_objective.py --write-report
- python3 tools/check_breezyvoice_full_render_gate.py --write-report
- python3 tools/export_breezyvoice_expert_review_package.py --overwrite

Logs:

- .local/breezyvoice/runtime/v1/pilot_reference_after_total_reject_repair_final5.log
- .local/breezyvoice/runtime/v1/pilot_reference_after_total_reject_repair_final5b.log
- .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_total_reject_repair_final5b_summary.json
- .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_total_reject_repair_final5b_gpu.jsonl
- .local/breezyvoice/runtime/v1/pacing_total_reject_repair_final5b.log
- .local/breezyvoice/runtime/v1/tail_trim_total_reject_repair_final5b.log
- .local/breezyvoice/review/v1/asr/pilot_whisper_tiny_after_total_reject_repair_final5b.log
- .local/breezyvoice/review/v1/objective_verification.json
- .local/breezyvoice/review/v1/full_render_gate_check.json

Outputs:

- .local/breezyvoice/manifests/v1/subclip_manifest.csv
- .local/breezyvoice/output/v1/subclips
- .local/breezyvoice/output/v1/parent_chunks
- .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav
- .local/breezyvoice/review/v1/pilot_listening_review.csv
- .local/breezyvoice/review/v1/render_review_log.csv
- .local/breezyvoice/review/v1/pilot_correction_matrix.md

Machine result:

- final5 was intentionally interrupted after stdout showed stale exposed K八S console wording; final5b completed 47 selected prompt-mode subclips with exit_code=0; final5b elapsed_s=507.566, avg_gpu_power_w=197.054, estimated_gpu_energy_wh=27.782796, avg_gpu_utilization_pct=65.497, max_gpu_memory_used_mb=14346; final stitched pilot duration=747.99s; parent runtimes/ratios after pacing and trim: cde01 232.49/185=1.26, cde16 172.19/190=0.91, cde20 168.97/190=0.89, cde26 172.23/155=1.11; objective verifier exit 2 and full-render gate exit 2 because all four chunks require fresh human listening decisions; export exit 0 and copied 1 full WAV, 4 parent WAVs, 47 subclip WAVs, 47 subclip text files.

Human result:

- Returned final4 expert review was total reject. No human acceptance exists for final5b; ASR tiny is auxiliary only and produced severe technical-term errors, reinforcing the need for expert listening rather than automated acceptance.

Decision: `final5b_exported_full_render_blocked_for_human_review`

Fix applied:

- Model-facing jargon-safe substitutions, confident-speech filler cleanup, 47-subclip pilot split, cde16 atempo=0.82 pacing, cde26 0.8s tail trim, refreshed review log/matrix, ASR auxiliary pass, and Downloads review package export.

Downloads package:

- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Stop rule:

- Stop here. Do not run the 80-minute full render until all four final5b parent chunks are explicitly accepted by human listening review and tools/check_breezyvoice_full_render_gate.py exits 0.

Next action:

- Send the refreshed Downloads package to the TTS expert; ingest the returned forms/expert_pilot_review_form.csv; if any row is reject, apply only the next minimal expert-specified pilot fix and rerender affected pilot chunks.

Additional observations:

- GPU energy is a GPU-only nvidia-smi power.draw estimate and excludes CPU, storage, display, PSU loss, and monitor energy; observable engineering intervention time includes one interrupted final5 render plus the 507.566s final5b render, post-processing, ASR, gate checks, export, and documentation; hidden model reasoning is not measurable, so the log records observable command chronology, timestamps, runtimes, and decision evidence instead. cde01 current subclips are 12 pieces, approximately 60-122 model-text chars each; observed generated audio lengths were roughly 11-26s with average about 18s before stitching. Full render remains closed even though a new package exists.

### EXP-20260528-16 - Partial-accept pilot repair for cde01 cde16 cde20 with Breeze-ASR-25 auxiliary check

- Timestamp: `2026-05-28T12:24:00+08:00`
- Stage: `final5b-partial-review-repair`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `cde_full_01_opening_positioning_crazyhunter_entry_case, cde_full_16_k8s_review_controls, cde_full_20_crowdstrike_update_524b`

Reason:

- Returned final5b review accepted cde26 but rejected cde01 for trust-sentence loop and filler hallucination, cde16 for tight RBAC/CI-CD/K8S boundaries, and cde20 for SBOM/Rollback/524B phrasing drift.
- User specified that all auxiliary ASR for this workflow must use Breeze-ASR-25 rather than Whisper.

Hypothesis:

- Repairing only the three rejected parent chunks while preserving accepted cde26 audio will reduce review churn and keep the full render gate conservative.
- Breeze-ASR-25 gives a project-aligned auxiliary transcript for current review packages, while human listening remains the acceptance authority.

Change summary:

- cde01 trust sentence isolated to a short subclip and opening split increased to 19 subclips.
- cde01 question list converted from short question bursts to declarative sentence boundaries.
- cde16 RBAC/CI-CD/application endpoint boundaries strengthened and cde16 post-synthesis atempo=0.88 applied.
- cde20 rollback replaced with 回滾 and cde20 SBOM occurrence expanded to 軟體物料清單，英文四個字母，S，B，O，M.
- cde26 accepted review preserved and not selected for rerender.
- Current canonical auxiliary ASR regenerated with MediaTek-Research/Breeze-ASR-25; the attempted Whisper tiny final6b transcript was archived as superseded and is not used for current review.

Commands:

- python3 tools/ingest_breezyvoice_expert_review.py --input .local/breezyvoice/review/v1/expert_review_returned_20260528_final5b_partial_accept.csv
- python3 tools/prepare_breezyvoice_render_package.py
- python3 tools/run_with_gpu_telemetry.py --telemetry-jsonl .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_partial_accept_repair_final6_gpu.jsonl --summary-json .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_partial_accept_repair_final6_summary.json --stdout-log .local/breezyvoice/runtime/v1/pilot_reference_after_partial_accept_repair_final6.log --sample-interval-s 1 -- .local/breezyvoice/runtime/v1/venv/bin/python tools/breezyvoice_render_subclips.py --selection pilot --voice-mode prompt --model-path MediaTek-Research/BreezyVoice --speaker-id auto --prompt-audio .local/breezyvoice/prompts/v1/jason_reference.wav --prompt-text-file .local/breezyvoice/prompts/v1/jason_reference.txt --subclip-manifest .local/breezyvoice/manifests/v1/subclip_manifest.csv --pilot-manifest .local/breezyvoice/manifests/v1/pilot_manifest_rejects_final6.csv --output-dir .local/breezyvoice/output/v1/subclips --overwrite
- python3 tools/apply_breezyvoice_audio_pacing.py --parent-prefix cde_full_16_k8s_review_controls --tempo 0.88 --label 20260528-partial-accept-repair-final6 --overwrite
- python3 tools/run_with_gpu_telemetry.py --telemetry-jsonl .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_partial_accept_repair_final6b_cde20_gpu.jsonl --summary-json .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_partial_accept_repair_final6b_cde20_summary.json --stdout-log .local/breezyvoice/runtime/v1/pilot_reference_after_partial_accept_repair_final6b_cde20.log --sample-interval-s 1 -- .local/breezyvoice/runtime/v1/venv/bin/python tools/breezyvoice_render_subclips.py --selection pilot --voice-mode prompt --model-path MediaTek-Research/BreezyVoice --speaker-id auto --prompt-audio .local/breezyvoice/prompts/v1/jason_reference.wav --prompt-text-file .local/breezyvoice/prompts/v1/jason_reference.txt --subclip-manifest .local/breezyvoice/manifests/v1/subclip_manifest.csv --pilot-manifest .local/breezyvoice/manifests/v1/pilot_manifest_cde20_final6b.csv --output-dir .local/breezyvoice/output/v1/subclips --overwrite
- python3 tools/stitch_breezyvoice_outputs.py --selection pilot --stitch-full --overwrite --silence-ms 700
- PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True .local/breezyvoice/runtime/v1/venv/bin/python tools/run_breeze_asr25.py --audio .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav --output-txt .local/breezyvoice/review/v1/asr/cde-2026-breezyvoice-pilot-stitched-v1.txt --output-json .local/breezyvoice/review/v1/asr/breeze_asr25_after_partial_accept_repair_final6b.json --output-timestamped .local/breezyvoice/review/v1/asr/breeze_asr25_after_partial_accept_repair_final6b_timestamped.txt --log .local/breezyvoice/review/v1/asr/breeze_asr25_after_partial_accept_repair_final6b.log --language zh --chunk-length-s 15 --batch-size 1 --num-beams 1
- python3 tools/build_breezyvoice_pilot_review.py
- python3 tools/build_breezyvoice_render_review_log.py
- python3 tools/build_breezyvoice_pilot_correction_matrix.py
- python3 tools/verify_breezyvoice_objective.py --write-report
- python3 tools/check_breezyvoice_full_render_gate.py --write-report
- python3 tools/export_breezyvoice_expert_review_package.py --overwrite

Logs:

- .local/breezyvoice/runtime/v1/pilot_reference_after_partial_accept_repair_final6.log
- .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_partial_accept_repair_final6_summary.json
- .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_partial_accept_repair_final6_gpu.jsonl
- .local/breezyvoice/runtime/v1/pacing_partial_accept_repair_final6.log
- .local/breezyvoice/runtime/v1/pilot_reference_after_partial_accept_repair_final6b_cde20.log
- .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_partial_accept_repair_final6b_cde20_summary.json
- .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_partial_accept_repair_final6b_cde20_gpu.jsonl
- .local/breezyvoice/review/v1/asr/breeze_asr25_after_partial_accept_repair_final6b.log
- .local/breezyvoice/review/v1/asr/breeze_asr25_after_partial_accept_repair_final6b.json
- .local/breezyvoice/review/v1/objective_verification.json
- .local/breezyvoice/review/v1/full_render_gate_check.json

Outputs:

- .local/breezyvoice/manifests/v1/subclip_manifest.csv
- .local/breezyvoice/output/v1/subclips
- .local/breezyvoice/output/v1/parent_chunks
- .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav
- .local/breezyvoice/review/v1/asr/cde-2026-breezyvoice-pilot-stitched-v1.txt
- .local/breezyvoice/review/v1/pilot_listening_review.csv
- .local/breezyvoice/review/v1/render_review_log.csv
- .local/breezyvoice/review/v1/pilot_correction_matrix.md

Machine result:

- final6 completed 39 selected prompt-mode subclips with exit_code=0; elapsed_s=407.155, avg_gpu_power_w=192.923, estimated_gpu_energy_wh=21.819338, avg_gpu_utilization_pct=65.404, max_gpu_memory_used_mb=15474.
- cde20 final6b completed 11 selected prompt-mode subclips with exit_code=0; elapsed_s=126.252, avg_gpu_power_w=186.973, estimated_gpu_energy_wh=6.557122, avg_gpu_utilization_pct=65.35, max_gpu_memory_used_mb=15683.
- cde16 pacing atempo=0.88 produced stitched runtime 168.96/190=0.89.
- Final stitched pilot duration is 743.57s: cde01 232.09/185=1.25 with 19 subclips; cde16 168.96/190=0.89 with 9 subclips; cde20 168.19/190=0.89 with 11 subclips; cde26 172.23/155=1.11 with 14 accepted baseline subclips.
- Breeze-ASR-25 auxiliary ASR ran on RTX 5080 CUDA with model_load_elapsed_s=3.111, asr_elapsed_s=41.487, text_characters=3692, chunk_count=216.
- Objective verifier exits 2 with gated_waiting_human_review; full-render gate exits 2 with full_render_blocked; export exits 0 and copied 1 full WAV, 4 parent WAVs, 53 subclip WAVs, and 53 subclip text files.

Human result:

- Final5b expert review accepted cde26 and rejected cde01/cde16/cde20. Final6/final6b repaired audio requires fresh human listening for those three chunks.

Decision: `final6b_exported_full_render_blocked_for_human_review`

Fix applied:

- Model-facing partial-accept repairs, cde16 atempo=0.88 pacing, cde20-only final6b SBOM repair, Breeze-ASR-25 auxiliary ASR replacement, refreshed review log/matrix, and Downloads review package export.

Downloads package:

- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/
- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Stop rule:

- Do not run the 80-minute full render until cde01, cde16, and cde20 receive explicit human accept decisions and tools/check_breezyvoice_full_render_gate.py exits 0. Use Breeze-ASR-25 for any auxiliary ASR; do not use Whisper for current review gates.

Next action:

- Send refreshed Downloads review package to expert, ingest returned form, and either open the full-render gate or apply the next minimal repair.

Additional observations:

- An initial Whisper tiny final6b ASR command was run before the user clarified the ASR policy; it is archived as superseded and is not used for current review.
- Breeze-ASR-25 is still auxiliary only: it can flag term drift and repeated phrases, but human listening owns acceptance.
- GPU energy is a GPU-only nvidia-smi estimate and excludes CPU, storage, display, PSU loss, and monitor energy.

### EXP-20260528-17 - Mixed-gate final7 pilot repair with 白箱 terminology

- Timestamp: `2026-05-28T13:23:00+08:00`
- Stage: `final6b-human-review-repair-final7`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `cde_full_01_opening_positioning_crazyhunter_entry_case; cde_full_20_crowdstrike_update_524b; cde_full_26_shared_close_test_anchors`

Reason:

- Returned mixed review accepted cde16 but kept cde01, cde20, and cde26 blocked; user required the Chinese white-box term to use 白箱 before continuing; during rerender, runtime G2P printed internal zhuyin annotations, so manifest text cleanliness was verified before proceeding.

Hypothesis:

- Using 白箱 terminology, localizing risky cde20 technical terms, splitting cde01/cde26 more finely, preserving accepted cde16, and trimming the final closing tail should produce a cleaner human-review pilot while keeping the 80-minute full render gate closed.

Change summary:

- Chinese white-box terminology was standardized to 白箱 across tracked docs/tools and current model-facing inputs; a Unicode fallback normalizer converts legacy source wording to 白箱 before TTS. Final7 also applies cde01 trust-question/list cleanup, cde20 Crowd-Strike/Falcon/update-validator/supply-chain/524B/SBOM localization, cde26 life-cycle-trust/final trust-chain cleanup, and cde26 p24 0.8s tail trim.

Commands:

- prepare_breezyvoice_render_package; run_with_gpu_telemetry + breezyvoice_render_subclips for cde01/cde20/cde26 prompt-mode final7; trim_breezyvoice_audio_tail cde26_p24 0.8s; stitch_breezyvoice_outputs pilot/full; build_breezyvoice_pilot_review/render_review_log/pilot_correction_matrix; run_breeze_asr25 on stitched pilot; verify_breezyvoice_objective; check_breezyvoice_full_render_gate; export_breezyvoice_expert_review_package.

Logs:

- .local/breezyvoice/runtime/v1/pilot_reference_after_mixed_gate_repair_final7.log; .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_mixed_gate_repair_final7_summary.json; .local/breezyvoice/runtime/v1/telemetry/pilot_reference_after_mixed_gate_repair_final7_gpu.jsonl; .local/breezyvoice/review/v1/asr/breeze_asr25_after_mixed_gate_repair_final7.log; .local/breezyvoice/review/v1/objective_verification.json; .local/breezyvoice/review/v1/full_render_gate_check.json.

Outputs:

- .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-pilot-stitched-v1.wav; .local/breezyvoice/output/v1/parent_chunks; .local/breezyvoice/output/v1/subclips; .local/breezyvoice/review/v1/pilot_listening_review.csv; .local/breezyvoice/review/v1/pilot_correction_matrix.md; .local/breezyvoice/review/v1/asr/breeze_asr25_after_mixed_gate_repair_final7.json; Downloads review package.

Machine result:

- Final7 clean render completed 59 selected prompt-mode subclips on RTX 5080: elapsed_s=494.616, avg_gpu_power_w=178.116, estimated_gpu_energy_wh=24.471971, avg_gpu_utilization_pct=61.365, peak GPU memory=13852 MB. Breeze-ASR-25 auxiliary pass used cuda/RTX 5080: model_load_elapsed_s=3.136, asr_elapsed_s=42.729, chunk_count=215, text_characters=3738. Parent runtimes after stitching: cde01=237.48s/22, cde16=168.96s/9 accepted, cde20=167.19s/13, cde26=204.26s/24; stitched pilot duration=779.99s. Objective verifier exit 2 and full-render gate exit 2 because cde01/cde20/cde26 require fresh human listening; cde16 remains accepted.

Human result:

- Latest human state before this run: cde16 accepted; cde01, cde20, and cde26 require renewed human listening after final7 repairs.

Decision: `final7_exported_full_render_blocked_for_human_review`

Fix applied:

- 白箱 terminology standardization, legacy white-box fallback normalization, cde01/cde20/cde26 final7 rerender, cde26 tail trim, Breeze-ASR-25 auxiliary ASR, review package export.

Downloads package:

- /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/; /home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz

Stop rule:

- Stop here. Do not run the 80-minute full render until cde01, cde20, and cde26 are accepted by human listening review and tools/check_breezyvoice_full_render_gate.py exits 0.

Next action:

- Send the refreshed Downloads package to the expert; ingest the returned review CSV; only if every required pilot chunk is accepted should the full render gate open.

Additional observations:

- BreezyVoice/G2P prints internal annotations like [:ㄌㄜ4] in runtime stdout. The actual subclip manifest text was checked and is clean; keep this as a watch item for human listening, not as source-text leakage. Current auxiliary ASR policy was followed: Breeze-ASR-25 only; no Whisper was used.

### EXP-20260528-18 - Owner-overridden full render after final7 repair

- Timestamp: `2026-05-28T14:30:00+08:00`
- Stage: `owner-release-full-render-final7`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `all 26 parent chunks, 146 full-session subclips`

Reason:

- Owner instructed that after the current human-review repair run, no additional listening review is required before the next concrete step.
- Preserve the returned review history while opening the full render path through an explicit owner override rather than fake accept rows.

Hypothesis:

- A recorded owner override can move the project from pilot repair to full-session synthesis while preserving traceability and keeping all machine/human review evidence intact.
- Reference-audio prompt mode plus final7 text conditioning, cde16 pacing, and cde26 tail trim should produce a complete local deliverable for the next packaging step.

Change summary:

- Added explicit full-render owner override gate artifacts and checker support.
- Rendered all 146 subclips in prompt mode with the local reference audio on RTX 5080.
- Applied cde16 atempo=0.88 pacing and cde26 p24 0.8s tail trim before stitching.
- Stitched 26 parent chunks into the full 73.37-minute WAV and created a 22.05 kHz loudness-normalized copy.
- Ran auxiliary full-audio ASR with MediaTek-Research/Breeze-ASR-25 only; no Whisper ASR was used.
- Added future-facing normalization so white-box / White-box model inputs become 白箱 terms.

Commands:

- python3 tools/open_breezyvoice_full_render_gate.py --reason <owner instruction>
- python3 tools/check_breezyvoice_full_render_gate.py --write-report
- tools/run_with_gpu_telemetry.py --summary-json .local/breezyvoice/runtime/v1/telemetry/full_reference_after_owner_release_final7_summary.json -- breezyvoice_render_subclips.py --selection all --voice-mode prompt --overwrite
- python3 tools/apply_breezyvoice_audio_pacing.py --parent-prefix cde_full_16_k8s_review_controls --tempo 0.88 --label 20260528-full-owner-release-final7 --overwrite
- python3 tools/trim_breezyvoice_audio_tail.py --subclip-id cde_full_26_shared_close_test_anchors_p24 --tail-seconds 0.8 --label 20260528-full-owner-release-final7 --overwrite
- python3 tools/stitch_breezyvoice_outputs.py --selection all --stitch-full --full-output .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-80min-v1.wav --overwrite --silence-ms 350
- tools/run_with_gpu_telemetry.py --summary-json .local/breezyvoice/runtime/v1/telemetry/asr_breeze25_full_owner_release_final7_summary.json -- tools/run_breeze_asr25.py --audio .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-80min-v1.wav
- ffmpeg -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 22050 .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-80min-v1.loudnorm-22050.wav
- python3 tools/verify_breezyvoice_objective.py --write-report

Logs:

- .local/breezyvoice/runtime/v1/full_reference_after_owner_release_final7.log
- .local/breezyvoice/runtime/v1/telemetry/full_reference_after_owner_release_final7_summary.json
- .local/breezyvoice/runtime/v1/telemetry/full_reference_after_owner_release_final7_gpu.jsonl
- .local/breezyvoice/runtime/v1/asr_breeze25_full_owner_release_final7.stdout.log
- .local/breezyvoice/runtime/v1/telemetry/asr_breeze25_full_owner_release_final7_summary.json
- .local/breezyvoice/runtime/v1/telemetry/asr_breeze25_full_owner_release_final7_gpu.jsonl
- .local/breezyvoice/runtime/v1/loudnorm_22050_full_owner_release_final7.ffmpeg.log
- .local/breezyvoice/review/v1/objective_verification.json
- .local/breezyvoice/review/v1/full_render_gate_check.json

Outputs:

- .local/breezyvoice/output/v1/subclips
- .local/breezyvoice/output/v1/parent_chunks
- .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-80min-v1.wav
- .local/breezyvoice/output/v1/full/cde-2026-breezyvoice-80min-v1.loudnorm-22050.wav
- .local/breezyvoice/review/v1/asr/cde-2026-breezyvoice-80min-v1.txt
- .local/breezyvoice/review/v1/asr/breeze_asr25_full_owner_release_final7.json
- .local/breezyvoice/review/v1/all_stitch_summary.json

Machine result:

- Full render exit_code=0; selected/rendered 146 prompt-mode subclips; elapsed_s=2696.62; avg_gpu_power_w=225.037; estimated_gpu_energy_wh=168.566734; avg_gpu_utilization_pct=74.17; max_gpu_memory_used_mb=15636.
- Full stitch exit_code=0; parent_count=26; full duration=4402.124s (73.37min); raw SHA256=0b7b85f9df3673a56a15143ffa90ddf5a324ad529b5c76aaeacea8c2d4288545.
- Breeze-ASR-25 auxiliary pass exit_code=0 on CUDA RTX 5080; total elapsed_s=236.101; model_load_elapsed_s=3.256; asr_elapsed_s=230.569; text_characters=26677; chunk_count=1297; avg_gpu_power_w=150.007; estimated_gpu_energy_wh=9.838006; max_gpu_memory_used_mb=6388.
- Loudnorm 22.05kHz copy completed in 35.14s; SHA256=917592bce31027911509865bb7dd484a4a67bff9ac08a4252f4cc9d8589212f6.
- Objective verifier exit 0 with overall_status=complete; full-render gate checker exit 0 with accepted_by_owner_override=true.

Human result:

- Latest owner instruction: after this human-review repair run, do not run another review round; proceed to the next concrete step.
- Returned expert review history remains preserved; no rows were converted to artificial accept decisions.

Decision: `full_render_completed_owner_release_post_render_logging`

Fix applied:

- Owner override gate; full prompt-mode render; cde16 pacing override; cde26 tail trim; all-parent stitch; Breeze-ASR-25 full auxiliary ASR; 22.05kHz loudness-normalized copy; future white-box to 白箱 normalization.

Downloads package:

- none for this step; generated audio remains local-only under .local/breezyvoice unless explicitly exported.

Stop rule:

- No further human review is required for this owner-release step.
- Do not treat Breeze-ASR-25 output as acceptance; use it only as a warning signal for future revisions.
- Before any future rerender, keep 白箱 terminology and no hesitant filler policy active.

Next action:

- Prepare the deliverable package or handoff copy from the full WAV and loudnorm copy; use Breeze-ASR-25 transcript only to prioritize future repair candidates.

Additional observations:

- The full stitched audio is 73.37 minutes, shorter than the 80-minute target because the generated 146 subclips synthesize faster than the stochastic timing plan.
- Energy estimates are GPU-only nvidia-smi power.draw estimates and exclude CPU, display, storage, PSU loss, and monitor energy.
- BreezyVoice/G2P runtime stdout prints internal zhuyin annotations; these are runtime diagnostics, not source-text leakage.
- Breeze-ASR-25 uses a WhisperTokenizer internally in Transformers, but the ASR model executed was MediaTek-Research/Breeze-ASR-25; no Whisper ASR command was used.

### EXP-20260528-23 - Set v3 delivery target to 70 minutes and story-condition case passages

- Timestamp: `2026-05-28T17:58:00+08:00`
- Stage: `v3-text-conditioning-policy`
- Input version: `v1`
- Source SHA-256: `05c4d43c6d60015bec302f73e0b01b8fef00270992e1b6294363d67b3caf6cdc`
- Affected prefixes: `all; cde_full_17_tesla_k8s_case; cde_full_20_crowdstrike_update_524b; cde_full_24_logging_synnovis_start`

Reason:

- Owner changed full-session TTS delivery target to approximately 70 minutes; case passages should feel like a concrete story shared with listeners in Taiwan Traditional Chinese.

Hypothesis:

- A single post-stitch tempo normalization to 4200 seconds preserves consistent whole-audio pacing better than section-by-section speed changes. Story-conditioned case passages reduce TTS instability caused by dense English technical lists.

Change summary:

- Updated repo and global TTS rules for 70-minute delivery target; added case-story text conditioning; preserved token and namespace as English technical terms; regenerated v1/v3 manifests from current model-facing text.

Commands:

- python3 -m py_compile tools/prepare_breezyvoice_render_package.py; python3 tools/prepare_breezyvoice_render_package.py; rebuilt .local/breezyvoice/manifests/v3 from current v1 manifests

Logs:

- .local/breezyvoice/runtime/v3/prepare_for_v3_70min_story_rule_r4.log

Outputs:

- .local/breezyvoice/manifests/v3/subclip_manifest.csv; .local/breezyvoice/inputs/v1/subclips

Machine result:

- Package preparation completed; current v3 manifest has 116 subclips; case passages were inspected in model-facing text; no render executed yet for this policy step.

Human result:

- Owner instructed to target about 70 minutes and make case passages feel like story sharing for listeners.

Decision: `proceed_to_v3_smoke_then_full_render`

Fix applied:

- Repo/global rule update; delivery target set to 70 minutes; final case-story polish added after CJK-English boundary punctuation; v3 manifest refreshed.

Downloads package:

- none recorded

Stop rule:

- No additional human review round is required by current owner instruction; after full render, apply one global tempo factor raw_duration_seconds / 4200, then loudness normalize and run Breeze-ASR-25 only as auxiliary warning signal.

Next action:

- Run v3 prompt-mode smoke on RTX 5080, then full render, stitch, normalize to approximately 70 minutes, loudness normalize, and run Breeze-ASR-25.

Additional observations:

- The 80-minute engineering source remains the frozen traceability source; the delivery master target is now the 70-minute post-processed audio.

## EXP-20260528-24 — v3 70-minute full render with ConvNet reference prompt and story-conditioned case passages

Timestamp: `2026-05-28T19:45:00+08:00`

Stage: `v3-full-render-70min-final`

Decision: `completed_local_70min_master_with_asr_warning_notes`

Reason:

- Owner changed the full-session delivery target from the prior 80-minute planning target to approximately 70 minutes.
- Case passages should sound like a concrete story shared with listeners, while general TTS wording should prefer Taiwan Traditional Chinese except preserved technical terms such as `token` and `namespace`.
- The whole file should use one consistent pacing transform rather than per-section speed changes.

Hypothesis:

- A representative 28-second prompt extracted from `深度捲積神經網路.mp4`, plus story-conditioned model text and a single post-stitch tempo normalization to 4200 seconds, can produce a stable full-session v3 master while preserving consistent whole-file pacing.

Fix applied:

- Added repo/global rules for 70-minute delivery, case-story phrasing, Taiwan Traditional Chinese TTS wording, CJK/English `、` boundaries, repeat deletion, and `token`/`namespace` preservation.
- Rebuilt v3 manifests from the current model-facing text.
- Rendered all v3 subclips with prompt voice mode on RTX 5080.
- Reran 56 repair subclips, then smaller late-fix selections for ordinary-English remnants and repeated phrases.
- Re-stitched after the final subclip fixes, then applied one global `atempo=0.827687993` transform to reach 70:00.
- Produced a loudness-normalized 22.05 kHz mono WAV.
- Ran auxiliary ASR with `MediaTek-Research/Breeze-ASR-25` only; no Whisper ASR command was used.

Commands:

- `python3 -m py_compile tools/prepare_breezyvoice_render_package.py`
- `python3 tools/prepare_breezyvoice_render_package.py`
- `tools/run_with_gpu_telemetry.py ... tools/breezyvoice_render_subclips.py --version v3 --selection all --voice-mode prompt ...`
- `tools/run_with_gpu_telemetry.py ... tools/breezyvoice_render_subclips.py --subclip-manifest .local/breezyvoice/manifests/v3/subclip_manifest_finalrepair_selection.csv ...`
- `tools/run_with_gpu_telemetry.py ... tools/breezyvoice_render_subclips.py --subclip-manifest .local/breezyvoice/manifests/v3/subclip_manifest_latefix2_selection.csv ...`
- `tools/run_with_gpu_telemetry.py ... tools/breezyvoice_render_subclips.py --subclip-manifest .local/breezyvoice/manifests/v3/subclip_manifest_dashboardfix_selection.csv ...`
- `tools/run_with_gpu_telemetry.py ... tools/breezyvoice_render_subclips.py --subclip-manifest .local/breezyvoice/manifests/v3/subclip_manifest_p08procedures_fix_selection.csv ...`
- `python3 tools/stitch_breezyvoice_outputs.py --version v3 --selection all --stitch-full --full-output .local/breezyvoice/output/v3/full/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.raw.wav --overwrite --silence-ms 350`
- `ffmpeg -filter:a atempo=0.827687993`
- `ffmpeg -af loudnorm=I=-16:TP=-1.5:LRA=11 -ar 22050`
- `tools/run_with_gpu_telemetry.py ... tools/run_breeze_asr25.py --audio .local/breezyvoice/output/v3/full/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.loudnorm-22050.wav ...`

Logs:

- `.local/breezyvoice/runtime/v3/full_convnet_70min_story_v3.log`
- `.local/breezyvoice/runtime/v3/finalrepair_convnet_70min_story_v3.log`
- `.local/breezyvoice/runtime/v3/latefix2_convnet_70min_story_v3.log`
- `.local/breezyvoice/runtime/v3/dashboardfix_convnet_70min_story_v3.log`
- `.local/breezyvoice/runtime/v3/p08proceduresfix_convnet_70min_story_v3.log`
- `.local/breezyvoice/runtime/v3/pacing_to_70min_v3.final.ffmpeg.log`
- `.local/breezyvoice/runtime/v3/loudnorm_70min_v3.final.ffmpeg.log`
- `.local/breezyvoice/runtime/v3/asr_breeze25_full_70min_v3_final.stdout.log`
- `.local/breezyvoice/runtime/v3/telemetry/asr_breeze25_full_70min_v3_final_summary.json`

Outputs:

- `.local/breezyvoice/output/v3/full/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.raw.wav`
- `.local/breezyvoice/output/v3/full/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.wav`
- `.local/breezyvoice/output/v3/full/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.loudnorm-22050.wav`
- `.local/breezyvoice/review/v3/asr/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.loudnorm-22050.final.breeze-asr-25.txt`
- `.local/breezyvoice/review/v3/asr/breeze_asr25_full_70min_v3_final.json`
- `.local/breezyvoice/review/v3/asr/breeze_asr25_full_70min_v3_final_timestamped.txt`

Machine result:

- Full render: `3177.503s`, `exit_code=0`, selected all v3 subclips, avg GPU power `229.422W`, estimated GPU energy `202.496971Wh`, avg GPU utilization `78.244%`, peak GPU memory `9999MB`.
- Main repair render: `1714.637s`, `exit_code=0`, 56 selected subclips, avg GPU power `231.624W`, estimated GPU energy `110.319859Wh`, avg GPU utilization `77.073%`, peak GPU memory `10480MB`.
- Late-fix render: `108.401s`, estimated GPU energy `6.689618Wh`.
- Dashboard-fix render: `109.175s`, estimated GPU energy `6.799862Wh`.
- p08 procedures-fix render: `58.695s`, estimated GPU energy `3.355616Wh`.
- Final raw stitch duration: `3476.290s` / `57.938min`, SHA256 `fce051da255142a4d8e1ea45efeb559ff288b01485ba59c1559fa927a5a286c0`.
- Final tempo-adjusted duration: `4199.983s` / `70.000min`, SHA256 `3a0b9e8dc9aec85c69e4703713cddaec70bd96db130733460c822e014eac1905`.
- Final loudness-normalized duration: `4199.983s` / `70.000min`, SHA256 `1acf46ee68199c0ed2e396ec5bcf0046f5dcb22dd245b2c8d761cabd17dabb7d`.
- Final Breeze-ASR-25 auxiliary pass: `242.634s`, model load `3.124s`, ASR `237.223s`, `1060` chunks, `17478` text characters, avg GPU power `150.652W`, estimated GPU energy `10.153708Wh`, peak GPU memory `6523MB`.
- Observable GPU-only energy for the retained final-render path and required repair/ASR passes is approximately `339.82Wh`. This excludes CPU, storage, PSU loss, display, and monitor energy.

Human result:

- No additional human review round was requested at this step.
- The current output is a local v3 full-session deliverable candidate, not an expert-accepted final publication master.

ASR warning result:

- Breeze-ASR-25 found no `白盒`, no `那個`, no `吱吱嗚嗚`, no `媽媽`, no `老能`, no `哈哈哈`, and no direct repeated strings for `剩餘風險剩餘風險`, `控制證據控制證據`, or `發現事項發現事項`.
- Breeze-ASR-25 still reports `dashboard` once and `這個` seven times. Manual interpretation is required because ASR also shows obvious recognition drift around dense K8S and case passages; this is a warning signal, not an acceptance decision.

Additional observations:

- The raw render was shorter than the target. The post-stitch tempo factor slowed the whole master from `57.938min` to exactly `70.000min`, keeping pacing globally consistent.
- The Transformers warning mentioning `WhisperTokenizer` comes from Breeze-ASR-25 internals; the executed ASR model was `MediaTek-Research/Breeze-ASR-25`.
- Some runtime stdout still prints internal G2P zhuyin annotations. The model-facing manifest text is clean; these annotations are runtime diagnostics.

Next action:

- If the user wants a handoff package, package the loudness-normalized 70-minute WAV with the corresponding model-facing transcript and Breeze-ASR-25 transcript.
- If future quality repair is requested, start from the ASR warning regions around K8S/Tesla and 524B/SBOM sections and rerender only those affected subclips.

Stop rule:

- Do not start another human-review cycle unless the user requests it.
- Do not use Whisper for auxiliary ASR in this project; continue using Breeze-ASR-25 only.

## EXP-20260528-25 — Wu teacher reference package with M4A and transcript

Timestamp: `2026-05-28T20:28:00+08:00`

Stage: `v3-wu-teacher-handoff-package`

Decision: `downloads_handoff_package_created`

Reason:

- Owner requested a reference package for Wu teacher containing the `cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.wav` audio converted to M4A and placed together with the transcript.
- This is a handoff/export step only; no new TTS generation and no new human review cycle were requested.

Fix applied:

- Converted the specified v3 target-70min WAV to M4A with AAC audio.
- Assembled the model-facing TTS transcript from the v3 subclip manifest in render order.
- Included the Breeze-ASR-25 auxiliary transcript as a warning-signal reference, not as acceptance authority.
- Added package metadata, SHA256 checksums, and the ffmpeg conversion log.
- Created both a folder and a compressed tarball in `Downloads`.

Commands:

- `ffmpeg -y -i .local/breezyvoice/output/v3/full/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.wav -c:a aac -b:a 128k -movflags +faststart /home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.m4a`
- `ffprobe -v error -show_entries format=duration,size,bit_rate -of json /home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.m4a`
- `tar -czf /home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28.tar.gz -C /home/jnln3799/Downloads cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28`

Logs:

- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/ffmpeg_m4a_conversion.log`

Outputs:

- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/`
- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28.tar.gz`
- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.m4a`
- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/cde-2026-breezyvoice-v3-model-facing-transcript-zh-tw.md`
- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/cde-2026-breezyvoice-v3-model-facing-transcript-zh-tw.txt`
- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/auxiliary-breeze-asr-25-transcript-warning-signal.txt`
- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/README_FOR_WU_TEACHER.md`
- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/package_metadata.json`
- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/SHA256SUMS.txt`

Machine result:

- Source WAV duration: `4199.983s` / `70.000min`; SHA256 `3a0b9e8dc9aec85c69e4703713cddaec70bd96db130733460c822e014eac1905`.
- M4A duration: `4199.983s` / `70.000min`; size `43565886` bytes; reported bit rate `82982`; SHA256 `09d7043190d2285f39fffecac3ff7605c0a246581f93e5925bad9430da7eec86`.
- Package archive size: approximately `42M`.
- No GPU generation or ASR pass was run for this package step.

Human result:

- No new human review was requested or initiated.
- Package is a stakeholder reference/handoff copy for Wu teacher.

Additional observations:

- The package uses the non-loudness-normalized `target-70min.wav` requested by the owner, converted to M4A.
- The included model-facing transcript is the authoritative text used for TTS conditioning; the included Breeze-ASR-25 transcript is only a warning signal for future repair.

Next action:

- Share the folder or tarball with Wu teacher.

Stop rule:

- Do not start another human-review cycle unless the owner requests it.
- Do not use Whisper for auxiliary ASR in this project; continue using Breeze-ASR-25 only.

## EXP-20260528-26 — Wu teacher package 0.9x M4A listening copy

Timestamp: `2026-05-28T20:35:00+08:00`

Stage: `v3-wu-teacher-handoff-postprocess`

Decision: `downloads_handoff_package_updated`

Reason:

- Owner requested the TTS audio already stored in the Downloads handoff package be post-processed once more at `0.9x` speed.
- Longer audio duration is acceptable, and the original audio should remain preserved.

Fix applied:

- Preserved the original `target-70min.m4a`.
- Created a new `target-70min.0_9x.m4a` copy using ffmpeg `atempo=0.9`.
- Updated the handoff README, package metadata, checksum file, and tar.gz archive.

Commands:

- `ffmpeg -y -i /home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.m4a -filter:a atempo=0.9 -c:a aac -b:a 128k -movflags +faststart /home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.0_9x.m4a`
- `ffprobe -v error -show_entries format=duration,size,bit_rate -of json /home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.0_9x.m4a`
- `tar -czf /home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28.tar.gz -C /home/jnln3799/Downloads cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28`

Logs:

- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/ffmpeg_m4a_0_9x_conversion.log`

Outputs:

- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28/cde-2026-breezyvoice-v3-convnet-reference-zh-tw-story.target-70min.0_9x.m4a`
- `/home/jnln3799/Downloads/cde-2026-breezyvoice-v3-wu-teacher-reference-package-2026-05-28.tar.gz`

Machine result:

- Input M4A duration: `4199.983s` / `70.000min`.
- 0.9x M4A duration: `4666.670s` / `77.778min`; size `47742788` bytes; reported bit rate `81844`; SHA256 `bf5d631363d3add989895fc441e45b91dc2f852682c9f58a5b13a1003eca7799`.
- Updated tar.gz package size: approximately `87M`.
- No GPU generation and no ASR pass were run for this post-processing step.

Human result:

- No new human review was requested or initiated.
- This is a slower stakeholder listening copy in the same Downloads package.

Additional observations:

- `atempo=0.9` slows playback and lengthens the audio while preserving pitch better than simple sample-rate reinterpretation.
- The original M4A remains available in the package for comparison.

Next action:

- Use the `0_9x.m4a` file when a slower listening reference is preferred.

Stop rule:

- Do not start another human-review cycle unless the owner requests it.
- Do not use Whisper for auxiliary ASR in this project; continue using Breeze-ASR-25 only.
