# OpenSolids Usage Guide

This guide is a practical walk-through from installation to engineering-style output.
It includes code, generated plots, and sample numeric outputs.

## 1. Install and Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev,viz]'
```

Quick sanity checks:

```bash
.venv/bin/python -c "import opensolids as osl; print(osl.list_providers())"
.venv/bin/pytest
```

## 2. Core Mental Model

OpenSolids has three core layers:

1. `Material`: high-level API (`k(T)`, `E(T)`, `sigma_y(T)`, ...).
2. `PropertyCurve`: normalized curve metadata + evaluator.
3. Provider/data-pack backend: NIST, NTRS, MIL-HDBK-5 records.

Typical call flow:

1. `osl.material(id)` resolves provider and loads record.
2. `mat.k(T)` evaluates model with selected out-of-range policy.
3. Optional units conversion happens at return.

## 3. First Script: Basic Evaluation

Source: `examples/01_quickstart.py`

```python
import opensolids as osl

mat = osl.material("nist-cryo:aluminum-6061-t6")

k_300 = mat.k(300.0)
E_vals = mat.E([77.0, 150.0, 293.15], units="GPa")
eps_120 = mat.eps_th(120.0, T_ref=293.15)

print(k_300)
print(E_vals)
print(eps_120)
```

Run:

```bash
.venv/bin/python examples/01_quickstart.py
```

Sample output:

```text
Material: nist-cryo:aluminum-6061-t6
Name: Aluminum 6061-T6
Available properties: E, cp, eps_th, k

k(300 K) = 20.903 W/(m*K)
E([77,150,293.15] K) = [69.844  67.8    63.7918] GPa
eps_th(120 K, T_ref=293.15 K) = -1.572163e-03
```

## 4. Visual Example: Property Curves

Source: `examples/05_plot_property_curves.py`

This script:

1. Evaluates thermal conductivity curves for regen-relevant copper alloys.
2. Evaluates yield-strength curves for copper alloys and Inconel 718.
3. Saves plots to `docs/assets/plots/`.
4. Saves numeric tables to `docs/assets/data/`.

Run:

```bash
.venv/bin/python examples/05_plot_property_curves.py
```

### 4.1 Thermal conductivity

Code excerpt:

```python
temps = np.linspace(293.15, 900.0, 180)
mat_grcop = osl.material("ntrs:20070017311:grcop-84")
mat_cucrzr = osl.material("ntrs:20160001501:cucrzr")

k_grcop = mat_grcop.k(temps, policy="clamp")
k_cucrzr = mat_cucrzr.k(temps, policy="clamp")
```

Plot output:

![Thermal conductivity](assets/plots/curve_k_regen.png)

Data output: `docs/assets/data/k_comparison_regen.csv`

| T [K] | GRCop-84 k [W/(m*K)] | CuCrZr k [W/(m*K)] |
| --- | ---: | ---: |
| 293.15 | 325.0 | 330.0 |
| 500.0 | 305.0 | 309.4 |
| 700.0 | 285.0 | 282.8 |
| 900.0 | 268.0 | 250.0 |

### 4.2 Yield strength

Code excerpt:

```python
temps = np.linspace(293.15, 900.0, 180)
mat_in718 = osl.material("mil-hdbk-5:H:inconel-718")

sy_in718 = mat_in718.sigma_y(temps, units="MPa", policy="clamp")
```

Plot output:

![Yield strength](assets/plots/curve_sigma_y_regen.png)

Data output: `docs/assets/data/sigma_y_comparison_regen.csv`

## 5. Visual Example: Out-of-Range Policies

Source: `examples/06_plot_policy_behavior.py`

Run:

```bash
.venv/bin/python examples/06_plot_policy_behavior.py
```

Code excerpt:

```python
mat = osl.material("ntrs:20160001501:cucrzr")
temps = np.linspace(200.0, 1200.0, 220)

k_clamp = mat.k(temps, policy="clamp")
k_extrap = mat.k(temps, policy="extrapolate")
```

Plot output:

![Policy behavior](assets/plots/policy_cucrzr_k.png)

Data output: `docs/assets/data/policy_cucrzr_k.csv`

| T [K] | clamp k [W/(m*K)] | extrapolate k [W/(m*K)] |
| --- | ---: | ---: |
| 250.0 | 330.0 | 333.4 |
| 293.15 | 330.0 | 330.2 |
| 900.0 | 250.2 | 250.2 |
| 1100.0 | 250.0 | 211.3 |

`policy="raise"` behavior at 1200 K:

```text
Temperature out of range [293.15, 900.0] K: [1200.0, 1200.0]
```

## 6. Search + Provenance Example

Source: `examples/03_search_and_provenance.py`

Code excerpt:

```python
hits = osl.search("inconel")
for hit in hits:
    print(hit.id, hit.name, hit.provider)

mat = osl.material("ntrs:20160001501:cucrzr")
for src in mat.sources:
    print(src.source_id, src.title, src.url_or_citation_id)
```

Sample output:

```text
Search hits for 'inconel':
- mil-hdbk-5:H:inconel-718 | Inconel 718 | provider=mil-hdbk-5

Provenance for ntrs:20160001501:cucrzr:
source_id       : ntrs-src:20160001501
title           : CuCrZr high-temperature behavior for engine liners
url/citation    : 20160001501
extraction      : tabular-digitized
```

## 7. Regen Trade Study Example

Source: `examples/04_regen_trade_study.py`

Run:

```bash
.venv/bin/python examples/04_regen_trade_study.py
```

Sample output:

```text
T = 700.00 K
material                                            k    sigma_y
ntrs:20070017311:grcop-84                      285.00     270.00
ntrs:20160001501:cucrzr                        282.80     214.00
ntrs:20190030979:alsi10mg                           -     120.00
mil-hdbk-5:H:inconel-718                            -     860.00
```

## 8. Generate All Visual Assets

Use the convenience script:

```bash
.venv/bin/python examples/07_generate_all_visuals.py
```

It refreshes all files under:

- `docs/assets/plots/`
- `docs/assets/data/`

## 9. CLI Data Workflows

### Sync NIST

```bash
opensolids sync nist-cryo --max-materials 20
```

### Sync NTRS metadata + redistributions

```bash
opensolids sync ntrs --since 2021-01-01 --citation-id 20070017311
```

### Import MIL-HDBK-5 local table

```bash
opensolids import mil-hdbk-5 --pdf /path/to/MIL-HDBK-5.pdf
```

## 10. Error Handling and Best Practices

- Use `policy="raise"` in validation pipelines.
- Use `policy="clamp"` for robust design sweeps.
- Use `mat.available_properties()` before optional property calls.
- Wrap mixed-provider loops with `try/except KeyError`.
- Always inspect `mat.sources` before depending on a curve in reports.

## 11. Known MVP Limits

- Coverage is starter-level and incomplete across materials/properties.
- NTRS is metadata-first with curated numeric subsets.
- MIL PDF import is intentionally minimal and expects clean table text.

## 12. Additional References

- PRD summary: `docs/prd/README.md`
- Compliance notes: `docs/compliance/`
- Example index: `examples/README.md`
