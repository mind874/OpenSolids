# OpenSolids

OpenSolids is a Python library for temperature-dependent solid material properties with
explicit provenance.

It is designed for workflows that need curves like `k(T)`, `cp(T)`,
`diffusivity(T)`, `E(T)`, `sigma_y(T)`, and `sigma_uts(T)`.

## Install

```bash
pip install opensolids
```

For plotting examples:

```bash
pip install "opensolids[viz]"
```

## Quick Start

```python
import opensolids as osl

mat = osl.material("al-6061-t6")
print(mat.k(300.0))
print(mat.diffusivity(300.0, units="mm^2/s"))
print(mat.sigma_y(293.15, units="MPa"))
```

## Focused Material IDs

- `alsi10mg-am`
- `cucrzr-am`
- `grcop-84-am`
- `in718-am`
- `ss316-am`
- `al-6061-am`
- `c110`
- `c101`
- `al-6061-t6`
- `ss316`
- `ss304`

Provider-scoped IDs are still supported when direct source selection is needed.

Per-property source and coverage status is tracked in:
- https://github.com/mind874/OpenSolids/blob/main/materials/material_sources.md
- https://github.com/mind874/OpenSolids/blob/main/docs/assets/data/focus_materials_coverage.csv

## API Overview

- `osl.material(id_or_alias)`
- `osl.search(query, required_properties=[...])`
- `osl.list_material_ids()`
- Properties:
  - `mat.k(T)`, `mat.cp(T)`, `mat.rho(T)`, `mat.E(T)`
  - `mat.sigma_y(T)`, `mat.sigma_uts(T)`
  - `mat.eps_th(T, T_ref=...)`
  - `mat.diffusivity(T)`

## Units

Canonical SI units:

- `k`: `W/(m*K)`
- `cp`: `J/(kg*K)`
- `rho`: `kg/m^3`
- `diffusivity`: `m^2/s`
- `E`, `sigma_y`, `sigma_uts`: `Pa`

## Bundled Data + Source Indexes

The wheel includes bundled NIST, NTRS, and MIL-HDBK-5 records.

Catalog and source mapping files in the repository:

- https://github.com/mind874/OpenSolids/blob/main/materials/canonical_materials.csv
- https://github.com/mind874/OpenSolids/blob/main/materials/material_catalog.csv
- https://github.com/mind874/OpenSolids/blob/main/materials/material_sources.md

## Example Plots

<img src="https://raw.githubusercontent.com/mind874/OpenSolids/main/docs/assets/plots/curve_k_regen.png" alt="Thermal conductivity comparison" width="65%">

<img src="https://raw.githubusercontent.com/mind874/OpenSolids/main/docs/assets/plots/curve_sigma_y_regen.png" alt="Yield strength comparison" width="65%">

<img src="https://raw.githubusercontent.com/mind874/OpenSolids/main/docs/assets/plots/curve_diffusivity_selected.png" alt="Thermal diffusivity comparison" width="65%">

<img src="https://raw.githubusercontent.com/mind874/OpenSolids/main/docs/assets/plots/focus_materials_properties.png" alt="Focused material set overview" width="65%">

## License

OpenSolids is licensed under `GPL-3.0-only`.
