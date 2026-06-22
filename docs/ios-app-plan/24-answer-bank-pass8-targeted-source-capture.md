# Answer Bank Pass 8: Targeted Source Capture

Date: 2026-06-22
Base commit: c97252e Hunt tier S sources for answer verification

## Purpose

Pass 8 moves from broad search to targeted source capture.

The goal is to attach usable URL-level or page-level answer-source metadata to the 27 `[source-verifiable]` entries, while keeping `answerStatus` conservative. A source can support a draft without being strong enough for `sourceVerified: true`.

Core principle: exam fit is more important than newest academic standards.

## Processing Result

- Source-verifiable entries processed: 27 / 27
- New verified promotions: 0
- Verified maintained: 3
- Source-backed drafts: 24
- Verified downgrades: 0
- Original `data/practical-questions.json` modified: no
- Existing web app files modified: no
- iOS answer bank resource synced: yes

## Source Capture Standard

For captured sources, `sourceRefs` may now include:

- `section`: source section, page, landing page, or rubric area
- `evidenceSummary`: concise statement of what the source supports

The Swift model currently decodes the standard source fields and ignores extra JSON keys safely. These extra fields are for audit/source governance and future UI use.

## 국민체력100 / PAPS Result

Processed:

- `practical-038`
- `practical-039`
- `practical-040`
- `practical-041`
- `practical-042`
- `practical-046`
- `practical-047`
- `practical-048`

Captured sources:

- 국민체력100 체력측정 항목
  - URL: `https://nfa.kspo.or.kr/reserve/0/selectMeasureItemListByAgeSe.kspo`
  - Section: `체력측정 > 국민체력인증 > 측정항목`
  - Supports: age-group measurement items, body composition, health fitness, motor fitness, and adult field-test items.
- 국민체력100 인증기준
  - URL: `https://nfa.kspo.or.kr/reserve/0/selectMeasureGradeItemListByAgeSe.kspo`
  - Section: `체력측정 > 국민체력인증 > 인증기준`
  - Supports: sex/age-based health and motor fitness criteria.
- PAPS official/education sources
  - Supports: PAPS purpose, health-fitness-centered evaluation, online management/prescription, and evaluation areas.

Decision:

- `practical-047` remains verified.
- The other 7 entries become `[source-backed-draft]`.
- Reason: URL-level official sources support topics and item names, but detailed oral-answer phrasing still needs page-level capture or a scoring/rubric source.

## 운동부하검사 Result

Processed:

- `practical-052`
- `practical-053`
- `practical-054`
- `practical-055`
- `practical-056`
- `practical-057`
- `practical-059`
- `practical-060`
- `practical-061`
- `practical-062`
- `practical-063`

Captured sources:

- ACSM Guidelines for Exercise Testing and Prescription
  - URL: `https://acsm.org/education-resources/books/guidelines-exercise-testing-prescription/`
  - Section: ACSM Guidelines landing page
  - Supports: exercise testing and prescription standards at the textbook/source-family level.
- ACSM Physical Activity Guidelines
  - URL: `https://acsm.org/education-resources/trending-topics-resources/physical-activity-guidelines/`
  - Supports: general exercise prescription principles.
- CDC High Blood Pressure
  - URL: `https://www.cdc.gov/high-blood-pressure/`
  - Supports: blood-pressure background only.

Decision:

- All 11 entries remain draft with `[source-backed-draft]`.
- Reason: public/landing-page sources are not enough for GXT details such as contraindications, termination criteria, Bruce/Ramp protocol details, hemodynamic variables, and exam-fit wording.
- Next evidence required: ACSM 11th/12th edition page-level excerpts or health exercise practical/oral scoring examples.

## 저항성 트레이닝 Result

Processed:

- `practical-064`
- `practical-097`
- `practical-098`
- `practical-102`
- `practical-104`
- `practical-105`

Captured sources:

- CDC Adult Physical Activity Guidelines
  - URL: `https://www.cdc.gov/physical-activity-basics/guidelines/adults.html`
  - Section: `Adult Activity: An Overview`
  - Supports: adult aerobic activity and muscle-strengthening frequency at public-health level.
- ACSM Resistance Training Guidelines Update 2026
  - URL: `https://acsm.org/resistance-training-guidelines-update-2026/`
  - Section: ACSM 2026 resistance training guideline summary
  - Supports: current strength, hypertrophy, and power concepts as a modern reference.

Decision:

- All 6 entries remain draft with `[source-backed-draft]`.
- Reason: 2026 ACSM guidance is useful but can conflict with older exam wording. Health-exercise oral answers need NSCA/NASM/ACSM textbook page-level details on intensity, repetition, sets, rest, order, and 1RM procedure.

## Existing Verified Recheck

Verified maintained:

- `practical-047`
  - Maintained because PAPS official/education sources still support the answer structure and no unresolved conflict note remains.
- `practical-155`
  - Maintained because the 2025 health exercise practical/oral scoring-rubric example directly covers Pivot Shift Test purpose and performance criteria.
- `practical-188`
  - Maintained because the 2025 scoring-rubric example directly covers manual massage effects and technique examples.

Verified downgrades: none.

## Source-Backed Drafts

Source-backed draft means: guidebook source exists, at least one non-guidebook source exists, but verified is still withheld.

Items:

- `practical-038`
- `practical-039`
- `practical-040`
- `practical-041`
- `practical-042`
- `practical-046`
- `practical-048`
- `practical-052`
- `practical-053`
- `practical-054`
- `practical-055`
- `practical-056`
- `practical-057`
- `practical-059`
- `practical-060`
- `practical-061`
- `practical-062`
- `practical-063`
- `practical-064`
- `practical-097`
- `practical-098`
- `practical-102`
- `practical-104`
- `practical-105`

## Validation Updates

`scripts/validate_answer_bank.py` now checks:

- 199 answer bank entries exist
- data and iOS resource JSON are identical
- guidebook sourceRef exists on all 199 entries
- `[source-verifiable]` count remains 27
- verified entries have a non-guidebook answer source
- `[source-backed-draft]` entries are draft, not sourceVerified, and have a non-guidebook sourceRef
- `[verified-maintained]` appears only on verified entries

## Next Pass

Pass 9 should focus on true page-level capture:

1. 국민체력100/PAPS page or screenshot capture for `practical-038` through `048`.
2. ACSM Guidelines textbook pages for exercise testing entries before any GXT promotion.
3. NSCA/NASM/ACSM textbook pages for resistance training entries.
4. Do not promote sourceVerified based on landing pages or broad public-health summaries alone.
