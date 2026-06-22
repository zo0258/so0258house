import Foundation

@MainActor
final class PracticeViewModel: ObservableObject {
    @Published private(set) var quiz: DailyQuiz
    @Published private(set) var currentIndex: Int = 0
    @Published private(set) var recordedCount: Int = 0
    @Published private(set) var isComplete: Bool = false

    private let recordStore: StudyRecordStore

    init(quiz: DailyQuiz, recordStore: StudyRecordStore) {
        self.quiz = quiz
        self.recordStore = recordStore
        self.recordedCount = recordStore.records(for: quiz).count
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

    func mark(_ status: ReviewStatus) {
        guard let question = currentQuestion else {
            return
        }

        recordStore.record(questionID: question.id, status: status, quizDate: quiz.date)
        recordedCount = min(recordedCount + 1, quiz.questionCount)

        if currentIndex >= quiz.questions.count - 1 {
            isComplete = true
        } else {
            currentIndex += 1
        }
    }
}
