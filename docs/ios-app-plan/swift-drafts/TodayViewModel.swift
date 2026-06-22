import Foundation

@MainActor
final class TodayViewModel: ObservableObject {
    @Published private(set) var quiz: DailyQuiz
    @Published private(set) var todayRecords: [StudyRecord] = []

    private let recordStore: StudyRecordStore

    init(quiz: DailyQuiz, recordStore: StudyRecordStore) {
        self.quiz = quiz
        self.recordStore = recordStore
        refresh()
    }

    var completedText: String {
        "오늘 완료 \(todayRecords.count)/\(quiz.questionCount)"
    }

    var reviewCount: Int {
        todayRecords.filter { $0.status == .review }.count
    }

    var hardCount: Int {
        todayRecords.filter { $0.status == .hard }.count
    }

    var typeSummary: String {
        let practical = quiz.questions.filter { $0.questionType == .practical }.count
        let oral = quiz.questions.filter { $0.questionType == .oral }.count
        return "실기 \(practical) · 구술 \(oral)"
    }

    func refresh() {
        todayRecords = recordStore.records(for: quiz)
    }
}
