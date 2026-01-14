import os
import re
import sys
from typing import Tuple, Optional

# Constants do Protocolo MARTINS-432-FLOW
EXPECTED_INTERVAL_NS = 2314814
EXPECTED_GOLDEN_RATIO = 1.618
FLOAT_TOLERANCE = 1e-4  
NS_TOLERANCE = 10       

# Caminhos locais (Modo Air-Gapped)
README_PATH = "README.md"
SOP_PATH = "docs/OFFLINESYNCSOP.md"
SOURCE_PATH = "src/martins_integrity.c"

def read_file(path: str) -> Optional[str]:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except FileNotFoundError:
        return None

def validate_coherence_interval(source_code: str) -> Tuple[bool, Optional[int], str]:
    matches = re.findall(r"(\d{6,})", source_code)
    for m in matches:
        val = int(m)
        if abs(val - EXPECTED_INTERVAL_NS) <= NS_TOLERANCE:
            return True, val, "Coherence interval matches expected value (432Hz)."
    return False, None, "Expected coherence interval (2,314,814 ns) not found."

def validate_golden_ratio(source_code: str) -> Tuple[bool, Optional[float], str]:
    float_matches = re.findall(r"(\d\.\d{3,})", source_code)
    for m in float_matches:
        val = float(m)
        if abs(val - EXPECTED_GOLDEN_RATIO) <= FLOAT_TOLERANCE:
            return True, val, "Golden Ratio constant (1.618) detected."
    return False, None, "Golden Ratio (1.618) not found."

def main():
    print(f"--- [STARTING SOVEREIGN STABILITY AUDIT] ---")
    source_code = read_file(SOURCE_PATH)
    
    if source_code is None:
        print(f"FAIL: Source file not found at {SOURCE_PATH}")
        sys.exit(1)

    int_ok, int_val, int_msg = validate_coherence_interval(source_code)
    rat_ok, rat_val, rat_msg = validate_golden_ratio(source_code)

    print(f"1. TIME INTEGRITY: {'PASS' if int_ok else 'FAIL'} -> {int_msg}")
    print(f"2. GEOMETRIC SCALING: {'PASS' if rat_ok else 'FAIL'} -> {rat_msg}")

    if int_ok and rat_ok:
        print(f"\n[OVERALL STATUS]: 100% SYNC - GRADE 1 READY")
    else:
        print(f"\n[OVERALL STATUS]: DESYNC DETECTED - REVIEW CORE CONSTANTS")

if __name__ == "__main__":
    main()
