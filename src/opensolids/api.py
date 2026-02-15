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
    registry: ProviderRegistry | None = None,
) -> list[MaterialSummary]:
    reg = registry or default_registry()
    hits = reg.search(query)

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


def register_provider(provider: Provider, *, registry: ProviderRegistry | None = None) -> None:
    reg = registry or default_registry()
    reg.register(provider)
