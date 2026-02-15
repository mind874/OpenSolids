# OpenSolids

OpenSolids is a Python library for temperature-dependent solid material properties with
explicit provenance and provider-based data ingestion.

It is designed for solver workflows that need values like `k(T)`, `cp(T)`, `E(T)`, and
`sigma_y(T)` instead of fixed constants.

## What You Get

- Temperature-dependent property evaluation with scalar and vector inputs.
- Consistent property API across providers.
- Explicit provenance (`SourceRef`) for each material record.
- Safe out-of-range behavior (`clamp` default, `raise`, `extrapolate`).
- Three provider modules and offline data-pack structure:
  - `nist-cryo`
  - `ntrs`
  - `mil-hdbk-5`

## Install

### Local development

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

### Use in code

```python
import opensolids as osl

mat = osl.material("nist-cryo:aluminum-6061-t6")
print(mat.k(300.0))
```

## Quick API Tour

```python
import opensolids as osl

mat = osl.material("ntrs:20160001501:cucrzr")

# scalar input -> scalar output
k_500 = mat.k(500.0)

# vector input -> numpy array output
E_curve = mat.E([293.15, 500.0, 700.0])

# units conversion through pint
sigma_y_mpa = mat.sigma_y(293.15, units="MPa")

# out-of-range policy: clamp | raise | extrapolate
safe_value = mat.k(2000.0, policy="clamp")
```

## Core Concepts

### Material lookup

```python
mat = osl.material("nist-cryo:aluminum-6061-t6")
```

### Property methods

Available method names include:

- `k`, `cp`, `rho`
- `E`, `nu`, `alpha`, `eps_th`
- `sigma_y`, `sigma_uts`

Use `mat.available_properties()` to inspect what a specific material supports.

### Thermal strain helper

`eps_th(T, T_ref=293.15)` works in two ways:

- Directly from stored `eps_th` curve when present.
- By integrating `alpha(T)` if `eps_th` is not stored.

### Provenance

Each material exposes `mat.sources`, a list of `SourceRef` objects with:

- source IDs and titles
- URL/citation info
- extraction method
- license notes

## Search and Discovery

```python
import opensolids as osl

providers = osl.list_providers()
results = osl.search("cucrzr")

for item in results:
    print(item.id, item.name, item.provider)
```

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

Runnable scripts are in `examples/`:

- `examples/01_quickstart.py`
- `examples/02_units_and_policies.py`
- `examples/03_search_and_provenance.py`
- `examples/04_regen_trade_study.py`

Run them with:

```bash
.venv/bin/python examples/01_quickstart.py
```

See `examples/README.md` for details.

## Full Usage Guide

Detailed, step-by-step guide: `docs/usage-guide.md`.

## Current Scope

This is an MVP-focused engineering toolkit. It is not a certification library and does
not replace source-document engineering judgment.

## License

OpenSolids is licensed under `GPL-3.0-only`.

This is a strong copyleft license. If you distribute a derivative work that includes
OpenSolids, you must make the derivative source available under GPL-compatible terms.
