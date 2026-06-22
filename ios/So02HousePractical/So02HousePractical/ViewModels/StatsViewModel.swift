import Foundation

@MainActor
final class StatsViewModel: ObservableObject {
    @Published private(set) var summaries: [SubjectSummary] = []
    @Published private(set) var totalCount: Int = 0
    @Published private(set) var doneCount: Int = 0
    @Published private(set) var reviewCount: Int = 0
    @Published private(set) var hardCount: Int = 0
    @Published private(set) var recentSevenDayCount: Int = 0

    private let questions: [Question]
    private let recordStore: StudyRecordStore

    var studiedCount: Int {
        doneCount + reviewCount + hardCount
    }

    var unstudiedCount: Int {
        max(totalCount - studiedCount, 0)
    }

    init(questions: [Question], recordStore: StudyRecordStore) {
        self.questions = questions
        self.recordStore = recordStore
        refresh()
    }

    func refresh() {
        let records = recordStore.load()
        let questionIds = Set(questions.map(\.id))
        let validRecords = records.values.filter { questionIds.contains($0.questionId) }
        let grouped = Dictionary(grouping: questions, by: \.subject)

        totalCount = questions.count
        doneCount = validRecords.filter { $0.status == .done }.count
        reviewCount = validRecords.filter { $0.status == .review }.count
        hardCount = validRecords.filter { $0.status == .hard }.count
        recentSevenDayCount = validRecords.filter { record in
            Calendar.current.dateComponents([.day], from: record.updatedAt, to: Date()).day.map { $0 < 7 } ?? false
        }.count

        summaries = grouped.map { subject, subjectQuestions in
            let ids = Set(subjectQuestions.map(\.id))
            let subjectRecords = validRecords.filter { ids.contains($0.questionId) }
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
