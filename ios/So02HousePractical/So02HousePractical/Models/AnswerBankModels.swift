import Foundation

enum AnswerStatus: String, Codable, CaseIterable, Identifiable {
    case draft
    case verified
    case needsReview = "needs_review"

    var id: String { rawValue }
}

enum AnswerSourceType: String, Codable {
    case official
    case academic
    case textbook
    case trustedWeb = "trusted_web"
    case tierSInternal = "tier_s_internal"
    case `internal`
}

struct AnswerSourceRef: Codable, Hashable {
    let title: String
    let url: String
    let type: AnswerSourceType
    let checkedAt: String
    let page: Int?
}

struct AnswerBankEntry: Identifiable, Codable, Hashable {
    var id: String { questionId }

    let questionId: String
    let answerStatus: AnswerStatus
    let modelAnswer: String
    let performanceSteps: [String]
    let oralAnswerStructure: [String]
    let keyPoints: [String]
    let commonMistakes: [String]
    let memoryTip: String
    let sourceRefs: [AnswerSourceRef]
    let sourceVerified: Bool
    let needsReview: Bool
    let reviewNotes: [String]
}
