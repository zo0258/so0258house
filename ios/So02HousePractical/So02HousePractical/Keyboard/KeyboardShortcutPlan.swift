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
        HStack(spacing: 10) {
            Button {
                mark(.done)
            } label: {
                Label("완료", systemImage: "checkmark.circle")
            }
            .keyboardShortcut(AppShortcut.done)

            Button {
                mark(.review)
            } label: {
                Label("다시 보기", systemImage: "arrow.uturn.backward.circle")
            }
            .keyboardShortcut(AppShortcut.review)

            Button {
                mark(.hard)
            } label: {
                Label("어려움", systemImage: "exclamationmark.triangle")
            }
            .keyboardShortcut(AppShortcut.hard)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
    }
}
