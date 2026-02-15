from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Protocol

from opensolids.search import matches_query
from opensolids.types import MaterialSummary, SourceRef
from opensolids.validation import validate_material_record


class Provider(Protocol):
    name: str
    version: str

    def has_material(self, material_id: str) -> bool:
        ...

    def get_material_record(self, material_id: str) -> dict:
        ...

    def search(self, query: str) -> list[MaterialSummary]:
        ...

    def list_material_ids(self) -> list[str]:
        ...

    def source_lookup(self) -> dict[str, SourceRef]:
        ...


class LocalDataPackProvider:
    def __init__(
        self,
        *,
        name: str,
        version: str,
        package_name: str,
        fallback_path: Path,
    ):
        self.name = name
        self.version = version
        self.package_name = package_name
        self.fallback_path = fallback_path

        self._loaded = False
        self._materials: dict[str, dict] = {}
        self._sources: dict[str, SourceRef] = {}

    def _resolve_base_path(self) -> Path:
        try:
            module = importlib.import_module(self.package_name)
            module_file = getattr(module, "__file__", None)
            if module_file:
                return Path(module_file).resolve().parent
        except ModuleNotFoundError:
            pass

        return self.fallback_path

    def _ensure_loaded(self) -> None:
        if self._loaded:
            return

        base = self._resolve_base_path()
        materials_dir = base / "materials"
        sources_dir = base / "sources"

        if sources_dir.exists():
            for fp in sorted(sources_dir.glob("*.json")):
                payload = json.loads(fp.read_text())
                if isinstance(payload, list):
                    records = payload
                else:
                    records = [payload]
                for rec in records:
                    self._sources[rec["source_id"]] = SourceRef(
                        source_id=rec["source_id"],
                        title=rec["title"],
                        publisher=rec["publisher"],
                        organization=rec.get("organization"),
                        url_or_citation_id=rec["url_or_citation_id"],
                        license_notes=rec.get("license_notes", ""),
                        retrieved_at=rec["retrieved_at"],
                        page_or_table=rec.get("page_or_table"),
                        extraction_method=rec.get("extraction_method", "manual"),
                        metadata=rec.get("metadata", {}),
                    )

        if materials_dir.exists():
            for fp in sorted(materials_dir.glob("*.json")):
                rec = json.loads(fp.read_text())
                validate_material_record(rec)
                self._materials[rec["id"]] = rec

        self._loaded = True

    def has_material(self, material_id: str) -> bool:
        self._ensure_loaded()
        return material_id in self._materials

    def get_material_record(self, material_id: str) -> dict:
        self._ensure_loaded()
        return self._materials[material_id]

    def list_material_ids(self) -> list[str]:
        self._ensure_loaded()
        return sorted(self._materials.keys())

    def source_lookup(self) -> dict[str, SourceRef]:
        self._ensure_loaded()
        return dict(self._sources)

    def search(self, query: str) -> list[MaterialSummary]:
        self._ensure_loaded()
        out: list[MaterialSummary] = []

        for rec in self._materials.values():
            aliases = rec.get("aliases", [])
            if matches_query(query, rec.get("name"), rec.get("id"), rec.get("condition"), *aliases):
                out.append(
                    MaterialSummary(
                        id=rec["id"],
                        name=rec["name"],
                        provider=self.name,
                        condition=rec.get("condition"),
                        aliases=tuple(aliases),
                        source_count=len(rec.get("sources", [])),
                        property_coverage=tuple(sorted(rec.get("properties", {}).keys())),
                    )
                )

        return out
