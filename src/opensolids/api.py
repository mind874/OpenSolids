from __future__ import annotations

from collections.abc import Iterable

from .material import Material
from .providers.base import Provider
from .registry import ProviderRegistry, default_registry
from .types import MaterialSummary


def material(material_id: str, *, registry: ProviderRegistry | None = None) -> Material:
    reg = registry or default_registry()
    return reg.material(material_id)


def search(
    query: str,
    *,
    required_properties: Iterable[str] | None = None,
    include_provider_records: bool = False,
    registry: ProviderRegistry | None = None,
) -> list[MaterialSummary]:
    reg = registry or default_registry()
    hits = reg.search(query, include_provider_records=include_provider_records)

    if required_properties is None:
        return hits

    required = {p for p in required_properties}
    if not required:
        return hits

    filtered: list[MaterialSummary] = []
    for hit in hits:
        mat = reg.material(hit.id)
        if required.issubset(set(mat.available_properties())):
            filtered.append(hit)
    return filtered


def list_providers(*, registry: ProviderRegistry | None = None) -> list[str]:
    reg = registry or default_registry()
    return reg.list_providers()


def list_material_ids(
    *,
    include_provider_records: bool = False,
    registry: ProviderRegistry | None = None,
) -> list[str]:
    reg = registry or default_registry()
    ids = reg.list_canonical_material_ids()
    if include_provider_records:
        for provider_name in reg.list_providers():
            ids.extend(reg.providers[provider_name].list_material_ids())
    return sorted(set(ids))


def register_provider(provider: Provider, *, registry: ProviderRegistry | None = None) -> None:
    reg = registry or default_registry()
    reg.register(provider)
