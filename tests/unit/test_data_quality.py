import json
from pathlib import Path

import opensolids as osl
from opensolids.units import CANONICAL_UNITS, UREG


def test_all_material_curve_units_convert_to_canonical_si():
    base_dirs = [
        Path("packages/opensolids_data_curated_public/src/opensolids_data_curated_public/materials"),
        Path("packages/opensolids_data_nist_cryo/src/opensolids_data_nist_cryo/materials"),
        Path("packages/opensolids_data_ntrs_public/src/opensolids_data_ntrs_public/materials"),
        Path("packages/opensolids_data_mil_hdbk_5/src/opensolids_data_mil_hdbk_5/materials"),
    ]

    for base in base_dirs:
        for fp in sorted(base.glob("*.json")):
            rec = json.loads(fp.read_text())
            for key, curve in rec["properties"].items():
                units = curve["units"]
                canonical = CANONICAL_UNITS[key]

                if canonical == "1":
                    assert units in {"", "1", "dimensionless"}
                else:
                    (1 * UREG(units)).to(canonical)


def test_nist_6061_reference_points_are_reasonable():
    mat = osl.material("nist-cryo:aluminum-6061-t6")

    assert 130.0 < mat.k(293.15) < 180.0
    assert 700.0 < mat.cp(293.15) < 1100.0
    assert 55.0 < mat.E(293.15, units="GPa") < 80.0

    eps_20 = mat.eps_th(20.0)
    eps_293 = mat.eps_th(293.15)
    assert -0.01 < eps_20 < -0.001
    assert abs(eps_293) < 5e-4


def test_nist_304_reference_points_are_reasonable():
    mat = osl.material("nist-cryo:stainless-steel-304")

    assert 10.0 < mat.k(293.15) < 25.0
    assert 350.0 < mat.cp(293.15) < 700.0
    assert 150.0 < mat.E(293.15, units="GPa") < 230.0


def test_nist_316_reference_points_are_reasonable():
    mat = osl.material("nist-cryo:stainless-steel-316")

    assert 10.0 < mat.k(293.15) < 30.0
    assert 350.0 < mat.cp(293.15) < 700.0
    assert 150.0 < mat.E(293.15, units="GPa") < 230.0


def test_nist_in718_reference_points_are_reasonable():
    mat = osl.material("nist-cryo:inconel-718")
    assert 5.0 < mat.k(293.15) < 20.0
    assert abs(mat.eps_th(293.15)) < 5e-4


def test_nist_ofhc_specific_heat_reference_point_is_reasonable():
    mat = osl.material("nist-cryo:oxygen-free-copper")
    assert 300.0 < mat.cp(293.15) < 500.0


def test_nist_316_low_temperature_specific_heat_is_physical():
    mat = osl.material("nist-cryo:stainless-steel-316")
    cp_49_9 = mat.cp(49.9)
    cp_50_0 = mat.cp(50.0)
    assert cp_49_9 > 10.0
    assert abs(cp_49_9 - cp_50_0) < 25.0


def test_nist_in718_source_url_uses_live_path():
    source_file = Path(
        "packages/opensolids_data_nist_cryo/src/opensolids_data_nist_cryo/sources/nist_in718.json"
    )
    payload = json.loads(source_file.read_text())
    assert "Iconel%20718" in payload["url_or_citation_id"]
