import numpy as np

import opensolids as osl


def test_material_lookup_and_property_calls():
    mat = osl.material("al-6061-t6")
    k = mat.k(300.0)
    assert isinstance(k, float)
    assert k > 0

    E = mat.E([77.0, 293.15])
    assert isinstance(E, np.ndarray)
    assert E.shape == (2,)


def test_eps_th_reference_shift_behavior():
    mat = osl.material("al-6061-t6")

    eps_default = mat.eps_th(120.0)
    eps_shifted = mat.eps_th(120.0, T_ref=150.0)

    assert eps_default != eps_shifted


def test_unit_conversion_strength_to_mpa():
    mat = osl.material("in718-am")
    sy_pa = mat.sigma_y(293.15)
    sy_mpa = mat.sigma_y(293.15, units="MPa")

    assert sy_pa > sy_mpa
    assert sy_mpa > 100.0


def test_diffusivity_is_available_when_density_ref_is_set():
    mat = osl.material("al-6061-t6")

    diffusivity = mat.diffusivity(293.15)
    assert isinstance(diffusivity, float)
    assert 4e-5 < diffusivity < 8e-5

    diffusivity_mm2_s = mat.diffusivity(293.15, units="mm^2/s")
    assert 40.0 < diffusivity_mm2_s < 80.0


def test_canonical_alias_lookup():
    mat = osl.material("6061-t6")
    assert mat.id == "al-6061-t6"
    assert "k" in mat.available_properties()
    assert "sigma_y" in mat.available_properties()


def test_list_providers_and_search():
    providers = osl.list_providers()
    assert "curated-public" in providers
    assert "nist-cryo" in providers
    assert "ntrs" in providers
    assert "mil-hdbk-5" in providers

    results = osl.search("cucrzr")
    ids = {r.id for r in results}
    assert "cucrzr-am" in ids

    provider_results = osl.search("cucrzr", include_provider_records=True)
    provider_ids = {r.id for r in provider_results}
    assert "ntrs:20210010991:cucrzr" in provider_ids
