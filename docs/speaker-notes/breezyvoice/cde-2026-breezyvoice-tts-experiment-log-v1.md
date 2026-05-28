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
- Current state: pilot rendered and stitched; full render is closed.
- Current blocker: four pilot parent chunks still require accepted human
  listening decisions after expert-conditioning rerender.
- Current review package:
  `/home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28/`
- Current review archive:
  `/home/jnln3799/Downloads/cde-2026-breezyvoice-pilot-review-package-2026-05-28.tar.gz`

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
| `EXP-20260528-12` | pilot-repair-rerender | Round-2 pilot rerender after all-reject contamination review | round2_pilot_rendered_stop_for_human_review | Export refreshed Downloads package and wait for round-2 human listening review |

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
