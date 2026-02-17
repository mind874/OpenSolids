"""Plot focused materials by family and export strict coverage/missing-status tables."""

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

PLOT_PROPERTIES: tuple[tuple[str, str, str], ...] = (
    ("k", "W/(m*K)", "Thermal Conductivity"),
    ("diffusivity", "mm^2/s", "Thermal Diffusivity"),
    ("sigma_y", "MPa", "Yield Strength"),
    ("sigma_uts", "MPa", "Ultimate Strength"),
)

COVERAGE_PROPERTIES: tuple[str, ...] = ("k", "cp", "diffusivity", "sigma_y", "sigma_uts", "E")


def _ensure_dirs(plot_dir: Path, data_dir: Path) -> None:
    plot_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)


def _all_material_ids() -> list[str]:
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


def _status_for_property(mat, property_key: str, units: str) -> tuple[str, str, float | None, float | None]:
    available = set(mat.available_properties())
    if property_key not in available:
        return "missing", "property unavailable", None, None

    try:
        valid_t_min, valid_t_max = _property_valid_range(mat, property_key)
    except KeyError:
        return "missing", "no curve/range available", None, None

    if not _is_temperature_varying(mat, property_key, units, valid_t_min, valid_t_max):
        return (
            "single-point-or-constant",
            f"valid range [{valid_t_min:.6g}, {valid_t_max:.6g}] K",
            valid_t_min,
            valid_t_max,
        )

    return "temp-varying", "source-valid varying curve", valid_t_min, valid_t_max


def _short_ids(material_ids: list[str], *, max_items: int = 3) -> str:
    if not material_ids:
        return "-"
    shown = material_ids[:max_items]
    text = ", ".join(shown)
    if len(material_ids) > max_items:
        text += ", ..."
    return text


def _write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


def main() -> None:
    apply_plot_style()

    plot_dir = Path("docs/assets/plots")
    data_dir = Path("docs/assets/data")
    _ensure_dirs(plot_dir, data_dir)

    material_ids = _all_material_ids()
    materials = {material_id: osl.material(material_id) for material_id in material_ids}
    color_map = _material_color_map(material_ids)

    temperatures = np.linspace(173.15, 1000.0, 360)

    fig, axes = plt.subplots(
        len(FAMILY_GROUPS),
        len(PLOT_PROPERTIES),
        figsize=(18.0, 10.8),
        dpi=165,
        squeeze=False,
    )

    legend_handles: dict[str, object] = {}
    status_rows: list[list[object]] = []

    for row_idx, (family_name, family_material_ids) in enumerate(FAMILY_GROUPS):
        for col_idx, (property_key, units, property_title) in enumerate(PLOT_PROPERTIES):
            axis = axes[row_idx][col_idx]
            missing_ids: list[str] = []
            nonvarying_ids: list[str] = []

            for material_id in family_material_ids:
                mat = materials[material_id]
                status, reason, valid_t_min, valid_t_max = _status_for_property(mat, property_key, units)
                status_rows.append(
                    [
                        family_name,
                        material_id,
                        property_key,
                        status,
                        "" if valid_t_min is None else float(valid_t_min),
                        "" if valid_t_max is None else float(valid_t_max),
                        reason,
                    ]
                )

                if status == "missing":
                    missing_ids.append(material_id)
                    continue
                if status != "temp-varying":
                    nonvarying_ids.append(material_id)
                    continue

                assert valid_t_min is not None and valid_t_max is not None
                mask = (temperatures >= valid_t_min) & (temperatures <= valid_t_max)
                if np.count_nonzero(mask) < 2:
                    nonvarying_ids.append(material_id)
                    continue

                t_valid = temperatures[mask]
                y_valid = np.asarray(
                    getattr(mat, property_key)(t_valid, units=units, policy="clamp"),
                    dtype=float,
                )

                line_style = "-" if material_id.endswith("-am") else "--"
                (line,) = axis.plot(
                    t_valid,
                    y_valid,
                    linewidth=2.0,
                    linestyle=line_style,
                    color=color_map[material_id],
                    label=material_id,
                )
                axis.scatter([t_valid[0], t_valid[-1]], [y_valid[0], y_valid[-1]], s=10, color=color_map[material_id], alpha=0.85, zorder=3)

                if material_id not in legend_handles:
                    legend_handles[material_id] = line

            if row_idx == 0:
                axis.set_title(property_title)
            if col_idx == 0:
                axis.set_ylabel(f"{family_name}\n{property_key} [{units}]")
            else:
                axis.set_ylabel(f"{property_key} [{units}]")

            axis.set_xlabel("Temperature [K]")
            axis.set_xlim(float(temperatures[0]), float(temperatures[-1]))

            note_lines = ["Only temperature-varying curves shown"]
            if missing_ids:
                note_lines.append(f"Missing: {_short_ids(missing_ids)}")
            if nonvarying_ids:
                note_lines.append(f"Excluded (non-T-varying): {_short_ids(nonvarying_ids)}")
            axis.text(
                0.02,
                0.02,
                "\n".join(note_lines),
                transform=axis.transAxes,
                fontsize=7.1,
                color="#55627c",
                va="bottom",
                bbox={"boxstyle": "round,pad=0.2", "facecolor": "#ffffff", "edgecolor": "#d5dceb", "alpha": 0.95},
            )

    fig.suptitle("Focused Materials by Family (Temperature-Varying Curves Only)", fontsize=14, fontweight="semibold")
    fig.legend(
        legend_handles.values(),
        legend_handles.keys(),
        loc="lower center",
        ncol=6,
        fontsize=8,
        frameon=True,
        bbox_to_anchor=(0.5, -0.01),
    )
    fig.tight_layout(rect=[0, 0.08, 1, 0.95])

    plot_path = plot_dir / "focus_materials_properties.png"
    fig.savefig(plot_path)
    plt.close(fig)

    coverage_rows: list[list[object]] = []
    missing_rows: list[list[object]] = []

    for material_id in material_ids:
        mat = materials[material_id]
        row: list[object] = [material_id, mat.name]
        for property_key in COVERAGE_PROPERTIES:
            units = "Pa" if property_key in {"sigma_y", "sigma_uts", "E"} else "W/(m*K)"
            if property_key == "cp":
                units = "J/(kg*K)"
            elif property_key == "diffusivity":
                units = "mm^2/s"

            status, reason, valid_t_min, valid_t_max = _status_for_property(mat, property_key, units)
            row.append(status)
            if status != "temp-varying":
                missing_rows.append(
                    [
                        material_id,
                        mat.name,
                        property_key,
                        status,
                        "" if valid_t_min is None else float(valid_t_min),
                        "" if valid_t_max is None else float(valid_t_max),
                        reason,
                    ]
                )
        coverage_rows.append(row)

    coverage_path = data_dir / "focus_materials_coverage.csv"
    _write_csv(
        coverage_path,
        ["material_id", "name", "k", "cp", "diffusivity", "sigma_y", "sigma_uts", "E"],
        coverage_rows,
    )

    missing_path = data_dir / "focus_materials_missing_data.csv"
    _write_csv(
        missing_path,
        ["material_id", "name", "property", "status", "valid_T_min_K", "valid_T_max_K", "reason"],
        missing_rows,
    )

    status_path = data_dir / "focus_material_plot_status.csv"
    _write_csv(
        status_path,
        ["family", "material_id", "property", "status", "valid_T_min_K", "valid_T_max_K", "reason"],
        status_rows,
    )

    print("Generated files:")
    print(f"- {plot_path}")
    print(f"- {coverage_path}")
    print(f"- {missing_path}")
    print(f"- {status_path}")


if __name__ == "__main__":
    main()
