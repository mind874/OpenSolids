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
- `05_plot_property_curves.py`: curve plots + CSV outputs.
- `06_plot_policy_behavior.py`: out-of-range policy plot + CSV output.
- `07_generate_all_visuals.py`: refreshes all documentation visual assets.
- `08_database_workflows.py`: practical walkthrough for NIST/NTRS/MIL usage.
- `10_plot_multidatabase_6061.py`: combines NIST and MIL data for one alloy workflow.
- `11_verify_units_and_sanity.py`: SI unit compatibility + reference sanity checks.

## Generated output locations

- Plots: `docs/assets/plots/`
- Data tables: `docs/assets/data/`
