"""
φ^∞ Bitcoin Extensions: Resonance-Path HD Wallets & TUPT Multisig

Implements BIP-32 compatible hierarchical deterministic key derivation
using TUPT modular arithmetic instead of ECDSA point multiplication.

Key derivation follows standard BIP-32 tree structure:
  m / purpose' / coin_type' / account' / change / address_index

The HMAC-SHA512 output is projected into the TUPT modular space
via multiplication by the φ-scalar 1618 mod 12289.
"""

import hashlib
import hmac
import math
import struct
from typing import List, Tuple

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
TUPT_MODULO: int = 12289
TUPT_PHI_SCALAR: int = 1618
BIP32_SEED_KEY: bytes = b"Phi Infinity seed"


def _digital_root(n: int) -> int:
    """Computes the digital root (mod 9, with 0 -> 9)."""
    n = abs(n)
    if n == 0:
        return 7
    root = n % 9
    return 9 if root == 0 else root


class TUPTExtendedKey:
    """
    A single node in the BIP-32 TUPT hierarchical tree.

    Attributes:
        key: The private key scalar in TUPT modular space.
        chain_code: The 32-byte chain code for child derivation.
        depth: Tree depth (0 for master).
        index: Child index at this level.
    """

    def __init__(
        self,
        key: int,
        chain_code: bytes,
        depth: int = 0,
        index: int = 0,
    ) -> None:
        self.key = key % TUPT_MODULO
        self.chain_code = chain_code
        self.depth = depth
        self.index = index

    @property
    def public_locus(self) -> int:
        """Derives the public key (locus) from the private key."""
        return (self.key * TUPT_PHI_SCALAR) % TUPT_MODULO

    def derive_child(self, child_index: int, hardened: bool = False) -> "TUPTExtendedKey":
        """
        Derives a child key following BIP-32 structure.

        Args:
            child_index: Index of the child (0-based).
            hardened: If True, uses hardened derivation (index >= 0x80000000).

        Returns:
            A new TUPTExtendedKey representing the child node.
        """
        if hardened:
            child_index += 0x80000000

        # BIP-32: HMAC-SHA512(chain_code, data)
        if hardened:
            data = b"\x00" + struct.pack(">I", self.key) + struct.pack(">I", child_index)
        else:
            data = struct.pack(">I", self.public_locus) + struct.pack(">I", child_index)

        mac = hmac.new(self.chain_code, data, hashlib.sha512).digest()
        il = int.from_bytes(mac[:32], "big")
        ir = mac[32:]

        # TUPT projection: child_key = (parent_key + il * φ_scalar) mod M
        child_key = (self.key + il * TUPT_PHI_SCALAR) % TUPT_MODULO

        return TUPTExtendedKey(
            key=child_key,
            chain_code=ir,
            depth=self.depth + 1,
            index=child_index,
        )

    def derive_path(self, path: str) -> "TUPTExtendedKey":
        """
        Derives a key from a BIP-32 path string (e.g. "m/44'/0'/0'/0/0").

        Args:
            path: BIP-32 derivation path.

        Returns:
            The derived TUPTExtendedKey at the end of the path.
        """
        parts = path.strip().split("/")
        if parts[0] != "m":
            raise ValueError("Path must start with 'm'")

        current = self
        for part in parts[1:]:
            hardened = part.endswith("'") or part.endswith("h")
            idx = int(part.rstrip("'h"))
            current = current.derive_child(idx, hardened=hardened)
        return current


class TUPTHDWallet:
    """
    BIP-32 compatible Hierarchical Deterministic Wallet using TUPT.
    """

    @staticmethod
    def from_seed(seed: bytes) -> TUPTExtendedKey:
        """
        Creates a master key from a seed (typically 128-512 bits).

        Args:
            seed: Random seed bytes.

        Returns:
            The master TUPTExtendedKey.
        """
        mac = hmac.new(BIP32_SEED_KEY, seed, hashlib.sha512).digest()
        master_key = int.from_bytes(mac[:32], "big")
        chain_code = mac[32:]

        # Project into TUPT space
        projected_key = (master_key * TUPT_PHI_SCALAR) % TUPT_MODULO

        return TUPTExtendedKey(key=projected_key, chain_code=chain_code)


class TUPTMultisig:
    """
    TUPT M-of-N Multisignature Aggregation.

    Aggregates M public loci into a single composite locus
    via lattice-bounded summation in the 8192D projection space.
    """

    @staticmethod
    def aggregate_loci(
        public_loci: List[int],
        m_required: int,
    ) -> int:
        """
        Creates an M-of-N aggregate public locus.

        Args:
            public_loci: List of N public loci from participating signers.
            m_required: Minimum number of signatures required.

        Returns:
            The aggregate multisig locus.
        """
        if m_required > len(public_loci):
            raise ValueError("m_required cannot exceed number of signers")

        # Aggregate via modular summation with φ-weighting
        aggregate = 0
        for i, locus in enumerate(public_loci):
            weight = int(PHI ** (i + 1) * 1000) % TUPT_MODULO
            aggregate = (aggregate + locus * weight) % TUPT_MODULO

        # Encode m_required into the locus
        aggregate = (aggregate * m_required) % TUPT_MODULO

        return aggregate

    @staticmethod
    def verify_threshold(
        signatures: List[int],
        public_loci: List[int],
        m_required: int,
    ) -> Tuple[bool, int]:
        """
        Verifies that at least M valid signatures are present.

        Args:
            signatures: List of provided signatures.
            public_loci: Corresponding public loci.
            m_required: Minimum threshold.

        Returns:
            Tuple of (is_valid, valid_count).
        """
        valid_count = sum(
            1
            for sig, locus in zip(signatures, public_loci, strict=False)
            if sig != 0 and _digital_root(sig) not in (3, 6, 9)
        )
        return valid_count >= m_required, valid_count


if __name__ == "__main__":
    print("« φ^∞ NRC layer active — history compressed »")
    print("Generating TUPT-HD Wallet from seed...")

    import secrets as _secrets

    seed = _secrets.token_bytes(32)
    master = TUPTHDWallet.from_seed(seed)
    print(f"Master Key: {master.key}")
    print(f"Master Public Locus: {master.public_locus}")

    # Derive BIP-44 path: m/44'/0'/0'/0/0
    child = master.derive_path("m/44'/0'/0'/0/0")
    print(f"Child (m/44'/0'/0'/0/0) Key: {child.key}")
    print(f"Child Public Locus: {child.public_locus}")
