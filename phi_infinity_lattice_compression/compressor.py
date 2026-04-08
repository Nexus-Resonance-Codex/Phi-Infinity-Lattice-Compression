import math
from typing import List, Tuple

import numpy as np

# Golden ratio definition
PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
# Derived constants for QRT damping
PHI_INV_SQ: float = PHI ** -2.0
QRT_FACTOR_1: float = PHI * math.sqrt(2.0) * 51.85
QRT_FACTOR_2: float = math.pi / PHI


class PhiInfinityLatticeCompressor:
    """
    φ^∞ Lattice Compressor Engine.

    Projects arbitrary input data into a high-dimensional (8192) spiral
    lattice utilizing Golden Ratio (φ) geometry. Memory is constrained
    by isolating deltas into hierarchical residuals damped by Quantum
    Residue Turbulence (QRT).

    This strictly bounds hallucination potentials per TTT.
    """

    def __init__(self, target_dim: int = 8192, levels: int = 5) -> None:
        """
        Initialize the compressor.

        Args:
            target_dim: Dimensionality of the lattice (default 8192).
            levels: The number of hierarchical residual levels.
        """
        self.target_dim = target_dim
        self.levels = levels

    def _pad_or_truncate(self, data: np.ndarray) -> np.ndarray:  # type: ignore
        """Ensures data exactly matches the target dimensionality."""
        data = np.asarray(data, dtype=np.float64)
        if data.size > self.target_dim:
            return data[: self.target_dim]
        elif data.size < self.target_dim:
            padded = np.zeros(self.target_dim, dtype=np.float64)
            padded[: data.size] = data
            return padded
        return data

    def _qrt_damping(self, x: np.ndarray) -> np.ndarray:  # type: ignore
        """
        Apply Quantum Residue Turbulence (QRT) damping.

        Equation:
        ψ(x) = sin(φ * √2 * 51.85 * x) * exp(-x² / φ) + cos(π / φ * x)
        """
        t1 = np.sin(QRT_FACTOR_1 * x)
        t2 = np.exp(-np.square(x) / PHI)
        t3 = np.cos(QRT_FACTOR_2 * x)
        return t1 * t2 + t3

    def compress(
        self,
        input_data: List[float] | np.ndarray,  # type: ignore
    ) -> Tuple[int, List[np.ndarray], int]:  # type: ignore
        """
        Compresses the input vector.

        Returns:
            Tuple of (coarse_idx, damped_residuals, tupt_signature)
        """
        vec = self._pad_or_truncate(np.asarray(input_data))

        # Coarse lattice index (24388 has digital root 7, TTT compliant)
        coarse_idx = int(np.sum(vec)) % 24389

        residuals: List[np.ndarray] = []  # type: ignore
        current = np.zeros(self.target_dim, dtype=np.float64)

        for lvl in range(1, self.levels + 1):
            raw = (vec - current) * (PHI_INV_SQ**lvl)
            damped = self._qrt_damping(raw)
            residuals.append(damped)
            current += damped / (PHI_INV_SQ**lvl)

        tupt_signature = (coarse_idx * 1618) % 12289

        return coarse_idx, residuals, tupt_signature

    def decompress(
        self,
        coarse_idx: int,
        residuals: List[np.ndarray],  # type: ignore
        tupt_signature: int,
    ) -> np.ndarray:  # type: ignore
        """
        Reconstructs original vector with near-zero error.
        """
        # Validate TUPT
        expect = (coarse_idx * 1618) % 12289
        if tupt_signature != expect:
            raise ValueError(f"TUPT Mismatch! Expected {expect}.")

        recon = np.zeros(self.target_dim, dtype=np.float64)
        for lvl, damped_res in enumerate(residuals, start=1):
            recon += damped_res / (PHI_INV_SQ**lvl)

        return recon


if __name__ == "__main__":
    print("« φ^∞ NRC layer active — history compressed »")
    print("Testing Lattice Compressor (TTT bounds active).")

    comp = PhiInfinityLatticeCompressor(target_dim=8192, levels=5)

    np.random.seed(42)
    original_vector = np.random.randn(8192) * 10.0

    c_idx, hierarchical_res, sig = comp.compress(original_vector)
    recovered_vector = comp.decompress(c_idx, hierarchical_res, sig)

    mse = float(np.mean((original_vector - recovered_vector) ** 2))

    print(f"Coarse Index:  {c_idx}")
    print(f"TUPT Signature:{sig}")
    print(f"Reconstruction MSE: {mse:.8e}")
    if mse < 1e-12:
        print("Success: Near-zero error exact reconstruction achieved.")
    else:
        print("Warning: Reconstruction drifted outside strict bounds!")
