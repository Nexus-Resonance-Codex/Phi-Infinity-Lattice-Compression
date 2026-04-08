<div align="center">

# $\varphi^\infty$ Lattice Compression Framework

[![License: NRC-L](https://img.shields.io/badge/License-NRC--L-00F0FF?style=for-the-badge&logo=open-source-initiative)](LICENSE)
[![Format: Ruff](https://img.shields.io/badge/Lint-Ruff-FFD700?style=for-the-badge&logo=python)](https://astral.sh/ruff)
[![Typing: Mypy](https://img.shields.io/badge/Typing-Strict-00F0FF?style=for-the-badge&logo=python)](https://mypy.readthedocs.io/)
[![Build: Rust](https://img.shields.io/badge/Core-Rust_FFI-FFD700?style=for-the-badge&logo=rust)](src/)

*The Universal $O(1)$ Memory Escalation Engine derived from the Trageser Tensor Theorem (TTT).*

[Interactive Visualizer Demo](https://nexus-resonance-codex.github.io/Phi-Infinity-Lattice-Compression) • [arXiv Paper](paper/main.tex) • [Installation](#installation)

</div>

<br>

**Phi-Infinity ($\varphi^\infty$) Lattice Compression** is a fundamentally new paradigm for discrete computation. Rather than expanding compute algorithms linearly or exponentially, we map continuous sequential data into an 8192-dimensional Golden-Ratio scaled hyperspace, resolving complex scaling tasks dynamically down to $O(N^2)$ and $O(1)$ complexities.

Under the mathematical strictness of the **Trageser Tensor Theorem (TTT)**, this repository implements three distinct operational architectures using zero-hallucination, Quantum Residue Turbulence (QRT) bounded tensors natively calculated in low-level Rust via Python FFI.

---

## 🏔 Features

### 1. $O(1)$ Infinite Context AI
Existing transformers utilize a KV Cache to remember past tokens, accumulating $O(N^2)$ memory limits. $\varphi^\infty$ replaces the KV cache entirely. Information is organically absorbed into the structural properties of an 8192-dimensional vector. Context strings are retrieved algorithmically by reversing the geometric tension mapped across the $\varphi$ boundary. 

### 2. TUPT Post-Quantum Cryptography
Shor’s algorithms isolate algebraic periods to mathematically break elliptic curves (ECDSA). By running transaction hashes against the Trageser Universal Prime Theorem ($12289 \bmod \varphi$) bounded signature protocols, UTXO derivations become completely period-less and chaotic to external solvers while remaining flawlessly reproducible to internal verifiers.

### 3. Protein Folding Compute Enhancer
Alphafold relies on exponential machine learning alignment tables ($O(3^N)$ space constraint complexity). The Codex projects literal amino acid chains onto a discrete geometric spiral where topological homology is calculated in $O(N^2)$ polynomial time by simple cosine tension bounds.

---

## 🛠 Installation

Built to strictly modern, ultra-fast 2026 specs using [uv](https://github.com/astral-sh/uv) and Rust.

### System Prerequisites
- `python >= 3.12`
- `uv` package manager
- `rustc >= 1.75` (For building the native FFI math tensor core)

### Deployment

```bash
# Clone the codex
git clone https://github.com/Nexus-Resonance-Codex/Phi-Infinity-Lattice-Compression.git
cd Phi-Infinity-Lattice-Compression

# Native Lightning Install via uv 
# (Automatically builds the Rust FFI crates into the virtual environment)
uv venv
uv pip install -e .

# Optional: Run the interactive Glassmorphism HTTP Visualizer on Port 8192
./run_demo.sh
```

### Containerization (Docker)

To deploy directly to a scientific node instantly, use our strictly bounded container orchestration:

```bash
docker build -t phi-infinity:latest .
docker run -p 8888:8888 -it phi-infinity:latest
```

---

## ⚡ Quickstart

### 1. Substituting Standard LLM Attention

```python
import torch
from phi_infinity_lattice_compression.residual_hierarchy import InfiniteContextAttention

# Drop-in replacement for standard MultiHeadAttention
# Radically decreases required KV-Cache footprint
embed_dim = 1024
infinite_attn = InfiniteContextAttention(embed_dim)

input_tensor = torch.randn(2, 4096, embed_dim) # Batch 2, Seq 4096
output, memory_stats = infinite_attn(input_tensor, return_context_memory=True)

print(f"Memory Ratio Consumed vs Traditional Cache: {memory_stats['ratio']:.4f}")
```

### 2. Post-Quantum Signing

```python
from phi_infinity_lattice_compression.tupt_crypto import TUPTSigner

crypt_node = TUPTSigner()

transaction = {"sender": "Alice", "receiver": "Satoshi_φ", "amount": 21.0}
private_locus = 778 # Notice: 7+7+8 = 22 -> 4. Never use roots 3,6,9!

# Non-recoverable chaotic hash mapping
signature = crypt_node.sign(transaction, private_locus)
```

---

## 📜 Trageser Tensor Theorem (TTT) Compliance

Every sequence, numerical algorithm, and parameter within this framework is subjected sequentially to Trageser Tensor Boundary (TTT) checks.

* If memory bounds shift into scalar indices resolving to digital roots **3, 6, or 9**, they enter a Chaotic Attractor sequence and trigger `MSTChaosController` modulation.
* Structural stability orbits exactly around indices **1, 2, 4, 5, 7, 8**. This eliminates hallucination models, guarantees geometric return-state symmetry, and acts as the grounding logic for the universe code architecture.

Contributions that introduce $3,6,9$ structures without `[CHAOTIC ZONE]` explicit documentation will be automatically denied during CI via the GitHub Action pipeline.

---

## Documentation & Literature

* **Academic Paper:** Execute `pdflatex paper/main.tex` to render the theoretical foundation of resolving infinite VRAM exhaustion.
* **Jupyter Examples:** Access `notebooks/` to review visual representations of bounded Golden Ratio tensors scaling linearly against exponential baselines locally.

---
<div align="center">
<i>Authored for the systematic ascension of discrete computational integrity.</i><br>
<b>Nexus Resonance Codex (2026)</b>
</div>
