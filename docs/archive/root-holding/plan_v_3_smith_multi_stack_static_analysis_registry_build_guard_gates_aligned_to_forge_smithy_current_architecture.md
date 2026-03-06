# Plan v3 — SMITH Multi-Stack Static Analysis Registry + BuildGuard Gates (Aligned to Current forge-smithy)

## Document Header

| Field | Value |
|------|-------|
| **Version** | v3 |
| **Date** | 2026-03-03 |
| **Owner** | Charlie / BDS |
| **Target Repo** | forge-smithy (Forge:SMITH) |
| **Scope** | Extend BuildGuard’s existing plugin+stack detection to full multi-stack static analysis (format/lint/type/schema/secrets/vulns/sast/policy) |
| **Blast Radius** | Class B — new plugin(s) + adapters + UI surfacing (no changes to MRPA / smith immutable core) |
| **Key Constraint** | Reuse existing BuildGuard command surface (`guard_detect`, `guard_run`, report exports) and ledger/evidence machinery; do **not** invent parallel “static runner” flows |

## Revision History

| Version | Date | Changes |
|---|---|---|
| v2 | 2026-03-03 | Original plan (new `buildguard/static/` subsystem + new command) |
| v3 | 2026-03-03 | Refit to current SMITH architecture: BuildGuard already has plugins, stack detection, evidence/reporting/ledger — we extend those instead of creating a parallel subsystem |

---

## 1) What you already have (baseline reality)

From the current forge-smithy system docs:

- SMITH has **BuildGuard** with a plugin model and commands like `guard_list_plugins`, `guard_detect`, `guard_run`, and exports including JSON/Markdown/SARIF. (See BuildGuard commands list.)
- BuildGuard already does **stack detection** for Python/TypeScript/Rust and runs “type check / lint / security / dependency audit / custom” gates. (Existing stack detection signals are already defined.)
- Repo already includes a robust `scripts/` directory with guard/lint/CI automation, plus `schemas/`, `governance/`, and `evidence/` roots.

**So:** v3 keeps your existing BuildGuard model as the single authority surface, and implements multi-stack coverage as **BuildGuard plugins + adapters**, not as a separate “static subsystem.”

---

## 2) Tool coverage (same toolset, now expressed as BuildGuard plugins)

Keep the same tooling intent from v2:

### Frontend
- ESLint (JS/TS) + Solid plugin
- TypeScript (`tsc --noEmit`)
- Prettier (+ optional Tailwind plugin)
- Svelte: `svelte-check` (+ `svelte-eslint-parser` if using ESLint)
- HTML: `html-validate`
- CSS: `stylelint` (+ prettier interop)
- Markdown: `markdownlint-cli2`

### Backend / Languages
- Python: Ruff (lint+format), mypy (type)
- Rust: `cargo fmt --check`, `cargo clippy`, `cargo deny`
- Go: `golangci-lint`
- C/C++: `clang-format`, `clang-tidy` (opt-in; needs compile db)

### Infra / Config
- Terraform: `terraform validate`, `tflint`, `tfsec`
- Dockerfile: `hadolint`
- YAML: `yamllint`
- JSON schema: `ajv` (primary)

### Security
- Secrets: `gitleaks`
- Vulns: `trivy` (primary), `osv-scanner` (secondary)
- SAST: `semgrep`

---

## 3) Architecture changes (v3 mapping)

### 3.1 Principle

**Everything runs through BuildGuard’s existing plugin pipeline**:

- Detection: `guard_detect` decides what applies.
- Execution: `guard_run` runs one plugin at a time (and/or a composed group), using a shared process runner.
- Evidence: writes raw logs + normalized findings into the existing evidence bundle structure.
- Reporting: `guard_report_json/markdown/sarif` stays the standard export surface.

### 3.2 New/extended code areas (names are guidance; align to existing module layout)

1) **BuildGuard plugin set expansion**
- Add/extend plugins so they cover the v2 block classes:
  - `format`
  - `lint`
  - `type`
  - `schema`
  - `secrets`
  - `vulns`
  - `sast`
  - `policy`

2) **Universal Finding contract (normalized)**
- Ensure every plugin returns a normalized finding list (even if source tool output is text).
- Keep a stable structure so JSON/SARIF exporters can map consistently.

3) **Shared process runner reuse**
- If BuildGuard already has a command runner, extend it with:
  - timeouts per plugin
  - deterministic cwd
  - captured stdout/stderr persisted to evidence
  - tool version capture (required in `release`)

### 3.3 Evidence layout (aligned)

Instead of creating a parallel `static_report.json`, store per-plugin evidence consistently:

- `evidence/buildguard/<plugin_id>/raw/<tool>.stdout.log`
- `evidence/buildguard/<plugin_id>/raw/<tool>.stderr.log`
- `evidence/buildguard/<plugin_id>/report.json` (plugin-level normalized report)

Then the **BuildGuard aggregated report** (your existing `guard_report_json`) becomes the canonical “static report.”

---

## 4) Detection rules (extend BuildGuard’s existing stack detection)

BuildGuard already detects Python/TS/Rust. Extend detection signals so `guard_detect` can add the new plugins:

### Frontend
- JS/TS: `package.json`
- TS: `tsconfig.json`
- Solid: deps include `solid-js` or `vite-plugin-solid`
- Svelte: `svelte.config.*` or any `*.svelte`
- Tailwind: `tailwind.config.*` or `@tailwind` usage
- CSS: `*.css` / `postcss.config.*`
- HTML: `*.html`
- Markdown: `*.md`

### Backend
- Go: `go.mod`
- C/C++: `compile_commands.json` / `CMakeLists.txt` / `*.c/*.cpp`

### Infra
- Terraform: `*.tf`
- Docker: `Dockerfile` / `*.Dockerfile`
- YAML: `*.yml/*.yaml`
- JSON: `*.json` + schema folders

### Security
- gitleaks: always runnable
- vulns: detect lockfiles (`bun.lockb`, `pnpm-lock.yaml`, `Cargo.lock`, `go.sum`, etc.)
- semgrep: always runnable

---

## 5) Profiles + gating defaults (ported as BuildGuard policy)

Implement policy at the BuildGuard layer (you already have `forge.policy.json` and BuildGuard gate policy concepts):

### dev (fast)
- FORMAT: warn
- LINT: fail on errors
- TYPE: warn
- SCHEMA: fail when schema is configured
- SECRETS: fail
- VULNS/SAST/POLICY: warn

### strict (engineering)
- FORMAT/LINT/TYPE/SCHEMA/SECRETS: fail
- VULNS: fail on High/Critical
- SAST: fail on High ruleset
- POLICY: fail on advisories/licenses

### release (ship)
- strict + missing tool => fail
- tool versions captured => required
- baseline must be empty or explicitly approved

---

## 6) Baseline debt (regression-only enforcement)

Keep the baseline concept from v2, but store it where your governance system expects it.

- Baseline file: `governance/static_baseline.json` (or keep `doc/governance/` if that’s your canonical governance doc root — choose the path that matches current repo conventions)
- Contents: stable hashes of normalized findings per plugin/tool.

Behavior:
- dev/strict: block only *new* violations above thresholds.
- release: baseline must be empty or approved/signed.

---

## 7) UI/HUD surfacing (SvelteKit)

Add a “Static Analysis” area that is driven by the existing BuildGuard report exports.

Tabs:
- Overview
- Format
- Lint
- Type
- Schema
- Secrets
- Vulns
- SAST
- Policy

Each tab:
- status + counts
- findings table
- links to raw logs
- rerun button (invokes `guard_run` with same profile/plugin)

---

## 8) Implementation slices (rewired to current BuildGuard commands)

### Slice 1 — Extend BuildGuard plugin interface + runner hardening
**Goal:** one plugin can run commands, persist raw logs, return normalized findings.

Acceptance:
- `guard_run` can execute an arbitrary plugin with timeout + evidence writing.

### Slice 2 — Detection expansion
**Goal:** `guard_detect` selects the new plugins based on repo signals.

Acceptance:
- On a repo with Svelte/TS/Rust/etc, `guard_detect` returns the expected plugin set.

### Slice 3 — Adapters/parsers (JSON-first)
Implement parsers in this order:
1) eslint (json)
2) ruff (json)
3) trivy (json)
4) gitleaks (json)
5) tfsec/tflint (json)
6) golangci-lint (json)
7) stylelint (json)
8) markdownlint (json)
9) mypy (json-report)
10) hadolint (json)

Then text parsers:
- svelte-check
- yamllint

Acceptance:
- Plugin reports contain normalized `Finding[]` for each tool.

### Slice 4 — Policy + baseline gate
Acceptance:
- dev/strict/release behavior matches §5.
- Baseline blocks regressions only.

### Slice 5 — HUD
Acceptance:
- Operator can see failures instantly and rerun a plugin.

---

## 9) VS Code implementation packet (what Codex should do)

Use this as the Codex task framing inside VS Code:

1) **Locate BuildGuard plugin architecture**
- Find where plugin traits/interfaces live.
- Identify how `guard_detect` builds plugin lists.
- Identify how `guard_run` executes a plugin and writes evidence.

2) **Implement new plugins (stubs first)**
- Add plugin IDs for: `format`, `lint`, `type`, `schema`, `secrets`, `vulns`, `sast`, `policy`.
- Each stub returns “SKIPPED” with an explicit reason if detection doesn’t apply.

3) **Extend detection signals**
- Add filesystem sniff rules listed in §4.

4) **Add runner features**
- tool version capture (command per tool)
- stdout/stderr capture to evidence paths
- timeout controls

5) **Implement adapters in Slice 3 order**
- For each tool:
  - command builder
  - parser (JSON preferred)
  - normalized Finding mapping

6) **Wire policy + baseline**
- baseline file read/write
- diff logic to isolate new findings
- release rules (missing tool => fail)

7) **UI**
- Add Static Analysis section reading BuildGuard report JSON
- Add plugin rerun actions

Done criteria:
- `guard_detect` + `guard_run` cover multi-stack across a real repo.
- `guard_report_json` includes these plugins with normalized findings.

---

## 10) Notes / constraints

- Prefer repo-native commands first (e.g., `pnpm lint`, `pnpm check`, `pnpm guard:all`) when they already exist, but still normalize results.
- Don’t add any new “parallel” top-level command if the existing `guard_*` command surface can express it cleanly.
- Keep MRPA and `smith/` immutable core untouched.

