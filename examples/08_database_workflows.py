"""How to choose and use different OpenSolids databases/providers."""

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
    print("Providers:", osl.list_providers())
    print()

    print("Use case 1: cryogenic thermal properties (NIST)")
    nist_id = "nist-cryo:aluminum-6061-t6"
    nist = osl.material(nist_id)
    print(f"{nist_id} k(T) at [20, 77, 293.15] K:")
    print(nist.k([20.0, 77.0, 293.15]))
    print(f"{nist_id} E(T) at [77, 293.15] K in GPa:")
    print(nist.E([77.0, 293.15], units="GPa"))
    print()

    print("Use case 2: high-temp chamber-liner style properties (NTRS)")
    ntrs_id = "ntrs:20160001501:cucrzr"
    ntrs = osl.material(ntrs_id)
    print(f"{ntrs_id} k(T) at [500, 700, 900] K:")
    print(ntrs.k([500.0, 700.0, 900.0]))
    print(f"{ntrs_id} sigma_y(T) at [500, 700, 900] K in MPa:")
    print(ntrs.sigma_y([500.0, 700.0, 900.0], units="MPa"))
    print()

    print("Use case 3: handbook allowables style strength curves (MIL-HDBK-5)")
    mil_id = "mil-hdbk-5:H:inconel-718"
    mil = osl.material(mil_id)
    print(f"{mil_id} sigma_y(T) at [294, 700, 1000] K in MPa:")
    print(mil.sigma_y([294.0, 700.0, 1000.0], units="MPa"))
    print()

    print("Combining databases for a single design workflow (6061):")
    nist_6061 = osl.material("nist-cryo:aluminum-6061-t6")
    mil_6061 = osl.material("mil-hdbk-5:H:al-6061-t6")

    t_design = 295.0
    k_val = nist_6061.k(t_design, policy="clamp")
    sy_val = mil_6061.sigma_y(t_design, units="MPa", policy="clamp")
    print(f"At T={t_design} K -> k from NIST: {k_val:.3f} W/(m*K)")
    print(f"At T={t_design} K -> sigma_y from MIL: {sy_val:.3f} MPa")
    print()

    _print_sources(nist_id)
    _print_sources(ntrs_id)
    _print_sources(mil_id)


if __name__ == "__main__":
    main()
