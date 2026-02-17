# Contributing Temperature-Dependent Data

This guide covers adding new `k(T)` and `sigma_y(T)` datasets to OpenSolids with
consistent SI units and provenance metadata.

## Scope

- Temperature-dependent curves only (not single-point room-temperature anchors).
- Curves are stored in provider data packs under `packages/*/src/*/materials/*.json`.
- Source metadata is stored under `packages/*/src/*/sources/*.json`.

## 1. Normalize to SI Before Writing JSON

OpenSolids stores curve values in canonical SI:

- Temperature axis `T`: `K`
- Thermal conductivity `k`: `W/(m*K)`
- Yield strength `sigma_y`: `Pa`

Common conversions:

- `T_K = T_C + 273.15`
- `T_K = (T_F - 32) * 5/9 + 273.15`
- `sigma_y(Pa) = sigma_y(MPa) * 1e6`
- `sigma_y(Pa) = sigma_y(GPa) * 1e9`
- `k(W/(m*K)) = k(W/(cm*K)) * 100`

If the source uses other units, convert to SI first, then store SI values only.

## 2. Add or Update Source Metadata (`sources/*.json`)

Each source record should include:

- Required in practice: `source_id`, `title`, `publisher`, `url_or_citation_id`, `retrieved_at`
- Strongly recommended: `organization`, `license_notes`, `page_or_table`, `extraction_method`, `metadata`

Use `metadata.data_origin` to tag how numbers were produced. Recommended tags:

- `experimental`: measured data
- `computed`: model-derived data (for example JMatPro/CALPHAD-based tables)
- `tabular-digitized`: digitized from figure/table
- `fit-parse`: parsed from published fit/equation
- `manual`: hand-entered from a tabulated source

`materials/material_sources.md` uses:

- `metadata.data_origin` when present
- otherwise `extraction_method`

## 3. Add or Update Material Record (`materials/*.json`)

Material records must include:

- `id`, `name`, `aliases`, `sources`, `properties`

For each property curve (`k`, `sigma_y`), include:

- `units` (SI canonical units above)
- `valid_T_min`, `valid_T_max` (Kelvin)
- `source_id` (must match a source record)
- `model`

For tabular curves, use:

```json
"model": {
  "type": "tabular",
  "interpolation": "linear",
  "T": [293.15, 500.0, 700.0],
  "y": [/* SI values */]
}
```

Curve hygiene requirements:

- `T` and `y` arrays are same length
- `T` is strictly increasing
- `valid_T_min == min(T)` and `valid_T_max == max(T)`
- No extrapolated points outside the cited source range

For `sigma_y`, add `properties.sigma_y.metadata.yield_definition` when known
(for example `0.2% offset`) so downstream users can interpret the strength basis.

## 4. Set `valid_T_range` Correctly

`valid_T_range_K` shown in `materials/material_sources.md` is the inclusive
source-supported interval `[valid_T_min, valid_T_max]` in Kelvin.

- It is a provenance/validity bound, not an uncertainty band.
- For derived properties (for example diffusivity from `k`, `cp`, `rho`), the
  exported range is the overlap/intersection of component ranges.

## 5. Regenerate Material Index Docs

After updating data files:

```bash
.venv/bin/python examples/12_export_material_catalog.py
```

This refreshes:

- `materials/material_catalog.csv`
- `materials/canonical_materials.csv`
- `materials/material_sources.md`

## 6. Quick Sanity Checks

- Load the material and evaluate both curves at representative temperatures.
- Confirm units round-trip (for example `Pa <-> MPa`, `K <-> degC` in API calls).
- Confirm out-of-range behavior is expected with `policy="raise"` and `policy="clamp"`.
