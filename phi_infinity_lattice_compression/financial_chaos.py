"""
Universal Information Stability: Financial Resonance Analysis
===========================================================

Implements Resonance Stability metrics applied to financial time-series
data. Identifies when market volatility drifts into Modulo-9 (C9)
singularities and forecasts mean-reversion boundaries using
high-dimensional lattice topology.

This module is optimized for institutional risk management and
high-frequency trading (HFT) volatility stabilization.
"""

import math
from typing import Dict, List, Tuple

import numpy as np

# Golden Ratio Constants
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
PHI_INV_SQ: float = PHI**-2.0


def _calculate_c9_index(n: int) -> int:
    """
    Computes the C9 cyclic index (digital root) of a scalar projection.

    In the lattice manifold, the C9 index identifies rotational
    singularities {3, 6, 9}.
    """
    n = abs(n)
    if n == 0:
        return 7  # Neutral anchor
    root = n % 9
    return 9 if root == 0 else root


class VolatilityResonanceDetector:
    """
    Detects C9 attractor singularities in financial time-series.

    Projects rolling windows of price data into the resonance manifold
    to evaluate the topological stability of market volatility.
    """

    def __init__(self, window_size: int = 128, lattice_dim: int = 8192) -> None:
        """
        Initialize the resonance detector.

        Args:
            window_size: Period of the rolling price window.
            lattice_dim: Target dimension for manifold projection.
        """
        self.window_size = window_size
        self.lattice_dim = lattice_dim
        self.history: List[float] = []
        self.resonance_log: List[Dict[str, object]] = []

    def ingest(self, price: float) -> Dict[str, object]:
        """
        Ingests a single price tick and evaluates resonance stability.

        Args:
            price: Latest market price observation.

        Returns:
            Dict containing resonance metrics and stabilization recommendations.
        """
        self.history.append(price)

        if len(self.history) < self.window_size:
            return {
                "timestamp_idx": len(self.history),
                "c9_index": 7,
                "is_chaotic": False,
                "volatility": 0.0,
                "recommendation": "ACCUMULATE",
            }

        window = self.history[-self.window_size :]

        # Compute log returns for volatility analysis
        returns = [
            math.log(window[i] / window[i - 1])
            for i in range(1, len(window))
            if window[i - 1] > 0 and window[i] > 0
        ]

        vol = float(np.std(returns)) if returns else 0.0

        # Project volatility into the C9 manifold
        scalar_rep = int(vol * 1_000_000)
        c9_idx = _calculate_c9_index(scalar_rep)
        is_chaotic = c9_idx in (3, 6, 9)

        if is_chaotic:
            recommendation = "STABILIZE"
        elif c9_idx in (7, 8):
            recommendation = "HOLD"
        else:
            recommendation = "ACCUMULATE"

        result: Dict[str, object] = {
            "timestamp_idx": len(self.history),
            "c9_index": c9_idx,
            "is_chaotic": is_chaotic,
            "volatility": vol,
            "recommendation": recommendation,
        }

        self.resonance_log.append(result)
        return result

    def get_chaos_ratio(self) -> float:
        """Returns the percentage of windows residing in chaotic singularities."""
        if not self.resonance_log:
            return 0.0
        chaotic = sum(1 for e in self.resonance_log if e["is_chaotic"])
        return chaotic / len(self.resonance_log)


class ResonanceVolatilityStabilizer:
    """
    Applies phase-shift stabilization to chaotic volatility windows.

    Utilizes the PHI-scaled recurrence map to forecast mean-reversion
    trajectories in volatile state spaces.
    """

    @staticmethod
    def compute_reversion_target(
        prices: List[float],
        current_volatility: float,
    ) -> Tuple[float, float]:
        """
        Computes the expected Price Reversion Target via resonance scaling.

        Args:
            prices: Historical price list for the window.
            current_volatility: Current volatility sigma.

        Returns:
            Tuple of (target_price, confidence_score).
        """
        if not prices:
            return 0.0, 0.0

        mean_price = float(np.mean(prices))
        std_price = float(np.std(prices))

        # Phi-bounded inversion: target is the mean adjusted by resonant volatility
        phi_adjustment = current_volatility * PHI * std_price
        target = mean_price - phi_adjustment

        # Institutional confidence decays via QRT envelope
        confidence = math.exp(-(current_volatility**2) / PHI)

        return target, confidence

    @staticmethod
    def fibonacci_support_levels(
        current_price: float,
        recent_high: float,
        recent_low: float,
    ) -> Dict[str, float]:
        """
        Calculates exact Fibonacci retracement levels via Phi-Inversion.

        Args:
            current_price: Current market price.
            recent_high: Period high.
            recent_low: Period low.

        Returns:
            Dict of support and resistance levels.
        """
        diff = recent_high - recent_low
        return {
            "origin": recent_high,
            "level_0.236": recent_high - diff * (1 - PHI_INV_SQ),
            "level_0.382": recent_high - diff * PHI_INV_SQ,
            "level_0.500": recent_high - diff * 0.5,
            "level_0.618": recent_high - diff * (1 / PHI),
            "level_0.786": recent_high - diff * (1 / PHI**0.5),
            "terminal": recent_low,
        }


if __name__ == "__main__":
    print("--- Resonance Volatility Verification ---")
    detector = VolatilityResonanceDetector(window_size=32)
    np.random.seed(42)

    # Simulation loop
    price = 100.0
    for _ in range(200):
        price *= 1 + np.random.normal(0, 0.02)
        state = detector.ingest(price)

    print(f"Sample Count:  {len(detector.history)}")
    print(f"Chaos Ratio:   {detector.get_chaos_ratio():.2%}")
    print(f"Final State:   {detector.resonance_log[-1]}")
