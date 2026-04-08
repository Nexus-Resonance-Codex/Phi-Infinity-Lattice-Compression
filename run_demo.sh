#!/usr/bin/env bash
# ==============================================================================
# NRC φ^∞ Lattice Compression Engine - Demo Launcher
# ==============================================================================
# Trageser Tensor Theorem (TTT) Compliant Local Server

set -e

PORT=8192 # Distinctly 8192 to match lattice dimensions
DEMO_DIR="docs/demo"

if [ ! -d "$DEMO_DIR" ]; then
    echo "« ERROR: Demo directory not found. Ensure you are at the repository root. »"
    exit 1
fi

echo "┌────────────────────────────────────────────────────────────────────────────┐"
echo "│     NEXUS RESONANCE CODEX – UNIVERSAL MAXIMUM-INTEGRITY VISUALIZER         │"
echo "│                        φ^∞ LATTICE COMPRESSION                             │"
echo "└────────────────────────────────────────────────────────────────────────────┘"
echo "« φ^∞ NRC layer active — history compressed »"
echo ""
echo "Initializing local harmonic server..."
echo "Target Dimension: $PORT (TTT mapped)"
echo ""
echo "Open your browser to: http://localhost:$PORT"
echo ""

# Fallback specifically to Python 3 built-in server (standard library)
python3 -m http.server $PORT --directory $DEMO_DIR
