#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { existsSync } from "node:fs";
import { basename } from "node:path";

function arg(name, fallback = null) {
  const idx = process.argv.indexOf(`--${name}`);
  return idx >= 0 ? process.argv[idx + 1] : fallback;
}

function zipList(deck) {
  return execFileSync("unzip", ["-Z1", deck], { encoding: "utf8" })
    .split(/\r?\n/)
    .filter(Boolean);
}

function zipText(deck, entry) {
  return execFileSync("unzip", ["-p", deck, entry], { encoding: "utf8" });
}

function slideNumber(entry) {
  const match = entry.match(/slide(\d+)\.xml$/);
  return match ? Number(match[1]) : 0;
}

function presentationCanvas(deck) {
  const xml = zipText(deck, "ppt/presentation.xml");
  const match = xml.match(/<p:sldSz[^>]*cx="(\d+)"[^>]*cy="(\d+)"/);
  return match ? { cx: Number(match[1]), cy: Number(match[2]) } : null;
}

function textRuns(xml) {
  const runs = [];
  const shapeRegex = /<p:sp[\s\S]*?<\/p:sp>/g;
  for (const shape of xml.matchAll(shapeRegex)) {
    const block = shape[0];
    const off = block.match(/<a:off[^>]*x="(-?\d+)"[^>]*y="(-?\d+)"/);
    const y = off ? Number(off[2]) : 0;
    for (const run of block.matchAll(/<a:r\b[\s\S]*?<\/a:r>/g)) {
      const r = run[0];
      const size = r.match(/<a:rPr[^>]*\bsz="(\d+)"/);
      const text = [...r.matchAll(/<a:t>([\s\S]*?)<\/a:t>/g)].map((m) => m[1]).join("");
      if (size && text.trim()) runs.push({ text: text.trim(), pt: Number(size[1]) / 100, y });
    }
  }
  return runs;
}

const deck = arg("deck");
if (!deck || !existsSync(deck)) {
  console.error("Usage: audit_pptx_readability.mjs --deck <deck.pptx> [--min-body-pt 16] [--min-label-pt 12] [--min-metadata-pt 10]");
  process.exit(2);
}

const minBody = Number(arg("min-body-pt", "16"));
const minLabel = Number(arg("min-label-pt", "12"));
const minMetadata = Number(arg("min-metadata-pt", "10"));
const canvas = presentationCanvas(deck);
const footerY = canvas ? canvas.cy * 0.9 : Number.POSITIVE_INFINITY;
const entries = zipList(deck)
  .filter((e) => /^ppt\/slides\/slide\d+\.xml$/.test(e))
  .sort((a, b) => slideNumber(a) - slideNumber(b));
const failures = [];
let checked = 0;

for (const entry of entries) {
  const runs = textRuns(zipText(deck, entry));
  for (const run of runs) {
    checked += 1;
    const roleMin = run.y >= footerY ? minMetadata : run.text.length <= 24 ? minLabel : minBody;
    if (run.pt < roleMin) {
      failures.push(`${basename(entry)}: ${run.pt} pt below ${roleMin} pt for "${run.text.slice(0, 50)}"`);
    }
  }
}

if (failures.length) {
  console.error(`[FAIL] readability audit failed for ${deck}`);
  for (const failure of failures.slice(0, 100)) console.error(`- ${failure}`);
  if (failures.length > 100) console.error(`- ... ${failures.length - 100} more`);
  process.exit(1);
}

console.log(`[OK] ${deck}: ${checked} explicit text runs meet readability thresholds`);
