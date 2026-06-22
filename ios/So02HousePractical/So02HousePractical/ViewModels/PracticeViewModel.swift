import Foundation

@MainActor
final class PracticeViewModel: ObservableObject {
    @Published private(set) var quiz: DailyQuiz
    @Published private(set) var currentIndex: Int = 0
    @Published private(set) var recordedCount: Int = 0
    @Published private(set) var isComplete: Bool = false

    let recordStore: StudyRecordStore

    init(quiz: DailyQuiz, recordStore: StudyRecordStore) {
        self.quiz = quiz
        self.recordStore = recordStore
        refreshProgress()
        currentIndex = firstUnrecordedIndex()
        isComplete = recordedCount == quiz.questionCount && quiz.questionCount > 0
    }

    var currentQuestion: Question? {
        guard quiz.questions.indices.contains(currentIndex), !isComplete else {
            return nil
        }
        return quiz.questions[currentIndex]
    }

    var progressText: String {
        isComplete ? "완료" : "\(min(currentIndex + 1, quiz.questionCount))/\(quiz.questionCount) 문제"
    }

    var recordText: String {
        "기록 \(recordedCount)/\(quiz.questionCount)"
    }

    var completionSummaryText: String {
        "오늘 4문제 기록을 저장했습니다."
    }

    func mark(_ status: ReviewStatus) {
        guard let question = currentQuestion else {
            return
        }

        recordStore.record(questionId: question.id, status: status, date: quiz.date)
        refreshProgress()

        if currentIndex >= quiz.questions.count - 1 {
            isComplete = true
        } else {
            currentIndex += 1
        }
    }

    func restart() {
        currentIndex = 0
        isComplete = false
        refreshProgress()
    }

    private func refreshProgress() {
        recordedCount = recordStore.records(for: quiz).count
    }

    private func firstUnrecordedIndex() -> Int {
        let recordedIds = Set(recordStore.records(for: quiz).map(\.questionId))
        return quiz.questions.firstIndex { !recordedIds.contains($0.id) } ?? 0
    }
}
