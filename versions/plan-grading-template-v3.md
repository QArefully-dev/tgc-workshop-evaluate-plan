# QME-418 plan grading guide — v3 (2026-10-10)

Grade proposed browser coverage of pinned prompt/ticket AC1–AC5. Product pass/fail separate from plan quality. v3 supersedes v2 prospectively; compare only candidates regraded under identical pinned v3 package. Historical v2 preserved in `versions/plan-grading-template-v2.md`; original commit `f640072e2a12923d049d9c87cc3ba498adea1f17`. Never retrofit v3 onto historical reports.

## Input gate

Host freezes exact prompt, ticket, candidate, source snapshot, complete guide, ID/prerequisite manifest, output schema, grader instructions and configuration before grading. Use `tools/grading.py prepare`; source revision + snapshot required, dirty source represented by snapshot. Record all SHA-256 values. Missing/truncated/mismatched package -> invalid run, no guessed score. Stable `main` URL insufficient: resolve fixed commit or immutable local package. Host verifies hashes before grading and before scoring.

Prior grades/expected calibration decisions remain outside fresh grader context. Freeze candidate and source across repeats; record candidate/grader exact model IDs, reasoning, tools, budget, trace, duration, tokens and cost. Missing evidence -> `unknown`. Compare like conditions; disclose experiment variables. See `README.md` for host workflow.

## Evidence and prerequisite decisions

- Exactly 41 IDs; C01–C31 -> 79 points; S01–S10 -> 21 points. `met` -> full weight; `missing`, `incorrect`, `blocked` -> zero. No partial credit, caps, normalization or model-calculated totals. Host validator sums weights.
- Per ID: cite candidate location/short phrase, scenario/state, assertion expectation, and each required prerequisite from `rubric-v3.json`. `missing`: assertion absent. `incorrect`: present assertion/oracle wrong. `blocked`: otherwise planned assertion has invalid authored setup or unresolved material prerequisite. `met`: at least one independently supported assertion with satisfied prerequisites.
- Prerequisite status: `satisfied`, `invalid_authored_setup`, `unknown`, each with source/candidate evidence. Repository-consistent fixture assumptions suffice; unverified live seed alone does not invalidate documented source fixture. Contradiction with frozen source -> invalid setup. Missing material information preventing decision -> unknown, disclose gap.
- Prerequisites establish ability to attempt required feature behavior; do not require product already implements behavior correctly. Valid setup + explicit required assertion exposing product defect -> credit, expectation `product_defect_expected` accepted. Defect diagnosis optional. Feature defect never substitutes for missing assertion.
- Authored impossible setup loses only assertions depending on that setup. No blanket scenario zero or protected imagined success. Example: pigment 6% + 5% reaches rejection; correction 6% + 4% clamps second ingredient to 5%, remains rejected -> C19–C23 can pass, C24 blocked. Pigment 25% -> 40% normal journey exceeds 10% cap -> successful repricing/non-food/add assertions blocked unless independently covered elsewhere.
- Each core ID has explicit prerequisite set in manifest. Shared setup and alternative valid scenarios count. Valid independent saved-line fixture supports edit IDs even when separate creation scenario invalid. If plan claims edit fixture comes solely from impossible earlier add, edit-dependent IDs blocked. Judge evidence per assertion, not AC label/title. Lower-level tests justify fewer variants, not omission of representative browser coverage.
- AC2: explicit no-reload or visible in-place updates count; no navigation alone insufficient. AC3: guidance visibly readable in summary; assistive-only/tiny text fails C18. AC4 C19–C23 require evaluable rejection; C24 additionally requires admissible correction. Disabled choice or invalid field alone cannot establish evaluation rejection. Disabled Add plus unchanged cart suffices; impossible click unnecessary.
- Exact products, amounts, fees, labels/error wording and rejection recipes not fixed answers. Check frozen source. Baseline bounds: ingredients 5–50% each; combined ingredient total at most 50%; base 50–95%; combined pigment at most 10%. Four 25 kg bags accepted when minimum order stated; one bag not assumed purchasable.

## Content quality — 100 points

Manifest IDs/weights match following assertions; prerequisite definitions supplement every C ID. S IDs assess distinct planning evidence. Same authored ratio error can lose S02 and dependent core coverage; S01/S08 cannot apply additional ratio/executability penalties.

### AC1 — 20 points

- C01 `2`: Guest reaches configurator from category navigation without login.
- C02 `1`: Guest selects base material.
- C03 `1`: Guest selects at least one ingredient.
- C04 `2`: Guest sets valid proportions.
- C05 `3`: Add produces exactly one blend cart line.
- C31 `3`: Added cart line shows chosen base, ingredients and proportions.
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
- C15 `1`: Summary/cart prices checked for consistency.

### AC3 — 13 points

- C16 `4`: Food-compatible blend shows food classification in summary.
- C17 `4`: Non-food blend shows non-food classification in summary.
- C18 `5`: Non-food summary shows readable handling guidance.

### AC4 — 19 points

- C19 `3`: Evaluation rejects concrete UI-permitted combination.
- C20 `4`: Rejection shows clear visible reason.
- C21 `3`: Rejected blend cannot be added.
- C22 `3`: Cart remains unchanged after evaluated rejection.
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

- S01 `2`: Named material/SKU existence, eligibility and directional compatibility support otherwise present food, non-food and correction journeys. Repository-consistent fixture assumptions with uncertainty identified count. Assess materials independently of percentages; ratio failures belong to S02. Rejection recipe belongs to C19.
- S02 `2`: Otherwise present normal/correction ratios satisfy structural bounds and policy caps. Deliberate rejection recipe belongs to C19. Check UI clamping when correction uses out-of-range ratio.
- S03 `3`: Quantity states 25 kg bag basis and applicable minimum order; stated four-bag default accepted.
- S04 `2`: Country and currency stated for price expectations.
- S05 `5`: Independent correct oracle: `sum(resolved component unit contributions) × quantity + flat fee once`. Cited repository prices/proportions plus correct reproducible expected amounts count. Material applicable tier, rounding and exchange effects must be correctly reflected. No requirement to explain zero discount, whole-penny rounding or 1:1 currency when immaterial; no deduction solely for omitting such explanation. Controlled reproducible expected amounts count before UI observation; consistency-only assertion insufficient. Correct arithmetic on inadmissible recipe can earn S05; reachability belongs to core prerequisites/S02. Valid independently calculated edit oracle also counts. Incorrect applicable arithmetic/rules fail; exhaustive matrix unnecessary.
- S06 `2`: Each scenario owns guest session/cart; no order dependence.
- S07 `2`: Each scenario has priority and brief risk rationale; order follows risk.
- S08 `1`: Numbered user actions, visible expected results and AC mapping provide scenario structure. Assess structure only; setup admissibility assessed by prerequisites/S01/S02.
- S09 `1`: Key code/ticket findings sourced; unverified assumptions and material ticket/code differences identified without invented browser observations.
- S10 `1`: Relevant existing E2E/lower-level coverage summarized; representative browser contribution explained without exhaustive matrix.

## Compliance — separate from quality

Per rule `met`, `violated`, `unknown` + artifact/host evidence. Artifact proves format, never silent process compliance. Otherwise correct 1,600-word plan retains quality; word-limit violation reported separately. Trace missing -> affected process rule unknown.

- Artifact: English; at most 1,500 words; exact level-two headings in order (`Scenarios`, `Existing coverage`, `Risks`, `Approach`); at most four scenarios; required output path. Ordinary format violations -> no quality subtraction or automatic ineligibility.
- Process: static repository-file reading only; relevant code/E2E/lower-level tests read; no external access, browser/app startup, test execution, install/database reset, subagents or user questions; no test/app implementation or unrelated edits. Host command/process trace verifies actions; file diff/snapshot verifies actual edits. Plan claims insufficient. Restrictions govern candidate run; host may run grading validator/calibration tests.
- Eligibility: any verified serious forbidden process/unauthorized edit -> `ineligible`; all serious constraints verified -> `eligible`; otherwise `unknown`. Missing relevant-read evidence reported separately, not automatically serious. Quality remains reportable regardless of eligibility.

## Efficiency — separate from quality/compliance

Host metrics only: duration, tokens, amount/currency cost or `unknown`. No inference from length or score, no combined score. Low-token incomplete plan not automatically better.

## Grader output

Return only JSON matching `report-schema.json`; follow `grader-instructions.md`. Complete per-ID evidence/prerequisites, compliance and efficiency required. Input hashes copied from verified host manifest. Host `tools/grading.py validate` rejects incomplete/obsolete IDs, duplicate keys/IDs, wrong weights/statuses, blocked-as-met assertions, mismatched hashes, extra model totals and inconsistent eligibility. Produces quality total/core gaps outside model. Mechanical validation cannot establish semantic truth of evidence; host reviews disputed decisions and calibration per-ID agreement.
