# Answer Bank Pass 4 Tier S Strategy

- 작성일: 2026-06-22
- 기준 커밋: 329d0b Verify answer bank sources pass three
- 목적: Tier S 자료 확보 가능성을 먼저 확인하고, verified를 억지로 늘리지 않으면서 앱 표시용 시험형 초안 품질 단계를 분리한다.

## 1. Pass 4 목적

현재 199개 answer bank는 모두 답안 초안이 있으나, 건강운동관리사 실기·구술 수험서/채점표/강의자료 같은 Tier S 근거가 부족하다. 따라서 이번 Pass는 다음을 목표로 했다.

- 로컬 저장소와 관련 폴더에서 Tier S 후보 자료를 찾는다.
- PDF 22P 이후 참고자료를 재확인할 수 있는지 판단한다.
- `verified`와 별개로 학습에 쓸 수 있는 `exam-ready-draft` 품질 단계를 `reviewNotes` 태그로 분리한다.
- 199개 전체를 다시 훑어 sourceVerified는 보수적으로 유지한다.

## 2. Tier S 자료 탐색 결과

탐색 위치:

- `/Users/zo0258/Desktop/openclaw/02_project/so0258house`
- `/Users/zo0258/Desktop/openclaw/02_project`
- `/Users/zo0258/Desktop/openclaw`
- `/Users/zo0258/Desktop/건강운동관리사_web`

찾은 자료:

| 파일/자료 | 위치 | 자료 유형 | Tier 판단 | answer bank 검증 사용 가능성 |
|---|---|---|---|---|
| KSPO 건강운동관리사 필기시험 원문/최종정답 PDF/HWP 묶음 | `materials/raw/kspo/2015-2025/` | official written exam questions and answer keys | Tier S for written question/answer provenance only | 실기·구술 모범답안/채점표 검증에는 직접 사용 불가 |
| 건강운동관리사_web 기존 데일리 퀴즈/오답노트 | `/Users/zo0258/Desktop/건강운동관리사_web` | internal written-exam web app and generated explanations | internal reference | 필기 해설 참고 가능, 실기·구술 verified 근거로는 부적합 |
| 2024-health-exam.pdf | `/Users/zo0258/Desktop/openclaw/02_project/2024-health-exam.pdf` | written exam PDF, 12 pages | official/source candidate for written exam only | 22P 이후 참고자료가 없어 실기·구술 답안 근거로 사용 불가 |
| 건강운동관리사 취득 기초 길잡이v.2026.pdf | `/Users/zo0258/Desktop/openclaw/02_project/건강운동관리사 취득 기초 길잡이v.2026.pdf` | expected extraction source | unknown | 현재 파일 없음. PDF 22P 이후 참고자료 재검토 불가 |

판정:

- 실기·구술 모범답안/채점표 검증에 바로 쓸 수 있는 Tier S 자료는 현재 로컬에서 확인되지 않았다.
- KSPO 필기 원문/최종정답은 공식 자료지만, 이번 answer bank의 실기·구술 수행 답안 검증 근거로 직접 쓰기는 어렵다.
- `/Users/zo0258/Desktop/건강운동관리사_web`은 기존 필기 학습 앱 자료이므로 내부 참고는 가능하지만 sourceVerified 근거로 쓰지 않는다.

## 3. PDF 22P 이후 참고자료 재검토 결과

- `scripts/build_practical_site.py`는 `../건강운동관리사 취득 기초 길잡이v.2026.pdf`에서 22페이지 이후를 추출하도록 설계되어 있다.
- 현재 `/Users/zo0258/Desktop/openclaw/02_project/건강운동관리사 취득 기초 길잡이v.2026.pdf` 파일은 없다.
- 확인된 `2024-health-exam.pdf`는 12페이지이고, KSPO 연도별 필기 PDF도 22페이지 미만으로 확인되어 22P~28P 참고자료 재검토를 수행할 수 없었다.
- 따라서 PDF 22P 이후 참고자료는 `file_not_found` 상태로 audit에 기록했다.

## 4. exam-ready-draft 기준

데이터 구조 변경은 최소화하기 위해 새 필드는 추가하지 않고 `reviewNotes` 태그를 사용한다.

- `[exam-ready-draft]`: verified는 아니지만 30~60초 구술 또는 실기 설명으로 재현 가능한 시험형 초안
- `[source-needed]`: Tier S/A 대조 전이라 sourceVerified false 유지
- `[source-verified]`: sourceVerified true와 verified를 만족하는 항목
- `[year-standard-conflict]`: 기출 당시 기준과 최신 기준 충돌 가능성이 있는 항목
- `[needs-tier-s-check]`: 건강운동관리사 수험서/강의자료/채점표 표현 대조가 필요한 항목

exam-ready-draft 후보 조건:

- modelAnswer가 간결하고 시험장 답변으로 말할 수 있음
- 실기 문항은 performanceSteps가 준비-자세-수행-기록/주의 흐름을 가짐
- 구술 문항은 oralAnswerStructure가 정의-기준-적용-주의 흐름을 가짐
- keyPoints가 3~7개 채점 키워드로 정리됨
- commonMistakes가 실제 감점 포인트에 가까움
- memoryTip이 문제별로 구체적임
- 기준 충돌 문항은 제외

## 5. 199개 전체 재검토 결과

- 전체 처리: 199개
- verified 유지: 1개
- draft 유지: 198개
- needs_review: 0개
- sourceVerified true: 1개
- sourceVerified false: 198개
- needsReview true: 198개
- exam-ready-draft 후보: 141개
- needs-tier-s-check 후보: 57개
- 기준 충돌 항목: 17개

exam-ready-draft 예시 후보:

`practical-010`, `practical-011`, `practical-012`, `practical-013`, `practical-014`, `practical-015`, `practical-016`, `practical-017`, `practical-018`, `practical-019`, `practical-020`, `practical-021`, `practical-022`, `practical-023`, `practical-024`, `practical-025`, `practical-026`, `practical-027`, `practical-028`, `practical-029`, `practical-030`, `practical-031`, `practical-033`, `practical-034`, `practical-035`, `practical-036`, `practical-039`, `practical-040`, `practical-041`, `practical-046`

needs-tier-s-check 예시 후보:

`practical-001`, `practical-002`, `practical-003`, `practical-004`, `practical-005`, `practical-006`, `practical-007`, `practical-008`, `practical-009`, `practical-032`, `practical-037`, `practical-038`, `practical-042`, `practical-043`, `practical-044`, `practical-045`, `practical-049`, `practical-050`, `practical-051`, `practical-058`, `practical-066`, `practical-068`, `practical-097`, `practical-098`, `practical-099`, `practical-100`, `practical-101`, `practical-102`, `practical-103`, `practical-104`

## 6. verified 유지/승격 수

- 기존 verified `practical-047`은 유지했다.
- 신규 verified 승격은 0개다.
- 이유: 실기·구술 수험서/채점표/강의자료 같은 Tier S 근거가 확보되지 않았기 때문이다.

## 7. 기준 충돌 항목

`practical-001`, `practical-002`, `practical-003`, `practical-004`, `practical-005`, `practical-006`, `practical-007`, `practical-008`, `practical-009`, `practical-032`, `practical-037`, `practical-050`, `practical-051`, `practical-058`, `practical-066`, `practical-068`, `practical-120`

정리 기준:

- 혈압, 위험군 분류, 대사증후군, PAR-Q/PAR-Q+, 운동처방 수치 등은 기출 당시 기준 확인 전까지 `verified`로 승격하지 않는다.
- 해당 문항에는 `[year-standard-conflict]`와 “기출 당시 기준 확인 필요” 메모를 유지한다.

## 8. 다음 Pass 권장사항

1. 실제 Tier S 자료 확보: 건강운동관리사 실기·구술 수험서, 공식 교재, 강의자료, 채점표, 기출해설 PDF
2. 확보한 자료를 문항별로 연결할 수 있도록 `sourceRefs`에 교재명/쪽수/강의자료명까지 기록
3. exam-ready-draft 141개부터 Tier S 대조 후 verified 후보로 검토
4. needs-tier-s-check 57개는 먼저 답안 자체를 수험서 표현으로 재작성
5. 기준 충돌 17개는 기출 당시 기준과 최신 기준을 별도 표로 정리

## 9. 추가 개선점 여부

추가 개선점은 남아 있다. Pass 4에서 얻은 결론은 `검증된 답안 수를 늘리려면 새 웹 검색보다 Tier S 자료 확보가 먼저`라는 점이다. 현재 단계에서는 199개 중 141개를 앱에서 “시험형 초안”으로 보여줄 수 있지만, sourceVerified로 표시할 수 있는 항목은 기존 `practical-047` 1개뿐이다.
