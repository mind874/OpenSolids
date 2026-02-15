"""Search and provenance inspection."""

import opensolids as osl


def main() -> None:
    print("Providers:", osl.list_providers())
    print()

    query = "in718"
    hits = osl.search(query)
    print(f"Search hits for {query!r}:")
    for hit in hits:
        print(
            f"- {hit.id} | {hit.name} | provider={hit.provider} | "
            f"properties={','.join(hit.property_coverage)}"
        )
    print()

    mat = osl.material("cucrzr")
    print(f"Provenance for {mat.id}:")
    for src in mat.sources:
        print(f"source_id       : {src.source_id}")
        print(f"title           : {src.title}")
        print(f"url/citation    : {src.url_or_citation_id}")
        print(f"extraction      : {src.extraction_method}")
        print(f"license notes   : {src.license_notes}")
        print()

    print("Provider records remain available when needed:")
    for hit in osl.search("cucrzr", include_provider_records=True):
        if ":" in hit.id:
            print(f"- {hit.id}")


if __name__ == "__main__":
    main()
