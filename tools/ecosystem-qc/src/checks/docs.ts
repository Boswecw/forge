/** Doc system build + git diff enforcement */

import type { CheckResult, RepoQcConfig } from "../types.js";
import { exec } from "../util/exec.js";
import { truncate } from "../util/truncate.js";

export async function checkDocBuild(
  repoPath: string,
  config: RepoQcConfig
): Promise<CheckResult | null> {
  const cmd = config.checks.docSystemBuild;
  if (!cmd) return null;

  const result = await exec(cmd, {
    cwd: repoPath,
    timeoutMs: config.timeoutsMs.docSystemBuild,
  });

  return {
    name: "docSystemBuild",
    ok: result.ok,
    cmd,
    ms: result.ms,
    stdout: truncate(result.stdout),
    stderr: truncate(result.stderr),
  };
}

export async function checkDocDiffClean(
  repoPath: string,
  config: RepoQcConfig
): Promise<CheckResult | null> {
  if (!config.checks.docSystemDiffClean) return null;

  const cmd = "git diff --exit-code -- doc/";
  const result = await exec(cmd, {
    cwd: repoPath,
    timeoutMs: config.timeoutsMs.docSystemDiffClean,
  });

  return {
    name: "docSystemDiffClean",
    ok: result.ok,
    cmd,
    ms: result.ms,
    stdout: truncate(result.stdout),
    stderr: result.ok
      ? ""
      : truncate("Doc build produced changes; commit required.\n" + result.stderr),
  };
}
