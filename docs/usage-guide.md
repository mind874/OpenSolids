# OpenSolids Usage Guide

This guide covers practical usage patterns for the OpenSolids MVP.

## 1. Install and Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

Sanity check:

```bash
.venv/bin/python -c "import opensolids as osl; print(osl.list_providers())"
```

Expected providers include:

- `nist-cryo`
- `ntrs`
- `mil-hdbk-5`

## 2. Material Lookup

Use stable material IDs.

```python
import opensolids as osl

mat = osl.material("nist-cryo:aluminum-6061-t6")
print(mat.name)
print(mat.available_properties())
```

## 3. Property Evaluation

All temperatures are in Kelvin.

```python
# scalar in -> scalar out
k_300 = mat.k(300.0)

# list/array in -> numpy array out
E_vals = mat.E([77.0, 293.15])
```

### Property method names

- Thermophysical: `k`, `cp`, `rho`
- Thermoelastic: `E`, `nu`, `alpha`, `eps_th`
- Strength: `sigma_y`, `sigma_uts`

If a property is missing for a material, calling it raises `KeyError`.

## 4. Units Conversion

OpenSolids stores canonical SI internally. Use `units=...` for conversions.

```python
sy_pa = mat.sigma_y(293.15)
sy_mpa = mat.sigma_y(293.15, units="MPa")
```

Examples:

- conductivity: `W/(m*K)`
- specific heat: `J/(kg*K)`
- modulus/strength: `Pa`, `MPa`, `GPa`

## 5. Out-of-Range Policy

Per property call, you can set:

- `policy="clamp"` (default)
- `policy="raise"`
- `policy="extrapolate"`

```python
mat.k(2500.0, policy="clamp")
```

Use `raise` in strict validation workflows to detect unsupported temperature ranges.

## 6. Thermal Strain (`eps_th`)

```python
eps = mat.eps_th(120.0, T_ref=293.15)
```

Behavior:

- If `eps_th` exists, OpenSolids evaluates the stored strain curve.
- If only `alpha` exists, OpenSolids numerically integrates `alpha(T)` from `T_ref`.

## 7. Search and Discovery

```python
import opensolids as osl

hits = osl.search("inconel")
for hit in hits:
    print(hit.id, hit.name, hit.provider)
```

Search matches ID, name, condition, and aliases.

## 8. Provenance Inspection

```python
mat = osl.material("ntrs:20160001501:cucrzr")
for src in mat.sources:
    print(src.source_id)
    print(src.title)
    print(src.url_or_citation_id)
    print(src.extraction_method)
```

Provenance records are intended to make data origin and extraction method explicit.

## 9. CLI Data Workflows

### Sync NIST cryogenic data

```bash
opensolids sync nist-cryo --max-materials 20
```

Writes provider data-pack files (`materials/`, `sources/`, `manifest.json`).

### Sync NTRS metadata

```bash
opensolids sync ntrs --since 2021-01-01 --citation-id 20070017311
```

### Import MIL-HDBK-5 local PDF data

```bash
opensolids import mil-hdbk-5 --pdf /path/to/MIL-HDBK-5.pdf
```

Note: this importer requires `pdftotext` and expects parseable two-column table rows.

## 10. Typical Engineering Patterns

### Pattern A: Hot-wall strength margin check

```python
mat = osl.material("mil-hdbk-5:H:inconel-718")
for T in [600.0, 800.0, 1000.0]:
    print(T, mat.sigma_y(T, units="MPa"))
```

### Pattern B: Material trade at selected temperatures

```python
ids = [
    "ntrs:20070017311:grcop-84",
    "ntrs:20160001501:cucrzr",
    "ntrs:20190030979:alsi10mg",
]
for material_id in ids:
    m = osl.material(material_id)
    if "k" in m.available_properties():
        print(material_id, m.k(700.0))
```

## 11. Error Handling Tips

- Wrap property calls in `try/except KeyError` when iterating mixed material sets.
- Use `policy="raise"` during validation to catch out-of-range conditions early.
- Inspect `mat.available_properties()` before calling optional properties.

## 12. Known MVP Limitations

- Data coverage is starter-level and provider dependent.
- Some provider tooling is intentionally conservative (compliance-first).
- MIL import parser is intentionally minimal and expects clean numeric rows.

## 13. Where to Look Next

- PRD summary: `docs/prd/README.md`
- Compliance notes: `docs/compliance/nist.md`, `docs/compliance/nasa_ntrs.md`, `docs/compliance/mil_hdbk_5.md`
- Runnable examples: `examples/README.md`
