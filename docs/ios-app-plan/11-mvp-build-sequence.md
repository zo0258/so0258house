# MVP Build Sequence

## 결론
Mac에서는 화면부터 만들지 말고 데이터 로딩과 선택 로직을 먼저 고정한다. 그다음 TodayView, PracticeView, 기록 저장, 복습노트, iPad/Pencil/Keyboard 순서로 붙인다.

## 1단계: 새 iOS App 프로젝트 생성
완료 기준:
- Xcode에서 `So02HousePractical` 프로젝트가 생성된다.
- SwiftUI App lifecycle로 빈 앱이 실행된다.

실패 시 확인:
- Xcode 설치 상태.
- Apple ID 로그인 여부.
- Team 선택 여부.
- Bundle Identifier 중복 여부.

## 2단계: practical-questions.json 번들 추가
완료 기준:
- `Resources/practical-questions.json`이 프로젝트에 보인다.
- Target Membership이 체크되어 있다.
- Copy Bundle Resources에 포함되어 있다.

실패 시 확인:
- 파일명이 `practical-questions.json`인지 확인.
- 폴더 reference가 아니라 실제 리소스로 들어갔는지 확인.

## 3단계: Question 모델 컴파일
완료 기준:
- `QuestionModels.swift`가 컴파일된다.
- Codable, Identifiable 관련 에러가 없다.

실패 시 확인:
- 파일이 target에 포함됐는지 확인.
- enum rawValue가 JSON의 `실기`, `구술`과 일치하는지 확인.

## 4단계: JSON 199문제 로딩 테스트
완료 기준:
- `QuestionRepository.loadQuestions()` 결과가 199개다.
- 실기 99개, 구술 100개가 확인된다.

실패 시 확인:
- Bundle URL이 nil인지 확인.
- JSONDecoder 에러 메시지 확인.
- `sourceRefs`, `reviewReasons` optional 처리 확인.

## 5단계: DailyQuizSelector로 오늘 4문제 선택
완료 기준:
- 오늘 날짜 기준 4문제가 선택된다.
- 실기 2문제 + 구술 2문제다.
- 같은 날짜에 다시 실행해도 같은 결과다.

실패 시 확인:
- Date와 Calendar timezone 차이 확인.
- `type` 문자열 변환 확인.
- fallback 로직이 중복 id를 만들지 않는지 확인.

## 6단계: TodayView
완료 기준:
- 오늘 완료 0/4, 복습 0, 어려움 0이 표시된다.
- 오늘 문제 요약이 표시된다.
- PracticeView로 이동할 수 있다.

실패 시 확인:
- ViewModel이 quiz와 records를 제대로 받는지 확인.
- iPhone 14 Pro 세로에서 텍스트가 잘리지 않는지 확인.

## 7단계: PracticeView
완료 기준:
- `1/4 문제`, `기록 0/4`가 표시된다.
- 유형 배지, 과목, section, 연도, 문제 원문이 표시된다.
- 완료 / 다시 보기 / 어려움 버튼이 보인다.

실패 시 확인:
- 상태 버튼 action이 ViewModel과 연결됐는지 확인.
- 마지막 문제에서 완료 화면으로 바뀌는지 확인.

## 8단계: UserDefaults 기록 저장
완료 기준:
- 상태 선택 후 앱 재실행 시 기록이 복원된다.
- TodayView의 오늘 완료 수가 갱신된다.

실패 시 확인:
- UserDefaults key가 동일한지 확인.
- JSONEncoder/Decoder가 Date를 정상 처리하는지 확인.
- 같은 문제 재기록 시 덮어쓰기 되는지 확인.

## 9단계: ReviewNoteView
완료 기준:
- 전체 / 다시 보기 / 어려움 필터가 동작한다.
- 다시 보기와 어려움 문제만 목록에 나온다.
- 문제 선택 시 상세 화면으로 이동한다.

실패 시 확인:
- StudyRecord.status와 필터 값 매핑 확인.
- 기록은 있으나 문제 id가 JSON에 없는 경우 처리 확인.

## 10단계: iPad NavigationSplitView
완료 기준:
- iPad 11인치 가로에서 sidebar와 detail이 분리된다.
- Today, Practice, Review, Stats, Settings 이동이 가능하다.

실패 시 확인:
- iPhone에서는 NavigationStack으로 collapse되는지 확인.
- ViewModel 공유 구조가 중복 생성되지 않는지 확인.

## 11단계: PencilKit 메모
완료 기준:
- 문제별 PencilNoteView가 열린다.
- PKDrawing 저장과 복원이 된다.
- 문제 id별 파일이 분리된다.

실패 시 확인:
- PencilKit import와 target iOS 설정 확인.
- Documents/PencilNotes 폴더 생성 확인.
- 실제 iPad + Apple Pencil 입력 확인.

## 12단계: Magic Keyboard 단축키
완료 기준:
- Command + 1: 완료.
- Command + 2: 다시 보기.
- Command + 3: 어려움.
- Command + R/T/M은 navigation 구현 후 연결된다.

실패 시 확인:
- Button에 `keyboardShortcut`이 붙어 있는지 확인.
- focus 상태와 상관없이 동작하는지 확인.
- 시스템 단축키와 충돌하지 않는지 확인.

## 13단계: 실기기 QA
완료 기준:
- iPhone 14 Pro 실제 기기 또는 시뮬레이터에서 주요 흐름 통과.
- iPad 11인치 실제 기기에서 Pencil 메모 저장/복원 통과.
- 앱 재실행 후 기록과 메모가 유지된다.

실패 시 확인:
- 실제 기기 iOS 버전.
- 저장 권한과 파일 경로.
- 화면 회전과 split view 상태.
- Dynamic Type 큰 글씨에서 레이아웃 깨짐 여부.

끝.
