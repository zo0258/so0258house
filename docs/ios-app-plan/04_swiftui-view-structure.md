# So02House SwiftUI View Structure

## 결론
초기 구조는 Repository, Selector, Store, ViewModel, View를 분리한다. 파일 수는 늘리되 역할을 작게 유지해서 6개월 뒤에도 수정 가능한 형태로 둔다.

## 권장 폴더 구조
```text
So02House/
  So02HouseApp.swift
  Models/
    QuestionModels.swift
  Data/
    QuestionRepository.swift
    DailyQuizSelector.swift
    StudyRecordStore.swift
    PencilNoteStore.swift
  ViewModels/
    PracticeViewModel.swift
    TodayViewModel.swift
    ReviewNoteViewModel.swift
  Views/
    TodayView.swift
    PracticeView.swift
    ReviewNoteView.swift
    StatsView.swift
    SettingsView.swift
    PencilNoteView.swift
  Components/
    QuestionTypeBadge.swift
    ProgressHeader.swift
    StatusButtonRow.swift
    QuestionMetaView.swift
```

## App 진입점
- `So02HouseApp`에서 Repository와 Store를 생성한다.
- MVP에서는 EnvironmentObject보다 명시적 주입을 우선 검토한다.
- 앱 시작 시 JSON 로딩 실패를 TodayView에서 오류 상태로 표시한다.

## Repository
- `QuestionRepository`는 번들 JSON을 읽는다.
- 네트워크는 MVP에 넣지 않는다.
- JSON 로딩과 디코딩만 담당한다.

## Selector
- `DailyQuizSelector`는 날짜 기준 4문제를 선택한다.
- 실기 2 + 구술 2를 우선한다.
- 과목과 section 중복을 낮추는 scoring을 둔다.

## Store
- `StudyRecordStore`는 UserDefaults 기반 기록 저장.
- `PencilNoteStore`는 파일 기반 PKDrawing 데이터 저장.
- Store는 SwiftUI View가 직접 UserDefaults나 FileManager를 만지지 않게 한다.

## ViewModel
- PracticeViewModel: 현재 문제 index, 기록 수, 상태 저장, 다음 문제 이동.
- TodayViewModel: 오늘 문제와 오늘 기록 요약.
- ReviewNoteViewModel: 복습 문제 필터와 목록.

## TodayView
- iPhone: 세로 카드형.
- iPad: 넓은 요약 + 오늘 문제 리스트.
- CTA는 `오늘 4문제 시작`을 최우선으로 둔다.

## PracticeView
- 문제 카드 구조:
  - 진행률.
  - 유형 배지.
  - 과목 / section / 연도.
  - 문제 원문.
  - 가이드.
  - 상태 버튼.
- 상태 선택 없이는 다음 문제로 가지 않는다.

## ReviewNoteView
- 전체 / 다시 보기 / 어려움 segmented control.
- 리스트 선택 시 상세로 이동.
- iPad에서는 detail column에 문제 상세 표시.

## StatsView
- MVP에서는 단순 집계.
- 차트 라이브러리는 추가하지 않는다.
- SwiftUI 기본 List, Grid, ProgressView만 사용한다.

## SettingsView
- 데이터 버전.
- 기록 초기화.
- 메모 파일 사용량.
- 원문 보존 원칙 안내.

## iPhone / iPad adaptive 기준
- iPhone 14 Pro: NavigationStack.
- iPad 11인치: NavigationSplitView 우선.
- 화면 폭이 좁아지면 split view는 자동 collapse되는 흐름을 따른다.

## NavigationStack vs NavigationSplitView
- iPhone: NavigationStack.
- iPad: NavigationSplitView.
- 코드 중복을 줄이기 위해 ViewModel은 공유하고 컨테이너만 분리한다.

## 참고 링크
- SwiftUI: https://developer.apple.com/documentation/swiftui
- NavigationSplitView: https://developer.apple.com/documentation/SwiftUI/NavigationSplitView

끝.
