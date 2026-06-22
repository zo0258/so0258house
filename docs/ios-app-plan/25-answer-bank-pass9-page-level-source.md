# Answer Bank Pass 9: Page-Level Source Capture

Date: 2026-06-22
Base commit: 97c43f7 Capture targeted sources for answer bank

## Purpose

Pass 9 checks whether the 24 `[source-backed-draft]` entries have enough page-level or section-level evidence to move toward verification.

The goal is not promotion volume. The goal is to state exactly whether each draft has page-level, section-level, URL-only, or partial evidence.

Core principle: exam fit is more important than newest academic standards.

## Processing Result

- Source-backed drafts processed: 24 / 24
- Existing verified entries rechecked: 3 / 3
- New verified promotions: 0
- Verified downgrades: 0
- Page-level source captured for source-backed drafts: 0
- Section-level source captured for source-backed drafts: 7
- URL-only maintained: 17
- Partial matches: 24
- Source capture archive created: `data/verification/source-capture/pass9-source-map.json`

## Capture Status Definitions

- `page_level`: source gives page-level answer evidence.
- `section_level`: source gives a clear section-level official basis, but not full page/rubric answer evidence.
- `url_only`: source family or landing page exists, but page/section evidence is not captured.
- `partial`: source supports the topic but does not directly verify all modelAnswer/keyPoints/commonMistakes.

## 국민체력100 / PAPS

Processed:

- `practical-038`
- `practical-039`
- `practical-040`
- `practical-041`
- `practical-042`
- `practical-046`
- `practical-048`

Result:

- Section-level captured: 7
- Partial match: 7
- New verified: 0

Captured source sections:

- 국민체력100 체력측정 항목
  - `체력측정 > 국민체력인증 > 측정항목`
- 국민체력100 인증기준
  - `체력측정 > 국민체력인증 > 인증기준`
- PAPS official/education resources remain useful for `practical-047`, which is already verified.

Decision:

The official sections support the measurement domain, but they do not fully verify every oral-answer element for BIA, BMI, skinfold, body composition interpretation, and adult field-test explanation. These entries stay draft with `[partial-source-match]`.

## 운동부하검사

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

Result:

- Page-level captured: 0
- URL-only maintained: 11
- Partial match: 11
- New verified: 0

Decision:

ACSM/CDC URLs identify the right source family, but they do not capture the required page-level evidence for GXT purpose, measured variables, absolute/relative contraindications, termination criteria, blood pressure response, Bruce protocol, or Ramp protocol. These remain draft.

## 저항성 트레이닝

Processed:

- `practical-064`
- `practical-097`
- `practical-098`
- `practical-102`
- `practical-104`
- `practical-105`

Result:

- Page-level captured: 0
- URL-only maintained: 6
- Partial match: 6
- New verified: 0

Decision:

ACSM/CDC pages support broad exercise and resistance training concepts, but not the exam-style details for strength, endurance, power, hypertrophy, 1RM procedure, sets, rest, and exercise order. These remain draft until NSCA/NASM/ACSM textbook pages are captured.

## Existing Verified Recheck

Verified maintained:

- `practical-047`
  - Section-level PAPS official/education evidence remains available.
- `practical-155`
  - 2025 practical/oral scoring rubric page 1 remains the direct answer source for Pivot Shift Test.
- `practical-188`
  - 2025 practical/oral scoring rubric page 1 remains the direct answer source for manual massage.

Verified downgrades: none.

## Tags Added

- `[partial-source-match]`: 24 entries
- `[url-level-source-only]`: 17 entries
- `[page-level-source-captured]`: 3 existing verified entries

No `[page-level-source-captured]` tag was added to the 24 source-backed drafts.

## Validation Updates

`scripts/validate_answer_bank.py` now checks:

- `[page-level-source-captured]` requires a non-guidebook sourceRef with `page` or `section`
- `[url-level-source-only]` is only valid for draft entries
- `[partial-source-match]` is only valid for draft entries
- existing source-backed/verified source guards remain active

## Next Pass

Pass 10 should acquire actual source pages, not just URLs:

1. Save 국민체력100/PAPS screen captures or PDFs for the 7 health-fitness drafts.
2. Find ACSM Guidelines 11th/12th edition pages for GXT contraindications, termination criteria, Bruce/Ramp, and measured variables.
3. Find NSCA/NASM/ACSM textbook pages for resistance training intensity, repetitions, sets, rest, order, and 1RM procedure.
4. Only then consider verified promotion.
