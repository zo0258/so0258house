import Foundation

enum AnswerBankRepositoryError: Error {
    case missingResource(String)
}

final class AnswerBankRepository {
    private let bundle: Bundle
    private let resourceName: String

    init(bundle: Bundle = .main, resourceName: String = "practical-answer-bank") {
        self.bundle = bundle
        self.resourceName = resourceName
    }

    func loadEntries() throws -> [AnswerBankEntry] {
        guard let url = bundle.url(forResource: resourceName, withExtension: "json") else {
            throw AnswerBankRepositoryError.missingResource("\(resourceName).json")
        }

        let data = try Data(contentsOf: url)
        return try JSONDecoder().decode([AnswerBankEntry].self, from: data)
    }

    func loadByQuestionId() throws -> [String: AnswerBankEntry] {
        Dictionary(uniqueKeysWithValues: try loadEntries().map { ($0.questionId, $0) })
    }
}
