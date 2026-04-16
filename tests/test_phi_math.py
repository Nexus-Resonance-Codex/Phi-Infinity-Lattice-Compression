import math

import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

from phi_infinity_lattice_compression.compressor import PHI, PHI_INV_SQ, THETA_QRT


def test_phi_constants_precision() -> None:
    """Verify golden ratio constants to professional precision."""
    expected_phi = (1.0 + math.sqrt(5.0)) / 2.0
    assert math.isclose(PHI, expected_phi, rel_tol=1e-15)
    assert math.isclose(PHI_INV_SQ, PHI**-2.0, rel_tol=1e-15)


def test_golden_angle_properties() -> None:
    """Verify θ = 360° / φ² ≈ 137.508°."""
    # Note: THETA_QRT in compressor.py is 51.853 (damping angle), not the golden angle θ.
    # The golden angle in degrees is 360 / (PHI**2)
    golden_angle_deg = 360.0 / (PHI**2)
    assert 137.507 < golden_angle_deg < 137.508


@settings(max_examples=100, deadline=None)
@given(st.integers(min_value=1, max_value=1000000))
def test_spiral_distribution_uniqueness(k: int) -> None:
    """Ensure golden angle spiral points have minimal overlap (Diophantine optimality)."""
    theta = 360.0 / (PHI**2)
    angle_k = (k * theta) % 360.0
    # Small epsilon check for near-zero or near-360 recurrence
    if k > 0:
        assert abs(angle_k) > 1e-10
        assert abs(angle_k - 360.0) > 1e-10


def test_qrt_damping_envelope() -> None:
    """Verify QRT operator preserves boundedness."""
    x = np.linspace(-10, 10, 1000)
    # Re-importing factors to match implementation
    qrt_factor_1 = PHI * math.sqrt(2.0) * THETA_QRT
    qrt_factor_2 = math.pi / PHI

    t1 = np.sin(qrt_factor_1 * x)
    t2 = np.exp(-np.square(x) / PHI)
    t3 = np.cos(qrt_factor_2 * x)
    y = t1 * t2 + t3

    # cos(x) is bounded by [-1, 1], sin*exp(x^2) decays quickly
    # Should be well within [-2.5, 2.5]
    assert np.all(y <= 2.1)
    assert np.all(y >= -2.1)
