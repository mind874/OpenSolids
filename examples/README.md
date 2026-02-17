# OpenSolids Examples

Run examples from repository root after installing in a virtual environment.

```bash
.venv/bin/python examples/01_quickstart.py
```

For visual examples (PNG plots):

```bash
source .venv/bin/activate
pip install "opensolids[viz]"
```

For local development in this repository:

```bash
pip install -e '.[dev,viz]'
```

## Scripts

- `01_quickstart.py`: basic material lookup and property calls.
- `02_units_and_policies.py`: unit conversion and out-of-range behavior.
- `03_search_and_provenance.py`: search and provenance inspection.
- `04_regen_trade_study.py`: regen-focused material comparison table.
- `05_plot_property_curves.py`: family-grouped curve plots (temperature-varying data only) + CSV outputs + exclusions report.
- `06_plot_policy_behavior.py`: out-of-range policy plot + CSV output.
- `07_generate_all_visuals.py`: refreshes all documentation visual assets.
- `08_database_workflows.py`: practical walkthrough for NIST/NTRS/MIL usage.
- `09_plot_focus_materials.py`: plots focused materials by family (temperature-varying data only) with strict coverage/missing-status exports.
- `10_plot_multidatabase_6061.py`: combines NIST and MIL data for one alloy workflow.
- `11_verify_units_and_sanity.py`: SI unit compatibility + reference sanity checks.
- `12_export_material_catalog.py`: exports a CSV inventory of bundled materials.
- `13_audit_focus_material_sources.py`: prints per-property SI values, valid temperature ranges, and source IDs for focused materials.

## Generated output locations

- Plots: `docs/assets/plots/`
- Data tables: `docs/assets/data/`
  - includes `plot_exclusions_by_property.csv`
  - includes `focus_materials_missing_data.csv`
  - includes `focus_material_plot_status.csv`
