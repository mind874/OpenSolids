import numpy as np
import pytest

from opensolids.curve import curve_from_record


SOURCE_LOOKUP = {}


def test_polynomial_scalar_and_vector_evaluation():
    rec = {
        "units": "Pa",
        "valid_T_min": 0,
        "valid_T_max": 1000,
        "model": {"type": "polynomial", "coefficients": [10.0, 2.0]},
    }
    curve = curve_from_record("E", rec, SOURCE_LOOKUP)

    assert curve(5.0) == pytest.approx(20.0)
    vec = curve(np.array([0.0, 1.0, 2.0]))
    np.testing.assert_allclose(vec, np.array([10.0, 12.0, 14.0]))


def test_log_polynomial_evaluation():
    rec = {
        "units": "W/(m*K)",
        "valid_T_min": 1,
        "valid_T_max": 1000,
        "model": {"type": "log_polynomial", "coefficients": [1.0]},
    }
    curve = curve_from_record("k", rec, SOURCE_LOOKUP)

    assert curve(10.0) == pytest.approx(10.0)


def test_piecewise_evaluation():
    rec = {
        "units": "W/(m*K)",
        "valid_T_min": 0,
        "valid_T_max": 10,
        "model": {
            "type": "piecewise",
            "branches": [
                {
                    "condition": {"kind": "lt", "upper": 5.0},
                    "model": {"type": "polynomial", "coefficients": [1.0]},
                },
                {
                    "condition": {"kind": "ge", "lower": 5.0},
                    "model": {"type": "polynomial", "coefficients": [2.0]},
                },
            ],
        },
    }
    curve = curve_from_record("k", rec, SOURCE_LOOKUP)
    values = curve(np.array([2.0, 5.0, 8.0]))
    np.testing.assert_allclose(values, np.array([1.0, 2.0, 2.0]))


def test_out_of_range_policies():
    rec = {
        "units": "Pa",
        "valid_T_min": 0,
        "valid_T_max": 10,
        "model": {"type": "polynomial", "coefficients": [0.0, 1.0]},
    }
    curve = curve_from_record("E", rec, SOURCE_LOOKUP)

    assert curve(-2.0, policy="clamp") == pytest.approx(0.0)
    assert curve(12.0, policy="clamp") == pytest.approx(10.0)
    assert curve(12.0, policy="extrapolate") == pytest.approx(12.0)

    with pytest.raises(ValueError):
        curve(12.0, policy="raise")
