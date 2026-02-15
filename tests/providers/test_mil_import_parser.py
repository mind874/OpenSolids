from opensolids.providers.mil_hdbk_5.import_local import parse_two_column_table



def test_parse_two_column_table():
    text = """
    294 276000000
    366 240000000
    422 190000000
    """

    T, y = parse_two_column_table(text)
    assert T == [294.0, 366.0, 422.0]
    assert y == [276000000.0, 240000000.0, 190000000.0]
