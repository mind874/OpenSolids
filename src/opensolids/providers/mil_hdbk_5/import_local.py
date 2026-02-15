from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

from .mapper import make_material_record



def _extract_text_from_pdf(pdf_path: Path) -> str:
    if shutil.which("pdftotext"):
        proc = subprocess.run(
            ["pdftotext", "-layout", "-f", "1", "-l", "20", str(pdf_path), "-"],
            check=True,
            text=True,
            capture_output=True,
        )
        return proc.stdout
    raise RuntimeError("pdftotext is required for PDF import in this implementation")



def parse_two_column_table(text: str) -> tuple[list[float], list[float]]:
    temperatures: list[float] = []
    values: list[float] = []

    for line in text.splitlines():
        m = re.match(
            r"^\s*([-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?)\s+([-+]?\d*\.?\d+(?:[Ee][-+]?\d+)?)\s*$",
            line,
        )
        if not m:
            continue
        temperatures.append(float(m.group(1)))
        values.append(float(m.group(2)))

    if len(temperatures) < 2:
        raise ValueError("Could not parse at least two table rows from PDF text")

    return temperatures, values



def import_mil_hdbk_5_pdf(
    pdf_path: Path,
    output_dir: Path,
    *,
    revision: str,
    material_slug: str,
    material_name: str,
    condition: str,
    property_key: str,
    units: str,
    basis: str,
    product_form: str | None,
    direction: str | None,
) -> dict:
    output_dir.mkdir(parents=True, exist_ok=True)
    materials_dir = output_dir / "materials"
    sources_dir = output_dir / "sources"
    materials_dir.mkdir(exist_ok=True)
    sources_dir.mkdir(exist_ok=True)

    text = _extract_text_from_pdf(pdf_path)
    temperatures, values = parse_two_column_table(text)

    material, source = make_material_record(
        revision=revision,
        material_slug=material_slug,
        material_name=material_name,
        condition=condition,
        property_key=property_key,
        temperatures=temperatures,
        values=values,
        units=units,
        basis=basis,
        product_form=product_form,
        direction=direction,
    )

    mat_fp = materials_dir / f"{material['id'].replace(':', '__')}.json"
    src_fp = sources_dir / f"{source['source_id'].replace(':', '__')}.json"
    mat_fp.write_text(json.dumps(material, indent=2))
    src_fp.write_text(json.dumps(source, indent=2))

    manifest = {
        "provider": "mil-hdbk-5",
        "version": "0.3.0",
        "record_counts": {"materials": 1, "sources": 1},
        "license_notes": [
            "Imported from local PDF provided by user.",
            "Record revision/date and distribution statement in provenance.",
        ],
    }
    (output_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest
