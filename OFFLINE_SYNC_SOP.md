# OFFLINE SYNC SOP

## Epoch Timing (432s Window)
- Synchronization epochs are defined as **432-second windows**, aligned with the harmonic constant of 432Hz.  
- **Anchor nodes** broadcast a 432Hz preamble at the start of each epoch to establish timing consensus.  
- All nodes align local operations within these windows, ensuring deterministic flow and minimizing drift.  
- Epochs provide structured intervals for proposal, validation, and canonicalization of bundles.

---

## Golden Ratio Quorum Rules
- Quorum thresholds are set at approximately **61% (1/φ)** of active nodes, reflecting the golden ratio principle.  
- Canonical releases require attestations from at least **φ regions** (minimum of 2 out of 3, or proportional equivalents).  
- Conflict resolution follows a strict preference order:  
  1. **Integrity:** Highest reproducibility and passing of `tests/`.  
  2. **Timing:** Closest alignment to anchor epoch markers.  
  3. **Co-signature diversity:** Greater distribution of signatures across distinct regions.  
- Nodes proposing losing branches must apply a **1.618× epoch backoff** before re-proposal, ensuring systemic harmony.

---

## Radio/Physical Media Transport Procedures
- **Radio Beacons:**  
  - Broadcast manifests, hashes, and attestations using low-bandwidth FSK/PSK signals.  
  - Each transmission begins with a **432Hz preamble** to allow synchronization and drift correction.  
  - Payloads are limited to metadata; full bundles are transported via physical media.  

- **Sneaker-net:**  
  - Use **USB/SD media** with append-only ledgers to transport full payloads.  
  - Redundant routes are required to prevent single-point failures.  
  - Each relay node adds a signed receipt; anchors reconcile receipts during epochs.  

- **Optical/Print:**  
  - Encode manifests and small patches into **QR or Aztec codes** for durable fallback.  
  - Printed hashes serve as verification anchors in case of digital corruption.  

- **Relay Operations:**  
  - Relays validate and cache bundles locally.  
  - Anchors reconcile receipts and broadcast canonical manifest IDs during each epoch.  
  - Edge nodes verify signatures and run `tests/` before applying updates.

---

## Declaration
This SOP formalizes the **Emergency Synchrony Network** procedures for MARTINS-432-FLOW-2025.  
By adhering to harmonic timing, golden ratio quorum, and resilient transport methods, the system ensures **offline survival and integrity preservation** even in the absence of global TCP/IP infrastructure.
