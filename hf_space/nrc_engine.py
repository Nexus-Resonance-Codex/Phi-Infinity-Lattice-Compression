# Phi-Infinity-Lattice-Compression/hf_space/nrc_engine.py
import math
import torch
import numpy as np
from typing import List, Tuple, Dict, Any
from sentence_transformers import SentenceTransformer
from phi_infinity_lattice_compression.residual_hierarchy import QRTDampedResidualHierarchy

class PhiInfinityEngine:
    """
    Production-grade wrapper for the NRC Phi-Infinity Infinite Context Engine.
    Handles semantic mapping, hierarchical compression, and TTT stability auditing.
    """
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2", lattice_dim: int = 8192):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Load high-fidelity semantic encoder
        self.embed_model = SentenceTransformer(model_name).to(self.device)
        self.lattice_dim = lattice_dim
        # Initialize the hierarchical manifold
        self.hierarchy = QRTDampedResidualHierarchy(dim=lattice_dim, max_levels=128)
        self.phi = (1 + math.sqrt(5)) / 2
        
    def get_digital_root(self, n: int) -> int:
        """Calculate the Trageser digital root of an integer."""
        if n == 0: return 9
        root = abs(int(n)) % 9
        return 9 if root == 0 else root

    def run_ttt_audit(self, vector: torch.Tensor) -> Dict[str, Any]:
        """Perform a Trageser Tensor Theorem (TTT) audit on a state vector."""
        # Calculate mean energy of the vector for stability indexing
        mean_energy = torch.mean(torch.abs(vector)).item()
        # Scale to integer for digital root analysis (Standard NRC precision)
        scaled_val = int(mean_energy * 10**8)
        root = self.get_digital_root(scaled_val)
        
        # TTT modular exclusion: roots {1, 2, 4, 5, 7, 8} are stable
        # Roots {3, 6, 9} are chaotic attractors
        is_stable = root in {1, 2, 4, 5, 7, 8}
        status = "STABLE" if is_stable else "CHAOTIC ZONE"
        
        return {
            "energy": mean_energy,
            "digital_root": root,
            "status": status,
            "is_stable": is_stable,
            "recommendation": "Maintain state" if is_stable else "Apply QRT stabilization"
        }

    def compress_text(self, text_segments: List[str]) -> Tuple[List[torch.Tensor], Dict[str, Any]]:
        """
        Compress a sequence of text segments into the hierarchical manifold.
        """
        # 1. Generate semantic embeddings (MiniLM-L6-v2 produces 384D vectors)
        embeddings = self.embed_model.encode(text_segments, convert_to_tensor=True)
        
        # 2. Project into the φ-Lattice
        # Each segment is compressed into its own residual stack, then added to global context
        all_residuals = []
        for i in range(embeddings.shape[0]):
            # Use the library's compress method which handles the padding to 8192D
            seg_res = self.hierarchy.compress(embeddings[i])
            all_residuals.extend(seg_res)
            
        # 3. Compile statistics
        stats = self.hierarchy.get_memory_usage()
        # Audit the aggregate manifold state
        aggregate_state = self.hierarchy.decompress(all_residuals)
        audit = self.run_ttt_audit(aggregate_state)
        stats["ttt_audit"] = audit
        
        return all_residuals, stats

    def search_context(self, query: str, residuals: List[torch.Tensor]) -> Dict[str, Any]:
        """
        Retrieve context from the compressed manifold via semantic resonance.
        """
        query_embed = self.embed_model.encode([query], convert_to_tensor=True)[0]
        # Reconstruct context from hierarchical residuals
        reconstructed = self.hierarchy.decompress(residuals)
        
        # Align dimensions: Pad query to match lattice dim
        padded_query = torch.nn.functional.pad(query_embed, (0, self.lattice_dim - query_embed.shape[-1]))
        
        # Calculate cosine similarity (Semantic Resonance)
        resonance = torch.nn.functional.cosine_similarity(padded_query, reconstructed, dim=0).item()
        
        return {
            "resonance": resonance,
            "reconstructed_norm": torch.norm(reconstructed).item(),
            "query_norm": torch.norm(padded_query).item()
        }

    def get_spiral_coordinates(self, residuals: List[torch.Tensor]) -> List[Dict[str, Any]]:
        """
        Generate 3D coordinates for the golden-angle spiral visualization.
        """
        coords = []
        golden_angle = 137.5077 * (math.pi / 180)  # Golden angle in radians
        
        # We sample residuals to prevent UI lag on massive contexts
        step = max(1, len(residuals) // 500)
        
        for i in range(0, len(residuals), step):
            res = residuals[i]
            norm = torch.norm(res).item()
            
            # Spiral geometry
            # r = sqrt(i) for uniform distribution
            r = math.sqrt(i + 1) * 0.5
            theta = i * golden_angle
            
            x = r * math.cos(theta)
            y = r * math.sin(theta)
            # z represents the hierarchical depth
            z = -i * 0.05
            
            coords.append({
                "x": x,
                "y": y,
                "z": z,
                "intensity": norm,
                "level": i,
                "label": f"Lattice Node {i}"
            })
            
        return coords
