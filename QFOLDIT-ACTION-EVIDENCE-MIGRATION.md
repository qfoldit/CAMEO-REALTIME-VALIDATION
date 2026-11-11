# qFoldIT Action/Evidence Migration — CAMEO Realtime Validation

**Snapshot:** 2026-11-11  
**Role:** external reconciliation and validation-context boundary  
**Status:** legacy contract; migration required

## Current contract

The reviewed `adapter-manifest.json` declares:
- input `qfoldit.mission-contract/1.0` and `qfoldit.scientific-action-envelope/1.0`;
- output `qfoldit.evidence/1.1` and `qfoldit.validation.completed/1.1`;
- reconciliation capabilities, not a general-purpose mission-control runtime.

This is a legacy integration declaration. Do not merely replace these identifiers with 1.1/1.2.

## Required migration

1. Bind the reconciliation request to the approved Mission Inception digest and mission contract revision.
2. Consume Action Envelope 1.1 and verify the exact action content hash through the canonical qfoldit-core implementation.
3. Preserve submission ID, session/candidate snapshot, source runtime/adapter identity and all artifact hashes.
4. Keep benchmark-profile reconciliation separate from the scientific validator identity and claim-level validator protocol.
5. Return a reconciliation artifact to the trusted qFoldIT control plane.
6. Do not construct or self-issue Evidence 1.2. The approved independent validator and separate authenticated Evidence publisher own that boundary.
7. Preserve historical 1.0/1.1 parsing; new mission work must fail closed on missing or inconsistent lineage.

## Conformance acceptance

- Positive and negative fixtures for missing/stale inception hash, action hash mismatch, wrong profile, unknown submission and provider/result substitution.
- Action 1.1 cross-contract conformance.
- Evidence 1.2 lineage consumption with trusted issuer verification.
- Live bounded CAMEO reconciliation smoke using an approved, versioned profile.
- Operational logs and replay/idempotency evidence.

## Canonical references

- [Provider Adapter Conformance Standard](https://github.com/qfoldit/UAG-SOS/blob/main/STANDARDS/MCP/SCIENTIFIC-MCP-PROVIDER-ADAPTER-CONFORMANCE-v0.1.md)
- [Action/Evidence Migration Plan](https://github.com/qfoldit/UAG-SOS/blob/main/STANDARDS/MCP/LEGACY-ACTION-EVIDENCE-MIGRATION-PLAN-2026-11-11.md)
- [Migration Register](https://github.com/qfoldit/UAG-SOS/blob/main/SCHEMAS/QSIS/provider-adapter-migration-register.json)
