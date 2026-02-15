import numpy as np

import opensolids as osl


def test_material_lookup_and_property_calls():
    mat = osl.material("nist-cryo:aluminum-6061-t6")
    k = mat.k(300.0)
    assert isinstance(k, float)
    assert k > 0

    E = mat.E([77.0, 293.15])
    assert isinstance(E, np.ndarray)
    assert E.shape == (2,)


def test_eps_th_reference_shift_behavior():
    mat = osl.material("nist-cryo:aluminum-6061-t6")

    eps_default = mat.eps_th(120.0)
    eps_shifted = mat.eps_th(120.0, T_ref=150.0)

    assert eps_default != eps_shifted


def test_unit_conversion_strength_to_mpa():
    mat = osl.material("ntrs:20160001501:cucrzr")
    sy_pa = mat.sigma_y(293.15)
    sy_mpa = mat.sigma_y(293.15, units="MPa")

    assert sy_pa > sy_mpa
    assert sy_mpa > 100.0


def test_list_providers_and_search():
    providers = osl.list_providers()
    assert "nist-cryo" in providers
    assert "ntrs" in providers
    assert "mil-hdbk-5" in providers

    results = osl.search("cucrzr")
    ids = {r.id for r in results}
    assert "ntrs:20160001501:cucrzr" in ids
