# BDS Doctrine Controls

> Machine-readable doctrine enforcement for Forge ecosystem

## Overview

This directory contains the **BDS Doctrine** - a set of machine-readable controls that enforce architectural, security, and quality standards across the Forge platform through automated validation.

### Purpose

- **Automated Quality Gates**: Block problematic patterns before they reach production
- **AI Code Generation Safety**: Ensure Claude-generated code follows BDS standards
- **Drift Visibility**: Track compliance trends across the codebase
- **Prompt Conditioning**: Feed recent violations back into AI prompts to prevent recurrence

## Directory Structure

```
doctrine/
├── README.md (this file)
├── bds_controls.json              # Control definitions
└── schemas/
    ├── bds_controls.schema.json          # JSON Schema for controls
    └── violation_signature.schema.json   # JSON Schema for evidence/reports
```

## Control Categories

| Category | Purpose | Examples |
|----------|---------|----------|
| **BDS-SEC** | Security enforcement | API key detection, path traversal prevention, SQL injection |
| **BDS-MAPO** | Model routing constraints | Capability routing, adapter isolation, no direct model IDs |
| **BDS-ARCH** | Architectural consistency | Svelte 5 runes, no global state, separation of concerns |
| **BDS-TEST** | Testing requirements | Test coverage, logging standards |
| **BDS-INT** | Ecosystem integration | Cross-service contracts, dependency alignment |

## Control Definition Format

Each control in `bds_controls.json` follows this structure:

```json
{
  "id": "BDS-SEC-001",
  "category": "BDS-SEC",
  "severity": "block",
  "kind": "regex_scan",
  "enabled": true,
  "message": "Human-readable violation description",
  "fixHint": "Suggested remediation steps",
  "match": {
    "pattern": "regex pattern",
    "flags": "gi"
  },
  "allowedPaths": ["**/*.test.ts"],
  "targetPaths": ["**/*.ts"],
  "tags": ["security", "secrets"]
}
```

### Control Fields

- **id**: Unique identifier (format: `BDS-{CATEGORY}-{NUMBER}`)
- **category**: One of: BDS-SEC, BDS-MAPO, BDS-ARCH, BDS-TEST, BDS-INT
- **severity**:
  - `block` - Stops merge/deployment
  - `warn` - Alerts but allows merge
  - `info` - Logs for visibility
- **kind**: Type of check
  - `regex_scan` - Pattern matching in file contents
  - `import_restriction` - Import statement validation
  - `command` - Execute shell command (e.g., run tests)
- **match**: Pattern or command definition
  - For `regex_scan`/`import_restriction`: `{ "pattern": "...", "flags": "gi" }`
  - For `command`: `{ "command": "npm test", "expectExitCode": 0 }`
- **allowedPaths**: Glob patterns exempt from this check (e.g., test files)
- **targetPaths**: Glob patterns to specifically check (empty = all files)

## Adding a New Control

1. **Choose an ID**: Use next available number in category (e.g., `BDS-SEC-004`)
2. **Define the check**:
   ```json
   {
     "id": "BDS-SEC-004",
     "category": "BDS-SEC",
     "severity": "warn",
     "kind": "regex_scan",
     "enabled": true,
     "message": "Detected eval() usage - security risk",
     "fixHint": "Replace eval() with safer alternatives like JSON.parse() or Function constructor",
     "match": {
       "pattern": "\\beval\\s*\\(",
       "flags": "g"
     },
     "allowedPaths": ["**/*.test.ts"],
     "targetPaths": ["**/*.ts", "**/*.js"],
     "tags": ["security", "code-injection"]
   }
   ```
3. **Validate against schema**:
   ```bash
   cd Forge/tools/doctrine-validator
   npm run validate-controls
   ```
4. **Test the control**:
   ```bash
   node dist/index.js validate --paths ../../path/to/test/file
   ```

## Exempting Code from Checks

### Option 1: Path-based exemption (Recommended)

Add glob patterns to `allowedPaths` in the control definition:

```json
{
  "allowedPaths": [
    "**/*.test.ts",
    "**/fixtures/**",
    "**/legacy/old-system/**"
  ]
}
```

### Option 2: Inline comments (Future)

_Not implemented in v1.0_

```typescript
// doctrine-disable-next-line BDS-SEC-001
const apiKey = "temporary-key-for-demo";
```

## Running Validation

### Local CLI

```bash
# Validate specific commit
cd Forge/tools/doctrine-validator
node dist/index.js validate --commit HEAD --out ../../evidence/doctrine

# Validate specific files
node dist/index.js validate --paths "../../ecosystem/**/*.ts" --out ../../evidence/doctrine

# Generate conditioning preamble (for AI prompts)
node dist/index.js preamble --from ../../evidence/doctrine --days 7 --limit 30
```

### CI/CD Integration

Doctrine validation runs automatically on:
- Pull requests to `main` or `develop`
- Push to protected branches

See `.github/workflows/doctrine_check.yml` for configuration.

### Exit Codes

- **0**: No blocking violations (pass)
- **1**: Blocking violations found (fail)

## Evidence Output

Validation runs produce evidence files in:
```
Forge/evidence/doctrine/YYYY-MM-DD/HHmmssZ_doctrine_report.json
```

Evidence includes:
- Timestamp, commit SHA, branch
- Generator marker (e.g., `claude-code`)
- List of violations with file/line/snippet
- Summary counts by severity

See `schemas/violation_signature.schema.json` for full format.

## Viewing Drift Trends

ForgeCommand includes a **Doctrine Drift Panel** that visualizes:
- Top violated controls
- Trend over last N runs (up/down/flat)
- Recent violation details

Enable in ForgeCommand settings or navigate to `/doctrine` route.

## Schema Validation

Both `bds_controls.json` and evidence reports are validated against JSON schemas:

- **Controls**: `schemas/bds_controls.schema.json`
- **Evidence**: `schemas/violation_signature.schema.json`

Validation happens automatically during:
1. Control loading in doctrine-validator
2. Evidence generation
3. CI pipeline checks

## Common Patterns

### Allowing test files

Most controls should exempt test files:
```json
"allowedPaths": ["**/*.test.ts", "**/*.spec.ts", "**/test/**", "**/tests/**"]
```

### Targeting specific file types

Use `targetPaths` to limit scope:
```json
"targetPaths": ["**/*.ts", "**/*.js"]  // TypeScript/JavaScript only
"targetPaths": ["**/*.rs"]              // Rust only
"targetPaths": ["**/*.svelte"]          // Svelte components only
```

### Command-based checks

Run external tools as controls:
```json
{
  "kind": "command",
  "match": {
    "command": "cargo clippy -- -D warnings",
    "cwd": "src-tauri",
    "expectExitCode": 0
  }
}
```

## Disabling Controls

### Temporarily disable a control

Set `"enabled": false` in `bds_controls.json`:
```json
{
  "id": "BDS-ARCH-003",
  "enabled": false,
  "message": "..."
}
```

### Reduce severity

Change from `block` to `warn` or `info`:
```json
{
  "severity": "warn"  // Won't block merge
}
```

## Best Practices

1. **Start with `warn` severity** for new controls - observe false positive rate first
2. **Be specific with patterns** - overly broad patterns create noise
3. **Always provide `fixHint`** - guide developers toward correct solution
4. **Test controls before committing** - validate against known violations
5. **Review exemptions regularly** - ensure `allowedPaths` remain necessary
6. **Use tags for filtering** - helps with reporting and analysis

## Troubleshooting

### "Control not triggering"

- Check `enabled` field is `true`
- Verify `targetPaths` includes the file type
- Test regex pattern in isolation: `echo "test code" | grep -P "pattern"`

### "Too many false positives"

- Add specific paths to `allowedPaths`
- Refine regex pattern to be more specific
- Consider changing severity to `warn` temporarily

### "Schema validation error"

- Validate JSON syntax: `jq . bds_controls.json`
- Check against schema: `npm run validate-controls`
- Ensure all required fields are present

## Version History

- **1.0.0** (2025-12-22): Initial release with 12 starter controls
  - 3 security controls
  - 3 MAPO routing controls
  - 3 architectural controls
  - 3 testing controls

## Support

- **Issues**: File in Forge repository issue tracker
- **Questions**: #forge-platform Slack channel
- **Documentation**: See `/docs/doctrine/` for architectural details

---

**Maintained by:** Forge Platform Team
**Last Updated:** 2025-12-22
