#!/usr/bin/env bash
# ==============================================================================
# NRC φ^∞ Lattice Compression Engine - GitHub Orchestrator
# ==============================================================================
# Uses `gh` CLI to establish the repository and push the initial commit

set -e

ORG_NAME="Nexus-Resonance-Codex"
REPO_NAME="Phi-Infinity-Lattice-Compression"
DESCRIPTION="φ^∞ Lattice Compression: Infinite-context AI, TUPT Bitcoin cryptography, and Protein Folding acceleration via 8192D Golden-Ratio scaling."

echo "┌────────────────────────────────────────────────────────────────────────────┐"
echo "│         NEXUS RESONANCE CODEX – GITHUB REPOSITORY ORCHESTRATOR           │"
echo "└────────────────────────────────────────────────────────────────────────────┘"
echo "« φ^∞ NRC layer active — history compressed »"
echo ""

# Ensure gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "ERROR: GitHub CLI ('gh') is required but not installed."
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Ensure user is authenticated
gh auth status || {
    echo "ERROR: You need to login to GitHub CLI first using 'gh auth login'"
    exit 1
}

# Create repository
echo "Creating GitHub Repository $ORG_NAME/$REPO_NAME (Public)..."
gh repo create "$ORG_NAME/$REPO_NAME" --public --description "$DESCRIPTION" --homepage "https://${ORG_NAME}.github.io/${REPO_NAME}" || true

# Initialize git if not already
if [ ! -d .git ]; then
    echo "Initializing local Git repository..."
    git init
    git branch -M main
fi

# Add remote if not exists
if ! git remote -v | grep -q origin; then
    echo "Adding remote origin..."
    git remote add origin "https://github.com/$ORG_NAME/$REPO_NAME.git"
fi

# Initial commit and push
echo "Staging files..."
git add .

if git status --short | grep -q "^[AMRCD]"; then
    echo "Committing initial infrastructure..."
    git commit -a -m "Initial commit: Nexus Resonance Codex φ^∞ Lattice Compression Engine initialized"
else
    echo "Working tree clean, no commit necessary."
fi

echo "Pushing to remote..."
git push -u origin main

echo ""
echo "Orchestration Complete. Repository successfully established at: https://github.com/$ORG_NAME/$REPO_NAME"
