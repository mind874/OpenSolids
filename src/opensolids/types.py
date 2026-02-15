from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class SourceRef:
    source_id: str
    title: str
    publisher: str
    organization: str | None
    url_or_citation_id: str
    license_notes: str
    retrieved_at: str
    page_or_table: str | None
    extraction_method: str
    metadata: dict[str, Any]


@dataclass(frozen=True)
class MaterialSummary:
    id: str
    name: str
    provider: str
    condition: str | None
    aliases: tuple[str, ...]
