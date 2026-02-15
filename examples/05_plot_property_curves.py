"""Generate property-curve visuals and CSV data for documentation and analysis."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

import opensolids as osl

try:
    import matplotlib.pyplot as plt
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "matplotlib is required for this example. Install with: pip install -e '.[viz]'"
    ) from exc


THERMAL_MATERIALS = {
    "GRCop-84": "ntrs:20070017311:grcop-84",
    "CuCrZr": "ntrs:20160001501:cucrzr",
}

STRENGTH_MATERIALS = {
    "GRCop-84": "ntrs:20070017311:grcop-84",
    "CuCrZr": "ntrs:20160001501:cucrzr",
    "Inconel 718": "mil-hdbk-5:H:inconel-718",
}



def _ensure_dirs(plot_dir: Path, data_dir: Path) -> None:
    plot_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)



def _write_csv(path: Path, header: list[str], rows: list[list[float]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)



def generate_thermal_conductivity(plot_dir: Path, data_dir: Path) -> tuple[Path, Path]:
    temps = np.linspace(293.15, 900.0, 180)
    curves: dict[str, np.ndarray] = {}

    for label, material_id in THERMAL_MATERIALS.items():
        mat = osl.material(material_id)
        curves[label] = np.asarray(mat.k(temps, policy="clamp"), dtype=float)

    fig, ax = plt.subplots(figsize=(8.8, 5.2), dpi=150)
    for label, values in curves.items():
        ax.plot(temps, values, linewidth=2.2, label=label)

    ax.set_title("Thermal Conductivity vs Temperature")
    ax.set_xlabel("Temperature [K]")
    ax.set_ylabel("k [W/(m*K)]")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()

    plot_path = plot_dir / "curve_k_regen.png"
    fig.savefig(plot_path)
    plt.close(fig)

    csv_rows: list[list[float]] = []
    for i, t in enumerate(temps):
        csv_rows.append([float(t), float(curves["GRCop-84"][i]), float(curves["CuCrZr"][i])])

    data_path = data_dir / "k_comparison_regen.csv"
    _write_csv(data_path, ["T_K", "k_grcop84_W_per_mK", "k_cucrzr_W_per_mK"], csv_rows)
    return plot_path, data_path



def generate_strength_curves(plot_dir: Path, data_dir: Path) -> tuple[Path, Path]:
    temps = np.linspace(293.15, 900.0, 180)
    curves: dict[str, np.ndarray] = {}

    for label, material_id in STRENGTH_MATERIALS.items():
        mat = osl.material(material_id)
        curves[label] = np.asarray(mat.sigma_y(temps, units="MPa", policy="clamp"), dtype=float)

    fig, ax = plt.subplots(figsize=(8.8, 5.2), dpi=150)
    for label, values in curves.items():
        ax.plot(temps, values, linewidth=2.2, label=label)

    ax.set_title("Yield Strength vs Temperature")
    ax.set_xlabel("Temperature [K]")
    ax.set_ylabel("sigma_y [MPa]")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
    fig.tight_layout()

    plot_path = plot_dir / "curve_sigma_y_regen.png"
    fig.savefig(plot_path)
    plt.close(fig)

    csv_rows: list[list[float]] = []
    for i, t in enumerate(temps):
        csv_rows.append(
            [
                float(t),
                float(curves["GRCop-84"][i]),
                float(curves["CuCrZr"][i]),
                float(curves["Inconel 718"][i]),
            ]
        )

    data_path = data_dir / "sigma_y_comparison_regen.csv"
    _write_csv(
        data_path,
        ["T_K", "sigma_y_grcop84_MPa", "sigma_y_cucrzr_MPa", "sigma_y_in718_MPa"],
        csv_rows,
    )
    return plot_path, data_path



def main() -> None:
    plot_dir = Path("docs/assets/plots")
    data_dir = Path("docs/assets/data")
    _ensure_dirs(plot_dir, data_dir)

    k_plot, k_csv = generate_thermal_conductivity(plot_dir, data_dir)
    sy_plot, sy_csv = generate_strength_curves(plot_dir, data_dir)

    print("Generated files:")
    print(f"- {k_plot}")
    print(f"- {k_csv}")
    print(f"- {sy_plot}")
    print(f"- {sy_csv}")


if __name__ == "__main__":
    main()
