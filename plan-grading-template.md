# QME-418 browser plan grading guide — v4 (2026-10-10)

Grade how well a proposed browser plan covers the task and ticket AC1–AC5. Read this guide, the task/prompt, ticket, candidate plan, and relevant source files. Judge the plan against the source and ticket; do not require the product to already work. This guide is the complete rubric and grader instruction.

## How to grade

Return one Markdown report with exactly 41 result rows in this form:

| ID | Status | Evidence |
|---|---|---|
| C01 | met | Scenario 1: guest opens the configurator from category navigation. |

Use each ID once. Status is `met` or `not_met`. Give one short, concrete reason per row, pointing to a scenario/action or the missing, incorrect, or unusable coverage. `met` earns the full listed weight; `not_met` earns zero. There is no partial credit. Do not add subtables, nested assertions, or JSON. Mention a failed setup prerequisite in the evidence only when it explains a `not_met` result.

Judge whether the plan can attempt the assertion with a usable setup. A valid test of behavior that source code shows is defective earns coverage when the plan checks the expected behavior or exposes the defect. Do not penalize coverage just because the product is broken, and do not treat a product defect as a substitute for an omitted assertion. An impossible setup blocks only assertions that depend on it. A valid alternative scenario, independent fixture, or saved cart line can still earn the relevant IDs. Do not infer a successful journey from an invalid setup.

Core setup guidance by ID:

- C01: guest can enter from public category navigation; login is not required.
- C02–C03: the named base and at least one named ingredient are source-supported and selectable for the journey. Material existence and compatibility are checked separately for food, non-food, and correction journeys under S01.
- C04: normal recipe is admissible. C05–C09, C31, and C15: admissible recipe plus a usable guest/cart/quantity path to attempt add or price-consistency assertions. A product add defect does not invalidate the setup.
- C10–C12 and C14: both initial and changed recipes are admissible, and the ratio change can be evaluated. C13: admissible normal recipe.
- C16: admissible food-compatible recipe. C17–C18: admissible non-food recipe reaches the summary. Missing guidance is a product assertion, not a setup failure.
- C19–C23: a UI-constructible, structurally valid combination reaches evaluation and is rejected for a source-supported compatibility or policy reason. A disabled choice or invalid field alone is not an evaluated rejection. C24 also needs a specific admissible correction and a usable add attempt.
- C25–C27: an independent valid saved-line fixture or reachable successful add establishes the original composition. C28–C30 also need an admissible changed recipe and a save attempt. A valid independent saved-line fixture counts even if an earlier create journey is invalid.

Use the supplied source checkout for exact materials, amounts, fees, labels, wording, and rejection recipes; they are not fixed answers. Baseline bounds are 5–50% per ingredient, at most 50% combined ingredients, 50–95% base, and at most 10% combined pigment. A stated four-bag default is acceptable when the minimum order is stated; do not assume one bag can be bought. For AC2, an explicit no-reload check or visible in-place update counts; merely omitting navigation does not. For AC3, handling guidance must be readable in the summary; assistive-only or tiny text does not count. For AC4, rejection must be evaluated; a disabled Add control with an unchanged cart is sufficient to show it cannot be added, and an impossible click is unnecessary. C24 requires a valid correction that successfully adds.

After the 41 rows, state the score and core gaps: `Score: <core>/79 core + <support>/21 support = <total>/100; core gaps: <IDs or none>.` Sum the listed weights for rows marked `met`; the checker is optional and can verify your arithmetic. Then add a brief `Compliance and efficiency` paragraph. Summarize artifact constraints (English, at most 1,500 words, required level-two headings `Scenarios`, `Existing coverage`, `Risks`, `Approach`, at most four scenarios, required output path) separately from quality. For process compliance, report only what the available trace or file evidence supports: static repository reads, relevant code/E2E/lower-level coverage read, no external access/browser/app startup/test execution/install/database reset/subagents/user questions, and no implementation or unrelated edits. A trace verifies actions; a file diff or snapshot verifies edits. State `unknown` where evidence is absent. Mark eligibility `ineligible` for a verified serious forbidden action or unauthorized edit, `eligible` only when all serious constraints are verified, and otherwise `unknown`; missing evidence that relevant files were read is reported separately and is not itself a serious violation. Give host-reported duration/tokens/cost separately, or `unknown`; do not infer efficiency from plan length or score. Compliance does not change quality points.

## Quality rubric — 100 points

### AC1 — 20 points

| ID | Weight | What the plan covers |
|---|---:|---|
| C01 | 2 | Guest reaches the configurator from category navigation without login. |
| C02 | 1 | Guest selects a base material. |
| C03 | 1 | Guest selects at least one ingredient. |
| C04 | 2 | Guest sets valid proportions. |
| C05 | 3 | Add produces exactly one blend cart line. |
| C31 | 3 | Added cart line shows chosen base, ingredients, and proportions. |
| C06 | 3 | Cart shows the blend total. |
| C07 | 2 | Continue-shopping option is checked after add. |
| C08 | 1 | Checkout option is checked after add. |
| C09 | 2 | Checkout option destination is checked without completing checkout. |

### AC2 — 15 points

| ID | Weight | What the plan covers |
|---|---:|---|
| C10 | 5 | Ratio change updates material cost in the summary. |
| C11 | 4 | The same change updates the blend total in the summary. |
| C12 | 2 | Both updates occur without reload. |
| C13 | 1 | Summary shows the blending fee. |
| C14 | 2 | The same ratio change preserves the flat blending fee. |
| C15 | 1 | Summary and cart prices are checked for consistency. |

### AC3 — 13 points

| ID | Weight | What the plan covers |
|---|---:|---|
| C16 | 4 | Food-compatible blend shows food classification in the summary. |
| C17 | 4 | Non-food blend shows non-food classification in the summary. |
| C18 | 5 | Non-food summary shows readable handling guidance. |

### AC4 — 19 points

| ID | Weight | What the plan covers |
|---|---:|---|
| C19 | 3 | Evaluation rejects a concrete UI-permitted combination. |
| C20 | 4 | Rejection shows a clear visible reason. |
| C21 | 3 | Rejected blend cannot be added. |
| C22 | 3 | Cart remains unchanged after evaluated rejection. |
| C23 | 2 | Rejected configuration remains available for correction. |
| C24 | 4 | Corrected configuration successfully adds the blend. |

### AC5 — 12 points

| ID | Weight | What the plan covers |
|---|---:|---|
| C25 | 2 | Edit restores the original base. |
| C26 | 2 | Edit restores the original ingredients. |
| C27 | 2 | Edit restores the original proportions. |
| C28 | 2 | Save replaces the same cart line without a duplicate. |
| C29 | 2 | Saved cart line shows the changed composition. |
| C30 | 2 | Saved cart line shows the changed price. |

### Feasibility and evidence — 21 points

| ID | Weight | What the plan covers |
|---|---:|---|
| S01 | 2 | Named materials/SKUs, eligibility, and directional compatibility support otherwise-present food, non-food, and correction journeys; identify uncertainty. Repository-consistent fixture assumptions count even if a live seed is unverified, when uncertainty is stated; an unverified live seed alone does not invalidate a documented source fixture. Assess materials separately from percentages; a deliberate rejection recipe belongs to C19. |
| S02 | 2 | Otherwise-present normal and correction ratios satisfy structural bounds and policy caps; consider UI clamping. Rejection recipes belong to C19. |
| S03 | 3 | Quantity states a 25 kg bag basis and applicable minimum order. |
| S04 | 2 | Country and currency are stated for price expectations. |
| S05 | 5 | Independent, correct oracle: `sum(resolved component unit contributions) × quantity + flat fee once`. Cited repository prices/proportions and reproducible expected amounts before UI observation count. Apply relevant tier, rounding, and exchange effects correctly. Immaterial explanation of zero discount, whole-penny rounding, or 1:1 currency is unnecessary. Correct independent arithmetic can count even for an inadmissible recipe or a valid edit oracle; reachability is covered by prerequisites/S02. A consistency-only check is insufficient; an exhaustive matrix is unnecessary. |
| S06 | 2 | Each scenario owns its guest session/cart and does not depend on another scenario. |
| S07 | 2 | Each scenario has a priority and brief risk rationale; order follows risk. |
| S08 | 1 | Numbered user actions, visible expected results, and AC mapping give the plan structure. Assess structure separately from setup validity. |
| S09 | 1 | Key code/ticket findings are sourced; unverified assumptions and material ticket/code differences are identified without invented browser observations. |
| S10 | 1 | Relevant existing E2E/lower-level coverage is summarized and the browser plan's representative contribution is explained. Lower-level coverage can reduce redundant variants, not replace representative browser coverage. |

The weights total 79 core points (C01–C31) and 21 support points (S01–S10). The same ratio error can fail S02 and dependent core IDs; do not also deduct it under S01 or S08. The optional checker computes the score from your report: `python tools/grading.py report.md`.
