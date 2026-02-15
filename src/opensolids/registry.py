from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field

from .canonical_catalog import (
    CANONICAL_MATERIALS_BY_ID,
    CanonicalMaterialSpec,
    build_canonical_lookup,
    normalize_lookup_key,
)
from .material import Material
from .providers.base import Provider
from .search import matches_query
from .types import MaterialSummary


@dataclass
class ProviderRegistry:
    providers: dict[str, Provider] = field(default_factory=dict)
    canonical_specs: dict[str, CanonicalMaterialSpec] = field(
        default_factory=lambda: dict(CANONICAL_MATERIALS_BY_ID)
    )
    canonical_lookup: dict[str, str] = field(default_factory=build_canonical_lookup)

    def register(self, provider: Provider) -> None:
        self.providers[provider.name] = provider

    def list_providers(self) -> list[str]:
        return sorted(self.providers.keys())

    def list_canonical_material_ids(self) -> list[str]:
        return sorted(self.canonical_specs.keys())

    def _resolve_provider(self, material_id: str) -> tuple[Provider, dict]:
        prefix = material_id.split(":", 1)[0]
        provider = self.providers.get(prefix)
        if provider and provider.has_material(material_id):
            return provider, provider.get_material_record(material_id)

        for candidate in self.providers.values():
            if candidate.has_material(material_id):
                return candidate, candidate.get_material_record(material_id)

        raise KeyError(f"Unknown material id: {material_id}")

    def resolve(self, material_id: str) -> tuple[Provider, dict]:
        return self._resolve_provider(material_id)

    def _resolve_canonical_id(self, material_id: str) -> str:
        if material_id in self.canonical_specs:
            return material_id
        normalized = normalize_lookup_key(material_id)
        canonical_id = self.canonical_lookup.get(normalized)
        if canonical_id is None:
            raise KeyError(f"Unknown material id: {material_id}")
        return canonical_id

    def _compose_canonical_record(self, canonical_id: str) -> tuple[dict, dict]:
        spec = self.canonical_specs[canonical_id]
        source_lookup: dict = {}
        selected_source_ids: list[str] = []
        properties: dict[str, dict] = {}

        for property_key, source_material_ids in spec.property_sources.items():
            for rank, source_material_id in enumerate(source_material_ids, start=1):
                try:
                    provider, source_record = self._resolve_provider(source_material_id)
                except KeyError:
                    continue

                source_curve = source_record.get("properties", {}).get(property_key)
                if source_curve is None:
                    continue

                curve_record = deepcopy(source_curve)
                metadata = dict(curve_record.get("metadata", {}))
                metadata["source_provider"] = provider.name
                metadata["source_material_id"] = source_record["id"]
                metadata["selection_rank"] = rank
                curve_record["metadata"] = metadata
                properties[property_key] = curve_record

                if curve_record.get("source_id"):
                    selected_source_ids.append(curve_record["source_id"])

                source_lookup.update(provider.source_lookup())
                break

        record = {
            "id": spec.id,
            "name": spec.name,
            "aliases": list(spec.aliases),
            "composition": spec.composition,
            "condition": spec.condition,
            "notes": spec.notes,
            "sources": sorted(set(selected_source_ids)),
            "properties": properties,
        }
        if spec.density_ref is not None:
            record["density_ref"] = float(spec.density_ref)
        return record, source_lookup

    def material(self, material_id: str) -> Material:
        try:
            provider, rec = self._resolve_provider(material_id)
        except KeyError:
            canonical_id = self._resolve_canonical_id(material_id)
            rec, source_lookup = self._compose_canonical_record(canonical_id)
            return Material.from_record(rec, source_lookup)

        return Material.from_record(rec, provider.source_lookup())

    def search(self, query: str, *, include_provider_records: bool = False) -> list[MaterialSummary]:
        out: list[MaterialSummary] = []

        for spec in self.canonical_specs.values():
            if not matches_query(query, spec.name, spec.id, spec.condition, *spec.aliases):
                continue
            material = self.material(spec.id)
            out.append(
                MaterialSummary(
                    id=spec.id,
                    name=spec.name,
                    provider="canonical",
                    condition=spec.condition,
                    aliases=tuple(spec.aliases),
                    canonical_id=spec.id,
                    source_count=len(material.sources),
                    property_coverage=tuple(material.available_properties()),
                )
            )

        if include_provider_records:
            for provider in self.providers.values():
                out.extend(provider.search(query))

        out.sort(key=lambda item: (item.provider != "canonical", item.name, item.id))
        return out


_DEFAULT_REGISTRY: ProviderRegistry | None = None


def default_registry() -> ProviderRegistry:
    global _DEFAULT_REGISTRY
    if _DEFAULT_REGISTRY is not None:
        return _DEFAULT_REGISTRY

    from .providers.curated_public.provider import CuratedPublicProvider
    from .providers.mil_hdbk_5.provider import MilHdbk5Provider
    from .providers.nist_cryo.provider import NISTCryoProvider
    from .providers.ntrs_openapi.provider import NTRSOpenAPIProvider

    reg = ProviderRegistry()
    reg.register(CuratedPublicProvider())
    reg.register(NISTCryoProvider())
    reg.register(NTRSOpenAPIProvider())
    reg.register(MilHdbk5Provider())
    _DEFAULT_REGISTRY = reg
    return reg
