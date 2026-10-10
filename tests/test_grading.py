import re
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
import grading


def report(rows=None):
    rows = rows or [(identifier, "met", f"Evidence for {identifier}.") for identifier in grading.WEIGHTS]
    body = "\n".join(f"| {identifier} | {status} | {evidence} |" for identifier, status, evidence in rows)
    return f"| ID | Status | Evidence |\n|---|---|---|\n{body}\n"


class GradingTests(unittest.TestCase):
    def test_weights_total_100_and_guide_matches_checker(self):
        self.assertEqual(sum(grading.CORE_WEIGHTS.values()), 79)
        self.assertEqual(sum(grading.SUPPORT_WEIGHTS.values()), 21)
        self.assertEqual(sum(grading.WEIGHTS.values()), 100)
        guide = (Path(__file__).resolve().parents[1] / "plan-grading-template.md").read_text(encoding="utf-8")
        listed = {identifier: int(weight) for identifier, weight in re.findall(r"\|\s*((?:C|S)\d{2})\s*\|\s*(\d+)\s*\|", guide)}
        self.assertEqual(listed, grading.WEIGHTS)

    def test_correct_report_sum_and_gaps(self):
        self.assertEqual(grading.score_report(report()), {"core": 79, "support": 21, "total": 100, "core_gaps": []})
        self.assertEqual(grading.score_report(report() + "\nDeclared score: 0/100; core gaps: C01\n")["total"], 100)
        rows = [(identifier, "not_met" if identifier in {"C01", "S05"} else "met", f"Evidence for {identifier}.") for identifier in grading.WEIGHTS]
        score = grading.score_report(report(rows))
        self.assertEqual((score["core"], score["support"], score["total"]), (77, 16, 93))
        self.assertEqual(score["core_gaps"], ["C01"])

    def test_missing_duplicate_and_unknown_ids_rejected(self):
        rows = list((identifier, "met", "Evidence.") for identifier in grading.WEIGHTS)
        with self.assertRaisesRegex(ValueError, "exactly 41"):
            grading.score_report(report(rows[:-1]))
        duplicate = rows.copy()
        duplicate[1] = (duplicate[0][0], "met", "Evidence.")
        with self.assertRaisesRegex(ValueError, "duplicate ID"):
            grading.score_report(report(duplicate))
        unknown = rows.copy()
        unknown[0] = ("C99", "met", "Evidence.")
        with self.assertRaisesRegex(ValueError, "unknown ID"):
            grading.score_report(report(unknown))

    def test_invalid_status_and_empty_evidence_rejected(self):
        rows = [(identifier, "met", "Evidence.") for identifier in grading.WEIGHTS]
        rows[0] = (rows[0][0], "blocked", "Evidence.")
        with self.assertRaisesRegex(ValueError, "status must be"):
            grading.score_report(report(rows))
        rows[0] = (rows[0][0], "met", "  ")
        with self.assertRaisesRegex(ValueError, "evidence is empty"):
            grading.score_report(report(rows))


if __name__ == "__main__":
    unittest.main()
