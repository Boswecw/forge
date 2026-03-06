/** Ecosystem-QC v0.3.0 — Shared Types */

export type Mode = "fast" | "deep" | "both";

export interface CliArgs {
  root: string;
  mode: Mode;
  only: string[];
  skip: string[];
  failFast: boolean;
  continueOnFastFail: boolean;
  concurrency: number;
  out: string;
}

export interface RepoQcConfig {
  checks: {
    docSystemBuild?: string;
    docSystemDiffClean?: boolean;
    stateforge?: string;
    cargoCheck?: string;
    cargoTest?: string;
    nodeTest?: string;
  };
  timeoutsMs: {
    docSystemBuild: number;
    docSystemDiffClean: number;
    stateforge: number;
    cargoCheck: number;
    cargoTest: number;
    nodeTest: number;
  };
  phases: {
    enableFast: boolean;
    enableDeep: boolean;
  };
  enforceCleanWorkingTree: boolean;
}

export interface ExecResult {
  ok: boolean;
  exitCode: number;
  stdout: string;
  stderr: string;
  ms: number;
  timedOut: boolean;
}

export interface CheckResult {
  name: string;
  ok: boolean;
  cmd?: string;
  ms: number;
  stdout: string;
  stderr: string;
  skipped?: boolean;
  reason?: string;
  warning?: boolean;
}

export interface ArtifactRef {
  path: string;
  sha256: string;
}

export interface RepoPhaseResult {
  name: string;
  path: string;
  ok: boolean;
  warnings: string[];
  checks: CheckResult[];
  artifacts?: ArtifactRef[];
}

export interface PhaseResult {
  ok: boolean;
  elapsedMs: number;
  repos: RepoPhaseResult[];
}

export interface EcosystemReport {
  tool: "ecosystem-qc";
  version: "0.3.0";
  mode: Mode;
  root: string;
  ok: boolean;
  startedAt: string;
  elapsedMs: number;
  phases: {
    fast?: PhaseResult;
    deep?: PhaseResult;
  };
}

export interface DiscoveredRepo {
  name: string;
  path: string;
}
