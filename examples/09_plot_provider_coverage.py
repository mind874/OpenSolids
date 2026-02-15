"""Generate provider coverage visuals (material count + property heatmap)."""

from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

import opensolids as osl
from opensolids.registry import default_registry

try:
    import matplotlib.pyplot as plt
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "matplotlib is required for this example. Install with: pip install -e '.[viz]'"
    ) from exc


PROPERTY_KEYS = ["k", "cp", "rho", "E", "nu", "alpha", "eps_th", "sigma_y", "sigma_uts"]



def _ensure_dirs(plot_dir: Path, data_dir: Path) -> None:
    plot_dir.mkdir(parents=True, exist_ok=True)
    data_dir.mkdir(parents=True, exist_ok=True)



def _write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)



def main() -> None:
    plot_dir = Path("docs/assets/plots")
    data_dir = Path("docs/assets/data")
    _ensure_dirs(plot_dir, data_dir)

    reg = default_registry()
    provider_names = reg.list_providers()

    material_counts: dict[str, int] = {}
    coverage = np.zeros((len(provider_names), len(PROPERTY_KEYS)), dtype=float)

    for i, provider_name in enumerate(provider_names):
        provider = reg.providers[provider_name]
        material_ids = provider.list_material_ids()
        material_counts[provider_name] = len(material_ids)

        if not material_ids:
            continue

        for mat_id in material_ids:
            props = set(osl.material(mat_id).available_properties())
            for j, key in enumerate(PROPERTY_KEYS):
                if key in props:
                    coverage[i, j] += 1.0

        coverage[i, :] = 100.0 * coverage[i, :] / len(material_ids)

    # Bar chart: material count by provider.
    fig, ax = plt.subplots(figsize=(8.4, 4.8), dpi=150)
    x = np.arange(len(provider_names))
    y = [material_counts[name] for name in provider_names]
    ax.bar(x, y, width=0.55)
    ax.set_xticks(x, provider_names)
    ax.set_ylabel("Material count")
    ax.set_title("Material Count by Provider")
    ax.grid(axis="y", alpha=0.25)
    fig.tight_layout()

    counts_plot = plot_dir / "provider_material_counts.png"
    fig.savefig(counts_plot)
    plt.close(fig)

    # Heatmap: property coverage percentage by provider.
    fig, ax = plt.subplots(figsize=(10.6, 4.8), dpi=150)
    im = ax.imshow(coverage, aspect="auto", cmap="YlGn", vmin=0.0, vmax=100.0)
    ax.set_xticks(np.arange(len(PROPERTY_KEYS)), PROPERTY_KEYS)
    ax.set_yticks(np.arange(len(provider_names)), provider_names)
    ax.set_title("Property Coverage by Provider (% of materials with property)")

    for i in range(coverage.shape[0]):
        for j in range(coverage.shape[1]):
            ax.text(j, i, f"{coverage[i, j]:.0f}", ha="center", va="center", fontsize=8)

    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Coverage [%]")
    fig.tight_layout()

    heatmap_plot = plot_dir / "provider_property_coverage_heatmap.png"
    fig.savefig(heatmap_plot)
    plt.close(fig)

    counts_csv = data_dir / "provider_material_counts.csv"
    _write_csv(counts_csv, ["provider", "material_count"], [[name, material_counts[name]] for name in provider_names])

    coverage_csv = data_dir / "provider_property_coverage.csv"
    rows: list[list[object]] = []
    for i, provider_name in enumerate(provider_names):
        row: list[object] = [provider_name]
        row.extend(float(v) for v in coverage[i, :])
        rows.append(row)
    _write_csv(coverage_csv, ["provider", *PROPERTY_KEYS], rows)

    print("Generated files:")
    print(f"- {counts_plot}")
    print(f"- {heatmap_plot}")
    print(f"- {counts_csv}")
    print(f"- {coverage_csv}")


if __name__ == "__main__":
    main()
