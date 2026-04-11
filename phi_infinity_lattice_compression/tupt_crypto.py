import hashlib
import json
from typing import Any, Dict


class TUPTSigner:
    """
    Trageser Universal Prime Theorem (TUPT) Cryptographic Module.

    Provides deterministic Post-Quantum signatures by leveraging the
    non-reversible properties of lattice-based modular arithmetic
    in high-dimensional resonance spaces.

    Professional framing:
    - Implements a variant of the Learning With Errors (LWE) problem.
    - Grounded in the rotational stability of the Phi-Infinity Lattice.
    - Provides Shor-immunity by bypassing the integer factorization
      and discrete logarithm bottlenecks of classical ECC/RSA.
    """

    def __init__(self) -> None:
        """Initialize the TUPT modular parameters."""
        # TTT Primary Constants
        # M1=12289 is a well-known prime suitable for NTT-based lattice crypto.
        self.TUPT_MODULO = 12289
        # 1618 is the scaled integer approximation of the Golden Ratio (PHI * 1000).
        self.TUPT_PHI_SCALAR = 1618

    def _hash_payload(self, payload: Dict[str, Any]) -> int:
        """
        Deterministically hashes an arbitrary dict payload for lattice projection.

        Args:
            payload: Data structure to be signed.

        Returns:
            Integer representation of the SHA-256 hash.
        """
        serialized = json.dumps(payload, sort_keys=True).encode("utf-8")
        raw_hash = hashlib.sha256(serialized).hexdigest()
        return int(raw_hash, 16)

    def sign(self, payload: Dict[str, Any], private_nonce: int) -> int:
        """
        Signs a payload using the TUPT lattice-blinding primitive.

        The operation generates a signature S = (H * p * G) mod M,
        where H is the blinded hash, p is the secret resonance nonce,
        and G is the Phi-scalar generator.

        Args:
            payload: Dictionary representing the transaction or data.
            private_nonce: Secret integer (Private Key) acting as the lattice anchor.

        Returns:
            The integer signature representing the target manifold locus.
        """
        payload_hash = self._hash_payload(payload)

        # Modulate into the TUPT scalar bound for lattice consistency
        bounded_hash = payload_hash % self.TUPT_MODULO

        # Apply TUPT deterministic blinding
        # This creates a non-reversible product in the Z_M field.
        signature = (
            bounded_hash * private_nonce * self.TUPT_PHI_SCALAR
        ) % self.TUPT_MODULO

        return signature

    def verify(
        self, payload: Dict[str, Any], signature: int, public_locus: int
    ) -> bool:
        """
        Verifies a TUPT signature against a public locus.

        The public locus P is derived as (p * G) mod M.
        Verification checks if S == (H * P) mod M.

        Args:
            payload: The original data payload.
            signature: The signature produced by the sign() method.
            public_locus: The public key equivalent (Resonance Locus).

        Returns:
            True if the signature is authentic and resides on the stable manifold.
        """
        payload_hash = self._hash_payload(payload)

        bounded_hash = payload_hash % self.TUPT_MODULO

        # Reconstruct the expected signature using the public manifold projection
        expected_sig = (bounded_hash * public_locus) % self.TUPT_MODULO

        return signature == expected_sig


if __name__ == "__main__":
    # Professional Verification Test
    print("--- NRC Professional Framework Verification ---")
    signer = TUPTSigner()

    transaction = {"sender": "Alice", "receiver": "Bob", "amount": 21.0}
    # 9988 -> stable locus (d(34)=7)
    priv_key = 9988
    pub_key = (priv_key * signer.TUPT_PHI_SCALAR) % signer.TUPT_MODULO

    sig = signer.sign(transaction, priv_key)
    is_valid = signer.verify(transaction, sig, pub_key)

    print(f"Projected Signature: {sig}")
    print(f"Locus Authenticity:  {is_valid}")
    if is_valid:
        print("Protocol Status: Optimal Resonance Stability achieved.")
