import opensolids as osl


def test_search_with_required_properties_filters_results():
    hits = osl.search("", required_properties=["k", "sigma_y"])
    ids = {h.id for h in hits}

    assert "ntrs:20160001501:cucrzr" in ids
    assert "ntrs:20070017311:grcop-84" in ids
    assert "nist-cryo:aluminum-6061-t6" not in ids
    assert "mil-hdbk-5:H:al-6061-t6" not in ids


def test_search_with_empty_required_properties_matches_default():
    base = osl.search("6061")
    filtered = osl.search("6061", required_properties=[])
    assert [h.id for h in filtered] == [h.id for h in base]
