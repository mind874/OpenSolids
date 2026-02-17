"""Visualize out-of-range policy behavior for CuCrZr thermal conductivity."""

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



def _ensure_dirs(plot_dir: Path, data_dir: Path) -> None:
    plot_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)



def _write_csv(path: Path, header: list[str], rows: list[list[float]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)



def main() -> None:
    apply_plot_style()

    plot_dir = Path("docs/assets/plots")
    data_dir = Path("docs/assets/data")
    _ensure_dirs(plot_dir, data_dir)

    mat = osl.material("cucrzr")
    curve = mat.curve("k")

    temps = np.linspace(200.0, 1200.0, 220)
    k_clamp = np.asarray(mat.k(temps, policy="clamp"), dtype=float)
    k_extrap = np.asarray(mat.k(temps, policy="extrapolate"), dtype=float)

    fig, ax = plt.subplots(figsize=(9.4, 5.4), dpi=165)
    clamp_color = color_for_label("CuCrZr (AM)", fallback="#00897b")
    extrap_color = "#c2185b"
    ax.plot(temps, k_clamp, linewidth=2.6, color=clamp_color, label="policy='clamp'")
    ax.plot(
        temps,
        k_extrap,
        linewidth=2.3,
        linestyle="--",
        color=extrap_color,
        label="policy='extrapolate'",
    )

    ax.axvspan(curve.valid_T_min, curve.valid_T_max, color="#e9effa", alpha=0.75, zorder=0)
    ax.axvspan(float(temps[0]), curve.valid_T_min, color="#fdeaea", alpha=0.5, zorder=0)
    ax.axvspan(curve.valid_T_max, float(temps[-1]), color="#fdeaea", alpha=0.5, zorder=0)
    ax.axvline(curve.valid_T_min, color="#5b6a84", linewidth=1.2, alpha=0.85)
    ax.axvline(curve.valid_T_max, color="#5b6a84", linewidth=1.2, alpha=0.85)
    label_y = float(np.max(k_extrap)) * 0.965
    ax.text(curve.valid_T_min + 6, label_y, "valid min", fontsize=9, color="#4e5c75")
    ax.text(curve.valid_T_max + 6, label_y, "valid max", fontsize=9, color="#4e5c75")
    ax.text(
        (curve.valid_T_min + curve.valid_T_max) * 0.5 - 94,
        label_y,
        "source-supported range",
        fontsize=9,
        color="#4e5c75",
    )
    ax.scatter([curve.valid_T_min, curve.valid_T_max], [mat.k(curve.valid_T_min), mat.k(curve.valid_T_max)], s=24, color=clamp_color, zorder=4, edgecolors="#ffffff", linewidths=0.9)

    ax.set_title("Out-of-Range Policy Behavior (CuCrZr k(T))")
    ax.set_xlabel("Temperature [K]")
    ax.set_ylabel("k [W/(m*K)]")
    ax.set_xlim(float(temps[0]), float(temps[-1]))
    ax.text(
        0.015,
        0.98,
        "blue band = source-valid range, red bands = out-of-range",
        transform=ax.transAxes,
        va="top",
        fontsize=9,
        color="#55627c",
    )
    ax.legend(loc="upper right")
    fig.tight_layout()

    plot_path = plot_dir / "policy_cucrzr_k.png"
    fig.savefig(plot_path)
    plt.close(fig)

    csv_rows: list[list[float]] = []
    for i, t in enumerate(temps):
        csv_rows.append([float(t), float(k_clamp[i]), float(k_extrap[i])])

    csv_path = data_dir / "policy_cucrzr_k.csv"
    _write_csv(csv_path, ["T_K", "k_clamp_W_per_mK", "k_extrapolate_W_per_mK"], csv_rows)

    print("Generated files:")
    print(f"- {plot_path}")
    print(f"- {csv_path}")

    try:
        mat.k(1200.0, policy="raise")
    except ValueError as exc:
        print("policy='raise' example:")
        print(f"- {exc}")


if __name__ == "__main__":
    main()
