# Question Answer Bank Plan

## 왜 Answer Bank가 먼저인가

iOS MVP는 199개 문제 로딩, 오늘 4문제 선택, 기록 저장까지 동작한다. 다음 품질 병목은 화면이 아니라 답안 데이터다. 문제 원문과 답안/수행방법/암기팁이 검증되지 않으면 앱은 매일 열 수 있어도 학습 신뢰도가 낮다. 그래서 실기기 UI QA 전에 정적 answer bank를 먼저 분리한다.

## 문제 발췌 검증 기준

- `data/practical-questions.json` 원문은 직접 수정하지 않는다.
- PDF 원문과 대조해 오탈자나 추출 오류가 확인된 경우에만 별도 `correctedQuestion` 제안으로 기록한다.
- 점검 항목은 총 문제 수, 중복 ID, 중복 문장, 연도 누락/오인식, 과목/section/type 분류, 깨진 문자, 단위 오타, PAR-Q 등 용어 오타다.
- 이번 1차에서는 자동 확정 판정 대신 의심 항목을 audit로 분리한다.

## Answer Bank 필드 구조

`data/practical-answer-bank.json`은 앱 번들에 넣을 정적 답안 후보 파일이다.

```json
{
  "questionId": "practical-001",
  "answerStatus": "draft | verified | needs_review",
  "modelAnswer": "",
  "performanceSteps": [],
  "oralAnswerStructure": [],
  "keyPoints": [],
  "commonMistakes": [],
  "memoryTip": "",
  "sourceRefs": [],
  "sourceVerified": false,
  "needsReview": true,
  "reviewNotes": []
}
```

## 출처 검증 기준

이 answer bank의 목적은 최신 운동생리학 지식 데이터베이스가 아니라 건강운동관리사 실기·구술 합격 데이터베이스다. 따라서 답안 작성과 검증에서는 `시험 적합성 > 최신 학술성`을 우선한다. 최신 기준과 기출 당시 기준이 충돌하면 최신 기준을 확정 답안으로 바로 채택하지 않고, `reviewNotes`에 `기출 당시 기준 확인 필요`를 남긴다.

출처 우선순위는 다음 순서다.

1. Tier S: 건강운동관리사 공식 교재, 기출문제 해설, 실기·구술 강의자료, 수험서, 교육과정 자료
2. Tier A: 국민체력100, PAPS, 대한체육회, 대한운동사협회, 국내 대학 운동처방 교재, 국내 학회 자료
3. Tier B: ACSM, NSCA, AHA, CDC, WHO
4. Tier C: 논문, PubMed, Physiopedia, Physiotutors
5. Tier D: 블로그, 카페, 커뮤니티

Tier D는 참고만 허용하고 `sourceVerified: true` 근거로 사용하지 않는다.

의학·운동처방 수치가 포함된 문제는 `checkedAt`을 남긴다. ACSM 구버전 기준과 최신 기준이 충돌하면 `reviewNotes`에 `기출 당시 기준 확인 필요`를 남긴다.

## 199개 전체 구축 전략

1. 모든 `questionId`에 answer bank 엔트리를 먼저 만든다.
2. 출처가 확인되지 않은 항목은 `answerStatus: needs_review`, `sourceVerified: false`로 둔다.
3. Pass 1에서 우선순위 문제군부터 `modelAnswer`, `performanceSteps`, `oralAnswerStructure`, `keyPoints`, `commonMistakes`, `memoryTip`을 채운다.
4. Pass 2에서 Tier S/A 출처부터 대조한다.
5. Pass 3에서 기출 의도와 채점자 기대 답안에 맞게 수정한다.
6. Pass 4에서 시험장에서 떠올릴 수 있는 암기팁을 보강한다.
7. Pass 5에서 시험 적합성을 검토한다.
8. Pass 6에서 검증 완료 항목만 `answerStatus: verified`로 승격한다.
9. 앱은 answer bank가 없어도 문제 로딩이 되도록 하고, answer bank가 있으면 보조 답안으로 붙인다.

`verified` 승격 조건은 `modelAnswer`, 3개 이상의 `keyPoints`, `commonMistakes`, `memoryTip`, `sourceRefs`, `sourceVerified: true`, 정리된 `reviewNotes`, `needsReview: false`다. 기준 충돌이나 수동 검수 메모가 남아 있으면 `verified`로 올리지 않는다.

## 1차 우선순위 문제군

- 2026-06-22 오늘 출제 4문제
- 2025년 문제
- 건강·체력측정평가: 위험군 분류, 혈압, 대사증후군, PAR-Q 관련 문항
- 트레이닝방법론: 저항성 트레이닝, RM, 세트/반복 관련 문항
- 운동손상평가 및 재활: 반복 출제되는 평가/검사/재활 문항

## 수동 검수 필요 기준

- PDF 원문 대조가 끝나지 않은 문제
- 단위/약어 오타 의심 문제
- 기준 연도에 따라 답이 달라질 수 있는 문제
- 출처가 블로그/카페 수준에 그치는 문제
- `modelAnswer`를 채우려면 전문서적 확인이 필요한 문제

## 앱 반영 계획

이번 단계에서는 `AnswerBankModels.swift`와 `AnswerBankRepository.swift`만 추가한다. `PracticeView`에서 answer bank를 실제 표시하는 작업은 다음 단계로 둔다. 반영 시에는 `questionId`로 문제와 답안 엔트리를 매칭하고, 누락된 답안은 화면에서 조용히 숨긴다.

끝.
