"""Practical workflows across bundled databases with canonical material IDs."""

from __future__ import annotations

import opensolids as osl


def _print_sources(mat_id: str) -> None:
    mat = osl.material(mat_id)
    print(f"Sources for {mat_id}:")
    for src in mat.sources:
        print(f"- {src.source_id} | {src.title}")
        print(f"  citation/url: {src.url_or_citation_id}")
        print(f"  extraction  : {src.extraction_method}")
    print()


def main() -> None:
    print("Canonical lookup with no provider prefix:")
    mat = osl.material("al-6061-t6")
    print(f"{mat.id} k(293.15 K): {mat.k(293.15):.3f} W/(m*K)")
    print(f"{mat.id} sigma_y(293.15 K): {mat.sigma_y(293.15, units='MPa'):.3f} MPa")
    print()

    print("AM-focused entries:")
    for material_id in ("alsi10mg-am", "cucrzr-am", "grcop-84-am", "grcop-42-am", "in718-am"):
        am = osl.material(material_id)
        props = ", ".join(am.available_properties())
        print(f"- {material_id}: {props}")
    print()

    print("Provider-specific IDs are still available when needed:")
    nist = osl.material("nist-cryo:aluminum-6061-t6")
    mil = osl.material("mil-hdbk-5:H:al-6061-t6")
    print(f"- NIST k(293.15 K): {nist.k(293.15):.3f} W/(m*K)")
    print(f"- MIL sigma_y(293.15 K): {mil.sigma_y(293.15, units='MPa'):.3f} MPa")
    print()

    _print_sources("al-6061-t6")
    _print_sources("cucrzr-am")


if __name__ == "__main__":
    main()
