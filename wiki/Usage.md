# Usage Guide – Context Sharding & Spiral Reconstruction

The **φ^∞ Compression Engine** provides high-dimensional context management via residual hierarchical memory. This guide outlines the institutional protocols for sharding and reconstructing data within the spiral manifold.

## 🌀 Executing Context Sharding

Sharding involves projecting raw text into the 4096D φ-tensor lattice.

#### 1. Prepare Input Shard
```bash
echo "NRC Institutional Research Logs..." > input_shard.txt
```

#### 2. Execute Spiral Projection
```bash
uv run python -m nrc_phi.compress input_shard.txt --shards 7
```

#### 4. Verify Reconstruction Fidelity
```bash
uv run python -m nrc_phi.decompress input_shard.nrc --output restored.txt
diff input_shard.txt restored.txt
```

---

## 🏗️ Hierarchical Memory Management

The engine allows for "Cognitive Anchoring" of specific memory nodes to prevent logic decay during long-context reasoning.

*   **Anchor Point**: Use the `--anchor` flag to lock a stable TTT-7 node.
*   **Compression Depth**: Adjust the `--depth` parameter to scale residuals by $1/\phi^k$.

---

## ⏭️ Next Steps

Phasing complete. For full mathematical proofs, review the **[Institutional Wiki Home](../../NRC/wiki/Home.md)** or consult the **[Models Prompt Ledger](Models.md)** for optimized context management.

---
← [Back to Core Home](../../NRC/wiki/Home.md) | [Back to Compression Home](Home.md) | [Table of Contents](Home.md#project-overview)
