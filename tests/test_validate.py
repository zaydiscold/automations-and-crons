import importlib.util
import json
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

    def test_every_job_declares_model_and_output_contract(self):
        for path in ROOT.glob("workflows/**/job.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            runtime = data["runtime"]
            self.assertEqual(runtime["model_attached"], runtime["uses_llm"])
            if runtime["model_attached"]:
                self.assertIsInstance(runtime["model"], dict)
                self.assertTrue(runtime["model"]["fallbacks"])
            else:
                self.assertIsNone(runtime["model"])
            self.assertTrue((path.parent / data["output_format"]["template"]).is_file())
            self.assertFalse(data["copying"]["ready_to_run"])
            self.assertTrue(data["limitations"])

    def test_repo_brand_and_license_are_current(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8").lower()
        self.assertIn("# automations and crons", readme)
        self.assertNotIn("hermes cron playbooks", readme)
        self.assertNotIn("san" + "itized", readme)
        self.assertNotIn("ver" + "ifiable", readme)
        self.assertFalse((ROOT / "LICENSE").exists())

    def test_empty_model_and_runtime_values_are_rejected(self):
        source = ROOT / "workflows/robinhood/premarket-brief/job.json"
        data = json.loads(source.read_text(encoding="utf-8"))
        data["runtime"]["scheduler"] = ""
        data["runtime"]["model"]["fallbacks"][0]["provider"] = ""
        data["verification"] = "looks nonempty but is not a list"
        data["copying"]["requires"] = "also not a list"
        data["limitations"] = "not a list either"
        issues = VALIDATOR.validate_spec(source, data)
        self.assertTrue(any("runtime.scheduler" in issue for issue in issues))
        self.assertTrue(any("every fallback" in issue for issue in issues))
        self.assertTrue(any("verification must be a nonempty list" in issue for issue in issues))
        self.assertTrue(any("copying.requires" in issue for issue in issues))
        self.assertTrue(any("limitations must contain" in issue for issue in issues))

    def test_market_templates_are_session_grounded(self):
        premarket_job = json.loads(
            (ROOT / "workflows/robinhood/premarket-brief/job.json").read_text(encoding="utf-8")
        )
        self.assertEqual(premarket_job["schedule"]["cron"], "30 5 * * 1-5")

        premarket = (
            ROOT / "workflows/robinhood/premarket-brief/output.md"
        ).read_text(encoding="utf-8")
        midday = (
            ROOT / "workflows/robinhood/midday-snapshot/output.md"
        ).read_text(encoding="utf-8")
        postmarket = (
            ROOT / "workflows/robinhood/postmarket-summary/output.md"
        ).read_text(encoding="utf-8")

        self.assertIn("Ext-hours vs prior close", premarket)
        self.assertIn("afterHoursChangeUsd", premarket)
        self.assertIn("not an isolated overnight session", premarket)
        self.assertIn("biggest regular-session drivers", midday)
        self.assertIn("Top regular-session $ movers", postmarket)
        for rendered in (premarket, midday, postmarket):
            self.assertNotIn("| Why |", rendered)
            self.assertIn("mandatory explanation column", rendered)


if __name__ == "__main__":
    unittest.main()
