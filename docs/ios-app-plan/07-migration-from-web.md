# So02House Web to iOS Migration

## 결론
웹앱은 계속 운영하고, iOS 앱은 같은 JSON 데이터와 같은 학습 규칙을 공유한다. UI 구현은 새로 만들되 문제 원문, 2+2 출제, 기록형 UX, 복습노트 개념은 유지한다.

## 웹앱에서 유지할 요소
- 실기 2문제 + 구술 2문제.
- 날짜 기준 결정적 출제.
- 과목과 section 분산.
- 완료 / 다시 보기 / 어려움 기록.
- 복습노트 필터.
- 문제 원문 보존.
- `methodGuide`, `memoryTip`의 학습 보조 역할.

## iOS 앱에서 버릴 요소
- HTML 파일 기반 화면 생성.
- localStorage 직접 사용.
- GitHub Pages 경로 의존.
- 브라우저 DOM 중심 상태 관리.
- 정적 HTML에 문제 데이터 전체를 심는 구조.

## localStorage 전환 기준
- 웹: `health-exercise-practical-records` localStorage.
- iOS MVP: UserDefaults에 StudyRecord dictionary 저장.
- 후속: SwiftData로 마이그레이션.
- 마이그레이션 파일을 만들 경우 JSON export/import 구조를 별도 설계한다.

## JSON 데이터 재사용 전략
- `data/practical-questions.json`을 앱 번들에 추가한다.
- iOS 모델은 현재 필드를 모두 디코딩 가능하게 한다.
- 화면 노출용 모델에서는 `sourceVerified`, `needsReview`, `reviewReasons`를 숨긴다.
- 문제 원문은 앱에서 수정하지 않는다.

## 웹앱과 iOS 앱 병행 운영
- 웹앱: 빠른 접근, GitHub Pages 배포, 외부 공유용.
- iOS 앱: 오프라인 학습, Pencil 메모, Keyboard 단축키, 네이티브 UX.
- 문제 데이터 업데이트는 저장소에서 JSON을 갱신한 뒤 웹앱과 iOS 앱에 각각 반영한다.

## 문제 데이터 업데이트 방식
1. PDF 또는 원자료 검수.
2. `data/practical-questions.json` 업데이트.
3. 웹앱 HTML 재생성.
4. iOS 앱 번들 JSON 교체.
5. iOS JSON 로딩 테스트.
6. 문제 수와 type 분포 확인.

## 원문 문제 보존 원칙
- `question` 필드는 원문을 보존한다.
- 앱 화면에서 줄바꿈이나 표시 방식은 바꿀 수 있으나 문장 자체는 바꾸지 않는다.
- OCR 오류는 별도 검수 필드나 issue로 관리한다.

## methodGuide / memoryTip 고도화 전략
- 초기에는 현재 보유 문구를 사용자 친화적으로 보여준다.
- 해설은 임의 생성하지 않는다.
- 공신력 있는 출처 검수 후 sourceVerified를 true로 변경한다.
- 문제별 수행 순서, 답변 순서, 체크포인트를 별도 필드로 분리하는 후속 마이그레이션을 검토한다.

## 권장 단계
1. iOS MVP: JSON 로딩, 4문제 선택, 기록, 복습노트.
2. iPad MVP: PencilNote 저장.
3. 사용성 보강: Magic Keyboard, 검색.
4. 데이터 보강: methodGuide 정교화.
5. 저장소 고도화: SwiftData 또는 iCloud.

끝.
