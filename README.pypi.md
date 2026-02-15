# OpenSolids

OpenSolids is a Python library for temperature-dependent solid material properties with
explicit provenance and provider-based data ingestion.

It is built for solver workflows that need curves like `k(T)`, `cp(T)`, `E(T)`, and
`sigma_y(T)` instead of fixed constants.

## Why OpenSolids Exists

Most engineering calculations need properties that change with temperature, not single
constants. OpenSolids was created to make those curves easy to access from Python while
keeping source/provenance information visible.

## Who This Is For

- Propulsion engineers (regen cooling, chamber/nozzle thermal-structural studies)
- Mechanical/materials engineers (strength margins and thermal stress studies)
- Students and independent builders who want reusable material-property tooling

## What You Can Use It For

- Evaluate temperature-dependent conductivity, heat capacity, modulus, and strength
- Compare materials across multiple data providers in one script
- Build design sweeps and trade studies with consistent APIs and units
- Keep source attribution attached to the data you use in analysis

## Install

```bash
pip install opensolids
```

For plot-generating examples:

```bash
pip install "opensolids[viz]"
```

## Quick Start

```python
import opensolids as osl

mat = osl.material("nist-cryo:aluminum-6061-t6")
print(mat.k(300.0))
print(mat.E([77.0, 150.0, 293.15], units="GPa"))
print(mat.eps_th(120.0, T_ref=293.15))
```

## API Overview

- Material lookup: `osl.material(material_id)`
- Search: `osl.search(query)`
- Provider list: `osl.list_providers()`
- Property calls: `mat.k(T)`, `mat.cp(T)`, `mat.E(T)`, `mat.sigma_y(T)`, ...
- Out-of-range policy per call: `policy="clamp" | "raise" | "extrapolate"`
- Units conversion per call: `units="MPa"`, `units="GPa"`, etc.

## Units

OpenSolids stores and serves curves in canonical SI units internally:

- `k`: `W/(m*K)`
- `cp`: `J/(kg*K)`
- `rho`: `kg/m^3`
- `E`, `sigma_y`, `sigma_uts`: `Pa`
- `alpha`: `1/K`
- `nu`, `eps_th`: `1`

## Material Catalog

Bundled material inventory:

- https://github.com/mind874/OpenSolids/blob/main/docs/materials/material_catalog.csv

## Visual Outputs

### Thermal conductivity comparison (NTRS copper alloys)

![Thermal conductivity comparison](https://raw.githubusercontent.com/mind874/OpenSolids/main/docs/assets/plots/curve_k_regen.png)

### Yield strength comparison (NTRS + MIL)

![Yield strength comparison](https://raw.githubusercontent.com/mind874/OpenSolids/main/docs/assets/plots/curve_sigma_y_regen.png)

### Out-of-range policy behavior

![Policy behavior plot](https://raw.githubusercontent.com/mind874/OpenSolids/main/docs/assets/plots/policy_cucrzr_k.png)

### Multi-database 6061 workflow

![Multi-database 6061](https://raw.githubusercontent.com/mind874/OpenSolids/main/docs/assets/plots/al6061_multidatabase.png)

## Documentation

- Usage guide: https://github.com/mind874/OpenSolids/blob/main/docs/usage-guide.md
- Examples: https://github.com/mind874/OpenSolids/blob/main/examples/README.md
- Compliance notes: https://github.com/mind874/OpenSolids/tree/main/docs/compliance
- Source repository: https://github.com/mind874/OpenSolids

## License

OpenSolids is licensed under `GPL-3.0-only`.
