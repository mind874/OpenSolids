import opensolids as osl


def test_search_with_required_properties_filters_results():
    hits = osl.search("", required_properties=["k", "sigma_y"])
    ids = {h.id for h in hits}

    assert "grcop-84-am" in ids
    assert "al-6061-t6" in ids
    assert "ss304" in ids
    assert "ss316" in ids
    assert "cucrzr-am" not in ids


def test_search_with_empty_required_properties_matches_default():
    base = osl.search("6061")
    filtered = osl.search("6061", required_properties=[])
    assert [h.id for h in filtered] == [h.id for h in base]
