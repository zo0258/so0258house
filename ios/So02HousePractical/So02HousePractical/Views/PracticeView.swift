import SwiftUI

struct PracticeView: View {
    @Environment(\.dismiss) private var dismiss
    @StateObject var viewModel: PracticeViewModel

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 16) {
                HStack {
                    Text(viewModel.progressText)
                        .font(.headline)
                    Spacer()
                    Text(viewModel.recordText)
                        .font(.subheadline)
                        .foregroundStyle(.secondary)
                }

                if let question = viewModel.currentQuestion {
                    QuestionCard(question: question)

                    PracticeStatusButtons { status in
                        viewModel.mark(status)
                    }
                    .buttonStyle(.borderedProminent)
                } else {
                    completionView
                }
            }
            .padding()
            .frame(maxWidth: 760, alignment: .center)
            .frame(maxWidth: .infinity)
        }
        .navigationTitle("Practice")
    }

    private var completionView: some View {
        VStack(alignment: .leading, spacing: 16) {
            Label("오늘 기록 완료", systemImage: "checkmark.circle.fill")
                .font(.title2)
                .fontWeight(.semibold)
                .foregroundStyle(.green)

            Text(viewModel.completionSummaryText)
                .foregroundStyle(.secondary)

            HStack {
                NavigationLink {
                    ReviewNoteView(
                        viewModel: ReviewNoteViewModel(
                            questions: viewModel.quiz.questions,
                            recordStore: viewModel.recordStore
                        )
                    )
                } label: {
                    Label("복습노트 보기", systemImage: "bookmark")
                }

                Button {
                    dismiss()
                } label: {
                    Label("홈으로 가기", systemImage: "house")
                }

                Button {
                    viewModel.restart()
                } label: {
                    Label("다시 풀기", systemImage: "arrow.clockwise")
                }
            }
            .buttonStyle(.bordered)
        }
        .padding()
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(.thinMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }
}

private struct QuestionCard: View {
    let question: Question

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                QuestionTypeBadge(type: question.questionType)
                Text(question.subject)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
            }

            Text(question.question)
                .font(.title3)
                .fontWeight(.semibold)

            Divider()

            VStack(alignment: .leading, spacing: 8) {
                Text("답변 순서")
                    .font(.headline)
                Text(question.answerGuide)
                    .font(.body)
            }

            VStack(alignment: .leading, spacing: 8) {
                Text("체크포인트")
                    .font(.headline)
                Text(question.methodGuide)
                    .font(.body)
            }

            VStack(alignment: .leading, spacing: 8) {
                Text("암기 포인트")
                    .font(.headline)
                Text(question.memoryTip)
                    .font(.body)
            }

            Text("\(question.section) · \(question.year.map(String.init) ?? "-")")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .padding()
        .background(.thinMaterial)
        .clipShape(RoundedRectangle(cornerRadius: 8))
    }
}
