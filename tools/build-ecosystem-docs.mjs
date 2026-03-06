#!/usr/bin/env node
// build-ecosystem-docs.mjs
// Local offline doc aggregator for Forge ecosystem.
// - Scans repos under --root
// - Copies selected markdown files to --out
// - Adds provenance headers
// - Generates an index README
// - Logs each run to _meta/generation.log

import fs from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';

/** Expand ~ to home directory */
function expandHome(p) {
  if (!p) return p;
  if (p === '~') return os.homedir();
  if (p.startsWith('~/')) return path.join(os.homedir(), p.slice(2));
  return p;
}

function parseArgs(argv) {
  const args = {
    root: '~/Forge/ecosystem',
    out: null,
    dryRun: false,
    include: null,
    exclude: null,
  };

  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--root') args.root = argv[++i];
    else if (a === '--out') args.out = argv[++i];
    else if (a === '--dry-run') args.dryRun = true;
    else if (a === '--include') args.include = argv[++i];
    else if (a === '--exclude') args.exclude = argv[++i];
    else {
      throw new Error(`Unknown arg: ${a}`);
    }
  }

  args.root = expandHome(args.root);
  args.out = expandHome(args.out || path.join(args.root, 'Ecosystem Documentation'));
  args.include = args.include ? new Set(args.include.split(',').map(s => s.trim()).filter(Boolean)) : null;
  args.exclude = args.exclude ? new Set(args.exclude.split(',').map(s => s.trim()).filter(Boolean)) : null;

  return args;
}

const IGNORE_DIRS = new Set([
  '.git',
  'node_modules',
  'dist',
  'build',
  '.svelte-kit',
  'target',
  '.next',
  '.turbo',
]);

async function pathExists(p) {
  try {
    await fs.access(p);
    return true;
  } catch {
    return false;
  }
}

async function ensureDir(p, dryRun) {
  if (dryRun) return;
  await fs.mkdir(p, { recursive: true });
}

async function readDirSafe(dir) {
  try {
    return await fs.readdir(dir, { withFileTypes: true });
  } catch {
    return [];
  }
}

async function collectDocs(repoPath) {
  const out = [];

  const topCandidates = [
    'README.md',
    'ARCHITECTURE.md',
    'GOVERNANCE.md',
    'DESIGN.md',
    'CONTRIBUTING.md',
    'SECURITY.md',
  ];

  for (const f of topCandidates) {
    const p = path.join(repoPath, f);
    if (await pathExists(p)) out.push({ absPath: p, relPath: f });
  }

  const docsRoot = path.join(repoPath, 'docs');
  if (await pathExists(docsRoot)) {
    const stack = [{ abs: docsRoot, rel: 'docs' }];
    while (stack.length) {
      const cur = stack.pop();
      const entries = await readDirSafe(cur.abs);
      for (const ent of entries) {
        if (ent.isDirectory()) {
          if (IGNORE_DIRS.has(ent.name)) continue;
          stack.push({
            abs: path.join(cur.abs, ent.name),
            rel: path.join(cur.rel, ent.name),
          });
        } else if (ent.isFile()) {
          if (!ent.name.toLowerCase().endsWith('.md')) continue;
          const absPath = path.join(cur.abs, ent.name);
          const relPath = path.join(cur.rel, ent.name);
          out.push({ absPath, relPath });
        }
      }
    }
  }

  out.sort((a, b) => a.relPath.localeCompare(b.relPath));
  return out;
}

function provenanceHeader(repoName, relPath, iso) {
  return `<!--
Source repo: ${repoName}
Original path: ${relPath}
Generated: ${iso}
-->

`;
}

async function copyWithProvenance({ repoName, absPath, relPath, destRoot, iso, dryRun }) {
  const destPath = path.join(destRoot, repoName, relPath);
  const destDir = path.dirname(destPath);

  const contents = await fs.readFile(absPath, 'utf8');
  const header = provenanceHeader(repoName, relPath, iso);
  const finalText = header + contents;

  if (!dryRun) {
    await ensureDir(destDir, dryRun);
    await fs.writeFile(destPath, finalText, 'utf8');
  }

  return { destPath };
}

async function writeIndexReadme({ outDir, iso, repoEntries, dryRun }) {
  const lines = [];
  lines.push('# Forge Ecosystem Documentation (Local)');
  lines.push('');
  lines.push('This folder is generated locally. It aggregates Markdown docs from independent Forge ecosystem repositories.');
  lines.push('It is intended for internal governance, long-term cohesion, and system understanding.');
  lines.push('');
  lines.push(`Generated: ${iso}`);
  lines.push('');

  for (const repo of repoEntries) {
    lines.push(`## ${repo.repoName}`);
    if (repo.warnings.length) {
      lines.push('');
      lines.push('**Warnings:**');
      for (const w of repo.warnings) lines.push(`- ${w}`);
    }
    lines.push('');

    if (!repo.docs.length) {
      lines.push('- (No markdown docs found by collector rules)');
      lines.push('');
      continue;
    }

    for (const d of repo.docs) {
      const link = `${repo.repoName}/${d.relPath}`.replace(/\\/g, '/');
      const label = d.relPath === 'README.md' ? 'README' : d.relPath;
      lines.push(`- [${label}](${link})`);
    }
    lines.push('');
  }

  const readmePath = path.join(outDir, 'README.md');
  if (!dryRun) {
    await fs.writeFile(readmePath, lines.join('\n'), 'utf8');
  }
}

async function appendLog({ outDir, iso, root, repoEntries, dryRun }) {
  const metaDir = path.join(outDir, '_meta');
  const logPath = path.join(metaDir, 'generation.log');

  const totalFiles = repoEntries.reduce((sum, r) => sum + r.docs.length, 0);
  const totalCopied = repoEntries.reduce((sum, r) => sum + r.copiedCount, 0);

  const lines = [];
  lines.push('============================================================');
  lines.push(`Run: ${iso}`);
  lines.push(`Root: ${root}`);
  lines.push(`Out:  ${outDir}`);
  lines.push(`Repos scanned: ${repoEntries.length}`);
  lines.push(`Docs discovered: ${totalFiles}`);
  lines.push(`Docs copied:     ${totalCopied}`);
  lines.push('');

  for (const r of repoEntries) {
    lines.push(`- ${r.repoName}: discovered=${r.docs.length} copied=${r.copiedCount}`);
    for (const w of r.warnings) lines.push(`  WARN: ${w}`);
  }

  lines.push('');

  if (!dryRun) {
    await ensureDir(metaDir, dryRun);
    await fs.appendFile(logPath, lines.join('\n') + '\n', 'utf8');
  }
}

async function main() {
  const args = parseArgs(process.argv);
  const iso = new Date().toISOString();

  const entries = await fs.readdir(args.root, { withFileTypes: true });
  const repos = entries
    .filter(e => e.isDirectory())
    .map(e => e.name)
    .filter(name => !name.startsWith('.'))
    .filter(name => name !== path.basename(args.out))
    .filter(name => !IGNORE_DIRS.has(name))
    .sort((a, b) => a.localeCompare(b));

  const selected = repos.filter(name => {
    if (args.include && !args.include.has(name)) return false;
    if (args.exclude && args.exclude.has(name)) return false;
    return true;
  });

  if (!args.dryRun) {
    await ensureDir(args.out, args.dryRun);
  }

  const repoEntries = [];

  for (const repoName of selected) {
    const repoPath = path.join(args.root, repoName);
    const warnings = [];

    const looksLikeRepo =
      (await pathExists(path.join(repoPath, '.git'))) ||
      (await pathExists(path.join(repoPath, 'package.json'))) ||
      (await pathExists(path.join(repoPath, 'Cargo.toml'))) ||
      (await pathExists(path.join(repoPath, 'README.md'))) ||
      (await pathExists(path.join(repoPath, 'docs')));

    if (!looksLikeRepo) {
      warnings.push('Skipped: does not look like a repo (no .git/package.json/Cargo.toml/README/docs)');
      repoEntries.push({ repoName, repoPath, warnings, docs: [], copiedCount: 0 });
      continue;
    }

    const docs = await collectDocs(repoPath);
    if (!docs.find(d => d.relPath === 'README.md')) {
      warnings.push('README.md not found by collector rules');
    }

    let copiedCount = 0;
    for (const d of docs) {
      await copyWithProvenance({
        repoName,
        absPath: d.absPath,
        relPath: d.relPath,
        destRoot: args.out,
        iso,
        dryRun: args.dryRun,
      });
      copiedCount++;
    }

    repoEntries.push({ repoName, repoPath, warnings, docs, copiedCount });
  }

  await writeIndexReadme({ outDir: args.out, iso, repoEntries, dryRun: args.dryRun });
  await appendLog({ outDir: args.out, iso, root: args.root, repoEntries, dryRun: args.dryRun });

  const totalCopied = repoEntries.reduce((sum, r) => sum + r.copiedCount, 0);
  console.log(`[ecosystem-docs] ${args.dryRun ? 'DRY RUN ' : ''}copied ${totalCopied} markdown files into: ${args.out}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
