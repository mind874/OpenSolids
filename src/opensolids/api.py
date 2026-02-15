from __future__ import annotations

from .material import Material
from .providers.base import Provider
from .registry import ProviderRegistry, default_registry
from .types import MaterialSummary


def material(material_id: str, *, registry: ProviderRegistry | None = None) -> Material:
    reg = registry or default_registry()
    return reg.material(material_id)


def search(query: str, *, registry: ProviderRegistry | None = None) -> list[MaterialSummary]:
    reg = registry or default_registry()
    return reg.search(query)


def list_providers(*, registry: ProviderRegistry | None = None) -> list[str]:
    reg = registry or default_registry()
    return reg.list_providers()


def register_provider(provider: Provider, *, registry: ProviderRegistry | None = None) -> None:
    reg = registry or default_registry()
    reg.register(provider)
