from __future__ import annotations

import numpy as np


class PolynomialModel:
    def __init__(self, coefficients: list[float]):
        if not coefficients:
            raise ValueError("Polynomial coefficients cannot be empty")
        self.coefficients = np.asarray(coefficients, dtype=float)

    def evaluate(self, T: np.ndarray) -> np.ndarray:
        out = np.zeros_like(T, dtype=float)
        power = np.ones_like(T, dtype=float)
        for a_i in self.coefficients:
            out += a_i * power
            power *= T
        return out
