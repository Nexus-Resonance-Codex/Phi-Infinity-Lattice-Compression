"""
φ^∞ Lattice Compression Engine
==============================
Nexus Resonance Codex mathematical compression, utilizing golden-ratio
spiral coordinate limits, Quantum Residue Turbulence (QRT) damping,
Lattice Resonance Stability, and TUPT post-quantum signatures.

This package provides primitives for:
- Infinite-Context Artificial Intelligence
- Ultra-Fast Protein Folding Accelerations
- Quantum-Resistant Digital Signatures (TUPT-LWE)
- Golden Ratio Key Exchange (GRKX)
- Resonance-Path HD Wallets (BIP-32 TUPT)
- Financial Resonance Stabilization

Professional standards:
- Adheres to the Modulo-9 Cyclic Group (C9) stability manifold.
- All primitives are optimized for O(1) and O(N^2) complexity.
"""

from .bitcoin_extensions import TUPTExtendedKey, TUPTHDWallet, TUPTMultisig
from .compressor import PhiInfinityLatticeCompressor
from .exceptions import (
    EntropyCollapseError,
    LatticeResonanceError,
    PhiInfinityError,
    ProteinFoldingTimeoutError,
    TTTViolationError,
    TUPTSignatureError,
)
from .financial_chaos import (
    ResonanceVolatilityStabilizer,
    VolatilityResonanceDetector,
)
from .mst_chaos_control import LatticeResonanceController
from .protein_accelerator import ProteinLatticeAccelerator
from .quantum_encryption import GRKXKeyPair, GRKXProtocol
from .residual_hierarchy import QRTDampedResidualHierarchy
from .tupt_crypto import TUPTSigner

__version__ = "1.2.0"  # Incremented for Professional Refactor

__all__ = [
    "PhiInfinityLatticeCompressor",
    "QRTDampedResidualHierarchy",
    "LatticeResonanceController",
    "ProteinLatticeAccelerator",
    "TUPTSigner",
    "GRKXKeyPair",
    "GRKXProtocol",
    "TUPTHDWallet",
    "TUPTExtendedKey",
    "TUPTMultisig",
    "VolatilityResonanceDetector",
    "ResonanceVolatilityStabilizer",
    "PhiInfinityError",
    "TTTViolationError",
    "EntropyCollapseError",
    "LatticeResonanceError",
    "TUPTSignatureError",
    "ProteinFoldingTimeoutError",
]
