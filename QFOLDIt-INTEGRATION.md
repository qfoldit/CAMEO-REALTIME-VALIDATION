# qFoldIT Validation Boundary

CAMEO Realtime Validation is an independent **validator service**.

It consumes canonical qFoldIT scientific state and returns validation/evidence data. It must not own mission semantics or runtime state.

```text
qfoldit-core
    ↓
Scientific Action / Candidate State
    ↓
CAMEO validator
    ↓
Validation Result
    ↓
Evidence / Provenance
```

Keep validator-specific algorithms and deployment concerns in this repository. Shared mission/object contracts belong to qFoldIT Rust core.
