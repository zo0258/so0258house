# Swift Compile Checklist

## 결론
현재 Windows 작업 환경에서는 Swift 컴파일을 검증하지 않았다. 이 문서는 Mac/Xcode에서 `swift-drafts` 초안을 실제 앱 파일로 옮긴 뒤 확인할 항목이다.

## 현재 상태
- Windows에서 문서와 Swift 초안만 작성했다.
- Xcode 프로젝트는 생성하지 않았다.
- iPhone 14 Pro, iPad 11인치 시뮬레이터 실행은 하지 않았다.
- Apple Pencil 기능은 실제 iPad에서만 최종 확인한다.
- Windows에서는 `validate_ios_plan.py`로 문서, JSON 계약, Swift 초안의 정적 조건만 확인한다.

## Xcode에서 확인할 import
- `Foundation`: 모델, JSON 디코딩, Date, UserDefaults, FileManager.
- `SwiftUI`: View, ObservableObject, keyboardShortcut.
- `PencilKit`: PKDrawing, PKCanvasView, PKToolPicker.

## 파일별 import 기준
| 파일 | 필요 import | 확인 항목 |
|---|---|---|
| QuestionModels.swift | Foundation | Codable, Identifiable 컴파일 |
| QuestionRepository.swift | Foundation | Bundle JSON 로딩 |
| DailyQuizSelector.swift | Foundation | 날짜 계산과 4문제 선택 |
| StudyRecordStore.swift | Foundation | UserDefaults 저장/복원 |
| PracticeViewModel.swift | Foundation | ObservableObject 컴파일 |
| TodayViewModel.swift | Foundation | 오늘 완료/복습/어려움 집계 |
| ReviewNoteViewModel.swift | Foundation | 복습노트 필터 |
| StatsViewModel.swift | Foundation | 과목별 집계 |
| PencilNoteStore.swift | Foundation, PencilKit | PKDrawing 저장/복원 |
| KeyboardShortcutPlan.swift | SwiftUI | keyboardShortcut 적용 |
| QuestionDataContractTests.swift | XCTest | JSON 계약 테스트 |

## QuestionModels.swift
- `Question`이 현재 JSON 필드를 모두 디코딩하는지 확인한다.
- `sourceRefs`의 `title`, `url`이 정상 디코딩되는지 확인한다.
- `reviewReasons`는 누락 가능성을 고려해 optional 유지 여부를 확인한다.
- `type` 문자열이 `QuestionType`으로 변환되는지 확인한다.

## QuestionRepository.swift
- `practical-questions.json`이 Bundle Resource에 포함됐는지 확인한다.
- 로딩 결과 문제 수가 199인지 확인한다.
- 디코딩 실패 시 Xcode console에 에러가 보이는지 확인한다.
- 파일명이 `practical-questions.json`과 정확히 일치하는지 확인한다.

## DailyQuizSelector.swift
- 같은 날짜에 항상 같은 4문제가 선택되는지 확인한다.
- 실기 2문제 + 구술 2문제인지 확인한다.
- 과목과 section이 가능한 범위에서 분산되는지 확인한다.
- 날짜를 바꾸면 다른 문제가 나오는지 확인한다.

## StudyRecordStore.swift
- 완료 / 다시 보기 / 어려움 저장 후 앱 재실행 시 복원되는지 확인한다.
- 같은 문제를 다시 기록하면 기존 기록이 갱신되는지 확인한다.
- 기록 초기화가 UserDefaults key만 제거하는지 확인한다.

## PracticeViewModel.swift
- `ObservableObject` + `@Published` 방식이 현재 Xcode 타깃에서 컴파일되는지 확인한다.
- iOS 17 이상으로 잡을 경우 Observation 매크로 전환 여부를 검토한다.
- 상태 선택 전에는 다음 문제로 넘어가지 않는 흐름을 유지한다.
- 마지막 문제 기록 후 완료 상태가 되는지 확인한다.

## TodayViewModel.swift
- 오늘 문제 4개 기준 완료 수가 계산되는지 확인한다.
- 복습과 어려움 수가 StudyRecordStore 기록과 일치하는지 확인한다.
- TodayView가 다시 나타날 때 `refresh()`가 호출되는지 확인한다.

## ReviewNoteViewModel.swift
- 전체 / 다시 보기 / 어려움 필터가 기록 상태와 맞는지 확인한다.
- records에는 있으나 JSON에 없는 questionID를 무시하는지 확인한다.
- 최신 기록이 위에 오도록 정렬되는지 확인한다.

## StatsViewModel.swift
- 과목별 totalCount가 JSON 원본 집계와 일치하는지 확인한다.
- 완료 / 다시 보기 / 어려움 수가 중복 계산되지 않는지 확인한다.
- 실기/구술 수가 `QuestionType` 변환 기준과 일치하는지 확인한다.

## PencilNoteStore.swift
- `#if canImport(PencilKit)` 분기가 Xcode iOS 타깃에서 정상 컴파일되는지 확인한다.
- `PKDrawing.dataRepresentation()` 저장이 되는지 확인한다.
- 저장한 `.drawing` 파일을 다시 열어 PKDrawing으로 복원하는지 확인한다.
- Documents 하위 `PencilNotes/` 폴더가 자동 생성되는지 확인한다.

## KeyboardShortcutPlan.swift
- `keyboardShortcut`이 각 Button에 정상 적용되는지 확인한다.
- Command + 1, Command + 2, Command + 3이 상태 기록과 연결되는지 확인한다.
- Command + R, Command + T, Command + M은 실제 Navigation 구현 후 연결한다.
- 시스템 단축키와 충돌하는 조합은 추가하지 않는다.

## QuestionDataContractTests.swift
- 테스트 타깃 이름의 `@testable import So02HousePractical`가 실제 프로젝트명과 맞는지 확인한다.
- JSON 199문제 로딩 테스트가 통과하는지 확인한다.
- 오늘 4문제 선택 테스트가 통과하는지 확인한다.

## iPhone 14 Pro 시뮬레이터
- TodayView 첫 화면이 세로 기준으로 잘리는 곳 없이 표시되는지 확인한다.
- PracticeView에서 유형 배지, 과목, section, 연도 줄바꿈을 확인한다.
- 상태 버튼 3개가 한 손 조작에 무리 없는지 확인한다.
- Dynamic Type 기본 크기와 큰 글씨 1단계에서 겹침이 없는지 확인한다.

## iPad 11인치 시뮬레이터
- 세로 화면에서 TodayView와 PracticeView 여백을 확인한다.
- 가로 화면에서 NavigationSplitView 적용 여부를 확인한다.
- ReviewNoteView 목록과 상세 화면 분리 가능성을 확인한다.
- Magic Keyboard 단축키는 시뮬레이터와 실제 기기에서 모두 확인한다.

## 실제 iPad + Apple Pencil
- PKCanvasView에 Pencil 입력이 자연스럽게 들어오는지 확인한다.
- 필기 저장 후 앱 재실행 시 복원되는지 확인한다.
- 문제별 메모 파일이 서로 섞이지 않는지 확인한다.
- iPhone에서는 Pencil 메모 편집을 제한할지 최종 판단한다.

끝.
