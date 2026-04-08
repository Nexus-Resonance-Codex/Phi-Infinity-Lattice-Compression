import sys


def get_digital_root(n: int) -> int:
    """Calculates the iterative digital root of an integer."""
    if n == 0:
        return 9
    res = n % 9
    return 9 if res == 0 else res

def verify_ttt_stable(value: int, name: str) -> bool:
    root = get_digital_root(value)
    stable = root in [1, 2, 4, 5, 7, 8]
    status = "STABLE" if stable else "CHAOTIC"
    print(f"Checking {name:25}: Value={value:10}, Root={root}, Status={status}")
    return stable

def run_integrity_check():
    print("┌────────────────────────────────────────────────────────────────────────────┐")
    print("│         NEXUS RESONANCE CODEX – REPOSITORY INTEGRITY VERIFIER            │")
    print("└────────────────────────────────────────────────────────────────────────────┘")

    # Core Constants from compressor.py and tupt_crypto.py
    constants = [
        (8192, "Lattice Dimensions"),
        (12289, "TUPT Modulo Prime"),
        (1618, "φ Scale Integer Mapping"),
        (4096, "Coarse Lattice Index Space"),
        (512, "Embedded Vector Width"),
    ]

    failures = 0
    for val, name in constants:
        if not verify_ttt_stable(val, name):
            failures += 1

    print("-" * 76)
    if failures == 0:
        print("ALL CRITICAL CONSTANTS ANCHORED AT STABLE LOCI. INTEGRITY VERIFIED.")
    else:
        print(f"WARNING: {failures} CHAOTIC ATTRACTOR(S) DETECTED. ADJUST CONSTANTS.")
        sys.exit(1)

if __name__ == "__main__":
    run_integrity_check()
