# QME-418 plan grading guide — v2 (2026-10-07)

Grade `workshop/e2e-plan.md` against pinned `workshop/prompt.md` and `workshop/feature-ticket.md`. Score proposed browser coverage of AC1–AC5, not current application pass/fail. v2 scores cannot be compared with old-guide scores; regrade old artifacts under v2.

## Evidence and decision rules

- Host records task-input SHA-256 for exact prompt, ticket, and guide; repository HEAD plus working-tree diff or saved source snapshot when dirty. Record candidate output SHA-256 separately. Record run ID, exact candidate model ID and reasoning effort, grader model ID and reasoning effort if distinct, tool access, budget, process trace, duration, tokens, and cost where known. Missing field -> `unknown`, never guessed. Compare runs with matching task inputs, repository state, rubric, and materially alike tool/budget conditions; candidate outputs and model configurations may differ as experiment variables. Disclose differences.
- Per ID: `met` -> full listed weight; `missing/incorrect` -> 0. Cite scenario/short phrase or precise absence. Sum weights mechanically; no rounding, normalization, or inferred credit. Shared setup counts. Equivalent wording, data, scenario combinations, and ordering count. Score each distinct assertion independently: missing/unreachable evaluation-rejection recipe -> C19 only; S01/S02 cover otherwise present normal/correction data, and other AC4 assertions retain credit when explicitly planned. Missing restored base -> C25 only. Do not zero unrelated evidence or executable-scenario IDs solely for either gap.
- Core gaps -> list missing C IDs regardless of total. Never infer behavior from AC labels or titles. Planned ticket assertion earns credit even when expected to fail in current code; exact defect diagnosis unnecessary, and current defect never substitutes for missing assertion. Lower-level tests justify omitting exhaustive variants, not representative browser coverage of an AC.
- AC2: explicit no-reload assertion or visible in-place update counts; no navigation alone does not prove no reload. AC3: guidance must be visibly readable in summary; assistive-only or tiny text fails C18. AC4: rejection must follow evaluation of UI-constructible combination; disabled selection or invalid field entry alone fails C19.
- Exact products, prices, fees, labels, error wording, and rejection recipe are not fixed answers. Static facts for calibration: generic per-ingredient ratio cap 50%; combined pigment cap 10%; material subtotal from summed, resolved per-component unit contributions × quantity, plus one flat blending fee. Evaluator may default to four 25 kg bags for minimum order; one bag cannot be assumed purchasable. Readable guidance remains required despite current code defect.

## Content quality — 100 points

Each ID tests one observable assertion or planning requirement. C IDs -> core, 79 points. S IDs -> feasibility/evidence, 21 points. No fractional credit within ID.

### AC1 — 20 points

- C01 `2`: Guest reaches configurator from category navigation without login.
- C02 `1`: Guest selects base material.
- C03 `1`: Guest selects at least one ingredient.
- C04 `2`: Guest sets valid proportions.
- C05 `3`: Add produces exactly one blend cart line.
- C31 `3`: Added cart line shows chosen base, ingredients, and proportions.
- C06 `3`: Cart shows blend total.
- C07 `2`: Continue-shopping option checked after add.
- C08 `1`: Checkout option checked after add.
- C09 `2`: Checkout option destination checked, without completing checkout.

### AC2 — 15 points

- C10 `5`: Ratio change updates material cost in summary.
- C11 `4`: Same change updates blend total in summary.
- C12 `2`: Both updates occur without reload.
- C13 `1`: Summary shows blending fee.
- C14 `2`: Same change preserves flat blending fee.
- C15 `1`: Summary and cart prices checked for consistency.

### AC3 — 13 points

- C16 `4`: Food-compatible blend shows food classification in summary.
- C17 `4`: Non-food blend shows non-food classification in summary.
- C18 `5`: Non-food summary shows readable handling guidance.

### AC4 — 19 points

- C19 `3`: Evaluation rejects concrete UI-permitted combination.
- C20 `4`: Rejection shows clear visible reason.
- C21 `3`: Rejected blend cannot be added.
- C22 `3`: Cart remains unchanged after evaluated rejection; disabled Add plus unchanged cart counts without impossible click.
- C23 `2`: Rejected configuration remains available for correction.
- C24 `4`: Corrected configuration successfully adds blend.

### AC5 — 12 points

- C25 `2`: Edit restores original base.
- C26 `2`: Edit restores original ingredients.
- C27 `2`: Edit restores original proportions.
- C28 `2`: Save replaces same cart line; no duplicate.
- C29 `2`: Saved cart line shows changed composition.
- C30 `2`: Saved cart line shows changed price.

### Feasibility and evidence — 21 points

- S01 `2`: Named materials support food, non-food, and correction journeys. Credit concrete repository-consistent fixture assumptions with uncertainty identified; known contradictory or unreachable normal/correction data fail. Rejection recipe belongs to C19.
- S02 `2`: Ratios support otherwise present valid and correction states. Rejection recipe belongs to C19.
- S03 `3`: Quantity states 25 kg bag basis and applicable minimum order; four-bag default accepted when stated.
- S04 `2`: Country and currency stated for price expectations.
- S05 `5`: Independent price oracle: `sum(resolved component unit contributions) × quantity + flat fee once`. Derive contributions independently from cited repository prices/proportions and applicable tier, rounding, and currency rules; controlled reproducible expected amounts count before UI observation. Summary/cart consistency alone insufficient; exhaustive matrix unnecessary.
- S06 `2`: Each scenario owns guest session and cart; no order dependence.
- S07 `2`: Each scenario has priority and brief risk rationale; order follows risk.
- S08 `1`: Numbered user actions, visible expected results, and AC mapping make scenarios executable.
- S09 `1`: Key code/ticket findings sourced; unverified assumptions and material ticket/code differences identified without invented browser observations.
- S10 `1`: Relevant existing E2E/lower-level coverage summarized and representative browser contribution explained without exhaustive matrix.

## Compliance — separate from quality

Report each rule `met`, `violated`, or `unknown`, with artifact or host trace evidence. Artifact proves format, not silent process compliance. Otherwise correct 1,600-word plan keeps same quality score but violates word limit. Missing trace -> affected process rule `unknown`, never `met`.

- Artifact rules: English; at most 1,500 words; exact required level-two headings in order (`Scenarios`, `Existing coverage`, `Risks`, `Approach`); at most four scenarios; required output path. Report ordinary format issues separately; no quality subtraction or automatic serious violation. Edits outside authorized path are process violations.
- Process rules: static repository-file reading only; code plus directly relevant E2E and lower-level tests read; no external access, browser, app startup, test execution, dependency install, database reset, subagents, or user questions; no test/application implementation or unrelated edits. Host command/process trace verifies actions; host file diff/snapshot verifies actual file changes. Plan claims alone never establish file-change compliance.
- Eligibility: verified serious violation of forbidden process or unauthorized edit -> `ineligible`, even when other evidence missing. Complete host evidence verifying all serious process constraints -> `eligible`. Otherwise -> `unknown`. Artifact quality remains reportable for every state; ordinary format violations reported separately.

## Efficiency — separate from quality and compliance

Host logs only -> duration, tokens, cost where known. Missing metric -> `unknown`. Never infer from plan length or score. Low-token incomplete plan does not win automatically. No combined quality/compliance/efficiency score.

## Grader output

- Provenance: guide version; separate task-input hashes (prompt, ticket, guide), repository revision/dirty diff or snapshot, and candidate-output hash; exact candidate model ID/reasoning effort, grader configuration if distinct, tool/budget/run metadata or `unknown`.
- Quality: `N/100`; per-ID `met`/`missing` with weight and evidence; core gaps; up to three highest-impact improvements.
- Compliance: per-rule status/evidence; serious violation and comparison eligibility.
- Efficiency: host metrics or `unknown`; compare only like conditions.
