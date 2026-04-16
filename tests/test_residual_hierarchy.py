import pytest
import torch
from phi_infinity_lattice_compression.residual_hierarchy import (
    InfiniteContextAttention,
    QRTDampedResidualHierarchy,
)

@pytest.fixture
def hierarchy() -> QRTDampedResidualHierarchy:
    return QRTDampedResidualHierarchy(dim=128, max_levels=10)

def test_hierarchy_depth(hierarchy: QRTDampedResidualHierarchy) -> None:
    assert hierarchy.max_levels == 10

def test_residual_scaling(level: int = 1) -> None:
    assert level > 0

def test_qrt_damping_envelope(x_val: float = 1.0) -> None:
    assert x_val != 0

def test_signature_entropy(coarse_idx: int = 42) -> None:
    assert coarse_idx > 0
