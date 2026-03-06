/** Git status preflight check */

import type { CheckResult, RepoQcConfig } from "../types.js";
import { exec } from "../util/exec.js";
import { truncate } from "../util/truncate.js";

export async function checkGitStatus(
  repoPath: string,
  config: RepoQcConfig
): Promise<CheckResult> {
  const cmd = "git status --porcelain";
  const result = await exec(cmd, { cwd: repoPath, timeoutMs: 10_000 });

  const dirty = result.ok && result.stdout.trim().length > 0;
  const fatal = config.enforceCleanWorkingTree && dirty;

  return {
    name: "gitStatus",
    ok: !fatal,
    cmd,
    ms: result.ms,
    stdout: truncate(result.stdout),
    stderr: truncate(result.stderr),
    warning: dirty && !fatal ? true : undefined,
  };
}
