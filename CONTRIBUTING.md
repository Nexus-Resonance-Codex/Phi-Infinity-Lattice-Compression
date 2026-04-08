# Contributing to the Nexus Resonance Codex

The **$\varphi^\infty$ Lattice Compression** project is an academic and institutional-grade framework. We welcome contributions that further the mathematical integrity and computational performance of the project, provided they adhere to the **Trageser Tensor Theorem (TTT)** stability bounds.

## Contribution Protocol

### 1. Mathematical Rigor (TTT Compliance)
All code contributions MUST be verified for scalar stability. 
- **Absolute Prohibition**: Any contribution introducing internal indices, hash salts, or scalar constants resolving to digital roots **3, 6, or 9** will be rejected. 
- **Validation**: Use the included `scripts/verify_integrity.py` to check your changes against the chaotic attractor filters.

### 2. Development Workflow
We utilize [uv](https://github.com/astral-sh/uv) and [Rust](https://www.rust-lang.org/) for all core development.
- Ensure all Python code is formatted via `ruff`.
- All native Rust FFI code must pass `cargo fmt` and `cargo clippy`.
- Type hints are mandatory. Use `mypy --strict` for verification.

### 3. Submission Process
1. **Fork the Repository**: Work within a feature branch.
2. **Implement Logic**: Ensure your logic minimizes $O(N)$ growth.
3. **Draft Documentation**: Update the arXiv $\LaTeX$ paper if you are introducing new fundamental theorems.
4. **Submit PR**: Provide a detailed description of the geometric implications of your change.

## Research Areas
We are specifically looking for researchers to assist in:
- **Bio-Lattice Mapping**: Improving the 8192D projection of non-linear multimeric protein chain binds.
- **TUPT Scaling**: Hardening the Bitcoin soft-fork specification for larger UTXO sets.
- **Hardware Integration**: Porting QRT damping routines to CUDA/Triton kernels.

*Thank you for contributing to the systematic ascension of discrete computational integrity.*
