"""Search and provenance inspection."""

import opensolids as osl


def main() -> None:
    print("Providers:", osl.list_providers())
    print()

    query = "inconel"
    hits = osl.search(query)
    print(f"Search hits for {query!r}:")
    for hit in hits:
        print(f"- {hit.id} | {hit.name} | provider={hit.provider}")
    print()

    mat = osl.material("ntrs:20160001501:cucrzr")
    print(f"Provenance for {mat.id}:")
    for src in mat.sources:
        print(f"source_id       : {src.source_id}")
        print(f"title           : {src.title}")
        print(f"url/citation    : {src.url_or_citation_id}")
        print(f"extraction      : {src.extraction_method}")
        print(f"license notes   : {src.license_notes}")
        print()


if __name__ == "__main__":
    main()
