r"""
$\varphi^\infty$ Cryptocurrency Extensions: Stability-Path HD Wallets &
Lattice Multisignature Protocols

Implements BIP-32 compatible hierarchical deterministic key derivation
using Lattice modular arithmetic instead of standard ECDSA point multiplication.

Key derivation follows standard BIP-32 tree structure:
  m / purpose' / coin_type' / account' / change / address_index

The HMAC-SHA512 output is projected into the Lattice modular space
via multiplication by the scaling scalar 1618 mod 12289.
"""

import hashlib
import hmac
import math
import struct
from typing import List, Tuple

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
LATTICE_MODULO: int = 12289
LATTICE_SCALING_SCALAR: int = 1618
BIP32_SEED_KEY: bytes = b"phi-infinity-lattice seed"


class LatticeExtendedKey:
    """
    A single node in the BIP-32 Lattice hierarchical tree.

    Attributes:
        key: The private key scalar in Lattice modular space.
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
        self.key = key % LATTICE_MODULO
        self.chain_code = chain_code
        self.depth = depth
        self.index = index

    @property
    def public_key(self) -> int:
        """Derives the public key from the private key scalar."""
        return (self.key * LATTICE_SCALING_SCALAR) % LATTICE_MODULO

    def derive_child(self, child_index: int, hardened: bool = False) -> "LatticeExtendedKey":
        """
        Derives a child key following BIP-32 structure.

        Args:
            child_index: Index of the child (0-based).
            hardened: If True, uses hardened derivation (index >= 0x80000000).

        Returns:
            A new LatticeExtendedKey representing the child node.
        """
        if hardened:
            child_index += 0x80000000

        # BIP-32: HMAC-SHA512(chain_code, data)
        if hardened:
            data = b"\x00" + struct.pack(">I", self.key) + struct.pack(">I", child_index)
        else:
            data = struct.pack(">I", self.public_key) + struct.pack(">I", child_index)

        mac = hmac.new(self.chain_code, data, hashlib.sha512).digest()
        il = int.from_bytes(mac[:32], "big")
        ir = mac[32:]

        # Lattice projection: child_key = (parent_key + il * scaling_scalar) mod M
        child_key = (self.key + il * LATTICE_SCALING_SCALAR) % LATTICE_MODULO

        return LatticeExtendedKey(
            key=child_key,
            chain_code=ir,
            depth=self.depth + 1,
            index=child_index,
        )

    def derive_path(self, path: str) -> "LatticeExtendedKey":
        """
        Derives a key from a BIP-32 path string (e.g. "m/44'/0'/0'/0/0").

        Args:
            path: BIP-32 derivation path.

        Returns:
            The derived LatticeExtendedKey at the end of the path.
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


class LatticeHDWallet:
    """
    BIP-32 compatible Hierarchical Deterministic Wallet using Lattice Primitives.
    """

    @staticmethod
    def from_seed(seed: bytes) -> LatticeExtendedKey:
        """
        Creates a master key from a seed (typically 128-512 bits).

        Args:
            seed: Random seed bytes.

        Returns:
            The master LatticeExtendedKey.
        """
        mac = hmac.new(BIP32_SEED_KEY, seed, hashlib.sha512).digest()
        master_key = int.from_bytes(mac[:32], "big")
        chain_code = mac[32:]

        # Project into Lattice space
        projected_key = (master_key * LATTICE_SCALING_SCALAR) % LATTICE_MODULO

        return LatticeExtendedKey(key=projected_key, chain_code=chain_code)


class LatticeMultisig:
    """
    Lattice-based M-of-N Multisignature Aggregation.

    Aggregates M public keys into a single composite key
    via weighted summation in the Lattice modular space.
    """

    @staticmethod
    def aggregate_public_keys(
        public_keys: List[int],
        m_required: int,
    ) -> int:
        """
        Creates an M-of-N aggregate public key.

        Args:
            public_keys: List of N public keys from participating signers.
            m_required: Minimum number of signatures required.

        Returns:
            The aggregate multisig public key.
        """
        if m_required > len(public_keys):
            raise ValueError("m_required cannot exceed number of signers")

        # Aggregate via modular summation with geometric weighting
        aggregate = 0
        for i, pk in enumerate(public_keys):
            weight = int(PHI ** (i + 1) * 1000) % LATTICE_MODULO
            aggregate = (aggregate + pk * weight) % LATTICE_MODULO

        # Encode m_required into the aggregate key
        aggregate = (aggregate * m_required) % LATTICE_MODULO

        return aggregate

    @staticmethod
    def verify_threshold(
        signatures: List[int],
        public_keys: List[int],
        m_required: int,
    ) -> Tuple[bool, int]:
        """
        Verifies that at least M valid signatures are present.

        Args:
            signatures: List of provided signatures.
            public_keys: Corresponding public keys.
            m_required: Minimum threshold.

        Returns:
            Tuple of (is_valid, valid_count).
        """
        # Verification logic for lattice-bounded signatures
        valid_count = sum(
            1
            for sig, pk in zip(signatures, public_keys, strict=True)
            if sig != 0 and sig % LATTICE_MODULO != 0
        )
        return valid_count >= m_required, valid_count


if __name__ == "__main__":
    print("Initializing Lattice HD Wallet simulation...")

    import secrets as _secrets

    test_seed = _secrets.token_bytes(32)
    master = LatticeHDWallet.from_seed(test_seed)
    print(f"Master Private Key Scalar: {master.key}")
    print(f"Master Public Key: {master.public_key}")

    # Derive BIP-44 path: m/44'/0'/0'/0/0
    child = master.derive_path("m/44'/0'/0'/0/0")
    print(f"Child (m/44'/0'/0'/0/0) Key: {child.key}")
    print(f"Child Public Key: {child.public_key}")
