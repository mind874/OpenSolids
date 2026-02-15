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
python3 -m venv .venv
source .venv/bin/activate
pip install opensolids
```

For plot-generating examples:

```bash
pip install "opensolids[viz]"
```

For local development from this repository:

```bash
pip install -e '.[dev,viz]'
```

## Quick Start

```python
import opensolids as osl

mat = osl.material("nist-cryo:aluminum-6061-t6")
print(mat.k(300.0))
print(mat.E([77.0, 150.0, 293.15], units="GPa"))
print(mat.eps_th(120.0, T_ref=293.15))
```

## Which Database Should I Use?

Use provider IDs by prefix:

- `nist-cryo:*` for cryogenic to room-temperature thermal/elastic curves.
- `ntrs:*` for curated NASA-report-derived high-temperature material curves.
- `mil-hdbk-5:*` for handbook allowables style strength curves.

Example material IDs:

- `nist-cryo:aluminum-6061-t6`
- `ntrs:20160001501:cucrzr`
- `mil-hdbk-5:H:inconel-718`

Provider workflow example script: `examples/08_database_workflows.py`

Run:

```bash
.venv/bin/python examples/08_database_workflows.py
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

You can request output units per call with `units=...`.

## Data Packaging

Provider databases are bundled with the `opensolids` wheel, so `pip install opensolids`
includes NIST, curated NTRS, and MIL-HDBK-5 records by default.

If you are working from source, provider data also resolves from the local
`packages/opensolids_data_*` directories.

## Material Catalog

See `docs/materials/material_catalog.csv` for a current list of bundled materials across
all providers.

## Visual Outputs

### Thermal conductivity comparison (NTRS copper alloys)

Code source: `examples/05_plot_property_curves.py`

<img src="docs/assets/plots/curve_k_regen.png" alt="Thermal conductivity comparison" width="65%">

### Yield strength comparison (NTRS + MIL)

Code source: `examples/05_plot_property_curves.py`

<img src="docs/assets/plots/curve_sigma_y_regen.png" alt="Yield strength comparison" width="65%">

### Out-of-range policy behavior

Code source: `examples/06_plot_policy_behavior.py`

<img src="docs/assets/plots/policy_cucrzr_k.png" alt="Policy behavior plot" width="65%">

### Multi-database 6061 workflow

Code source: `examples/10_plot_multidatabase_6061.py`

<img src="docs/assets/plots/al6061_multidatabase.png" alt="Multi-database 6061" width="65%">

## CLI Workflows

```bash
# Sync NIST cryogenic pages into a data-pack directory
opensolids sync nist-cryo --max-materials 10

# Sync NTRS metadata and redistribution checks
opensolids sync ntrs --since 2021-01-01 --citation-id 20070017311

# Import MIL-HDBK-5 tabular data from local PDF (pdftotext required)
opensolids import mil-hdbk-5 --pdf /path/to/MIL-HDBK-5.pdf
```

## Examples

- `examples/01_quickstart.py`
- `examples/02_units_and_policies.py`
- `examples/03_search_and_provenance.py`
- `examples/04_regen_trade_study.py`
- `examples/05_plot_property_curves.py`
- `examples/06_plot_policy_behavior.py`
- `examples/07_generate_all_visuals.py`
- `examples/08_database_workflows.py`
- `examples/10_plot_multidatabase_6061.py`
- `examples/11_verify_units_and_sanity.py`
- `examples/12_export_material_catalog.py`

Run all visual examples:

```bash
.venv/bin/python examples/07_generate_all_visuals.py
```

Run the database SI/sanity verification example:

```bash
.venv/bin/python examples/11_verify_units_and_sanity.py
```

Export the bundled material catalog:

```bash
.venv/bin/python examples/12_export_material_catalog.py
```

## Documentation

- Comprehensive guide: `docs/usage-guide.md`
- Example index: `examples/README.md`
- Compliance notes: `docs/compliance/`
- Release guide: `docs/releasing.md`

## License

OpenSolids is licensed under `GPL-3.0-only`.

If you plan to distribute software that includes OpenSolids, review the GPL terms in
`LICENSE` to understand your distribution requirements.
