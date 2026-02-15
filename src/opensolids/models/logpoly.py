from __future__ import annotations

import numpy as np


class LogPolynomialModel:
    def __init__(self, coefficients: list[float]):
        if not coefficients:
            raise ValueError("Log-polynomial coefficients cannot be empty")
        self.coefficients = np.asarray(coefficients, dtype=float)

    def evaluate(self, T: np.ndarray) -> np.ndarray:
        if np.any(T <= 0):
            raise ValueError("Log-polynomial model requires T > 0")
        logT = np.log10(T)
        out = np.zeros_like(logT, dtype=float)
        power = np.ones_like(logT, dtype=float)
        for a_i in self.coefficients:
            out += a_i * power
            power *= logT
        return np.power(10.0, out)
