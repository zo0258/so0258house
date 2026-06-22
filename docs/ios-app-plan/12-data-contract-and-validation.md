# Data Contract and Validation

## 결론
iOS 앱은 `data/practical-questions.json`을 그대로 번들에 넣어 사용한다. 따라서 JSON 필드 계약을 명확히 두고, Mac에서 앱을 만들기 전에 Windows에서도 최소 계약 검증을 자동화한다.

## 원본 데이터 위치
- 웹앱 원본: `data/practical-questions.json`
- iOS 번들 대상 파일명: `practical-questions.json`
- iOS 배치 후보: `Resources/practical-questions.json`

## 현재 데이터 기준
- 총 문제 수: 199
- 유형: 실기 99, 구술 100
- 과목: 건강·체력측정평가, 트레이닝방법론, 운동손상평가 및 재활
- 연도 범위: 2015~2025
- section 수: 9

## 필수 필드 계약
| 필드 | 필수 | Swift 타입 | 화면 노출 |
|---|---|---|---|
| id | 예 | String | 예 |
| subject | 예 | String | 예 |
| section | 예 | String | 예 |
| type | 예 | String / QuestionType | 예 |
| year | 예 | Int? | 예 |
| question | 예 | String | 예 |
| methodGuide | 예 | String | 예 |
| memoryTip | 예 | String | 예 |
| answerGuide | 예 | String | 조건부 |
| sourceRefs | 예 | [SourceRef] | 기본 숨김 |
| sourceVerified | 예 | Bool | 숨김 |
| needsReview | 예 | Bool | 숨김 |
| reviewReasons | 아니오 | [String]? | 숨김 |

## 값 검증 규칙
- `id`는 중복되면 안 된다.
- `type`은 `실기`, `구술`, `공통` 중 하나여야 한다.
- `question`은 빈 문자열이면 안 된다.
- `year`는 현재 데이터 기준 2015~2025 사이여야 한다.
- `subject`, `section`은 빈 문자열이면 안 된다.
- 화면용 공개 모델에는 `sourceVerified`, `needsReview`, `reviewReasons`를 직접 노출하지 않는다.

## DailyQuiz 검증 규칙
- 날짜 하나에 4문제를 선택한다.
- 가능하면 실기 2 + 구술 2를 유지한다.
- 가능한 범위에서 과목과 section을 분산한다.
- 같은 날짜와 같은 JSON이면 항상 같은 결과가 나와야 한다.
- 사용자의 완료 기록은 문제 선택에 영향을 주지 않는다.

## iOS 디코딩 기준
- JSONDecoder로 `[Question]`을 직접 디코딩한다.
- `reviewReasons`는 optional로 둔다.
- 앱에서 문제 원문을 수정하지 않는다.
- 앱 화면에서 줄바꿈과 표시 방식만 조정한다.

## Windows 자동 검증 기준
- `validate_ios_plan.py`로 문서와 데이터 계약을 확인한다.
- Swift 컴파일은 Windows에서 검증하지 않는다.
- Swift 초안은 파일 존재, 핵심 타입명, 금지 placeholder 여부만 점검한다.

## Mac/Xcode 검증 기준
- Bundle Resource 포함 여부 확인.
- Repository 로딩 결과 199개 확인.
- QuestionType 변환 확인.
- DailyQuizSelector 결과 4개 확인.
- StudyRecordStore 저장/복원 확인.

끝.
