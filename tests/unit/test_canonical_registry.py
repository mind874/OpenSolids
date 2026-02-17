import opensolids as osl
import pytest


def test_canonical_material_lookup_by_alias():
    mat = osl.material("al6061")
    assert mat.id == "al-6061-am"
    assert "k" in mat.available_properties()
    assert "sigma_y" in mat.available_properties()


def test_search_defaults_to_canonical_results():
    hits = osl.search("cucrzr")
    ids = {hit.id for hit in hits}
    assert "cucrzr-am" in ids
    assert "ntrs:20210010991:cucrzr" not in ids


def test_list_material_ids_returns_canonical_only_by_default():
    ids = set(osl.list_material_ids())
    assert "al-6061-t6" in ids
    assert "cucrzr-am" in ids
    assert "ntrs:20210010991:cucrzr" not in ids


def test_c110_has_room_temperature_curves():
    mat = osl.material("c110")
    assert mat.id == "c110"
    props = set(mat.available_properties())
    assert {"k", "cp", "rho", "E", "sigma_y", "sigma_uts", "diffusivity"}.issubset(props)


def test_ss316_has_stitched_conductivity_and_strength_curves():
    mat = osl.material("ss316")
    props = set(mat.available_properties())
    assert {"k", "cp", "E", "eps_th", "diffusivity", "sigma_y", "sigma_uts"}.issubset(props)
    assert mat.curve("k").valid_T_max >= 873.15
    assert mat.sigma_y(293.15, units="MPa") >= 180.0


def test_ss304_has_strength_curves_and_extended_conductivity_range():
    mat = osl.material("ss304")
    props = set(mat.available_properties())
    assert {"k", "cp", "E", "eps_th", "diffusivity", "sigma_y", "sigma_uts"}.issubset(props)
    assert mat.curve("k").valid_T_max >= 973.15
    assert mat.sigma_y(293.15, units="MPa") >= 200.0


def test_ss316_am_includes_strength_fallback_curves():
    mat = osl.material("ss316-am")
    props = set(mat.available_properties())
    assert {"k", "cp", "E", "eps_th", "diffusivity", "sigma_y", "sigma_uts"}.issubset(props)
    assert mat.curve("k").valid_T_max >= 873.15


def test_in718_am_includes_nist_thermal_conductivity():
    mat = osl.material("in718-am")
    props = set(mat.available_properties())
    assert "k" in props
    assert "sigma_y" in props


def test_grcop42_am_has_temperature_dependent_k_and_strength():
    mat = osl.material("grcop-42-am")
    props = set(mat.available_properties())
    assert {"k", "sigma_y", "sigma_uts"}.issubset(props)
    assert mat.curve("k").valid_T_max > mat.curve("k").valid_T_min
    assert mat.sigma_y(298.15, units="MPa") > 100.0


def test_cucrzr_am_exposes_thermal_curves_but_not_strength_until_verified_source():
    mat = osl.material("cucrzr-am")
    props = set(mat.available_properties())
    assert {"k", "cp", "diffusivity"}.issubset(props)
    assert "sigma_y" not in props
    with pytest.raises(KeyError):
        mat.sigma_y(293.15)


def test_c101_includes_thermal_and_room_mechanical_properties():
    mat = osl.material("c101")
    props = set(mat.available_properties())
    assert {"k", "cp", "diffusivity", "E", "sigma_y", "sigma_uts"}.issubset(props)


def test_c101_c110_conductivity_reference_values_are_reasonable():
    c101 = osl.material("c101")
    c110 = osl.material("c110")

    assert 300.0 < c101.k(293.15) < 450.0
    assert 300.0 < c110.k(293.15) < 450.0


def test_c101_c110_have_temperature_dependent_thermal_curves():
    c101 = osl.material("c101")
    c110 = osl.material("c110")

    for mat in (c101, c110):
        assert mat.curve("k").valid_T_max - mat.curve("k").valid_T_min > 250.0
        assert mat.curve("cp").valid_T_max - mat.curve("cp").valid_T_min > 250.0
        assert mat.curve("alpha").valid_T_max - mat.curve("alpha").valid_T_min > 250.0


def test_c101_eps_th_derives_from_alpha_without_error():
    c101 = osl.material("c101")
    eps = c101.eps_th(77.0)
    assert isinstance(eps, float)


def test_c101_c110_diffusivity_has_temperature_coverage():
    for material_id in ("c101", "c110"):
        mat = osl.material(material_id)
        valid_t_min = max(
            mat.curve("k").valid_T_min,
            mat.curve("cp").valid_T_min,
            mat.curve("rho").valid_T_min,
        )
        valid_t_max = min(
            mat.curve("k").valid_T_max,
            mat.curve("cp").valid_T_max,
            mat.curve("rho").valid_T_max,
        )
        assert valid_t_max - valid_t_min >= 250.0


def test_c110_room_temperature_yield_strength_is_not_understated():
    c110 = osl.material("c110")
    sy_mpa = c110.sigma_y(293.15, units="MPa")
    assert 65.0 < sy_mpa < 75.0


def test_alsi10mg_am_has_complete_core_properties():
    mat = osl.material("alsi10mg-am")
    props = set(mat.available_properties())
    assert {"k", "cp", "rho", "diffusivity", "E", "sigma_y", "sigma_uts"}.issubset(props)
    assert 100.0 < mat.k(293.15) < 200.0
    assert 500.0 < mat.cp(293.15) < 1100.0
