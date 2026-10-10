# QME-418 plan evaluation

The current guide is **v3**. It keeps the same 41 IDs and 100 points as v2, but requires usable prerequisites for each core assertion. Valid tests of broken product behavior retain credit. Invalid authored setup loses only dependent assertions. v2 remains available in `versions/plan-grading-template-v2.md` and at commit `f640072e2a12923d049d9c87cc3ba498adea1f17`; scores across versions are not comparable.

## Freeze before grading

Use a checkout at a fixed evaluation-repository commit. Save that commit with the host experiment record. Provide complete local input files and a source archive that represents the actual source revision and dirty state. A clean `git archive` is suitable only for clean source. For dirty source, include relevant uncommitted code and a file manifest/diff. Exclude prior grade reports, calibration answers, investigation artifacts and the candidate from the source archive; provide the candidate separately. Inspect the archive inventory before dispatch. Never expose prior grade names or scores to fresh graders.

For example, from this grading checkout:

```powershell
python tools/grading.py prepare --run-id repeat-01 --prompt ../inputs/prompt.md --ticket ../inputs/feature-ticket.md --candidate ../inputs/e2e-plan.md --source-snapshot ../inputs/source.zip --source-revision SOURCE_COMMIT --config ../inputs/config.json --output C:/wt/qme-418-runs/repeat-01
```

The output directory must be new. The command copies all eight required input files and hashes their exact bytes. `run-manifest.json` records source revision and configuration. Use `python tools/grading.py verify --run ...` before dispatch; `validate` verifies again before scoring. The host must preserve the manifest independently and keep the frozen directory read-only for graders. Hashes detect changes against the saved manifest; they are not signatures against a party who can rewrite both.

Optional configuration file fields are `candidate_model`, `candidate_reasoning_effort`, `grader_model`, `grader_reasoning_effort`, `tool_access`, `budget`, `candidate_trace`, and `grader_trace`. Values omitted become `unknown`. Record exact model IDs, reasoning, enabled tools, limits, host trace references and file-change evidence. Keep referenced trace files in the host evidence archive with their hashes; make only necessary candidate process evidence available to graders. Record grader trace after each run. An artifact alone cannot establish process compliance or efficiency.

Give each fresh grader the complete frozen package and manifest, using `grader-instructions.md` as its instructions. Include source files through extraction/read-only access as needed; do not silently replace the snapshot with live source. Ask for raw JSON only. Keep repeated runs independent, using matching input hashes, configuration and budgets. Do not show past outputs during repeats.

## Validate and score

```powershell
python tools/grading.py validate --run C:/wt/qme-418-runs/repeat-01 --report C:/wt/qme-418-runs/raw-01.json --output C:/wt/qme-418-runs/scored-01.json
python -m unittest discover -s tests -v
```

Python 3.10+ and its standard library suffice. Validation rejects obsolete 17-check reports, missing/duplicate/unknown IDs, wrong weights/statuses, missing prerequisites, assertions marked met despite invalid setup, fabricated model totals and input drift. It computes core, support and total points and core gaps itself. Quality, compliance and efficiency remain separate.

Use the **matching grading commit and validator** when replaying a historical frozen v3 run. The validator checks its local package hashes against the frozen copy; a later package revision deliberately rejects the old run. The complete package is the guide, ID manifest, schema and grader instructions, not just one Markdown URL. Exact byte hashes may differ between LF/CRLF checkouts; use the frozen bytes for repeat runs and record the checkout commit plus hashes.

Mechanical validation checks structure and declared prerequisite consistency. It cannot prove that citations or semantic decisions are correct. Review fixture decisions and disputed per-ID results; do not average disagreements into a gold score. Correct arithmetic on an unreachable recipe can earn S05 while dependent core IDs remain blocked.

## Calibration and comparisons

Development probes and expected per-ID decisions are in `calibration/development.json`; held-out probes are in `calibration/held-out.json`. They contain concrete candidate snippets, source facts, narrow focus IDs and rationale. The valid-plan probe covers all 41 IDs. Other probes are intentionally scoped; their totals measure only listed IDs, not complete-plan grades. Do not expose expected decisions to graders. Prepare each probe as candidate text with its stated source facts, then compare fresh outputs to the expected decisions on focus IDs.

Run at least three independent grades per development case with the intended configuration. Record per-ID status, failed prerequisite, agreement count and adjudication; inspect drift before freezing the rubric. Evaluate held-out cases after policy tuning, without changing answers to suit scores. Report both development and held-out per-ID agreement and unresolved disagreements. Keep held-out answers outside tuning context. If held-out content becomes tuning input, retire it and add new cases before claiming held-out model performance.

`calibration/RESULTS.md` records the actual deterministic checks performed for this implementation and the lack of fresh-model repeatability evidence. No source/task/candidate/old grade is regraded or changed by this package. Regrade all candidates used in a comparison under the same v3 commit before comparing quality. Compare eligibility and host efficiency separately, with unknowns explicit.
