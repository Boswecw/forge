#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "docs" / "canonical" / "documentation_registry_v1.json"


@dataclass(frozen=True)
class DocumentationSurface:
    repo_id: str
    display_name: str
    path: Path
    surface_type: str
    maturity_class: str
    doc_class: str
    policy_class: str
    requires_readme_contract: bool
    requires_doc_system: bool
    system_prefix: str | None
    assembled_system_path: Path | None
    status: str
    notes: str
    report_labels: tuple[str, ...]

    @property
    def root(self) -> Path:
        return ROOT if self.path == Path(".") else ROOT / self.path

    @property
    def readme_path(self) -> Path:
        return self.root / "README.md"

    @property
    def doc_system_dir(self) -> Path:
        return self.root / "doc" / "system"

    @property
    def index_path(self) -> Path:
        return self.doc_system_dir / "_index.md"

    @property
    def build_path(self) -> Path:
        return self.doc_system_dir / "BUILD.sh"

    @property
    def assembled_path(self) -> Path | None:
        if self.assembled_system_path is None:
            return None
        return ROOT / self.assembled_system_path

    @property
    def maintained_protocol_paths(self) -> list[Path]:
        paths: list[Path] = []
        if self.requires_readme_contract:
            paths.append(self.readme_path)
        if self.requires_doc_system:
            paths.append(self.index_path)
            if self.assembled_path is not None:
                paths.append(self.assembled_path)
        return paths

    @property
    def required_report_labels(self) -> tuple[str, ...]:
        labels = [self.repo_id, self.display_name, self.path.as_posix()]
        labels.extend(self.report_labels)
        deduped: list[str] = []
        for label in labels:
            if label not in deduped:
                deduped.append(label)
        return tuple(deduped)


@dataclass(frozen=True)
class DocumentationRegistry:
    registry_version: str
    effective_date: str
    owner: str
    protocol_spec: Path
    controlled_vocabularies: dict[str, tuple[str, ...]]
    surfaces: tuple[DocumentationSurface, ...]

    def surfaces_by_status(self, *statuses: str) -> tuple[DocumentationSurface, ...]:
        if not statuses:
            return self.surfaces
        return tuple(surface for surface in self.surfaces if surface.status in statuses)

    def surfaces_requiring_doc_system(self) -> tuple[DocumentationSurface, ...]:
        return tuple(surface for surface in self.surfaces if surface.requires_doc_system)

    def surfaces_requiring_readme(self) -> tuple[DocumentationSurface, ...]:
        return tuple(surface for surface in self.surfaces if surface.requires_readme_contract)


REQUIRED_ENTRY_KEYS = {
    "repo_id",
    "display_name",
    "path",
    "surface_type",
    "maturity_class",
    "doc_class",
    "requires_readme_contract",
    "requires_doc_system",
    "system_prefix",
    "assembled_system_path",
    "status",
    "notes",
    "policy_class",
}


def _coerce_path(value: str | None) -> Path | None:
    if value is None:
        return None
    return Path(value)


def load_registry(registry_path: Path = REGISTRY_PATH) -> DocumentationRegistry:
    raw = json.loads(registry_path.read_text(encoding="utf-8"))

    controlled_vocabularies = {
        key: tuple(values) for key, values in raw["controlled_vocabularies"].items()
    }

    surfaces: list[DocumentationSurface] = []
    seen_repo_ids: set[str] = set()
    seen_paths: set[str] = set()

    for entry in raw["surfaces"]:
        missing = REQUIRED_ENTRY_KEYS - entry.keys()
        if missing:
            raise ValueError(f"registry entry missing keys {sorted(missing)}: {entry}")

        if entry["repo_id"] in seen_repo_ids:
            raise ValueError(f"duplicate repo_id in registry: {entry['repo_id']}")
        seen_repo_ids.add(entry["repo_id"])

        path_value = Path(entry["path"]).as_posix()
        if path_value in seen_paths:
            raise ValueError(f"duplicate path in registry: {path_value}")
        seen_paths.add(path_value)

        for field in ("surface_type", "maturity_class", "doc_class", "status", "policy_class"):
            allowed = controlled_vocabularies[field]
            value = entry[field]
            if value not in allowed:
                raise ValueError(f"invalid {field} {value!r} for {entry['repo_id']}; allowed={allowed}")

        surfaces.append(
            DocumentationSurface(
                repo_id=entry["repo_id"],
                display_name=entry["display_name"],
                path=Path(entry["path"]),
                surface_type=entry["surface_type"],
                maturity_class=entry["maturity_class"],
                doc_class=entry["doc_class"],
                policy_class=entry["policy_class"],
                requires_readme_contract=bool(entry["requires_readme_contract"]),
                requires_doc_system=bool(entry["requires_doc_system"]),
                system_prefix=entry["system_prefix"],
                assembled_system_path=_coerce_path(entry["assembled_system_path"]),
                status=entry["status"],
                notes=entry["notes"],
                report_labels=tuple(entry.get("report_labels", [])),
            )
        )

    return DocumentationRegistry(
        registry_version=str(raw["registry_version"]),
        effective_date=raw["effective_date"],
        owner=raw["owner"],
        protocol_spec=ROOT / raw["protocol_spec"],
        controlled_vocabularies=controlled_vocabularies,
        surfaces=tuple(surfaces),
    )


def registry_payload(registry: DocumentationRegistry) -> dict[str, Any]:
    return {
        "registry_version": registry.registry_version,
        "effective_date": registry.effective_date,
        "owner": registry.owner,
        "protocol_spec": registry.protocol_spec.relative_to(ROOT).as_posix(),
        "surface_count": len(registry.surfaces),
        "surfaces": [
            {
                "repo_id": surface.repo_id,
                "display_name": surface.display_name,
                "path": surface.path.as_posix(),
                "surface_type": surface.surface_type,
                "maturity_class": surface.maturity_class,
                "doc_class": surface.doc_class,
                "policy_class": surface.policy_class,
                "requires_readme_contract": surface.requires_readme_contract,
                "requires_doc_system": surface.requires_doc_system,
                "system_prefix": surface.system_prefix,
                "assembled_system_path": None
                if surface.assembled_system_path is None
                else surface.assembled_system_path.as_posix(),
                "status": surface.status,
                "notes": surface.notes,
                "report_labels": list(surface.report_labels),
            }
            for surface in registry.surfaces
        ],
    }
