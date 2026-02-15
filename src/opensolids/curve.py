from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np

from .models import (
    BranchCondition,
    LogPolynomialModel,
    PiecewiseBranch,
    PiecewiseModel,
    PolynomialModel,
    TabularModel,
)
from .policies import apply_temperature_policy, validate_policy
from .types import SourceRef
from .units import as_array_with_scalar_flag, restore_scalar_if_needed


@dataclass
class PropertyCurve:
    property_key: str
    units: str
    model: Any
    model_type: str
    valid_T_min: float
    valid_T_max: float
    recommended_T_min: float | None
    recommended_T_max: float | None
    source_ref: SourceRef | None
    reference_temperature: float | None = None

    def __call__(self, T, *, policy: str | None = None):
        arr, was_scalar = as_array_with_scalar_flag(T)
        policy_value = validate_policy(policy)
        adjusted = apply_temperature_policy(arr, self.valid_T_min, self.valid_T_max, policy_value)
        values = np.asarray(self.model.evaluate(adjusted), dtype=float)
        return restore_scalar_if_needed(values, was_scalar)



def build_model(model_spec: dict[str, Any]):
    model_type = model_spec.get("type")
    if model_type == "tabular":
        return TabularModel(
            T=model_spec["T"],
            y=model_spec["y"],
            interpolation=model_spec.get("interpolation", "linear"),
        )
    if model_type == "polynomial":
        return PolynomialModel(model_spec["coefficients"])
    if model_type == "log_polynomial":
        return LogPolynomialModel(model_spec["coefficients"])
    if model_type == "piecewise":
        branches: list[PiecewiseBranch] = []
        for branch_spec in model_spec["branches"]:
            cond = branch_spec["condition"]
            condition = BranchCondition(
                kind=cond["kind"],
                lower=cond.get("lower"),
                upper=cond.get("upper"),
            )
            model = build_model(branch_spec["model"])
            branches.append(PiecewiseBranch(condition=condition, model=model))
        return PiecewiseModel(branches)
    raise ValueError(f"Unsupported model type: {model_type}")


def curve_from_record(
    property_key: str,
    curve_record: dict[str, Any],
    source_refs: dict[str, SourceRef],
) -> PropertyCurve:
    model_spec = curve_record["model"]
    source_id = curve_record.get("source_id")
    source_ref = source_refs.get(source_id) if source_id else None

    return PropertyCurve(
        property_key=property_key,
        units=curve_record["units"],
        model=build_model(model_spec),
        model_type=model_spec["type"],
        valid_T_min=float(curve_record["valid_T_min"]),
        valid_T_max=float(curve_record["valid_T_max"]),
        recommended_T_min=(
            float(curve_record["recommended_T_min"])
            if curve_record.get("recommended_T_min") is not None
            else None
        ),
        recommended_T_max=(
            float(curve_record["recommended_T_max"])
            if curve_record.get("recommended_T_max") is not None
            else None
        ),
        source_ref=source_ref,
        reference_temperature=(
            float(curve_record["reference_temperature"])
            if curve_record.get("reference_temperature") is not None
            else None
        ),
    )
