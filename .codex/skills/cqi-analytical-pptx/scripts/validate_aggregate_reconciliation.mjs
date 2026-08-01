#!/usr/bin/env node
import { existsSync, readFileSync } from "node:fs";

function arg(name) {
  const idx = process.argv.indexOf(`--${name}`);
  return idx >= 0 ? process.argv[idx + 1] : null;
}

const forbiddenColumns = new Set([
  "person_id",
  "member_id",
  "account_id",
  "customer_id",
  "phone",
  "email",
  "passport",
  "national_id",
]);

function sum(values) {
  return values.reduce((acc, value) => acc + Number(value || 0), 0);
}

function validateCheck(check) {
  const failures = [];
  const label = check.label || check.type;
  if (check.type === "parent_subset" && Number(check.subset) > Number(check.parent)) {
    failures.push(`${label}: subset ${check.subset} exceeds parent ${check.parent}`);
  }
  if (check.type === "mutually_exclusive_sum" && sum(check.buckets || []) !== Number(check.total)) {
    failures.push(`${label}: buckets sum ${sum(check.buckets || [])} != total ${check.total}`);
  }
  if (check.type === "monthly_stack") {
    for (const row of check.rows || []) {
      if (sum(row.buckets || []) !== Number(row.total)) {
        failures.push(`${label}: ${row.month || "month"} buckets sum ${sum(row.buckets || [])} != total ${row.total}`);
      }
    }
  }
  if (check.type === "tier_exclusivity") {
    for (const entity of check.entities || []) {
      if ((entity.tiers || []).length > 1) {
        failures.push(`${label}: ${entity.entity || "entity"} has multiple tiers in one cut`);
      }
    }
  }
  if (check.type === "forbidden_export_columns") {
    for (const column of check.columns || []) {
      if (forbiddenColumns.has(String(column).toLowerCase())) {
        failures.push(`${label}: forbidden person-level column exported: ${column}`);
      }
    }
  }
  if (check.type === "candidate_universe" && Number(check.candidate_events) > Number(check.base_universe)) {
    failures.push(`${label}: candidate events ${check.candidate_events} exceed base universe ${check.base_universe}`);
  }
  if (check.type === "slide_count" && Number(check.actual) !== Number(check.expected)) {
    failures.push(`${label}: slide count ${check.actual} != expected ${check.expected}`);
  }
  return failures;
}

const specPath = arg("spec");
if (!specPath || !existsSync(specPath)) {
  console.error("Usage: validate_aggregate_reconciliation.mjs --spec <checks.json>");
  process.exit(2);
}

const spec = JSON.parse(readFileSync(specPath, "utf8"));
const checks = Array.isArray(spec) ? spec : spec.checks || [];
const failures = checks.flatMap(validateCheck);

if (failures.length) {
  console.error(`[FAIL] aggregate reconciliation failed for ${specPath}`);
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`[OK] ${specPath}: ${checks.length} aggregate reconciliation checks passed`);
