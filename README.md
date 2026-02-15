# OpenSolids

OpenSolids is an open-source tooling layer for temperature-dependent solid material
properties with explicit provenance and provider-based data ingestion.

## License

OpenSolids is licensed under `GPL-3.0-only`. Distributed derivative programs that
incorporate OpenSolids must also be released under GPL-compatible open-source terms.

## Quick start

```python
import opensolids as osl

mat = osl.material("nist-cryo:aluminum-6061-t6")
print(mat.k(300.0))
```

## CLI

```bash
opensolids sync nist-cryo
opensolids sync ntrs --since 2021-01-01
opensolids import mil-hdbk-5 --pdf /path/to/MIL-HDBK-5.pdf
```
