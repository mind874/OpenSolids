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

## API Overview

- Material lookup: `osl.material(material_id)`
- Search: `osl.search(query)`
- Provider list: `osl.list_providers()`
- Property calls: `mat.k(T)`, `mat.cp(T)`, `mat.E(T)`, `mat.sigma_y(T)`, ...
- Out-of-range policy per call: `policy="clamp" | "raise" | "extrapolate"`
- Units conversion per call: `units="MPa"`, `units="GPa"`, etc.

## Visual Example Outputs

The repository includes generated visual outputs under `docs/assets/plots/`.

### Thermal conductivity comparison

Code source: `examples/05_plot_property_curves.py`

![Thermal conductivity comparison](docs/assets/plots/curve_k_regen.png)

Sample data (`docs/assets/data/k_comparison_regen.csv`):

| T [K] | GRCop-84 k [W/(m*K)] | CuCrZr k [W/(m*K)] |
| --- | ---: | ---: |
| 293.15 | 325.0 | 330.0 |
| 500.0 | 305.0 | 309.4 |
| 700.0 | 285.0 | 282.8 |
| 900.0 | 268.0 | 250.0 |

### Yield strength comparison

Code source: `examples/05_plot_property_curves.py`

![Yield strength comparison](docs/assets/plots/curve_sigma_y_regen.png)

### Out-of-range policy behavior

Code source: `examples/06_plot_policy_behavior.py`

![Policy behavior plot](docs/assets/plots/policy_cucrzr_k.png)

Sample policy behavior (`docs/assets/data/policy_cucrzr_k.csv`):

| T [K] | clamp k [W/(m*K)] | extrapolate k [W/(m*K)] |
| --- | ---: | ---: |
| 250.0 | 330.0 | 333.4 |
| 293.15 | 330.0 | 330.2 |
| 900.0 | 250.2 | 250.2 |
| 1100.0 | 250.0 | 211.3 |

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
