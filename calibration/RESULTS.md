# v3 calibration evidence — 2026-10-10

The implementation passed **11 standard-library unittest methods**, including all ten policy fixtures, CLI freezing/verification/scoring and malformed-output rejection. Source anchors and fixture arithmetic were reviewed statically against source revision `88bdafdf4855cae8acea65f536fa0e5f98c08f6e`. This is deterministic validator and policy-fixture evidence. **No fresh-model grading runs, repeated-grader agreement measurement or new candidate grade were performed.**

Command: `python -m unittest discover -s tests -v`. Result: `Ran 11 tests … OK`. Test-generated files use a temporary directory under `C:/wt` on Windows and are cleaned after each test. The preserved v2 copy matches the historical Git blob after newline normalization; the v3 versioned guide matches the current guide byte for byte.

## Per-ID fixture decisions checked

Expected decisions were authored from the stated source facts and reviewed for policy consistency. The harness constructs structured results from those decisions, then validates prerequisites and sums independently. It does not ask a model to interpret the snippets. Unlisted IDs in scoped probes are missing; totals below are probe totals, **not full-plan candidate scores**. Only the valid-plan probe covers all 41 IDs.

| Probe | Expected decisions | Failed prerequisite | Computed points |
| --- | --- | --- | ---: |
| Valid plan | C01–C31, S01–S10 met | None | 100 |
| Invalid normal setup | C01–C03, S01, S05, S08 met; C04–C15, C17–C18, C31 blocked; S02 incorrect | `normal_admissible`, `initial_and_changed_admissible`, `nonfood_admissible`: invalid authored setup | 12 |
| Invalid correction | C19–C23, S01, S08 met; C24 blocked; S02 incorrect | `correction_admissible`: invalid authored setup | 18 |
| Valid product-defect assertion | C17, C18 met | None; missing product guidance is asserted behavior | 9 |
| Omitted guidance | C17 met; C18 missing | None | 4 |
| Correct oracle, immaterial rounding | S05 met | None; whole-penny contributions/no applicable discount or exchange effect | 5 |
| Held-out disabled selection | C19–C24 blocked | `evaluable_rejection`: invalid authored setup | 0 |
| Held-out independent edit | C05 blocked; C25–C30 met; S02 incorrect | `normal_admissible` invalid; independent saved-line/edit prerequisites satisfied | 12 |
| Held-out material rounding | C04, S02 met; S05 incorrect | None; wrong oracle rounds after summing instead of each contribution | 4 |
| Held-out alternative guidance | C18 met | First instance invalid; independent second instance satisfies `nonfood_admissible` | 5 |

The material-rounding probe independently verifies unit contributions `7339`, `644`, `644` pence, giving `37008` pence total. Summing raw contributions instead gives `37012`; rounding is material in this case. The valid oracle probe gives `41620` pence without requiring an explanation of immaterial operations.

## Rejection and separation checks

- Obsolete 17-check output, duplicate/unknown IDs, wrong/boolean weights, obsolete statuses, empty evidence, model totals/normalization and wrong run version/hash rejected.
- Missing/wrong/duplicate prerequisites and duplicate assertion IDs rejected. `met` with invalid or unknown prerequisite rejected; explicit `blocked` accepted at zero credit. `missing` cannot carry a present assertion; `blocked` cannot discard a valid alternative.
- Valid product-defect assertions and valid alternatives retain full ID credit. Invalid correction retains independently reachable rejection IDs. Independent edit survives unrelated invalid create setup.
- Unknown host trace yields unknown eligibility and metrics. Word-limit or serious process violations do not change quality total; serious violations require ineligible status. Negative token counts rejected.
- Prepare copies/hashes the complete package; verify checks it before dispatch. Validate repeats those checks and calculates totals. Missing/tampered frozen inputs and a modified rubric with a rewritten hash rejected against the matching local package. Existing frozen run/output files cannot be overwritten. Duplicate JSON keys rejected.

## Remaining uncertainty

Fresh grader semantic accuracy and per-ID repeatability remain **unknown**. No agreement percentage, confidence interval or claimed model-calibration success follows from these tests. The validator trusts cited semantic decisions; it cannot prove an actual recipe, assertion or process claim from nonempty text. Host semantic review remains necessary.

Held-out fixtures are distinct from development cases and were not used for model tuning or a desired candidate total. Their answers were nevertheless inspected for implementation QA. They remain suitable as initial fresh-model probes with answers withheld; they do not constitute untouched empirical held-out performance evidence. If used to tune the grader/rubric, retire them and add new held-out cases.

Next experiment: freeze this package commit, source/candidate/configuration and traces; run at least three fresh grades per development case, then held-out probes. Record per-ID status/prerequisite agreement, disagreements and adjudication. Do not average conflicting decisions or adjust gold answers toward a target score. Historical 96/93/71 reports remain unchanged and are not v3 calibration outcomes.
