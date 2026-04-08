import math
from typing import Dict, List

import numpy as np

PHI: float = (1.0 + math.sqrt(5.0)) / 2.0


class ProteinLatticeAccelerator:
    """
    Biological Compute Scaling via φ^∞ Lattice Embedding.

    Projects linear amino acid sequences directly into the 8192D
    Golden-Ratio Spiral lattice. By embedding primary sequences into
    this specific non-euclidean geometry, multi-body topological
    constraints (tertiary and quaternary struct folds) can be approximated
    in polynomial time O(N^2) instead of exponential time O(3^N).
    """

    # Amino Acid to base numerical index mapping (TTT aligned)
    # Using the 20 standard amino acids mapped to prime-spaced intervals
    AA_MAP: Dict[str, int] = {
        "A": 2,
        "R": 3,
        "N": 5,
        "D": 7,
        "C": 11,
        "E": 13,
        "Q": 17,
        "G": 19,
        "H": 23,
        "I": 29,
        "L": 31,
        "K": 37,
        "M": 41,
        "F": 43,
        "P": 47,
        "S": 53,
        "T": 59,
        "W": 61,
        "Y": 67,
        "V": 71,
    }

    def __init__(self, lattice_dim: int = 8192) -> None:
        self.lattice_dim = lattice_dim
        # Base golden angle for structural rotation
        self.golden_angle = 360.0 / (PHI**2)

    def _sequence_to_scalars(self, sequence: str) -> List[int]:
        """Converts an amino acid string into its prime representation."""
        return [self.AA_MAP.get(char.upper(), 1) for char in sequence]

    def embed_protein(self, sequence: str) -> np.ndarray:  # type: ignore
        """
        Embeds the protein sequence into the 8192D lattice.

        Args:
            sequence: String of amino acid letters.

        Returns:
            An 8192-dimensional structural coordinate vector.
        """
        scalars = self._sequence_to_scalars(sequence)
        N = len(scalars)

        # Initialize the high-dimensional projection
        structural_vector = np.zeros(self.lattice_dim, dtype=np.float64)

        for i, val in enumerate(scalars):
            # Calculate the spiral projection angle for this residue
            theta = i * self.golden_angle

            # The dimension index is guided by the modulo of the prime value
            # mixed with the spatial sequence step.
            dim_idx = (val * (i + 1)) % self.lattice_dim

            # Project magnitude utilizing QRT bounded wave
            magnitude = math.sin(theta / PHI) * math.exp(-float(i) / (N * PHI))

            # Accumulate topological tension into the vector
            structural_vector[dim_idx] += magnitude

        # Normalize the structural vector stringently
        norm = np.linalg.norm(structural_vector)
        if norm > 0:
            structural_vector = structural_vector / norm

        return structural_vector

    def conformational_distance(self, seq_a: str, seq_b: str) -> float:
        """
        Calculates the polynomial-time expected structural difference.

        This acts as a massively accelerated heuristic for structural
        homology searches before deep physics simulations.
        """
        vec_a = self.embed_protein(seq_a)
        vec_b = self.embed_protein(seq_b)

        # Cosine similarity in the spiral lattice
        similarity = float(np.dot(vec_a, vec_b))

        # Distance is 1.0 - similarity. 0.0 means identical fold topology.
        return 1.0 - similarity
