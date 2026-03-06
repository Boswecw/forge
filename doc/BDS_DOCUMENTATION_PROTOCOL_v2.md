# BDS Documentation Protocol v2.0

> Standardized modular documentation build system for multi-repo ecosystems.
> "One pattern. Every repo. Instant identification."

**Protocol version:** 2.0 (2026-02-25)

---

## 1. Purpose

When working with AI assistants (Claude.ai, ChatGPT, etc.), engineers routinely paste system documentation files for context. In a multi-repo ecosystem, every repo's documentation looks structurally identical — making it impossible to tell at a glance which repo a pasted file belongs to.

BDS Documentation Protocol v2.0 solves this with:

1. **Modular sections** — numbered markdown files that can be edited independently
2. **Deterministic assembly** — a single `BUILD.sh` that concatenates sections into one file
3. **Prefix identification** — a 2-character repo identifier prepended to the output filename

---

## 2. Current Deployment

12 repos are live on Protocol v2.0 as of 2026-02-25:

| Prefix | Repo         | Lines | Sections |
|--------|--------------|-------|----------|
| `af`   | AuthorForge  | 8,669 | 34       |
| `cb`   | CortexBDS    | 1,729 | 11       |
| `df`   | DataForge    | 2,311 | 11       |
| `fa`   | ForgeAgents  | 3,747 | 11       |
| `fc`   | ForgeCommand | 5,535 | 20       |
| `fi`   | ForgeImages  | 1,293 | 11       |
| `fs`   | Forge:SMITH  | 3,465 | 16       |
| `nf`   | NeuroForge   | 2,207 | 11       |
| `ra`   | Rake         | 2,242 | 11       |
| `sp`   | Smithy       | 726   | 11       |
| `tc`   | Tarcie       | 636   | 11       |
| `zs`   | ZFSS         | 770   | 11       |

**Reserved:** `ec` (Ecosystem root)

See [PREFIX_REGISTRY.md](PREFIX_REGISTRY.md) for the canonical registry.

---

## 3. Directory Structure

Every participating repo maintains this structure:

```
repo/
├── doc/
│   ├── system/
│   │   ├── _index.md              # Header + table of contents
│   │   ├── BUILD.sh               # Assembly script
│   │   ├── 01-overview-philosophy.md
│   │   ├── 02-architecture.md
│   │   ├── 03-tech-stack.md
│   │   ├── 04-project-structure.md
│   │   ├── 05-config-env.md
│   │   ├── ...                    # Up to 99 sections
│   │   └── NN-topic-name.md
│   └── {prefix}SYSTEM.md          # ← Generated output (do not edit)
```

### Naming Conventions

| Item | Convention | Example |
|------|-----------|---------|
| Section files | `[0-9][0-9]-kebab-case.md` | `07-frontend.md` |
| Index file | `_index.md` (underscore prefix) | Always present |
| Build script | `BUILD.sh` | Always present |
| Output file | `{prefix}SYSTEM.md` | `afSYSTEM.md` |

---

## 4. Prefix Registry

Each repo in the ecosystem is assigned a unique **lowercase 2-character prefix**. This prefix is embedded in the BUILD.sh and appears in the output filename.

### Requirements

- Exactly 2 characters, lowercase alphanumeric
- Unique across the entire ecosystem
- Mnemonic — should evoke the repo name
- Registered in a central `PREFIX_REGISTRY.md` at the ecosystem root

### Choosing a Prefix

| Strategy | Example |
|----------|---------|
| First letters of words | AuthorForge → `af` |
| Abbreviation | NeuroForge → `nf` |
| Disambiguation | ForgeAgents `fa` vs ForgeCommand `fc` |

### Anti-patterns

- Single character (too ambiguous)
- 3+ characters (diminishing returns, clutters filename)
- Uppercase (inconsistent with unix conventions)
- Numbers only (confusing with section numbers)

---

## 5. _index.md Specification

The `_index.md` file serves as the **header and table of contents** for the assembled document. It is the first content in the output file.

### Required Content

```markdown
# {Repo Name} — System Documentation

> One-line description of the repo's role

| Part | File | Contents |
|------|------|----------|
| §1 | `01-overview-philosophy.md` | ... |
| §2 | `02-architecture.md` | ... |
| ... | ... | ... |

## Quick Assembly

\`\`\`bash
bash doc/system/BUILD.sh   # Assembles all parts into doc/{prefix}SYSTEM.md
\`\`\`
```

### Optional Content

- Document version and date
- Protocol version reference
- Companion documentation links (if the repo has additional docs outside `doc/system/`)
- Last-updated timestamp

### Rules

1. The `_index.md` must reference the correct prefixed output filename
2. Section links should use relative paths (e.g., `01-overview-philosophy.md`, not absolute)
3. The TOC table must list every numbered section file in the directory

---

## 6. Section Files

### Numbering

- Files are numbered `01` through `99`
- Numbers determine concatenation order (lexicographic sort)
- Gaps are allowed (e.g., `01`, `02`, `05`, `10`) — they don't affect output
- Number `00` is reserved (avoid using it)

### Recommended Section Order

| Range | Category | Typical Sections |
|-------|----------|-----------------|
| 01–05 | **Identity** | Overview, architecture, tech stack, project structure, config |
| 06–09 | **Interface** | Design system, frontend, API layer, backend internals |
| 10–15 | **Data** | Database schema, integrations, error handling, testing |
| 16–20 | **Operations** | Security, deployment, handover, migrations |
| 21+ | **Extensions** | Feature-specific modules added over time |

### Content Guidelines

- Each section should be self-contained and readable independently
- Use markdown headers starting at `##` (the `#` level is reserved for _index.md)
- No frontmatter comments (e.g., `<!-- Part of RepoName -->`) — if present, the BUILD.sh can strip them but it's preferred to omit
- Cross-references between sections should use descriptive text, not anchor links (anchors break in the assembled file)

---

## 7. BUILD.sh Specification

### Canonical Template

```bash
#!/usr/bin/env bash
# BDS Documentation Protocol v2.0 — BUILD.sh
# Assembles numbered section files into {prefix}SYSTEM.md
# Usage: bash doc/system/BUILD.sh

set -euo pipefail

PREFIX="xx"  # ← 2-char repo identifier from PREFIX_REGISTRY.md
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
OUTPUT="${SCRIPT_DIR}/../${PREFIX}SYSTEM.md"

# Write _index.md header
cat "${SCRIPT_DIR}/_index.md" > "${OUTPUT}"
printf '\n---\n' >> "${OUTPUT}"

# Concatenate all numbered sections in order
for part in "${SCRIPT_DIR}"/[0-9][0-9]-*.md; do
  [ -f "$part" ] || continue
  printf '\n' >> "${OUTPUT}"
  cat "${part}" >> "${OUTPUT}"
  printf '\n---\n' >> "${OUTPUT}"
done

echo "${PREFIX}SYSTEM.md rebuilt ($(wc -l < "${OUTPUT}") lines)"
```

### Invariants

| Rule | Rationale |
|------|-----------|
| `set -euo pipefail` | Fail fast on any error |
| `${BASH_SOURCE[0]}` | Works when sourced or called from any directory |
| Output to `../` (one level up from `system/`) | Keeps generated file at `doc/{prefix}SYSTEM.md` |
| Glob `[0-9][0-9]-*.md` | Matches 00–99, excludes `_index.md` and non-numbered files |
| `[ -f "$part" ] || continue` | Graceful no-op if no section files exist |
| `printf '\n---\n'` | Clean horizontal rule separators between sections |
| Echo line count on success | Confirms build completed and gives size feedback |

### Allowed Variations

| Variation | When |
|-----------|------|
| `grep -v` frontmatter strip | If legacy section files contain comment headers |
| Additional echo/logging | For debugging during development |

### Forbidden

| Anti-pattern | Why |
|-------------|-----|
| Hardcoded TOC in heredoc | Duplicates _index.md, drifts out of sync |
| Output to repo root | Inconsistent paths, clutters root |
| Output named `context-bundle.md` | Non-standard, doesn't carry prefix |
| Glob `0*.md` | Matches _index.md-adjacent files, misses sections 10+ |
| Glob `[0-1][0-9]-*.md` | Caps at 19 sections — too restrictive |
| Interactive prompts | BUILD.sh must run unattended (CI/CD, hooks) |

---

## 8. Output File

### Location

Always: `doc/{prefix}SYSTEM.md`

### Structure

```
┌─────────────────────────────┐
│  _index.md content          │  ← Header + TOC
├─────────────────────────────┤
│  ---                        │  ← Separator
├─────────────────────────────┤
│  01-overview-philosophy.md  │  ← Section 1
├─────────────────────────────┤
│  ---                        │
├─────────────────────────────┤
│  02-architecture.md         │  ← Section 2
├─────────────────────────────┤
│  ...                        │
└─────────────────────────────┘
```

### Git Tracking

The output file **should be committed to git**. Rationale:

- Allows `git diff` to show documentation changes in PRs
- Available immediately after clone (no build step required)
- AI assistants can read it directly from the repo

### .gitignore

Do **not** gitignore the output file. Do gitignore any intermediate build artifacts if they exist.

---

## 9. Adding a New Repo

### Checklist

1. **Choose a 2-char prefix** — check `PREFIX_REGISTRY.md` for conflicts
2. **Register the prefix** — add entry to ecosystem `PREFIX_REGISTRY.md`
3. **Create directory** — `mkdir -p doc/system`
4. **Create `_index.md`** — header, TOC table, quick assembly reference
5. **Create section files** — start with `01-overview-philosophy.md` at minimum
6. **Copy BUILD.sh template** — set `PREFIX="xx"` to your chosen prefix
7. **Run `bash doc/system/BUILD.sh`** — verify output at `doc/{prefix}SYSTEM.md`
8. **Commit all files** — including the generated output

### Minimum Viable Documentation

A new repo needs at minimum:

```
doc/system/
├── _index.md
├── BUILD.sh
└── 01-overview-philosophy.md
```

This produces a valid `{prefix}SYSTEM.md` with header + one section.

---

## 10. Adding a New Section

1. Create `doc/system/NN-topic-name.md` with the next available number
2. Update `_index.md` TOC table with the new entry
3. Run `bash doc/system/BUILD.sh`
4. Commit all three files (`NN-topic-name.md`, `_index.md`, `{prefix}SYSTEM.md`)

---

## 11. Migration from Legacy Patterns

### From `context-bundle.md` (Pattern B)

1. Ensure `_index.md` exists with proper TOC
2. Replace BUILD.sh with v2.0 template
3. Run BUILD.sh to generate `{prefix}SYSTEM.md`
4. Delete `context-bundle.md` from repo root
5. Remove from `.gitignore` if listed

### From unprefixed `SYSTEM.md` (Pattern A/C)

1. Update `_index.md` to reference `{prefix}SYSTEM.md`
2. Replace BUILD.sh with v2.0 template
3. Run BUILD.sh to generate `{prefix}SYSTEM.md`
4. Delete old `doc/SYSTEM.md`
5. Git will detect the rename automatically

### From hardcoded TOC heredoc (Pattern A)

1. Move TOC content from BUILD.sh heredoc into `_index.md`
2. Replace BUILD.sh with v2.0 template
3. If section files have frontmatter comments, add `grep -v` strip to BUILD.sh
4. Run BUILD.sh and verify output matches previous content

---

## 12. Integration with AI Workflows

### Intended Use

```
1. Developer runs: bash doc/system/BUILD.sh
2. Output: doc/afSYSTEM.md (8,669 lines)
3. Developer copies afSYSTEM.md to Claude.ai
4. Claude sees filename "afSYSTEM.md" → knows it's AuthorForge
5. Full system context available in one file
```

### Multi-Repo Sessions

When working across repos, paste multiple prefixed files:

```
afSYSTEM.md  →  AuthorForge context
dfSYSTEM.md  →  DataForge context
nfSYSTEM.md  →  NeuroForge context
```

The prefix eliminates ambiguity about which repo each file describes.

### CI/CD Integration

BUILD.sh can run in CI to ensure documentation stays current:

```yaml
# Example: GitHub Actions
- name: Verify documentation build
  run: |
    bash doc/system/BUILD.sh
    git diff --exit-code doc/*SYSTEM.md || {
      echo "Documentation out of date. Run: bash doc/system/BUILD.sh"
      exit 1
    }
```

---

## 13. Portability

This protocol is framework-agnostic and language-agnostic. It requires only:

- Bash (available on Linux, macOS, WSL, Git Bash)
- Standard Unix tools (`cat`, `printf`, `wc`, `grep`)
- Markdown files

It can be adopted by any project that wants modular, prefix-identified documentation assembly — not just Forge ecosystem repos.

### Adaptation for Other Ecosystems

1. Fork `PREFIX_REGISTRY.md` for your ecosystem
2. Choose your own 2-char prefixes
3. Copy the BUILD.sh template
4. Adjust section numbering conventions to your needs

---

*Protocol authored by Boswell Digital Solutions LLC. 2026-02-25.*
