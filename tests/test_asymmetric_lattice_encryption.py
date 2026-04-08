from phi_infinity_lattice_compression.asymmetric_lattice_encryption import (
    AsymmetricLatticeProtocol,
)


def test_asymmetric_shared_secret_agreement() -> None:
    """Alice and Bob must derive identical shared secrets."""
    alice_s, bob_s = AsymmetricLatticeProtocol.execute_exchange()
    assert alice_s == bob_s
    assert len(alice_s) == 32  # 256-bit key


def test_lattice_key_integrity() -> None:
    """All generated private keys must adhere to manifold stability bounds."""
    for _ in range(50):
        kp = AsymmetricLatticeProtocol.generate_keypair()
        # Verify bit length and non-zero initialization
        assert kp.bit_length() >= 256
        assert len(kp.public_key) == 32


def test_basis_sifting_logic() -> None:
    """Protocol sifting must return a valid basis subset."""
    alice_s, bob_s = AsymmetricLatticeProtocol.execute_exchange()
    is_aligned = AsymmetricLatticeProtocol.sift_basis(alice_s, bob_s)
    assert is_aligned is True
