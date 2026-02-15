# OpenSolids Examples

Run examples from repository root after installing in a virtual environment.

```bash
.venv/bin/python examples/01_quickstart.py
```

For visual examples (PNG plots):

```bash
source .venv/bin/activate
pip install -e '.[viz]'
```

## Scripts

- `01_quickstart.py`: basic material lookup and property calls.
- `02_units_and_policies.py`: unit conversion and out-of-range behavior.
- `03_search_and_provenance.py`: search and provenance inspection.
- `04_regen_trade_study.py`: regen-focused material comparison table.
- `05_plot_property_curves.py`: generates curve plots + CSV output data.
- `06_plot_policy_behavior.py`: visualizes policy behavior + CSV output data.
- `07_generate_all_visuals.py`: runs the visual scripts and refreshes docs assets.

## Generated output locations

- Plots: `docs/assets/plots/`
- Data tables: `docs/assets/data/`
