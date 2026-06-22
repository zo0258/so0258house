import SwiftUI

struct ContentView: View {
    let appState: AppState
    let recordStore: StudyRecordStore

    var body: some View {
        TabView {
            NavigationStack {
                TodayView(
                    appState: appState,
                    recordStore: recordStore,
                    viewModel: TodayViewModel(
                        quiz: appState.quiz,
                        recordStore: recordStore
                    )
                )
            }
            .tabItem {
                Label("Today", systemImage: "sun.max")
            }

            NavigationStack {
                PracticeView(
                    viewModel: PracticeViewModel(
                        quiz: appState.quiz,
                        recordStore: recordStore
                    )
                )
            }
            .tabItem {
                Label("Practice", systemImage: "checklist")
            }

            NavigationStack {
                ReviewNoteView(
                    viewModel: ReviewNoteViewModel(
                        questions: appState.questions,
                        recordStore: recordStore
                    )
                )
            }
            .tabItem {
                Label("Review", systemImage: "bookmark")
            }

            NavigationStack {
                StatsView(
                    viewModel: StatsViewModel(
                        questions: appState.questions,
                        recordStore: recordStore
                    )
                )
            }
            .tabItem {
                Label("Stats", systemImage: "chart.bar")
            }
        }
    }
}

struct StatsView: View {
    @StateObject var viewModel: StatsViewModel

    var body: some View {
        List {
            Section("전체") {
                LabeledContent("전체 문제 수", value: "\(viewModel.totalCount)")
                LabeledContent("완료", value: "\(viewModel.doneCount)")
                LabeledContent("다시 보기", value: "\(viewModel.reviewCount)")
                LabeledContent("어려움", value: "\(viewModel.hardCount)")
                LabeledContent("미학습", value: "\(viewModel.unstudiedCount)")
                LabeledContent("최근 7일 기록", value: "\(viewModel.recentSevenDayCount)")
            }

            Section("과목별 진행률") {
                ForEach(viewModel.summaries) { summary in
                    VStack(alignment: .leading, spacing: 8) {
                        HStack {
                            Text(summary.subject)
                                .font(.headline)
                            Spacer()
                            Text("\(summary.studiedCount)/\(summary.totalCount)")
                                .font(.subheadline)
                                .foregroundStyle(.secondary)
                        }
                        ProgressView(value: summary.progress)
                        HStack(spacing: 12) {
                            Text("완료 \(summary.doneCount)")
                            Text("복습 \(summary.reviewCount)")
                            Text("어려움 \(summary.hardCount)")
                        }
                        .font(.caption)
                        .foregroundStyle(.secondary)
                    }
                    .padding(.vertical, 4)
                }
            }
        }
        .navigationTitle("통계")
        .onAppear {
            viewModel.refresh()
        }
    }
}
