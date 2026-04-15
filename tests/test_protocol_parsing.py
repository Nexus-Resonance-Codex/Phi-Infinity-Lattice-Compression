import os

PROMPT_PATH = "/home/jtrag/NRC/github-repos/Nexus-Resonance-Codex/Phi-Infinity-Lattice-Compression/LLM-Infinite-Context-Prompt.md"


def test_protocol_file_exists():
    """Verify the physical presence of the activation protocol."""
    assert os.path.exists(PROMPT_PATH)


def test_activation_markers():
    """Verify that all three mandatory activation markers are present."""
    with open(PROMPT_PATH, "r") as f:
        content = f.read()

    markers = [
        "« φ^∞ NRC layer active — history compressed »",
        "« Codex context lattice engaged »",
        "« 4096D spiral memory online »",
    ]

    for marker in markers:
        assert marker in content


def test_mathematical_definitions_consistency():
    """Verify that the phi constants in the doc match standard precision."""
    with open(PROMPT_PATH, "r") as f:
        lines = f.readlines()

    # Check for φ = (1 + √5)/2 ≈ 1.6180339887498948482
    phi_line_found = False
    for line in lines:
        if "1.6180339887498948482" in line:
            phi_line_found = True
            break
    assert phi_line_found


def test_structure_integrity():
    """Verify header and end-of-protocol tagging."""
    with open(PROMPT_PATH, "r") as f:
        content = f.read()

    assert "# Nexus Resonance Codex" in content
    assert "**End of Protocol Specification**" in content
    assert "### 1. Fundamental Mathematical Definitions" in content
    assert "### 2. φ^∞ Spiral Hierarchical Compression Mechanism" in content
