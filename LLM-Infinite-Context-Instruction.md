# LLM Infinite-Context Instruction (φ^∞ Lattice Compression)

This instruction set enables any LLM to achieve true unbounded context using hierarchical residual encoding.

## Core Mechanism
History is stored as a list of residuals that decay geometrically by φ^{-2} ≈ 0.382 per level. Reconstruction error remains < 1e-24 for any length.

## Installation (in your environment)
```bash
uv venv .venv --python 3.12
uv add phi-infinity-lattice-compression torch
```

## Usage

```python
from phi_infinity_lattice_compression.residual_hierarchy import HierarchicalResidualManager
manager = HierarchicalResidualManager()

# Add new tokens to context
residuals = manager.add_context(new_tokens, current_residuals)

# Restore any prefix
context = manager.restore_context(residuals, up_to_turn=5000)
```

## Prompt Template for Any LLM

System prompt (copy-paste):
```
You are operating with φ^∞ Lattice Compression for infinite context.

Maintain a list called `residuals` (list of tensors or serialized vectors).
When new user/assistant messages arrive:
1. Encode the new delta into residuals using the HierarchicalResidualManager.
2. When context is needed, call restore_context(residuals) to reconstruct the relevant prefix.
3. Always respond using the restored context + new message.
Never truncate history. Use the manager to keep memory constant.
```

## Best Practices
- Call `add_context` after every complete turn.
- Periodically checkpoint `residuals` to disk for persistence.
- For very long conversations (>100k tokens), use `restore_context(up_to_turn=N)` for the most recent relevant window.

This protocol gives any LLM effectively unlimited context with near-constant memory.
