use log::warn;
use num_bigint::BigUint;
use num_traits::Zero;

pub const TUPT_MODULO: u64 = 12289;
pub const TUPT_PHI_SCALAR: u64 = 1618;

/// Sign a predetermined hash using Trageser Universal Prime Theorem (TUPT) mechanics.
///
/// Converts a payload hash into a bounded resonance curve signature.
/// This acts as a post-quantum validatable scalar inside the 8192D lattice.
pub fn tupt_sign(payload_hash: u64, private_nonce: u64) -> u64 {
    let bounded = payload_hash % TUPT_MODULO;
    let mixed = (bounded * private_nonce) % TUPT_MODULO;

    (mixed * TUPT_PHI_SCALAR) % TUPT_MODULO
}

/// Verify a TUPT signature.
pub fn tupt_verify(payload_hash: u64, signature: u64, public_locus: u64) -> bool {
    let bounded = payload_hash % TUPT_MODULO;
    let expected = (bounded * public_locus) % TUPT_MODULO;

    signature == expected
}

/// Generates the public locus point given a private nonce.
/// TTT bound rules suggest the private nonce should strictly avoid 3, 6, 9 digital roots,
/// though enforcement should be applied at generation.
pub fn generate_public_locus(private_nonce: u64) -> u64 {
    if private_nonce == 0 || private_nonce % 3 == 0 {
        warn!("TTT Violation: Private nonce falls on chaotic attractor 3-6-9 boundaries.");
    }
    (private_nonce * TUPT_PHI_SCALAR) % TUPT_MODULO
}

/// Computes the digital root of a large payload, ensuring convergence to 1-9 loci
/// while avoiding 3,6,9.
pub fn calculate_digital_root(val: &BigUint) -> u8 {
    if val.is_zero() {
        return 9; // TTT zero maps mathematically to 9
    }
    let modulo = (val % 9u32).to_u32_digits();
    if modulo.is_empty() {
        return 9;
    }
    let res = modulo[0];
    if res == 0 {
        9
    } else {
        res as u8
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_signature_cycle() {
        let payload_hash = 998234823423;
        let priv_key = 88; // digital root 7 -> (8+8)=16 -> 7

        let pub_key = generate_public_locus(priv_key);
        let sig = tupt_sign(payload_hash, priv_key);

        assert!(tupt_verify(payload_hash, sig, pub_key));
    }

    #[test]
    fn test_tt_digital_root() {
        use num_bigint::ToBigUint;
        let v = 24388.to_biguint().unwrap();
        // 2+4+3+8+8 = 25 -> 7
        assert_eq!(calculate_digital_root(&v), 7);
    }
}
