# Real-time CAMEO-style validation bus — UEFN ↔ OpenStructure ↔ GitHub Pages

**Status:** design proposal / reconciliation architecture  
**Principal Global Headquarters:** Elkridge, Maryland, USA.

This repository defines the CAMEO-style reconciliation path between the UEFN runtime, external scientific validation, evidence records, and the public state projection. It is designed around the platform constraints of the UEFN/Verse sandbox rather than against them.

## 1. The constraint this proposal designs around

Verse runs inside Epic's sandbox and cannot be treated as an arbitrary network client for live calls to external scientific services such as OpenStructure.

**Therefore this architecture does not attempt to route around the sandbox.** The intended pattern is:

```text
UEFN Runtime
    ↓
Session / Submission Publication
    ↓
External Reconciliation
    ↓
OpenStructure / Approved Validator
    ↓
Evidence / Contribution Record
    ↓
World State Projection
```

## 2. Target architecture

```text
[ Ops / Scientific Panel ]       [ UEFN Island / Live Match ]       [ Public World State ]
        │                                  │                              ▲
        │ target created                   │ player builds                │
        ▼                                  ▼                              │
 qfoldit-scene-export                local mission logic                  │
        │                                  │                              │
        ▼                                  │                              │
 building_grid_mapper.py                  │                              │
        │                                  │                              │
        ▼                                  ▼                              │
 authoring-time compiled            Validate / checkpoint                  │
 runtime representation                    │                              │
                                           ▼                              │
                                  publish session state                     │
                                  through supported runtime                │
                                  persistence/publication                  │
                                           │                              │
                                           ▼                              │
                               External reconciliation service             │
                                           │                              │
                           ┌───────────────┴──────────────┐                │
                           │                              │                │
                           ▼                              ▼                │
                    schema/provenance              OpenStructure /         │
                    normalization                  approved validator       │
                           │                              │                │
                           └───────────────┬──────────────┘                │
                                           ▼                              │
                               scientific-contribution-record              │
                                           │                              │
                                           ▼                              │
                                  generated STATE object ──────────────────┘
```

## 3. What each piece actually is

### 3.1 Target authoring

The ops/scientific panel creates a governed target or reference through the normal authoring-time scientific workflow. Private scientific data remains outside public runtime assets.

### 3.2 Procedural level assembly

`building_grid_mapper.py` and `qfoldit-scene-export` can translate canonical target state into ordered runtime placement information. The generated representation is a runtime manifestation of the mission contract, not the scientific authority itself.

### 3.3 In-match validation interaction

Inside a live match, Verse can inspect local mission state, apply local/baked gameplay checks where appropriate, provide immediate player feedback, and publish the permitted session/submission state.

The immediate in-game result must be clearly distinguished from authoritative external scientific validation.

### 3.4 External reconciliation service

The external service is responsible for:

- retrieving or receiving permitted session publications;
- validating schema and provenance;
- reconstructing the submitted candidate/state;
- dispatching the candidate through the configured scientific validator;
- recording result hashes, evidence level and validator metadata;
- publishing reconciled aggregate state to the public/world-state layer.

### 3.5 World page

A static world page can read generated state such as `state.json`. The public page is a projection of the validated evidence state; it is not the scientific authority.

## 4. Honest latency characterization

This architecture provides **near-real-time global state, not literally live in-match OpenStructure scoring**.

The player can receive an immediate local runtime response. The authoritative OpenStructure/validator result is produced by the external reconciliation path and then projected to the shared state. The final latency therefore depends on session publication, read-back availability, reconciliation scheduling and validator runtime.

## 5. Three-clock model

The system explicitly separates:

```text
AUTHORING CLOCK
objective → reference → mission compilation → runtime build

RUNTIME CLOCK
player / AI interaction → local mission state → submission

RECONCILIATION CLOCK
session read-back → validation → evidence → state projection → settlement
```

A single timestamp must not be used to imply that all three clocks are one transaction.

## 6. Build order

1. Confirm the supported mechanism for external read-back/publication of session data.
2. Stand up the smallest reconciliation service: ingest → validate schema → score → write evidence.
3. Wire `scientific-contribution-record` into the reconciliation result.
4. Publish generated state through the qfoldit.github.io pipeline.
5. Point the dashboard at the published state once the live path is operating.
6. Add monitoring for missing, delayed, rejected, or unverifiable submissions.

## 7. Fail-closed rule

```text
No authoritative validator result
        ↓
No accepted scientific result
        ↓
No evidence completion
        ↓
No evidence-gated settlement
```

The system must never replace unavailable scientific validation with a synthetic success score.
