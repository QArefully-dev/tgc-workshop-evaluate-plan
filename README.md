# QME-418 plan evaluation

The complete v4 rubric and grader instructions are in [plan-grading-template.md](plan-grading-template.md). Give one grader that guide, the task or prompt, ticket, candidate plan, and relevant source checkout. For example, ask: “Read the grading guide, task, ticket, candidate plan, and relevant source. Return the required Markdown report with exactly 41 `ID | Status | Evidence` rows, plus the summed core/support/total score and core gaps.”

Save the report as Markdown and score it from the repository root:

```powershell
python tools/grading.py report.md
```

The checker requires the 41 known IDs exactly once, `met` or `not_met` statuses, and nonempty evidence. It prints core points, support points, total points, and core gaps. Python's standard library is sufficient. Run the focused checker tests with `python -m unittest discover -s tests -v`.

Scores from different rubric versions are not comparable. For comparisons, use the same v4 grading-repository commit and source revision, and keep the task, ticket, and candidate fixed. Optional experiment notes can record those commits, model/configuration, and available run trace; no calibration campaign is required. The v2 and v3 guides in `versions/` are historical references.
