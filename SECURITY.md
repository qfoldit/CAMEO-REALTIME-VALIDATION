# Security Policy

## Role

CAMEO-REALTIME-VALIDATION is the realtime submission and reconciliation boundary between runtime experiences and qFoldIT scientific evidence.

## Production security boundary

Production validation services should run inside the qFoldIT private corporate infrastructure boundary. Protected scientific references, customer submissions, credentials, private policies and internal reconciliation data must remain outside public client payloads.

## Required controls

- private production deployment and organization-controlled access;
- least-privilege service credentials;
- authenticated submission endpoints;
- immutable submission and evidence identifiers;
- payload size and schema validation;
- request logging without raw confidential scientific payloads;
- dependency/license scanning;
- signed release artifacts and provenance records;
- immutable audit retention.

## Disclosure boundary

Any source already distributed under an open-source license remains subject to that license. This document defines the intended boundary for qFoldIT production infrastructure and confidential deployments.
