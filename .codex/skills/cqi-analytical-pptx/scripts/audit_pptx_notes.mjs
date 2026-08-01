#!/usr/bin/env node
import { execFileSync } from "node:child_process";
import { existsSync } from "node:fs";
import { basename } from "node:path";

function arg(name) {
  const idx = process.argv.indexOf(`--${name}`);
  return idx >= 0 ? process.argv[idx + 1] : null;
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
  const match = entry.match(/(\d+)\.xml$/);
  return match ? Number(match[1]) : 0;
}

function textFromXml(xml) {
  return [...xml.matchAll(/<a:t>([\s\S]*?)<\/a:t>/g)]
    .map((m) => m[1].replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&amp;/g, "&"))
    .join("\n");
}

const requiredFields = [
  "Source:",
  "Window:",
  "Grain:",
  "Population:",
  "Denominator:",
  "Association:",
  "Deduplication:",
  "Evidence status:",
  "Limitation:",
  "Allowed conclusion:",
];

const deck = arg("deck");
if (!deck || !existsSync(deck)) {
  console.error("Usage: audit_pptx_notes.mjs --deck <deck.pptx>");
  process.exit(2);
}

const entries = zipList(deck);
const slideEntries = entries.filter((e) => /^ppt\/slides\/slide\d+\.xml$/.test(e));
const noteEntries = entries
  .filter((e) => /^ppt\/notesSlides\/notesSlide\d+\.xml$/.test(e))
  .sort((a, b) => slideNumber(a) - slideNumber(b));
const failures = [];

if (noteEntries.length !== slideEntries.length) {
  failures.push(`notes ${noteEntries.length} != slides ${slideEntries.length}`);
}

for (const entry of noteEntries) {
  const text = textFromXml(zipText(deck, entry));
  const label = basename(entry);
  if (!text.includes("[Evidence]") || !text.includes("[/Evidence]")) {
    failures.push(`${label}: missing [Evidence] block`);
    continue;
  }
  const block = text.slice(text.indexOf("[Evidence]"), text.indexOf("[/Evidence]") + "[/Evidence]".length);
  for (const field of requiredFields) {
    if (!block.includes(field)) failures.push(`${label}: missing field ${field}`);
  }
  if (/BLOCKED_DATA|BLOCKED_AUTH|BLOQUEADO/.test(text)) {
    failures.push(`${label}: forbidden stakeholder evidence state in notes`);
  }
}

if (failures.length) {
  console.error(`[FAIL] note evidence contract failed for ${deck}`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`[OK] ${deck}: ${noteEntries.length} notes include required evidence blocks`);
