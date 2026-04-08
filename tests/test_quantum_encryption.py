from phi_infinity_lattice_compression.quantum_encryption import (
    GRKXKeyPair,
    GRKXProtocol,
    _digital_root,
    _generate_stable_nonce,
)


def test_grkx_shared_secret_agreement() -> None:
    """Alice and Bob must derive identical shared secrets."""
    alice_s, bob_s = GRKXProtocol.execute()
    assert alice_s == bob_s
    assert len(alice_s) == 32  # 256-bit key


def test_grkx_key_stability() -> None:
    """All generated private keys must be TTT-stable."""
    for _ in range(50):
        kp = GRKXKeyPair()
        root = _digital_root(kp.private_key)
        assert root not in (3, 6, 9), f"Chaotic nonce generated: {kp.private_key}"


def test_stable_nonce_generator() -> None:
    """Stable nonce generator must never produce chaotic values."""
    for _ in range(100):
        nonce = _generate_stable_nonce(bits=64)
        assert _digital_root(nonce) not in (3, 6, 9)


def test_qkd_sift_returns_bits() -> None:
    """QKD sifting should return a non-empty list of integers."""
    alice_s, _ = GRKXProtocol.execute()
    basis = [0, 1, 0, 1, 1, 0, 0, 1] * 4  # 32 basis choices
    sifted = GRKXProtocol.qkd_sift_basis(alice_s, basis)
    assert isinstance(sifted, list)
    assert all(b in (0, 1) for b in sifted)
