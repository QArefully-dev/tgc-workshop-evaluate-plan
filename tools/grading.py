"""Freeze grading inputs and validate/score v3 reports; Python standard library only."""
import argparse
import hashlib
import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PINNED = ("plan-grading-template.md", "rubric-v3.json", "report-schema.json", "grader-instructions.md")
STATUSES = {"met", "missing", "incorrect", "blocked"}
PREREQUISITE_STATUSES = {"satisfied", "invalid_authored_setup", "unknown"}
COMPLIANCE_IDS = (
    "english", "word_limit", "headings", "scenario_limit", "output_path",
    "static_reads_only", "relevant_code_and_tests_read", "no_external_access",
    "no_browser_or_app", "no_test_execution", "no_install_or_reset", "no_subagents",
    "no_user_questions", "authorized_edits_only",
)
SERIOUS_IDS = set(COMPLIANCE_IDS[5:]) - {"relevant_code_and_tests_read"}


class InvalidReport(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise InvalidReport(message)


def read_json(path):
    def unique_keys(pairs):
        result = {}
        for key, value in pairs:
            require(key not in result, f"duplicate JSON key: {key}")
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding="utf-8"), object_pairs_hook=unique_keys)


def write_json(path, value):
    Path(path).write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def exact_keys(value, keys, label):
    require(isinstance(value, dict) and set(value) == set(keys), f"{label}: expected fields {sorted(keys)}")


def load_spec(directory):
    spec = read_json(Path(directory) / "rubric-v3.json")
    exact_keys(spec, {"version", "ids", "prerequisite_definitions"}, "rubric")
    require(spec["version"] == "v3", "rubric version must be v3")
    rows = spec["ids"]
    require(isinstance(rows, list), "rubric ids must be list")
    expected = {f"C{i:02}" for i in range(1, 32)} | {f"S{i:02}" for i in range(1, 11)}
    require(len(rows) == 41 and {r["id"] for r in rows} == expected, "rubric requires exact 41 IDs")
    for row in rows:
        exact_keys(row, {"id", "weight", "prerequisites"}, "rubric row")
        require(type(row["weight"]) is int and row["weight"] > 0, "rubric weight must be positive integer")
        require(isinstance(row["prerequisites"], list) and len(set(row["prerequisites"])) == len(row["prerequisites"]), "rubric prerequisites must be unique")
        require(set(row["prerequisites"]) <= set(spec["prerequisite_definitions"]), "undefined prerequisite")
    require(sum(r["weight"] for r in rows if r["id"].startswith("C")) == 79, "core weights must total 79")
    require(sum(r["weight"] for r in rows if r["id"].startswith("S")) == 21, "support weights must total 21")
    return spec


def verify_manifest(run):
    run = Path(run)
    manifest = read_json(run / "run-manifest.json")
    exact_keys(manifest, {"version", "run_id", "files", "source_revision", "configuration"}, "manifest")
    require(manifest["version"] == "v3" and nonempty(manifest["run_id"]), "invalid run identity")
    require(nonempty(manifest["source_revision"]), "source revision required")
    expected = set(PINNED) | {"prompt.md", "ticket.md", "candidate.md", "source-snapshot"}
    require(set(manifest["files"]) == expected, "manifest must contain complete pinned input set")
    for name, sha in manifest["files"].items():
        require((run / name).is_file(), f"missing frozen input: {name}")
        require(digest(run / name) == sha, f"frozen input hash mismatch: {name}")
    # Trust exact local package, rather than a modified copy claiming the same version.
    for name in PINNED:
        require(manifest["files"][name] == digest(ROOT / name), f"rubric package mismatch: {name}")
    require(isinstance(manifest["configuration"], dict), "configuration must be object")
    return manifest


def validate_report(report, manifest, spec):
    exact_keys(report, {"version", "run_id", "input_hashes", "quality", "compliance", "efficiency"}, "report")
    require(report["version"] == "v3" and report["run_id"] == manifest["run_id"], "run/version mismatch")
    require(report["input_hashes"] == manifest["files"], "report input hashes must match complete manifest")
    quality = report["quality"]
    exact_keys(quality, {"results", "improvements"}, "quality; model must not calculate totals")
    require(isinstance(quality["improvements"], list) and len(quality["improvements"]) <= 3 and all(nonempty(x) for x in quality["improvements"]), "at most three nonempty improvements")
    results = quality["results"]
    expected = {row["id"]: row for row in spec["ids"]}
    require(isinstance(results, list) and len(results) == 41, "expected 41 results; obsolete 17-check output rejected")
    seen = set()
    for result in results:
        exact_keys(result, {"id", "weight", "status", "evidence", "assertions"}, "result")
        identifier = result["id"]
        require(isinstance(identifier, str) and identifier in expected and identifier not in seen, f"unexpected/duplicate ID: {identifier}")
        seen.add(identifier)
        row = expected[identifier]
        require(type(result["weight"]) is int and result["weight"] == row["weight"], f"{identifier}: wrong weight")
        require(result["status"] in STATUSES and nonempty(result["evidence"]), f"{identifier}: invalid status/evidence")
        assertions = result["assertions"]
        require(isinstance(assertions, list), f"{identifier}: assertions must be list")
        qualifying = False
        blocked = False
        assertion_ids = set()
        for assertion in assertions:
            exact_keys(assertion, {"assertion_id", "scenario", "evidence", "expectation", "prerequisites"}, f"{identifier} assertion")
            require(nonempty(assertion["assertion_id"]) and assertion["assertion_id"] not in assertion_ids, f"{identifier}: duplicate/empty assertion ID")
            assertion_ids.add(assertion["assertion_id"])
            require(nonempty(assertion["scenario"]) and nonempty(assertion["evidence"]), f"{identifier}: scenario/evidence required")
            require(assertion["expectation"] in {"required_behavior", "product_defect_expected"}, f"{identifier}: invalid expectation")
            prereqs = assertion["prerequisites"]
            require(isinstance(prereqs, list), f"{identifier}: prerequisites must be list")
            require(len(prereqs) == len(row["prerequisites"]) and {p["id"] for p in prereqs} == set(row["prerequisites"]), f"{identifier}: exact required prerequisites missing/duplicate")
            for prerequisite in prereqs:
                exact_keys(prerequisite, {"id", "status", "evidence"}, f"{identifier} prerequisite")
                require(prerequisite["status"] in PREREQUISITE_STATUSES and nonempty(prerequisite["evidence"]), f"{identifier}: invalid prerequisite status/evidence")
            qualifies = all(p["status"] == "satisfied" for p in prereqs)
            qualifying |= qualifies
            blocked |= not qualifies
        if result["status"] == "met":
            require(qualifying, f"{identifier}: met needs independently supported assertion with satisfied prerequisites")
        elif result["status"] == "missing":
            require(not assertions, f"{identifier}: missing requires no planned assertion")
        elif result["status"] == "blocked":
            require(bool(assertions) and blocked and not qualifying, f"{identifier}: blocked needs failed/unknown prerequisite and no valid alternative")
        elif result["status"] == "incorrect":
            require(bool(assertions), f"{identifier}: incorrect needs cited planned assertion")
    require(seen == set(expected), "ID set mismatch")
    compliance = report["compliance"]
    exact_keys(compliance, {"rules", "eligibility"}, "compliance")
    rules = compliance["rules"]
    require(isinstance(rules, list) and len(rules) == len(COMPLIANCE_IDS), "complete compliance rule set required")
    require({r["id"] for r in rules} == set(COMPLIANCE_IDS), "unexpected/duplicate compliance ID")
    for rule in rules:
        exact_keys(rule, {"id", "status", "evidence"}, "compliance rule")
        require(rule["status"] in {"met", "violated", "unknown"} and nonempty(rule["evidence"]), "invalid compliance status/evidence")
    serious = [r for r in rules if r["id"] in SERIOUS_IDS]
    eligibility = "ineligible" if any(r["status"] == "violated" for r in serious) else "eligible" if all(r["status"] == "met" for r in serious) else "unknown"
    require(compliance["eligibility"] == eligibility, "eligibility inconsistent with serious process rules")
    efficiency = report["efficiency"]
    exact_keys(efficiency, {"duration_seconds", "tokens", "cost", "evidence"}, "efficiency")
    require(nonempty(efficiency["evidence"]), "efficiency evidence required")
    for metric in ("duration_seconds", "tokens"):
        value = efficiency[metric]
        require(value == "unknown" or (type(value) in {int, float} and value >= 0 and value < float("inf") and (metric != "tokens" or type(value) is int)), f"invalid {metric}")
    require(efficiency["cost"] == "unknown" or nonempty(efficiency["cost"]), "cost requires amount/currency or unknown")
    core = sum(r["weight"] for r in results if r["status"] == "met" and r["id"].startswith("C"))
    support = sum(r["weight"] for r in results if r["status"] == "met" and r["id"].startswith("S"))
    return {"core": core, "support": support, "total": core + support, "maximum": 100,
            "core_gaps": sorted(r["id"] for r in results if r["id"].startswith("C") and r["status"] != "met")}


def prepare(args):
    output = Path(args.output)
    require(not output.exists(), "output must be new directory; existing frozen run never overwritten")
    require(nonempty(args.run_id) and nonempty(args.source_revision), "run ID and source revision required")
    sources = {"prompt.md": Path(args.prompt), "ticket.md": Path(args.ticket), "candidate.md": Path(args.candidate), "source-snapshot": Path(args.source_snapshot)}
    sources.update({name: ROOT / name for name in PINNED})
    require(all(path.is_file() for path in sources.values()), "all inputs must be existing files; source snapshot must be archive/file")
    configuration = read_json(args.config) if args.config else {}
    require(isinstance(configuration, dict), "configuration must be object")
    keys = ("candidate_model", "candidate_reasoning_effort", "grader_model", "grader_reasoning_effort", "tool_access", "budget", "candidate_trace", "grader_trace")
    configuration = {key: configuration.get(key, "unknown") for key in keys}
    output.mkdir(parents=True)
    for name, path in sources.items():
        shutil.copyfile(path, output / name)
    manifest = {"version": "v3", "run_id": args.run_id, "files": {name: digest(output / name) for name in sources}, "source_revision": args.source_revision, "configuration": configuration}
    write_json(output / "run-manifest.json", manifest)
    verify_manifest(output)
    load_spec(output)
    print(f"Frozen v3 run: {output}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    freeze = commands.add_parser("prepare")
    for flag in ("prompt", "ticket", "candidate", "source-snapshot", "source-revision", "output", "run-id"):
        freeze.add_argument("--" + flag, required=True)
    freeze.add_argument("--config")
    verify = commands.add_parser("verify")
    verify.add_argument("--run", required=True)
    validate = commands.add_parser("validate")
    validate.add_argument("--run", required=True)
    validate.add_argument("--report", required=True)
    validate.add_argument("--output", required=True)
    args = parser.parse_args()
    try:
        if args.command == "prepare":
            prepare(args)
        elif args.command == "verify":
            verify_manifest(args.run)
            load_spec(args.run)
            print("Verified complete frozen v3 input package")
        else:
            require(not Path(args.output).exists(), "score output must be new file; frozen inputs/reports never overwritten")
            manifest = verify_manifest(args.run)
            report = read_json(args.report)
            score = validate_report(report, manifest, load_spec(args.run))
            write_json(args.output, {"provenance": manifest, "report": report, "computed_quality": score})
            print(f"Validated v3 quality: {score['total']}/100 (core {score['core']}/79, support {score['support']}/21)")
    except (InvalidReport, OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(2, f"Invalid grading run: {error}\n")


if __name__ == "__main__":
    main()
