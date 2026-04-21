#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const { Presentation, PresentationFile } = await import("@oai/artifact-tool");

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const dataPath = path.join(root, "data", "presentation_os.json");
const outputDir = path.join(root, "outputs", "deck");
const previewDir = path.join(outputDir, "previews");
const deckPath = path.join(outputDir, "cybersec-2026-ai-samd-compact-optimized.pptx");
const reportPath = path.join(outputDir, "deck_build_report.json");

const WIDTH = 1280;
const HEIGHT = 720;

const COLORS = {
  bg: "#070B12",
  bg2: "#0D1422",
  panel: "#101A2B",
  panel2: "#111F34",
  text: "#F5F7FA",
  muted: "#9AA7B8",
  dim: "#344255",
  accent: "#38D7FF",
  accent2: "#9BF2FF",
  risk: "#FF4D5E",
  evidence: "#E7F6FF",
  line: "#2B3B52",
};

const FONT = {
  title: "Poppins",
  body: "Lato",
};

async function readImageBlob(imagePath) {
  const bytes = await fs.readFile(imagePath);
  return bytes.buffer.slice(bytes.byteOffset, bytes.byteOffset + bytes.byteLength);
}

function secondsToTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const rem = String(seconds % 60).padStart(2, "0");
  return `${minutes}:${rem}`;
}

function createDeck() {
  const presentation = Presentation.create({
    slideSize: { width: WIDTH, height: HEIGHT },
  });
  presentation.theme.colorScheme = {
    name: "CYBERSEC Dark",
    themeColors: {
      accent1: COLORS.accent,
      accent2: COLORS.risk,
      bg1: COLORS.bg,
      bg2: COLORS.bg2,
      tx1: COLORS.text,
      tx2: COLORS.muted,
    },
  };
  return presentation;
}

function addText(slide, text, position, options = {}) {
  const shape = slide.shapes.add({
    geometry: "rect",
    position,
    fill: options.fill ?? "#00000000",
    line: { style: "solid", fill: "#00000000", width: 0 },
  });
  shape.text = Array.isArray(text) ? text : String(text);
  shape.text.fontSize = options.size ?? 32;
  shape.text.bold = options.bold ?? false;
  shape.text.color = options.color ?? COLORS.text;
  shape.text.typeface = options.typeface ?? FONT.body;
  shape.text.alignment = options.align ?? "left";
  shape.text.verticalAlignment = options.valign ?? "middle";
  shape.text.insets = options.insets ?? { left: 0, right: 0, top: 0, bottom: 0 };
  if (options.autoFit) shape.text.autoFit = options.autoFit;
  return shape;
}

function addPanel(slide, position, options = {}) {
  return slide.shapes.add({
    geometry: options.geometry ?? "roundRect",
    position,
    adjustmentList: [{ name: "adj", formula: "val 9000" }],
    fill: options.fill ?? COLORS.panel,
    line: {
      style: "solid",
      fill: options.lineFill ?? COLORS.line,
      width: options.lineWidth ?? 1.2,
    },
  });
}

function addLine(slide, left, top, width, height, color = COLORS.line) {
  return slide.shapes.add({
    geometry: "rect",
    position: { left, top, width, height },
    fill: color,
    line: { style: "solid", fill: color, width: 0 },
  });
}

function addPill(slide, label, left, top, width, color = COLORS.accent) {
  const pill = addPanel(slide, { left, top, width, height: 42 }, {
    fill: `${color}18`,
    lineFill: `${color}88`,
  });
  addText(slide, label, { left, top: top + 1, width, height: 40 }, {
    size: 17,
    bold: true,
    color,
    align: "center",
    typeface: FONT.body,
  });
  return pill;
}

function addBackground(slide) {
  slide.background.fill = COLORS.bg;
  addLine(slide, 72, 638, 1136, 1.5, "#1E2B3D");
  addLine(slide, 72, 78, 70, 3, COLORS.accent);
}

function addSpeakerNotes(slide, text) {
  if (slide.speakerNotes && typeof slide.speakerNotes.setText === "function") {
    slide.speakerNotes.setText(text);
  }
}

function buildTitleSlide(presentation, slideData) {
  const slide = presentation.slides.add();
  addBackground(slide);
  addText(slide, slideData.onscreen[0], { left: 72, top: 154, width: 770, height: 130 }, {
    size: 54,
    bold: true,
    typeface: FONT.title,
  });
  addText(slide, slideData.onscreen[1], { left: 76, top: 300, width: 640, height: 50 }, {
    size: 26,
    color: COLORS.accent2,
    typeface: FONT.body,
  });
  addText(slide, slideData.onscreen[2], { left: 76, top: 560, width: 560, height: 36 }, {
    size: 19,
    color: COLORS.muted,
  });

  const nodes = [
    [900, 190, "FDA 524B"],
    [980, 315, "Threat\nModel"],
    [850, 445, "Patch\nSLA"],
  ];
  for (const [left, top, label] of nodes) {
    addPanel(slide, { left, top, width: 170, height: 86 }, {
      fill: "#0F1B2C",
      lineFill: "#294766",
    });
    addText(slide, label, { left: left + 12, top: top + 10, width: 146, height: 66 }, {
      size: 21,
      bold: true,
      align: "center",
      color: COLORS.evidence,
    });
  }
  addLine(slide, 984, 276, 2, 42, "#294766");
  addLine(slide, 936, 402, 2, 42, "#294766");
  addSpeakerNotes(slide, slideData.speaker_note);
  return slide;
}

async function buildDisclaimerSlide(presentation, slideData, metadata) {
  const slide = presentation.slides.add();
  slide.background.fill = COLORS.bg;
  try {
    await fs.access(metadata.disclaimer_image);
    const image = slide.images.add({
      blob: await readImageBlob(metadata.disclaimer_image),
      fit: "contain",
      alt: "Required CYBERSEC disclaimer",
    });
    image.position = { left: 0, top: 0, width: WIDTH, height: HEIGHT };
  } catch {
    addText(slide, "Required CYBERSEC Disclaimer", { left: 140, top: 300, width: 1000, height: 80 }, {
      size: 42,
      bold: true,
      align: "center",
      typeface: FONT.title,
    });
  }
  addSpeakerNotes(slide, slideData.speaker_note);
  return slide;
}

function buildBigStatement(presentation, slideData, variant = "default") {
  const slide = presentation.slides.add();
  addBackground(slide);
  const titleSize = slideData.id === 10 ? 58 : slideData.id === 14 ? 50 : 64;
  const titleText = slideData.id === 14 ? slideData.onscreen.slice(0, 2).join("\n") : slideData.onscreen[0];
  addText(slide, titleText, { left: 90, top: 175, width: 820, height: 170 }, {
    size: titleSize,
    bold: true,
    typeface: FONT.title,
  });
  if (slideData.id === 3) {
    addPill(slide, "Trust", 100, 402, 128, COLORS.accent);
    addPill(slide, "Patch", 252, 402, 128, COLORS.accent);
    addPill(slide, "Evidence", 404, 402, 160, COLORS.accent);
    addPanel(slide, { left: 875, top: 168, width: 236, height: 236 }, {
      fill: "#0E1A2B",
      lineFill: "#284D68",
    });
    addLine(slide, 920, 252, 146, 2, COLORS.accent);
    addLine(slide, 992, 205, 2, 146, COLORS.accent);
  } else if (slideData.id === 10) {
    addText(slide, "Vendor responsibility | Hospital continuity | Clinical workflow", { left: 90, top: 410, width: 760, height: 44 }, {
      size: 20,
      color: COLORS.muted,
    });
    addLine(slide, 945, 190, 4, 300, COLORS.risk);
  } else if (slideData.id === 14) {
    addText(slide, "Build trust before the audit", { left: 94, top: 410, width: 560, height: 48 }, {
      size: 24,
      color: COLORS.accent2,
    });
    addLine(slide, 880, 250, 260, 2, COLORS.accent);
    addLine(slide, 880, 286, 190, 2, COLORS.dim);
    addLine(slide, 880, 322, 225, 2, COLORS.dim);
  }
  addSpeakerNotes(slide, slideData.speaker_note);
  return slide;
}

function buildInfrastructureSlide(presentation, slideData) {
  const slide = presentation.slides.add();
  addBackground(slide);
  addText(slide, "AI is becoming infrastructure", { left: 72, top: 104, width: 760, height: 70 }, {
    size: 42,
    bold: true,
    typeface: FONT.title,
  });
  const layers = ["Infrastructure", "Runtime", "Model"];
  layers.forEach((label, idx) => {
    const top = 210 + idx * 88;
    addPanel(slide, { left: 110 + idx * 34, top, width: 360, height: 68 }, {
      fill: idx === 2 ? "#102A3A" : COLORS.panel,
      lineFill: idx === 2 ? COLORS.accent : "#263C55",
    });
    addText(slide, label, { left: 138 + idx * 34, top: top + 10, width: 300, height: 48 }, {
      size: 26,
      bold: true,
      color: idx === 2 ? COLORS.accent2 : COLORS.text,
    });
  });
  addLine(slide, 670, 260, 340, 3, COLORS.accent);
  addLine(slide, 1008, 244, 4, 36, COLORS.risk);
  addLine(slide, 1010, 260, 110, 3, COLORS.dim);
  addText(slide, "Care continuity", { left: 672, top: 298, width: 400, height: 44 }, {
    size: 28,
    bold: true,
  });
  addText(slide, "Cyber incidents become care disruption", { left: 672, top: 360, width: 430, height: 54 }, {
    size: 23,
    color: COLORS.muted,
  });
  addSpeakerNotes(slide, slideData.speaker_note);
  return slide;
}

function buildScaleLadder(presentation, slideData) {
  const slide = presentation.slides.add();
  addBackground(slide);
  addText(slide, "Risk grows with architecture", { left: 72, top: 105, width: 780, height: 68 }, {
    size: 44,
    bold: true,
    typeface: FONT.title,
  });
  const steps = [
    ["Model", 110, 455, 190],
    ["Viewer", 320, 392, 220],
    ["Platform / Database", 560, 318, 270],
    ["Connected Medical System", 850, 236, 310],
  ];
  steps.forEach(([label, left, top, width], idx) => {
    addPanel(slide, { left, top, width, height: 94 }, {
      fill: idx === 3 ? "#172338" : COLORS.panel,
      lineFill: idx === 3 ? COLORS.accent : "#2A3C52",
    });
    addText(slide, label, { left: left + 15, top: top + 18, width: width - 30, height: 58 }, {
      size: idx === 3 ? 22 : 24,
      bold: true,
      align: "center",
      color: idx === 3 ? COLORS.accent2 : COLORS.text,
    });
  });
  addLine(slide, 180, 585, 850, 3, COLORS.accent);
  addText(slide, "Evidence grows", { left: 900, top: 598, width: 220, height: 34 }, {
    size: 20,
    color: COLORS.accent2,
  });
  addSpeakerNotes(slide, slideData.speaker_note);
  return slide;
}

function buildEvidenceChain(presentation, slideData) {
  const slide = presentation.slides.add();
  addBackground(slide);
  addText(slide, "Evidence, not slogans", { left: 72, top: 104, width: 760, height: 70 }, {
    size: 44,
    bold: true,
    typeface: FONT.title,
  });
  const nodes = ["Risk", "Control", "Test", "Fix", "Evidence"];
  nodes.forEach((label, idx) => {
    const left = 100 + idx * 195;
    addPanel(slide, { left, top: 300, width: 150, height: 82 }, {
      fill: idx === 4 ? "#102C3A" : COLORS.panel,
      lineFill: idx === 4 ? COLORS.accent : COLORS.line,
    });
    addText(slide, label, { left: left + 8, top: 316, width: 134, height: 50 }, {
      size: 25,
      bold: true,
      align: "center",
      color: idx === 4 ? COLORS.accent2 : COLORS.text,
    });
    if (idx < nodes.length - 1) addLine(slide, left + 150, 340, 45, 2.5, COLORS.accent);
  });
  ["Monitor", "Patch", "Disclose", "SBOM"].forEach((label, idx) => {
    addPill(slide, label, 184 + idx * 215, 455, 130, idx === 1 ? COLORS.risk : COLORS.accent);
  });
  addSpeakerNotes(slide, slideData.speaker_note);
  return slide;
}

function buildThreeColumnBridge(presentation, slideData) {
  const slide = presentation.slides.add();
  addBackground(slide);
  addText(slide, "Model, governance, stack", { left: 72, top: 104, width: 760, height: 70 }, {
    size: 44,
    bold: true,
    typeface: FONT.title,
  });
  const cols = [
    ["Model evidence", ["Intended use", "Data", "V&V"]],
    ["Governance language", ["Govern", "Protect", "Recover"]],
    ["AI stack", ["Provenance", "Isolation", "Updates"]],
  ];
  cols.forEach(([heading, labels], idx) => {
    const left = 105 + idx * 365;
    addPanel(slide, { left, top: 235, width: 300, height: 282 }, {
      fill: idx === 1 ? "#111F34" : COLORS.panel,
      lineFill: idx === 1 ? COLORS.accent : COLORS.line,
    });
    addText(slide, heading, { left: left + 24, top: 260, width: 252, height: 46 }, {
      size: 24,
      bold: true,
      color: idx === 1 ? COLORS.accent2 : COLORS.text,
    });
    labels.forEach((label, labelIdx) => {
      addText(slide, label, { left: left + 32, top: 330 + labelIdx * 52, width: 236, height: 34 }, {
        size: 21,
        color: COLORS.muted,
      });
      addLine(slide, left + 24, 347 + labelIdx * 52, 4, 4, COLORS.accent);
    });
  });
  addSpeakerNotes(slide, slideData.speaker_note);
  return slide;
}

function buildContrastSlide(presentation, slideData) {
  const slide = presentation.slides.add();
  addBackground(slide);
  addText(slide, slideData.title, { left: 72, top: 102, width: 760, height: 70 }, {
    size: 44,
    bold: true,
    typeface: FONT.title,
  });
  const isTesting = slideData.id === 11;
  const panels = isTesting
    ? [
        ["White-box", ["Repair before release"], COLORS.accent],
        ["Black-box", ["Validate external exposure"], COLORS.risk],
      ]
    : slideData.id === 8
      ? [
          ["Model", ["Artifact", "Data lineage", "SBOM", "Update boundary"], COLORS.accent],
          ["Viewer", ["Parser", "Upload", "Cache", "Output limits"], COLORS.risk],
        ]
      : [
          ["Platform / Database", ["Identity", "RBAC", "API", "Database", "Audit log"], COLORS.accent],
          ["Connected Medical System", ["PACS / HIS", "Hospital network", "Update server", "Remote service"], COLORS.risk],
        ];
  panels.forEach(([heading, labels, color], idx) => {
    const left = idx === 0 ? 104 : 690;
    addPanel(slide, { left, top: 228, width: 486, height: isTesting ? 235 : 310 }, {
      fill: COLORS.panel,
      lineFill: color,
    });
    addText(slide, heading, { left: left + 28, top: 258, width: 420, height: 48 }, {
      size: 30,
      bold: true,
      color,
      typeface: FONT.title,
    });
    labels.forEach((label, labelIdx) => {
      addText(slide, label, { left: left + 38, top: 332 + labelIdx * 42, width: 390, height: 30 }, {
        size: 21,
        color: COLORS.text,
      });
    });
  });
  if (isTesting) {
    addPanel(slide, { left: 305, top: 530, width: 670, height: 64 }, {
      fill: "#0F2435",
      lineFill: COLORS.accent,
    });
    addText(slide, "Finding list + retest evidence", { left: 325, top: 540, width: 630, height: 44 }, {
      size: 26,
      bold: true,
      align: "center",
      color: COLORS.accent2,
    });
  }
  addSpeakerNotes(slide, slideData.speaker_note);
  return slide;
}

function buildPatchSla(presentation, slideData) {
  const slide = presentation.slides.add();
  addBackground(slide);
  addText(slide, "Patch SLA", { left: 72, top: 102, width: 400, height: 70 }, {
    size: 48,
    bold: true,
    typeface: FONT.title,
  });
  addText(slide, "Every finding needs a decision", { left: 76, top: 172, width: 600, height: 44 }, {
    size: 27,
    color: COLORS.accent2,
  });
  const flow = ["Intake", "Triage", "Decision", "Patch", "Retest", "Archive"];
  flow.forEach((label, idx) => {
    const isDecision = label === "Decision";
    const left = 86 + idx * 184;
    const top = isDecision ? 285 : 310;
    const width = isDecision ? 172 : 132;
    const height = isDecision ? 112 : 72;
    addPanel(slide, { left: isDecision ? left - 20 : left, top, width, height }, {
      fill: isDecision ? "#122F3F" : COLORS.panel,
      lineFill: isDecision ? COLORS.accent : COLORS.line,
      lineWidth: isDecision ? 2.4 : 1.2,
    });
    addText(slide, label, { left: isDecision ? left - 10 : left + 8, top: top + 14, width: width - 16, height: height - 28 }, {
      size: isDecision ? 31 : 20,
      bold: true,
      align: "center",
      color: isDecision ? COLORS.accent2 : COLORS.text,
    });
    if (idx < flow.length - 1) addLine(slide, left + width + (isDecision ? -20 : 0), 346, 42, 2.5, COLORS.accent);
  });
  ["Fix now", "Compensate", "Defer", "Not applicable"].forEach((label, idx) => {
    addPill(slide, label, 246 + idx * 200, 505, 150, idx === 2 ? COLORS.risk : COLORS.accent);
  });
  addSpeakerNotes(slide, slideData.speaker_note);
  return slide;
}

function buildRoadmap(presentation, slideData) {
  const slide = presentation.slides.add();
  addBackground(slide);
  addText(slide, "Small Team 30 / 60 / 90", { left: 72, top: 102, width: 760, height: 70 }, {
    size: 44,
    bold: true,
    typeface: FONT.title,
  });
  const blocks = [
    ["30", "Inventory\nSBOM\nData flow"],
    ["60", "Threat model\nCI gates\nFinding workflow"],
    ["90", "Pen test\nPatch SLA\nRetest evidence"],
  ];
  blocks.forEach(([day, text], idx) => {
    const left = 114 + idx * 365;
    addPanel(slide, { left, top: 244, width: 300, height: 265 }, {
      fill: idx === 2 ? "#111F34" : COLORS.panel,
      lineFill: idx === 2 ? COLORS.accent : COLORS.line,
    });
    addText(slide, day, { left: left + 30, top: 268, width: 240, height: 64 }, {
      size: 48,
      bold: true,
      align: "center",
      color: idx === 2 ? COLORS.accent2 : COLORS.text,
      typeface: FONT.title,
    });
    addText(slide, text, { left: left + 42, top: 352, width: 216, height: 110 }, {
      size: 22,
      align: "center",
      color: COLORS.muted,
    });
  });
  addSpeakerNotes(slide, slideData.speaker_note);
  return slide;
}

async function buildDeck() {
  const data = JSON.parse(await fs.readFile(dataPath, "utf-8"));
  if (data.slides.length !== 14) throw new Error("Expected exactly 14 slides");
  const totalSeconds = data.slides.reduce((sum, slide) => sum + slide.speaking_seconds, 0);
  if (totalSeconds !== 1710) throw new Error(`Expected 1710 seconds, got ${totalSeconds}`);
  const failingSlides = data.slides.filter((slide) => slide.constraint.pass_fail !== "PASS");
  if (failingSlides.length > 0) {
    throw new Error(`Hard constraint gate failed for slides: ${failingSlides.map((slide) => slide.id).join(", ")}`);
  }

  await fs.mkdir(outputDir, { recursive: true });
  await fs.mkdir(previewDir, { recursive: true });

  const presentation = createDeck();
  const builtSlides = [];
  for (const slideData of data.slides) {
    if (slideData.id === 1) builtSlides.push(buildTitleSlide(presentation, slideData));
    else if (slideData.id === 2) builtSlides.push(await buildDisclaimerSlide(presentation, slideData, data.metadata));
    else if ([3, 10, 14].includes(slideData.id)) builtSlides.push(buildBigStatement(presentation, slideData));
    else if (slideData.id === 4) builtSlides.push(buildInfrastructureSlide(presentation, slideData));
    else if (slideData.id === 5) builtSlides.push(buildScaleLadder(presentation, slideData));
    else if (slideData.id === 6) builtSlides.push(buildEvidenceChain(presentation, slideData));
    else if (slideData.id === 7) builtSlides.push(buildThreeColumnBridge(presentation, slideData));
    else if ([8, 9, 11].includes(slideData.id)) builtSlides.push(buildContrastSlide(presentation, slideData));
    else if (slideData.id === 12) builtSlides.push(buildPatchSla(presentation, slideData));
    else if (slideData.id === 13) builtSlides.push(buildRoadmap(presentation, slideData));
  }

  if (presentation.slides.count !== 14) {
    throw new Error(`Expected 14 slides after build, got ${presentation.slides.count}`);
  }

  const previewSlides = [0, 2, 4, 9, 11, 13];
  const previewFiles = [];
  for (const index of previewSlides) {
    const rendered = await presentation.export({
      slide: presentation.slides.getItem(index),
      format: "png",
      scale: 0.5,
    });
    const previewPath = path.join(previewDir, `slide-${String(index + 1).padStart(2, "0")}.png`);
    await fs.writeFile(previewPath, Buffer.from(await rendered.arrayBuffer()));
    previewFiles.push(previewPath);
  }

  const pptx = await PresentationFile.exportPptx(presentation);
  await pptx.save(deckPath);

  const report = {
    deckPath,
    slideCount: presentation.slides.count,
    timingSeconds: totalSeconds,
    timing: secondsToTime(totalSeconds),
    editableTextSource: "All visible talk text except the organizer disclaimer image is created as editable PowerPoint text/shapes.",
    hardConstraintGate: "PASS",
    previewFiles,
    keyText: [
      "你賣的不是模型",
      "Risk grows with architecture",
      "Cyber Safety Is Patient Safety",
      "Every finding needs a decision",
      "Build trust before the audit",
    ],
  };
  await fs.writeFile(reportPath, JSON.stringify(report, null, 2), "utf-8");
  console.log(JSON.stringify(report, null, 2));
}

await buildDeck();
