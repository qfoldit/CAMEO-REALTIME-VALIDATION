from __future__ import annotations

import unittest

from qfoldit_lineage import LineageError, validate_openstructure_result


VALID = {
    "jobId": "job-1",
    "missionId": "mission-1",
    "actionEnvelopeHash": "sha256:" + "a" * 64,
    "submissionId": "11111111-1111-4111-8111-111111111111",
    "status": "completed",
    "engine": "OpenStructure",
    "engineVersion": "2.12.0",
    "reference": {
        "referenceId": "reference-1",
        "sha256": "b" * 64,
        "format": "cif",
    },
    "modelSha256": "c" * 64,
    "scores": {"lddt": 0.91},
    "validationVersion": "qfoldit.openstructure/1.2",
    "completedAt": "2026-08-23T15:49:00Z",
}


class LineageContractTests(unittest.TestCase):
    def test_normalizes_valid_result(self) -> None:
        normalized = validate_openstructure_result(VALID)
        self.assertEqual(normalized["missionId"], "mission-1")
        self.assertEqual(normalized["actionEnvelopeHash"], "sha256:" + "a" * 64)
        self.assertEqual(normalized["submissionId"], VALID["submissionId"])

    def test_rejects_missing_action_hash(self) -> None:
        payload = dict(VALID)
        payload.pop("actionEnvelopeHash")
        with self.assertRaises(LineageError):
            validate_openstructure_result(payload)

    def test_rejects_wrong_submission_identity(self) -> None:
        payload = dict(VALID)
        payload["submissionId"] = "not-a-uuid"
        with self.assertRaises(LineageError):
            validate_openstructure_result(payload)

    def test_rejects_non_completed_result(self) -> None:
        payload = dict(VALID)
        payload["status"] = "failed"
        with self.assertRaises(LineageError):
            validate_openstructure_result(payload)


if __name__ == "__main__":
    unittest.main()
