from __future__ import annotations

from dataclasses import dataclass, field

from .material import Material
from .providers.base import Provider
from .types import MaterialSummary


@dataclass
class ProviderRegistry:
    providers: dict[str, Provider] = field(default_factory=dict)

    def register(self, provider: Provider) -> None:
        self.providers[provider.name] = provider

    def list_providers(self) -> list[str]:
        return sorted(self.providers.keys())

    def resolve(self, material_id: str) -> tuple[Provider, dict]:
        prefix = material_id.split(":", 1)[0]
        provider = self.providers.get(prefix)
        if provider and provider.has_material(material_id):
            return provider, provider.get_material_record(material_id)

        for candidate in self.providers.values():
            if candidate.has_material(material_id):
                return candidate, candidate.get_material_record(material_id)

        raise KeyError(f"Unknown material id: {material_id}")

    def material(self, material_id: str) -> Material:
        provider, rec = self.resolve(material_id)
        return Material.from_record(rec, provider.source_lookup())

    def search(self, query: str) -> list[MaterialSummary]:
        out: list[MaterialSummary] = []
        for provider in self.providers.values():
            out.extend(provider.search(query))
        out.sort(key=lambda item: (item.provider, item.name, item.id))
        return out


_DEFAULT_REGISTRY: ProviderRegistry | None = None


def default_registry() -> ProviderRegistry:
    global _DEFAULT_REGISTRY
    if _DEFAULT_REGISTRY is not None:
        return _DEFAULT_REGISTRY

    from .providers.mil_hdbk_5.provider import MilHdbk5Provider
    from .providers.nist_cryo.provider import NISTCryoProvider
    from .providers.ntrs_openapi.provider import NTRSOpenAPIProvider

    reg = ProviderRegistry()
    reg.register(NISTCryoProvider())
    reg.register(NTRSOpenAPIProvider())
    reg.register(MilHdbk5Provider())
    _DEFAULT_REGISTRY = reg
    return reg
