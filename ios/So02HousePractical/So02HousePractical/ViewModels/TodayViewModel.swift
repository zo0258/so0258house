import Foundation

@MainActor
final class TodayViewModel: ObservableObject {
    @Published private(set) var quiz: DailyQuiz
    @Published private(set) var todayRecords: [StudyRecord] = []
    @Published private(set) var recordsByQuestionId: [String: StudyRecord] = [:]

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

    var doneCount: Int {
        todayRecords.filter { $0.status == .done }.count
    }

    var startButtonTitle: String {
        todayRecords.isEmpty ? "오늘 학습 시작" : "이어하기"
    }

    var typeSummary: String {
        let practical = quiz.questions.filter { $0.questionType == .practical }.count
        let oral = quiz.questions.filter { $0.questionType == .oral }.count
        return "실기 \(practical) · 구술 \(oral)"
    }

    func refresh() {
        todayRecords = recordStore.records(for: quiz)
        recordsByQuestionId = Dictionary(uniqueKeysWithValues: todayRecords.map { ($0.questionId, $0) })
    }

    func status(for question: Question) -> ReviewStatus? {
        recordsByQuestionId[question.id]?.status
    }
}
