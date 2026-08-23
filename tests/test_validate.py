import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("validator", ROOT / "scripts/validate.py")
assert SPEC and SPEC.loader
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


class ValidationTests(unittest.TestCase):
    def test_repository_is_valid(self):
        self.assertEqual(VALIDATOR.validate(ROOT), [])

    def test_redaction_guard_catches_live_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "workflows/example").mkdir(parents=True)
            (root / "matrix.csv").write_text(
                "workflow,domain,cadence,runtime,risk,delivery,receipt,verification,failure\n",
                encoding="utf-8",
            )
            (root / "workflows/example/job.json").write_text(
                '{"job_id":"abcdef123456"}', encoding="utf-8"
            )
            issues = VALIDATOR.validate(root)
            self.assertTrue(any("forbidden live job id" in issue for issue in issues))


if __name__ == "__main__":
    unittest.main()
