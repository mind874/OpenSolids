"""Visualize a multi-database workflow for 6061 (NIST + MIL-HDBK-5)."""

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

    nist = osl.material("nist-cryo:aluminum-6061-t6")
    mil = osl.material("mil-hdbk-5:H:al-6061-t6")
    canonical = osl.material("al-6061-t6")

    t_k = np.linspace(20.0, 300.0, 180)
    t_sy = np.linspace(294.0, 533.0, 180)

    k_vals = np.asarray(nist.k(t_k, policy="clamp"), dtype=float)
    sy_vals = np.asarray(mil.sigma_y(t_sy, units="MPa", policy="clamp"), dtype=float)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.2, 4.8), dpi=150)

    ax1.plot(t_k, k_vals, linewidth=2.2, color="#1f77b4")
    ax1.set_title("NIST: 6061-T6 Thermal Conductivity")
    ax1.set_xlabel("Temperature [K]")
    ax1.set_ylabel("k [W/(m*K)]")
    ax1.grid(alpha=0.25)

    ax2.plot(t_sy, sy_vals, linewidth=2.2, color="#d62728")
    ax2.set_title("MIL-HDBK-5: 6061-T6 Yield Strength")
    ax2.set_xlabel("Temperature [K]")
    ax2.set_ylabel("sigma_y [MPa]")
    ax2.grid(alpha=0.25)

    fig.suptitle("Multi-Database Workflow Example: 6061-T6", fontsize=12)
    fig.tight_layout()

    plot_path = plot_dir / "al6061_multidatabase.png"
    fig.savefig(plot_path)
    plt.close(fig)

    k_csv = data_dir / "al6061_nist_k.csv"
    sy_csv = data_dir / "al6061_mil_sigma_y.csv"

    _write_csv(k_csv, ["T_K", "k_W_per_mK"], [[float(t), float(v)] for t, v in zip(t_k, k_vals)])
    _write_csv(sy_csv, ["T_K", "sigma_y_MPa"], [[float(t), float(v)] for t, v in zip(t_sy, sy_vals)])

    t_design = 295.0
    print("Design-point combined query at 295 K:")
    print(f"- k from NIST: {nist.k(t_design, policy='clamp'):.3f} W/(m*K)")
    print(f"- sigma_y from MIL: {mil.sigma_y(t_design, units='MPa', policy='clamp'):.3f} MPa")
    print(
        f"- canonical diffusivity: "
        f"{canonical.diffusivity(t_design, units='mm^2/s', policy='clamp'):.3f} mm^2/s"
    )
    print("Generated files:")
    print(f"- {plot_path}")
    print(f"- {k_csv}")
    print(f"- {sy_csv}")


if __name__ == "__main__":
    main()
