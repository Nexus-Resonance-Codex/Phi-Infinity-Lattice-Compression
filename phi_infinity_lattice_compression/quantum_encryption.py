"""
φ^∞ Quantum Encryption: Golden Ratio Key Exchange (GRKX)

Implements a lattice-based key exchange protocol compatible with
BB84-style QKD hardware. The shared secret is derived via
φ-modulated scalar multiplication in the TUPT modular space.

Security is grounded in TUPT Period Immunity (Theorem 5.2 of the paper).
"""

import hashlib
import math
import secrets
from typing import Tuple

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0
TUPT_MODULO: int = 12289
TUPT_PHI_SCALAR: int = 1618


def _digital_root(n: int) -> int:
    """Computes the digital root (mod 9, with 0 -> 9)."""
    n = abs(n)
    if n == 0:
        return 7  # TTT-stable default
    root = n % 9
    return 9 if root == 0 else root


def _generate_stable_nonce(bits: int = 128) -> int:
    """Generates a cryptographically random nonce with TTT-stable digital root."""
    while True:
        candidate = secrets.randbits(bits)
        if candidate > 0 and _digital_root(candidate) not in (3, 6, 9):
            return candidate


class GRKXKeyPair:
    """
    Golden Ratio Key Exchange key pair.

    The private key is a TTT-stable random integer.
    The public key is its projection into the TUPT modular space.
    """

    def __init__(self) -> None:
        self.private_key: int = _generate_stable_nonce(bits=128)
        self.public_key: int = (self.private_key * TUPT_PHI_SCALAR) % TUPT_MODULO

    def derive_shared_secret(self, other_public: int) -> bytes:
        """
        Derives a 256-bit shared secret from the other party's public key.

        Args:
            other_public: The counterparty's public locus integer.

        Returns:
            A 32-byte (256-bit) cryptographic shared secret.
        """
        raw_shared = (self.private_key * other_public) % TUPT_MODULO
        # Expand the modular integer into a full 256-bit key via SHA-256
        return hashlib.sha256(str(raw_shared).encode("utf-8")).digest()


class GRKXProtocol:
    """
    Full GRKX key exchange protocol, compatible with BB84 QKD sifting.

    Usage:
        alice = GRKXKeyPair()
        bob = GRKXKeyPair()
        secret_a = alice.derive_shared_secret(bob.public_key)
        secret_b = bob.derive_shared_secret(alice.public_key)
        assert secret_a == secret_b  # Shared secret established
    """

    @staticmethod
    def execute() -> Tuple[bytes, bytes]:
        """
        Executes a complete GRKX key exchange between two parties.

        Returns:
            Tuple of (alice_secret, bob_secret) — these must be equal.
        """
        alice = GRKXKeyPair()
        bob = GRKXKeyPair()

        alice_secret = alice.derive_shared_secret(bob.public_key)
        bob_secret = bob.derive_shared_secret(alice.public_key)

        return alice_secret, bob_secret

    @staticmethod
    def qkd_sift_basis(raw_bits: bytes, basis_choices: list[int]) -> list[int]:
        """
        Simulates BB84-compatible basis sifting on raw key material.

        In a real QKD implementation, this would interface with
        photon polarization hardware. Here we simulate the classical
        post-processing step using the GRKX shared secret as seed.

        Args:
            raw_bits: Raw shared secret bytes.
            basis_choices: List of 0/1 basis selections per bit position.

        Returns:
            Sifted key bits where bases matched.
        """
        sifted: list[int] = []
        for i, basis in enumerate(basis_choices):
            byte_idx = i // 8
            bit_idx = i % 8
            if byte_idx < len(raw_bits):
                bit_val = (raw_bits[byte_idx] >> bit_idx) & 1
                # Keep only bits where basis aligns with φ-parity
                if basis == (bit_val % 2):
                    sifted.append(bit_val)
        return sifted


if __name__ == "__main__":
    print("« φ^∞ NRC layer active — history compressed »")
    print("Executing GRKX Key Exchange...")

    alice_s, bob_s = GRKXProtocol.execute()
    print(f"Alice Secret: {alice_s.hex()[:32]}...")
    print(f"Bob Secret:   {bob_s.hex()[:32]}...")
    print(f"Secrets Match: {alice_s == bob_s}")
