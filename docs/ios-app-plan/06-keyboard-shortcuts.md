# So02House Keyboard Shortcuts

## 결론
Magic Keyboard 단축키는 iPad 학습 속도를 높이는 보조 기능으로 둔다. 기본 iOS 시스템 단축키와 충돌 가능성이 큰 조합은 피하고, 상태 기록 중심으로 설계한다.

## 단축키 원칙
- 한 손으로 누르기 쉬운 조합을 우선한다.
- 시스템 단축키와 흔히 겹치는 `Command + Space`, `Command + Tab`, `Command + H`는 제외한다.
- 삭제나 초기화 같은 위험 작업에는 단축키를 두지 않는다.
- 단축키는 버튼 동작과 같은 action을 호출한다.

## 제안 단축키
| 기능 | 단축키 | 비고 |
|---|---|---|
| 완료 | Command + 1 | 현재 문제 완료 |
| 다시 보기 | Command + 2 | 복습노트에 남김 |
| 어려움 | Command + 3 | 어려움으로 남김 |
| 다음 문제 | 없음 | 상태 선택이 다음 이동을 겸함 |
| 복습노트 이동 | Command + R | ReviewNoteView |
| 검색 | Command + F | 후속 검색 기능 |
| TodayView 복귀 | Command + T | 홈 역할 |
| 메모 열기 | Command + M | PencilNoteView |

## 상태 기록 방식
- PracticeView의 버튼에 `keyboardShortcut`을 붙인다.
- 사용자가 단축키를 누르면 상태 저장 후 다음 문제로 이동한다.
- 마지막 문제에서는 완료 화면으로 이동한다.

## SwiftUI 예시
```swift
Button("완료") {
    viewModel.mark(.done)
}
.keyboardShortcut("1", modifiers: [.command])

Button("다시 보기") {
    viewModel.mark(.review)
}
.keyboardShortcut("2", modifiers: [.command])

Button("어려움") {
    viewModel.mark(.hard)
}
.keyboardShortcut("3", modifiers: [.command])
```

## 검색 단축키
- MVP에 검색이 없다면 `Command + F`는 예약만 한다.
- 검색 추가 전까지는 구현하지 않는다.

## 충돌 가능성으로 제외
- Command + Space: Spotlight.
- Command + Tab: 앱 전환.
- Command + H: 홈.
- Command + W: 창 닫기 의미가 강함.
- Command + Q: iPad 앱에서는 일반적이지 않지만 종료 의미가 강함.

## 참고 링크
- KeyboardShortcut: https://developer.apple.com/documentation/SwiftUI/KeyboardShortcut
- keyboardShortcut modifier: https://developer.apple.com/documentation/swiftui/view/keyboardshortcut%28_%3A%29-3vjx6

끝.
