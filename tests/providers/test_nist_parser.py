from pathlib import Path

from opensolids.providers.nist_cryo.parser import parse_material_links, parse_material_page



def test_parse_nist_material_page_extracts_coefficients_and_ranges_from_synthetic_fixture():
    html = Path("tests/fixtures/nist_6061_fixture.html").read_text()
    parsed = parse_material_page(html, "https://example.test/6061")

    assert "6061" in parsed["name"].lower()
    assert "k" in parsed["properties"]

    k_prop = parsed["properties"]["k"]
    assert k_prop["model"]["type"] == "log_polynomial"
    assert k_prop["model"]["coefficients"] == [1.22, 0.09, -0.02]
    assert k_prop["valid_T_min"] == 4.0
    assert k_prop["valid_T_max"] == 300.0



def test_parse_nist_live_index_links():
    html = Path("tests/fixtures/nist_index_live.html").read_text()
    links = parse_material_links(
        html,
        "https://trc.nist.gov/cryogenics/materials/materialproperties.htm",
    )

    assert len(links) > 30
    assert any("6061" in link for link in links)
    assert any("304stainless" in link.lower() for link in links)



def test_parse_nist_live_6061_page_table_layout():
    html = Path("tests/fixtures/nist_6061_live.html").read_text()
    parsed = parse_material_page(
        html,
        "https://trc.nist.gov/cryogenics/materials/6061%20Aluminum/6061_T6Aluminum_rev.htm",
    )

    assert "6061" in parsed["name"].lower()
    props = parsed["properties"]
    assert {"k", "cp", "E", "eps_th"}.issubset(props.keys())

    assert props["k"]["model"]["type"] == "log_polynomial"
    assert props["cp"]["model"]["type"] == "log_polynomial"
    assert props["E"]["model"]["type"] == "polynomial"
    assert props["E"]["units"] == "Pa"
    assert props["eps_th"]["model"]["type"] == "piecewise"
    assert props["eps_th"]["units"] == "1"
    assert props["k"]["model"]["coefficients"][0] == 0.07918
    assert props["cp"]["model"]["coefficients"][0] == 46.6467
    assert props["eps_th"]["model"]["branches"][0]["model"]["y"][0] == -0.0041545
    assert props["k"]["valid_T_min"] == 1.0
    assert props["k"]["valid_T_max"] == 300.0



def test_parse_nist_live_304_page_table_layout():
    html = Path("tests/fixtures/nist_304_live.html").read_text()
    parsed = parse_material_page(
        html,
        "https://trc.nist.gov/cryogenics/materials/304Stainless/304Stainless_rev.htm",
    )

    props = parsed["properties"]
    assert {"k", "cp", "E", "eps_th"}.issubset(props.keys())
    assert props["k"]["model"]["type"] == "log_polynomial"
    assert props["eps_th"]["model"]["type"] in {"piecewise", "polynomial"}
    assert props["E"]["units"] == "Pa"
    assert props["E"]["model"]["coefficients"][0] == 210059300000.0
