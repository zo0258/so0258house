# iOS Risk Register

## 결론
가장 큰 위험은 Swift 초안의 실제 컴파일 미검증, PencilKit 실기기 UX 미검증, JSON 데이터 고도화 지연이다. MVP에서는 범위를 줄이고 검증 순서를 앞당기는 방식으로 대응한다.

## 리스크 목록
| ID | 리스크 | 영향 | 가능성 | 대응 |
|---|---|---:|---:|---|
| R1 | Windows에서 Swift 컴파일 미검증 | 높음 | 높음 | Mac 첫 작업을 컴파일 확인으로 시작 |
| R2 | JSON Bundle Resource 누락 | 높음 | 중간 | Xcode Copy Bundle Resources 확인 |
| R3 | Date timezone 차이로 오늘 문제 불일치 | 중간 | 중간 | Calendar와 dateKey 테스트 추가 |
| R4 | PencilKit 저장/복원 실패 | 높음 | 중간 | 실제 iPad에서 11단계 전에 단독 검증 |
| R5 | Magic Keyboard 단축키 충돌 | 낮음 | 중간 | 시스템 단축키 제외, 실제 키보드 QA |
| R6 | SwiftData 조기 도입으로 복잡도 증가 | 중간 | 중간 | MVP는 UserDefaults 유지 |
| R7 | methodGuide 미검수 상태 노출 | 중간 | 중간 | 공개 모델에서 내부 검수 상태 숨김 |
| R8 | iPad SplitView 구조 과설계 | 중간 | 중간 | iPhone NavigationStack 먼저 완성 |
| R9 | 문제 데이터 업데이트 경로 불명확 | 중간 | 중간 | 데이터 계약 문서와 검증 스크립트 유지 |
| R10 | 실제 사용자 흐름보다 기능이 많아짐 | 중간 | 중간 | 하루 4문제 완료 흐름 우선 |

## 우선 대응 순서
1. QuestionModels.swift 컴파일.
2. JSON 199문제 로딩.
3. DailyQuizSelector 결과 확인.
4. StudyRecordStore 저장/복원.
5. iPhone PracticeView.
6. ReviewNoteView.
7. iPad layout.
8. PencilKit.
9. Keyboard shortcuts.

## 보류할 결정
- SwiftData 전환 여부.
- iCloud 동기화.
- App Store 배포.
- iPhone Pencil 편집 지원.
- 문제 검색 범위.

## MVP 중단 기준
- JSON 로딩이 안정화되지 않으면 UI 작업을 늘리지 않는다.
- 기록 저장/복원이 실패하면 PencilKit으로 넘어가지 않는다.
- iPad layout이 흔들리면 iPhone 단일 흐름을 먼저 고정한다.

끝.
