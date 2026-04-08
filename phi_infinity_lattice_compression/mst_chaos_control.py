import math

import numpy as np

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0


class MSTChaosController:
    """
    Multi-Scale Tensor (MST) Chaos Controller.

    Implements recurrence modulation to stabilize high-dimensional
    residual sequences. Evaluates whether vectors drift towards
    chaotic attractors (digital roots 3, 6, 9) and applies a non-linear
    recurrence filter to force stabilization into the TTT compliant
    loci (1, 2, 4, 5, 7, 8).
    """

    def __init__(self, target_dim: int = 8192) -> None:
        self.target_dim = target_dim
        # TTT base prime modulos
        self.M1 = 12289
        self.M2 = 24389

    def _digital_root(self, n: int) -> int:
        """Calculates the absolute digital root (base 10) of an integer."""
        n = abs(n)
        if n == 0:
            return 9  # Map absolute zero to the 9 singularity mathematically
        root = n % 9
        return 9 if root == 0 else root

    def check_stability_locus(self, state_vector: np.ndarray) -> bool:  # type: ignore
        """
        Evaluate if the state tensor resides in a stable TTT locus.

        Args:
            state_vector: An 8192-dimensional vector numpy array.

        Returns:
            True if stable (1, 2, 4, 5, 7, 8), False if chaotic (3, 6, 9).
        """
        # Formulate scalar representation via projection
        scalar_rep = int(np.sum(np.abs(state_vector)) * 1000)
        root = self._digital_root(scalar_rep)
        return root not in (3, 6, 9)

    def modulate(self, residual_layer: np.ndarray) -> np.ndarray:  # type: ignore
        """
        Applies MST recurrence formula if the residual drifts into chaos.

        Recurrence map:
        S_{n} = (S_{n_old} * φ) mod (1.0)
        We apply a localized phase-shift based on φ invariant bounds.

        Args:
            residual_layer: Current level's raw residual.

        Returns:
            Modulated (stabilized) residual, preserving Euclidean norm.
        """
        if self.check_stability_locus(residual_layer):
            # Already stable, return identity
            return residual_layer

        # Modulate away from chaotic attractor
        # Phase shift components using modulo 1.0 logic on scaled elements
        phase_shifted = np.mod(residual_layer * PHI, 1.0)

        # Re-normalize to exactly match the original magnitude (lossless norm)
        original_norm = np.linalg.norm(residual_layer)
        shifted_norm = np.linalg.norm(phase_shifted)

        if shifted_norm > 1e-12:
            stabilized = phase_shifted * (original_norm / shifted_norm)
        else:
            stabilized = residual_layer

        return stabilized
