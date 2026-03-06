/** Rust checks — cargo check + cargo test */

import type { CheckResult, RepoQcConfig } from "../types.js";
import { exec } from "../util/exec.js";
import { truncate } from "../util/truncate.js";

export async function checkCargoCheck(
  repoPath: string,
  config: RepoQcConfig
): Promise<CheckResult | null> {
  const cmd = config.checks.cargoCheck;
  if (!cmd) return null;

  const result = await exec(cmd, {
    cwd: repoPath,
    timeoutMs: config.timeoutsMs.cargoCheck,
  });

  return {
    name: "cargoCheck",
    ok: result.ok,
    cmd,
    ms: result.ms,
    stdout: truncate(result.stdout),
    stderr: truncate(result.stderr),
  };
}

export async function checkCargoTest(
  repoPath: string,
  config: RepoQcConfig
): Promise<CheckResult | null> {
  const cmd = config.checks.cargoTest;
  if (!cmd) return null;

  const result = await exec(cmd, {
    cwd: repoPath,
    timeoutMs: config.timeoutsMs.cargoTest,
  });

  return {
    name: "cargoTest",
    ok: result.ok,
    cmd,
    ms: result.ms,
    stdout: truncate(result.stdout),
    stderr: truncate(result.stderr),
  };
}
