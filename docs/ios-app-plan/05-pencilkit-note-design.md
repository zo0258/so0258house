# So02House PencilKit Note Design

## 결론
Apple Pencil 메모는 iPad 학습 경험의 보조 기능으로 둔다. MVP는 문제별 PKDrawing 데이터를 파일로 저장하고, ReviewNoteView에서 다시 열 수 있게 한다.

## 사용 목적
- 실기 동작 순서 스케치.
- 구술 답변 키워드 구조화.
- 자세 / 호흡 / 안전 / 기록 체크 메모.
- 반복 복습 시 이전 손글씨 확인.

## 문제별 저장 방식
- 파일명: `{questionID}.drawing`.
- 위치: 앱 Documents 하위 `PencilNotes/`.
- 메타데이터: PencilNote 모델에 questionID, updatedAt, fileName 저장.
- StudyRecord와 PencilNote는 분리한다.

## PKCanvasView 래핑 구조
- SwiftUI에서 UIViewRepresentable로 PKCanvasView를 감싼다.
- `PencilCanvasView`는 drawing 바인딩 또는 저장 콜백을 받는다.
- iPad에서는 PKToolPicker를 표시한다.
- iPhone에서는 캔버스 편집을 제한하거나 텍스트 메모 중심으로 시작한다.

## PKDrawing 저장
- PKDrawing은 PKCanvasView의 드로잉 데이터를 저장하는 객체다.
- `dataRepresentation()`으로 Data를 만들고 파일에 저장한다.
- 다시 열 때 Data에서 PKDrawing을 복원한다.

## 이미지 저장 vs PKDrawing 데이터 저장
| 방식 | 장점 | 단점 | 판단 |
|---|---|---|---|
| 이미지 PNG | 미리보기 쉬움 | 재편집 어려움 | 썸네일 후속 |
| PKDrawing Data | 재편집 가능 | PencilKit 의존 | MVP 추천 |

## iPad 11인치 UX
- PracticeView에서 `메모` 버튼으로 PencilNoteView 진입.
- 가로 화면 후속안: 문제 카드 왼쪽, 캔버스 오른쪽.
- 세로 화면: 문제 요약 상단, 캔버스 하단.
- 자동 저장은 1초 debounce 또는 화면 이탈 시 저장으로 검토한다.

## iPhone UX
- 초기 MVP에서는 필기 작성보다 메모 보기와 텍스트 메모를 우선 검토한다.
- 손가락 입력 캔버스는 오작동 가능성이 있어 기본 기능에서 제외 가능하다.
- iPhone에서도 기존 iPad 메모 이미지는 확인할 수 있게 후속 설계한다.

## 복습노트 재열람 흐름
1. ReviewNoteView에서 문제 선택.
2. 문제 상세에서 메모 존재 여부 표시.
3. PencilNoteView로 이동.
4. 기존 PKDrawing을 로드.
5. 수정 후 자동 저장.

## 주의
- 필기 메모는 문제 원문과 별도 파일로 저장한다.
- 문제 JSON은 수정하지 않는다.
- iCloud 동기화는 후속 범위다.

## 참고 링크
- PencilKit: https://developer.apple.com/documentation/pencilkit
- PKDrawing: https://developer.apple.com/documentation/pencilkit/pkdrawing-swift.struct

끝.
