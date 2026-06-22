# So02House iOS Data Model

## 결론
현재 `data/practical-questions.json`은 iOS 번들 데이터로 재사용한다. MVP에서는 문제 원본은 읽기 전용 Codable 모델로 두고, 학습 기록은 UserDefaults, Pencil 메모는 파일 저장으로 분리한다.

## 현재 JSON 필드
현재 문제 수는 199개다.

| 필드 | 타입 | iOS 처리 |
|---|---:|---|
| id | String | Question.id |
| subject | String | Question.subject |
| section | String | Question.section |
| type | String | Question.questionType |
| year | Int? | Question.year |
| question | String | 원문 보존 |
| methodGuide | String | 초기 표시용, 검수 전 문구 순화 가능 |
| memoryTip | String | 초기 표시용 |
| answerGuide | String | 비어 있을 수 있음 |
| sourceRefs | [SourceRef] | 내부 검수와 참고용 |
| sourceVerified | Bool | 화면 직접 노출 금지 |
| needsReview | Bool | 화면 직접 노출 금지 |
| reviewReasons | [String] | 개발/검수용 |

## Swift 모델 초안
- Question: JSON 문제 원본.
- SourceRef: 출처 제목과 URL.
- DailyQuiz: 특정 날짜의 4문제 묶음.
- StudyRecord: 문제별 상태 기록.
- PencilNote: 문제별 필기 메모 메타데이터.
- ReviewStatus: none, done, review, hard.
- SubjectSummary: 통계 화면용 과목 집계.

## Question
- `id`는 안정적인 기본 키다.
- `type` 문자열은 Swift 내부에서 `QuestionType`으로 변환한다.
- 원문 문제 `question`은 앱에서 수정하지 않는다.

## DailyQuiz
- `date: Date`.
- `questions: [Question]`.
- `questionCount`는 4로 고정.
- 선택 로직은 DailyQuizSelector에 둔다.

## StudyRecord
- `questionID`.
- `status`.
- `quizDate`.
- `updatedAt`.
- 후속으로 `elapsedSeconds`, `attemptCount` 추가 가능.

## PencilNote
- `questionID`.
- `updatedAt`.
- `fileName`.
- `storageKind`.
- MVP에서는 `PKDrawing.dataRepresentation()` 결과를 파일로 저장한다.

## ReviewStatus
- none: 기록 없음.
- done: 완료.
- review: 다시 보기.
- hard: 어려움.

## SubjectSummary
- subject.
- totalCount.
- doneCount.
- reviewCount.
- hardCount.
- practicalCount.
- oralCount.

## JSON 디코딩 기준
- 앱 번들에 `practical-questions.json`을 추가한다.
- JSONDecoder로 `[Question]`을 읽는다.
- 알 수 없는 필드는 무시된다.
- 필수 필드 누락은 개발 단계에서 assertion 또는 로깅으로 확인한다.

## UserDefaults vs SwiftData
| 항목 | UserDefaults | SwiftData |
|---|---|---|
| 초기 구현 | 단순 | 상대적으로 큼 |
| 기록 수 | 199문제 수준에 충분 | 충분 |
| 구조 변경 | 직접 마이그레이션 필요 | 모델 기반 관리 |
| iCloud 확장 | 직접 설계 필요 | 후속 설계 필요 |
| 추천 | MVP 추천 | 후속 추천 |

## MVP 저장 기준
- StudyRecord: UserDefaults에 `[String: StudyRecord]` 형태로 JSON 인코딩.
- PencilNote: 앱 Documents 디렉터리에 문제 id별 `.drawing` 파일 저장.
- Settings: UserDefaults.
- 문제 원본: 앱 번들 JSON 읽기 전용.

## 참고 링크
- UserDefaults: https://developer.apple.com/documentation/foundation/userdefaults
- SwiftData: https://developer.apple.com/documentation/swiftdata

끝.
