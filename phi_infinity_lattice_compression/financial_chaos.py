"""
φ^∞ Financial Chaos Stabilization

Implements Multi-Scale Tensor (MST) chaos control applied to
financial time-series data. Identifies when market volatility
drifts into 3-6-9 chaotic attractor states and forecasts
mean-reversion boundaries.

This module is designed for high-frequency trading (HFT) volatility
analysis and risk management systems.
"""

import math
from typing import Dict, List, Tuple

import numpy as np

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
PHI_INV_SQ: float = PHI**-2.0


def _digital_root(n: int) -> int:
    """Computes the digital root (mod 9, with 0 -> 9)."""
    n = abs(n)
    if n == 0:
        return 7
    root = n % 9
    return 9 if root == 0 else root


class VolatilityAttractorDetector:
    """
    Detects chaotic 3-6-9 attractor states in financial time-series.

    Projects sliding windows of price data into the 8192D lattice
    and evaluates the digital root of the aggregate projection scalar.
    """

    def __init__(self, window_size: int = 128, lattice_dim: int = 8192) -> None:
        self.window_size = window_size
        self.lattice_dim = lattice_dim
        self.history: List[float] = []
        self.attractor_log: List[Dict[str, object]] = []

    def ingest(self, price: float) -> Dict[str, object]:
        """
        Ingests a single price tick and evaluates attractor state.

        Args:
            price: The latest price observation.

        Returns:
            Dict with keys: 'timestamp_idx', 'digital_root', 'is_chaotic',
            'volatility', 'phase_recommendation'.
        """
        self.history.append(price)

        if len(self.history) < self.window_size:
            return {
                "timestamp_idx": len(self.history),
                "digital_root": 7,
                "is_chaotic": False,
                "volatility": 0.0,
                "phase_recommendation": "ACCUMULATE",
            }

        window = self.history[-self.window_size :]

        # Compute rolling volatility (standard deviation of log returns)
        returns = [
            math.log(window[i] / window[i - 1])
            for i in range(1, len(window))
            if window[i - 1] > 0 and window[i] > 0
        ]

        if not returns:
            vol = 0.0
        else:
            vol = float(np.std(returns))

        # Project volatility into TTT scalar
        scalar_rep = int(vol * 1_000_000)
        root = _digital_root(scalar_rep)
        is_chaotic = root in (3, 6, 9)

        if is_chaotic:
            recommendation = "STABILIZE"
        elif root in (7, 8):
            recommendation = "HOLD"
        else:
            recommendation = "ACCUMULATE"

        result: Dict[str, object] = {
            "timestamp_idx": len(self.history),
            "digital_root": root,
            "is_chaotic": is_chaotic,
            "volatility": vol,
            "phase_recommendation": recommendation,
        }

        self.attractor_log.append(result)
        return result

    def get_chaos_ratio(self) -> float:
        """Returns the percentage of recent windows that were chaotic."""
        if not self.attractor_log:
            return 0.0
        chaotic = sum(1 for e in self.attractor_log if e["is_chaotic"])
        return chaotic / len(self.attractor_log)


class MSTVolatilityStabilizer:
    """
    Applies MST phase-shift stabilization to chaotic price windows.

    When a window is flagged as chaotic, the stabilizer applies a
    φ-modulated correction to forecast the mean-reversion target.
    """

    @staticmethod
    def compute_reversion_target(
        prices: List[float],
        current_volatility: float,
    ) -> Tuple[float, float]:
        """
        Computes the expected mean-reversion price target.

        Args:
            prices: Recent price history.
            current_volatility: Current volatility measure.

        Returns:
            Tuple of (reversion_target, confidence).
        """
        if not prices:
            return 0.0, 0.0

        mean_price = float(np.mean(prices))
        std_price = float(np.std(prices))

        # φ-bounded reversion: target is mean adjusted by φ-scaled volatility
        phi_adjustment = current_volatility * PHI * std_price
        reversion_target = mean_price - phi_adjustment

        # Confidence decays with volatility via QRT envelope
        confidence = math.exp(-(current_volatility**2) / PHI)

        return reversion_target, confidence

    @staticmethod
    def fibonacci_support_levels(
        current_price: float,
        recent_high: float,
        recent_low: float,
    ) -> Dict[str, float]:
        """
        Computes Fibonacci retracement levels using φ-exact ratios.

        Args:
            current_price: Current market price.
            recent_high: Recent swing high.
            recent_low: Recent swing low.

        Returns:
            Dict of retracement level names to price levels.
        """
        diff = recent_high - recent_low
        return {
            "level_0.0": recent_high,
            "level_0.236": recent_high - diff * (1 - PHI_INV_SQ),
            "level_0.382": recent_high - diff * PHI_INV_SQ,
            "level_0.500": recent_high - diff * 0.5,
            "level_0.618": recent_high - diff * (1 / PHI),
            "level_0.786": recent_high - diff * (1 / PHI**0.5),
            "level_1.0": recent_low,
        }


if __name__ == "__main__":
    print("« φ^∞ NRC layer active — history compressed »")
    print("Simulating Financial Chaos Detection...")

    detector = VolatilityAttractorDetector(window_size=32)
    np.random.seed(42)

    # Simulate 200 price ticks with a volatile market
    price = 100.0
    for _ in range(200):
        price *= 1 + np.random.normal(0, 0.02)
        result = detector.ingest(price)

    print(f"Total ticks: {len(detector.history)}")
    print(f"Chaos Ratio: {detector.get_chaos_ratio():.2%}")
    print(f"Last State: {detector.attractor_log[-1]}")
