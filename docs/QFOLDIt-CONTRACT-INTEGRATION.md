# qFoldIT Contract Integration

CAMEO-REALTIME-VALIDATION is the runtime-to-science reconciliation boundary. It connects engine-local validation, externally observable runtime submissions and authoritative scientific evidence.

## Dual-clock model

```text
Runtime clock
player action -> local validation -> published submission

Scientific clock
published submission -> reconciliation -> scientific solver -> evidence
```

The runtime may provide immediate gameplay feedback. Scientific evidence remains authoritative only after the external validation path completes.

## Canonical contracts

- `qfoldit.submission/1.0`
- `qfoldit.evidence/1.0`
- `qfoldit.contribution-record/1.0`
- `qfoldit.event/1.0`
- `qfoldit.scientific-state/1.0`

## Reconciliation sequence

1. Read a new runtime publication.
2. Normalize it to `qfoldit.submission/1.0`.
3. Preserve runtime provenance and hashes.
4. Submit the candidate to the configured scientific validation authority.
5. Normalize the response as `qfoldit.evidence/1.0`.
6. Append or update the contribution record.
7. Emit `validation.completed` and related lifecycle events.
8. Publish only the approved projection to STATE.

## Scientific integrity

A runtime score, gameplay score, or heuristic match is an experience signal. It is not automatically scientific evidence. The evidence record must identify the validation method, engine/version, job identifier and relevant content/reference hashes when available.
