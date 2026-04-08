/*!
# φ^∞ Lattice Compression Engine - Rust Core

This library provides the ultra-high-performance implementations of the
Trageser Tensor Theorem (TTT) and Quantum Residue Turbulence (QRT) formulas
required for the phi_infinity_lattice_compression Python package.

These perform the lowest-level lattice matrix multiplications and cryptographic
hashes mapped natively directly to CPU registers, stripping away Python's GIL.
*/

pub mod compression;
pub mod crypto;

/// Core mathematical constant for the Nexus Resonance Codex
pub const PHI: f64 = 1.618_033_988_749_895;

/// TTT stable digital roots bounds
pub const STABLE_LOCI: [u8; 6] = [1, 2, 4, 5, 7, 8];

/// Standard 8192-dimensional lattice allocation
pub const LATTICE_DIM: usize = 8192;

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_phi_bound() {
        assert!((PHI - 1.618_033_988_749).abs() < 1e-10);
    }
}
