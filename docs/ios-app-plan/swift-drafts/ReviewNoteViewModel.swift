import Foundation

enum ReviewFilter: String, CaseIterable, Identifiable {
    case all = "전체"
    case review = "다시 보기"
    case hard = "어려움"

    var id: String { rawValue }
}

@MainActor
final class ReviewNoteViewModel: ObservableObject {
    @Published var activeFilter: ReviewFilter = .all
    @Published private(set) var items: [ReviewNoteItem] = []

    private let questions: [Question]
    private let recordStore: StudyRecordStore

    init(questions: [Question], recordStore: StudyRecordStore) {
        self.questions = questions
        self.recordStore = recordStore
        refresh()
    }

    var filteredItems: [ReviewNoteItem] {
        switch activeFilter {
        case .all:
            return items
        case .review:
            return items.filter { $0.status == .review }
        case .hard:
            return items.filter { $0.status == .hard }
        }
    }

    func refresh() {
        let byID = Dictionary(uniqueKeysWithValues: questions.map { ($0.id, $0) })
        items = recordStore.load().values.compactMap { record in
            guard record.status == .review || record.status == .hard,
                  let question = byID[record.questionID] else {
                return nil
            }
            return ReviewNoteItem(question: question, status: record.status, updatedAt: record.updatedAt)
        }
        .sorted { $0.updatedAt > $1.updatedAt }
    }
}

struct ReviewNoteItem: Identifiable, Hashable {
    var id: String { question.id }
    let question: Question
    let status: ReviewStatus
    let updatedAt: Date
}
