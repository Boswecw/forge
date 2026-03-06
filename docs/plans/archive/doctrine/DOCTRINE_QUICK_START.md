# Doctrine Validation - Quick Start

## 🚀 What is this?

Automated quality enforcement for Forge ecosystem that:
- ✅ Scans code on every commit
- ✅ Blocks PRs with security/quality violations
- ✅ Generates evidence reports
- ✅ Shows trends in ForgeCommand dashboard

---

## 📁 Key Files

| Path | Purpose |
|------|---------|
| [`doctrine/bds_controls.json`](../doctrine/bds_controls.json) | 12 quality control rules |
| [`tools/doctrine-validator/`](../tools/doctrine-validator/) | CLI tool (TypeScript) |
| [`.github/workflows/doctrine_check.yml`](.github/workflows/doctrine_check.yml) | CI gate |
| [`Forge_Command/src/lib/components/doctrine/`](Forge_Command/src/lib/components/doctrine/) | Dashboard widget |
| [`evidence/doctrine/`](../evidence/doctrine/) | Generated reports |

---

## 🔨 Commands

### Validate Locally
```bash
cd /home/charlie/Forge/tools/doctrine-validator
npm run build
node dist/index.js validate --commit HEAD --verbose
```

### Check Specific Files
```bash
node dist/index.js validate --paths "ecosystem/**/*.ts" "ecosystem/**/*.rs"
```

### Generate AI Preamble
```bash
node dist/index.js preamble --days 7 --limit 30
```

---

## 🎯 Control Categories

- **BDS-SEC** (Security): Hardcoded secrets, SQL injection, XSS
- **BDS-MAPO** (Patterns): Error handling, async patterns, logging
- **BDS-ARCH** (Architecture): Singletons, dependency injection, circular deps
- **BDS-TEST** (Testing): Coverage, skipped tests, missing assertions
- **BDS-INT** (Integration): Contract drift, dependency alignment _(future)_

---

## 🚦 Severity Levels

| Level | Name | Behavior |
|-------|------|----------|
| `block` | Blocker | ❌ Fails CI, blocks merge |
| `warn` | Warning | ⚠️ Alerts but allows merge |
| `info` | Info | ℹ️ Logged for awareness |

---

## 📊 ForgeCommand Widget

Add to dashboard:
```svelte
<script>
  import { DoctrineDriftPanel } from '$lib/components/doctrine';
</script>

<DoctrineDriftPanel />
```

**Shows:**
- Latest validation result (pass/fail)
- Violation counts by severity
- Trend arrows per control (↑↓→✦)
- Historical patterns

---

## 🔧 Add New Control

Edit [`doctrine/bds_controls.json`](../doctrine/bds_controls.json):

```json
{
  "id": "BDS-SEC-004",
  "category": "BDS-SEC",
  "severity": "block",
  "kind": "regex_scan",
  "enabled": true,
  "message": "Detect password in plain text",
  "fixHint": "Use bcrypt or argon2 for password hashing",
  "match": {
    "pattern": "password\\s*=\\s*['\"][^'\"]{8,}['\"]",
    "flags": "gi"
  },
  "allowedPaths": ["**/*.test.ts", "**/*.example.*"],
  "targetPaths": ["**/*.ts", "**/*.js"]
}
```

Then commit and push - CI will enforce immediately.

---

## 📖 Full Documentation

- **[Implementation Summary](DOCTRINE_VALIDATION_IMPLEMENTATION.md)** - Complete technical details
- **[Controls README](../doctrine/README.md)** - Control authoring guide
- **[CLI README](../tools/doctrine-validator/README.md)** - Validator usage
- **[Widget README](Forge_Command/src/lib/components/doctrine/README.md)** - Component integration

---

## ⚡ Quick Test

```bash
# 1. Build validator
cd /home/charlie/Forge/tools/doctrine-validator && npm run build

# 2. Run validation
node dist/index.js validate --commit HEAD --out ../../evidence/doctrine

# 3. Check evidence
ls -lh /home/charlie/Forge/evidence/doctrine/$(date +%Y-%m-%d)/

# 4. View in ForgeCommand
cd /home/charlie/Forge/ecosystem/Forge_Command && npm run dev
```

---

## 🆘 Troubleshooting

**"No files found to scan"**
→ Check `git status` - ensure you're in a git repo with committed changes

**"Controls validation failed"**
→ Run: `jq . doctrine/bds_controls.json` to verify JSON syntax

**Widget shows no violations**
→ Widget uses mock data by default - see [Widget README](Forge_Command/src/lib/components/doctrine/README.md) to enable Tauri command

**CI workflow not running**
→ Verify [`.github/workflows/doctrine_check.yml`](.github/workflows/doctrine_check.yml) is committed to `main` or `develop`

---

## 🎓 Next Steps

1. ✅ Test CLI locally
2. ✅ Push commit to trigger CI
3. ✅ Review evidence in GitHub Actions artifacts
4. ✅ Add DoctrineDriftPanel to ForgeCommand dashboard
5. ⬜ Implement Tauri command for real-time evidence loading
6. ⬜ Add project-specific controls to `bds_controls.json`
7. ⬜ Enable branch protection to require passing validation

---

**Status:** ✅ Fully implemented (Batches 0-4 complete)
**Version:** 1.0.0
**Date:** 2025-12-22
