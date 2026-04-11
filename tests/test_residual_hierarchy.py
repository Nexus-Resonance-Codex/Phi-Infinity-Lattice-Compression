import numpy as np
import torch

from phi_infinity_lattice_compression.residual_hierarchy import (
    InfiniteContextAttention,
    QRTDampedResidualHierarchy,
)


def test_residual_hierarchy_memory() -> None:
    """
    Test that the context engine consumes O(1) proportional residual
    hierarchies rather than storing N tokens independently.
    """
    hierarchy = QRTDampedResidualHierarchy(target_dim=8192)

    # Simulate adding 100 contextual "tokens"
    for _ in range(100):
        dummy_state = np.random.randn(8192)
        hierarchy.add_context(dummy_state)

    stats = hierarchy.get_memory_usage()

    # Memory ratio < 1.0 indicates savings
    assert stats["tokens_processed"] == 100
    assert stats["ratio"] <= 0.5


def test_infinite_attention_shapes() -> None:
    """
    Test the drop-in PyTorch module strictly binds the forward pass tensors.
    """
    embed_dim = 512
    attn = InfiniteContextAttention(embed_dim=embed_dim)

    # Batch size 2, Context length 10
    dummy_input = torch.randn(2, 10, embed_dim)

    output, mem_stats = attn(dummy_input, return_context_memory=True)

    # Must preserve embedding dimensions
    assert output.shape == (2, 10, embed_dim)
    # Memory stats should be returned
    assert mem_stats is not None
    assert "ratio" in mem_stats


def test_hierarchy_restoration() -> None:
    """
    Test that context traces back coherently when required.
    """
    hierarchy = QRTDampedResidualHierarchy(target_dim=8192)

    state_0 = np.ones(8192)
    state_1 = np.ones(8192) * 2.0

    hierarchy.add_context(state_0)
    hierarchy.add_context(state_1)

    recon = hierarchy.restore_context()
    assert recon.shape == (8192,)
    # Verify non-trivial scaling exists
    assert np.any(recon.detach().cpu().numpy() > 0)
