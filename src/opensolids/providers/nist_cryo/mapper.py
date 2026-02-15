from __future__ import annotations

import re
from datetime import datetime, timezone
from urllib.parse import urlparse


def _slugify(name: str) -> str:
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = re.sub(r"-+", "-", slug).strip("-")
    return slug


def material_record_from_parsed(parsed: dict) -> tuple[dict, dict]:
    name = parsed["name"]
    slug = _slugify(name)
    material_id = f"nist-cryo:{slug}"
    source_id = f"nist-cryo-src:{slug}"

    properties = {}
    for key, curve in parsed.get("properties", {}).items():
        properties[key] = {
            **curve,
            "source_id": source_id,
            "reference_temperature": 293.15 if key == "eps_th" else None,
        }

    material = {
        "id": material_id,
        "name": name,
        "aliases": [name],
        "composition": None,
        "condition": None,
        "notes": "Parsed from NIST Cryogenics material page.",
        "sources": [source_id],
        "properties": properties,
    }

    source = {
        "source_id": source_id,
        "title": name,
        "publisher": "NIST",
        "organization": "National Institute of Standards and Technology",
        "url_or_citation_id": parsed["url"],
        "license_notes": "NIST data reused with attribution per NIST fair use/license statement.",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "page_or_table": urlparse(parsed["url"]).path,
        "extraction_method": "fit-parse",
        "metadata": {
            "provider": "nist-cryo",
            "disclaimer": "Engineering use requires independent verification for certification workflows.",
        },
    }

    return material, source
