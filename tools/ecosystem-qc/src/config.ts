/** Per-repo config — load .forgeqc.json or auto-detect */

import { join } from "node:path";
import { readFileSync } from "node:fs";
import type { RepoQcConfig } from "./types.js";
import { isFile, readJsonFile } from "./util/fs.js";

const DEFAULT_TIMEOUTS: RepoQcConfig["timeoutsMs"] = {
  docSystemBuild: 60_000,
  docSystemDiffClean: 30_000,
  stateforge: 60_000,
  cargoCheck: 300_000,
  cargoTest: 900_000,
  nodeTest: 600_000,
};

export function loadRepoConfig(repoPath: string): RepoQcConfig {
  const configPath = join(repoPath, ".forgeqc.json");
  const override = readJsonFile<Partial<RepoQcConfig>>(configPath);

  const config: RepoQcConfig = {
    checks: {},
    timeoutsMs: { ...DEFAULT_TIMEOUTS },
    phases: { enableFast: true, enableDeep: true },
    enforceCleanWorkingTree: false,
  };

  if (override) {
    // Merge checks
    if (override.checks) {
      config.checks = { ...config.checks, ...override.checks };
    }
    // Merge timeouts
    if (override.timeoutsMs) {
      config.timeoutsMs = { ...config.timeoutsMs, ...override.timeoutsMs };
    }
    // Merge phases
    if (override.phases) {
      config.phases = { ...config.phases, ...override.phases };
    }
    if (override.enforceCleanWorkingTree !== undefined) {
      config.enforceCleanWorkingTree = override.enforceCleanWorkingTree;
    }
    return config;
  }

  // Auto-detect if no config file
  autoDetect(repoPath, config);

  return config;
}

function autoDetect(repoPath: string, config: RepoQcConfig): void {
  // --- Docs ---
  const buildScript = join(repoPath, "doc/system/BUILD.sh");
  if (isFile(buildScript)) {
    config.checks.docSystemBuild = "bash doc/system/BUILD.sh";
    config.checks.docSystemDiffClean = true;
  }

  // --- Rust ---
  const tauriCargo = join(repoPath, "src-tauri/Cargo.toml");
  const rootCargo = join(repoPath, "Cargo.toml");

  if (isFile(tauriCargo)) {
    const manifest = "src-tauri/Cargo.toml";
    const hasLib = cargoHasLib(tauriCargo);
    const libFlag = hasLib ? " --lib" : "";
    config.checks.cargoCheck =
      `cargo check --manifest-path ${manifest}${libFlag}`;
    config.checks.cargoTest =
      `cargo test --manifest-path ${manifest}${libFlag} -q`;
  } else if (isFile(rootCargo)) {
    const hasLib = cargoHasLib(rootCargo);
    const libFlag = hasLib ? " --lib" : "";
    config.checks.cargoCheck = `cargo check${libFlag}`;
    config.checks.cargoTest = `cargo test${libFlag} -q`;
  }

  // --- StateForge ---
  const sfPkg = join(repoPath, "tools/stateforge/package.json");
  if (isFile(sfPkg)) {
    config.checks.stateforge = "bun run stateforge";
  }

  // --- Node (only if bun lock exists — conservative default) ---
  const bunLockB = join(repoPath, "bun.lockb");
  const bunLock = join(repoPath, "bun.lock");
  const pkgJson = join(repoPath, "package.json");
  if (isFile(pkgJson) && (isFile(bunLockB) || isFile(bunLock))) {
    // Node test is NOT auto-enabled — only if explicitly configured.
    // We note it is available but don't set it.
  }
}

/**
 * Check whether a Cargo.toml declares a library target.
 *
 * A lib target exists if:
 *  1. An explicit `[lib]` section is present, OR
 *  2. `src/lib.rs` exists next to the Cargo.toml (Cargo implicit convention)
 *
 * If neither is true, the crate is bin-only and `--lib` would fail with
 * "no library targets found".
 */
function cargoHasLib(cargoTomlPath: string): boolean {
  try {
    const content = readFileSync(cargoTomlPath, "utf-8");
    // Explicit [lib] section (not inside a comment)
    if (/^\[lib\]/m.test(content)) return true;
  } catch {
    // If we can't read it, assume no lib to be safe
    return false;
  }

  // Implicit lib: src/lib.rs next to the Cargo.toml
  const dir = join(cargoTomlPath, "..");
  const implicitLib = join(dir, "src/lib.rs");
  return isFile(implicitLib);
}
