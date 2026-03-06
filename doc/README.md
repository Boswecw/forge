# doc/

Forge documentation hub and ecosystem-level system documentation.

## Contents

| Path | Purpose |
|------|---------|
| `system/` | Modular Forge documentation sections assembled by `BUILD.sh` |
| `SYSTEM.md` | Compiled ecosystem system documentation (generated) |
| `../docs/canonical/documentation_protocol_v1.md` | Canonical documentation standard governing protocol-bearing repo surfaces |
| `PREFIX_REGISTRY.md` | 2-char prefix assignments for all 13 protocol-bearing repos |

## Build

```bash
bash doc/system/BUILD.sh   # Regenerates SYSTEM.md from sections
```

See [`../docs/canonical/documentation_protocol_v1.md`](../docs/canonical/documentation_protocol_v1.md) for the full specification.
