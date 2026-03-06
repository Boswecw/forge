/** StateForge check + artifact collection */

import { join } from "node:path";
import type { CheckResult, ArtifactRef, RepoQcConfig } from "../types.js";
import { exec } from "../util/exec.js";
import { truncate } from "../util/truncate.js";
import { isFile } from "../util/fs.js";
import { sha256File } from "../util/hash.js";

export async function checkStateforge(
  repoPath: string,
  config: RepoQcConfig
): Promise<{ check: CheckResult; artifact?: ArtifactRef } | null> {
  const cmd = config.checks.stateforge;
  if (!cmd) return null;

  const result = await exec(cmd, {
    cwd: repoPath,
    timeoutMs: config.timeoutsMs.stateforge,
  });

  const check: CheckResult = {
    name: "stateforge",
    ok: result.ok,
    cmd,
    ms: result.ms,
    stdout: truncate(result.stdout),
    stderr: truncate(result.stderr),
  };

  // Collect artifact if present
  let artifact: ArtifactRef | undefined;
  const reportPath = join(repoPath, "tools/stateforge/out/stateforge.report.json");
  if (isFile(reportPath)) {
    artifact = {
      path: reportPath,
      sha256: sha256File(reportPath),
    };
  }

  return { check, artifact };
}
