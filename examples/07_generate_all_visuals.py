"""Run all visualization examples and regenerate docs assets."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path



def _run(script_name: str) -> None:
    script_path = Path(__file__).resolve().parent / script_name
    print(f"Running {script_path}...")
    subprocess.run([sys.executable, str(script_path)], check=True)



def main() -> None:
    _run("05_plot_property_curves.py")
    _run("06_plot_policy_behavior.py")
    _run("10_plot_multidatabase_6061.py")
    print("Done. Updated docs/assets/plots and docs/assets/data")


if __name__ == "__main__":
    main()
