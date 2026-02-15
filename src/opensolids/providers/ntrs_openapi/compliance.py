from __future__ import annotations

from typing import Any

SAFE_DETERMINATION_TYPES = {
    "PUBLIC_USE_PERMITTED",
    "GOV_PUBLIC_USE_PERMITTED",
}



def is_safe_for_numeric_extraction(citation: dict[str, Any]) -> bool:
    copyright_obj = citation.get("copyright") or {}
    determination_type = (copyright_obj.get("determinationType") or "").upper()
    third_party = citation.get("containsThirdPartyMaterial")

    return determination_type in SAFE_DETERMINATION_TYPES and third_party in {False, None}



def apply_redistributions(
    material_records: list[dict[str, Any]],
    redistribution_payload: dict[str, Any],
) -> list[str]:
    updated_ids: list[str] = []
    redistributions = redistribution_payload.get("results") or redistribution_payload.get("citations") or []

    by_citation = {}
    for red in redistributions:
        citation_id = str(red.get("id") or red.get("citationId") or "")
        if citation_id:
            by_citation[citation_id] = red

    for material in material_records:
        mid = material.get("id", "")
        if not mid.startswith("ntrs:"):
            continue
        parts = mid.split(":")
        if len(parts) < 3:
            continue
        citation_id = parts[1]

        red = by_citation.get(citation_id)
        if not red:
            continue

        dissemination = str(red.get("disseminated") or red.get("distribution") or "").upper()
        if dissemination == "NONE":
            material["active"] = False
            material["notes"] = (material.get("notes", "") + " [Inactive due to redistribution]").strip()
            updated_ids.append(mid)

    return updated_ids
