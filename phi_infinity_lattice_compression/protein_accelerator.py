import torch
import torch.nn as nn
from phi_infinity_lattice_compression.compressor import PHI, PHI_INV_SQ, THETA_QRT

class PhiLatticeProteinAccelerator(nn.Module):
    def __init__(self, dim: int = 128):
        super().__init__()
        self.dim = dim
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x * PHI
