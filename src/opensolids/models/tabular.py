from __future__ import annotations

import numpy as np
from scipy.interpolate import PchipInterpolator, interp1d


class TabularModel:
    def __init__(self, T: list[float], y: list[float], interpolation: str = "linear"):
        if len(T) != len(y):
            raise ValueError("Tabular T and y must be same length")
        if len(T) < 2:
            raise ValueError("Tabular model requires at least 2 points")

        self.T = np.asarray(T, dtype=float)
        self.y = np.asarray(y, dtype=float)

        if not np.all(np.diff(self.T) > 0):
            raise ValueError("Tabular temperatures must be strictly increasing")

        self.interpolation = interpolation
        self._linear = interp1d(
            self.T,
            self.y,
            kind="linear",
            fill_value="extrapolate",
            assume_sorted=True,
        )
        self._pchip = PchipInterpolator(self.T, self.y, extrapolate=True)

    def evaluate(self, T: np.ndarray) -> np.ndarray:
        if self.interpolation == "linear":
            return np.asarray(self._linear(T), dtype=float)
        if self.interpolation == "pchip":
            return np.asarray(self._pchip(T), dtype=float)
        raise ValueError(f"Unsupported interpolation: {self.interpolation}")
