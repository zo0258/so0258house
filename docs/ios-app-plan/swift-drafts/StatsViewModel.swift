import Foundation

@MainActor
final class StatsViewModel: ObservableObject {
    @Published private(set) var summaries: [SubjectSummary] = []

    private let questions: [Question]
    private let recordStore: StudyRecordStore

    init(questions: [Question], recordStore: StudyRecordStore) {
        self.questions = questions
        self.recordStore = recordStore
        refresh()
    }

    func refresh() {
        let records = recordStore.load()
        let grouped = Dictionary(grouping: questions, by: \.subject)

        summaries = grouped.map { subject, subjectQuestions in
            let ids = Set(subjectQuestions.map(\.id))
            let subjectRecords = records.values.filter { ids.contains($0.questionID) }
            return SubjectSummary(
                subject: subject,
                totalCount: subjectQuestions.count,
                doneCount: subjectRecords.filter { $0.status == .done }.count,
                reviewCount: subjectRecords.filter { $0.status == .review }.count,
                hardCount: subjectRecords.filter { $0.status == .hard }.count,
                practicalCount: subjectQuestions.filter { $0.questionType == .practical }.count,
                oralCount: subjectQuestions.filter { $0.questionType == .oral }.count
            )
        }
        .sorted { $0.subject < $1.subject }
    }
}
