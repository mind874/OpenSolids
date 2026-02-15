from __future__ import annotations

import json
from pathlib import Path

import requests

from .mapper import material_record_from_parsed
from .parser import parse_material_links, parse_material_page

INDEX_URL = "https://trc.nist.gov/cryogenics/materials/materialproperties.htm"


def sync_nist_cryo(output_dir: Path, *, max_materials: int | None = None, timeout: int = 30) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    materials_dir = output_dir / "materials"
    sources_dir = output_dir / "sources"
    materials_dir.mkdir(exist_ok=True)
    sources_dir.mkdir(exist_ok=True)

    with requests.Session() as session:
        session.headers.update(
            {
                "User-Agent": "OpenSolids/0.2 (+https://github.com/mind874/OpenSolids)",
                "Accept": "text/html,application/xhtml+xml",
            }
        )
        index_res = session.get(INDEX_URL, timeout=timeout)
        index_res.raise_for_status()
        links = parse_material_links(index_res.text, INDEX_URL)

        if max_materials is not None:
            links = links[:max_materials]

        material_count = 0
        source_count = 0
        errors: list[dict[str, str]] = []

        for link in links:
            try:
                page_res = session.get(link, timeout=timeout)
                page_res.raise_for_status()
                parsed = parse_material_page(page_res.text, link)
                if not parsed.get("properties"):
                    errors.append({"url": link, "error": "no_supported_properties"})
                    continue

                material, source = material_record_from_parsed(parsed)
                (materials_dir / f"{material['id'].replace(':', '__')}.json").write_text(
                    json.dumps(material, indent=2)
                )
                (sources_dir / f"{source['source_id'].replace(':', '__')}.json").write_text(
                    json.dumps(source, indent=2)
                )
                material_count += 1
                source_count += 1
            except Exception as exc:  # pragma: no cover - network/errors vary
                errors.append({"url": link, "error": str(exc)})

    manifest = {
        "provider": "nist-cryo",
        "version": "0.2.2",
        "record_counts": {"materials": material_count, "sources": source_count},
        "license_notes": [
            "NIST attribution required.",
            "NIST fair use/license statement applies.",
        ],
        "errors": errors,
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest
