import XCTest
@testable import So02HousePractical

final class QuestionDataContractTests: XCTestCase {
    func testQuestionJSONLoadsExpectedCounts() throws {
        let repository = QuestionRepository(bundle: Bundle(for: Self.self))
        let questions = try repository.loadQuestions()

        XCTAssertEqual(questions.count, 199)
        XCTAssertEqual(questions.filter { $0.questionType == .practical }.count, 99)
        XCTAssertEqual(questions.filter { $0.questionType == .oral }.count, 100)
    }

    func testDailyQuizSelectsTwoPracticalAndTwoOralQuestions() throws {
        let repository = QuestionRepository(bundle: Bundle(for: Self.self))
        let questions = try repository.loadQuestions()
        let date = ISO8601DateFormatter().date(from: "2026-06-22T00:00:00Z")!

        let quiz = DailyQuizSelector().select(from: questions, for: date)

        XCTAssertEqual(quiz.questions.count, 4)
        XCTAssertEqual(quiz.questions.filter { $0.questionType == .practical }.count, 2)
        XCTAssertEqual(quiz.questions.filter { $0.questionType == .oral }.count, 2)
        XCTAssertGreaterThanOrEqual(Set(quiz.questions.map(\.subject)).count, 2)
        XCTAssertGreaterThanOrEqual(Set(quiz.questions.map(\.section)).count, 3)
    }

    func testDailyQuizSelectsSameQuestionsForSameDate() throws {
        let repository = QuestionRepository(bundle: Bundle(for: Self.self))
        let questions = try repository.loadQuestions()
        let date = ISO8601DateFormatter().date(from: "2026-06-22T00:00:00Z")!
        let selector = DailyQuizSelector()

        let first = selector.select(from: questions, for: date)
        let second = selector.select(from: questions, for: date)

        XCTAssertEqual(first.questions.map(\.id), second.questions.map(\.id))
    }

    func testStudyRecordStoreSavesAndRestoresRecords() throws {
        let suiteName = "StudyRecordStoreTests.\(UUID().uuidString)"
        let defaults = try XCTUnwrap(UserDefaults(suiteName: suiteName))
        defer {
            defaults.removePersistentDomain(forName: suiteName)
        }
        let updatedAt = ISO8601DateFormatter().date(from: "2026-06-22T09:00:00Z")!
        let quizDate = ISO8601DateFormatter().date(from: "2026-06-22T00:00:00Z")!
        let store = StudyRecordStore(defaults: defaults, key: "records", now: { updatedAt })

        store.record(questionId: "q-1", status: .review, date: quizDate)
        let restored = StudyRecordStore(defaults: defaults, key: "records").load()

        XCTAssertEqual(restored["q-1"]?.questionId, "q-1")
        XCTAssertEqual(restored["q-1"]?.status, .review)
        XCTAssertEqual(restored["q-1"]?.date, quizDate)
        XCTAssertEqual(restored["q-1"]?.updatedAt, updatedAt)
    }

    func testStudyRecordStoreOverwritesExistingStatus() throws {
        let suiteName = "StudyRecordStoreTests.\(UUID().uuidString)"
        let defaults = try XCTUnwrap(UserDefaults(suiteName: suiteName))
        defer {
            defaults.removePersistentDomain(forName: suiteName)
        }
        let quizDate = ISO8601DateFormatter().date(from: "2026-06-22T00:00:00Z")!
        let store = StudyRecordStore(defaults: defaults, key: "records")

        store.record(questionId: "q-1", status: .review, date: quizDate)
        store.record(questionId: "q-1", status: .hard, date: quizDate)
        let records = store.load()

        XCTAssertEqual(records.count, 1)
        XCTAssertEqual(records["q-1"]?.status, .hard)
    }

    func testStudyRecordStoreReviewCandidatesOnlyReturnsReviewAndHard() throws {
        let suiteName = "StudyRecordStoreTests.\(UUID().uuidString)"
        let defaults = try XCTUnwrap(UserDefaults(suiteName: suiteName))
        defer {
            defaults.removePersistentDomain(forName: suiteName)
        }
        let quizDate = ISO8601DateFormatter().date(from: "2026-06-22T00:00:00Z")!
        let store = StudyRecordStore(defaults: defaults, key: "records")

        store.record(questionId: "done", status: .done, date: quizDate)
        store.record(questionId: "review", status: .review, date: quizDate)
        store.record(questionId: "hard", status: .hard, date: quizDate)

        XCTAssertEqual(Set(store.reviewCandidates().map(\.questionId)), ["review", "hard"])
    }

    @MainActor
    func testPracticeViewModelRecordsSelectionAndCompletesQuiz() throws {
        let suiteName = "PracticeViewModelTests.\(UUID().uuidString)"
        let defaults = try XCTUnwrap(UserDefaults(suiteName: suiteName))
        defer {
            defaults.removePersistentDomain(forName: suiteName)
        }
        let repository = QuestionRepository(bundle: Bundle(for: Self.self))
        let questions = try repository.loadQuestions()
        let date = ISO8601DateFormatter().date(from: "2026-06-22T00:00:00Z")!
        let quiz = DailyQuizSelector().select(from: questions, for: date)
        let store = StudyRecordStore(defaults: defaults, key: "records")
        let viewModel = PracticeViewModel(quiz: quiz, recordStore: store)

        viewModel.mark(.done)
        XCTAssertEqual(viewModel.recordedCount, 1)
        XCTAssertEqual(store.record(for: quiz.questions[0].id)?.status, .done)

        viewModel.mark(.review)
        viewModel.mark(.hard)
        viewModel.mark(.done)

        XCTAssertTrue(viewModel.isComplete)
        XCTAssertEqual(viewModel.recordedCount, 4)
    }
}
