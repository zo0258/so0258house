import Foundation

struct DailyQuizSelector {
    private let calendar: Calendar

    init(calendar: Calendar = .current) {
        self.calendar = calendar
    }

    func select(from questions: [Question], for date: Date) -> DailyQuiz {
        let seed = dateSeed(date)
        let practical = questions.filter { $0.questionType == .practical }
        let oral = questions.filter { $0.questionType == .oral }
        let pools = [practical, oral, practical, oral]

        var selected: [Question] = []
        var used = Set<String>()

        for offset in pools.indices {
            if let item = pickDiverse(
                from: pools[offset],
                seed: seed + offset * 17,
                selected: selected,
                used: used
            ) {
                selected.append(item)
                used.insert(item.id)
            }
        }

        while selected.count < 4 {
            guard let fallback = pickFrom(questions, start: seed + selected.count, used: used) else {
                break
            }
            selected.append(fallback)
            used.insert(fallback.id)
        }

        return DailyQuiz(
            id: "\(dateKey(date))-practical-daily",
            date: date,
            questions: Array(selected.prefix(4))
        )
    }

    private func dateSeed(_ date: Date) -> Int {
        let parts = calendar.dateComponents([.year, .month, .day], from: date)
        return (parts.year ?? 0) * 10_000 + (parts.month ?? 0) * 100 + (parts.day ?? 0)
    }

    private func dateKey(_ date: Date) -> String {
        let formatter = DateFormatter()
        formatter.calendar = calendar
        formatter.locale = Locale(identifier: "en_US_POSIX")
        formatter.dateFormat = "yyyy-MM-dd"
        return formatter.string(from: date)
    }

    private func pickFrom(_ pool: [Question], start: Int, used: Set<String>) -> Question? {
        guard !pool.isEmpty else { return nil }
        for offset in 0..<pool.count {
            let item = pool[(start + offset) % pool.count]
            if !used.contains(item.id) {
                return item
            }
        }
        return pool[start % pool.count]
    }

    private func pickDiverse(
        from pool: [Question],
        seed: Int,
        selected: [Question],
        used: Set<String>
    ) -> Question? {
        let candidates = pool.filter { !used.contains($0.id) }
        guard !candidates.isEmpty else { return nil }

        let subjects = Set(selected.map(\.subject))
        let sections = Set(selected.map(\.section))

        return candidates.enumerated().min { left, right in
            score(left.element, index: left.offset, seed: seed, count: candidates.count, subjects: subjects, sections: sections)
                < score(right.element, index: right.offset, seed: seed, count: candidates.count, subjects: subjects, sections: sections)
        }?.element
    }

    private func score(
        _ question: Question,
        index: Int,
        seed: Int,
        count: Int,
        subjects: Set<String>,
        sections: Set<String>
    ) -> Double {
        let duplicateSubject = subjects.contains(question.subject) ? 10.0 : 0.0
        let duplicateSection = sections.contains(question.section) ? 4.0 : 0.0
        let rotation = Double((index - seed).positiveModulo(count)) / Double(max(count, 1))
        return duplicateSubject + duplicateSection + rotation
    }
}

private extension Int {
    func positiveModulo(_ divisor: Int) -> Int {
        guard divisor != 0 else { return 0 }
        let value = self % divisor
        return value >= 0 ? value : value + divisor
    }
}
