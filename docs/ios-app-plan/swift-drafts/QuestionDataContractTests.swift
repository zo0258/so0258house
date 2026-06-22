import XCTest
@testable import So02HousePractical

final class QuestionDataContractTests: XCTestCase {
    func testQuestionJSONLoadsExpectedCounts() throws {
        let repository = QuestionRepository()
        let questions = try repository.loadQuestions()

        XCTAssertEqual(questions.count, 199)
        XCTAssertEqual(questions.filter { $0.questionType == .practical }.count, 99)
        XCTAssertEqual(questions.filter { $0.questionType == .oral }.count, 100)
    }

    func testDailyQuizSelectsTwoPracticalAndTwoOralQuestions() throws {
        let repository = QuestionRepository()
        let questions = try repository.loadQuestions()
        let date = ISO8601DateFormatter().date(from: "2026-06-22T00:00:00Z")!

        let quiz = DailyQuizSelector().select(from: questions, for: date)

        XCTAssertEqual(quiz.questions.count, 4)
        XCTAssertEqual(quiz.questions.filter { $0.questionType == .practical }.count, 2)
        XCTAssertEqual(quiz.questions.filter { $0.questionType == .oral }.count, 2)
        XCTAssertGreaterThanOrEqual(Set(quiz.questions.map(\.subject)).count, 2)
        XCTAssertGreaterThanOrEqual(Set(quiz.questions.map(\.section)).count, 3)
    }
}
