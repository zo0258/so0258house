# So02House iOS App Product Spec

## 결론
기존 GitHub Pages 웹앱은 유지하고, iOS 앱은 건강운동관리사 실기·구술 대비에 집중한 오프라인 우선 학습 앱으로 만든다. MVP는 하루 4문제, 기록, 복습노트, 문제별 메모까지로 제한한다.

## 앱 목적
- PDF에서 추출한 기출문제 기반 실기·구술 학습을 iPhone과 iPad에서 빠르게 반복한다.
- 객관식 채점이 아니라 `완료 / 다시 보기 / 어려움` 기록형 학습 흐름을 유지한다.
- 웹앱의 JSON 문제 데이터를 iOS 번들 리소스로 재사용한다.

## 주요 사용자
- 건강운동관리사 실기·구술 시험을 준비하는 1인 학습자.
- 짧은 시간에 매일 반복하고, 어려운 문제를 다시 보는 사용자를 기준으로 한다.

## 하루 학습 흐름
1. TodayView에서 오늘 4문제 현황을 확인한다.
2. PracticeView에서 실기 2문제 + 구술 2문제를 순서대로 본다.
3. 각 문제마다 `완료 / 다시 보기 / 어려움` 중 하나를 기록한다.
4. 필요하면 PencilNoteView에서 문제별 메모를 남긴다.
5. ReviewNoteView에서 다시 보기와 어려움 문제만 반복한다.

## 2+2 문제 구조
- 기본 구성: 실기 2문제 + 구술 2문제.
- 같은 날짜에는 같은 문제가 나오도록 날짜 기반 결정적 선택을 사용한다.
- 가능하면 과목과 section이 겹치지 않도록 분산한다.
- 부족한 경우에만 같은 과목 또는 같은 section을 허용한다.

## 복습노트 구조
- 전체 / 다시 보기 / 어려움 필터를 제공한다.
- 문제 원문, 과목, section, 연도, 유형, 최근 기록일을 표시한다.
- iPad에서는 문제와 필기 메모를 나란히 보는 구조를 후속 범위로 둔다.

## iPhone 사용 시나리오
- 이동 중 4문제 기록에 집중한다.
- 필기보다는 상태 기록, 짧은 텍스트 메모, 복습 목록 확인을 우선한다.
- iPhone 14 Pro 세로 화면 기준으로 한 화면에 문제, 유형 배지, 상태 버튼이 자연스럽게 들어오게 한다.

## iPad 사용 시나리오
- 책상 학습과 시범 답변 연습을 기준으로 한다.
- iPad 11인치에서는 TodayView와 PracticeView를 넓게 쓰고, Apple Pencil 메모를 적극 활용한다.
- 가로 화면에서는 사이드바 + 상세 화면 구조를 우선 검토한다.

## Apple Pencil 방향
- 문제별 손글씨 메모, 동작 순서 스케치, 답변 구조 메모에 사용한다.
- PencilKit의 PKCanvasView와 PKDrawing을 사용한다.
- Apple 공식 문서 기준으로 PKDrawing은 PKCanvasView의 사용자 드로잉 데이터를 저장하는 객체다.

## Magic Keyboard 방향
- iPad에서 손을 화면으로 옮기지 않고 기록할 수 있게 한다.
- 완료, 다시 보기, 어려움, 검색, 복습노트 이동, TodayView 복귀를 단축키 대상으로 둔다.
- SwiftUI `keyboardShortcut`은 버튼이나 토글에 키 조합을 지정하는 방식으로 설계한다.

## MVP 범위
- 번들 JSON 로딩.
- 날짜 기준 4문제 선택.
- 완료 / 다시 보기 / 어려움 기록.
- 복습노트 필터.
- UserDefaults 기반 StudyRecord 저장.
- 문제별 PencilKit 메모 파일 저장 초안.
- iPhone 14 Pro / iPad 11인치 adaptive layout.

## 후속 고도화 범위
- SwiftData 전환.
- iCloud 동기화.
- 문제 검색과 과목별 통계 고도화.
- methodGuide / memoryTip 원자료 검수 후 보강.
- 실제 iPad Apple Pencil UX 튜닝.
- 앱 아이콘, 스플래시, App Store 배포 설정.

## 참고 링크
- PencilKit: https://developer.apple.com/documentation/pencilkit
- PKDrawing: https://developer.apple.com/documentation/pencilkit/pkdrawing-swift.struct
- KeyboardShortcut: https://developer.apple.com/documentation/SwiftUI/KeyboardShortcut

끝.
