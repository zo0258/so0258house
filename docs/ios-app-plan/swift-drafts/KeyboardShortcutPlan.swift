import SwiftUI

enum AppShortcut {
    static let done = KeyboardShortcut("1", modifiers: [.command])
    static let review = KeyboardShortcut("2", modifiers: [.command])
    static let hard = KeyboardShortcut("3", modifiers: [.command])
    static let reviewNote = KeyboardShortcut("r", modifiers: [.command])
    static let today = KeyboardShortcut("t", modifiers: [.command])
    static let memo = KeyboardShortcut("m", modifiers: [.command])
    static let search = KeyboardShortcut("f", modifiers: [.command])
}

struct PracticeStatusButtons: View {
    let mark: (ReviewStatus) -> Void

    var body: some View {
        HStack {
            Button("완료") {
                mark(.done)
            }
            .keyboardShortcut(AppShortcut.done)

            Button("다시 보기") {
                mark(.review)
            }
            .keyboardShortcut(AppShortcut.review)

            Button("어려움") {
                mark(.hard)
            }
            .keyboardShortcut(AppShortcut.hard)
        }
    }
}
