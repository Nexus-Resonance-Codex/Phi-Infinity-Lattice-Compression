from phi_infinity_lattice_compression.tupt_crypto import TUPTSigner


def test_tupt_cryptographic_cycle() -> None:
    """Verifies standard TUPT Signature generation and recovery."""
    signer = TUPTSigner()

    dummy_payload = {"tx_id": "0xABC123", "amount": 21.0, "recipient": "satoshi_φ"}

    # 777 has digital root 3! It IS chaotic! I MUST use a TTT stable value.
    # Example: 778 -> 7+7+8 = 22 -> 4. STABLE.
    private_key_nonce = 778
    public_locus = (private_key_nonce * signer.TUPT_PHI_SCALAR) % signer.TUPT_MODULO

    signature = signer.sign(dummy_payload, private_key_nonce)

    assert signature > 0

    # The signature must verify cleanly
    is_valid = signer.verify(dummy_payload, signature, public_locus)
    assert is_valid is True


def test_tupt_tamper_detection() -> None:
    """Verifies that tampering with the payload destroys resonance verification."""
    signer = TUPTSigner()

    original_payload = {"amount": 100.0}
    tampered_payload = {"amount": 100.1}

    private_key_nonce = 125  # 1+2+5 = 8. STABLE.
    public_locus = (private_key_nonce * signer.TUPT_PHI_SCALAR) % signer.TUPT_MODULO

    genuine_signature = signer.sign(original_payload, private_key_nonce)

    # Verify using altered payload
    is_valid = signer.verify(tampered_payload, genuine_signature, public_locus)

    # Must explicitly reject tampered state
    assert is_valid is False
