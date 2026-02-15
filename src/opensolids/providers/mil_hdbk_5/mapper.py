from __future__ import annotations

from datetime import datetime, timezone



def make_material_record(
    *,
    revision: str,
    material_slug: str,
    material_name: str,
    condition: str,
    property_key: str,
    temperatures: list[float],
    values: list[float],
    units: str,
    basis: str,
    product_form: str | None,
    direction: str | None,
) -> tuple[dict, dict]:
    material_id = f"mil-hdbk-5:{revision}:{material_slug}"
    source_id = f"mil-hdbk-5-src:{revision}:{material_slug}"

    material = {
        "id": material_id,
        "name": material_name,
        "aliases": [material_name],
        "composition": None,
        "condition": condition,
        "notes": "Imported from user-supplied MIL-HDBK-5 table.",
        "sources": [source_id],
        "properties": {
            property_key: {
                "units": units,
                "valid_T_min": min(temperatures),
                "valid_T_max": max(temperatures),
                "recommended_T_min": None,
                "recommended_T_max": None,
                "model": {
                    "type": "tabular",
                    "T": temperatures,
                    "y": values,
                    "interpolation": "linear",
                },
                "source_id": source_id,
            }
        },
    }

    source = {
        "source_id": source_id,
        "title": f"MIL-HDBK-5{revision} material table for {material_name}",
        "publisher": "DoD ASSIST",
        "organization": "Department of Defense",
        "url_or_citation_id": f"MIL-HDBK-5{revision}",
        "license_notes": "Distribution Statement A (public release) must be verified for imported revision.",
        "retrieved_at": datetime.now(timezone.utc).isoformat(),
        "page_or_table": None,
        "extraction_method": "tabular-digitized",
        "metadata": {
            "revision": revision,
            "basis": basis,
            "product_form": product_form,
            "direction": direction,
            "distribution_statement": "A",
        },
    }

    return material, source
