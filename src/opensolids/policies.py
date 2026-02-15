from __future__ import annotations

from typing import Literal

import numpy as np

Policy = Literal["clamp", "raise", "extrapolate"]
DEFAULT_POLICY: Policy = "clamp"


def validate_policy(policy: str | None) -> Policy:
    if policy is None:
        return DEFAULT_POLICY
    if policy not in {"clamp", "raise", "extrapolate"}:
        raise ValueError(f"Unknown out-of-range policy: {policy}")
    return policy  # type: ignore[return-value]


def apply_temperature_policy(
    T: np.ndarray,
    valid_T_min: float,
    valid_T_max: float,
    policy: Policy,
) -> np.ndarray:
    if policy == "extrapolate":
        return T

    out_of_range = (T < valid_T_min) | (T > valid_T_max)
    if policy == "raise" and np.any(out_of_range):
        tmin = float(np.min(T))
        tmax = float(np.max(T))
        raise ValueError(
            f"Temperature out of range [{valid_T_min}, {valid_T_max}] K: [{tmin}, {tmax}]"
        )

    if policy == "clamp":
        return np.clip(T, valid_T_min, valid_T_max)

    raise AssertionError(f"Unhandled policy: {policy}")
