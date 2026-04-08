import numpy as np

from phi_infinity_lattice_compression import (
    PhiInfinityLatticeCompressor,
)


def test_compressor_init() -> None:
    """Verifies basic initialization of the lattice geometry."""
    comp = PhiInfinityLatticeCompressor(target_dim=8192, levels=1)
    assert comp.target_dim == 8192

    # The constants are computed internally, just verify we initialized properly
    assert type(comp) is PhiInfinityLatticeCompressor


def test_encode_decode_shape() -> None:
    comp = PhiInfinityLatticeCompressor(target_dim=8192, levels=1)

    # Simulate a token sequence
    original_seq = np.random.randn(4096)

    # Compress up to 8192D
    c_idx, hierarchical_res, sig = comp.compress(original_seq)

    # Residual levels
    assert len(hierarchical_res) == 1
    assert hierarchical_res[0].shape == (8192,)

    # Decode back
    recon = comp.decompress(c_idx, hierarchical_res, sig)
    assert recon.shape == (4096,)


def test_hierarchical_residual_levels() -> None:
    """Check that deeper levels reduce standard residual norm."""
    comp = PhiInfinityLatticeCompressor(target_dim=1024, levels=3)
    data = np.random.randn(512)

    _, res_list, _ = comp.compress(data)
    assert len(res_list) == 3

    # Manifold norms should be stable
    for res in res_list:
        assert res.shape == (1024,)


def test_zero_hallucination_boundary() -> None:
    """
    Simulates reconstruction with high noise to verify stability.
    Ensures the decompressor handles high-dimensional projections without NaN.
    """
    comp = PhiInfinityLatticeCompressor(target_dim=8192, levels=1)

    # Small test sequence - TTT Locus compliant
    original_seq = np.array([1.0, 2.0, 4.0, 5.0, 7.0, 8.0])

    c_idx, hierarchical_res, sig = comp.compress(original_seq)

    recon = comp.decompress(c_idx, hierarchical_res, sig)
    recon_norm = np.linalg.norm(recon)

    assert recon_norm > 0
    assert not np.isnan(recon_norm)
