/** Repo discovery — find all git repos under ecosystem root */

import { join } from "node:path";
import type { DiscoveredRepo } from "./types.js";
import { listDirs, isDir } from "./util/fs.js";

const EXCLUDED = new Set(["tools"]);

export function discoverRepos(
  root: string,
  only: string[],
  skip: string[]
): DiscoveredRepo[] {
  const dirs = listDirs(root);

  const repos: DiscoveredRepo[] = [];

  for (const name of dirs) {
    // Skip hidden folders
    if (name.startsWith(".")) continue;
    // Skip excluded
    if (EXCLUDED.has(name)) continue;
    // Skip if not a git repo
    const repoPath = join(root, name);
    if (!isDir(join(repoPath, ".git"))) continue;

    repos.push({ name, path: repoPath });
  }

  // Apply --only filter
  let filtered = repos;
  if (only.length > 0) {
    const onlySet = new Set(only);
    filtered = filtered.filter((r) => onlySet.has(r.name));
  }

  // Apply --skip filter
  if (skip.length > 0) {
    const skipSet = new Set(skip);
    filtered = filtered.filter((r) => !skipSet.has(r.name));
  }

  // Deterministic: sort by name
  filtered.sort((a, b) => a.name.localeCompare(b.name));

  return filtered;
}
