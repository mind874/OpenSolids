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


def _origin_from_source(source) -> str:
    if source is None:
        return "n/a"
    metadata = source.metadata or {}
    origin = metadata.get("data_origin")
    if origin:
        return str(origin)
    return source.extraction_method


def _derived_diffusivity_details(mat) -> tuple[str, str, str, str, str, float, float]:
    component_keys = ["k", "cp"]
    component_curves = [mat.curve("k"), mat.curve("cp")]
    source_parts: list[str] = []
    origins: list[str] = []
    citations: list[str] = []

    for key, curve in zip(component_keys, component_curves):
        source = curve.source_ref
        if source:
            source_parts.append(f"{key}:{source.source_id}")
            origins.append(_origin_from_source(source))
            citations.append(source.url_or_citation_id)

    if "rho" in set(mat.available_properties()):
        curve = mat.curve("rho")
        component_curves.append(curve)
        source = curve.source_ref
        if source:
            source_parts.append(f"rho:{source.source_id}")
            origins.append(_origin_from_source(source))
            citations.append(source.url_or_citation_id)
    elif mat.density_ref is not None:
        source_parts.append(f"rho:density_ref={mat.density_ref:.1f} kg/m^3")
        origins.append("assumed-constant")

    valid_t_min = max(curve.valid_T_min for curve in component_curves)
    valid_t_max = min(curve.valid_T_max for curve in component_curves)

    source_text = " | ".join(source_parts) if source_parts else "derived"
    origin_text = " | ".join(dict.fromkeys(origins)) if origins else "derived"
    citation_text = "<br>".join(dict.fromkeys(citations)) if citations else "derived"
    range_text = f"[{valid_t_min:.6g}, {valid_t_max:.6g}]"
    return "m^2/s", range_text, source_text, origin_text, citation_text, valid_t_min, valid_t_max


def _temperature_dependent(valid_t_min: float, valid_t_max: float) -> str:
    return "yes" if (valid_t_max - valid_t_min) > 1e-12 else "no"


def _curve_metadata_summary(curve) -> str:
    metadata = curve.metadata or {}
    if not metadata:
        return "-"
    hidden_keys = {"selection_rank", "source_material_id", "source_provider"}
    visible = {k: v for k, v in metadata.items() if k not in hidden_keys}
    if not visible:
        return "-"
    parts = [f"{k}={v}" for k, v in sorted(visible.items())]
    return "; ".join(parts)


def _source_lines() -> list[str]:
    lines = [
        "# Material Sources",
        "",
        "This table shows where each canonical property curve comes from, including units,",
        "valid temperature range, and whether data is modeled/computed or experimentally derived.",
        "",
        "Column notes:",
        "",
        "- `valid_T_range_K`: inclusive source-supported interval `[valid_T_min, valid_T_max]` in Kelvin.",
        "- `temperature_dependent`: `yes` if `valid_T_max > valid_T_min`; `no` for single-temperature anchors.",
        "- `data_origin`: uses `source.metadata.data_origin` when present; otherwise `source.extraction_method`.",
        "- `curve_metadata`: property-specific metadata (for example yield definition, process, heat treatment).",
        "",
        "| canonical_id | property | units | valid_T_range_K | temperature_dependent | source_id / derivation | data_origin | curve_metadata | citation_or_url |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    for material_id in osl.list_material_ids():
        mat = osl.material(material_id)
        props = mat.available_properties()
        if not props:
            lines.append(f"| `{mat.id}` | `-` | `-` | `-` | no bundled curves yet | `n/a` | n/a |")
            continue

        for property_key in props:
            try:
                curve = mat.curve(property_key)
            except KeyError:
                if property_key == "diffusivity":
                    units, valid_range, source_text, origin_text, citation_text, tmin, tmax = (
                        _derived_diffusivity_details(mat)
                    )
                    temp_dep = _temperature_dependent(tmin, tmax)
                else:
                    units, valid_range, source_text, origin_text, citation_text = (
                        "-",
                        "-",
                        "derived",
                        "derived",
                        "derived",
                    )
                    temp_dep = "n/a"
                lines.append(
                    f"| `{mat.id}` | `{property_key}` | `{units}` | `{valid_range}` | "
                    f"`{temp_dep}` | `{source_text}` | `{origin_text}` | `-` | {citation_text} |"
                )
                continue

            source = curve.source_ref
            source_id = source.source_id if source else "n/a"
            origin = _origin_from_source(source)
            citation = source.url_or_citation_id if source else "n/a"
            valid_range = f"[{curve.valid_T_min:.6g}, {curve.valid_T_max:.6g}]"
            temp_dep = _temperature_dependent(curve.valid_T_min, curve.valid_T_max)
            curve_meta = _curve_metadata_summary(curve)
            lines.append(
                f"| `{mat.id}` | `{property_key}` | `{curve.units}` | `{valid_range}` | "
                f"`{temp_dep}` | `{source_id}` | `{origin}` | `{curve_meta}` | {citation} |"
            )

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
