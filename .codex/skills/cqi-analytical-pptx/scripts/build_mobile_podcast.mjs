#!/usr/bin/env node
import { createHash } from "node:crypto";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { basename } from "node:path";

function arg(name, fallback = null) {
  const idx = process.argv.indexOf(`--${name}`);
  return idx >= 0 ? process.argv[idx + 1] : fallback;
}

function hasFlag(name) {
  return process.argv.includes(`--${name}`);
}

function sha256(path) {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

const manifestPath = arg("manifest");
if (!manifestPath || !existsSync(manifestPath)) {
  console.error("Usage: build_mobile_podcast.mjs --manifest <manifest.json> [--dry-run] [--output-manifest <path>]");
  process.exit(2);
}

const manifest = JSON.parse(readFileSync(manifestPath, "utf8"));
const chapters = manifest.chapters || [];
const expectedSlideCount = Number(manifest.expected_slide_count || 0);
const failures = [];

if (!expectedSlideCount) failures.push("expected_slide_count is required");
if (chapters.length !== expectedSlideCount) {
  failures.push(`chapter count ${chapters.length} != expected slide count ${expectedSlideCount}`);
}
for (const [idx, chapter] of chapters.entries()) {
  for (const field of ["slide", "title", "question", "population", "denominator", "data_problem", "conclusion"]) {
    if (!chapter[field]) failures.push(`chapter ${idx + 1}: missing ${field}`);
  }
}

if (manifest.audio_file) {
  if (!existsSync(manifest.audio_file)) {
    failures.push(`audio_file not found: ${manifest.audio_file}`);
  } else if (!/\.mp3$/i.test(manifest.audio_file)) {
    failures.push("audio_file must be MP3");
  }
} else if (!hasFlag("dry-run")) {
  failures.push("audio_file is required unless --dry-run is used");
}

if (failures.length) {
  console.error(`[FAIL] podcast manifest invalid: ${manifestPath}`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

const output = {
  deck_id: manifest.deck_id || basename(manifestPath, ".json"),
  expected_slide_count: expectedSlideCount,
  chapter_count: chapters.length,
  format: manifest.audio_file ? "mp3 mono 22.05kHz 96kbps expected" : "dry-run",
  audio_file: manifest.audio_file || null,
  audio_sha256: manifest.audio_file ? sha256(manifest.audio_file) : null,
  generated_by: "cqi-analytical-pptx/build_mobile_podcast.mjs",
};

const outputManifest = arg("output-manifest");
if (outputManifest) writeFileSync(outputManifest, `${JSON.stringify(output, null, 2)}\n`);

console.log(`[OK] podcast ${hasFlag("dry-run") ? "dry-run" : "manifest"} valid: ${chapters.length} chapters`);
