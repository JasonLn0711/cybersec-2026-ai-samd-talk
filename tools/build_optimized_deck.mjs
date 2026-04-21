#!/usr/bin/env node
import { execFile } from "node:child_process";
import fs from "node:fs/promises";
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const require = createRequire(import.meta.url);
const pptxgen = require("pptxgenjs");
const execFileAsync = promisify(execFile);

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");
const dataPath = path.join(root, "data", "presentation_os.json");
const outputDir = path.join(root, "outputs", "deck");
const previewDir = path.join(outputDir, "previews");
const deckPath = path.join(outputDir, "cybersec-2026-ai-samd-compact-optimized.pptx");
const pdfPath = path.join(outputDir, "cybersec-2026-ai-samd-compact-optimized.pdf");
const reportPath = path.join(outputDir, "deck_build_report.json");

const WIDTH = 1280;
const HEIGHT = 720;
const SCALE = 100;

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

function resolveRepoPath(filePath) {
  if (!filePath || path.isAbsolute(filePath)) return filePath;
  return path.resolve(root, filePath);
}

function toRepoRelative(filePath) {
  return path.relative(root, filePath);
}

function secondsToTime(seconds) {
  const minutes = Math.floor(seconds / 60);
  const rem = String(seconds % 60).padStart(2, "0");
  return `${minutes}:${rem}`;
}

function u(value) {
  return Number((value / SCALE).toFixed(3));
}

function box(position) {
  return {
    x: u(position.left),
    y: u(position.top),
    w: u(position.width),
    h: u(position.height),
  };
}

function parseColor(value, fallback = COLORS.text) {
  const normalized = String(value || fallback).replace("#", "");
  const color = normalized.slice(0, 6);
  if (normalized.length >= 8) {
    const alpha = Number.parseInt(normalized.slice(6, 8), 16);
    return { color, transparency: Math.round(100 - (alpha / 255) * 100) };
  }
  return { color, transparency: 0 };
}

function fill(value, fallback = COLORS.panel) {
  const parsed = parseColor(value, fallback);
  return { color: parsed.color, transparency: parsed.transparency };
}

function stroke(value, width = 1.2) {
  const parsed = parseColor(value, COLORS.line);
  return { color: parsed.color, transparency: parsed.transparency, width };
}

function textColor(value) {
  return parseColor(value, COLORS.text).color;
}

function createDeck() {
  const pptx = new pptxgen();
  pptx.defineLayout({ name: "CYBERSEC_WIDE", width: u(WIDTH), height: u(HEIGHT) });
  pptx.layout = "CYBERSEC_WIDE";
  pptx.author = "Lin Jiasheng";
  pptx.company = "CYBERSEC 2026";
  pptx.subject = "AI SaMD cybersecurity talk";
  pptx.title = "AI SaMD Cybersecurity: From Model Demo to Product Trust";
  pptx.lang = "zh-TW";
  pptx.theme = {
    headFontFace: FONT.title,
    bodyFontFace: FONT.body,
    lang: "zh-TW",
  };
  return pptx;
}

function addText(slide, text, position, options = {}) {
  slide.addText(String(text ?? ""), {
    ...box(position),
    margin: options.margin ?? 0.02,
    breakLine: false,
    fit: options.fit ?? "shrink",
    fontFace: options.typeface ?? FONT.body,
    fontSize: options.size ?? 24,
    bold: options.bold ?? false,
    color: textColor(options.color ?? COLORS.text),
    align: options.align ?? "left",
    valign: options.valign ?? "mid",
    fill: fill(options.fill ?? "#00000000", "#000000"),
    line: stroke("#00000000", 0),
  });
}

function addPanel(pptx, slide, position, options = {}) {
  slide.addShape(options.shape ?? pptx.ShapeType.roundRect, {
    ...box(position),
    rectRadius: 0.05,
    fill: fill(options.fill ?? COLORS.panel),
    line: stroke(options.lineFill ?? COLORS.line, options.lineWidth ?? 1.1),
  });
}

function addLine(pptx, slide, left, top, width, height, color = COLORS.line) {
  slide.addShape(pptx.ShapeType.rect, {
    x: u(left),
    y: u(top),
    w: u(width),
    h: u(height),
    fill: fill(color),
    line: stroke(color, 0),
  });
}

function addPill(pptx, slide, label, left, top, width, color = COLORS.accent) {
  addPanel(pptx, slide, { left, top, width, height: 42 }, {
    fill: `${color}18`,
    lineFill: `${color}88`,
  });
  addText(slide, label, { left, top: top + 1, width, height: 40 }, {
    size: 17,
    bold: true,
    color,
    align: "center",
  });
}

function addBackground(pptx, slide) {
  slide.background = fill(COLORS.bg);
  addLine(pptx, slide, 72, 638, 1136, 1.5, "#1E2B3D");
  addLine(pptx, slide, 72, 78, 70, 3, COLORS.accent);
}

function addSpeakerNotes(slide, text) {
  if (text) slide.addNotes(String(text));
}

function buildTitleSlide(pptx, slideData) {
  const slide = pptx.addSlide();
  addBackground(pptx, slide);
  addText(slide, slideData.onscreen[0], { left: 72, top: 150, width: 780, height: 132 }, {
    size: 54,
    bold: true,
    typeface: FONT.title,
  });
  addText(slide, slideData.onscreen[1], { left: 76, top: 300, width: 690, height: 50 }, {
    size: 26,
    color: COLORS.accent2,
  });
  addText(slide, slideData.onscreen[2], { left: 76, top: 560, width: 560, height: 36 }, {
    size: 19,
    color: COLORS.muted,
  });

  const nodes = [
    [880, 160, "Boundary"],
    [1008, 278, "Evidence"],
    [845, 432, "Repair\nProof"],
  ];
  for (const [left, top, label] of nodes) {
    addPanel(pptx, slide, { left, top, width: 180, height: 88 }, {
      fill: "#0F1B2C",
      lineFill: "#294766",
    });
    addText(slide, label, { left: left + 12, top: top + 10, width: 156, height: 68 }, {
      size: 21,
      bold: true,
      align: "center",
      color: COLORS.evidence,
    });
  }
  addLine(pptx, slide, 980, 248, 2, 62, "#294766");
  addLine(pptx, slide, 940, 366, 2, 66, "#294766");
  addSpeakerNotes(slide, slideData.speaker_note);
}

async function buildDisclaimerSlide(pptx, slideData, metadata) {
  const slide = pptx.addSlide();
  slide.background = fill(COLORS.bg);
  const disclaimerImage = resolveRepoPath(metadata.disclaimer_image);
  try {
    await fs.access(disclaimerImage);
    slide.addImage({
      path: disclaimerImage,
      x: 0,
      y: 0,
      w: u(WIDTH),
      h: u(HEIGHT),
    });
  } catch {
    addText(slide, "Required CYBERSEC Disclaimer", { left: 140, top: 300, width: 1000, height: 80 }, {
      size: 42,
      bold: true,
      align: "center",
      typeface: FONT.title,
    });
  }
  addSpeakerNotes(slide, slideData.speaker_note);
}

function buildBigStatement(pptx, slideData) {
  const slide = pptx.addSlide();
  addBackground(pptx, slide);
  const titleSize = slideData.id === 10 ? 58 : slideData.id === 14 ? 50 : 64;
  const titleText = slideData.id === 14 ? slideData.onscreen.slice(0, 2).join("\n") : slideData.onscreen[0];
  addText(slide, titleText, { left: 90, top: 175, width: 820, height: 170 }, {
    size: titleSize,
    bold: true,
    typeface: FONT.title,
  });

  if (slideData.id === 3) {
    addPill(pptx, slide, slideData.onscreen[1], 100, 402, 138, COLORS.accent);
    addPill(pptx, slide, slideData.onscreen[2], 264, 402, 128, COLORS.accent);
    addPill(pptx, slide, slideData.onscreen[3], 418, 402, 148, COLORS.accent);
    addPanel(pptx, slide, { left: 875, top: 168, width: 236, height: 236 }, {
      fill: "#0E1A2B",
      lineFill: "#284D68",
    });
    addLine(pptx, slide, 920, 252, 146, 2, COLORS.accent);
    addLine(pptx, slide, 992, 205, 2, 146, COLORS.accent);
  } else if (slideData.id === 10) {
    const labels = slideData.onscreen.slice(1);
    labels.forEach((label, idx) => {
      addPill(pptx, slide, label, 92 + idx * 185, 410, 160, idx === 1 ? COLORS.risk : COLORS.accent);
    });
    addLine(pptx, slide, 945, 190, 4, 300, COLORS.risk);
  } else if (slideData.id === 14) {
    addText(slide, slideData.onscreen[2], { left: 94, top: 410, width: 560, height: 48 }, {
      size: 24,
      color: COLORS.accent2,
    });
    addLine(pptx, slide, 880, 250, 260, 2, COLORS.accent);
    addLine(pptx, slide, 880, 286, 190, 2, COLORS.dim);
    addLine(pptx, slide, 880, 322, 225, 2, COLORS.dim);
  }
  addSpeakerNotes(slide, slideData.speaker_note);
}

function buildInfrastructureSlide(pptx, slideData) {
  const slide = pptx.addSlide();
  addBackground(pptx, slide);
  addText(slide, slideData.onscreen[0], { left: 72, top: 104, width: 860, height: 70 }, {
    size: 42,
    bold: true,
    typeface: FONT.title,
  });

  slideData.onscreen.slice(1, 5).forEach((label, idx) => {
    const top = 205 + idx * 74;
    addPanel(pptx, slide, { left: 110 + idx * 28, top, width: 390, height: 58 }, {
      fill: idx === 3 ? "#102A3A" : COLORS.panel,
      lineFill: idx === 3 ? COLORS.accent : "#263C55",
    });
    addText(slide, label, { left: 138 + idx * 28, top: top + 8, width: 332, height: 42 }, {
      size: 24,
      bold: true,
      color: idx === 3 ? COLORS.accent2 : COLORS.text,
    });
  });

  addLine(pptx, slide, 670, 260, 340, 3, COLORS.accent);
  addLine(pptx, slide, 1008, 244, 4, 36, COLORS.risk);
  addLine(pptx, slide, 1010, 260, 110, 3, COLORS.dim);
  addText(slide, slideData.onscreen[5], { left: 672, top: 298, width: 400, height: 44 }, {
    size: 28,
    bold: true,
  });
  addText(slide, slideData.onscreen[6], { left: 672, top: 360, width: 460, height: 58 }, {
    size: 23,
    color: COLORS.muted,
  });
  addSpeakerNotes(slide, slideData.speaker_note);
}

function buildScaleLadder(pptx, slideData) {
  const slide = pptx.addSlide();
  addBackground(pptx, slide);
  addText(slide, slideData.onscreen[0], { left: 72, top: 105, width: 780, height: 68 }, {
    size: 44,
    bold: true,
    typeface: FONT.title,
  });

  const steps = [
    [slideData.onscreen[1], 110, 455, 190],
    [slideData.onscreen[2], 320, 392, 220],
    [slideData.onscreen[3], 560, 318, 270],
    [slideData.onscreen[4], 850, 236, 310],
  ];
  steps.forEach(([label, left, top, width], idx) => {
    addPanel(pptx, slide, { left, top, width, height: 94 }, {
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
  addLine(pptx, slide, 180, 585, 850, 3, COLORS.accent);
  addText(slide, slideData.onscreen[5], { left: 830, top: 598, width: 330, height: 34 }, {
    size: 20,
    color: COLORS.accent2,
    align: "right",
  });
  addSpeakerNotes(slide, slideData.speaker_note);
}

function buildEvidenceChain(pptx, slideData) {
  const slide = pptx.addSlide();
  addBackground(pptx, slide);
  addText(slide, slideData.onscreen[0], { left: 72, top: 104, width: 760, height: 70 }, {
    size: 44,
    bold: true,
    typeface: FONT.title,
  });

  const nodes = slideData.onscreen.slice(1, 7);
  nodes.forEach((label, idx) => {
    const left = 82 + idx * 180;
    const width = idx === 5 ? 176 : 138;
    addPanel(pptx, slide, { left, top: 292, width, height: 82 }, {
      fill: idx === nodes.length - 1 ? "#102C3A" : COLORS.panel,
      lineFill: idx === nodes.length - 1 ? COLORS.accent : COLORS.line,
    });
    addText(slide, label, { left: left + 8, top: 308, width: width - 16, height: 50 }, {
      size: idx === 5 ? 20 : 23,
      bold: true,
      align: "center",
      color: idx === nodes.length - 1 ? COLORS.accent2 : COLORS.text,
    });
    if (idx < nodes.length - 1) addLine(pptx, slide, left + width, 332, 42, 2.5, COLORS.accent);
  });

  slideData.onscreen.slice(7).forEach((label, idx) => {
    addPill(pptx, slide, label, 182 + idx * 215, 455, 130, idx === 1 ? COLORS.risk : COLORS.accent);
  });
  addSpeakerNotes(slide, slideData.speaker_note);
}

function buildThreeColumnBridge(pptx, slideData) {
  const slide = pptx.addSlide();
  addBackground(pptx, slide);
  addText(slide, slideData.title, { left: 72, top: 104, width: 860, height: 70 }, {
    size: 42,
    bold: true,
    typeface: FONT.title,
  });

  const cols = [
    [slideData.onscreen[0], slideData.onscreen.slice(1, 4)],
    [slideData.onscreen[4], slideData.onscreen.slice(5, 8)],
    [slideData.onscreen[8], slideData.onscreen.slice(9, 12)],
  ];
  cols.forEach(([heading, labels], idx) => {
    const left = 105 + idx * 365;
    addPanel(pptx, slide, { left, top: 235, width: 300, height: 282 }, {
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
      addLine(pptx, slide, left + 24, 347 + labelIdx * 52, 4, 4, COLORS.accent);
    });
  });
  addSpeakerNotes(slide, slideData.speaker_note);
}

function buildContrastSlide(pptx, slideData) {
  const slide = pptx.addSlide();
  addBackground(pptx, slide);
  addText(slide, slideData.title, { left: 72, top: 102, width: 900, height: 70 }, {
    size: 42,
    bold: true,
    typeface: FONT.title,
  });

  const panels = slideData.id === 8
    ? [
        [slideData.onscreen[0], slideData.onscreen.slice(1, 5), COLORS.accent],
        [slideData.onscreen[5], slideData.onscreen.slice(6, 10), COLORS.risk],
      ]
    : [
        [slideData.onscreen[0], slideData.onscreen.slice(1, 6), COLORS.accent],
        [slideData.onscreen[6], slideData.onscreen.slice(7, 12), COLORS.risk],
      ];

  panels.forEach(([heading, labels, color], idx) => {
    const left = idx === 0 ? 104 : 690;
    addPanel(pptx, slide, { left, top: 218, width: 486, height: 322 }, {
      fill: COLORS.panel,
      lineFill: color,
    });
    addText(slide, heading, { left: left + 28, top: 248, width: 420, height: 48 }, {
      size: 30,
      bold: true,
      color,
      typeface: FONT.title,
    });
    labels.forEach((label, labelIdx) => {
      addText(slide, label, { left: left + 38, top: 322 + labelIdx * 42, width: 390, height: 30 }, {
        size: 21,
        color: COLORS.text,
      });
    });
  });
  addSpeakerNotes(slide, slideData.speaker_note);
}

function buildTestingPortfolio(pptx, slideData) {
  const slide = pptx.addSlide();
  addBackground(pptx, slide);
  addText(slide, slideData.title, { left: 72, top: 102, width: 980, height: 70 }, {
    size: 40,
    bold: true,
    typeface: FONT.title,
  });

  slideData.onscreen.forEach((label, idx) => {
    const row = Math.floor(idx / 3);
    const col = idx % 3;
    const left = 96 + col * 365;
    const top = 232 + row * 152;
    addPanel(pptx, slide, { left, top, width: 310, height: 112 }, {
      fill: idx === 5 ? "#102C3A" : COLORS.panel,
      lineFill: idx === 5 ? COLORS.accent : COLORS.line,
    });
    const [head, ...rest] = String(label).split(":");
    addText(slide, head, { left: left + 22, top: top + 18, width: 266, height: 30 }, {
      size: 22,
      bold: true,
      color: idx === 5 ? COLORS.accent2 : COLORS.text,
    });
    addText(slide, rest.join(":").trim(), { left: left + 22, top: top + 54, width: 266, height: 36 }, {
      size: 18,
      color: COLORS.muted,
    });
  });
  addSpeakerNotes(slide, slideData.speaker_note);
}

function buildPatchSla(pptx, slideData) {
  const slide = pptx.addSlide();
  addBackground(pptx, slide);
  addText(slide, slideData.onscreen[0], { left: 72, top: 102, width: 400, height: 70 }, {
    size: 48,
    bold: true,
    typeface: FONT.title,
  });
  addText(slide, slideData.onscreen[1], { left: 76, top: 172, width: 600, height: 44 }, {
    size: 27,
    color: COLORS.accent2,
  });

  slideData.onscreen.slice(2, 5).forEach((label, idx) => {
    addPill(pptx, slide, label, 690 + idx * 140, 170, 120, COLORS.accent);
  });

  const flow = slideData.onscreen.slice(5, 11);
  flow.forEach((label, idx) => {
    const isDecision = label === "Decision";
    const left = 86 + idx * 184;
    const top = isDecision ? 285 : 310;
    const width = isDecision ? 192 : 132;
    const height = isDecision ? 112 : 72;
    addPanel(pptx, slide, { left: isDecision ? left - 20 : left, top, width, height }, {
      fill: isDecision ? "#122F3F" : COLORS.panel,
      lineFill: isDecision ? COLORS.accent : COLORS.line,
      lineWidth: isDecision ? 2.4 : 1.2,
    });
    addText(slide, label, { left: isDecision ? left - 10 : left + 8, top: top + 14, width: width - 16, height: height - 28 }, {
      size: isDecision ? 26 : 20,
      bold: true,
      align: "center",
      color: isDecision ? COLORS.accent2 : COLORS.text,
    });
    if (idx < flow.length - 1) addLine(pptx, slide, left + width + (isDecision ? -20 : 0), 346, 42, 2.5, COLORS.accent);
  });

  slideData.onscreen.slice(11).forEach((label, idx) => {
    addPill(pptx, slide, label, 246 + idx * 200, 505, 150, idx === 2 ? COLORS.risk : COLORS.accent);
  });
  addSpeakerNotes(slide, slideData.speaker_note);
}

function buildRoadmap(pptx, slideData) {
  const slide = pptx.addSlide();
  addBackground(pptx, slide);
  addText(slide, slideData.title, { left: 72, top: 102, width: 760, height: 70 }, {
    size: 44,
    bold: true,
    typeface: FONT.title,
  });

  const blocks = [
    [slideData.onscreen[0], slideData.onscreen[1]],
    [slideData.onscreen[2], slideData.onscreen[3]],
    [slideData.onscreen[4], slideData.onscreen[5]],
  ];
  blocks.forEach(([day, text], idx) => {
    const left = 114 + idx * 365;
    addPanel(pptx, slide, { left, top: 244, width: 300, height: 265 }, {
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
    addText(slide, text.replaceAll(" / ", "\n"), { left: left + 42, top: 352, width: 216, height: 110 }, {
      size: 22,
      align: "center",
      color: COLORS.muted,
    });
  });
  addSpeakerNotes(slide, slideData.speaker_note);
}

async function renderPdfAndPreviews(previewSlides) {
  await fs.rm(pdfPath, { force: true });
  await execFileAsync("libreoffice", [
    "--headless",
    "--convert-to",
    "pdf",
    "--outdir",
    outputDir,
    deckPath,
  ], { cwd: root });

  await fs.access(pdfPath);

  await fs.mkdir(previewDir, { recursive: true });
  const existingPreviewFiles = await fs.readdir(previewDir).catch(() => []);
  await Promise.all(existingPreviewFiles
    .filter((file) => /^slide-\d+\.png$/.test(file))
    .map((file) => fs.rm(path.join(previewDir, file), { force: true })));

  const previewFiles = [];
  for (const index of previewSlides) {
    const page = index + 1;
    const basePath = path.join(previewDir, `slide-${String(page).padStart(2, "0")}`);
    await execFileAsync("pdftoppm", [
      "-f",
      String(page),
      "-l",
      String(page),
      "-png",
      "-singlefile",
      "-scale-to",
      "960",
      pdfPath,
      basePath,
    ]);
    previewFiles.push(toRepoRelative(`${basePath}.png`));
  }

  return previewFiles;
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
  const pptx = createDeck();
  let slideCount = 0;
  for (const slideData of data.slides) {
    if (slideData.id === 1) buildTitleSlide(pptx, slideData);
    else if (slideData.id === 2) await buildDisclaimerSlide(pptx, slideData, data.metadata);
    else if ([3, 10, 14].includes(slideData.id)) buildBigStatement(pptx, slideData);
    else if (slideData.id === 4) buildInfrastructureSlide(pptx, slideData);
    else if (slideData.id === 5) buildScaleLadder(pptx, slideData);
    else if (slideData.id === 6) buildEvidenceChain(pptx, slideData);
    else if (slideData.id === 7) buildThreeColumnBridge(pptx, slideData);
    else if ([8, 9].includes(slideData.id)) buildContrastSlide(pptx, slideData);
    else if (slideData.id === 11) buildTestingPortfolio(pptx, slideData);
    else if (slideData.id === 12) buildPatchSla(pptx, slideData);
    else if (slideData.id === 13) buildRoadmap(pptx, slideData);
    else throw new Error(`No builder for slide ${slideData.id}`);
    slideCount += 1;
  }

  if (slideCount !== 14) {
    throw new Error(`Expected 14 slides after build, got ${slideCount}`);
  }

  await pptx.writeFile({ fileName: deckPath, compression: true });

  const previewSlides = [0, 2, 4, 9, 11, 13];
  let previewFiles = [];
  let pdfExport = "PASS";
  try {
    previewFiles = await renderPdfAndPreviews(previewSlides);
  } catch (error) {
    pdfExport = `SKIPPED: ${error.message}`;
  }

  const report = {
    deckPath: toRepoRelative(deckPath),
    pdfPath: pdfExport === "PASS" ? toRepoRelative(pdfPath) : null,
    slideCount,
    timingSeconds: totalSeconds,
    timing: secondsToTime(totalSeconds),
    editableTextSource: "All visible talk text except the organizer disclaimer image is created as editable PowerPoint text/shapes.",
    buildEngine: "pptxgenjs with LibreOffice PDF export and Poppler preview rendering",
    hardConstraintGate: "PASS",
    pdfExport,
    previewFiles,
    keyText: [
      slideDataById(data, 3).onscreen[0],
      slideDataById(data, 5).onscreen[0],
      slideDataById(data, 10).onscreen[0],
      slideDataById(data, 12).onscreen[1],
      slideDataById(data, 14).onscreen[2],
    ],
  };
  await fs.writeFile(reportPath, JSON.stringify(report, null, 2), "utf-8");
  console.log(JSON.stringify(report, null, 2));
}

function slideDataById(data, id) {
  return data.slides.find((slide) => slide.id === id);
}

await buildDeck();
