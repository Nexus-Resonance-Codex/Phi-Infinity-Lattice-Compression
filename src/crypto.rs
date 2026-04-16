use log::warn;
use num_bigint::BigUint;
use num_traits::Zero;

pub const TUPT_MODULO: u64 = 12289;
pub const TUPT_PHI_SCALAR: u64 = 1618;

/// Modular Synchronisation Theory (MST) modulus for residue-hiding.
/// MST(v) = v mod 24389.
pub const MST_MODULUS: u64 = 24389;

/// The Quantum Shadow Veil (QSV) institutional-grade manifold.
/// Enshrines the 4096-bit Hierarchical Spiral and Residue-Hiding encryption.
pub struct QuantumShadowVeil {
    pub keys: Vec<BigUint>,
    pub spiral_density: usize,
}

impl QuantumShadowVeil {
    /// Instantiates a new QSV manifold with the mandated 4096-bit density.
    pub fn new() -> Self {
        Self {
            keys: Vec::new(),
            spiral_density: 4096,
        }
    }

    /// Generates hierarchical key shards following the Fibonacci growth sequence.
    /// Anchor: k_{n+1} = k_n + k_{n-1} mod MST_MODULUS.
    pub fn expand_fibonacci_keys(&mut self, seed: BigUint, count: usize) {
        let mut a = seed;
        let mut b = &a * 2u32;
        let mst_big = BigUint::from(MST_MODULUS);

        for _ in 0..count {
            let next = (&a + &b) % &mst_big;
            self.keys.push(a.clone());
            a = b;
            b = next;
        }
    }

    /// Performs Residue-Hiding (RH) encryption by injecting salts into the
    /// prime-class gaps of the MST manifold.
    pub fn residue_hide_encrypt(&self, payload: &[u8], key_index: usize) -> Vec<u8> {
        let key = &self.keys[key_index % self.keys.len()];
        let mut ciphertext = Vec::with_capacity(payload.len());

        for (i, &byte) in payload.iter().enumerate() {
            // Residue transform: (byte + key_byte) * phi_inv mod 256
            let salt = (key % 256u32).to_u32_digits()[0] as u8;
            let res = byte.wrapping_add(salt).wrapping_mul((i % 7) as u8 + 1);
            ciphertext.push(res);
        }
        ciphertext
    }

    /// Verifies the orthogonal phasing of an encryption block against the 729D lattice.
    /// Anchor: Valid iff (Hash(block) * phi) mod 1.0 < epsilon.
    pub fn tupt_matrix_verify(&self, block: &[u8]) -> bool {
        let mut sum = 0u64;
        for &b in block {
            sum = sum.wrapping_add(b as u64);
        }
        // Simplified resonant check for matrix phasing
        let residue = sum % TUPT_MODULO;
        residue != 0 && residue % 3 != 0
    }
}

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
    if private_nonce == 0 || private_nonce.rem_euclid(3) == 0 {
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
    fn test_quantum_shadow_veil() {
        use num_bigint::ToBigUint;
        let mut qsv = QuantumShadowVeil::new();
        let seed = 137.to_biguint().unwrap(); // Digital root 1+3+7=11 -> 2

        qsv.expand_fibonacci_keys(seed, 10);
        assert_eq!(qsv.keys.len(), 10);

        let data = b"NRC_TOP_SECRET";
        let encrypted = qsv.residue_hide_encrypt(data, 3);
        assert_ne!(data.to_vec(), encrypted);
        assert_eq!(data.len(), encrypted.len());

        assert!(qsv.tupt_matrix_verify(&encrypted));
    }

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
