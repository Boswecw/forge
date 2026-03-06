/** Node test check — only runs if explicitly configured */

import type { CheckResult, RepoQcConfig } from "../types.js";
import { exec } from "../util/exec.js";
import { truncate } from "../util/truncate.js";

export async function checkNodeTest(
  repoPath: string,
  config: RepoQcConfig
): Promise<CheckResult | null> {
  const cmd = config.checks.nodeTest;
  if (!cmd) return null;

  const result = await exec(cmd, {
    cwd: repoPath,
    timeoutMs: config.timeoutsMs.nodeTest,
  });

  return {
    name: "nodeTest",
    ok: result.ok,
    cmd,
    ms: result.ms,
    stdout: truncate(result.stdout),
    stderr: truncate(result.stderr),
  };
}
