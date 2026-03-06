/** Report writer — deterministic JSON output */

import { mkdirSync, writeFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import type { CliArgs, EcosystemReport } from "./types.js";
import type { RunResult } from "./runner.js";

export function buildReport(
  args: CliArgs,
  startedAt: string,
  elapsedMs: number,
  result: RunResult
): EcosystemReport {
  const phases: EcosystemReport["phases"] = {};

  if (result.fast) {
    phases.fast = result.fast;
  }
  if (result.deep) {
    phases.deep = result.deep;
  }

  const ok = Object.values(phases).every((p) => p.ok);

  return {
    tool: "ecosystem-qc",
    version: "0.3.0",
    mode: args.mode,
    root: resolve(args.root),
    ok,
    startedAt,
    elapsedMs,
    phases,
  };
}

export function writeReport(report: EcosystemReport, outPath: string): void {
  const absPath = resolve(outPath);
  mkdirSync(dirname(absPath), { recursive: true });

  // Deterministic JSON: keys are in declared order (V8 preserves insertion order)
  // Repos and checks are already sorted by the runner.
  const json = JSON.stringify(report, null, 2);
  writeFileSync(absPath, json + "\n", "utf-8");
}

export function writePartialReport(
  args: CliArgs,
  startedAt: string,
  result: Partial<RunResult>,
  outPath: string
): void {
  const elapsed = Math.round(performance.now());
  const report = buildReport(
    args,
    startedAt,
    elapsed,
    { fast: result.fast, deep: result.deep }
  );
  report.ok = false; // Interrupted = not ok
  writeReport(report, outPath);
}
