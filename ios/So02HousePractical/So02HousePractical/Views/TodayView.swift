import SwiftUI

struct TodayView: View {
    let appState: AppState
    let recordStore: StudyRecordStore
    @StateObject var viewModel: TodayViewModel

    var body: some View {
        List {
            Section {
                NavigationLink {
                    PracticeView(
                        viewModel: PracticeViewModel(
                            quiz: appState.quiz,
                            recordStore: recordStore
                        )
                    )
                } label: {
                    HStack {
                        VStack(alignment: .leading, spacing: 4) {
                            Text(viewModel.startButtonTitle)
                                .font(.headline)
                            Text(viewModel.completedText)
                                .font(.subheadline)
                                .foregroundStyle(.secondary)
                        }
                        Spacer()
                        Image(systemName: "play.circle.fill")
                            .font(.title2)
                    }
                }
            }

            Section("오늘 현황") {
                LabeledContent("완료", value: "\(viewModel.doneCount)")
                LabeledContent("다시 보기", value: "\(viewModel.reviewCount)")
                LabeledContent("어려움", value: "\(viewModel.hardCount)")
                LabeledContent("오늘 구성", value: viewModel.typeSummary)
            }

            Section("전체 데이터") {
                LabeledContent("전체 문제", value: "\(appState.questions.count)")
                LabeledContent("실기", value: "\(appState.practicalCount)")
                LabeledContent("구술", value: "\(appState.oralCount)")
            }

            Section("오늘의 4문제") {
                ForEach(appState.quiz.questions) { question in
                    TodayQuestionRow(
                        question: question,
                        status: viewModel.status(for: question)
                    )
                }
            }
        }
        .navigationTitle("오늘 학습")
        .onAppear {
            viewModel.refresh()
        }
    }
}

private struct TodayQuestionRow: View {
    let question: Question
    let status: ReviewStatus?

    var body: some View {
        VStack(alignment: .leading, spacing: 6) {
            HStack {
                QuestionTypeBadge(type: question.questionType)
                Text(question.subject)
                    .font(.caption)
                    .foregroundStyle(.secondary)
                Spacer()
                if let status {
                    Text(status.displayName)
                        .font(.caption)
                        .fontWeight(.semibold)
                        .foregroundStyle(statusColor)
                }
            }
            Text(question.question)
                .font(.body)
                .lineLimit(3)
            Text("\(question.section) · \(question.year.map(String.init) ?? "-")")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .padding(.vertical, 4)
    }

    private var statusColor: Color {
        switch status {
        case .done:
            .green
        case .review:
            .orange
        case .hard:
            .red
        case nil:
            .secondary
        }
    }
}
