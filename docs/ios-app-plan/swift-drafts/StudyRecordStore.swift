import Foundation

final class StudyRecordStore {
    private let defaults: UserDefaults
    private let key: String

    init(defaults: UserDefaults = .standard, key: String = "health-exercise-practical-records") {
        self.defaults = defaults
        self.key = key
    }

    func load() -> [String: StudyRecord] {
        guard let data = defaults.data(forKey: key) else {
            return [:]
        }
        return (try? JSONDecoder().decode([String: StudyRecord].self, from: data)) ?? [:]
    }

    func save(_ records: [String: StudyRecord]) {
        guard let data = try? JSONEncoder().encode(records) else {
            return
        }
        defaults.set(data, forKey: key)
    }

    func record(questionID: String, status: ReviewStatus, quizDate: Date) {
        var records = load()
        records[questionID] = StudyRecord(
            questionID: questionID,
            status: status,
            quizDate: quizDate,
            updatedAt: Date()
        )
        save(records)
    }

    func records(for quiz: DailyQuiz) -> [StudyRecord] {
        let records = load()
        let ids = Set(quiz.questions.map(\.id))
        return records.values.filter { ids.contains($0.questionID) }
    }

    func reset() {
        defaults.removeObject(forKey: key)
    }
}
