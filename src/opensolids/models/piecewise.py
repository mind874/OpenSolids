from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass
class BranchCondition:
    kind: str
    lower: float | None = None
    upper: float | None = None

    def mask(self, T: np.ndarray) -> np.ndarray:
        if self.kind == "lt":
            assert self.upper is not None
            return T < self.upper
        if self.kind == "le":
            assert self.upper is not None
            return T <= self.upper
        if self.kind == "gt":
            assert self.lower is not None
            return T > self.lower
        if self.kind == "ge":
            assert self.lower is not None
            return T >= self.lower
        if self.kind == "between":
            assert self.lower is not None and self.upper is not None
            return (T >= self.lower) & (T <= self.upper)
        if self.kind == "default":
            return np.ones_like(T, dtype=bool)
        raise ValueError(f"Unsupported piecewise condition kind: {self.kind}")


@dataclass
class PiecewiseBranch:
    condition: BranchCondition
    model: object


class PiecewiseModel:
    def __init__(self, branches: list[PiecewiseBranch]):
        if not branches:
            raise ValueError("Piecewise model requires at least one branch")
        self.branches = branches

    def evaluate(self, T: np.ndarray) -> np.ndarray:
        out = np.full_like(T, np.nan, dtype=float)
        assigned = np.zeros_like(T, dtype=bool)

        for branch in self.branches:
            mask = branch.condition.mask(T) & (~assigned)
            if np.any(mask):
                out[mask] = branch.model.evaluate(T[mask])
                assigned[mask] = True

        if not np.all(assigned):
            raise ValueError("Piecewise model did not assign all input temperatures")

        return out
