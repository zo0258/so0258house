import Foundation

enum QuestionType: String, Codable, CaseIterable, Identifiable {
    case practical = "실기"
    case oral = "구술"
    case common = "공통"

    var id: String { rawValue }
}

enum ReviewStatus: String, Codable, CaseIterable, Identifiable {
    case none
    case done
    case review
    case hard

    var id: String { rawValue }
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
    var id: String { questionID }
    let questionID: String
    var status: ReviewStatus
    var quizDate: Date
    var updatedAt: Date
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
}
