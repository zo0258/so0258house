import Foundation

enum QuestionRepositoryError: Error {
    case missingResource(String)
}

final class QuestionRepository {
    private let bundle: Bundle
    private let resourceName: String

    init(bundle: Bundle = .main, resourceName: String = "practical-questions") {
        self.bundle = bundle
        self.resourceName = resourceName
    }

    func loadQuestions() throws -> [Question] {
        guard let url = bundle.url(forResource: resourceName, withExtension: "json") else {
            throw QuestionRepositoryError.missingResource("\(resourceName).json")
        }

        let data = try Data(contentsOf: url)
        let decoder = JSONDecoder()
        return try decoder.decode([Question].self, from: data)
    }
}
