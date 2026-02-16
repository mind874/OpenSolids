"""Plot the focused material set requested for propulsion and thermal studies."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

import opensolids as osl
from _plot_style import apply_plot_style

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


def _material_color_map(material_ids: list[str]) -> dict[str, tuple[float, float, float, float]]:
    cmap = plt.get_cmap("tab20")
    return {material_id: cmap(i % 20) for i, material_id in enumerate(material_ids)}


def main() -> None:
    apply_plot_style()

    plot_dir = Path("docs/assets/plots")
    data_dir = Path("docs/assets/data")
    _ensure_dirs(plot_dir, data_dir)

    temps = np.linspace(293.15, 900.0, 180)
    coverage_rows: list[list[str]] = []

    fig, axes = plt.subplots(2, 2, figsize=(13.2, 8.8), dpi=165)
    axes_flat = list(axes.ravel())
    color_map = _material_color_map(FOCUS_MATERIALS)
    line_handles: dict[str, object] = {}

    for ax, (prop, units, title) in zip(axes_flat, PLOT_PROPERTIES):
        missing_count = 0
        for material_id in FOCUS_MATERIALS:
            mat = osl.material(material_id)
            available = prop in set(mat.available_properties())
            if not available:
                missing_count += 1
                continue
            values = np.asarray(getattr(mat, prop)(temps, units=units, policy="clamp"), dtype=float)
            label = _material_label(material_id)
            line_style = "-" if material_id.endswith("-am") else "--"
            (line,) = ax.plot(
                temps,
                values,
                linewidth=2.0,
                linestyle=line_style,
                color=color_map[material_id],
                label=label,
            )
            if label not in line_handles:
                line_handles[label] = line

        ax.set_title(f"{title} vs Temperature")
        ax.set_xlabel("Temperature [K]")
        ax.set_ylabel(f"{prop} [{units}]")
        ax.set_xlim(float(temps[0]), float(temps[-1]))
        if missing_count:
            ax.text(
                0.02,
                0.02,
                f"omitted (missing property): {missing_count}",
                transform=ax.transAxes,
                fontsize=8,
                color="#607089",
            )

    fig.suptitle("Focused Material Property Curves", fontsize=14, fontweight="semibold")
    fig.legend(
        line_handles.values(),
        line_handles.keys(),
        loc="lower center",
        ncol=4,
        fontsize=8,
        frameon=True,
        bbox_to_anchor=(0.5, -0.01),
    )
    fig.tight_layout(rect=[0, 0.06, 1, 0.95])
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
