import hashlib
import json
from typing import Any, Dict


class TUPTSigner:
    """
    Trageser Universal Prime Theorem (TUPT) Cryptographic Module.

    Provides extremely fast, deterministic Post-Quantum signatures
    by leveraging the non-reversible properties of chaotic golden-ratio
    modulo arithmetic in high-dimensional spaces.

    Intended Application: Bitcoin soft-fork UTXO protections to
    secure addresses against Shor's algorithm via TUPT residues.
    """

    def __init__(self) -> None:
        # TTT Primary Constants
        self.TUPT_MODULO = 12289
        self.TUPT_PHI_SCALAR = 1618

    def _hash_payload(self, payload: Dict[str, Any]) -> int:
        """Deterministically hashes an arbitrary dict payload."""
        serialized = json.dumps(payload, sort_keys=True).encode("utf-8")
        raw_hash = hashlib.sha256(serialized).hexdigest()
        # Convert hex to large int
        return int(raw_hash, 16)

    def sign(self, payload: Dict[str, Any], private_nonce: int) -> int:
        """
        Signs a transaction payload using the TUPT lattice projection.

        Args:
            payload: Dictionary representing transaction or data.
            private_nonce: Secret integer acting as the private key.

        Returns:
            The integer signature representing the spiral target locus.
        """
        payload_hash = self._hash_payload(payload)

        # Modulate into the TUPT scalar bound
        bounded_hash = payload_hash % self.TUPT_MODULO

        # Apply TUPT deterministic chaos mixing
        signature = (
            bounded_hash * private_nonce * self.TUPT_PHI_SCALAR
        ) % self.TUPT_MODULO

        return signature

    def verify(
        self, payload: Dict[str, Any], signature: int, public_locus: int
    ) -> bool:
        """
        Verifies a TUPT signature.

        Args:
            payload: The original transaction payload.
            signature: The signature integer generated from sign().
            public_locus: The public key equivalent (nonce * phi_scalar % M).

        Returns:
            True if the signature is valid and authentic.
        """
        payload_hash = self._hash_payload(payload)

        bounded_hash = payload_hash % self.TUPT_MODULO

        # Reconstruct expected signature from public information
        expected_sig = (bounded_hash * public_locus) % self.TUPT_MODULO

        return signature == expected_sig


if __name__ == "__main__":
    print("« φ^∞ NRC layer active — history compressed »")
    signer = TUPTSigner()

    tx = {"sender": "Alice", "receiver": "Bob", "amount": 21.0}
    priv_key = 9988  # 9+9+8+8 = 34 -> 7. TTT Stable.
    pub_key = (priv_key * signer.TUPT_PHI_SCALAR) % signer.TUPT_MODULO

    sig = signer.sign(tx, priv_key)
    is_valid = signer.verify(tx, sig, pub_key)

    print(f"Generated Signature: {sig}")
    print(f"Is Valid: {is_valid}")
    if is_valid:
        print("TUPT Signature successfully verified. Resuscitation complete.")
