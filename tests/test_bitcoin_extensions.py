import secrets

from phi_infinity_lattice_compression.bitcoin_extensions import (
    TUPT_MODULO,
    TUPTHDWallet,
    TUPTMultisig,
)


def test_hd_wallet_deterministic() -> None -> None:
    """Same seed must produce same master key."""
    seed = b"test_seed_for_determinism_12345678"
    master_a = TUPTHDWallet.from_seed(seed)
    master_b = TUPTHDWallet.from_seed(seed)
    assert master_a.key == master_b.key
    assert master_a.chain_code == master_b.chain_code


def test_child_derivation_unique() -> None -> None:
    """Different child indices must produce different keys."""
    seed = secrets.token_bytes(32)
    master = TUPTHDWallet.from_seed(seed)
    child_0 = master.derive_child(0)
    child_1 = master.derive_child(1)
    assert child_0.key != child_1.key


def test_bip32_path_derivation() -> None -> None:
    """BIP-44 path derivation must produce valid keys in TUPT space."""
    seed = secrets.token_bytes(32)
    master = TUPTHDWallet.from_seed(seed)
    child = master.derive_path("m/44'/0'/0'/0/0")
    assert 0 <= child.key < TUPT_MODULO
    assert child.depth == 5


def test_hardened_vs_normal() -> None -> None:
    """Hardened and normal derivation must produce different keys."""
    seed = secrets.token_bytes(32)
    master = TUPTHDWallet.from_seed(seed)
    normal = master.derive_child(0, hardened=False)
    hardened = master.derive_child(0, hardened=True)
    assert normal.key != hardened.key


def test_multisig_aggregate() -> None -> None:
    """Multisig aggregate must produce a valid locus."""
    loci = [1234, 5678, 8888]
    aggregate = TUPTMultisig.aggregate_loci(loci, m_required=2)
    assert 0 <= aggregate < TUPT_MODULO
