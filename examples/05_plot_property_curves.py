"""Generate family-grouped property-curve visuals and CSV data."""

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


FAMILY_GROUPS: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("Copper Family", ("c101", "c110", "cucrzr-am", "grcop-42-am", "grcop-84-am")),
    ("Aluminum Family", ("alsi10mg-am", "al-6061-am", "al-6061-t6")),
    ("Nickel/Steel Family", ("in718-am", "ss304", "ss316", "ss316-am")),
)

PROPERTY_PLOTS: tuple[tuple[str, str, str, str, str], ...] = (
    ("k", "W/(m*K)", "Thermal Conductivity", "curve_k_regen.png", "k_comparison_regen.csv"),
    ("sigma_y", "MPa", "Yield Strength", "curve_sigma_y_regen.png", "sigma_y_comparison_regen.csv"),
    (
        "diffusivity",
        "mm^2/s",
        "Thermal Diffusivity",
        "curve_diffusivity_selected.png",
        "diffusivity_comparison_selected.csv",
    ),
)


def _ensure_dirs(plot_dir: Path, data_dir: Path) -> None:
    plot_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)


def _ordered_material_ids() -> list[str]:
    out: list[str] = []
    for _, material_ids in FAMILY_GROUPS:
        for material_id in material_ids:
            if material_id not in out:
                out.append(material_id)
    return out


def _material_color_map(material_ids: list[str]) -> dict[str, str]:
    cmap = plt.get_cmap("tab20")
    out: dict[str, str] = {}
    for idx, material_id in enumerate(material_ids):
        out[material_id] = color_for_label(material_id, fallback=cmap(idx % 20))
    return out


def _property_valid_range(mat, property_key: str) -> tuple[float, float]:
    if property_key != "diffusivity":
        curve = mat.curve(property_key)
        return curve.valid_T_min, curve.valid_T_max

    try:
        curve = mat.curve("diffusivity")
        return curve.valid_T_min, curve.valid_T_max
    except KeyError:
        components = [mat.curve("k"), mat.curve("cp")]
        if "rho" in set(mat.available_properties()):
            components.append(mat.curve("rho"))
        return (
            max(curve.valid_T_min for curve in components),
            min(curve.valid_T_max for curve in components),
        )


def _is_temperature_varying(mat, property_key: str, units: str, t_min: float, t_max: float) -> bool:
    if t_max - t_min <= 1e-9:
        return False
    y0 = float(getattr(mat, property_key)(t_min, units=units, policy="clamp"))
    y1 = float(getattr(mat, property_key)(t_max, units=units, policy="clamp"))
    scale = max(1.0, abs(y0), abs(y1))
    return abs(y1 - y0) > 1e-6 * scale


def _temperature_grid(property_key: str) -> np.ndarray:
    if property_key == "diffusivity":
        return np.linspace(173.15, 1000.0, 320)
    return np.linspace(173.15, 1000.0, 320)


def _write_wide_csv(path: Path, temperatures: np.ndarray, material_order: list[str], values_map: dict[str, np.ndarray]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["T_K", *material_order])
        for idx, temp in enumerate(temperatures):
            row: list[object] = [float(temp)]
            for material_id in material_order:
                value = float(values_map[material_id][idx])
                row.append("" if np.isnan(value) else value)
            writer.writerow(row)


def _short_ids(material_ids: list[str], *, max_items: int = 4) -> str:
    if not material_ids:
        return "-"
    shown = material_ids[:max_items]
    text = ", ".join(shown)
    if len(material_ids) > max_items:
        text += ", ..."
    return text


def _plot_property_figure(
    *,
    property_key: str,
    units: str,
    title: str,
    plot_path: Path,
    csv_path: Path,
    materials: dict[str, object],
    color_map: dict[str, str],
) -> tuple[Path, Path, list[list[str]]]:
    temperatures = _temperature_grid(property_key)
    material_order = _ordered_material_ids()
    values_map = {material_id: np.full_like(temperatures, np.nan, dtype=float) for material_id in material_order}

    fig, axes = plt.subplots(1, 3, figsize=(15.8, 5.4), dpi=165)
    handles: dict[str, object] = {}
    exclusion_rows: list[list[str]] = []

    for axis, (family_name, family_material_ids) in zip(axes, FAMILY_GROUPS):
        missing_ids: list[str] = []
        nonvarying_ids: list[str] = []

        for material_id in family_material_ids:
            mat = materials[material_id]
            available = set(mat.available_properties())
            if property_key not in available:
                missing_ids.append(material_id)
                exclusion_rows.append([property_key, family_name, material_id, "missing", "property unavailable"])
                continue

            try:
                valid_t_min, valid_t_max = _property_valid_range(mat, property_key)
            except KeyError:
                missing_ids.append(material_id)
                exclusion_rows.append([property_key, family_name, material_id, "missing", "no curve/range available"])
                continue

            if not _is_temperature_varying(mat, property_key, units, valid_t_min, valid_t_max):
                nonvarying_ids.append(material_id)
                exclusion_rows.append(
                    [
                        property_key,
                        family_name,
                        material_id,
                        "single-point-or-constant",
                        f"valid range [{valid_t_min:.6g}, {valid_t_max:.6g}] K",
                    ]
                )
                continue

            mask = (temperatures >= valid_t_min) & (temperatures <= valid_t_max)
            if np.count_nonzero(mask) < 2:
                nonvarying_ids.append(material_id)
                exclusion_rows.append(
                    [
                        property_key,
                        family_name,
                        material_id,
                        "single-point-or-constant",
                        "insufficient in-range temperature samples",
                    ]
                )
                continue

            t_valid = temperatures[mask]
            y_valid = np.asarray(
                getattr(mat, property_key)(t_valid, units=units, policy="clamp"),
                dtype=float,
            )
            values_map[material_id][mask] = y_valid

            line_style = "-" if material_id.endswith("-am") else "--"
            label = material_id
            (line,) = axis.plot(
                t_valid,
                y_valid,
                linewidth=2.1,
                linestyle=line_style,
                color=color_map[material_id],
                label=label,
            )
            axis.scatter([t_valid[0], t_valid[-1]], [y_valid[0], y_valid[-1]], s=12, color=color_map[material_id], alpha=0.85, zorder=3)
            if label not in handles:
                handles[label] = line

        axis.set_title(family_name)
        axis.set_xlabel("Temperature [K]")
        axis.set_ylabel(f"{property_key} [{units}]")
        axis.set_xlim(float(temperatures[0]), float(temperatures[-1]))

        note_lines = ["Only temperature-varying curves are plotted"]
        if missing_ids:
            note_lines.append(f"Missing: {_short_ids(missing_ids)}")
        if nonvarying_ids:
            note_lines.append(f"Excluded (non-T-varying): {_short_ids(nonvarying_ids)}")

        axis.text(
            0.02,
            0.02,
            "\n".join(note_lines),
            transform=axis.transAxes,
            fontsize=7.5,
            color="#55627c",
            va="bottom",
            bbox={"boxstyle": "round,pad=0.22", "facecolor": "#ffffff", "edgecolor": "#d5dceb", "alpha": 0.95},
        )

    fig.suptitle(f"{title} by Material Family", fontsize=14, fontweight="semibold")
    if handles:
        fig.legend(
            handles.values(),
            handles.keys(),
            loc="lower center",
            ncol=6,
            fontsize=8,
            frameon=True,
            bbox_to_anchor=(0.5, -0.01),
        )
    fig.tight_layout(rect=[0, 0.08, 1, 0.94])
    fig.savefig(plot_path)
    plt.close(fig)

    _write_wide_csv(csv_path, temperatures, material_order, values_map)
    return plot_path, csv_path, exclusion_rows


def main() -> None:
    apply_plot_style()

    plot_dir = Path("docs/assets/plots")
    data_dir = Path("docs/assets/data")
    _ensure_dirs(plot_dir, data_dir)

    material_ids = _ordered_material_ids()
    materials = {material_id: osl.material(material_id) for material_id in material_ids}
    color_map = _material_color_map(material_ids)

    generated: list[Path] = []
    exclusion_rows: list[list[str]] = []

    for property_key, units, title, plot_name, csv_name in PROPERTY_PLOTS:
        plot_path, csv_path, rows = _plot_property_figure(
            property_key=property_key,
            units=units,
            title=title,
            plot_path=plot_dir / plot_name,
            csv_path=data_dir / csv_name,
            materials=materials,
            color_map=color_map,
        )
        generated.extend([plot_path, csv_path])
        exclusion_rows.extend(rows)

    exclusion_path = data_dir / "plot_exclusions_by_property.csv"
    with exclusion_path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["property", "family", "material_id", "status", "reason"])
        writer.writerows(exclusion_rows)
    generated.append(exclusion_path)

    print("Generated files:")
    for path in generated:
        print(f"- {path}")


if __name__ == "__main__":
    main()
