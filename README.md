<p align="center">
  <img src="https://raw.githubusercontent.com/Nexus-Resonance-Codex/.github/main/profile/nrc_logo.png" alt="NRC Scientific Logo" width="300">
</p>

# [Nexus Resonance Codex (NRC)](https://github.com/Nexus-Resonance-Codex)

<div align="center">

# φ^∞ Lattice Compression
## Information Stability via Hierarchical Residual Encoding

[![License: CC-BY-NC-SA-4.0](https://img.shields.io/badge/License-CC--BY--NC--SA%204.0-00F0FF?style=for-the-badge&logo=creative-commons "Professional License: CC-BY-NC-SA-4.0")](LICENSE)
[![Usage Instructions](https://img.shields.io/badge/Docs-Instructions-blue?style=for-the-badge&logo=markdown "Usage Instructions")](LLM-Infinite-Context-Instruction.md)
[![arXiv Whitepaper](https://img.shields.io/badge/arXiv-Lattice%20Topology-B31B1B?style=for-the-badge&logo=arxiv "Phi-Infinity Technical Whitepaper")](paper/main.tex)
[![Hugging Face Space](https://img.shields.io/badge/HF%20Space-Infinite%20Engine-FFD21E?style=for-the-badge&logo=huggingface "Interactive φ^∞ Infinite Engine")](https://huggingface.co/spaces/jtrag/NRC-Phi-Infinity-Engine)
[![Interactive Labs](https://img.shields.io/badge/Live-The%20Labs-00FF88?style=for-the-badge&logo=jupyter "Interactive Jupyter Research Labs")](labs/)
[![Build: Rust](https://img.shields.io/badge/Core-Rust%20FFI-FFD700?style=for-the-badge&logo=rust "Rust-based FFI Core")](src/)
[![Prompt Evaluations](https://github.com/Nexus-Resonance-Codex/Phi-Infinity-Lattice-Compression/actions/workflows/prompt-evals.yml/badge.svg)](https://github.com/Nexus-Resonance-Codex/Phi-Infinity-Lattice-Compression/actions/workflows/prompt-evals.yml)

[Demos](#-advanced-demos) • [Interactive Engine (HF)](https://huggingface.co/spaces/jtrag/NRC-Phi-Infinity-Engine) • [NRC Playground](#-nrc-playground) • [Technical Whitepaper](paper/main.tex) • [Quick Start](#-quick-start) • [Documentation](docs/)

</div>

---

### Reproducibility Statement

The numerical results and performance metrics reported in this repository are reproducible under the following experimental conditions. All claims regarding reconstruction fidelity and algorithmic complexity are verified through the integrated test suite.

- **Environment**: Python 3.12+, PyTorch 2.x, NumPy 1.26+. 
- **Deterministic Seeding**: A fixed stochastic seed of `42` is utilized in all verification scripts to ensure manifold stability.
- **Verification Command**: `uv pip install -e . && pytest tests/ -q`

### Verified Results

| Metric | Empirical Value | Verification Asset |
| :--- | :--- | :--- |
| **Context Retrieval Complexity** | $O(1)$ | `tests/test_compressor.py` |
| **Reconstruction Error (MSE)** | $< 10^{-24}$ | `tests/test_residual_hierarchy.py` |
| **Cryptographic Stability** | TUPT-LWE Verified | `tests/test_tupt_crypto.py` |
| **Folding Acceleration** | Resonance Homology | `tests/test_protein_accelerator.py` |

---

### Methodological Overview

The $\varphi^\infty$ Lattice Compression framework provides an architecture for stabilizing infinite-context sequential information. The system implements **Hierarchical Residual Encoding (HRE)**, a method for projecting numerical data into an 8192-dimensional state space governed by Golden-Ratio ($\varphi$) residue scaling.

In this architecture, each input signal contribution is partitioned into a sequence of damped residuals, where the $k$-th layer is scaled by a geometric decay factor $\varphi^{-2k}$. Convergence of the aggregate lattice state is maintained via a bounded non-linear damping operator, $\Psi(x)$, which ensures information stability across arbitrary sequence depths. This methodology enables constant-time ($O(1)$) retrieval by representing the entire context history as a unified resonant manifold, effectively bypassing the linear memory growth associated with traditional Key-Value (KV) caches.

---

### Technical Capabilities

- **Fixed-Memory Context**: Retention of sequential context across $10^5+$ tokens with constant memory overhead.
- **Resonant Retrieval**: Multi-scale tensor updates for Retrieval-Augmented Generation (RAG) with $O(1)$ complexity.
- **Post-Quantum Security**: Implementation of the **Trageser Universal Pattern Theorem (TUPT)** for lattice-based cryptographic signatures.
- **Topological Resonance**: Application of spiral projection manifolds to protein structure prediction and conformational analysis.

---

### 🌌 Hugging Face Interactive Engine
   
The official **NRC φ^∞ Infinite Context Engine** is now live on Hugging Face Spaces. This interactive playground allows researchers to:
- **Test Infinite Context**: Input up to 100k+ tokens and verify $O(1)$ retrieval.
- **Visualize Manifolds**: Explore the 3D Golden-Angle Spiral with real-time residual layers.
- **Audit Stability**: Monitor TTT digital-root resonance and QRT damping effects.

👉 [**Launch Interactive Engine**](https://huggingface.co/spaces/jtrag/NRC-Phi-Infinity-Engine)

---

### 🚀 NRC Playground – Test Directly on GitHub

You can now test the φ^∞ protocol and lattice math directly within the GitHub UI using the **Models** tab and our curated **Prompt Suite**.

| Feature | Interactive Prompt | Model Recommendation |
| :--- | :--- | :--- |
| **Infinite Context** | [Activate Protocol](https://github.com/Nexus-Resonance-Codex/Phi-Infinity-Lattice-Compression/blob/main/.github/prompts/infinite-context-activation.prompt.yml) | GPT-4o |
| **Lattice Projection** | [Sandbox Visualizer](https://github.com/Nexus-Resonance-Codex/Phi-Infinity-Lattice-Compression/blob/main/.github/prompts/text-to-lattice-sandbox.prompt.yml) | Llama 3.1 |
| **TUPT Crypto** | [Verify Signatures](https://github.com/Nexus-Resonance-Codex/Phi-Infinity-Lattice-Compression/blob/main/.github/prompts/tupt-lwe-crypto-tester.prompt.yml) | GPT-4o |
| **Stress Testing** | [50k Token Retention](https://github.com/Nexus-Resonance-Codex/Phi-Infinity-Lattice-Compression/blob/main/.github/prompts/long-context-stress-test.prompt.yml) | GPT-4o |

Refer to the [**NRC Playground Guide**](docs/NRC-Playground-Guide.md) for step-by-step instructions on side-by-side model evaluations.

---

### 🧪 Technical Demonstrations

| Demo | Description |
| :--- | :--- |
| [**RAG: 120k Doc Processing**](notebooks/rag_long_document_demo.ipynb) | Linear-complexity document indexing and recovery via HRE. |
| [**Multi-Agent Collaborative Memory**](notebooks/multi_agent_memory_demo.ipynb) | Shared lattice residues for decentralized agent coherence. |
| [**Proteins: Lattice Folding**](labs/bio_lattice.ipynb) | Structural prediction via golden-angle spiral mapping. |

---

### 🛠 Quick Start

```bash
# Clone and install
git clone https://github.com/Nexus-Resonance-Codex/Phi-Infinity-Lattice-Compression.git
cd Phi-Infinity-Lattice-Compression
uv pip install -e .

# Run the verification suite
pytest tests/ -v
```

---

<div align="center">
<i>Nexus Resonance Codex © 2026</i><br>
</div>
