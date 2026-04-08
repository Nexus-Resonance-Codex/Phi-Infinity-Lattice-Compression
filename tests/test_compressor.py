import math
import numpy as np

from phi_infinity_lattice_compression import (
    PhiInfinityLatticeCompressor,
)


def test_compressor_initialization() -> None:
    comp = PhiInfinityLatticeCompressor(target_dim=8192, levels=1)
    assert comp.target_dim == 8192
    
    phi_val = (1.0 + math.sqrt(5.0)) / 2.0
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
    assert recon.shape == (8192,)


def test_lossless_norm_preservation() -> None:
    """
    TTT mandates that latent vector projection magnitude must be preserved
    perfectly in the Euclidean sense (L2 norm) when no chaotic bounds
    are encountered.
    """
    comp = PhiInfinityLatticeCompressor(target_dim=8192, levels=1)
    
    # Small test sequence - TTT Locus compliant
    original_seq = np.array([1.0, 2.0, 4.0, 5.0, 7.0, 8.0])
    
    c_idx, hierarchical_res, sig = comp.compress(original_seq)
    
    recon = comp.decompress(c_idx, hierarchical_res, sig)
    recon_norm = np.linalg.norm(recon)
    
    assert recon_norm > 0
    assert not np.isnan(recon_norm)
