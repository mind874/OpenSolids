from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class CanonicalMaterialSpec:
    id: str
    name: str
    aliases: tuple[str, ...]
    composition: str | None
    condition: str | None
    notes: str | None
    density_ref: float | None
    property_sources: dict[str, tuple[str, ...]]


_NORMALIZE_RE = re.compile(r"[^a-z0-9]+")


def normalize_lookup_key(value: str) -> str:
    return " ".join(_NORMALIZE_RE.sub(" ", value.lower()).split())


CANONICAL_MATERIAL_SPECS: tuple[CanonicalMaterialSpec, ...] = (
    CanonicalMaterialSpec(
        id="alsi10mg-am",
        name="AlSi10Mg (AM)",
        aliases=(
            "alsi10mg",
            "alsi10mg am",
            "alsi10mg 3d printed",
            "lpbf alsi10mg",
            "am alsi10mg",
        ),
        composition="Al-Si-Mg",
        condition="as-built",
        notes=(
            "AM-focused entry using a temperature-dependent AlSi10Mg table (MDPI Applied Sciences 2023) "
            "for thermophysical and yield behavior, with room-temperature UTS anchor from NASA "
            "NTRS citation 20205003675."
        ),
        density_ref=2670.0,
        property_sources={
            "k": ("curated-public:alsi10mg-temp-mdpi-ma2023",),
            "cp": ("curated-public:alsi10mg-temp-mdpi-ma2023",),
            "rho": ("curated-public:alsi10mg-temp-mdpi-ma2023",),
            "alpha": ("curated-public:alsi10mg-temp-mdpi-ma2023",),
            "E": (
                "curated-public:alsi10mg-temp-mdpi-ma2023",
                "curated-public:alsi10mg-room-temp-nasa",
            ),
            "nu": ("curated-public:alsi10mg-temp-mdpi-ma2023",),
            "sigma_y": (
                "curated-public:alsi10mg-temp-mdpi-ma2023",
                "curated-public:alsi10mg-room-temp-nasa",
            ),
            "sigma_uts": ("curated-public:alsi10mg-room-temp-nasa",),
        },
    ),
    CanonicalMaterialSpec(
        id="cucrzr-am",
        name="CuCrZr (AM)",
        aliases=(
            "cucrzr",
            "cucrzr am",
            "cucrzr 3d printed",
            "am cucrzr",
        ),
        composition="Cu-Cr-Zr",
        condition="aged",
        notes="Additive manufacturing-focused record with direct NTRS-derived thermal and strength curves.",
        density_ref=8900.0,
        property_sources={
            "k": ("ntrs:20210010991:cucrzr",),
            "cp": ("ntrs:20210010991:cucrzr",),
            "sigma_y": ("ntrs:20210010991:cucrzr",),
        },
    ),
    CanonicalMaterialSpec(
        id="grcop-84-am",
        name="GRCop-84 (AM)",
        aliases=(
            "grcop-84",
            "gr-cop-84",
            "grcop",
            "gr cop",
            "grcop 3d printed",
            "grcop am",
        ),
        composition="Cu-Cr-Nb",
        condition="solution treated & aged",
        notes="Additive manufacturing-focused record with direct NTRS-derived thermal and strength curves.",
        density_ref=8750.0,
        property_sources={
            "k": ("ntrs:20070017311:grcop-84",),
            "sigma_y": ("ntrs:20070017311:grcop-84",),
            "sigma_uts": ("ntrs:20070017311:grcop-84",),
        },
    ),
    CanonicalMaterialSpec(
        id="in718-am",
        name="IN718 (AM)",
        aliases=(
            "in718",
            "inconel 718",
            "in718 am",
            "in718 3d printed",
            "am in718",
        ),
        composition="Ni-Cr-Fe-Nb-Mo",
        condition="solution treated and aged",
        notes=(
            "AM-first entry; bundled strength curves currently fall back to the conventional "
            "Inconel 718 handbook dataset. Thermal conductivity/expansion curves come from NIST."
        ),
        density_ref=8190.0,
        property_sources={
            "k": ("nist-cryo:inconel-718",),
            "eps_th": ("nist-cryo:inconel-718",),
            "sigma_y": ("mil-hdbk-5:H:inconel-718",),
            "sigma_uts": ("mil-hdbk-5:H:inconel-718",),
        },
    ),
    CanonicalMaterialSpec(
        id="ss316-am",
        name="Stainless Steel 316 (AM)",
        aliases=(
            "ss316 am",
            "ss316 3d printed",
            "316 am",
            "316l am",
            "am ss316",
        ),
        composition="Fe-Cr-Ni-Mo",
        condition=None,
        notes=(
            "AM-first entry; currently uses NIST 316 cryogenic/room-temperature thermal and "
            "elastic curves as fallback."
        ),
        density_ref=8000.0,
        property_sources={
            "k": ("nist-cryo:stainless-steel-316",),
            "cp": ("nist-cryo:stainless-steel-316",),
            "E": ("nist-cryo:stainless-steel-316",),
            "eps_th": ("nist-cryo:stainless-steel-316",),
        },
    ),
    CanonicalMaterialSpec(
        id="al-6061-am",
        name="Aluminum 6061 (AM)",
        aliases=(
            "al-6061",
            "al6061",
            "al6061 am",
            "al-6061 3d printed",
            "6061 am",
            "6061 3d printed",
        ),
        composition="Al-Mg-Si",
        condition="T6",
        notes=(
            "AM-first entry; bundled curves currently use conventional 6061-T6 thermal and "
            "strength records with explicit provenance."
        ),
        density_ref=2700.0,
        property_sources={
            "k": ("nist-cryo:aluminum-6061-t6",),
            "cp": ("nist-cryo:aluminum-6061-t6",),
            "E": ("nist-cryo:aluminum-6061-t6",),
            "eps_th": ("nist-cryo:aluminum-6061-t6",),
            "sigma_y": ("mil-hdbk-5:H:al-6061-t6",),
            "sigma_uts": ("mil-hdbk-5:H:al-6061-t6",),
        },
    ),
    CanonicalMaterialSpec(
        id="c110",
        name="Copper C110",
        aliases=("c110", "c11000", "etp copper", "electrolytic tough pitch copper"),
        composition="Cu",
        condition="annealed",
        notes=(
            "Uses Copper.org C11000 room-temperature datasheet properties plus NIST OFHC "
            "temperature-dependent thermal proxies (RRR50 conductivity, cp(T), and alpha(T))."
        ),
        density_ref=8940.0,
        property_sources={
            "k": ("nist-cryo:oxygen-free-copper-rrr50", "curated-public:c110-room-temp"),
            "cp": ("nist-cryo:oxygen-free-copper", "curated-public:c110-room-temp"),
            "rho": ("curated-public:c110-room-temp",),
            "E": ("curated-public:c110-room-temp",),
            "alpha": ("nist-cryo:oxygen-free-copper", "curated-public:c110-room-temp"),
            "sigma_y": ("curated-public:c110-room-temp",),
            "sigma_uts": ("curated-public:c110-room-temp",),
        },
    ),
    CanonicalMaterialSpec(
        id="c101",
        name="Copper C101",
        aliases=("c101", "c10100", "ofhc copper", "oxygen free copper"),
        composition="Cu",
        condition="OFHC",
        notes=(
            "Uses Copper.org room-temperature datasheet properties plus NIST OFHC "
            "temperature-dependent curves for conductivity (RRR100), cp(T), and alpha(T)."
        ),
        density_ref=8940.0,
        property_sources={
            "k": ("nist-cryo:oxygen-free-copper-rrr100", "curated-public:c101-room-temp"),
            "cp": ("nist-cryo:oxygen-free-copper", "curated-public:c101-room-temp"),
            "rho": ("curated-public:c101-room-temp",),
            "E": ("curated-public:c101-room-temp",),
            "alpha": ("nist-cryo:oxygen-free-copper", "curated-public:c101-room-temp"),
            "sigma_y": ("curated-public:c101-room-temp",),
            "sigma_uts": ("curated-public:c101-room-temp",),
        },
    ),
    CanonicalMaterialSpec(
        id="al-6061-t6",
        name="Aluminum 6061-T6",
        aliases=("al6061-t6", "6061-t6", "aa6061-t6", "al 6061 t6"),
        composition="Al-Mg-Si",
        condition="T6",
        notes="Combined thermal/elastic and strength curves from bundled sources.",
        density_ref=2700.0,
        property_sources={
            "k": ("nist-cryo:aluminum-6061-t6",),
            "cp": ("nist-cryo:aluminum-6061-t6",),
            "E": ("nist-cryo:aluminum-6061-t6",),
            "eps_th": ("nist-cryo:aluminum-6061-t6",),
            "sigma_y": ("mil-hdbk-5:H:al-6061-t6",),
            "sigma_uts": ("mil-hdbk-5:H:al-6061-t6",),
        },
    ),
    CanonicalMaterialSpec(
        id="ss316",
        name="Stainless Steel 316",
        aliases=("ss316", "316", "316 stainless", "uns s31600", "uns s31603", "316l"),
        composition="Fe-Cr-Ni-Mo",
        condition=None,
        notes="Cryogenic to room-temperature thermal and elastic curves from NIST.",
        density_ref=8000.0,
        property_sources={
            "k": ("nist-cryo:stainless-steel-316",),
            "cp": ("nist-cryo:stainless-steel-316",),
            "E": ("nist-cryo:stainless-steel-316",),
            "eps_th": ("nist-cryo:stainless-steel-316",),
        },
    ),
    CanonicalMaterialSpec(
        id="ss304",
        name="Stainless Steel 304",
        aliases=("ss304", "304", "304 stainless", "uns s30400"),
        composition="Fe-Cr-Ni",
        condition=None,
        notes="Cryogenic to room-temperature thermal and elastic curves from NIST.",
        density_ref=8030.0,
        property_sources={
            "k": ("nist-cryo:stainless-steel-304",),
            "cp": ("nist-cryo:stainless-steel-304",),
            "E": ("nist-cryo:stainless-steel-304",),
            "eps_th": ("nist-cryo:stainless-steel-304",),
        },
    ),
)

CANONICAL_MATERIALS_BY_ID: dict[str, CanonicalMaterialSpec] = {
    spec.id: spec for spec in CANONICAL_MATERIAL_SPECS
}


def build_canonical_lookup() -> dict[str, str]:
    lookup: dict[str, str] = {}
    for spec in CANONICAL_MATERIAL_SPECS:
        keys = (spec.id, spec.name, *spec.aliases)
        for key in keys:
            normalized = normalize_lookup_key(key)
            if not normalized:
                continue
            existing = lookup.get(normalized)
            if existing and existing != spec.id:
                continue
            lookup[normalized] = spec.id
    return lookup
