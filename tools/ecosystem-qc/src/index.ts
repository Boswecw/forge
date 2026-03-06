#!/usr/bin/env bun
/** Ecosystem-QC v0.3.0 — Entry Point */

import { resolve } from "node:path";
import { parseCli } from "./cli.js";
import { discoverRepos } from "./discover.js";
import { runAll, type RunResult } from "./runner.js";
import { buildReport, writeReport, writePartialReport } from "./report.js";

/** Format a Date as local ISO 8601 with UTC offset, e.g. 2026-02-26T12:56:29-05:00 */
function localIso(d: Date): string {
  const off = d.getTimezoneOffset();
  const sign = off <= 0 ? "+" : "-";
  const absOff = Math.abs(off);
  const hh = String(Math.floor(absOff / 60)).padStart(2, "0");
  const mm = String(absOff % 60).padStart(2, "0");
  const local = new Date(d.getTime() - off * 60_000);
  return local.toISOString().replace("Z", `${sign}${hh}:${mm}`);
}

const args = parseCli(process.argv.slice(2));
const outPath = resolve(args.out);
const startedAt = localIso(new Date());
const t0 = performance.now();

// Partial result accumulator for SIGINT handling
let partialResult: Partial<RunResult> = {};

// ─── SIGINT handler: write partial report before exiting ─────────────────────

process.on("SIGINT", () => {
  console.error("\n⚠  SIGINT received — writing partial report…");
  try {
    writePartialReport(args, startedAt, partialResult, outPath);
    console.error(`   Report written to ${outPath}`);
  } catch (err) {
    console.error("   Failed to write partial report:", err);
  }
  process.exit(1);
});

// ─── Main ────────────────────────────────────────────────────────────────────

async function main(): Promise<void> {
  console.log(`🔧 ecosystem-qc v0.3.0  mode=${args.mode}  root=${args.root}`);
  console.log(`   concurrency=${args.concurrency}  failFast=${args.failFast}`);

  // Discover repos
  const repos = discoverRepos(args.root, args.only, args.skip);

  if (repos.length === 0) {
    console.error("❌ No repos discovered. Check --root, --only, --skip.");
    const report = buildReport(args, startedAt, 0, {});
    report.ok = false;
    writeReport(report, outPath);
    process.exit(1);
  }

  console.log(`   Found ${repos.length} repos: ${repos.map((r) => r.name).join(", ")}`);

  // Run phases
  const result = await runAll(repos, args);
  partialResult = result;

  const elapsedMs = Math.round(performance.now() - t0);

  // Build and write report
  const report = buildReport(args, startedAt, elapsedMs, result);
  writeReport(report, outPath);

  // Summary
  console.log("");
  printSummary(report);
  console.log(`\n📄 Report: ${outPath}`);

  process.exit(report.ok ? 0 : 1);
}

function printSummary(report: ReturnType<typeof buildReport>): void {
  const icon = report.ok ? "✅" : "❌";
  console.log(`${icon} Overall: ${report.ok ? "PASS" : "FAIL"}  (${report.elapsedMs}ms)`);

  for (const [phaseName, phase] of Object.entries(report.phases)) {
    if (!phase) continue;
    const pi = phase.ok ? "✅" : "❌";
    console.log(`\n  ${pi} Phase: ${phaseName}  (${phase.elapsedMs}ms)`);

    for (const repo of phase.repos) {
      const ri = repo.ok ? "  ✓" : "  ✗";
      const warns = repo.warnings.length > 0 ? ` ⚠ ${repo.warnings.join("; ")}` : "";
      console.log(`    ${ri} ${repo.name}${warns}`);

      for (const check of repo.checks) {
        if (check.skipped) {
          console.log(`       ⊘ ${check.name} (skipped: ${check.reason})`);
        } else if (!check.ok) {
          console.log(`       ✗ ${check.name} (${check.ms}ms)`);
          if (check.stderr) {
            const firstLine = check.stderr.split("\n")[0]?.slice(0, 120);
            if (firstLine) console.log(`         ${firstLine}`);
          }
        }
      }
    }
  }
}

main().catch((err) => {
  console.error("Fatal error:", err);
  try {
    writePartialReport(args, startedAt, partialResult, outPath);
  } catch {
    // Last resort — nothing we can do
  }
  process.exit(1);
});
