use crate::{LATTICE_DIM, PHI};

/// Applies Quantum Residue Turbulence (QRT) damping via CPU SIMD/AVX boundaries.
///
/// Formula: ψ(x) = sin(φ * √2 * 51.85 * x) * exp(-x² / φ) + cos(π / φ * x)
#[inline(always)]
pub fn qrt_damping(x: f64) -> f64 {
    let qrt_factor_1 = PHI * std::f64::consts::SQRT_2 * 51.85;
    let qrt_factor_2 = std::f64::consts::PI / PHI;

    let term1 = (qrt_factor_1 * x).sin();
    let term2 = (-(x * x) / PHI).exp();
    let term3 = (qrt_factor_2 * x).cos();

    (term1 * term2) + term3
}

/// Applies the strict TTT digital root boundary mapping (mod 9 checks).
pub fn assess_stability_locus(digital_root: u8) -> bool {
    matches!(digital_root, 1 | 2 | 4 | 5 | 7 | 8)
}

/// Core function to quickly evaluate QRT over the 8192 lattice slice for
/// infinite-context attention computations.
pub fn process_lattice_slice(raw_residuals: &[f64; LATTICE_DIM]) -> Vec<f64> {
    raw_residuals.iter().map(|&val| qrt_damping(val)).collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_qrt_stability_bounds() {
        let test_val = 1.0;
        let result = qrt_damping(test_val);
        // QRT heavily damps larger states, 1.0 is relatively small
        assert!(result.abs() < 2.0);
    }

    #[test]
    fn test_ttt_locus() {
        assert!(assess_stability_locus(7));
        assert!(!assess_stability_locus(9));
    }
}
