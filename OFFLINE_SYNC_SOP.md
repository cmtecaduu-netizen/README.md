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
flowchart LR
  %% Emergency Synchrony Network (ESN) Topology
  %% Anchor Nodes emit 432Hz pulses; Relays bridge Sneaker-net/Radio; Edge Nodes (154 clones) validate via tests/
  %% Quorum: ~1/φ ≈ 61% ; Epoch Window: 432s

  %% Styling
  classDef anchor fill:#1f77b4,stroke:#0d3b66,stroke-width:2,color:#fff
  classDef relay fill:#ff7f0e,stroke:#8c3f00,stroke-width:2,color:#fff
  classDef edge fill:#2ca02c,stroke:#145214,stroke-width:2,color:#fff
  classDef meta fill:#6a5acd,stroke:#3b2f8f,stroke-width:2,color:#fff

  %% Legend / Meta
  subgraph META[Harmonic & Governance Parameters]
    Q[Quorum ≈ 1/φ ≈ 61%]:::meta
    W[Epoch Window = 432s]:::meta
  end

  %% Anchors
  subgraph A[Anchor Nodes — 432Hz Pulse Emitters]
    A1[Anchor-1\nCalibrated 432Hz]:::anchor
    A2[Anchor-2\nCalibrated 432Hz]:::anchor
    A3[Anchor-3\nCalibrated 432Hz]:::anchor
  end

  %% Relays
  subgraph R[Relay Nodes — Sneaker-net & Radio Bridge]
    R1[Relay-Alpha\nFSK/PSK + USB/SD]:::relay
    R2[Relay-Beta\nHF/VHF + QR/Print]:::relay
    R3[Relay-Gamma\nOptical + Cache]:::relay
  end

  %% Edge Nodes (154 clones)
  subgraph E[Edge Nodes — 154 Clones (tests/ Validation)]
    E1[Clone-001\nVerify + tests/]:::edge
    E2[Clone-002\nVerify + tests/]:::edge
    E3[Clone-003\nVerify + tests/]:::edge
    Eall[Clone-004…154\nDistributed Regions]:::edge
  end

  %% Pulsation & Epoch Alignment
  A1 -- "432Hz Preamble\nEpoch Start" --> R1
  A2 -- "432Hz Preamble\nEpoch Start" --> R2
  A3 -- "432Hz Preamble\nEpoch Start" --> R3
  W -. "Window Alignment" .- A1
  W -. "Window Alignment" .- A2
  W -. "Window Alignment" .- A3

  %% Transport Flows
  R1 -- "Manifests/Hashes\nRadio Beacon" --> E1
  R2 -- "Attestations\nRadio Beacon" --> E2
  R3 -- "Canonical IDs\nRadio Beacon" --> E3

  R1 == "Full Bundles\nUSB/SD (Append-only)" ==> E1
  R2 == "Full Bundles\nSneaker-net Routes" ==> E2
  R3 == "Patches/QR\nOptical/Print" ==> E3
  R1 == "Redundant Routes\nReceipts Signed" ==> Eall
  R2 == "Redundant Routes\nReceipts Signed" ==> Eall
  R3 == "Redundant Routes\nReceipts Signed" ==> Eall

  %% Validation & Consensus
  E1 -- "Run tests/\nVerify Signatures" --> R1
  E2 -- "Run tests/\nVerify Signatures" --> R2
  E3 -- "Run tests/\nVerify Signatures" --> R3
  Eall -- "Attestations\nDistributed Regions" --> R1
  Eall -- "Attestations\nDistributed Regions" --> R2
  Eall -- "Attestations\nDistributed Regions" --> R3

  R1 -- "Aggregate Attestations" --> A1
  R2 -- "Aggregate Attestations" --> A2
  R3 -- "Aggregate Attestations" --> A3

  %% Canonicalization Broadcast
  A1 -- "Canonical Manifest ID\nCo-signed" --> R1
  A2 -- "Canonical Manifest ID\nCo-signed" --> R2
  A3 -- "Canonical Manifest ID\nCo-signed" --> R3
  R1 -- "Canonical ID\nEpoch Window" --> Eall
  R2 -- "Canonical ID\nEpoch Window" --> Eall
  R3 -- "Canonical ID\nEpoch Window" --> Eall

  %% Quorum Note
  Q -. "Canonicalization requires\n~61% attestations across φ regions" .- A1
  Q -. "Backoff for conflicts:\n1.618× epochs" .- R2
