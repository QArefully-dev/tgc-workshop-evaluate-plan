import argparse
import copy
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import grading

SPEC = grading.load_spec(grading.ROOT)
MANIFEST = {"version": "v3", "run_id": "calibration", "files": {"fixture": "frozen-test-only"}}


def empty_report():
    return {
        "version": "v3", "run_id": "calibration", "input_hashes": MANIFEST["files"].copy(),
        "quality": {"results": [{"id": row["id"], "weight": row["weight"], "status": "missing", "evidence": "Scoped probe: assertion absent outside focus IDs.", "assertions": []} for row in SPEC["ids"]], "improvements": []},
        "compliance": {"rules": [{"id": identifier, "status": "unknown", "evidence": "No candidate host trace supplied."} for identifier in grading.COMPLIANCE_IDS], "eligibility": "unknown"},
        "efficiency": {"duration_seconds": "unknown", "tokens": "unknown", "cost": "unknown", "evidence": "No candidate host metrics supplied."},
    }


def fixture_report(case):
    report = empty_report()
    by_id = {row["id"]: row for row in SPEC["ids"]}
    for result in report["quality"]["results"]:
        identifier = result["id"]
        if identifier not in case["expected"]:
            continue
        result["status"] = case["expected"][identifier]
        result["evidence"] = case["rationale"]
        if result["status"] == "missing":
            continue
        result["assertions"] = [{
            "assertion_id": "primary", "scenario": case["name"], "evidence": case["candidate"],
            "expectation": "product_defect_expected" if identifier in case["defect_ids"] else "required_behavior",
            "prerequisites": [{"id": prerequisite, "status": case["failed_prerequisites"].get(prerequisite, "satisfied"), "evidence": case["rationale"]} for prerequisite in by_id[identifier]["prerequisites"]],
        }]
        extra = case.get("extra_blocked_assertion")
        if extra and extra["id"] == identifier:
            blocked = copy.deepcopy(result["assertions"][0])
            blocked["assertion_id"] = "invalid-earlier-instance"
            blocked["scenario"] = "first invalid normal journey"
            for prerequisite in blocked["prerequisites"]:
                if prerequisite["id"] == extra["prerequisite"]:
                    prerequisite["status"] = "invalid_authored_setup"
            result["assertions"].insert(0, blocked)
    return report


def all_met_report():
    case = grading.read_json(grading.ROOT / "calibration/development.json")["cases"][0]
    return fixture_report(case)


class GradingTests(unittest.TestCase):
    def test_reviewed_fixture_decisions_and_external_totals(self):
        # Tests consistency of author-reviewed decisions, not model interpretation of text.
        expected_totals = {"valid_plan": 100, "invalid_normal_setup": 12, "invalid_correction": 18,
                           "valid_product_defect": 9, "omitted_guidance": 4,
                           "correct_oracle_immaterial_rounding": 5,
                           "disabled_selection_is_not_rejection": 0,
                           "independent_edit_survives_invalid_create": 12,
                           "material_rounding_error": 4, "alternative_guidance_coverage": 5}
        for filename in ("development.json", "held-out.json"):
            for case in grading.read_json(grading.ROOT / "calibration" / filename)["cases"]:
                with self.subTest(case=case["name"]):
                    score = grading.validate_report(fixture_report(case), MANIFEST, SPEC)
                    self.assertEqual(score["total"], expected_totals[case["name"]])
                    self.assertEqual(score["maximum"], 100)

    def test_obsolete_ids_weights_statuses_and_totals_rejected(self):
        mutations = {
            "17 checks": lambda r: r["quality"].update(results=r["quality"]["results"][:17]),
            "duplicate ID": lambda r: r["quality"]["results"][0].update(id="C02"),
            "unknown ID": lambda r: r["quality"]["results"][0].update(id="C99"),
            "wrong weight": lambda r: r["quality"]["results"][0].update(weight=5),
            "boolean weight": lambda r: r["quality"]["results"][1].update(weight=True),
            "obsolete status": lambda r: r["quality"]["results"][0].update(status="partial"),
            "model total": lambda r: r["quality"].update(total=100),
            "normalization": lambda r: r["quality"].update(normalized=71),
            "wrong version": lambda r: r.update(version="v2"),
            "wrong hash": lambda r: r.update(input_hashes={}),
            "empty evidence": lambda r: r["quality"]["results"][0].update(evidence=" "),
        }
        for name, mutate in mutations.items():
            with self.subTest(name=name):
                report = all_met_report()
                mutate(report)
                with self.assertRaises(grading.InvalidReport):
                    grading.validate_report(report, MANIFEST, SPEC)

    def test_prerequisites_cannot_be_omitted_or_failed_as_met(self):
        for status in ("invalid_authored_setup", "unknown"):
            report = all_met_report()
            result = next(r for r in report["quality"]["results"] if r["id"] == "C18")
            result["assertions"][0]["prerequisites"][0]["status"] = status
            with self.assertRaisesRegex(grading.InvalidReport, "met needs"):
                grading.validate_report(report, MANIFEST, SPEC)
            result["status"] = "blocked"
            self.assertEqual(grading.validate_report(report, MANIFEST, SPEC)["total"], 95)
        for prereqs in ([], [{"id": "normal_admissible", "status": "satisfied", "evidence": "wrong prerequisite"}]):
            report = all_met_report()
            result = next(r for r in report["quality"]["results"] if r["id"] == "C18")
            result["assertions"][0]["prerequisites"] = prereqs
            with self.assertRaisesRegex(grading.InvalidReport, "exact required prerequisites"):
                grading.validate_report(report, MANIFEST, SPEC)

    def test_duplicate_prerequisite_and_assertion_rejected(self):
        report = all_met_report()
        result = next(r for r in report["quality"]["results"] if r["id"] == "C05")
        prereqs = result["assertions"][0]["prerequisites"]
        prereqs[1] = copy.deepcopy(prereqs[0])
        with self.assertRaises(grading.InvalidReport):
            grading.validate_report(report, MANIFEST, SPEC)
        report = all_met_report()
        report["quality"]["results"][0]["assertions"] *= 2
        with self.assertRaises(grading.InvalidReport):
            grading.validate_report(report, MANIFEST, SPEC)

    def test_missing_and_blocked_consistency(self):
        for status in ("missing", "blocked"):
            report = all_met_report()
            report["quality"]["results"][0]["status"] = status
            with self.assertRaises(grading.InvalidReport):
                grading.validate_report(report, MANIFEST, SPEC)

    def test_compliance_quality_and_efficiency_separate(self):
        report = all_met_report()
        self.assertEqual(grading.validate_report(report, MANIFEST, SPEC)["total"], 100)
        for rule in report["compliance"]["rules"]:
            if rule["id"] == "word_limit":
                rule["status"] = "violated"
        self.assertEqual(grading.validate_report(report, MANIFEST, SPEC)["total"], 100)
        report["compliance"]["eligibility"] = "eligible"
        with self.assertRaisesRegex(grading.InvalidReport, "eligibility inconsistent"):
            grading.validate_report(report, MANIFEST, SPEC)
        report["compliance"]["eligibility"] = "unknown"
        for rule in report["compliance"]["rules"]:
            if rule["id"] == "no_browser_or_app":
                rule["status"] = "violated"
        report["compliance"]["eligibility"] = "ineligible"
        self.assertEqual(grading.validate_report(report, MANIFEST, SPEC)["total"], 100)
        report["efficiency"]["tokens"] = -1
        with self.assertRaises(grading.InvalidReport):
            grading.validate_report(report, MANIFEST, SPEC)

    def test_versions_and_manifest_weights(self):
        self.assertEqual((grading.ROOT / "plan-grading-template.md").read_bytes(), (grading.ROOT / "versions/plan-grading-template-v3.md").read_bytes())
        historical = subprocess.check_output(["git", "show", "f640072:plan-grading-template.md"], cwd=grading.ROOT)
        preserved = (grading.ROOT / "versions/plan-grading-template-v2.md").read_bytes()
        self.assertEqual(preserved.replace(b"\r\n", b"\n"), historical.replace(b"\r\n", b"\n"))
        self.assertEqual(sum(r["weight"] for r in SPEC["ids"]), 100)

    def test_heldout_rounding_oracle_independent_arithmetic(self):
        # Exact integer half-up, independently calculated fixture expected amount.
        rounded = [(price * percent + 50) // 100 for price, percent in ((8340, 88), (10740, 6), (10740, 6))]
        self.assertEqual(rounded, [7339, 644, 644])
        self.assertEqual(sum(rounded) * 4 + 2500, 37008)
        self.assertEqual((8340 * 88 + 10740 * 6 + 10740 * 6) * 4 // 100 + 2500, 37012)


class FrozenCliTests(unittest.TestCase):
    def setUp(self):
        scratch = Path("C:/wt") if os.name == "nt" else None
        self.temporary = tempfile.TemporaryDirectory(prefix="qme-v3-tests-", dir=scratch)
        self.directory = Path(self.temporary.name)
        self.inputs = {}
        for name in ("prompt", "ticket", "candidate", "source"):
            path = self.directory / name
            path.write_text(f"frozen {name}\n", encoding="utf-8")
            self.inputs[name] = path
        self.run = self.directory / "run"

    def tearDown(self):
        self.temporary.cleanup()

    def cli(self, *args):
        return subprocess.run([sys.executable, str(grading.ROOT / "tools/grading.py"), *map(str, args)], capture_output=True, text=True)

    def prepare(self):
        result = self.cli("prepare", "--run-id", "calibration", "--prompt", self.inputs["prompt"], "--ticket", self.inputs["ticket"], "--candidate", self.inputs["candidate"], "--source-snapshot", self.inputs["source"], "--source-revision", "fixture-revision", "--output", self.run)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_prepare_verify_validate_and_no_overwrite(self):
        self.prepare()
        self.assertEqual(self.cli("verify", "--run", self.run).returncode, 0)
        manifest = grading.read_json(self.run / "run-manifest.json")
        self.assertEqual(set(manifest["configuration"].values()), {"unknown"})
        report = all_met_report()
        report["input_hashes"] = manifest["files"]
        raw = self.directory / "raw.json"
        grading.write_json(raw, report)
        output = self.directory / "scored.json"
        result = self.cli("validate", "--run", self.run, "--report", raw, "--output", output)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(grading.read_json(output)["computed_quality"]["total"], 100)
        self.assertEqual(self.cli("validate", "--run", self.run, "--report", raw, "--output", self.run / "candidate.md").returncode, 2)
        self.assertEqual(self.cli("validate", "--run", self.run, "--report", raw, "--output", output).returncode, 2)
        self.assertEqual(self.cli("prepare", "--run-id", "again", "--prompt", self.inputs["prompt"], "--ticket", self.inputs["ticket"], "--candidate", self.inputs["candidate"], "--source-snapshot", self.inputs["source"], "--source-revision", "fixture", "--output", self.run).returncode, 2)

    def test_frozen_input_and_package_tampering_rejected(self):
        self.prepare()
        for filename in ("candidate.md", "plan-grading-template.md"):
            path = self.run / filename
            original = path.read_bytes()
            path.write_bytes(original + b"tampered\n")
            self.assertEqual(self.cli("verify", "--run", self.run).returncode, 2)
            if filename == "plan-grading-template.md":
                manifest = grading.read_json(self.run / "run-manifest.json")
                manifest["files"][filename] = grading.digest(path)
                grading.write_json(self.run / "run-manifest.json", manifest)
                self.assertEqual(self.cli("verify", "--run", self.run).returncode, 2)
            path.write_bytes(original)

    def test_missing_inputs_bad_report_and_duplicate_json_key_rejected(self):
        self.prepare()
        duplicate = self.directory / "duplicate.json"
        duplicate.write_text('{"version":"v3","version":"v2"}', encoding="utf-8")
        result = self.cli("validate", "--run", self.run, "--report", duplicate, "--output", self.directory / "score.json")
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate JSON key", result.stderr)
        (self.run / "rubric-v3.json").unlink()
        result = self.cli("verify", "--run", self.run)
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing frozen input", result.stderr)


if __name__ == "__main__":
    unittest.main()
