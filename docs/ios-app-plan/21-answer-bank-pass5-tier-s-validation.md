# Answer Bank Pass 5: Tier S Guidebook Validation

Date: 2026-06-22
Base commit: b354c41 Define exam ready answer bank strategy

## Purpose

Pass 5 validates the 199 practical/oral answer bank entries against the newly secured `건강운동관리사 취득 기초 길잡이 2026` PDF.

The guidebook is treated as a Tier S internal source for this project because it contains the practical/oral exam scope, evaluation criteria, recommended materials, preparation strategy, and 2015-2025 practical/oral question list. It is still not treated as an official scoring key or full model-answer source.

Core principle: exam fit is more important than newest academic standards.

## Source Review

- Source file: `/Users/zo0258/Downloads/temp_1782127873338.1898256780.pdf`
- PDF pages: 45
- Criteria/preparation review: PDF p.22-28
- Question provenance review: PDF p.29-44
- Note: the user-specified p.29-43 range covers most questions, but the final taping question is on physical PDF p.44 with printed footer `-42p-`.

## 199-Question Processing

- 199 entries processed: yes
- Guidebook question extraction count: 199
- Source reference added to answer bank entries: 199
- iOS resource copy synced: yes

Each entry now includes a `tier_s_internal` sourceRef for guidebook provenance, with a PDF page number where the question appears.

This sourceRef confirms the original question/scope location. It does not by itself verify every model answer, performance step, or oral answer wording.

## Question Text Audit

Only one substantive mismatch was found between `data/practical-questions.json` and the guidebook extraction:

- `practical-050`: the exercise test result table is misordered in the current JSON. The guidebook p.32 shows the correct order as `고객 A / 고객 B`, then `나이`, `몸무게`, `안정시 심박수`, `안정시 혈압`, `최대산소섭취량(min/L)`.

Previously tracked correction candidates were rechecked:

- `practical-001`: guidebook p.29 also shows `125/85mmg`. This is likely a source typo for `mmHg`, but Pass 5 does not confirm a PDF extraction error.
- `practical-008`: guidebook p.29 also shows `PAP-Q`. The earlier 2020 official written exam source contains `PAR-Q+`, so `PAR-Q` remains a likely correction, but the guidebook alone does not confirm it.

`data/practical-questions.json` remains unchanged.

## Answer Bank Status

- verified: 1
- draft: 198
- needs_review status: 0
- sourceVerified true: 1
- sourceVerified false: 198
- needsReview true: 198

No new entries were promoted to verified in Pass 5. The guidebook strongly improves exam-scope and question-provenance confidence, but it is not a model-answer key. Verified promotion still requires answer-source or scoring-expression confirmation.

Existing verified entry:

- `practical-047`: PAPS definition/features/evaluation areas, already verified from Tier A public education sources and now additionally tied to the guidebook question page.

## Tag Reorganization

- `[exam-ready-draft]`: 141 entries
- `[source-needed]`: 198 entries
- `[source-verified]`: 1 entry
- `[year-standard-conflict]`: 17 entries
- `[needs-tier-s-check]`: 0 entries
- `[needs-answer-source-check]`: 57 entries

Pass 5 removes the older `needs-tier-s-check` tag because a Tier S internal guidebook is now available. Entries that still need scoring-key, textbook, or model-answer-source comparison now use `[needs-answer-source-check]`.

## Repeated-Domain Review

Repeated/priority domains were rescanned across all 199 entries. Priority-domain candidates: 137 entries.

Covered domains include:

- 위험군 분류
- PAR-Q/PAP-Q
- 혈압
- 대사증후군
- BIA
- BMI
- 운동부하검사
- 저항성 트레이닝
- 근력 / 근지구력 / 근파워
- 국민체력100
- PAPS
- Y-Balance
- 스페셜 테스트
- 운동손상 재활

These entries now have guidebook provenance, but most remain draft because the guidebook does not provide full model-answer scoring language.

## Remaining Conflicts

Year/standard conflict count: 17.

These include risk classification, hypertension, PAR-Q/PAP-Q, metabolic syndrome, exercise testing criteria, and prescription values where the historical exam standard may differ from newer ACSM/AHA/CDC/WHO wording.

The reviewNotes keep the “기출 당시 기준 확인 필요” family of notes for these entries.

## Next Pass Plan

Pass 6 should focus on answer-source verification, not broad web searching.

Recommended order:

1. Use guidebook recommended materials by subject.
2. For health/fitness assessment and exercise testing, compare against ACSM 11th edition wording where the guidebook recommends it.
3. For training-method practical items, compare against NSCA/NASM or bodybuilding practical-source wording.
4. For injury assessment/rehab, compare against `건강운동관리사를 위한 운동상해(2판)`, `임상 정형의학 검사 - 스페셜 테스트`, and `스포츠재활총론(6판)`.
5. Promote verified only when answer wording and source support align without unresolved conflict notes.
