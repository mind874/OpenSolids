# Materials Inventory

- `material_catalog.csv` lists bundled provider-scoped records.
- `canonical_materials.csv` lists plain user-facing material IDs.
- `material_sources.md` maps canonical properties to source references and includes
  units, valid temperature range, and data origin tags.

Regenerate with:

```bash
.venv/bin/python examples/12_export_material_catalog.py
```
