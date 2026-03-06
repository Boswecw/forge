# Forge Ecosystem Tools

## build-ecosystem-docs

Aggregates Markdown documentation from independent local repos into a single local folder:

- `Ecosystem Documentation/`

### Run

```bash
node ./build-ecosystem-docs.mjs
```

### Dry run

```bash
node ./build-ecosystem-docs.mjs --dry-run
```

### Custom root/out

```bash
node ./build-ecosystem-docs.mjs --root ~/Forge/ecosystem --out ~/Forge/ecosystem/Ecosystem\ Documentation
```

### Include/exclude

```bash
node ./build-ecosystem-docs.mjs --include forge-smith,dataforge
node ./build-ecosystem-docs.mjs --exclude node_modules
```

### Output

* `Ecosystem Documentation/README.md` (index)
* `Ecosystem Documentation/<repo>/**` (copied docs with provenance headers)
* `Ecosystem Documentation/_meta/generation.log` (append-only)

Manual runs retain semantic authority; scheduled executions just keep the spine fresh and are recorded alongside the manual ones.

### generation.log schema

```
Run: <ISO timestamp>
Root: <root path>
Out:  <output path>
run_mode: manual | scheduled
invoked_by: <user or cron>
Repos scanned: N
Docs discovered: X
Docs copied:     Y
- <repo>: discovered=A copied=B
  WARN: ...
```
