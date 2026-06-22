import SwiftUI

struct QuestionTypeBadge: View {
    let type: QuestionType

    var body: some View {
        Text(type.rawValue)
            .font(.caption)
            .fontWeight(.semibold)
            .padding(.horizontal, 8)
            .padding(.vertical, 4)
            .foregroundStyle(.white)
            .background(background)
            .clipShape(Capsule())
    }

    private var background: Color {
        switch type {
        case .practical:
            .teal
        case .oral:
            .indigo
        case .common:
            .gray
        }
    }
}
