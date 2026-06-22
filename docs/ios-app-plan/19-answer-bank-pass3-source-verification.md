# Answer Bank Pass 3 Source Verification

- 작성일: 2026-06-22
- 기준 커밋: c3bc345 Refine full answer bank pass two
- 목적: 199개 전체 answer bank를 대상으로 출처 대조와 시험 적합성 판정을 수행하고, verified 가능 항목을 보수적으로 분리한다.

## 1. 원칙

- 시험 적합성 > 최신 학술성
- Tier S/A 대조 없이 `sourceVerified: true`로 올리지 않는다.
- Tier B/C만 있는 항목은 답안이 좋아도 `draft`를 유지한다.
- 기준 연도 충돌 가능 문항은 `기출 당시 기준 확인 필요`를 유지한다.

## 2. 199개 전체 처리 여부

- 전체 문제: 199개
- 과목별: 건강·체력측정평가 63, 트레이닝방법론 70, 운동손상평가 및 재활 66
- type별: 구술 100, 실기 99
- 2025년 24개 처리: 24개
- 반복출제 영역 처리 후보: 121개

## 3. 2025년 24개 검증 결과

- `practical-047`은 PAPS 정의/특징/평가 영역이 Tier A 교육기관 자료로 대조 가능하여 verified로 승격했다.
- 나머지 2025년 문항은 AHA/ACSM/재활 특수검사 자료처럼 Tier B/C 중심이거나, 실기 채점표 수준의 세부 기준 대조가 부족하여 draft를 유지했다.

## 4. 반복출제 영역 검증 결과

- 위험군 분류/혈압/대사증후군/PAR-Q: 기준 연도 충돌 가능성이 있어 draft 유지
- 저항성 트레이닝/근력/근지구력/근파워: Tier B 자료는 있으나 건강운동관리사 수험서 표현 대조가 부족해 draft 유지
- 노인 체력검사/Y-Balance/FMS: 검사명 근거는 있으나 세부 시행/채점표 대조가 부족해 draft 유지
- ROM/손상평가/재활운동: Tier C 참고 출처 중심이라 draft 유지

## 5. 상태 요약

- verified: 1
- draft: 198
- needs_review: 0
- sourceVerified true: 1
- sourceVerified false: 198
- verified 승격 항목: practical-047
- draft 유지 항목: 198개
- 기준 충돌 항목: 17개
- 출처 부족 항목: 198개

## 6. correctedQuestion 확인 현황

- `practical-001`: 2015 HWP 원문 추출이 아직 안 되어 `mmg -> mmHg`는 pending 유지
- `practical-008`: 2020 PDF에서 `PAR-Q+` 표현 확인. audit의 correctedQuestion 제안 유지

## 7. 다음 Pass에서 볼 항목

- Tier S 확보: 건강운동관리사 공식 교재, 수험서, 실기·구술 강의자료
- 2025년 실기 12개는 채점표 수준의 수행 순서 대조 필요
- 위험군/혈압/대사증후군/PAR-Q는 기출 당시 기준과 최신 기준 차이 정리 필요
- 운동손상평가/재활은 특수검사별 자세, 고정 손 위치, 양성 소견을 수험서 표현으로 대조 필요

## 8. 추가 개선점 여부

추가 개선점은 남아 있다. Pass 3에서 verified는 1개만 보수 승격했고, 나머지는 Tier S/A 대조 부족으로 draft 유지했다. 다음 루프는 Tier S 자료 확보와 문항별 수험서 표현 대조가 중심이다.
