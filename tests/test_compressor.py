import numpy as np
import pytest
from hypothesis import given, settings
from hypothesis import strategies as st

from phi_infinity_lattice_compression import PhiInfinityLatticeCompressor

# Set seed for determinism in numpy
np.random.seed(42)


def test_compressor_init() -> None:
    """Verifies basic initialization of the lattice geometry."""
    comp = PhiInfinityLatticeCompressor(target_dim=8192, levels=1)
    assert comp.target_dim == 8192
    assert type(comp) is PhiInfinityLatticeCompressor


@settings(max_examples=20, deadline=None)
@given(st.integers(min_value=128, max_value=8192))
def test_dimension_conformity(dim):
    """Verify pad/truncate logic for arbitrary input sizes."""
    comp = PhiInfinityLatticeCompressor(target_dim=8192)
    data = np.random.randn(dim)
    # Access private method for unit testing
    conform = comp._pad_or_truncate(data)
    assert conform.shape == (8192,)
    if dim <= 8192:
        assert np.allclose(conform[:dim], data)
        assert np.all(conform[dim:] == 0)


def test_high_precision_round_trip():
    """
    Verify residual reconstruction with extreme fidelity.
    Target: MSE < 10^{-24} when enough levels are used.
    """
    # Using 128 levels to achieve near-lossless state in 8192D
    comp = PhiInfinityLatticeCompressor(target_dim=1024, levels=64)
    original = np.random.randn(1024) * 0.5

    c_idx, residuals, sig = comp.compress(original)
    reconstructed = comp.decompress(c_idx, residuals, sig)

    mse = np.mean((original - reconstructed) ** 2)
    # Professional requirement: MSE < 1e-24
    assert mse < 1e-24


def test_tupt_integrity_violation():
    """Verify that tampered signatures raise ValueError."""
    comp = PhiInfinityLatticeCompressor(target_dim=512, levels=1)
    data = np.random.randn(512)
    c_idx, res, sig = comp.compress(data)

    with pytest.raises(ValueError, match="Integrity Violation"):
        comp.decompress(c_idx, res, sig + 1)


def test_scaling_stability_256_to_8192():
    """Verify stability across a wide range of manifold projections."""
    for dim in [256, 1024, 4096, 8192]:
        comp = PhiInfinityLatticeCompressor(target_dim=dim, levels=5)
        data = np.random.randn(128)
        c_idx, res, sig = comp.compress(data)
        recon = comp.decompress(c_idx, res, sig)
        assert not np.any(np.isnan(recon))
        assert recon.shape == (dim,)
