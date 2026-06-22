# iOS QA Matrix

## 결론
MVP QA는 기능별로 iPhone 14 Pro, iPad 11인치 세로, iPad 11인치 가로, 실제 iPad + Apple Pencil을 나눠 확인한다. 시뮬레이터로 충분한 항목과 실기기 필수 항목을 분리한다.

## 대상 환경
| 환경 | 목적 | 필수 여부 |
|---|---|---|
| iPhone 14 Pro 시뮬레이터 | 작은 화면 세로 흐름 | 필수 |
| iPad 11인치 시뮬레이터 세로 | 태블릿 세로 흐름 | 필수 |
| iPad 11인치 시뮬레이터 가로 | SplitView 후보 검증 | 필수 |
| 실제 iPad + Apple Pencil | PencilKit 입력감과 저장 | 필수 |
| 실제 Magic Keyboard | 단축키 입력 | 권장 |

## 기능별 QA
| 기능 | iPhone | iPad 세로 | iPad 가로 | 실기기 |
|---|---|---|---|---|
| JSON 199문제 로딩 | 예 | 예 | 예 | 예 |
| 오늘 4문제 선택 | 예 | 예 | 예 | 예 |
| 실기 2 + 구술 2 | 예 | 예 | 예 | 예 |
| 상태 기록 저장 | 예 | 예 | 예 | 예 |
| 복습노트 필터 | 예 | 예 | 예 | 예 |
| Pencil 메모 | 보기 중심 | 예 | 예 | 실제 Pencil 필수 |
| Keyboard 단축키 | 제외 가능 | 예 | 예 | 실제 키보드 권장 |
| SplitView | 해당 없음 | 선택 | 예 | 예 |

## iPhone 14 Pro 체크
- TodayView 첫 화면에서 주요 CTA가 보이는지 확인한다.
- PracticeView에서 유형 배지와 메타 정보가 겹치지 않는지 확인한다.
- 상태 버튼 3개가 세로로 배치되어도 화면 흐름이 자연스러운지 확인한다.
- 복습노트 필터가 한 줄 또는 자연스러운 줄바꿈으로 표시되는지 확인한다.

## iPad 11인치 세로 체크
- TodayView 요약과 오늘 문제 리스트가 과밀하지 않은지 확인한다.
- PracticeView 카드 폭이 너무 넓어 읽기 불편하지 않은지 확인한다.
- PencilNoteView에서 캔버스 높이가 충분한지 확인한다.
- ReviewNoteView 목록 항목이 손가락 터치에 충분한 높이인지 확인한다.

## iPad 11인치 가로 체크
- NavigationSplitView sidebar가 과도하게 넓지 않은지 확인한다.
- PracticeView와 PencilNoteView 병렬 배치 가능성을 확인한다.
- ReviewNoteView 목록과 상세 화면 분리가 자연스러운지 확인한다.
- Magic Keyboard 단축키가 포커스 상태와 무관하게 동작하는지 확인한다.

## 실제 iPad + Apple Pencil 체크
- Pencil 입력 지연이 학습에 방해되지 않는지 확인한다.
- 손바닥 터치 오작동이 없는지 확인한다.
- PKDrawing 저장 후 앱 재실행 시 복원되는지 확인한다.
- 문제별 메모 파일이 다른 문제와 섞이지 않는지 확인한다.

## 실패 기록 방식
- 실패 기기.
- 재현 단계.
- 기대 결과.
- 실제 결과.
- 관련 파일.
- 다음 조치.

끝.
