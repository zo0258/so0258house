import Foundation

enum ReviewFilter: String, CaseIterable, Identifiable {
    case all = "전체"
    case review = "다시 보기"
    case hard = "어려움"

    var id: String { rawValue }
}

enum SubjectFilter: String, CaseIterable, Identifiable {
    case all = "전체"
    case healthMeasurement = "건강·체력측정평가"
    case trainingMethod = "트레이닝방법론"
    case injuryRehab = "운동손상평가 및 재활"

    var id: String { rawValue }
}

@MainActor
final class ReviewNoteViewModel: ObservableObject {
    @Published var activeFilter: ReviewFilter = .all
    @Published var subjectFilter: SubjectFilter = .all
    @Published var searchText: String = ""
    @Published private(set) var items: [ReviewNoteItem] = []

    private let questions: [Question]
    private let recordStore: StudyRecordStore

    init(questions: [Question], recordStore: StudyRecordStore) {
        self.questions = questions
        self.recordStore = recordStore
        refresh()
    }

    var filteredItems: [ReviewNoteItem] {
        let statusFiltered: [ReviewNoteItem]
        switch activeFilter {
        case .all:
            statusFiltered = items
        case .review:
            statusFiltered = items.filter { $0.status == .review }
        case .hard:
            statusFiltered = items.filter { $0.status == .hard }
        }

        let subjectFiltered = statusFiltered.filter { item in
            subjectFilter == .all || item.question.subject == subjectFilter.rawValue
        }

        let query = searchText.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !query.isEmpty else {
            return subjectFiltered
        }

        return subjectFiltered.filter { item in
            item.question.question.localizedCaseInsensitiveContains(query)
                || item.question.subject.localizedCaseInsensitiveContains(query)
                || item.question.section.localizedCaseInsensitiveContains(query)
                || item.yearText.localizedCaseInsensitiveContains(query)
        }
    }

    func refresh() {
        let byID = Dictionary(uniqueKeysWithValues: questions.map { ($0.id, $0) })
        items = recordStore.reviewCandidates().compactMap { record in
            guard let question = byID[record.questionId] else {
                return nil
            }
            return ReviewNoteItem(question: question, status: record.status, updatedAt: record.updatedAt)
        }
        .sorted { $0.updatedAt > $1.updatedAt }
    }

    func markDone(_ item: ReviewNoteItem) {
        recordStore.record(questionId: item.question.id, status: .done, date: Date())
        refresh()
    }
}

struct ReviewNoteItem: Identifiable, Hashable {
    var id: String { question.id }
    let question: Question
    let status: ReviewStatus
    let updatedAt: Date

    var yearText: String {
        question.year.map(String.init) ?? "-"
    }
}
