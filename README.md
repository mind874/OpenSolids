# OpenSolids

OpenSolids is a Python library for temperature-dependent solid material properties with
explicit provenance and provider-based data ingestion.

It is built for solver workflows that need curves like `k(T)`, `cp(T)`, `E(T)`, and
`sigma_y(T)` instead of fixed constants.

## Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

For plot-generating examples:

```bash
pip install -e '.[viz]'
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

## Visual Outputs

### Thermal conductivity comparison (NTRS copper alloys)

Code source: `examples/05_plot_property_curves.py`

![Thermal conductivity comparison](docs/assets/plots/curve_k_regen.png)

### Yield strength comparison (NTRS + MIL)

Code source: `examples/05_plot_property_curves.py`

![Yield strength comparison](docs/assets/plots/curve_sigma_y_regen.png)

### Out-of-range policy behavior

Code source: `examples/06_plot_policy_behavior.py`

![Policy behavior plot](docs/assets/plots/policy_cucrzr_k.png)

### Provider coverage across databases

Code source: `examples/09_plot_provider_coverage.py`

![Provider material counts](docs/assets/plots/provider_material_counts.png)

![Provider property coverage](docs/assets/plots/provider_property_coverage_heatmap.png)

### Multi-database 6061 workflow

Code source: `examples/10_plot_multidatabase_6061.py`

![Multi-database 6061](docs/assets/plots/al6061_multidatabase.png)

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
- `examples/09_plot_provider_coverage.py`
- `examples/10_plot_multidatabase_6061.py`

Run all visual examples:

```bash
.venv/bin/python examples/07_generate_all_visuals.py
```

## Documentation

- Comprehensive guide: `docs/usage-guide.md`
- Example index: `examples/README.md`
- Compliance notes: `docs/compliance/`

## License

OpenSolids is licensed under `GPL-3.0-only`.

This is a strong copyleft license. If you distribute a derivative work that includes
OpenSolids, you must make the derivative source available under GPL-compatible terms.
