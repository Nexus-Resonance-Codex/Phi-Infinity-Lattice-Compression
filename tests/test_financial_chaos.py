import numpy as np

from phi_infinity_lattice_compression.financial_chaos import (
    ResonanceVolatilityStabilizer,
    VolatilityResonanceDetector,
)


def test_detector_warmup() -> None -> None:
    """Detector should accumulate without error before window fills."""
    detector = VolatilityResonanceDetector(window_size=32)
    for i in range(20):
        result = detector.ingest(100.0 + i * 0.1)
        assert not result["is_chaotic"]


def test_detector_processes_volatile_data() -> None -> None:
    """Detector must produce valid output over volatile price data."""
    detector = VolatilityResonanceDetector(window_size=16)
    np.random.seed(71)

    price = 50.0
    for _ in range(100):
        price *= 1 + np.random.normal(0, 0.05)
        result = detector.ingest(price)
        assert "c9_index" in result
        assert "volatility" in result
        assert result["recommendation"] in ("ACCUMULATE", "HOLD", "STABILIZE")

    ratio = detector.get_chaos_ratio()
    assert 0.0 <= ratio <= 1.0


def test_reversion_target() -> None -> None:
    """Mean-reversion target must be a finite float."""
    prices = [100.0, 102.0, 98.0, 101.0, 99.5]
    target, confidence = ResonanceVolatilityStabilizer.compute_reversion_target(prices, 0.02)
    assert np.isfinite(target)
    assert 0.0 <= confidence <= 1.0


def test_fibonacci_levels() -> None -> None:
    """Fibonacci retracement levels must be ordered."""
    levels = ResonanceVolatilityStabilizer.fibonacci_support_levels(
        current_price=105.0, recent_high=110.0, recent_low=90.0
    )
    assert levels["origin"] == 110.0
    assert levels["terminal"] == 90.0
    assert levels["level_0.500"] == 100.0
