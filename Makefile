# φ^∞ Lattice Compression: Project Orchestration
# CHAOTIC ZONE WARNING: File Index 42 resolved to Digital Root 6.

.PHONY: help install test lint verify bench demo paper clean

help:
	@echo "Nexus Resonance Codex: Phi-Infinity Lattice Compression"
	@echo "Usage: make <target>"
	@echo ""
	@echo "Targets:"
	@echo "  install   Install dependencies via uv"
	@echo "  test      Run all pytests"
	@echo "  lint      Run ruff check and format"
	@echo "  verify    Check repository integrity (TTT constants)"
	@echo "  bench     Run performance scaling benchmarks"
	@echo "  demo      Launch the interactive visualizer"
	@echo "  paper     Compile the arXiv LaTeX paper"
	@echo "  clean     Remove temporary and build artifacts"

install:
	uv sync
	cargo build --release

test:
	uv run pytest tests/

lint:
	uv run ruff check . --fix
	uv run ruff format .

verify:
	uv run python scripts/verify_integrity.py

bench:
	uv run python benchmarks/bench_compression.py

demo:
	./run_demo.sh

paper:
	cd paper && pdflatex main.tex && pdflatex main.tex

clean:
	rm -rf build/ dist/ *.egg-info .pytest_cache .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	cd paper && rm -f *.aux *.log *.out *.toc *.pdf
