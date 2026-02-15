"""Verify packaged database units and key sanity reference points."""

from __future__ import annotations

import json
from pathlib import Path

import opensolids as osl
from opensolids.units import CANONICAL_UNITS, UREG

MATERIAL_DIRS = [
    Path("packages/opensolids_data_curated_public/src/opensolids_data_curated_public/materials"),
    Path("packages/opensolids_data_nist_cryo/src/opensolids_data_nist_cryo/materials"),
    Path("packages/opensolids_data_ntrs_public/src/opensolids_data_ntrs_public/materials"),
    Path("packages/opensolids_data_mil_hdbk_5/src/opensolids_data_mil_hdbk_5/materials"),
]


def verify_units() -> tuple[int, int]:
    checked = 0
    failures = 0

    for base in MATERIAL_DIRS:
        for fp in sorted(base.glob("*.json")):
            rec = json.loads(fp.read_text())
            mat_id = rec["id"]
            for key, curve in rec["properties"].items():
                checked += 1
                units = curve["units"]
                canonical = CANONICAL_UNITS[key]

                try:
                    if canonical == "1":
                        if units not in {"", "1", "dimensionless"}:
                            raise ValueError(f"expected dimensionless units, got {units}")
                    else:
                        (1 * UREG(units)).to(canonical)
                except Exception as exc:  # pragma: no cover - diagnostics script
                    failures += 1
                    print(f"[FAIL] {mat_id}::{key} units='{units}' canonical='{canonical}' -> {exc}")

    return checked, failures


def print_reference_points() -> None:
    print("\nReference checkpoints:")

    al = osl.material("al-6061-t6")
    print(f"- 6061-T6 k(293.15 K): {al.k(293.15):.3f} W/(m*K)")
    print(f"- 6061-T6 cp(293.15 K): {al.cp(293.15):.3f} J/(kg*K)")
    print(f"- 6061-T6 E(293.15 K): {al.E(293.15, units='GPa'):.3f} GPa")
    print(f"- 6061-T6 diffusivity(293.15 K): {al.diffusivity(293.15, units='mm^2/s'):.3f} mm^2/s")

    ss = osl.material("ss304")
    print(f"- 304 SS k(293.15 K): {ss.k(293.15):.3f} W/(m*K)")
    print(f"- 304 SS E(293.15 K): {ss.E(293.15, units='GPa'):.3f} GPa")
    print(f"- 304 SS diffusivity(293.15 K): {ss.diffusivity(293.15, units='mm^2/s'):.3f} mm^2/s")

    cu = osl.material("c101")
    print(f"- OFHC cp(293.15 K): {cu.cp(293.15):.3f} J/(kg*K)")


def main() -> None:
    checked, failures = verify_units()
    print(f"Checked {checked} property curves for SI compatibility.")
    if failures:
        print(f"Found {failures} unit incompatibilities.")
    else:
        print("All curve units are SI-compatible (or dimensionless where expected).")

    print_reference_points()


if __name__ == "__main__":
    main()
