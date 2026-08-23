from __future__ import annotations

import re
import uuid
from datetime import datetime
from typing import Any

_SHA256_PREFIX = re.compile(r"^sha256:[A-Fa-f0-9]+$")
_HEX64 = re.compile(r"^[A-Fa-f0-9]{64}$")


class LineageError(ValueError):
    """Raised when a validator result cannot be promoted to evidence safely."""


def validate_openstructure_result(result: dict[str, Any]) -> dict[str, Any]:
    """Validate and normalize OpenStructure/qFoldIT provenance without owning mission semantics."""
    required = (
        "missionId",
        "actionEnvelopeHash",
        "submissionId",
        "status",
        "engine",
        "engineVersion",
        "reference",
        "modelSha256",
        "validationVersion",
        "completedAt",
    )
    missing = [key for key in required if key not in result]
    if missing:
        raise LineageError(f"missing provenance fields: {', '.join(missing)}")

    mission_id = str(result["missionId"]).strip()
    action_hash = str(result["actionEnvelopeHash"]).strip()
    submission_id = str(result["submissionId"]).strip()
    if not mission_id:
        raise LineageError("missionId cannot be empty")
    if not _SHA256_PREFIX.fullmatch(action_hash):
        raise LineageError("actionEnvelopeHash must use sha256: representation")
    try:
        uuid.UUID(submission_id)
    except ValueError as exc:
        raise LineageError("submissionId must be a UUID") from exc
    if str(result["status"]).lower() != "completed":
        raise LineageError("validator result is not completed")
    if not str(result["engine"]).strip() or not str(result["engineVersion"]).strip():
        raise LineageError("validator engine provenance is incomplete")

    reference = result["reference"]
    if not isinstance(reference, dict):
        raise LineageError("reference provenance must be an object")
    reference_id = str(reference.get("referenceId", "")).strip()
    reference_hash = str(reference.get("sha256", "")).strip()
    reference_format = str(reference.get("format", "")).strip()
    if not reference_id or not _HEX64.fullmatch(reference_hash) or not reference_format:
        raise LineageError("reference provenance is incomplete")

    model_hash = str(result["modelSha256"]).strip()
    if not _HEX64.fullmatch(model_hash):
        raise LineageError("modelSha256 must be a 64-character hex SHA-256")

    try:
        completed_at = datetime.fromisoformat(str(result["completedAt"]).replace("Z", "+00:00"))
    except ValueError as exc:
        raise LineageError("completedAt must be an ISO-8601 timestamp") from exc

    return {
        "missionId": mission_id,
        "actionEnvelopeHash": action_hash,
        "submissionId": submission_id,
        "status": "completed",
        "engine": str(result["engine"]),
        "engineVersion": str(result["engineVersion"]),
        "reference": {
            "referenceId": reference_id,
            "sha256": reference_hash,
            "format": reference_format,
        },
        "modelSha256": model_hash,
        "validationVersion": str(result["validationVersion"]),
        "completedAt": completed_at.isoformat().replace("+00:00", "Z"),
    }
