"""Visualize out-of-range policy behavior for CuCrZr thermal conductivity."""

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



def _ensure_dirs(plot_dir: Path, data_dir: Path) -> None:
    plot_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)



def _write_csv(path: Path, header: list[str], rows: list[list[float]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)



def main() -> None:
    plot_dir = Path("docs/assets/plots")
    data_dir = Path("docs/assets/data")
    _ensure_dirs(plot_dir, data_dir)

    mat = osl.material("cucrzr")
    curve = mat.curve("k")

    temps = np.linspace(200.0, 1200.0, 220)
    k_clamp = np.asarray(mat.k(temps, policy="clamp"), dtype=float)
    k_extrap = np.asarray(mat.k(temps, policy="extrapolate"), dtype=float)

    fig, ax = plt.subplots(figsize=(8.8, 5.2), dpi=150)
    ax.plot(temps, k_clamp, linewidth=2.2, label="clamp")
    ax.plot(temps, k_extrap, linewidth=2.2, linestyle="--", label="extrapolate")

    ax.axvline(curve.valid_T_min, color="gray", linewidth=1.2, alpha=0.75)
    ax.axvline(curve.valid_T_max, color="gray", linewidth=1.2, alpha=0.75)
    ax.text(curve.valid_T_min + 6, np.max(k_extrap) - 8, "valid min", fontsize=9)
    ax.text(curve.valid_T_max + 6, np.max(k_extrap) - 8, "valid max", fontsize=9)

    ax.set_title("Out-of-Range Policy Behavior (CuCrZr k(T))")
    ax.set_xlabel("Temperature [K]")
    ax.set_ylabel("k [W/(m*K)]")
    ax.grid(alpha=0.25)
    ax.legend(frameon=False)
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
