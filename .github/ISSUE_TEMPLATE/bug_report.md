---
name: Bug Report
about: Create a report to help us improve the lattice integrity.
title: "[BUG] - Short Description"
labels: bug, technical-integrity
assignees: ''

---

**1. Observed Deviation**
A clear and concise description of what the bug is, specifically noting if it involves a deviation from expected Golden-Ratio resonant states.

**2. TTT Stability Verification**
Please run `uv run python scripts/verify_integrity.py` and paste the output here.
- Did the failure happen at a specific scalar index?
- What was the digital root of the failing index?

**3. Reproduction Steps**
Steps to reproduce the behavior:
1. Initialize `PhiInfinityLatticeCompressor` with target_dim ...
2. Add context ...
3. Observe `EntropyCollapseError` or similar.

**4. Expected Behavior**
A clear and concise description of what you expected to happen according to the paper mathematics.

**5. Environment Information**
- OS: (e.g., Pop!_OS 24.04)
- CPU Architecture: (e.g., x86_64, aarch64)
- Python Version: (e.g., 3.12.2)
- Rustc Version: (e.g., 1.76)

**6. Additional Context**
Add any other context about the problem here (e.g., screenshot of the visualizer anomaly).
