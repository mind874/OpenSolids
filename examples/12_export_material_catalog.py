"""Export provider and canonical material indexes to the materials/ folder."""

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


def _write_markdown(path: Path, lines: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def _provider_rows() -> list[list[str]]:
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
    return rows


def _canonical_rows() -> list[list[str]]:
    rows: list[list[str]] = []

    for material_id in osl.list_material_ids():
        mat = osl.material(material_id)
        rows.append(
            [
                mat.id,
                mat.name,
                mat.condition or "",
                ",".join(mat.available_properties()),
                ",".join(mat.aliases),
            ]
        )

    rows.sort(key=lambda r: (r[1], r[0]))
    return rows


def _derived_source_text(mat, property_key: str) -> str:
    if property_key != "diffusivity":
        return ""

    source_parts: list[str] = []
    for base_prop in ("k", "cp"):
        try:
            source_ref = mat.curve(base_prop).source_ref
        except KeyError:
            source_ref = None
        if source_ref:
            source_parts.append(f"{base_prop}:{source_ref.source_id}")
    if "rho" in set(mat.available_properties()):
        try:
            source_ref = mat.curve("rho").source_ref
        except KeyError:
            source_ref = None
        if source_ref:
            source_parts.append(f"rho:{source_ref.source_id}")
    elif mat.density_ref is not None:
        source_parts.append(f"rho:density_ref={mat.density_ref:.1f} kg/m^3")
    return " | ".join(source_parts)


def _source_lines() -> list[str]:
    lines = [
        "# Material Sources",
        "",
        "This table shows where each canonical property curve comes from.",
        "",
        "| canonical_id | property | source_id / derivation | citation_or_url |",
        "|---|---|---|---|",
    ]

    for material_id in osl.list_material_ids():
        mat = osl.material(material_id)
        props = mat.available_properties()
        if not props:
            lines.append(f"| `{mat.id}` | `-` | no bundled curves yet | n/a |")
            continue

        for property_key in props:
            try:
                curve = mat.curve(property_key)
            except KeyError:
                lines.append(
                    f"| `{mat.id}` | `{property_key}` | `{_derived_source_text(mat, property_key)}` | derived |"
                )
                continue

            source = curve.source_ref
            source_id = source.source_id if source else "n/a"
            citation = source.url_or_citation_id if source else "n/a"
            lines.append(f"| `{mat.id}` | `{property_key}` | `{source_id}` | {citation} |")

    return lines


def main() -> None:
    provider_out = Path("materials/material_catalog.csv")
    canonical_out = Path("materials/canonical_materials.csv")
    sources_out = Path("materials/material_sources.md")

    provider_rows = _provider_rows()
    canonical_rows = _canonical_rows()

    _write_csv(
        provider_out,
        ["provider", "material_id", "name", "condition", "properties", "aliases"],
        provider_rows,
    )
    _write_csv(
        canonical_out,
        ["material_id", "name", "condition", "properties", "aliases"],
        canonical_rows,
    )
    _write_markdown(sources_out, _source_lines())

    print(f"Wrote {len(provider_rows)} provider materials to {provider_out}")
    print(f"Wrote {len(canonical_rows)} canonical materials to {canonical_out}")
    print(f"Wrote source mapping to {sources_out}")


if __name__ == "__main__":
    main()
