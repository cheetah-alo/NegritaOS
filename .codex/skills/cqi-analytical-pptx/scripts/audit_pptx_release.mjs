#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { basename } from "node:path";

function arg(name, fallback = null) {
  const idx = process.argv.indexOf(`--${name}`);
  return idx >= 0 ? process.argv[idx + 1] : fallback;
}

function args(name) {
  const values = [];
  for (let i = 0; i < process.argv.length; i += 1) {
    if (process.argv[i] === `--${name}`) values.push(process.argv[i + 1]);
  }
  return values.filter(Boolean);
}

function usage() {
  console.error("Usage: audit_pptx_release.mjs --deck <deck.pptx> [--expected-slide-count N] [--expected-note-count N] [--forbidden-term TERM]");
  process.exit(2);
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

function textFromXml(xml) {
  return [...xml.matchAll(/<a:t>([\s\S]*?)<\/a:t>/g)]
    .map((m) => m[1].replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&"))
    .join("\n");
}

function presentationCanvas(deck) {
  const xml = zipText(deck, "ppt/presentation.xml");
  const match = xml.match(/<p:sldSz[^>]*cx="(\d+)"[^>]*cy="(\d+)"/);
  if (!match) return null;
  return { cx: Number(match[1]), cy: Number(match[2]) };
}

function outOfCanvasShapes(deck, slideEntries, canvas) {
  if (!canvas) return [];
  const failures = [];
  for (const entry of slideEntries) {
    const xml = zipText(deck, entry);
    const shapeRegex = /<p:sp[\s\S]*?<\/p:sp>|<p:pic[\s\S]*?<\/p:pic>|<p:graphicFrame[\s\S]*?<\/p:graphicFrame>/g;
    for (const match of xml.matchAll(shapeRegex)) {
      const block = match[0];
      const off = block.match(/<a:off[^>]*x="(-?\d+)"[^>]*y="(-?\d+)"/);
      const ext = block.match(/<a:ext[^>]*cx="(\d+)"[^>]*cy="(\d+)"/);
      if (!off || !ext) continue;
      const x = Number(off[1]);
      const y = Number(off[2]);
      const cx = Number(ext[1]);
      const cy = Number(ext[2]);
      if (x < 0 || y < 0 || x + cx > canvas.cx || y + cy > canvas.cy) {
        failures.push(`${basename(entry)} shape outside canvas x=${x} y=${y} cx=${cx} cy=${cy}`);
      }
    }
  }
  return failures;
}

const deck = arg("deck");
if (!deck) usage();
if (!existsSync(deck)) {
  console.error(`[FAIL] deck not found: ${deck}`);
  process.exit(1);
}

const expectedSlideCount = arg("expected-slide-count");
const expectedNoteCount = arg("expected-note-count");
const forbiddenTerms = [
  "BLOCKED_DATA",
  "BLOCKED_AUTH",
  "BLOQUEADO",
  "Click to add",
  "Lorem ipsum",
  ...args("forbidden-term"),
];
const manifestPath = arg("manifest");
let manifest = null;
if (manifestPath) {
  manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
}

const entries = zipList(deck);
const slideEntries = entries
  .filter((e) => /^ppt\/slides\/slide\d+\.xml$/.test(e))
  .sort((a, b) => slideNumber(a) - slideNumber(b));
const noteEntries = entries
  .filter((e) => /^ppt\/notesSlides\/notesSlide\d+\.xml$/.test(e))
  .sort((a, b) => slideNumber(a) - slideNumber(b));
const canvas = presentationCanvas(deck);
const allText = [...slideEntries, ...noteEntries].map((entry) => textFromXml(zipText(deck, entry))).join("\n");
const failures = [];

const slideCount = slideEntries.length;
const noteCount = noteEntries.length;
const slideTarget = expectedSlideCount ?? manifest?.expected_slide_count;
const noteTarget = expectedNoteCount ?? manifest?.expected_note_count;

if (slideTarget && slideCount !== Number(slideTarget)) {
  failures.push(`slide count ${slideCount} != expected ${slideTarget}`);
}
if (noteTarget && noteCount !== Number(noteTarget)) {
  failures.push(`note count ${noteCount} != expected ${noteTarget}`);
}
for (const term of forbiddenTerms) {
  if (term && allText.includes(term)) failures.push(`forbidden term found: ${term}`);
}
for (const entry of slideEntries) {
  const text = textFromXml(zipText(deck, entry));
  if (/Click to add|Lorem ipsum/i.test(text)) failures.push(`placeholder text found in ${basename(entry)}`);
}
failures.push(...outOfCanvasShapes(deck, slideEntries, canvas));

if (failures.length) {
  console.error(`[FAIL] ${deck}`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`[OK] ${deck}: ${slideCount} slides, ${noteCount} notes, canvas ${canvas ? `${canvas.cx}x${canvas.cy}` : "unknown"}, release checks passed`);
