# tests/stability_check.py
# Stability Check Script for MARTINS-432-FLOW-2025
# Validates coherence interval (2,314,814 ns) and Golden Ratio (1.618) usage from local source files in air-gapped mode.

import os
import re
import sys
from typing import Tuple, Optional

# Constants
EXPECTED_INTERVAL_NS = 2_314_814
EXPECTED_GOLDEN_RATIO = 1.618
FLOAT_TOLERANCE = 1e-4  # allowable float deviation
NS_TOLERANCE = 10       # allowable integer deviation in nanoseconds

# Local file paths (air-gapped, relative to repo root)
README_PATH = "README.md"
SOP_PATH = "docs/OFFLINE_SYNC_SOP.md"
SOURCE_PATH = "src/martins_integrity.c"

def read_file(path: str) -> Optional[str]:
    """Read a local file safely; return None if missing."""
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    except FileNotFoundError:
        return None

def validate_coherence_interval(source_code: str) -> Tuple[bool, Optional[int], str]:
    """
    Search for timing constants in nanoseconds within the C source.
    Accepts integers possibly annotated with ns/nanoseconds/UL/ULL.
    """
    # Match large integers with optional suffixes (ns, UL, ULL)
    matches = re.findall(r"(\d{6,})(?:\s*(?:ns|nanoseconds|UL|ULL))?", source_code)
    for m in matches:
        try:
            val = int(m)
            if abs(val - EXPECTED_INTERVAL_NS) <= NS_TOLERANCE:
                return True, val, "Coherence interval matches expected value."
        except ValueError:
            continue

    # Secondary: look for explicit defines or variables that hint at interval
    # e.g., #define COHERENCE_NS 2314814
    def_matches = re.findall(r"#\s*define\s+\w+\s+(\d{6,})", source_code)
    for m in def_matches:
        try:
            val = int(m)
            if abs(val - EXPECTED_INTERVAL_NS) <= NS_TOLERANCE:
                return True, val, "Coherence interval found via macro definition."
        except ValueError:
            continue

    return False, None, "Expected coherence interval (2,314,814 ns) not found."

def validate_golden_ratio_usage(source_code: str) -> Tuple[bool, Optional[float], str]:
    """
    Detect usage of the Golden Ratio (1.618) or close approximations in float constants.
    """
    # Capture float literals like 1.618, 1.6180, 1.618033, etc.
    float_matches = re.findall(r"(?<!\w)(\d?\.\d{3,})(?!\w)", source_code)
    for m in float_matches:
        try:
            val = float(m)
            if abs(val - EXPECTED_GOLDEN_RATIO) <= FLOAT_TOLERANCE:
                return True, val, "Golden Ratio constant detected in source logic."
        except ValueError:
            continue

    # Also check for common phi approximations in comments or defines
    # e.g., #define PHI 1.618 or const double PHI = 1.618033;
    phi_matches = re.findall(r"(?:PHI|phi|golden[_ ]?ratio)\s*[:=]\s*([0-9]*\.[0-9]+)", source_code, flags=re.IGNORECASE)
    for m in phi_matches:
        try:
            val = float(m)
            if abs(val - EXPECTED_GOLDEN_RATIO) <= FLOAT_TOLERANCE:
                return True, val, "Golden Ratio constant detected via PHI alias."
        except ValueError:
            continue

    return False, None, "Golden Ratio (1.618) not found in source logic."

def summarize_context(readme: Optional[str], sop: Optional[str]) -> None:
    """
    Optional contextual checks: confirm references to 432s window and quorum ~1/phi in docs.
    Does not affect PASS/FAIL for core checks, but provides visibility.
    """
    print("\n[Context Summary]")
    if readme:
        has_432s = bool(re.search(r"\b432s\b|\b432\s*seconds\b", readme, flags=re.IGNORECASE))
        has_phi = bool(re.search(r"\b1\.618\b|\bgolden\s*ratio\b|\bphi\b", readme, flags=re.IGNORECASE))
        print(f"- README.md mentions 432s window: {'YES' if has_432s else 'NO'}")
        print(f"- README.md mentions Golden Ratio (1.618/phi): {'YES' if has_phi else 'NO'}")
    else:
        print("- README.md not found.")

    if sop:
        has_432s = bool(re.search(r"\b432s\b|\b432\s*seconds\b", sop, flags=re.IGNORECASE))
        has_quorum = bool(re.search(r"\bquorum\b|\b1\/\s*phi\b|\b1\.618\b", sop, flags=re.IGNORECASE))
        print(f"- OFFLINE_SYNC_SOP.md mentions 432s window: {'YES' if has_432s else 'NO'}")
        print(f"- OFFLINE_SYNC_SOP.md mentions quorum ~1/phi: {'YES' if has_quorum else 'NO'}")
    else:
        print("- docs/OFFLINE_SYNC_SOP.md not found.")

def main() -> None:
    # Air-gapped assumption: only local files are truth
    source_code = read_file(SOURCE_PATH)
    readme = read_file(README_PATH)
    sop = read_file(SOP_PATH)

    if source_code is None:
        print(f"FAIL: Source file not found at {SOURCE_PATH}")
        sys.exit(1)

    # Perform core validations
    interval_ok, interval_val, interval_msg = validate_coherence_interval(source_code)
    ratio_ok, ratio_val, ratio_msg = validate_golden_ratio_usage(source_code)

    print("[Stability Check Results]")
    if interval_ok:
        print(f"PASS: Coherence interval found: {interval_val} ns — {interval_msg}")
    else:
        print(f"FAIL: {interval_msg}")

    if ratio_ok:
        print(f"PASS: Golden Ratio constant found: {ratio_val} — {ratio_msg}")
    else:
        print(f"FAIL: {ratio_msg}")

    # Optional context summary from docs
    summarize_context(readme, sop)

    # Overall status
    overall = "PASS" if (interval_ok and ratio_ok) else "FAIL"
    print(f"\n[Overall] {overall}")

if __name__ == "__main__":
    main()
