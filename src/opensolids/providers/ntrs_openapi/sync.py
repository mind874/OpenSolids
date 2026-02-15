from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from .client import NTRSOpenAPIClient
from .compliance import is_safe_for_numeric_extraction



def sync_ntrs(
    output_dir: Path,
    *,
    since: str,
    curated_citation_ids: list[str] | None = None,
    client: NTRSOpenAPIClient | None = None,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    materials_dir = output_dir / "materials"
    sources_dir = output_dir / "sources"
    materials_dir.mkdir(exist_ok=True)
    sources_dir.mkdir(exist_ok=True)

    ntrs = client or NTRSOpenAPIClient()
    curated_citation_ids = curated_citation_ids or []

    source_count = 0
    for citation_id in curated_citation_ids:
        citation = ntrs.get_citation(citation_id)
        source = {
            "source_id": f"ntrs-src:{citation_id}",
            "title": citation.get("title") or f"NASA NTRS Citation {citation_id}",
            "publisher": "NASA STI",
            "organization": "NASA",
            "url_or_citation_id": citation.get("stiUrl") or citation.get("url") or citation_id,
            "license_notes": "NTRS metadata stored; full text redistribution disabled by default.",
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "page_or_table": None,
            "extraction_method": "manual",
            "metadata": {
                "citation_id": citation_id,
                "safe_for_numeric_extraction": is_safe_for_numeric_extraction(citation),
                "license": ntrs.extract_license_fields(citation),
            },
        }
        (sources_dir / f"ntrs-src__{citation_id}.json").write_text(json.dumps(source, indent=2))
        source_count += 1

    redistributions = ntrs.get_redistributions(since)

    manifest = {
        "provider": "ntrs",
        "version": "0.2.2",
        "record_counts": {"materials": 0, "sources": source_count},
        "synced_since": since,
        "redistributions_checked": len(
            redistributions.get("results") or redistributions.get("citations") or []
        ),
        "license_notes": [
            "Use citation URLs by default.",
            "Redistribution review required for full text.",
        ],
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest
