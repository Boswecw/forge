/** CLI argument parser — no external deps, just Bun.argv */

import type { CliArgs, Mode } from "./types.js";

const VALID_MODES: Mode[] = ["fast", "deep", "both"];

export function parseCli(argv: string[]): CliArgs {
  const args: CliArgs = {
    root: "/home/charlie/Forge/ecosystem",
    mode: "both",
    only: [],
    skip: [],
    failFast: false,
    continueOnFastFail: false,
    concurrency: 2,
    out: "out/ecosystem-qc.report.json",
  };

  for (const arg of argv) {
    if (arg.startsWith("--root=")) {
      args.root = arg.slice("--root=".length);
    } else if (arg.startsWith("--mode=")) {
      const mode = arg.slice("--mode=".length) as Mode;
      if (!VALID_MODES.includes(mode)) {
        throw new Error(`Invalid mode: ${mode}. Must be one of: ${VALID_MODES.join(", ")}`);
      }
      args.mode = mode;
    } else if (arg.startsWith("--only=")) {
      args.only = arg.slice("--only=".length).split(",").filter(Boolean);
    } else if (arg.startsWith("--skip=")) {
      args.skip = arg.slice("--skip=".length).split(",").filter(Boolean);
    } else if (arg === "--fail-fast") {
      args.failFast = true;
    } else if (arg === "--continue-on-fast-fail") {
      args.continueOnFastFail = true;
    } else if (arg.startsWith("--concurrency=")) {
      const n = parseInt(arg.slice("--concurrency=".length), 10);
      if (isNaN(n) || n < 1) {
        throw new Error("--concurrency must be a positive integer");
      }
      args.concurrency = n;
    } else if (arg.startsWith("--out=")) {
      args.out = arg.slice("--out=".length);
    }
  }

  return args;
}
