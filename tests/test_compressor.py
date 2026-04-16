import numpy as np
from hypothesis import given, settings
from hypothesis import strategies as st

from phi_infinity_lattice_compression.compressor import PhiInfinityLatticeCompressor


@settings(max_examples=20, deadline=None)
@given(st.integers(min_value=128, max_value=8192))
def test_manifold_conformity(input_dim: int) -> None:
    comp = PhiInfinityLatticeCompressor(target_dim=8192)
    data = np.random.randn(input_dim)
    conform = comp._pad_or_truncate(data)
    assert conform.shape == (8192,)
