# Answer Bank Pass 6: Answer Source Check

Date: 2026-06-22
Base commit: d6182f2 Validate answer bank with tier S guidebook

## Purpose

Pass 6 checks whether each answer bank entry can be validated against an answer source, not merely against the guidebook question list.

The guidebook remains the source for question provenance, exam scope, evaluation criteria, and preparation strategy. It is not used by itself as a full model-answer source.

Core principle: exam fit is more important than newest academic standards.

## 199-Entry Processing

- 199 entries processed: yes
- Original `data/practical-questions.json` modified: no
- Existing web app files modified: no
- iOS answer bank resource synced: yes

## Source Materials Found

- `건강운동관리사 취득 기초 길잡이 2026`
  - Tier S internal source
  - Useful for question provenance, exam scope, evaluation criteria, recommended materials, and preparation strategy
- `2025년도 건강운동관리사 실기구술 채점표`
  - Tier S internal source
  - Useful as answer-source evidence for the included scoring-rubric examples
- `2016-2024 건강운동관리사 실기구술 기출정리표`
  - Tier S internal source
  - Useful for question-list cross-check, not detailed model answers
- `2025년도 건강운동관리사 실기구술 출제영역`
  - Tier S internal source
  - Useful for scope cross-check; text extraction is poor, so OCR/manual review is still needed

## Answer-Source Classification

Each entry received one primary Pass 6 classification tag.

- `[source-verifiable]`: 27
- `[guidebook-only]`: 27
- `[conflicting-standard]`: 17
- `[practical-demonstration-needed]`: 64
- `[specialist-source-needed]`: 64

Definitions:

- `[source-verifiable]`: likely verifiable with public, textbook, scoring-rubric, or guidebook-recommended sources
- `[guidebook-only]`: question/scope source exists, but answer source is still insufficient
- `[conflicting-standard]`: year/version standards may conflict; verified is held
- `[practical-demonstration-needed]`: practical performance needs video, in-person, or rubric-level demonstration evidence
- `[specialist-source-needed]`: orthopedic, injury, special-test, rehab, or taping source is needed

## Verified Promotion

Verified status after Pass 6:

- verified: 3
- draft: 196
- needs_review status: 0
- sourceVerified true: 3
- sourceVerified false: 196

Newly promoted in Pass 6:

- `practical-155`: Pivot Shift Test
  - Basis: 2025 practical/oral scoring-rubric example includes the purpose, supine position, knee flexion angle, tibial internal rotation, valgus/rotation force, and positive-response explanation.
- `practical-188`: Manual massage techniques and physiological effects
  - Basis: 2025 practical/oral scoring-rubric example includes circulation promotion, tissue stretching, metabolite/edema removal, relaxation/fatigue recovery, and technique examples such as effleurage, petrissage, friction, tapotement, and vibration.

Previously verified and maintained:

- `practical-047`: PAPS definition/features/evaluation areas

## Draft Maintained

Draft maintained: 196 entries.

Main reasons:

- guidebook confirms question provenance but does not provide detailed answers
- practical demonstrations need video/rubric confirmation
- injury and rehab questions need specialist texts
- year/version conflicts remain unresolved
- public Tier B/C sources are useful but not enough for sourceVerified in this project

## Conflict Items

17 entries retain standard-conflict handling:

- `practical-001`
- `practical-002`
- `practical-003`
- `practical-004`
- `practical-005`
- `practical-006`
- `practical-007`
- `practical-008`
- `practical-009`
- `practical-032`
- `practical-037`
- `practical-050`
- `practical-051`
- `practical-058`
- `practical-066`
- `practical-068`
- `practical-120`

Each remains held because historical exam standards, source text anomalies, or scoring expression need more precise answer-source comparison.

## CorrectedQuestion Status

- `practical-050`: confirmed correctedQuestion proposal remains. Guidebook p.32 shows the exercise-test result table in the correct order.
- `practical-001`: guidebook source also shows `mmg`; source typo suspicion remains, original JSON unchanged.
- `practical-008`: guidebook source also shows `PAP-Q`; 2020 official `PAR-Q+` conflict remains, original JSON unchanged.

## Next Pass

Pass 7 should use subject-specific answer sources from the guidebook recommendation list:

1. ACSM 11th edition for health/fitness assessment and exercise testing.
2. 국민체력100 official pages/videos for age-group practical measurement steps.
3. NSCA/NASM texts for resistance and training-method practical items.
4. `건강운동관리사를 위한 운동상해(2판)`, `임상 정형의학 검사`, and `스포츠재활총론(6판)` for special tests, rehab, and taping.
5. Promote verified only when modelAnswer, keyPoints, commonMistakes, and memoryTip match the answer source without unresolved conflict notes.
