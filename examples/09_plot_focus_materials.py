"""Plot the focused material set requested for propulsion and thermal studies."""

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


FOCUS_MATERIALS = [
    "alsi10mg-am",
    "cucrzr-am",
    "grcop-84-am",
    "in718-am",
    "ss316-am",
    "al-6061-am",
    "c110",
    "c101",
    "al-6061-t6",
    "ss316",
    "ss304",
]

PLOT_PROPERTIES = (
    ("k", "W/(m*K)", "Thermal Conductivity"),
    ("diffusivity", "mm^2/s", "Thermal Diffusivity"),
    ("sigma_y", "MPa", "Yield Strength"),
    ("sigma_uts", "MPa", "Ultimate Strength"),
)


def _ensure_dirs(plot_dir: Path, data_dir: Path) -> None:
    plot_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)


def _write_csv(path: Path, header: list[str], rows: list[list[str]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def _material_label(material_id: str) -> str:
    return material_id.replace("-am", " (AM)")


def main() -> None:
    plot_dir = Path("docs/assets/plots")
    data_dir = Path("docs/assets/data")
    _ensure_dirs(plot_dir, data_dir)

    temps = np.linspace(293.15, 900.0, 180)
    coverage_rows: list[list[str]] = []

    fig, axes = plt.subplots(2, 2, figsize=(12.0, 8.2), dpi=150)
    axes_flat = list(axes.ravel())

    for ax, (prop, units, title) in zip(axes_flat, PLOT_PROPERTIES):
        for material_id in FOCUS_MATERIALS:
            mat = osl.material(material_id)
            available = prop in set(mat.available_properties())
            if not available:
                continue
            values = np.asarray(getattr(mat, prop)(temps, units=units, policy="clamp"), dtype=float)
            ax.plot(temps, values, linewidth=1.8, label=_material_label(material_id))

        ax.set_title(f"{title} vs Temperature")
        ax.set_xlabel("Temperature [K]")
        ax.set_ylabel(f"{prop} [{units}]")
        ax.grid(alpha=0.2)
        if ax.lines:
            ax.legend(frameon=False, fontsize=7, ncol=2)

    fig.tight_layout()
    plot_path = plot_dir / "focus_materials_properties.png"
    fig.savefig(plot_path)
    plt.close(fig)

    for material_id in FOCUS_MATERIALS:
        mat = osl.material(material_id)
        props = set(mat.available_properties())
        coverage_rows.append(
            [
                material_id,
                mat.name,
                "yes" if "k" in props else "",
                "yes" if "cp" in props else "",
                "yes" if "diffusivity" in props else "",
                "yes" if "sigma_y" in props else "",
                "yes" if "sigma_uts" in props else "",
                "yes" if "E" in props else "",
            ]
        )

    coverage_path = data_dir / "focus_materials_coverage.csv"
    _write_csv(
        coverage_path,
        ["material_id", "name", "k", "cp", "diffusivity", "sigma_y", "sigma_uts", "E"],
        coverage_rows,
    )

    print("Generated files:")
    print(f"- {plot_path}")
    print(f"- {coverage_path}")


if __name__ == "__main__":
    main()
