#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
PLAN = ROOT / "docs" / "ios-app-plan"
DATA = ROOT / "data" / "practical-questions.json"

REQUIRED_DOCS = [f"{index:02d}" for index in range(1, 16)]
REQUIRED_SWIFT = {
    "QuestionModels.swift": ["struct Question", "enum QuestionType", "enum ReviewStatus"],
    "QuestionRepository.swift": ["final class QuestionRepository", "loadQuestions()"],
    "DailyQuizSelector.swift": ["struct DailyQuizSelector", "pickDiverse", "positiveModulo"],
    "StudyRecordStore.swift": ["final class StudyRecordStore", "UserDefaults"],
    "PracticeViewModel.swift": ["final class PracticeViewModel", "func mark"],
    "PencilNoteStore.swift": ["final class PencilNoteStore", "PKDrawing"],
    "KeyboardShortcutPlan.swift": ["enum AppShortcut", "keyboardShortcut"],
    "TodayViewModel.swift": ["final class TodayViewModel", "completedText"],
    "ReviewNoteViewModel.swift": ["final class ReviewNoteViewModel", "ReviewFilter"],
    "StatsViewModel.swift": ["final class StatsViewModel", "SubjectSummary"],
    "QuestionDataContractTests.swift": ["XCTest", "testQuestionJSONLoadsExpectedCounts"],
}


def fail(message: str) -> None:
    raise AssertionError(message)


def check_docs() -> None:
    docs = {path.name[:2]: path for path in PLAN.glob("*.md")}
    for prefix in REQUIRED_DOCS:
        if prefix not in docs:
            fail(f"missing doc prefix {prefix}")
        text = docs[prefix].read_text(encoding="utf-8")
        if not text.startswith("# "):
            fail(f"{docs[prefix].name} must start with h1")
        if text.rstrip().splitlines()[-1] != "끝.":
            fail(f"{docs[prefix].name} must end with 끝.")
        if "TBD" in text or "TODO" in text:
            fail(f"{docs[prefix].name} contains placeholder")


def check_data_contract() -> None:
    questions = json.loads(DATA.read_text(encoding="utf-8"))
    if len(questions) != 199:
        fail(f"unexpected question count: {len(questions)}")
    required = {
        "id", "subject", "section", "type", "year", "question", "methodGuide",
        "memoryTip", "answerGuide", "sourceRefs", "sourceVerified", "needsReview",
    }
    ids = set()
    for item in questions:
        missing = required - set(item)
        if missing:
            fail(f"{item.get('id')} missing keys: {sorted(missing)}")
        if item["id"] in ids:
            fail(f"duplicate id: {item['id']}")
        ids.add(item["id"])
        if item["type"] not in {"실기", "구술", "공통"}:
            fail(f"unexpected type: {item['type']}")
        if not item["question"].strip():
            fail(f"empty question: {item['id']}")
    counts = Counter(item["type"] for item in questions)
    if counts["실기"] != 99 or counts["구술"] != 100:
        fail(f"unexpected type counts: {counts}")


def check_swift_drafts() -> None:
    swift_dir = PLAN / "swift-drafts"
    for name, needles in REQUIRED_SWIFT.items():
        path = swift_dir / name
        if not path.exists():
            fail(f"missing swift draft: {name}")
        text = path.read_text(encoding="utf-8")
        for needle in needles:
            if needle not in text:
                fail(f"{name} missing {needle}")
        if re.search(r"\bTODO\b|\bFIXME\b|fatalError\(", text):
            fail(f"{name} contains unfinished marker")
    question_models = (swift_dir / "QuestionModels.swift").read_text(encoding="utf-8")
    for value in ("실기", "구술", "공통"):
        if value not in question_models:
            fail(f"QuestionModels.swift missing Korean raw value {value}")


def main() -> None:
    check_docs()
    check_data_contract()
    check_swift_drafts()
    print("ios plan validation passed")


if __name__ == "__main__":
    main()
