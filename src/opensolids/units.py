from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pint

UREG = pint.UnitRegistry(autoconvert_offset_to_baseunit=True)


CANONICAL_UNITS: dict[str, str] = {
    "k": "W/(m*K)",
    "cp": "J/(kg*K)",
    "rho": "kg/m^3",
    "E": "Pa",
    "nu": "1",
    "alpha": "1/K",
    "eps_th": "1",
    "sigma_y": "Pa",
    "sigma_uts": "Pa",
}


def as_array_with_scalar_flag(value: float | Iterable[float]) -> tuple[np.ndarray, bool]:
    arr = np.asarray(value, dtype=float)
    return (arr.reshape(1), True) if arr.ndim == 0 else (arr, False)


def restore_scalar_if_needed(value: np.ndarray, was_scalar: bool):
    if was_scalar:
        return float(value.reshape(-1)[0])
    return value


def convert_values(values, from_units: str, to_units: str | None):
    if to_units is None or to_units == from_units:
        return values

    arr, was_scalar = as_array_with_scalar_flag(values)

    if from_units in {"", "1", "dimensionless"}:
        q = arr * UREG.dimensionless
    else:
        q = arr * UREG(from_units)

    converted = q.to(to_units).magnitude
    return restore_scalar_if_needed(np.asarray(converted, dtype=float), was_scalar)
