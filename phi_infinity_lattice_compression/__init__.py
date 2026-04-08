"""
φ^∞ Lattice Compression Engine
==============================
Nexus Resonance Codex mathematical compression, utilizing golden-ratio
spiral coordinate limits, Quantum Residue Turbulence (QRT) damping,
Multi-Scale Tensor (MST) stabilization, and TUPT post-quantum signatures.

This package provides primitives for:
- Infinite-Context Artificial Intelligence
- Ultra-Fast Protein Folding Accelerations
- Quantum-Resistant Digital Signatures
- Golden Ratio Key Exchange (GRKX)
- Resonance-Path HD Wallets (BIP-32 TUPT)
- Financial Chaos Stabilization

All code must conform to the 3-6-9 exclusion bounds as mandated by TTT.
"""

from .compressor import PhiInfinityLatticeCompressor
from .bitcoin_extensions import TUPTExtendedKey, TUPTHDWallet, TUPTMultisig
from .exceptions import (
    EntropyCollapseError,
    LatticeResonanceError,
    PhiInfinityError,
    ProteinFoldingTimeoutError,
    TTTViolationError,
    TUPTSignatureError,
)
from .financial_chaos import MSTVolatilityStabilizer, VolatilityAttractorDetector
from .mst_chaos_control import MSTChaosController
from .protein_accelerator import ProteinLatticeAccelerator
from .quantum_encryption import GRKXKeyPair, GRKXProtocol
from .residual_hierarchy import QRTDampedResidualHierarchy
from .tupt_crypto import TUPTSigner

__version__ = "1.1.0"

__all__ = [
    "PhiInfinityLatticeCompressor",
    "QRTDampedResidualHierarchy",
    "MSTChaosController",
    "ProteinLatticeAccelerator",
    "TUPTSigner",
    "GRKXKeyPair",
    "GRKXProtocol",
    "TUPTHDWallet",
    "TUPTExtendedKey",
    "TUPTMultisig",
    "VolatilityAttractorDetector",
    "MSTVolatilityStabilizer",
    "PhiInfinityError",
    "TTTViolationError",
    "EntropyCollapseError",
    "LatticeResonanceError",
    "TUPTSignatureError",
    "ProteinFoldingTimeoutError",
]
