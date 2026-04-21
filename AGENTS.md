# AGENTS.md

This repository is the canonical CYBERSEC 2026 AI SaMD talk delivery package.

It keeps the public talk, compact deck, script, scoring system, rehearsal loop, and generated presentation outputs separate from daily planning, course grading, and private source material.

## Mission

Maintain a clear, credible, reusable talk package for:

- talk design and audience promise
- compact slide structure
- speakable stage language
- scoring and slide gates
- rehearsal and repair
- generated markdown, CSV, and deck outputs

## Non-goals

Do not turn this repo into:

- a personal planning system
- a course grading archive
- a general cybersecurity notebook
- a raw source dump
- an exploit cookbook
- a storage place for private hospital, client, student, credential, or patent-sensitive material

## First-Principles Boundary

Use this routing rule:

```text
planning-everything-track = why / when / priority / status / capacity
cybersec-2026-ai-samd-talk = what the talk says / shows / scores / rehearses
```

The planning repo may link to this repo for project context. This repo should not duplicate the planning system.

## Canonical Object Model

| Object | Canonical location | Rule |
| --- | --- | --- |
| repo purpose and workflow | `README.md` | Human routing and current delivery promise |
| talk design and stage script | `docs/01_talk_design.md` | Owns audience promise, slide spine, timing, script, and build path |
| scoring and slide gates | `docs/02_evaluation_system.md` | Owns macro rubric, hard slide constraints, penalties, and generated evaluation outputs |
| rehearsal workflow | `docs/03_rehearsal_workflow.md` | Owns dry-run checkpoints, repair order, and readiness |
| structured source | `data/presentation_os.json` | Source of generated operating outputs and deck content |
| generated reports | `outputs/current/` | Rebuildable from structured source |
| generated deck | `outputs/deck/` | Rebuildable presentation artifact |
| generators | `tools/` | Keep commands documented and reproducible |
| local heavy/private work | `.local/` or ignored paths | Do not commit unless explicitly safe |

## Working Rules

1. Preserve one canonical source.
   - If changing generated reports, update `data/presentation_os.json` or the generator first.
   - Do not treat generated files as independent live sources unless `README.md` explicitly says so.

2. Keep the talk package public-safe.
   - Exclude proprietary code, raw student records, private hospital/client detail, credentials, exploit-ready private instructions, and patent-sensitive implementation mechanics.

3. Keep the deck compact.
   - The active talk target is the compact `14`-slide package unless `README.md` or the project owner changes that decision.

4. Maintain traceability.
   - Talk design, evaluation, rehearsal workflow, generated reports, and deck output should stay mutually consistent.
   - If the canonical file set or workflow changes, update `README.md` and the planning handoff.

5. Use relative repo paths where possible.
   - Absolute local paths are allowed only as clearly labeled machine-specific examples.

6. Keep generated artifacts reproducible.
   - When changing generator behavior, run the relevant generation command and inspect outputs.

7. Keep edits small and operational.
   - Prefer a focused correction to a broad redesign unless the current structure blocks work.

## Recommended Workflow

1. Read `README.md` for the current package promise.
2. Read `docs/01_talk_design.md` before changing narrative, slides, timing, or script.
3. Edit `data/presentation_os.json` when generated reports or deck content should change.
4. Regenerate outputs with:

```bash
python3 tools/generate_presentation_outputs.py
```

5. Build the editable deck when needed with:

```bash
node tools/build_optimized_deck.mjs
```

This requires `@oai/artifact-tool` in the active Node environment.

6. Use `docs/02_evaluation_system.md` before timed rehearsal.
7. Use `docs/03_rehearsal_workflow.md` to score, repair, and decide readiness.
8. Update the planning repo only with project status, handoff links, and reusable lessons.

## Cross-Repo Rule

When unsure where something belongs, classify it before moving it:

| Question | Route |
| --- | --- |
| Is it a deadline, status, capacity decision, or weekly task? | Planning repo |
| Is it talk strategy, script, deck design, or rehearsal evidence? | This repo |
| Is it reusable cybersecurity knowledge? | Planning repo `data/knowledge/cybersecurity/` after promotion |
| Is it course handout or lecture study material? | Course study repo |
| Is it private or sensitive raw material? | Do not commit; use a local excluded path |

The simplest correct home wins.
