from opensolids.providers.ntrs_openapi.compliance import apply_redistributions



def test_apply_redistributions_marks_records_inactive():
    records = [
        {
            "id": "ntrs:123:foo",
            "active": True,
            "notes": "",
        }
    ]
    payload = {"results": [{"id": "123", "disseminated": "NONE"}]}
    changed = apply_redistributions(records, payload)

    assert changed == ["ntrs:123:foo"]
    assert records[0]["active"] is False
