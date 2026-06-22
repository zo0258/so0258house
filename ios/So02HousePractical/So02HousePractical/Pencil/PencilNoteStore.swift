import Foundation
#if canImport(PencilKit)
import PencilKit
#endif

enum PencilNoteStoreError: Error {
    case documentsDirectoryMissing
}

final class PencilNoteStore {
    private let fileManager: FileManager
    private let folderName: String

    init(fileManager: FileManager = .default, folderName: String = "PencilNotes") {
        self.fileManager = fileManager
        self.folderName = folderName
    }

    func noteURL(for questionID: String) throws -> URL {
        let directory = try notesDirectory()
        return directory.appendingPathComponent("\(questionID).drawing")
    }

    func hasNote(for questionID: String) -> Bool {
        guard let url = try? noteURL(for: questionID) else {
            return false
        }
        return fileManager.fileExists(atPath: url.path)
    }

    #if canImport(PencilKit)
    func loadDrawing(for questionID: String) throws -> PKDrawing {
        let url = try noteURL(for: questionID)
        guard fileManager.fileExists(atPath: url.path) else {
            return PKDrawing()
        }
        let data = try Data(contentsOf: url)
        return try PKDrawing(data: data)
    }

    func saveDrawing(_ drawing: PKDrawing, for questionID: String) throws {
        let url = try noteURL(for: questionID)
        let data = drawing.dataRepresentation()
        try data.write(to: url, options: [.atomic])
    }
    #endif

    private func notesDirectory() throws -> URL {
        guard let documents = fileManager.urls(for: .documentDirectory, in: .userDomainMask).first else {
            throw PencilNoteStoreError.documentsDirectoryMissing
        }
        let directory = documents.appendingPathComponent(folderName, isDirectory: true)
        if !fileManager.fileExists(atPath: directory.path) {
            try fileManager.createDirectory(at: directory, withIntermediateDirectories: true)
        }
        return directory
    }
}
