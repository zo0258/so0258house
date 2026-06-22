# Xcode Folder Structure

## 결론
Xcode 프로젝트는 기능별 폴더를 작게 나누고, `swift-drafts` 파일은 실제 앱 역할에 맞춰 이동한다. JSON 원본은 `Resources`에 넣고 읽기 전용 번들 데이터로 사용한다.

## 추천 Xcode 프로젝트명
- `So02HousePractical`

## Bundle Identifier 제안
- `com.so0258.so02house.practical`

## 최소 iOS 버전 제안
- MVP 권장: iOS 17 이상.
- 이유: SwiftUI와 iPad adaptive layout을 단순하게 유지하기 위함.
- 단, 실제 배포 대상 기기 iOS 버전은 Mac에서 Xcode 프로젝트 생성 시 다시 확인한다.

## 추천 폴더 구조
```text
So02HousePractical/
  App/
  Models/
  Repositories/
  ViewModels/
  Views/
  Components/
  Stores/
  Resources/
  Pencil/
  Keyboard/
```

## App
- `So02HousePracticalApp.swift`
- 앱 진입점.
- Repository, Store, Selector를 생성하고 화면에 주입한다.

## Models
- `QuestionModels.swift`
- `Question`, `DailyQuiz`, `StudyRecord`, `PencilNote`, `ReviewStatus`, `SubjectSummary`.
- JSON 구조와 앱 내부 모델을 정의한다.

## Repositories
- `QuestionRepository.swift`
- `DailyQuizSelector.swift`
- 번들 JSON 로딩과 오늘 문제 선택을 담당한다.

## ViewModels
- `PracticeViewModel.swift`
- 후속 생성 파일:
  - `TodayViewModel.swift`
  - `ReviewNoteViewModel.swift`
  - `StatsViewModel.swift`
- 화면 상태와 사용자 action을 관리한다.

## Views
- `TodayView.swift`
- `PracticeView.swift`
- `ReviewNoteView.swift`
- `StatsView.swift`
- `SettingsView.swift`
- `PencilNoteView.swift`

## Components
- `QuestionTypeBadge.swift`
- `ProgressHeader.swift`
- `QuestionMetaView.swift`
- `StatusButtonRow.swift`
- 반복 UI를 작게 분리한다.

## Stores
- `StudyRecordStore.swift`
- 기록 저장, 복원, 초기화를 담당한다.
- UserDefaults 구현은 MVP에서 유지한다.

## Resources
- `practical-questions.json`
- 앱 번들 리소스로 추가한다.
- Target Membership과 Copy Bundle Resources 포함 여부를 확인한다.
- 원본 문제 문장은 앱에서 수정하지 않는다.

## Pencil
- `PencilNoteStore.swift`
- 후속 생성 파일:
  - `PencilCanvasView.swift`
  - `PencilToolPickerController.swift`
- PencilKit 관련 코드를 한 곳에 모은다.

## Keyboard
- `KeyboardShortcutPlan.swift`
- 단축키 상수와 버튼 적용 예시를 둔다.
- 실제 navigation 연결은 View 구현 후 추가한다.

## swift-drafts 이동 기준
| 초안 파일 | 실제 폴더 | 비고 |
|---|---|---|
| QuestionModels.swift | Models | 그대로 이동 |
| QuestionRepository.swift | Repositories | Bundle Resource 확인 후 사용 |
| DailyQuizSelector.swift | Repositories | 날짜 선택 로직 유지 |
| StudyRecordStore.swift | Stores | UserDefaults key 유지 |
| PracticeViewModel.swift | ViewModels | View 연결 시 확장 |
| PencilNoteStore.swift | Pencil | PencilKit import 확인 |
| KeyboardShortcutPlan.swift | Keyboard | 실제 Button에 적용 |

## practical-questions.json 배치 기준
- `Resources/practical-questions.json`으로 추가한다.
- Xcode에서 `Add files to...`로 넣고 target membership을 체크한다.
- 앱 빌드 후 `Bundle.main.url(forResource: "practical-questions", withExtension: "json")`이 nil이 아닌지 확인한다.

끝.
