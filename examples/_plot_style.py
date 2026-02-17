"""Shared plot styling helpers for README-facing visual examples."""

from __future__ import annotations

import matplotlib.pyplot as plt


_COLOR_BY_LABEL = {
    "Al 6061-T6": "#1f78b4",
    "Aluminum 6061": "#1f78b4",
    "CuCrZr (AM)": "#00897b",
    "GRCop-42 (AM)": "#ef6c00",
    "GRCop-84 (AM)": "#e67e22",
    "IN718 (AM entry)": "#d81b60",
    "IN718 (AM)": "#d81b60",
    "SS304": "#3949ab",
    "SS316": "#6d4c41",
}


def apply_plot_style() -> None:
    """Apply a readable, consistent style for documentation plots."""
    plt.style.use("default")
    plt.rcParams.update(
        {
            "figure.facecolor": "#fbfcff",
            "savefig.facecolor": "#fbfcff",
            "axes.facecolor": "#f6f8fc",
            "axes.edgecolor": "#c7cfdf",
            "axes.linewidth": 1.0,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.titlesize": 13,
            "axes.titleweight": "semibold",
            "axes.labelsize": 11,
            "axes.labelweight": "medium",
            "font.size": 10,
            "grid.alpha": 0.35,
            "grid.color": "#c8d0e0",
            "grid.linestyle": "-",
            "grid.linewidth": 0.8,
            "legend.frameon": True,
            "legend.framealpha": 0.95,
            "legend.facecolor": "#ffffff",
            "legend.edgecolor": "#d5dceb",
        }
    )


def color_for_label(label: str, fallback: str = "#1f77b4") -> str:
    return _COLOR_BY_LABEL.get(label, fallback)
