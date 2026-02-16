"""Generate property-curve visuals and CSV data for documentation and analysis."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

import opensolids as osl
from _plot_style import apply_plot_style, color_for_label

try:
    import matplotlib.pyplot as plt
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "matplotlib is required for this example. Install with: pip install -e '.[viz]'"
    ) from exc


THERMAL_MATERIALS = {
    "GRCop-84 (AM)": "grcop-84-am",
    "CuCrZr (AM)": "cucrzr-am",
}

STRENGTH_MATERIALS = {
    "GRCop-84 (AM)": "grcop-84-am",
    "IN718 (AM entry)": "in718-am",
}

DIFFUSIVITY_MATERIALS = {
    "Al 6061-T6": "al-6061-t6",
    "CuCrZr (AM)": "cucrzr-am",
    "SS304": "ss304",
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

    fig, ax = plt.subplots(figsize=(9.4, 5.4), dpi=165)
    for label, values in curves.items():
        color = color_for_label(label)
        ax.plot(temps, values, linewidth=2.6, color=color, label=label)
        ax.scatter(temps[::35], values[::35], s=14, color=color, alpha=0.9, zorder=3)

    ax.set_title("Thermal Conductivity vs Temperature")
    ax.set_xlabel("Temperature [K]")
    ax.set_ylabel("k [W/(m*K)]")
    ax.set_xlim(float(temps[0]), float(temps[-1]))
    ax.legend(loc="upper right")
    fig.tight_layout()

    plot_path = plot_dir / "curve_k_regen.png"
    fig.savefig(plot_path)
    plt.close(fig)

    csv_rows: list[list[float]] = []
    for i, t in enumerate(temps):
        csv_rows.append(
            [
                float(t),
                float(curves["GRCop-84 (AM)"][i]),
                float(curves["CuCrZr (AM)"][i]),
            ]
        )

    data_path = data_dir / "k_comparison_regen.csv"
    _write_csv(data_path, ["T_K", "k_grcop84_W_per_mK", "k_cucrzr_W_per_mK"], csv_rows)
    return plot_path, data_path


def generate_strength_curves(plot_dir: Path, data_dir: Path) -> tuple[Path, Path]:
    temps = np.linspace(293.15, 900.0, 180)
    curves: dict[str, np.ndarray] = {}

    for label, material_id in STRENGTH_MATERIALS.items():
        mat = osl.material(material_id)
        curves[label] = np.asarray(mat.sigma_y(temps, units="MPa", policy="clamp"), dtype=float)

    fig, ax = plt.subplots(figsize=(9.4, 5.4), dpi=165)
    for label, values in curves.items():
        color = color_for_label(label)
        ax.plot(temps, values, linewidth=2.6, color=color, label=label)
        ax.scatter(temps[::35], values[::35], s=14, color=color, alpha=0.9, zorder=3)

    ax.set_title("Yield Strength vs Temperature")
    ax.set_xlabel("Temperature [K]")
    ax.set_ylabel("sigma_y [MPa]")
    ax.set_xlim(float(temps[0]), float(temps[-1]))
    ax.legend(loc="upper right")
    fig.tight_layout()

    plot_path = plot_dir / "curve_sigma_y_regen.png"
    fig.savefig(plot_path)
    plt.close(fig)

    csv_rows: list[list[float]] = []
    for i, t in enumerate(temps):
        csv_rows.append(
            [
                float(t),
                float(curves["GRCop-84 (AM)"][i]),
                float(curves["IN718 (AM entry)"][i]),
            ]
        )

    data_path = data_dir / "sigma_y_comparison_regen.csv"
    _write_csv(
        data_path,
        ["T_K", "sigma_y_grcop84_MPa", "sigma_y_in718_MPa"],
        csv_rows,
    )
    return plot_path, data_path


def generate_diffusivity_curves(plot_dir: Path, data_dir: Path) -> tuple[Path, Path]:
    temps = np.linspace(293.15, 900.0, 180)
    curves: dict[str, np.ndarray] = {}

    for label, material_id in DIFFUSIVITY_MATERIALS.items():
        mat = osl.material(material_id)
        curves[label] = np.asarray(mat.diffusivity(temps, units="mm^2/s", policy="clamp"), dtype=float)

    fig, ax = plt.subplots(figsize=(9.4, 5.4), dpi=165)
    for label, values in curves.items():
        color = color_for_label(label)
        ax.plot(temps, values, linewidth=2.6, color=color, label=label)
        ax.scatter(temps[::35], values[::35], s=14, color=color, alpha=0.9, zorder=3)

    # 6061 data is valid to 300 K in this dataset; values beyond that are clamp-policy behavior.
    ax.axvspan(300.0, float(temps[-1]), color="#eceff8", alpha=0.65, zorder=0)
    ax.axvline(300.0, color="#7f8aa3", linewidth=1.2, linestyle="--", alpha=0.8)
    ax.text(307.0, float(np.max([v.max() for v in curves.values()])) * 0.97, "clamp region for 6061", fontsize=9)

    ax.set_title("Thermal Diffusivity vs Temperature")
    ax.set_xlabel("Temperature [K]")
    ax.set_ylabel("diffusivity [mm^2/s]")
    ax.set_xlim(float(temps[0]), float(temps[-1]))
    ax.legend(loc="upper right")
    fig.tight_layout()

    plot_path = plot_dir / "curve_diffusivity_selected.png"
    fig.savefig(plot_path)
    plt.close(fig)

    csv_rows: list[list[float]] = []
    for i, t in enumerate(temps):
        csv_rows.append(
            [
                float(t),
                float(curves["Al 6061-T6"][i]),
                float(curves["CuCrZr (AM)"][i]),
                float(curves["SS304"][i]),
            ]
        )

    data_path = data_dir / "diffusivity_comparison_selected.csv"
    _write_csv(
        data_path,
        ["T_K", "a_6061_mm2_per_s", "a_cucrzr_mm2_per_s", "a_ss304_mm2_per_s"],
        csv_rows,
    )
    return plot_path, data_path


def main() -> None:
    apply_plot_style()

    plot_dir = Path("docs/assets/plots")
    data_dir = Path("docs/assets/data")
    _ensure_dirs(plot_dir, data_dir)

    k_plot, k_csv = generate_thermal_conductivity(plot_dir, data_dir)
    sy_plot, sy_csv = generate_strength_curves(plot_dir, data_dir)
    a_plot, a_csv = generate_diffusivity_curves(plot_dir, data_dir)

    print("Generated files:")
    print(f"- {k_plot}")
    print(f"- {k_csv}")
    print(f"- {sy_plot}")
    print(f"- {sy_csv}")
    print(f"- {a_plot}")
    print(f"- {a_csv}")


if __name__ == "__main__":
    main()
