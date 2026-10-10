"""Score a v4 Markdown grading report; standard library only."""
import argparse
import re
import sys
from pathlib import Path

CORE_WEIGHTS = {
    "C01": 2, "C02": 1, "C03": 1, "C04": 2, "C05": 3, "C06": 3,
    "C07": 2, "C08": 1, "C09": 2, "C10": 5, "C11": 4, "C12": 2,
    "C13": 1, "C14": 2, "C15": 1, "C16": 4, "C17": 4, "C18": 5,
    "C19": 3, "C20": 4, "C21": 3, "C22": 3, "C23": 2, "C24": 4,
    "C25": 2, "C26": 2, "C27": 2, "C28": 2, "C29": 2, "C30": 2,
    "C31": 3,
}
SUPPORT_WEIGHTS = {"S01": 2, "S02": 2, "S03": 3, "S04": 2, "S05": 5,
                   "S06": 2, "S07": 2, "S08": 1, "S09": 1, "S10": 1}
WEIGHTS = CORE_WEIGHTS | SUPPORT_WEIGHTS


def require(condition, message):
    if not condition:
        raise ValueError(message)


def cells(line, number):
    line = line.strip()
    require(line.startswith("|") and line.endswith("|"), f"line {number}: malformed Markdown table row")
    return [cell.strip() for cell in line[1:-1].split("|")]


def score_report(text):
    lines = text.splitlines()
    headers = [i for i, line in enumerate(lines) if line.strip().startswith("|")
               and line.strip().endswith("|") and cells(line, i + 1) == ["ID", "Status", "Evidence"]]
    require(len(headers) == 1, "expected one table headed | ID | Status | Evidence |")
    rows, index = [], headers[0] + 1
    if index < len(lines) and all(re.fullmatch(r":?-{3,}:?", x) for x in cells(lines[index], index + 1)):
        index += 1
    while index < len(lines) and lines[index].strip().startswith("|"):
        row = cells(lines[index], index + 1)
        require(len(row) == 3, f"line {index + 1}: expected three columns")
        rows.append(row)
        index += 1
    require(len(rows) == 41, f"expected exactly 41 result rows, found {len(rows)}")
    seen, earned = set(), set()
    for offset, (identifier, status, evidence) in enumerate(rows, headers[0] + 2):
        require(identifier in WEIGHTS, f"row {offset}: unknown ID {identifier!r}")
        require(identifier not in seen, f"row {offset}: duplicate ID {identifier}")
        require(status in {"met", "not_met"}, f"row {offset} ({identifier}): status must be met or not_met")
        require(bool(evidence.strip()), f"row {offset} ({identifier}): evidence is empty")
        seen.add(identifier)
        if status == "met":
            earned.add(identifier)
    require(seen == set(WEIGHTS), "result rows do not contain the complete known ID set")
    core = sum(CORE_WEIGHTS[i] for i in earned if i in CORE_WEIGHTS)
    support = sum(SUPPORT_WEIGHTS[i] for i in earned if i in SUPPORT_WEIGHTS)
    return {"core": core, "support": support, "total": core + support,
            "core_gaps": sorted(set(CORE_WEIGHTS) - earned)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("report", help="Markdown report with the 41-row ID/Status/Evidence table")
    args = parser.parse_args()
    try:
        score = score_report(Path(args.report).read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        parser.exit(2, f"Invalid grading report: {error}\n")
    print(f"Score: {score['total']}/100 (core {score['core']}/79; support {score['support']}/21)")
    print("Core gaps: " + (", ".join(score["core_gaps"]) or "none"))


if __name__ == "__main__":
    main()
