#!/usr/bin/env python3
"""Generate CYBERSEC 2026 presentation operating-system outputs.

The generator is deterministic and uses only the Python standard library.
It treats data/presentation_os.json as the single source of truth for the
strategy report, slide blueprint, evaluation report, constraint report,
optimization plan, and CSV review artifacts.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DATA_PATH = ROOT / "data" / "presentation_os.json"
OUT_DIR = ROOT / "outputs" / "current"

SCORING_HEADERS = [
    "Category",
    "Score",
    "MaxScore",
    "Strengths",
    "Weaknesses",
    "Evidence",
]
SLIDE_HEADERS = ["SlideID", "PassFail", "Violations", "Severity"]


def load_data() -> dict:
    with DATA_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def fmt_seconds(seconds: int) -> str:
    minutes, rem = divmod(seconds, 60)
    return f"{minutes}:{rem:02d}"


def md_table_cell(value: object) -> str:
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def table(headers: Iterable[str], rows: Iterable[Iterable[object]]) -> str:
    header_list = [md_table_cell(h) for h in headers]
    lines = [
        "| " + " | ".join(header_list) + " |",
        "| " + " | ".join("---" for _ in header_list) + " |",
    ]
    for row in rows:
        cells = [md_table_cell(cell) for cell in row]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


def bullet(items: Iterable[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def numbered(items: Iterable[str]) -> str:
    return "\n".join(f"{idx}. {item}" for idx, item in enumerate(items, 1))


def validate(data: dict) -> None:
    slides = data["slides"]
    if len(slides) != data["metadata"]["active_slide_count"]:
        raise ValueError("slide count must equal metadata.active_slide_count")

    timing_total = sum(int(slide["speaking_seconds"]) for slide in slides)
    if timing_total != data["metadata"]["content_seconds"]:
        raise ValueError(f"slide timing total must be 1710 seconds, got {timing_total}")

    score_total = sum(int(category["max_score"]) for category in data["scoring_categories"])
    if score_total != 100:
        raise ValueError(f"scoring category max points must total 100, got {score_total}")

    baseline_total = sum(int(category["baseline_score"]) for category in data["scoring_categories"])
    optimized_total = sum(int(category["optimized_score"]) for category in data["scoring_categories"])
    summary = data["score_summary"]
    if baseline_total != summary["baseline_macro_score"]:
        raise ValueError("baseline category scores do not match score_summary")
    if optimized_total != summary["optimized_macro_score"]:
        raise ValueError("optimized category scores do not match score_summary")

    for slide in slides:
        if slide["layout_type"] not in data["constraint_system"]["allowed_layouts"]:
            raise ValueError(f"slide {slide['id']} has invalid layout type")
        if not slide["rubric_categories"]:
            raise ValueError(f"slide {slide['id']} must map to at least one rubric category")

    if SCORING_HEADERS != ["Category", "Score", "MaxScore", "Strengths", "Weaknesses", "Evidence"]:
        raise ValueError("scoring CSV headers changed")
    if SLIDE_HEADERS != ["SlideID", "PassFail", "Violations", "Severity"]:
        raise ValueError("slide CSV headers changed")


def render_main_strategy(data: dict) -> str:
    brief = data["brief"]
    metadata = data["metadata"]
    timing = data["time_architecture"]
    summary = data["score_summary"]
    lines: list[str] = [
        "# CYBERSEC 2026 Presentation Operating System",
        "",
        f"Canonical topic: `{metadata['canonical_topic']}`",
        "",
        "This generated strategy file turns the existing compact CYBERSEC talk into a reusable operating system. The macro speech rubric stays at `100` points; the slide constraint layer is a separate pass/fail and penalty gate; the optimization loop repairs the highest-leverage failures before rehearsal.",
        "",
        "## 1. Engine Architecture",
        "",
        table(
            ["Engine", "Operating Role"],
            [(engine["name"], engine["function"]) for engine in data["engines"]],
        ),
        "",
        "## 2. Presentation Brief",
        "",
        table(
            ["Field", "Decision"],
            [
                ("Recommended title", brief["recommended_title"]),
                ("Positioning", brief["positioning"]),
                ("Core thesis", brief["core_thesis"]),
                ("Why this matters now", brief["why_now"]),
                ("Speaker authority angle", brief["speaker_authority_angle"]),
                ("Differentiator", brief["differentiator"]),
                ("Active deck", f"{metadata['active_slide_count']} slides, {metadata['content_time']} content plus {metadata['buffer_time']} buffer"),
                ("Language policy", metadata["language_policy"]),
            ],
        ),
        "",
        "### Title Candidates",
        "",
        numbered(brief["title_candidates"]),
        "",
        "### Intended Audience",
        "",
        bullet(brief["audience_segments"]),
        "",
        "### Audience Assumptions",
        "",
        bullet(brief["audience_assumptions"]),
        "",
        "### Audience Pain Points",
        "",
        bullet(brief["pain_points"]),
        "",
        "### Desired Takeaways",
        "",
        bullet(brief["desired_takeaways"]),
        "",
        "### Risk Factors And Mitigations",
        "",
        table(
            ["Risk Factor", "Mitigation"],
            zip(brief["risk_factors"], brief["risk_mitigations"]),
        ),
        "",
        "## 3. Rubric-To-Design Translation Matrix",
        "",
        table(
            [
                "Category",
                "Points",
                "Design Goal",
                "Observable Success",
                "Tactics",
                "Failure Pattern",
                "Avoid",
                "Slide Influence",
                "Speaking Influence",
            ],
            [
                (
                    item["category"],
                    item["points"],
                    item["design_goal"],
                    item["observable_success"],
                    item["tactics"],
                    item["failure_patterns"],
                    item["avoid"],
                    item["slide_influence"],
                    item["speaking_influence"],
                )
                for item in data["rubric_translation"]
            ],
        ),
        "",
        "## 4. 30-Minute Time Architecture",
        "",
        f"Normal target: `{timing['normal']['target']}` content plus `{timing['normal']['buffer']}` buffer.",
        "",
        table(
            ["Slide Range", "Time", "Function", "Load"],
            [
                (segment["slides"], segment["time"], segment["function"], segment["load"])
                for segment in timing["normal"]["segments"]
            ],
        ),
        "",
        "### Timing Variants",
        "",
        table(
            ["Mode", "Target", "Rule"],
            [(variant["name"], variant["target"], variant["rules"]) for variant in timing["variants"]],
        ),
        "",
        "### Attention Drop Prediction",
        "",
        table(
            ["Risk Point", "Why Attention Drops", "Recovery Strategy"],
            [
                (risk["risk_point"], risk["why"], risk["recovery"])
                for risk in timing["attention_drops"]
            ],
        ),
        "",
        "## 5. Narrative Architecture",
        "",
        table(
            ["Narrative Field", "Decision"],
            [
                ("Mode", data["narrative"]["mode"]),
                ("Why this mode", data["narrative"]["why_this_mode"]),
                ("Opening hook", data["narrative"]["opening_hook"]),
                ("Problem framing", data["narrative"]["problem_framing"]),
                ("Tension", data["narrative"]["tension"]),
                ("Climax", data["narrative"]["climax"]),
                ("Closing structure", data["narrative"]["closing_structure"]),
                ("Final takeaway", data["narrative"]["final_takeaway"]),
            ],
        ),
        "",
        "### Development Arc",
        "",
        bullet(data["narrative"]["development_arc"]),
        "",
        "## 6. Visual Strategy",
        "",
        table(
            ["Rule", "Production Meaning", "Rubric Protected"],
            [
                ("One dominant object", "Each slide must be a phrase, ladder, chain, stack, contrast, flow, or roadmap.", "Visual Design"),
                ("Color carries semantics", "Use the primary accent for evidence/decision and risk color only for interruption or unresolved exposure.", "Visual Design"),
                ("Technical detail becomes labels", "Regulatory and testing substance appears as diagram labels; the explanation belongs in stage speech.", "Content Depth and Value"),
                ("Memory slides breathe", "Slides 3, 10, 12, and 14 use stillness and negative space.", "Audience Impact"),
                ("Public-safe examples only", "No private, proprietary, exploit, or patent-sensitive content appears on screen.", "Stage Presence"),
            ],
        ),
        "",
        "## 7. Audience Impact Design",
        "",
        table(
            ["Moment", "Audience Reaction To Create", "Design Action"],
            [
                ("First minute", "This is not an AI hype talk.", "Open on `你賣的不是模型` after the required compliance beat."),
                ("Slide 5", "I can locate my product on this map.", "Use four scales and evidence growth."),
                ("Slide 6", "Regulation is traceability, not paperwork.", "Show the evidence chain instead of legal text."),
                ("Slide 10", "This connects to patient safety.", "Use a standalone phrase and silence."),
                ("Slide 12", "This is the operating mechanism we need.", "Make Decision the largest node."),
                ("Final minute", "I know the next move.", "Use 30 / 60 / 90 and close on trust-before-audit."),
            ],
        ),
        "",
        "## 8. Score Model",
        "",
        table(
            ["Metric", "Value"],
            [
                ("Baseline macro score", summary["baseline_macro_score"]),
                ("Baseline slide penalty", summary["baseline_slide_penalty"]),
                ("Baseline adjusted score", summary["baseline_adjusted_score"]),
                ("Optimized macro score", summary["optimized_macro_score"]),
                ("Optimized slide penalty", summary["optimized_slide_penalty"]),
                ("Optimized multiplier", summary["optimized_multiplier"]),
                ("Optimized adjusted score", summary["optimized_adjusted_score"]),
                ("Improvement", f"+{summary['improvement']}"),
            ],
        ),
        "",
        "## 9. Source Anchors",
        "",
        table(
            ["Source", "Anchor"],
            [
                (source["label"], source.get("url") or source.get("path"))
                for source in data["source_anchors"]
            ],
        ),
        "",
    ]
    return "\n".join(lines)


def render_slide_blueprint(data: dict) -> str:
    lines = [
        "# Slide Blueprint",
        "",
        "This generated blueprint is the active 14-slide CYBERSEC 2026 target. Slide 2 is preserved as the required CYBERSEC disclaimer and functions as a compliance beat, not narrative content.",
        "",
        "## Timing Summary",
        "",
        table(
            ["Slide", "Title", "Time", "Layout", "Rubric Support"],
            [
                (
                    slide["id"],
                    slide["title"],
                    fmt_seconds(int(slide["speaking_seconds"])),
                    slide["layout_type"],
                    ", ".join(slide["rubric_categories"]),
                )
                for slide in data["slides"]
            ],
        ),
        "",
    ]
    cumulative = 0
    for slide in data["slides"]:
        cumulative += int(slide["speaking_seconds"])
        lines.extend(
            [
                f"## Slide {slide['id']}. {slide['title']}",
                "",
                table(
                    ["Field", "Blueprint"],
                    [
                        ("Slide objective", slide["message"]),
                        ("One-sentence message", slide["message"]),
                        ("Audience understanding", slide["audience_understanding"]),
                        ("Recommended visual form", slide["layout_type"]),
                        ("Visual concept", slide["visual_concept"]),
                        ("On-screen content", "<br>".join(slide["onscreen"])),
                        ("What must not appear", "<br>".join(slide["must_not_show"])),
                        ("Speaking time", f"{fmt_seconds(int(slide['speaking_seconds']))} (cumulative {fmt_seconds(cumulative)})"),
                        ("Transition in", slide["transition_in"]),
                        ("Transition out", slide["transition_out"]),
                        ("Supported rubric categories", ", ".join(slide["rubric_categories"])),
                        ("Stage cue", slide["speaker_note"]),
                    ],
                ),
                "",
            ]
        )
    return "\n".join(lines)


def render_evaluation_report(data: dict) -> str:
    summary = data["score_summary"]
    rows = []
    for category in data["scoring_categories"]:
        rows.append(
            (
                category["category"],
                f"{category['baseline_score']} -> {category['optimized_score']}",
                category["max_score"],
                category["strengths"],
                category["weaknesses"],
                category["evidence"],
            )
        )
    lines = [
        "# Evaluation Report",
        "",
        "The macro score is evaluated first on the `100`-point speech rubric. Slide penalties and the optional slide-quality multiplier are applied afterward so slide execution does not hide narrative or delivery problems.",
        "",
        "## Score Summary",
        "",
        table(
            ["Pass", "Macro Score", "Slide Penalty", "Multiplier", "Adjusted Readiness Score"],
            [
                ("Baseline", summary["baseline_macro_score"], summary["baseline_slide_penalty"], summary["baseline_multiplier"], summary["baseline_adjusted_score"]),
                ("Optimized", summary["optimized_macro_score"], summary["optimized_slide_penalty"], summary["optimized_multiplier"], summary["optimized_adjusted_score"]),
            ],
        ),
        "",
        f"Second-pass improvement: `+{summary['improvement']}` adjusted points.",
        "",
        "## Category Evidence",
        "",
        table(
            ["Category", "Score", "Max", "Strengths", "Weaknesses", "Evidence"],
            rows,
        ),
        "",
        "## Strict Scoring Bands",
        "",
        table(
            ["Band", "Range", "Meaning", "Required Action"],
            [
                ("Excellent", "90-100", "Conference-ready with strong narrative, timing, delivery, and memorability.", "Polish delivery and slide-level precision."),
                ("Strong", "80-89", "Professional talk with visible repair points.", "Fix the lowest category before adding content."),
                ("Acceptable", "70-79", "Understandable but not yet high-impact.", "Repair structure, timing, and density first."),
                ("Weak", "60-69", "Content exists but delivery or structure is not conference-ready.", "Simplify and rebuild the talk spine."),
                ("Poor", "<60", "Not ready for a professional audience.", "Rebuild from thesis, map, evidence chain, and Patch SLA."),
            ],
        ),
        "",
        "## Evidence-Based Scoring Instructions",
        "",
        numbered(
            [
                "Score only observable delivery evidence, not preparation effort.",
                "If the evaluator cannot state the arc in one sentence, Structure and Narrative Design cannot exceed 14/20.",
                "If FDA, TFDA, or NIST are named without operational translation, Content Depth and Value cannot exceed 13/20.",
                "If Slide 14 starts after 28:00, Stage Rhythm and Time Control cannot exceed 10/15.",
                "If any major slide requires paragraph reading, Visual Design cannot exceed 7/10.",
                "If the speaker turns away during `Cyber Safety is Patient Safety` or the Patch SLA line, Stage Presence cannot exceed 7/10.",
                "If the audience cannot recall product scale, Patch SLA, or 30 / 60 / 90, Audience Impact cannot exceed 6/10.",
            ]
        ),
        "",
        "## Evaluator Note Format",
        "",
        "```text",
        "Run date:",
        "Version scored:",
        "Macro score:",
        "Slide penalty:",
        "Adjusted readiness score:",
        "",
        "Top 3 strengths:",
        "1.",
        "2.",
        "3.",
        "",
        "Top 3 deductions:",
        "1. Category / slide / evidence / severity / fix:",
        "2. Category / slide / evidence / severity / fix:",
        "3. Category / slide / evidence / severity / fix:",
        "",
        "Timing checkpoints:",
        "- Slide 3:",
        "- Slide 7:",
        "- Slide 10:",
        "- Slide 12:",
        "- Slide 14:",
        "- Finish:",
        "",
        "Next repair pass:",
        "```",
        "",
    ]
    return "\n".join(lines)


def render_constraint_report(data: dict) -> str:
    constraint = data["constraint_system"]
    rows = [
        (
            slide["id"],
            slide["title"],
            slide["constraint"]["pass_fail"],
            slide["constraint"]["violations"],
            slide["constraint"]["severity"],
        )
        for slide in data["slides"]
    ]
    lines = [
        "# Slide Constraint Report",
        "",
        "This report is the slide-level quality firewall. It does not replace the macro `100`-point speech rubric; it applies pass/fail gates, penalties, and design-risk checks after the macro score is assigned.",
        "",
        "## Hard Rules",
        "",
        bullet(constraint["hard_rules"]),
        "",
        "## Allowed Layouts",
        "",
        bullet(constraint["allowed_layouts"]),
        "",
        "## Design System",
        "",
        table(
            ["Axis", "Rule"],
            [(key.replace("_", " ").title(), value) for key, value in constraint["design_system"].items()],
        ),
        "",
        "## Penalty Model",
        "",
        table(
            ["Severity", "Penalty", "Condition"],
            [
                (penalty["severity"], penalty["penalty"], penalty["condition"])
                for penalty in constraint["penalties"]
            ],
        ),
        "",
        "## Baseline Violations Before Optimization",
        "",
        table(
            ["Slide", "Pass/Fail", "Violations", "Severity", "Penalty", "Required Redesign"],
            [
                (
                    item["slide_id"],
                    item["pass_fail"],
                    item["violations"],
                    item["severity"],
                    item["penalty"],
                    item["redesign"],
                )
                for item in data["baseline_constraint_results"]
            ],
        ),
        "",
        "## Optimized Slide Gate",
        "",
        table(
            ["Slide", "Title", "Pass/Fail", "Violations", "Severity"],
            rows,
        ),
        "",
        "## Redesign Priority",
        "",
        numbered(data["optimization"]["top_improvements"]),
        "",
    ]
    return "\n".join(lines)


def render_optimization_plan(data: dict) -> str:
    optimization = data["optimization"]
    summary = data["score_summary"]
    lines = [
        "# Optimization Plan",
        "",
        "The optimization loop targets the highest-leverage weak points first: density in the evidence bridge, testing drift, timing protection, visual distinctiveness, and final-minute control.",
        "",
        "## Top 5 Failure Points",
        "",
        numbered(optimization["top_failure_points"]),
        "",
        "## Top 5 High-Leverage Improvements",
        "",
        numbered(optimization["top_improvements"]),
        "",
        "## Improved Outline",
        "",
        numbered(optimization["improved_outline"]),
        "",
        "## Improved Opening",
        "",
        f"> {optimization['improved_opening']}",
        "",
        "## Improved Closing",
        "",
        f"> {optimization['improved_closing']}",
        "",
        "## Improved Transitions",
        "",
        numbered(optimization["improved_transitions"]),
        "",
        "## Three Memorable Moments",
        "",
        table(
            ["Slide", "Line", "Purpose"],
            [
                (moment["slide"], moment["line"], moment["purpose"])
                for moment in optimization["memorable_moments"]
            ],
        ),
        "",
        "## Simulated Second Evaluation",
        "",
        table(
            ["Metric", "Baseline", "Optimized"],
            [
                ("Macro score", summary["baseline_macro_score"], summary["optimized_macro_score"]),
                ("Slide penalty", summary["baseline_slide_penalty"], summary["optimized_slide_penalty"]),
                ("Multiplier", summary["baseline_multiplier"], summary["optimized_multiplier"]),
                ("Adjusted readiness score", summary["baseline_adjusted_score"], summary["optimized_adjusted_score"]),
            ],
        ),
        "",
        f"Target improvement achieved: `+{summary['improvement']}` adjusted points.",
        "",
        "## Fix Order By Score Band",
        "",
        table(
            ["Score Band", "First Fix", "Reason"],
            [
                ("Below 70", "Rebuild Slides 3, 5, 6, 12, and 14.", "The talk spine is not yet stable."),
                ("70-80", "Reduce visual density and rehearse cut markers.", "The talk is understandable but not conference-ready."),
                ("80-90", "Tighten Slide 6, Slide 12, and final-minute delivery.", "The talk is strong enough to refine."),
                ("90+", "Practice silence, eye contact, and exact timing.", "The difference is control under pressure."),
            ],
        ),
        "",
    ]
    return "\n".join(lines)


def write_csvs(data: dict) -> None:
    scoring_path = OUT_DIR / "scoring_report.csv"
    with scoring_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SCORING_HEADERS)
        writer.writeheader()
        for category in data["scoring_categories"]:
            writer.writerow(
                {
                    "Category": category["category"],
                    "Score": category["optimized_score"],
                    "MaxScore": category["max_score"],
                    "Strengths": category["strengths"],
                    "Weaknesses": category["weaknesses"],
                    "Evidence": category["evidence"],
                }
            )

    slide_path = OUT_DIR / "slide_validation.csv"
    with slide_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=SLIDE_HEADERS)
        writer.writeheader()
        for slide in data["slides"]:
            writer.writerow(
                {
                    "SlideID": slide["id"],
                    "PassFail": slide["constraint"]["pass_fail"],
                    "Violations": slide["constraint"]["violations"],
                    "Severity": slide["constraint"]["severity"],
                }
            )


def main() -> None:
    data = load_data()
    validate(data)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    outputs = {
        "main_strategy.md": render_main_strategy(data),
        "slide_blueprint.md": render_slide_blueprint(data),
        "evaluation_report.md": render_evaluation_report(data),
        "slide_constraint_report.md": render_constraint_report(data),
        "optimization_plan.md": render_optimization_plan(data),
    }
    for name, content in outputs.items():
        (OUT_DIR / name).write_text(content, encoding="utf-8")

    write_csvs(data)
    print(f"Generated {len(outputs) + 2} files in {OUT_DIR}")
    print(f"Slides: {len(data['slides'])}")
    print(f"Timing: {sum(int(slide['speaking_seconds']) for slide in data['slides'])} seconds")
    print(f"Rubric max: {sum(int(category['max_score']) for category in data['scoring_categories'])}")


if __name__ == "__main__":
    main()
