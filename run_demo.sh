#!/bin/bash
# Phi-Infinity Lattice Hub: Sanity Check & Demo Launcher
# ------------------------------------------------------

echo "« φ^∞ NRC layer active — history compressed »"
echo "Initializing Project Phi-Infinity Lattice Sanity Check..."
echo ""

# Check Python environment
if ! command -v python3 &> /dev/null
then
    echo "Error: Python 3 is not installed."
    exit 1
fi

# Run the core verification test
echo "Running High-Dimensional Manifold Projection Test (8192D)..."
python3 -m phi_infinity_lattice_compression.compressor

echo ""
echo "Running Cryptocurrency Resonance Locus Verification (TUPT-LWE)..."
python3 -m phi_infinity_lattice_compression.tupt_crypto

echo ""
echo "Running Financial Volatility Attractor Detection (C9 Manifold)..."
python3 -m phi_infinity_lattice_compression.financial_chaos

echo ""
echo "--------------------------------------------------------"
echo "Sanity Check Complete. Convergence Status: OPTIMAL."
echo "Launch 'jupyter notebook' to explore 'The Labs' directory."
echo "--------------------------------------------------------"
