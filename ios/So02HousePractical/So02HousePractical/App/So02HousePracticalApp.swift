import SwiftUI

@main
struct So02HousePracticalApp: App {
    private let recordStore = StudyRecordStore()
    private let appState: AppState

    init() {
        let repository = QuestionRepository()
        let questions = (try? repository.loadQuestions()) ?? []
        let quiz = DailyQuizSelector().select(from: questions, for: Date())
        appState = AppState(questions: questions, quiz: quiz)
    }

    var body: some Scene {
        WindowGroup {
            ContentView(appState: appState, recordStore: recordStore)
        }
    }
}

struct AppState {
    let questions: [Question]
    let quiz: DailyQuiz

    var practicalCount: Int {
        questions.filter { $0.questionType == .practical }.count
    }

    var oralCount: Int {
        questions.filter { $0.questionType == .oral }.count
    }
}
