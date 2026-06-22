# Mac Xcode Next Steps

## 결론
Mac에서는 새 iOS App 프로젝트를 만들고, 먼저 JSON 로딩과 DailyQuizSelector 테스트부터 확인한다. PencilKit은 실제 iPad에서 별도로 검증한다.

## 체크리스트
1. Xcode 설치와 실행 확인.
2. 새 iOS App 프로젝트 생성.
3. SwiftUI App lifecycle 선택.
4. Bundle Identifier 설정.
5. 최소 iOS 버전 설정.
6. `practical-questions.json`을 앱 번들에 추가.
7. Swift 초안 파일을 프로젝트에 복사.
8. JSON 로딩 테스트.
9. iPhone 14 Pro 시뮬레이터 확인.
10. iPad 11인치 시뮬레이터 확인.
11. Apple Pencil 기능은 실제 iPad에서 확인.
12. GitHub 저장소 분리 여부 결정.

## Bundle Identifier 제안
- `com.so0258.so02house.practical`
- 개인 Apple Developer 계정의 Team ID와 충돌 여부는 Xcode에서 확인 필요.

## 최소 iOS 버전 제안
- PencilKit과 SwiftUI 기본 구현은 가능하지만, SwiftData까지 바로 쓸 계획이면 배포 대상 제약이 커진다.
- MVP는 UserDefaults + 파일 저장이므로 최소 버전은 Mac에서 설치된 Xcode와 타깃 기기 기준으로 다시 확정한다.
- 문서 초안 기준 추천: iOS 17 이상.

## practical-questions.json 추가
- Xcode Project Navigator에 JSON 파일 추가.
- Target Membership 체크.
- Copy Bundle Resources에 포함됐는지 확인.
- 파일명은 `practical-questions.json` 유지.

## Swift 모델 파일 생성
- `QuestionModels.swift`.
- `QuestionRepository.swift`.
- `DailyQuizSelector.swift`.
- `StudyRecordStore.swift`.
- `PracticeViewModel.swift`.
- `PencilNoteStore.swift`.
- `KeyboardShortcutPlan.swift`.

## JSON 로딩 테스트
- 앱 시작 시 Repository로 `[Question]` 로드.
- 문제 수 199 확인.
- 실기 99, 구술 100 확인.
- 첫 문제 id와 question이 JSON과 같은지 확인.

## 시뮬레이터 확인
- iPhone 14 Pro: 세로 PracticeView, 버튼, 배지 줄바꿈.
- iPad 11인치: 세로/가로 TodayView, split view 후보.
- Dynamic Type 기본 크기와 큰 글씨 1단계 정도까지 확인.

## Apple Pencil 테스트
- 시뮬레이터만으로는 실제 필기감 검증이 부족하다.
- 실제 iPad 11인치와 Apple Pencil로 PKCanvasView 입력, 저장, 재열람을 확인한다.

## GitHub 저장소 분리 검토
- 같은 저장소 유지: JSON과 문서 공유가 쉽다.
- 별도 저장소: iOS 프로젝트 관리가 깔끔하다.
- 추천: MVP까지는 같은 저장소의 `ios/` 또는 별도 로컬 프로젝트로 시작하고, 빌드 가능해진 뒤 분리 여부를 결정한다.

## Mac에서 첫 실행 목표
1. 빈 SwiftUI 앱 실행.
2. JSON 199문제 로딩.
3. 오늘 4문제 선택.
4. PracticeView에 첫 문제 표시.
5. UserDefaults 기록 저장.

끝.
