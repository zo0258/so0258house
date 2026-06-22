# iOS Implementation Backlog

## 결론
MVP는 데이터 로딩, 오늘 문제, 상태 기록, 복습노트까지다. PencilKit과 Keyboard는 MVP 후반에 붙이고, SwiftData와 iCloud는 후속으로 미룬다.

## P0: MVP 필수
- Xcode 프로젝트 생성.
- `practical-questions.json` 번들 추가.
- QuestionModels 컴파일.
- QuestionRepository 로딩.
- DailyQuizSelector 선택.
- TodayView.
- PracticeView.
- StudyRecordStore.
- ReviewNoteView.
- iPhone 14 Pro QA.

## P1: iPad 학습 경험
- iPad 11인치 세로 layout.
- iPad 11인치 가로 NavigationSplitView.
- PencilNoteStore.
- PencilCanvasView.
- PencilNoteView.
- 실제 iPad + Apple Pencil QA.

## P2: 조작 속도
- KeyboardShortcutPlan 적용.
- Command + 1/2/3 상태 기록.
- Command + R 복습노트.
- Command + T TodayView.
- Command + M 메모.
- 실제 Magic Keyboard QA.

## P3: 학습 관리
- StatsView.
- 과목별 summary.
- section별 어려움 수.
- 최근 복습 문제.
- 데이터 버전 표시.

## P4: 데이터 고도화
- methodGuide 검수.
- memoryTip 보강.
- sourceRefs 정리.
- sourceVerified true 전환 기준.
- needsReview 해소 목록.

## P5: 후속 기술
- SwiftData 전환 검토.
- iCloud 동기화 검토.
- 검색 기능.
- App Icon.
- Launch Screen.
- App Store 배포 준비.

## 하지 않을 일
- MVP에서 서버 연동.
- MVP에서 로그인.
- MVP에서 결제.
- MVP에서 AI 해설 자동 생성.
- MVP에서 원문 문제 수정.

## 첫 주 작업 추천
1. Mac에서 컴파일 확인.
2. JSON 로딩.
3. DailyQuizSelector.
4. TodayView.
5. PracticeView.
6. UserDefaults 기록.
7. ReviewNoteView.

끝.
