# Materials Inventory

- `material_catalog.csv` lists bundled provider-scoped records.
- `canonical_materials.csv` lists plain user-facing material IDs.
- `material_sources.md` maps canonical properties to source references and includes
  units, valid temperature range, and data origin tags.
- `../docs/contributing_data.md` is the contributor guide for adding new
  temperature-dependent `k(T)` / `sigma_y(T)` datasets.

Interpretation notes for `material_sources.md`:

- `data_origin` is read from `source.metadata.data_origin` when present; otherwise
  it falls back to `source.extraction_method`.
- `valid_T_range_K` is an inclusive Kelvin interval `[T_min, T_max]` where the
  source-backed curve is intended to be used; it is not an uncertainty interval.
- `temperature_dependent` is `yes` when `valid_T_max > valid_T_min`; `no` means a
  single-temperature anchor value.
- `curve_metadata` carries property-specific context (for example
  `yield_definition`, heat treatment, process, and notes).
- Derived-property rows (for example diffusivity) use the overlap/intersection of
  component ranges.

Regenerate with:

```bash
.venv/bin/python examples/12_export_material_catalog.py
```
