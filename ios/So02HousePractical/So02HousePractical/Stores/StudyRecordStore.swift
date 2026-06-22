import Foundation

final class StudyRecordStore {
    private let defaults: UserDefaults
    private let key: String
    private let now: () -> Date

    init(
        defaults: UserDefaults = .standard,
        key: String = "health-exercise-practical-records",
        now: @escaping () -> Date = Date.init
    ) {
        self.defaults = defaults
        self.key = key
        self.now = now
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

    func record(questionId: String, status: ReviewStatus, date: Date) {
        var records = load()
        records[questionId] = StudyRecord(
            questionId: questionId,
            status: status,
            date: date,
            updatedAt: now()
        )
        save(records)
    }

    func records(for quiz: DailyQuiz) -> [StudyRecord] {
        let records = load()
        return quiz.questions.compactMap { records[$0.id] }
    }

    func record(for questionId: String) -> StudyRecord? {
        load()[questionId]
    }

    func reviewCandidates() -> [StudyRecord] {
        load().values
            .filter { $0.status == .review || $0.status == .hard }
            .sorted { $0.updatedAt > $1.updatedAt }
    }

    func reset() {
        defaults.removeObject(forKey: key)
    }
}
