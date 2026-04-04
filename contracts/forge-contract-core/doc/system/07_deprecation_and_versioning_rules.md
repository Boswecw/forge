# 07 — Deprecation and Versioning Rules

## Version scheme

Family versions are monotonic integers: v1, v2, v3...

- v1 is the first admitted version for all proving-slice families.
- Major-version bumps (v1→v2) are required for breaking changes.
- Minor additions (new optional fields) do not require a version bump but must be documented.

## Active version support

At any time, the set of supported versions per family is defined in `enums.py`:

```python
ADMITTED_VERSIONS: dict[str, frozenset[int]] = {
    "source_drift_finding": frozenset({1}),
    ...
}
```

Consumers must reject unsupported versions. Unsupported version rejection is a non-retryable outcome.

## Dual-read posture

Dual-read (supporting two concurrent major versions) is not active in proving slice v1.

It may be enabled for a specific family during a version transition window. The enabling of dual-read requires an RFC.

## Deprecation lifecycle

| Stage | When | Action |
|---|---|---|
| Deprecated | New version admitted | Add to deprecation_registry.json, set deprecated_at |
| Sunset window | Announced in RFC | Consumers given time to migrate |
| Removed | After sunset | Remove version from ADMITTED_VERSIONS |

## Removing a version

A version may only be removed after its sunset_at date has passed and there are no known active consumers. Removal requires an RFC.

## Family retirement

A family may be retired when it has no active admitted producers or consumers. Retirement requires an RFC and full removal from all registries.

## Proving slice scope

For proving slice 01, no deprecations are active. The version registry is empty on the deprecation side at inception.
