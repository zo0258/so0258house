import Foundation

enum QuestionType: String, Codable, CaseIterable, Identifiable {
    case practical = "실기"
    case oral = "구술"
    case common = "공통"

    var id: String { rawValue }
}

enum ReviewStatus: String, Codable, CaseIterable, Identifiable {
    case done
    case review
    case hard

    var id: String { rawValue }

    var displayName: String {
        switch self {
        case .done:
            return "완료"
        case .review:
            return "다시 보기"
        case .hard:
            return "어려움"
        }
    }
}

struct SourceRef: Codable, Hashable {
    let title: String
    let url: String
}

struct Question: Identifiable, Codable, Hashable {
    let id: String
    let subject: String
    let section: String
    let type: String
    let year: Int?
    let question: String
    let methodGuide: String
    let memoryTip: String
    let answerGuide: String
    let sourceRefs: [SourceRef]
    let sourceVerified: Bool
    let needsReview: Bool
    let reviewReasons: [String]?

    var questionType: QuestionType {
        QuestionType(rawValue: type) ?? .common
    }
}

struct DailyQuiz: Identifiable, Codable, Hashable {
    let id: String
    let date: Date
    let questions: [Question]

    var questionCount: Int { questions.count }
}

struct StudyRecord: Identifiable, Codable, Hashable {
    var id: String { questionId }
    let questionId: String
    var status: ReviewStatus
    var date: Date
    var updatedAt: Date

    enum CodingKeys: String, CodingKey {
        case questionId
        case legacyQuestionID = "questionID"
        case status
        case date
        case legacyQuizDate = "quizDate"
        case updatedAt
    }

    init(questionId: String, status: ReviewStatus, date: Date, updatedAt: Date) {
        self.questionId = questionId
        self.status = status
        self.date = date
        self.updatedAt = updatedAt
    }

    init(from decoder: Decoder) throws {
        let container = try decoder.container(keyedBy: CodingKeys.self)
        questionId = try container.decodeIfPresent(String.self, forKey: .questionId)
            ?? container.decode(String.self, forKey: .legacyQuestionID)
        status = try container.decode(ReviewStatus.self, forKey: .status)
        date = try container.decodeIfPresent(Date.self, forKey: .date)
            ?? container.decode(Date.self, forKey: .legacyQuizDate)
        updatedAt = try container.decode(Date.self, forKey: .updatedAt)
    }

    func encode(to encoder: Encoder) throws {
        var container = encoder.container(keyedBy: CodingKeys.self)
        try container.encode(questionId, forKey: .questionId)
        try container.encode(status, forKey: .status)
        try container.encode(date, forKey: .date)
        try container.encode(updatedAt, forKey: .updatedAt)
    }
}

struct PencilNote: Identifiable, Codable, Hashable {
    var id: String { questionID }
    let questionID: String
    var fileName: String
    var updatedAt: Date
}

struct SubjectSummary: Identifiable, Hashable {
    var id: String { subject }
    let subject: String
    let totalCount: Int
    let doneCount: Int
    let reviewCount: Int
    let hardCount: Int
    let practicalCount: Int
    let oralCount: Int

    var studiedCount: Int {
        doneCount + reviewCount + hardCount
    }

    var progress: Double {
        guard totalCount > 0 else { return 0 }
        return Double(studiedCount) / Double(totalCount)
    }
}
