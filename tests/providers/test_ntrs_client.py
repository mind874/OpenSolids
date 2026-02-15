from opensolids.providers.ntrs_openapi.client import NTRSOpenAPIClient
from opensolids.providers.ntrs_openapi.compliance import is_safe_for_numeric_extraction


class FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class FakeSession:
    def request(self, method, url, timeout=30, **kwargs):
        if url.endswith("/citations/123"):
            return FakeResponse(
                {
                    "id": "123",
                    "title": "Test citation",
                    "containsThirdPartyMaterial": False,
                    "copyright": {
                        "determinationType": "PUBLIC_USE_PERMITTED",
                        "owner": "NASA",
                    },
                }
            )
        if url.endswith("/citations/redistributions"):
            return FakeResponse({"results": [{"id": "123", "disseminated": "NONE"}]})
        return FakeResponse({"results": []})



def test_ntrs_client_and_compliance_fields():
    client = NTRSOpenAPIClient(session=FakeSession())
    citation = client.get_citation("123")

    fields = client.extract_license_fields(citation)
    assert fields["determinationType"] == "PUBLIC_USE_PERMITTED"
    assert fields["containsThirdPartyMaterial"] is False

    assert is_safe_for_numeric_extraction(citation)
