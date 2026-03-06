/** Runner — orchestrates FAST, DEEP, and BOTH phase execution */

import type {
  CliArgs,
  DiscoveredRepo,
  RepoQcConfig,
  RepoPhaseResult,
  PhaseResult,
  CheckResult,
  ArtifactRef,
} from "./types.js";
import { loadRepoConfig } from "./config.js";
import { checkGitStatus } from "./checks/git.js";
import { checkDocBuild, checkDocDiffClean } from "./checks/docs.js";
import { checkCargoCheck, checkCargoTest } from "./checks/rust.js";
import { checkNodeTest } from "./checks/node.js";
import { checkStateforge } from "./checks/stateforge.js";

// ─── Fast Phase ──────────────────────────────────────────────────────────────

async function runFastChecks(
  repo: DiscoveredRepo,
  config: RepoQcConfig
): Promise<RepoPhaseResult> {
  const checks: CheckResult[] = [];
  const warnings: string[] = [];
  const artifacts: ArtifactRef[] = [];
  let repoOk = true;

  // 1. gitStatus
  const git = await checkGitStatus(repo.path, config);
  checks.push(git);
  if (!git.ok) repoOk = false;
  if (git.warning) warnings.push("Working tree has uncommitted changes");

  // 2. docSystemBuild
  const docBuild = await checkDocBuild(repo.path, config);
  if (docBuild) {
    checks.push(docBuild);
    if (!docBuild.ok) repoOk = false;
  }

  // 3. docSystemDiffClean
  if (docBuild?.ok) {
    const docDiff = await checkDocDiffClean(repo.path, config);
    if (docDiff) {
      checks.push(docDiff);
      if (!docDiff.ok) repoOk = false;
    }
  }

  // 4. stateforge
  const sf = await checkStateforge(repo.path, config);
  if (sf) {
    checks.push(sf.check);
    if (!sf.check.ok) repoOk = false;
    if (sf.artifact) artifacts.push(sf.artifact);
  }

  // Deterministic: sort checks by name
  checks.sort((a, b) => a.name.localeCompare(b.name));

  return {
    name: repo.name,
    path: repo.path,
    ok: repoOk,
    warnings,
    checks,
    artifacts: artifacts.length > 0 ? artifacts : undefined,
  };
}

// ─── Deep Phase ──────────────────────────────────────────────────────────────

async function runDeepChecks(
  repo: DiscoveredRepo,
  config: RepoQcConfig,
  includeFastFirst: boolean
): Promise<{ fast?: RepoPhaseResult; deep: RepoPhaseResult }> {
  let fastResult: RepoPhaseResult | undefined;

  // If deep-only mode, run fast checks first as part of the pipeline
  if (includeFastFirst) {
    fastResult = await runFastChecks(repo, config);
  }

  const checks: CheckResult[] = [];
  const artifacts: ArtifactRef[] = [];
  let repoOk = true;

  // 5. cargoCheck
  const cc = await checkCargoCheck(repo.path, config);
  if (cc) {
    checks.push(cc);
    if (!cc.ok) repoOk = false;
  }

  // 6. cargoTest
  const ct = await checkCargoTest(repo.path, config);
  if (ct) {
    checks.push(ct);
    if (!ct.ok) repoOk = false;
  }

  // 7. nodeTest (only if explicitly configured)
  const nt = await checkNodeTest(repo.path, config);
  if (nt) {
    checks.push(nt);
    if (!nt.ok) repoOk = false;
  }

  // Deterministic: sort checks by name
  checks.sort((a, b) => a.name.localeCompare(b.name));

  return {
    fast: fastResult,
    deep: {
      name: repo.name,
      path: repo.path,
      ok: repoOk,
      warnings: [],
      checks,
      artifacts: artifacts.length > 0 ? artifacts : undefined,
    },
  };
}

// ─── Concurrency Pool ────────────────────────────────────────────────────────

async function runWithConcurrency<T>(
  items: T[],
  concurrency: number,
  fn: (item: T) => Promise<void>
): Promise<void> {
  const queue = [...items];
  const workers: Promise<void>[] = [];

  for (let i = 0; i < Math.min(concurrency, items.length); i++) {
    workers.push(
      (async () => {
        while (queue.length > 0) {
          const item = queue.shift();
          if (item !== undefined) {
            await fn(item);
          }
        }
      })()
    );
  }

  await Promise.all(workers);
}

// ─── Phase Runners ───────────────────────────────────────────────────────────

export async function runFastPhase(
  repos: DiscoveredRepo[],
  args: CliArgs
): Promise<PhaseResult> {
  const start = performance.now();
  const results: RepoPhaseResult[] = [];

  for (const repo of repos) {
    const config = loadRepoConfig(repo.path);
    if (!config.phases.enableFast) continue;

    const result = await runFastChecks(repo, config);
    results.push(result);

    if (args.failFast && !result.ok) break;
  }

  // Deterministic sort
  results.sort((a, b) => a.name.localeCompare(b.name));

  return {
    ok: results.every((r) => r.ok),
    elapsedMs: Math.round(performance.now() - start),
    repos: results,
  };
}

export async function runDeepPhase(
  repos: DiscoveredRepo[],
  args: CliArgs,
  priorFastResults?: Map<string, RepoPhaseResult>
): Promise<PhaseResult> {
  const start = performance.now();
  const results: RepoPhaseResult[] = [];
  let aborted = false;

  const eligibleRepos = repos.filter((repo) => {
    const config = loadRepoConfig(repo.path);
    return config.phases.enableDeep;
  });

  const processRepo = async (repo: DiscoveredRepo) => {
    if (aborted) return;

    const config = loadRepoConfig(repo.path);

    // In "both" mode, check if fast failed
    if (priorFastResults) {
      const fastResult = priorFastResults.get(repo.name);
      if (fastResult && !fastResult.ok && !args.continueOnFastFail) {
        // Mark deep as skipped
        results.push({
          name: repo.name,
          path: repo.path,
          ok: false,
          warnings: [],
          checks: [
            {
              name: "deepPhase",
              ok: false,
              ms: 0,
              stdout: "",
              stderr: "",
              skipped: true,
              reason: "fast_failed",
            },
          ],
        });
        return;
      }
    }

    // includeFastFirst = true only in --mode=deep (no prior fast run)
    const includeFastFirst = !priorFastResults;
    const result = await runDeepChecks(repo, config, includeFastFirst);
    results.push(result.deep);

    if (args.failFast && !result.deep.ok) {
      aborted = true;
    }
  };

  if (args.concurrency <= 1) {
    for (const repo of eligibleRepos) {
      await processRepo(repo);
      if (aborted) break;
    }
  } else {
    await runWithConcurrency(eligibleRepos, args.concurrency, processRepo);
  }

  // Deterministic sort
  results.sort((a, b) => a.name.localeCompare(b.name));

  return {
    ok: results.every((r) => r.ok),
    elapsedMs: Math.round(performance.now() - start),
    repos: results,
  };
}

// ─── Mode Dispatch ───────────────────────────────────────────────────────────

export interface RunResult {
  fast?: PhaseResult;
  deep?: PhaseResult;
}

export async function runAll(
  repos: DiscoveredRepo[],
  args: CliArgs
): Promise<RunResult> {
  const result: RunResult = {};

  if (args.mode === "fast") {
    result.fast = await runFastPhase(repos, args);
  } else if (args.mode === "deep") {
    // Deep mode runs fast+deep as one pipeline per repo
    result.deep = await runDeepPhase(repos, args);
  } else {
    // "both" — run fast first, then deep with skip logic
    result.fast = await runFastPhase(repos, args);

    // Build lookup of fast results
    const fastMap = new Map<string, RepoPhaseResult>();
    if (result.fast) {
      for (const r of result.fast.repos) {
        fastMap.set(r.name, r);
      }
    }

    result.deep = await runDeepPhase(repos, args, fastMap);
  }

  return result;
}
