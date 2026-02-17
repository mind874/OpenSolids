from __future__ import annotations

from typing import Any

from .units import CANONICAL_UNITS, UREG

REQUIRED_MATERIAL_FIELDS = {
    "id",
    "name",
    "aliases",
    "sources",
    "properties",
}

REQUIRED_CURVE_FIELDS = {
    "units",
    "valid_T_min",
    "valid_T_max",
    "model",
}


def _validate_units(units: str) -> None:
    if units in {"", "1", "dimensionless"}:
        return
    UREG(units)


def validate_curve_record(curve: dict[str, Any], *, property_key: str | None = None) -> None:
    missing = REQUIRED_CURVE_FIELDS.difference(curve.keys())
    if missing:
        raise ValueError(f"Curve missing required fields: {sorted(missing)}")

    units = curve["units"]
    _validate_units(units)

    if property_key and property_key in CANONICAL_UNITS:
        canonical_units = CANONICAL_UNITS[property_key]
        if canonical_units == "1":
            if units not in {"", "1", "dimensionless"}:
                raise ValueError(
                    f"Invalid units for dimensionless property '{property_key}': {units}"
                )
        else:
            (1 * UREG(units)).to(canonical_units)

    tmin = float(curve["valid_T_min"])
    tmax = float(curve["valid_T_max"])
    if tmax < tmin:
        raise ValueError(f"Invalid curve temperature range: [{tmin}, {tmax}]")

    model = curve["model"]
    if not isinstance(model, dict) or "type" not in model:
        raise ValueError("Curve model must be a dict containing 'type'")



def validate_material_record(record: dict[str, Any]) -> None:
    missing = REQUIRED_MATERIAL_FIELDS.difference(record.keys())
    if missing:
        raise ValueError(f"Material record missing required fields: {sorted(missing)}")

    if not isinstance(record["aliases"], list):
        raise ValueError("Material aliases must be a list")
    if not isinstance(record["sources"], list):
        raise ValueError("Material sources must be a list")
    if not isinstance(record["properties"], dict):
        raise ValueError("Material properties must be an object/dict")

    for prop_key, curve in record["properties"].items():
        if not isinstance(prop_key, str):
            raise ValueError("Property key must be a string")
        if not isinstance(curve, dict):
            raise ValueError(f"Curve record for {prop_key} must be a dict")
        validate_curve_record(curve, property_key=prop_key)
