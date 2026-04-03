#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ECOSYSTEM_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
TODAY="$(date +%F)"
REPORT_PATH="$ECOSYSTEM_ROOT/docs/audits/ecosystem_documentation_protocol_audit_${TODAY}.md"
WRITE_MODE=false

if [[ "${1:-}" == "--write" ]]; then
  WRITE_MODE=true
fi

find_repos() {
  find "$ECOSYSTEM_ROOT" -mindepth 0 -maxdepth 2 -type d -name .git -printf '%h\n' | sort
}

repo_basename() {
  basename "$1"
}

repo_display_name() {
  local name
  name="$(repo_basename "$1")"
  if [[ "$1" == "$ECOSYSTEM_ROOT" ]]; then
    printf 'Forge Ecosystem'
    return 0
  fi
  case "$name" in
    forgeHQ) printf 'forgeHQ' ;;
    Forge_Command) printf 'Forge Command' ;;
    zfss) printf 'ZFSS' ;;
    fa-local) printf 'FA Local' ;;
    dataforge-Local) printf 'DataForge Local' ;;
    df-local-foundation) printf 'DF Local Foundation' ;;
    forge-local-runtime) printf 'Forge Local Runtime' ;;
    forge-smithy) printf 'Forge Smithy' ;;
    canebrake_press) printf 'Canebrake Press' ;;
    cortex_bds) printf 'Cortex BDS' ;;
    *) printf '%s' "$(printf '%s' "$name" | sed 's/[-_]/ /g')" ;;
  esac
}

repo_slug() {
  repo_basename "$1" | tr '[:upper:]' '[:lower:]' | tr ' _' '--'
}

has_top_level_dir() {
  local repo="$1"
  local dir_name="$2"
  [[ -d "$repo/$dir_name" ]]
}

has_any_dir() {
  local repo="$1"
  shift
  local dir_name
  for dir_name in "$@"; do
    if [[ -d "$repo/$dir_name" ]]; then
      return 0
    fi
  done
  return 1
}

primary_dirs() {
  local repo="$1"
  find "$repo" -maxdepth 1 -mindepth 1 -type d \
    ! -name '.git' \
    ! -name '.github' \
    ! -name '.claude' \
    ! -name '.pytest_cache' \
    ! -name '.ruff_cache' \
    ! -name '.venv' \
    ! -name 'venv' \
    ! -name 'node_modules' \
    ! -name 'dist' \
    ! -name 'build' \
    ! -name 'target' \
    ! -name 'out' \
    ! -name '.svelte-kit' \
    ! -name '.vite' \
    ! -name '.tmp' \
    -printf '%f\n' | sort
}

render_dir_tree() {
  local repo="$1"
  local entries=()
  local entry
  while IFS= read -r entry; do
    entries+=("$entry")
  done < <(primary_dirs "$repo" | sed -n '1,12p')

  printf '```text\n%s/\n' "$(repo_basename "$repo")"
  for entry in "${entries[@]}"; do
    printf '├── %s/\n' "$entry"
  done
  printf '```\n'
}

detect_stack_rows() {
  local repo="$1"
  local rows=()
  if [[ -f "$repo/package.json" ]]; then
    rows+=('| Frontend / JS Tooling | `package.json` present | JavaScript or TypeScript application tooling detected |')
  fi
  if has_any_dir "$repo" src src-tauri browser-extension static apps; then
    rows+=('| UI / Desktop Surface | `src/`, `src-tauri/`, `browser-extension/`, `static/`, or `apps/` present | Local UI or desktop surface detected in the repo tree |')
  fi
  if has_any_dir "$repo" app api service cortex_runtime crates; then
    rows+=('| Backend / Core Runtime | `app/`, `api/`, `service/`, `cortex_runtime/`, or `crates/` present | Primary application or library runtime detected |')
  fi
  if has_any_dir "$repo" alembic migrations db sql models schemas; then
    rows+=('| Persistence / Schemas | `alembic/`, `migrations/`, `db/`, `sql/`, `models/`, or `schemas/` present | Database, migration, or schema layer detected |')
  fi
  if has_any_dir "$repo" prompts analytics evals registry tools governance; then
    rows+=('| AI / Governance / Ops | `prompts/`, `analytics/`, `evals/`, `registry/`, `tools/`, or `governance/` present | AI-adjacent, governance, or operational surfaces detected |')
  fi
  if [[ ${#rows[@]} -eq 0 ]]; then
    rows+=('| Stack Inventory | No obvious framework marker detected from root files alone | Expand this section as concrete stack details are cataloged |')
  fi
  printf '%s\n' "${rows[@]}"
}

detect_module_rows() {
  local repo="$1"
  local rows=()
  rows+=('| Documentation Stack | `doc/system/`, `SYSTEM.md`, `scripts/context-bundle.sh` | Canonical repo context and build surfaces |')
  if has_any_dir "$repo" app service cortex_runtime api src src-tauri crates; then
    rows+=('| Runtime Surface | `app/`, `service/`, `cortex_runtime/`, `api/`, `src/`, `src-tauri/`, or `crates/` | Primary implementation boundary |')
  fi
  if has_any_dir "$repo" schemas models db sql alembic migrations; then
    rows+=('| Data and Schemas | `schemas/`, `models/`, `db/`, `sql/`, `alembic/`, or `migrations/` | Persistence and validation surfaces |')
  fi
  if has_any_dir "$repo" docs governance DECISIONS prompts evals analytics registry; then
    rows+=('| Governance and Specs | `docs/`, `governance/`, `DECISIONS/`, `prompts/`, `evals/`, `analytics/`, or `registry/` | Repo doctrine, experiments, and supporting design material |')
  fi
  if has_any_dir "$repo" tests fixtures evidence audit reports; then
    rows+=('| Verification | `tests/`, `fixtures/`, `evidence/`, `audit/`, or `reports/` | Test and audit surfaces |')
  fi
  printf '%s\n' "${rows[@]}"
}

legacy_output_rel() {
  local repo="$1"
  local build_path="$repo/doc/system/BUILD.sh"
  local legacy=''
  if [[ -f "$build_path" ]]; then
    legacy="$(rg -o 'doc/[A-Za-z0-9_-]+SYSTEM\.md' "$build_path" | head -n1 || true)"
  fi
  if [[ -z "$legacy" ]]; then
    legacy="$(find "$repo/doc" -maxdepth 1 -type f -name '*SYSTEM.md' ! -name 'SYSTEM.md' -printf '%P\n' | head -n1 || true)"
    [[ -n "$legacy" ]] && legacy="doc/$legacy"
  fi
  printf '%s' "$legacy"
}

ensure_gitignore() {
  local repo="$1"
  local gitignore="$repo/.gitignore"
  touch "$gitignore"
  if ! rg -n '^context-bundle\.md$' "$gitignore" >/dev/null 2>&1; then
    printf '\ncontext-bundle.md\n' >> "$gitignore"
  fi
}

install_build_script() {
  local repo="$1"
  local legacy_rel="$2"
  mkdir -p "$repo/doc/system" "$repo/doc"
  cat > "$repo/doc/system/BUILD.sh" <<EOF
#!/bin/bash
set -euo pipefail

PARTS_DIR="\$(cd "\$(dirname "\$0")" && pwd)"
REPO_ROOT="\$(cd "\$PARTS_DIR/../.." && pwd)"
ROOT_OUTPUT="\$REPO_ROOT/SYSTEM.md"
DOC_OUTPUT="\$REPO_ROOT/doc/SYSTEM.md"
LEGACY_OUTPUT_REL="$legacy_rel"
TMP_OUTPUT="\$(mktemp)"

echo "Assembling SYSTEM.md..."

cat "\$PARTS_DIR/_index.md" > "\$TMP_OUTPUT"

for part in "\$PARTS_DIR"/[0-9][0-9]-*.md; do
  echo "" >> "\$TMP_OUTPUT"
  echo "---" >> "\$TMP_OUTPUT"
  echo "" >> "\$TMP_OUTPUT"
  cat "\$part" >> "\$TMP_OUTPUT"
done

cp "\$TMP_OUTPUT" "\$ROOT_OUTPUT"
cp "\$TMP_OUTPUT" "\$DOC_OUTPUT"

if [[ -n "\$LEGACY_OUTPUT_REL" ]]; then
  LEGACY_OUTPUT="\$REPO_ROOT/\$LEGACY_OUTPUT_REL"
  mkdir -p "\$(dirname "\$LEGACY_OUTPUT")"
  cp "\$TMP_OUTPUT" "\$LEGACY_OUTPUT"
fi

chmod 664 "\$ROOT_OUTPUT" "\$DOC_OUTPUT"
if [[ -n "\$LEGACY_OUTPUT_REL" ]]; then
  chmod 664 "\$REPO_ROOT/\$LEGACY_OUTPUT_REL"
fi

LINE_COUNT=\$(wc -l < "\$ROOT_OUTPUT")
rm -f "\$TMP_OUTPUT"
echo "SYSTEM.md assembled: \$LINE_COUNT lines"
EOF
  chmod +x "$repo/doc/system/BUILD.sh"
}

install_context_bundle() {
  local repo="$1"
  mkdir -p "$repo/scripts"
  cat > "$repo/scripts/context-bundle.sh" <<'EOF'
#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
SYSTEM_DIR="$REPO_ROOT/doc/system"
OUTPUT="$REPO_ROOT/context-bundle.md"

WITH_ROADMAP=false
WITH_SPECS=false
DRY_RUN=false
LIST_ONLY=false
INCLUDE_ALL=false
PRESET=""
declare -a SECTIONS=()

available_sections() {
  for part in "$SYSTEM_DIR"/[0-9][0-9]-*.md; do
    basename "$part" | cut -d- -f1
  done
}

available_parts() {
  find "$SYSTEM_DIR" -maxdepth 1 -type f -name '[0-9][0-9]-*.md' | sort
}

add_if_exists() {
  local section="$1"
  local match=("$SYSTEM_DIR"/"$section"-*.md)
  [[ -e "${match[0]}" ]] && SECTIONS+=("$section")
}

append_unique() {
  local value="$1"
  local existing
  for existing in "${SECTIONS[@]}"; do
    [[ "$existing" == "$value" ]] && return 0
  done
  SECTIONS+=("$value")
}

show_list() {
  echo "Available sections:"
  for part in "$SYSTEM_DIR"/[0-9][0-9]-*.md; do
    echo "  $(basename "$part")"
  done
  echo
  echo "Presets:"
  echo "  core"
  echo "  foundation"
  echo "  governance"
  echo "  docs"
  echo "  architecture"
  echo "  config"
  echo "  testing"
  echo "  handover"
  echo "  frontend"
  echo "  backend"
  echo "  api"
  echo "  schema"
  echo "  integration"
}

select_by_keywords() {
  local keywords=("$@")
  local part
  local section
  local slug
  SECTIONS=()
  while IFS= read -r part; do
    section="$(basename "$part" | cut -d- -f1)"
    slug="$(basename "$part" | tr '[:upper:]' '[:lower:]')"
    for keyword in "${keywords[@]}"; do
      if [[ "$slug" == *"$keyword"* ]]; then
        append_unique "$section"
        break
      fi
    done
  done < <(available_parts)
}

resolve_preset() {
  SECTIONS=()
  case "$1" in
    core|foundation)
      while IFS= read -r section; do
        case "$section" in
          01|02|03|04|05) append_unique "$section" ;;
        esac
      done < <(available_sections)
      while IFS= read -r section; do
        append_unique "$section"
      done < <(available_sections | tail -n 3)
      ;;
    governance)
      select_by_keywords governance boundary doctrine policy security error testing handover
      if [[ ${#SECTIONS[@]} -eq 0 ]]; then
        resolve_preset testing
      else
        while IFS= read -r section; do
          case "$section" in
            01|02) append_unique "$section" ;;
          esac
        done < <(available_sections)
      fi
      ;;
    docs|documentation)
      while IFS= read -r section; do
        case "$section" in
          01|02|04|05) append_unique "$section" ;;
        esac
      done < <(available_sections)
      while IFS= read -r section; do
        append_unique "$section"
      done < <(available_sections | tail -n 2)
      ;;
    architecture|config)
      select_by_keywords architecture overview structure config environment tech stack
      if [[ ${#SECTIONS[@]} -eq 0 ]]; then
        resolve_preset docs
      fi
      ;;
    testing)
      select_by_keywords testing error handover qa audit
      if [[ ${#SECTIONS[@]} -eq 0 ]]; then
        while IFS= read -r section; do
          append_unique "$section"
        done < <(available_sections | tail -n 3)
      fi
      ;;
    handover)
      select_by_keywords handover migration error testing
      if [[ ${#SECTIONS[@]} -eq 0 ]]; then
        resolve_preset testing
      fi
      ;;
    frontend)
      select_by_keywords frontend design tauri browser component ui
      if [[ ${#SECTIONS[@]} -eq 0 ]]; then
        resolve_preset core
      fi
      ;;
    backend)
      select_by_keywords backend runtime service command api worker internals
      if [[ ${#SECTIONS[@]} -eq 0 ]]; then
        resolve_preset core
      fi
      ;;
    api)
      select_by_keywords api route proxy middleware command
      if [[ ${#SECTIONS[@]} -eq 0 ]]; then
        resolve_preset backend
      fi
      ;;
    schema)
      select_by_keywords schema database migration model persistence sql
      if [[ ${#SECTIONS[@]} -eq 0 ]]; then
        resolve_preset core
      fi
      ;;
    integration)
      select_by_keywords integration ecosystem ai provider adapter forge
      if [[ ${#SECTIONS[@]} -eq 0 ]]; then
        resolve_preset core
      fi
      ;;
    *)
      echo "Unknown preset: $1" >&2
      exit 1
      ;;
  esac
}

resolve_section_file() {
  local section="$1"
  local matches=("$SYSTEM_DIR"/"$section"-*.md)
  if [[ ! -e "${matches[0]}" ]]; then
    echo "Missing section file for $section" >&2
    exit 1
  fi
  printf '%s\n' "${matches[0]}"
}

collect_roadmap_files() {
  find "$REPO_ROOT/docs" -maxdepth 1 -type f -iname '*roadmap*.md' | sort
}

collect_spec_files() {
  find "$REPO_ROOT/docs" -type f \( -iname '*spec*.md' -o -iname '*architecture*.md' \) | sort
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --list)
      LIST_ONLY=true
      shift
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --preset)
      PRESET="${2:-}"
      shift 2
      ;;
    --all)
      INCLUDE_ALL=true
      shift
      ;;
    --with-roadmap)
      WITH_ROADMAP=true
      shift
      ;;
    --with-specs)
      WITH_SPECS=true
      shift
      ;;
    *)
      if [[ "$1" =~ ^[0-9]+$ ]]; then
        printf -v PADDED '%02d' "$1"
        SECTIONS+=("$PADDED")
        shift
      else
        echo "Unknown argument: $1" >&2
        exit 1
      fi
      ;;
  esac
done

if [[ "$LIST_ONLY" == true ]]; then
  show_list
  exit 0
fi

if [[ -n "$PRESET" ]]; then
  resolve_preset "$PRESET"
fi

if [[ "$INCLUDE_ALL" == true ]]; then
  SECTIONS=()
  while IFS= read -r section; do
    SECTIONS+=("$section")
  done < <(available_sections)
fi

if [[ ${#SECTIONS[@]} -eq 0 ]]; then
  resolve_preset core
fi

if [[ "$DRY_RUN" == true ]]; then
  echo "Would assemble:"
  for section in "${SECTIONS[@]}"; do
    file="$(resolve_section_file "$section")"
    echo "  $section -> $(basename "$file") ($(wc -l < "$file") lines)"
  done
  if [[ "$WITH_ROADMAP" == true ]]; then
    while IFS= read -r roadmap; do
      [[ -n "$roadmap" ]] || continue
      echo "  roadmap -> $(basename "$roadmap") ($(wc -l < "$roadmap") lines)"
    done < <(collect_roadmap_files)
  fi
  if [[ "$WITH_SPECS" == true ]]; then
    while IFS= read -r spec; do
      [[ -n "$spec" ]] || continue
      echo "  spec -> $(basename "$spec") ($(wc -l < "$spec") lines)"
    done < <(collect_spec_files)
  fi
  exit 0
fi

cat "$SYSTEM_DIR/_index.md" > "$OUTPUT"

for section in "${SECTIONS[@]}"; do
  file="$(resolve_section_file "$section")"
  echo "" >> "$OUTPUT"
  echo "---" >> "$OUTPUT"
  echo "" >> "$OUTPUT"
  cat "$file" >> "$OUTPUT"
done

if [[ "$WITH_ROADMAP" == true ]]; then
  while IFS= read -r roadmap; do
    [[ -n "$roadmap" ]] || continue
    echo "" >> "$OUTPUT"
    echo "---" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    cat "$roadmap" >> "$OUTPUT"
  done < <(collect_roadmap_files)
fi

if [[ "$WITH_SPECS" == true ]]; then
  while IFS= read -r spec; do
    [[ -n "$spec" ]] || continue
    echo "" >> "$OUTPUT"
    echo "---" >> "$OUTPUT"
    echo "" >> "$OUTPUT"
    cat "$spec" >> "$OUTPUT"
  done < <(collect_spec_files)
fi

echo "context-bundle.md assembled: $(wc -l < "$OUTPUT") lines"
EOF
  chmod +x "$repo/scripts/context-bundle.sh"
}

write_baseline_doc_system() {
  local repo="$1"
  local display_name="$2"
  local slug="$3"
  local repo_name
  repo_name="$(repo_basename "$repo")"
  mkdir -p "$repo/doc/system" "$repo/docs"

  cat > "$repo/doc/system/_index.md" <<EOF
# ${display_name} — Complete System Reference

> Baseline documentation-protocol adoption for ${display_name}.
> "Current repo truth before deeper authored expansion."

**Document version:** 0.1 (${TODAY}) — Baseline protocol adoption

---

## Table of Contents

1. [Overview & Philosophy](#1-overview--philosophy)
2. [Architecture](#2-architecture)
3. [Tech Stack](#3-tech-stack)
4. [Project Structure](#4-project-structure)
5. [Configuration & Environment](#5-configuration--environment)
6. [Design System](#6-design-system)
7. [Frontend](#7-frontend)
8. [API Layer](#8-api-layer)
9. [Backend](#9-backend)
10. [Ecosystem Integration](#10-ecosystem-integration)
11. [Database Schema](#11-database-schema)
12. [AI Integration](#12-ai-integration)
13. [Error Handling Contract](#13-error-handling-contract)
14. [Testing Infrastructure](#14-testing-infrastructure)
15. [Handover / Migration Notes](#15-handover--migration-notes)
EOF

  cat > "$repo/doc/system/01-overview-philosophy.md" <<EOF
## 1. Overview & Philosophy

${display_name} is currently documented through a baseline protocol-adoption pass.
This section records only repository surfaces directly observable from the working tree.

### 1.1 Current Posture

| Topic | Current truth |
| --- | --- |
| Repo | \`${repo_name}\` |
| Protocol status | Baseline adoption in progress |
| Canonical technical reference | \`doc/system/\` plus generated root \`SYSTEM.md\` |
| Current scope | Expand this section as product and service boundaries are cataloged |
EOF

  cat > "$repo/doc/system/02-architecture.md" <<EOF
## 2. Architecture

This baseline architecture section records the major repo surfaces present today.

### 2.1 Observed Top-Level Areas

$(render_dir_tree "$repo")
EOF

  cat > "$repo/doc/system/03-tech-stack.md" <<EOF
## 3. Tech Stack

This baseline stack inventory is inferred from repository markers and directory layout.

### 3.1 Detected Surfaces

| Layer | Marker | Current interpretation |
| --- | --- | --- |
$(detect_stack_rows "$repo")
EOF

  cat > "$repo/doc/system/04-project-structure.md" <<EOF
## 4. Project Structure

### 4.1 Directory Layout

$(render_dir_tree "$repo")

### 4.2 Documentation Rule

- \`doc/system/\` is the canonical modular source for the root \`SYSTEM.md\`
- \`scripts/context-bundle.sh\` is the selective context assembly surface
- \`CLAUDE.md\` is the repo-local AI instruction file
EOF

  cat > "$repo/doc/system/05-configuration.md" <<EOF
## 5. Configuration & Environment

This baseline section has not yet enumerated every environment variable or configuration file.

### 5.1 Current Status

| Surface | Status |
| --- | --- |
| Environment variable inventory | Not yet expanded in this baseline |
| Config ownership mapping | Not yet expanded in this baseline |
| Protocol requirement | Every env var must be documented here as this repo matures |
EOF

  cat > "$repo/doc/system/06-design-system.md" <<EOF
## 6. Design System

This section is a placeholder unless a UI surface is present in the current repo.

### 6.1 Current Status

| Surface | Status |
| --- | --- |
| Design tokens | Expand when UI tokens are inventoried |
| Component patterns | Expand when UI components are cataloged |
| Brand posture | Keep this section grounded in implemented UI reality only |
EOF

  if has_any_dir "$repo" src src-tauri browser-extension static apps; then
    frontend_status='Frontend or desktop surfaces are present in the repository tree and need continued section expansion.'
  else
    frontend_status='No obvious frontend surface was detected from the current top-level directory layout.'
  fi
  cat > "$repo/doc/system/07-frontend.md" <<EOF
## 7. Frontend

${frontend_status}

### 7.1 Current Status

| Surface | Status |
| --- | --- |
| UI routing and component inventory | Expand from current source files as the repo is cataloged |
| Desktop shell / browser surface | Record here only if implemented in the repo |
EOF

  if has_any_dir "$repo" api app service; then
    api_status='API-adjacent directories are present and should be documented here as concrete routes and contracts.'
  else
    api_status='No obvious dedicated API directory was detected from the current top-level directory layout.'
  fi
  cat > "$repo/doc/system/08-api-layer.md" <<EOF
## 8. API Layer

${api_status}

### 8.1 Current Status

| Surface | Status |
| --- | --- |
| Endpoint inventory | Expand with real routes and shapes if this repo exposes APIs |
| Middleware and auth | Expand when the transport contract is cataloged |
EOF

  cat > "$repo/doc/system/09-backend.md" <<EOF
## 9. Backend

This baseline section records the backend or core runtime surfaces detectable from the repo layout.

### 9.1 Observed Runtime Areas

| Surface | Current interpretation |
| --- | --- |
| Core runtime | Expand from \`app/\`, \`service/\`, \`cortex_runtime/\`, \`crates/\`, or \`src-tauri/\` as applicable |
| Delivery posture | Keep this section aligned with implemented code, not roadmap intent |
EOF

  cat > "$repo/doc/system/10-ecosystem-integration.md" <<EOF
## 10. Ecosystem Integration

This baseline section should be expanded with concrete downstream and upstream dependencies as they are documented.

### 10.1 Current Status

| Surface | Status |
| --- | --- |
| Shared service integrations | Expand as concrete integrations are cataloged |
| Cross-repo boundaries | Keep explicit as this repo's authority boundary is clarified |
EOF

  if has_any_dir "$repo" alembic migrations db sql models schemas; then
    db_status='Database, schema, or migration surfaces are present in the repository tree.'
  else
    db_status='No obvious database or migration directory was detected from the current top-level layout.'
  fi
  cat > "$repo/doc/system/11-database-schema.md" <<EOF
## 11. Database Schema

${db_status}

### 11.1 Current Status

| Surface | Status |
| --- | --- |
| Table inventory | Expand with real table, column, and constraint definitions |
| Migration contract | Expand if this repo owns migrations or persistent schemas |
EOF

  if has_any_dir "$repo" prompts analytics evals registry service tools; then
    ai_status='AI-adjacent, evaluation, or reasoning surfaces are present in the repo tree.'
  else
    ai_status='No obvious AI-specific directory was detected from the current top-level layout.'
  fi
  cat > "$repo/doc/system/12-ai-integration.md" <<EOF
## 12. AI Integration

${ai_status}

### 12.1 Current Status

| Surface | Status |
| --- | --- |
| Prompt or model routing docs | Expand as concrete AI surfaces are cataloged |
| Transparency and fallback posture | Record here when the current runtime contract is documented |
EOF

  cat > "$repo/doc/system/13-error-handling.md" <<EOF
## 13. Error Handling Contract

Current error-handling documentation is a baseline only.

### 13.1 Baseline Law

- fail closed on missing documentation truth, malformed inputs, and unsupported runtime states
- document real error envelopes here as soon as they are cataloged from code or tests
EOF

  cat > "$repo/doc/system/14-testing-infrastructure.md" <<EOF
## 14. Testing Infrastructure

This baseline section records only that testing surfaces exist in the repository tree.

### 14.1 Current Status

| Surface | Status |
| --- | --- |
| \`tests/\` directory | $(if [[ -d "$repo/tests" ]]; then echo 'Present'; else echo 'Not detected at top level'; fi) |
| QA expansion | Expand with concrete commands, suites, and pre-flight checks as they are cataloged |
EOF

  cat > "$repo/doc/system/15-handover-migration-notes.md" <<EOF
## 15. Handover / Migration Notes

This repository entered a baseline documentation-protocol migration on ${TODAY}.

### 15.1 Current Migration Note

- modular \`doc/system/\` was established or normalized to support root \`SYSTEM.md\`
- further authored expansion is still required for exact APIs, schemas, and runtime contracts
EOF
}

ensure_claude() {
  local repo="$1"
  local display_name="$2"
  if [[ -f "$repo/CLAUDE.md" ]]; then
    return 0
  fi
  mkdir -p "$repo/scripts"
  cat > "$repo/CLAUDE.md" <<EOF
# ${display_name} — Claude Instructions

## Module Map

| Module | Surface | Current role |
| --- | --- | --- |
$(detect_module_rows "$repo")

## Coding Standards

- Treat \`doc/system/\` part files as canonical; rebuild root \`SYSTEM.md\` with \`bash doc/system/BUILD.sh\`
- Keep documentation in present tense and aligned to implemented reality
- Prefer bounded patches over broad rewrites unless a file is clearly scaffold-only
- Do not bypass repo-local authority boundaries documented in \`SYSTEM.md\`

## File Conventions

- Canonical system docs live under \`doc/system/\`
- Root \`SYSTEM.md\` is a build artifact
- Supporting design material lives under \`docs/\`
- Repo automation scripts live under \`scripts/\`
- Tests live under \`tests/\` when present

## Context Loading

\`\`\`bash
# Show available sections and presets
./scripts/context-bundle.sh --list

# Core bundle
./scripts/context-bundle.sh --preset core

# Documentation or testing-focused bundles
./scripts/context-bundle.sh --preset docs
./scripts/context-bundle.sh --preset testing
\`\`\`

## Ecosystem Rules

- Keep cross-repo integrations explicit and documented
- Do not invent undocumented APIs, tables, routes, or environment variables
- If a runtime contract changes, update \`doc/system/\`, rebuild \`SYSTEM.md\`, and keep \`CLAUDE.md\` current

## Testing Expectations

- Run the repo's existing tests when available before claiming a change is complete
- Keep documentation build and context-bundle scripts working
- Expand test documentation in \`SYSTEM.md\` as exact suites and commands are cataloged

## Change Protocol

- Edit \`doc/system/\` part files, not the generated root \`SYSTEM.md\`
- Rebuild \`SYSTEM.md\` after documentation changes
- Keep new docs honest about current implementation state
EOF
}

ensure_architecture_docs() {
  local repo="$1"
  local display_name="$2"
  local slug="$3"
  mkdir -p "$repo/docs"

  if ! find "$repo/docs" -maxdepth 1 -type f -iname '*architecture*.md' | grep -q .; then
    cat > "$repo/docs/${slug}_architecture_spec.md" <<EOF
# ${display_name} Architecture Spec

**Document version:** 1.0 (${TODAY}) — Baseline protocol adoption

## 1. Purpose

This baseline architecture spec establishes a protocol-compliant design reference for ${display_name}.
It records only repository surfaces directly observable from the current working tree.

## 2. Current Implementation State

| Surface | Current truth |
| --- | --- |
| Canonical technical reference | \`doc/system/\` plus generated root \`SYSTEM.md\` |
| Repo-local instructions | \`CLAUDE.md\` |
| Current maturity | Baseline documentation protocol alignment |

## 3. Module Map

| Module | Surface | Current role |
| --- | --- | --- |
$(detect_module_rows "$repo")

## 4. Architectural Boundary

- this document is a baseline and must be expanded as concrete modules, routes, schemas, and integrations are cataloged
- when this spec and \`SYSTEM.md\` diverge, \`SYSTEM.md\` wins as the implemented reality reference
EOF
  fi

  if ! find "$repo/docs" -maxdepth 1 -type f -iname '*roadmap*.md' | grep -q .; then
    cat > "$repo/docs/${slug}_extended_roadmap.md" <<EOF
# ${display_name} Extended Roadmap

**Document version:** 1.0 (${TODAY}) — Baseline protocol adoption

## Current Status

| Phase | Status | Outcome |
| --- | --- | --- |
| Documentation normalization | Complete | Protocol-required baseline surfaces are present |
| Module catalog expansion | Pending | Expand exact routes, tables, and runtime contracts from code |
| QA alignment | Pending | Add repo-specific testing tiers and pre-flight checks |

## Phase 0 — Documentation Normalization

**Goal:** establish the required documentation stack and build surfaces.

**Delivered:**

- root \`CLAUDE.md\`
- modular \`doc/system/\`
- \`doc/system/BUILD.sh\`
- root \`SYSTEM.md\`
- \`scripts/context-bundle.sh\`

## Phase 1 — Exact Surface Expansion

**Goal:** replace baseline placeholders with exact module, API, schema, and environment documentation.

## Phase 2 — Verification Hardening

**Goal:** align repo-specific testing, QA, and handover documentation with current implementation reality.
EOF
  fi
}

ensure_doc_stack() {
  local repo="$1"
  local display_name="$2"
  local slug="$3"

  if [[ ! -f "$repo/doc/system/_index.md" ]]; then
    write_baseline_doc_system "$repo" "$display_name" "$slug"
  fi

  install_build_script "$repo" "$(legacy_output_rel "$repo")"
  ensure_gitignore "$repo"
  install_context_bundle "$repo"

  ensure_claude "$repo" "$display_name"
  ensure_architecture_docs "$repo" "$display_name" "$slug"
  (cd "$repo" && bash doc/system/BUILD.sh >/dev/null)
}

emit_report() {
  local report="$1"
  {
    echo "# Ecosystem Documentation Protocol Audit"
    echo
    echo "**Date:** ${TODAY}"
    echo "**Protocol source:** \`forgeHQ/BDS_DOCUMENTATION_PROTOCOL_v1.md\`"
    echo "**Mode:** $(if [[ "$WRITE_MODE" == true ]]; then echo 'write'; else echo 'audit'; fi)"
    echo
    echo "This audit tracks protocol-surface compliance first: required files, modular build surfaces, context-bundle entrypoints, and baseline architecture/roadmap presence."
    echo "A repo marked \`clean\` has the required protocol surfaces present and command-verified."
    echo "Repos that previously lacked authored docs may still carry baseline-generated sections that need deeper repo-specific expansion over time."
    echo
    echo "| Repo | CLAUDE.md | Root SYSTEM.md | doc/system | BUILD.sh | context-bundle | docs architecture | docs roadmap | context ignored | Notes |"
    echo "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |"
    while IFS= read -r repo; do
      local display_name
      display_name="$(repo_display_name "$repo")"
      local notes=()
      [[ -f "$repo/CLAUDE.md" ]] || notes+=("missing CLAUDE.md")
      [[ -f "$repo/SYSTEM.md" ]] || notes+=("missing root SYSTEM.md")
      [[ -d "$repo/doc/system" ]] || notes+=("missing doc/system")
      [[ -f "$repo/doc/system/BUILD.sh" ]] || notes+=("missing BUILD.sh")
      [[ -f "$repo/scripts/context-bundle.sh" ]] || notes+=("missing context-bundle")
      find "$repo/docs" -maxdepth 1 -type f -iname '*architecture*.md' 2>/dev/null | grep -q . || notes+=("missing architecture spec")
      find "$repo/docs" -maxdepth 1 -type f -iname '*roadmap*.md' 2>/dev/null | grep -q . || notes+=("missing roadmap")
      rg -n '^context-bundle\.md$' "$repo/.gitignore" >/dev/null 2>&1 || notes+=("context-bundle not gitignored")
      echo "| ${display_name} | $( [[ -f "$repo/CLAUDE.md" ]] && echo yes || echo no ) | $( [[ -f "$repo/SYSTEM.md" ]] && echo yes || echo no ) | $( [[ -d "$repo/doc/system" ]] && echo yes || echo no ) | $( [[ -f "$repo/doc/system/BUILD.sh" ]] && echo yes || echo no ) | $( [[ -f "$repo/scripts/context-bundle.sh" ]] && echo yes || echo no ) | $( find "$repo/docs" -maxdepth 1 -type f -iname '*architecture*.md' 2>/dev/null | grep -q . && echo yes || echo no ) | $( find "$repo/docs" -maxdepth 1 -type f -iname '*roadmap*.md' 2>/dev/null | grep -q . && echo yes || echo no ) | $( rg -n '^context-bundle\.md$' "$repo/.gitignore" >/dev/null 2>&1 && echo yes || echo no ) | ${notes[*]:-clean} |"
    done < <(find_repos)
  } > "$report"
}

main() {
  while IFS= read -r repo; do
    if [[ "$WRITE_MODE" == true ]]; then
      ensure_doc_stack "$repo" "$(repo_display_name "$repo")" "$(repo_slug "$repo")"
    fi
  done < <(find_repos)

  mkdir -p "$(dirname "$REPORT_PATH")"
  emit_report "$REPORT_PATH"
  printf '%s\n' "$REPORT_PATH"
}

main
