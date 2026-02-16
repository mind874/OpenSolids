import json
from pathlib import Path

import opensolids as osl
import pytest
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


def test_nist_ofhc_alpha_reference_point_is_reasonable():
    mat = osl.material("nist-cryo:oxygen-free-copper")
    assert 1.0e-5 < mat.alpha(293.15) < 2.5e-5


def test_nist_ofhc_rrr_conductivity_variants_are_reasonable():
    k50 = osl.material("nist-cryo:oxygen-free-copper-rrr50").k(293.15)
    k100 = osl.material("nist-cryo:oxygen-free-copper-rrr100").k(293.15)
    assert 350.0 < k50 < 450.0
    assert 350.0 < k100 < 450.0
    assert k100 >= k50


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


def test_cucrzr_provider_record_has_only_thermal_curves_from_ntrs_20210010991():
    rec = osl.material("ntrs:20210010991:cucrzr")
    props = set(rec.available_properties())
    assert props == {"cp", "k"}


def test_cucrzr_canonical_has_no_sigma_y_until_source_backed_curve_exists():
    mat = osl.material("cucrzr-am")
    assert "sigma_y" not in set(mat.available_properties())
    with pytest.raises(KeyError):
        mat.sigma_y(293.15)


def test_alsi10mg_mdpi_source_is_marked_as_model_derived():
    source_file = Path(
        "packages/opensolids_data_curated_public/src/opensolids_data_curated_public/sources/curated_alsi10mg_mdpi_ma2023.json"
    )
    payload = json.loads(source_file.read_text())
    assert payload["metadata"]["data_origin"] == "computed"
    assert payload["metadata"]["modeling_tool"] == "JMatPro"
