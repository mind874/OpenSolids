"""Audit focused materials and print per-property SI values with source IDs."""

from __future__ import annotations

import opensolids as osl
from opensolids.units import CANONICAL_UNITS

TEMPERATURE_K = 293.15
MATERIAL_IDS = ("c101", "c110", "alsi10mg-am")


def _value_at_temperature_si(mat, property_key: str, temperature_k: float) -> tuple[float, str]:
    units = CANONICAL_UNITS.get(property_key, "")
    value = float(getattr(mat, property_key)(temperature_k, units=units))
    return value, units


def _property_range_and_source(mat, property_key: str) -> tuple[float, float, str]:
    if property_key != "diffusivity":
        curve = mat.curve(property_key)
        source_id = curve.source_ref.source_id if curve.source_ref else "n/a"
        return curve.valid_T_min, curve.valid_T_max, source_id

    try:
        curve = mat.curve("diffusivity")
        source_id = curve.source_ref.source_id if curve.source_ref else "n/a"
        return curve.valid_T_min, curve.valid_T_max, source_id
    except KeyError:
        component_curves = [mat.curve("k"), mat.curve("cp")]
        if "rho" in mat.available_properties():
            component_curves.append(mat.curve("rho"))

        valid_t_min = max(curve.valid_T_min for curve in component_curves)
        valid_t_max = min(curve.valid_T_max for curve in component_curves)
        return valid_t_min, valid_t_max, "derived"


def _format_float(value: float) -> str:
    return f"{value:.6g}"


def _print_table(headers: list[str], rows: list[list[str]]) -> None:
    widths = [len(header) for header in headers]
    for row in rows:
        for idx, cell in enumerate(row):
            widths[idx] = max(widths[idx], len(cell))

    header_line = " | ".join(header.ljust(widths[idx]) for idx, header in enumerate(headers))
    separator_line = "-+-".join("-" * width for width in widths)
    print(header_line)
    print(separator_line)
    for row in rows:
        print(" | ".join(cell.ljust(widths[idx]) for idx, cell in enumerate(row)))


def main() -> None:
    headers = [
        "material",
        "property",
        "value_at_293.15K_SI",
        "value_units",
        "valid_T_range_K",
        "source_id",
    ]
    rows: list[list[str]] = []

    for material_id in MATERIAL_IDS:
        mat = osl.material(material_id)
        for property_key in mat.available_properties():
            value, units = _value_at_temperature_si(mat, property_key, TEMPERATURE_K)
            valid_t_min, valid_t_max, source_id = _property_range_and_source(mat, property_key)
            rows.append(
                [
                    mat.id,
                    property_key,
                    _format_float(value),
                    units,
                    f"[{_format_float(valid_t_min)}, {_format_float(valid_t_max)}]",
                    source_id,
                ]
            )

    _print_table(headers, rows)


if __name__ == "__main__":
    main()
