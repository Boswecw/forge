#!/usr/bin/env node
import fs from "node:fs";
import path from "node:path";

const filePath =
  process.argv[2] ||
  "docs/contracts/forge_command_connectivity_acceptance_gate.v1.checklist.json";

function die(msg, code = 2) {
  console.error(msg);
  process.exit(code);
}

function norm(s) {
  return String(s ?? "").trim().toLowerCase();
}

let data;
try {
  const raw = fs.readFileSync(filePath, "utf8");
  data = JSON.parse(raw);
} catch (e) {
  die(
    `[validator] Failed to read/parse JSON: ${filePath}\n${e?.message || e}`,
  );
}

const gates = Array.isArray(data?.gates)
  ? data.gates
  : Array.isArray(data?.Gates)
    ? data.Gates
    : Array.isArray(data?.definitions)
      ? data.definitions
      : null;

if (!gates) {
  die(
    `[validator] Could not find gates array. Expected one of: data.gates | data.Gates | data.definitions\n` +
      `[validator] File: ${path.resolve(filePath)}`,
  );
}

const criticalFailures = [];
for (const g of gates) {
  const id = g?.id ?? g?.gate_id ?? g?.key ?? "(unknown)";
  const isCriticalBool = g?.critical === true;
  const criticality = norm(g?.criticality ?? g?.severity ?? g?.level);
  const status = norm(g?.status ?? g?.result ?? g?.state);
  const isCritical = isCriticalBool || criticality === "critical";

  if (isCritical && status !== "pass") {
    criticalFailures.push({
      id,
      status: g?.status ?? status,
      notes: g?.notes ?? g?.note ?? "",
      evidence:
        g?.required_evidence ?? g?.evidence_required ?? g?.evidence ?? [],
    });
  }
}

if (criticalFailures.length) {
  console.error(`[validator] Connectivity acceptance gate FAILED`);
  console.error(
    `[validator] Critical gate failures (${criticalFailures.length}):`,
  );
  for (const f of criticalFailures) {
    console.error(`- ${f.id}: status=${f.status}`);
    if (f.notes) console.error(`  notes: ${String(f.notes).slice(0, 240)}`);
    if (Array.isArray(f.evidence) && f.evidence.length) {
      console.error(
        `  required_evidence: ${f.evidence.join(", ").slice(0, 240)}`,
      );
    }
  }
  process.exit(1);
}

console.log(
  `[validator] Connectivity acceptance gate PASSED (no failing critical gates)`,
);
process.exit(0);
