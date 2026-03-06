#!/usr/bin/env node
const fs = require('fs/promises');
const path = require('path');

const DEFAULT_ROOT = path.resolve(process.argv[2] || '.');
const DOC_ROOT_NAME = 'Ecosystem Documentation';
const SKIP_ROOT = new Set([DOC_ROOT_NAME, 'node_modules', '.git', '.DS_Store']);
const SKIP_DIRS = new Set(['node_modules', '.git', 'dist', 'build', '.svelte-kit', 'target']);
const INCLUDE_NAMES = new Set(['README.md', 'ARCHITECTURE.md', 'GOVERNANCE.md', 'DESIGN.md']);
const DATE_FORMAT = new Intl.DateTimeFormat('en-CA');

function isMarkdownFile(name) {
  return name.toLowerCase().endsWith('.md');
}

function formatDate(date = new Date()) {
  return DATE_FORMAT.format(date);
}

async function ensureDir(dir) {
  await fs.mkdir(dir, { recursive: true });
}

async function readExistingLog(logPath) {
  try {
    return await fs.readFile(logPath, 'utf8');
  } catch (error) {
    return '';
  }
}

function shouldInclude(relativePath) {
  const normalized = relativePath.replace(/\\/g, '/');
  const baseName = path.basename(relativePath);
  if (INCLUDE_NAMES.has(baseName)) return true;
  if (normalized.toLowerCase().startsWith('docs/')) return true;
  return false;
}

async function collectDocs(repoPath, repoName) {
  const collected = [];
  async function recurse(current, relative) {
    const entries = await fs.readdir(current, { withFileTypes: true });
    for (const entry of entries) {
      const entryPath = path.join(current, entry.name);
      const entryRel = relative ? path.posix.join(relative, entry.name) : entry.name;
      if (entry.isDirectory()) {
        if (SKIP_DIRS.has(entry.name)) continue;
        await recurse(entryPath, entryRel);
      } else if (entry.isFile() && isMarkdownFile(entry.name)) {
        if (shouldInclude(entryRel)) {
          collected.push(entryRel);
        }
      }
    }
  }
  await recurse(repoPath, '');
  return collected;
}

async function copyDocs(rootDir, repoName, files, targetBase) {
  const repoTarget = path.join(targetBase, repoName);
  const results = [];
  for (const relPath of files) {
    const sourcePath = path.join(rootDir, relPath);
    const destPath = path.join(repoTarget, relPath);
    await ensureDir(path.dirname(destPath));
    const originalContent = await fs.readFile(sourcePath, 'utf8');
    const header = `<!--\nSource repo: ${repoName}\nOriginal path: ${relPath}\nGenerated: ${formatDate()}\n-->\n\n`;
    await fs.writeFile(destPath, header + originalContent, 'utf8');
    results.push(relPath);
  }
  return results;
}

function buildIndexContent(indexMap) {
  const lines = [];
  lines.push('# Ecosystem Documentation');
  lines.push('');
  lines.push('## Overview');
  lines.push('This collection aggregates Markdown documentation from every local Forge repository for human reference and governance.');
  lines.push('');
  lines.push('## Systems Index');
  for (const repo of Object.keys(indexMap).sort()) {
    lines.push(`- [${repo}](./${repo.replace(/ /g, '_')}/README.md)`);
  }
  lines.push('');
  lines.push('## Documentation Map');
  for (const repo of Object.keys(indexMap).sort()) {
    const docList = indexMap[repo];
    if (!docList.length) continue;
    lines.push(`### ${repo}`);
    for (const doc of docList) {
      const display = doc === 'README.md' ? 'README' : doc.replace(/\.md$/i, '');
      const link = doc.replace(/ /g, '%20');
      lines.push(`- [${display}](./${repo.replace(/ /g, '_')}/${link})`);
    }
    lines.push('');
  }
  return lines.join('\n');
}

async function main() {
  const rootDir = DEFAULT_ROOT;
  const targetRoot = path.join(rootDir, DOC_ROOT_NAME);
  const metaDir = path.join(targetRoot, '_meta');
  const logPath = path.join(metaDir, 'generation.log');

  const existingLog = await readExistingLog(logPath);
  await fs.rm(targetRoot, { recursive: true, force: true });
  await ensureDir(metaDir);

  const dirEntries = await fs.readdir(rootDir, { withFileTypes: true });
  const repoDirs = dirEntries
    .filter((entry) => entry.isDirectory() && !SKIP_ROOT.has(entry.name))
    .map((entry) => entry.name);

  const indexMap = {};
  let totalDocs = 0;

  for (const repoName of repoDirs) {
    const repoPath = path.join(rootDir, repoName);
    const docs = await collectDocs(repoPath, repoName);
    if (!docs.length) continue;
    const copied = await copyDocs(repoPath, repoName, docs, targetRoot);
    totalDocs += copied.length;
    indexMap[repoName] = copied;
  }

  const indexContent = buildIndexContent(indexMap);
  await fs.writeFile(path.join(targetRoot, 'README.md'), indexContent, 'utf8');

  const timestamp = new Date().toISOString();
  const logEntry = `Generated: ${timestamp}\nRoot: ${rootDir}\nRepos: ${Object.keys(indexMap).length}\nDocs copied: ${totalDocs}`;
  const combinedLog = [existingLog.trim(), logEntry].filter(Boolean).join('\n\n');
  await fs.writeFile(logPath, combinedLog + '\n', 'utf8');
  console.log('Ecosystem documentation updated. Docs:', totalDocs);
}

if (require.main === module) {
  main().catch((error) => {
    console.error('Failed to build ecosystem docs:', error);
    process.exit(1);
  });
}
