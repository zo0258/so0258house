import SwiftUI

struct ReviewNoteView: View {
    @StateObject var viewModel: ReviewNoteViewModel

    var body: some View {
        List {
            Section {
                Picker("상태", selection: $viewModel.activeFilter) {
                    ForEach(ReviewFilter.allCases) { filter in
                        Text(filter.rawValue).tag(filter)
                    }
                }
                .pickerStyle(.segmented)

                Picker("과목", selection: $viewModel.subjectFilter) {
                    ForEach(SubjectFilter.allCases) { subject in
                        Text(subject.rawValue).tag(subject)
                    }
                }
            }

            Section("복습 대상") {
                if viewModel.filteredItems.isEmpty {
                    ContentUnavailableView(
                        "복습할 문제가 없습니다",
                        systemImage: "bookmark.slash",
                        description: Text("다시 보기 또는 어려움으로 표시한 문제가 여기에 표시됩니다.")
                    )
                } else {
                    ForEach(viewModel.filteredItems) { item in
                        ReviewNoteRow(item: item) {
                            viewModel.markDone(item)
                        }
                    }
                }
            }
        }
        .navigationTitle("복습노트")
        .searchable(text: $viewModel.searchText, prompt: "문제, 과목, section, 연도")
        .onAppear {
            viewModel.refresh()
        }
    }
}

private struct ReviewNoteRow: View {
    let item: ReviewNoteItem
    let markDone: () -> Void

    var body: some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                QuestionTypeBadge(type: item.question.questionType)
                Text(item.status.displayName)
                    .font(.caption)
                    .fontWeight(.semibold)
                    .foregroundStyle(item.status == .hard ? .red : .orange)
                Spacer()
                Button("완료로 변경", action: markDone)
                    .font(.caption)
                    .buttonStyle(.bordered)
            }
            Text(item.question.question)
                .font(.body)
            Text("\(item.question.subject) · \(item.question.section) · \(item.yearText)")
                .font(.caption)
                .foregroundStyle(.secondary)
        }
        .padding(.vertical, 4)
    }
}
