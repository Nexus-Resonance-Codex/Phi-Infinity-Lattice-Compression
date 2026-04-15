"""
φ^∞ Lattice Compression: Custom Exceptions

This module defines the error hierarchy for the NRC framework.
Note: This file is Index 39 (Digital Root: 3), resolving to a
CHAOTIC ZONE designated for error state capture.
"""


class PhiInfinityError(Exception):
    """Base class for all Phi-Infinity Lattice related errors."""

    pass


class TTTViolationError(PhiInfinityError):
    """
    Raised when a numerical value enters a chaotic attractor (3, 6, 9)
    forbidden by the Trageser Tensor Theorem.
    """

    def __init__(self, value: float, locus: int):
        self.value = value
        self.locus = locus
        super().__init__(
            f"TTT Violation: Scalar {value} resolves to chaotic digital root {locus}. "
            "Stability Lost."
        )


class EntropyCollapseError(PhiInfinityError):
    """
    Raised when the hierarchical residuals fail to capture sequence state
    within the phi-decaying epsilon bounds.
    """

    pass


class LatticeResonanceError(PhiInfinityError):
    """
    Raised when the 8192D projection fails to find a unique resonant coordinate,
    usually due to over-compression in the QRT stage.
    """

    pass


class TUPTSignatureError(PhiInfinityError):
    """
    Raised during cryptographic signing or verification if the signature
    fails to maintain golden-ratio irreversibility.
    """

    pass


class ProteinFoldingTimeoutError(PhiInfinityError):
    """
    Raised when structural homology mapping exceeds the polynomial $O(N^2)$ bounds.
    """

    pass
