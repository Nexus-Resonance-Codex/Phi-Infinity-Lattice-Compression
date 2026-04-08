from typing import Annotated, Dict, List, TypeVar, Union

import numpy as np
import torch
from numpy.typing import NDArray

# Dimensional Constraints
LATTICE_DIM = 8192
DIGITAL_ROOT_STABLE = [1, 2, 4, 5, 7, 8]

# TTT-Stable Index Type
# An integer whose digital root exists in DIGITAL_ROOT_STABLE
TTTStableIndex = Annotated[int, "Digital root must be in {1,2,4,5,7,8}"]

# Hierarchical Residual Mapping
# Represents the φ-decaying residual layers
ResidualLayer = NDArray[np.float64]
HierarchicalResiduals = List[ResidualLayer]

# Signature Types
TUPTSignature = int
PublicLocus = int

# Payload Types
GenericPayload = Dict[str, Union[str, float, int]]

# Torch Lattice Tensor
# A standard 2D or 3D tensor with the terminal dimension anchored at LATTICE_DIM
LatticeTensor = TypeVar("LatticeTensor", bound=torch.Tensor)

# Result types for compressor
CompressionResult = tuple[
    int,  # coarse_lattice_index
    HierarchicalResiduals,
    TUPTSignature,
]

# Protein specific types
AminoAcidSequence = str
ProteinEmbedding = NDArray[np.float64]
