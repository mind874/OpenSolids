"""Export all packaged provider materials to materials/material_catalog.csv."""

from __future__ import annotations

import csv
from pathlib import Path

import opensolids as osl
from opensolids.registry import default_registry


def _write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def main() -> None:
    reg = default_registry()
    rows: list[list[str]] = []

    for provider_name in reg.list_providers():
        provider = reg.providers[provider_name]
        for material_id in provider.list_material_ids():
            mat = osl.material(material_id)
            rows.append(
                [
                    provider_name,
                    mat.id,
                    mat.name,
                    mat.condition or "",
                    ",".join(mat.available_properties()),
                    ",".join(mat.aliases),
                ]
            )

    rows.sort(key=lambda r: (r[0], r[2], r[1]))

    out = Path("materials/material_catalog.csv")
    _write_csv(
        out,
        ["provider", "material_id", "name", "condition", "properties", "aliases"],
        rows,
    )

    print(f"Wrote {len(rows)} materials to {out}")


if __name__ == "__main__":
    main()
