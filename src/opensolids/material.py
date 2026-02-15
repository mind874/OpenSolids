from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .curve import PropertyCurve, curve_from_record
from .types import SourceRef
from .units import convert_values


@dataclass
class Material:
    id: str
    name: str
    aliases: list[str]
    composition: str | None
    condition: str | None
    notes: str | None
    sources: list[SourceRef]
    _properties: dict
    _source_lookup: dict[str, SourceRef]
    _curve_cache: dict[str, PropertyCurve]

    @classmethod
    def from_record(cls, record: dict, source_lookup: dict[str, SourceRef]) -> "Material":
        source_ids = record.get("sources", [])
        material_sources = [source_lookup[sid] for sid in source_ids if sid in source_lookup]
        return cls(
            id=record["id"],
            name=record["name"],
            aliases=list(record.get("aliases", [])),
            composition=record.get("composition"),
            condition=record.get("condition"),
            notes=record.get("notes"),
            sources=material_sources,
            _properties=record.get("properties", {}),
            _source_lookup=source_lookup,
            _curve_cache={},
        )

    def available_properties(self) -> list[str]:
        return sorted(self._properties.keys())

    def curve(self, property_key: str) -> PropertyCurve:
        if property_key in self._curve_cache:
            return self._curve_cache[property_key]
        if property_key not in self._properties:
            raise KeyError(f"Property not available for {self.id}: {property_key}")

        curve = curve_from_record(property_key, self._properties[property_key], self._source_lookup)
        self._curve_cache[property_key] = curve
        return curve

    def _eval(self, property_key: str, T, *, units: str | None = None, policy: str | None = None):
        curve = self.curve(property_key)
        values = curve(T, policy=policy)
        return convert_values(values, curve.units, units)

    def k(self, T, *, units: str | None = None, policy: str | None = None):
        return self._eval("k", T, units=units, policy=policy)

    def cp(self, T, *, units: str | None = None, policy: str | None = None):
        return self._eval("cp", T, units=units, policy=policy)

    def rho(self, T, *, units: str | None = None, policy: str | None = None):
        return self._eval("rho", T, units=units, policy=policy)

    def E(self, T, *, units: str | None = None, policy: str | None = None):
        return self._eval("E", T, units=units, policy=policy)

    def nu(self, T, *, units: str | None = None, policy: str | None = None):
        return self._eval("nu", T, units=units, policy=policy)

    def alpha(self, T, *, units: str | None = None, policy: str | None = None):
        return self._eval("alpha", T, units=units, policy=policy)

    def sigma_y(self, T, *, units: str | None = None, policy: str | None = None):
        return self._eval("sigma_y", T, units=units, policy=policy)

    def sigma_uts(self, T, *, units: str | None = None, policy: str | None = None):
        return self._eval("sigma_uts", T, units=units, policy=policy)

    def eps_th(
        self,
        T,
        *,
        T_ref: float = 293.15,
        units: str | None = None,
        policy: str | None = None,
    ):
        if "eps_th" in self._properties:
            curve = self.curve("eps_th")
            values = curve(T, policy=policy)

            if curve.reference_temperature is not None and abs(curve.reference_temperature - T_ref) > 1e-9:
                ref_value = curve(T_ref, policy=policy)
                values = np.asarray(values, dtype=float) - float(ref_value)

            return convert_values(values, curve.units, units)

        if "alpha" not in self._properties:
            raise KeyError(f"Property not available for {self.id}: eps_th (and alpha missing)")

        curve = self.curve("alpha")
        arr = np.asarray(T, dtype=float)
        was_scalar = arr.ndim == 0
        arr = arr.reshape(1) if was_scalar else arr

        out = np.zeros_like(arr, dtype=float)
        for i, t_i in enumerate(arr):
            n_points = 64
            grid = np.linspace(T_ref, t_i, n_points)
            alpha_values = np.asarray(curve(grid, policy=policy), dtype=float)
            out[i] = np.trapz(alpha_values, grid)

        values = float(out[0]) if was_scalar else out
        return convert_values(values, "1", units)
