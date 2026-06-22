#!/usr/bin/env python3
import json
import hashlib
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_PATH = ROOT / "data" / "practical-questions.json"
ANSWER_BANK_PATH = ROOT / "data" / "practical-answer-bank.json"
IOS_ANSWER_BANK_PATH = (
    ROOT
    / "ios"
    / "So02HousePractical"
    / "So02HousePractical"
    / "Resources"
    / "practical-answer-bank.json"
)
ALLOWED_STATUSES = {"draft", "verified", "needs_review"}
ALLOWED_SOURCE_TYPES = {"official", "academic", "textbook", "trusted_web", "internal"}


def load_json(path):
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def fail(errors):
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    raise SystemExit(1)


def main():
    questions = load_json(QUESTIONS_PATH)
    answer_bank = load_json(ANSWER_BANK_PATH)
    ios_answer_bank = load_json(IOS_ANSWER_BANK_PATH)
    errors = []

    question_ids = {question["id"] for question in questions}
    year_2025_ids = {question["id"] for question in questions if question.get("year") == 2025}
    bank_ids = [entry.get("questionId") for entry in answer_bank]
    bank_id_set = set(bank_ids)

    if len(questions) != 199:
        errors.append(f"expected 199 questions, found {len(questions)}")
    if len(answer_bank) != len(questions):
        errors.append(f"answer bank count mismatch: {len(answer_bank)} != {len(questions)}")
    if answer_bank != ios_answer_bank:
        errors.append("iOS Resources practical-answer-bank.json is not identical to data/practical-answer-bank.json")
    if ANSWER_BANK_PATH.read_bytes() != IOS_ANSWER_BANK_PATH.read_bytes():
        data_sha = hashlib.sha256(ANSWER_BANK_PATH.read_bytes()).hexdigest()
        ios_sha = hashlib.sha256(IOS_ANSWER_BANK_PATH.read_bytes()).hexdigest()
        errors.append(f"answer bank SHA mismatch: data={data_sha} ios={ios_sha}")
    if len(bank_ids) != len(bank_id_set):
        errors.append("duplicate questionId in answer bank")

    missing = sorted(question_ids - bank_id_set)
    extra = sorted(bank_id_set - question_ids)
    if missing:
        errors.append(f"missing answer bank entries: {', '.join(missing[:20])}")
    if extra:
        errors.append(f"unknown answer bank entries: {', '.join(extra[:20])}")

    missing_2025 = sorted(year_2025_ids - bank_id_set)
    if missing_2025:
        errors.append(f"missing 2025 answer bank entries: {', '.join(missing_2025)}")

    for index, entry in enumerate(answer_bank):
        prefix = entry.get("questionId") or f"index:{index}"
        status = entry.get("answerStatus")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{prefix}: invalid answerStatus {status!r}")
        if status in {"draft", "verified"}:
            has_answer_content = any(
                entry.get(field)
                for field in ("modelAnswer", "performanceSteps", "oralAnswerStructure")
            )
            if not has_answer_content:
                errors.append(
                    f"{prefix}: {status} entry needs modelAnswer, performanceSteps, or oralAnswerStructure"
                )
            if not entry.get("modelAnswer"):
                errors.append(f"{prefix}: {status} entry requires modelAnswer")
            if len(entry.get("keyPoints") or []) < 3:
                errors.append(f"{prefix}: {status} entry requires at least 3 keyPoints")
            if not entry.get("commonMistakes"):
                errors.append(f"{prefix}: {status} entry requires commonMistakes")
            if not entry.get("memoryTip"):
                errors.append(f"{prefix}: {status} entry requires memoryTip")
        if not isinstance(entry.get("sourceRefs"), list):
            errors.append(f"{prefix}: sourceRefs must be a list")
            continue
        for source_index, source in enumerate(entry["sourceRefs"]):
            for field in ("title", "url", "type", "checkedAt"):
                if not source.get(field):
                    errors.append(f"{prefix}: sourceRefs[{source_index}] missing {field}")
            if source.get("type") not in ALLOWED_SOURCE_TYPES:
                errors.append(f"{prefix}: invalid source type {source.get('type')!r}")

        if entry.get("sourceVerified") is True and status != "verified":
            errors.append(f"{prefix}: sourceVerified true requires answerStatus verified")
        if status == "verified" and entry.get("sourceVerified") is not True:
            errors.append(f"{prefix}: verified answer requires sourceVerified true")
        if status == "verified" and not entry.get("modelAnswer"):
            errors.append(f"{prefix}: verified answer requires modelAnswer")
        if status == "verified" and len(entry.get("keyPoints") or []) < 3:
            errors.append(f"{prefix}: verified answer requires at least 3 keyPoints")
        if status == "verified" and not entry.get("commonMistakes"):
            errors.append(f"{prefix}: verified answer requires commonMistakes")
        if status == "verified" and not entry.get("memoryTip"):
            errors.append(f"{prefix}: verified answer requires memoryTip")
        if status == "verified" and not entry.get("sourceRefs"):
            errors.append(f"{prefix}: verified answer requires sourceRefs")
        if status == "verified":
            review_notes = entry.get("reviewNotes") or []
            if not review_notes:
                errors.append(f"{prefix}: verified answer requires reviewNotes")
            pending_markers = ("기출 당시 기준 확인 필요", "확인 필요", "수동 검수", "pending")
            pending_notes = [
                note
                for note in review_notes
                if any(marker in note for marker in pending_markers)
            ]
            if pending_notes:
                errors.append(f"{prefix}: verified answer has unresolved reviewNotes")
        if entry.get("sourceVerified") is True and not entry.get("sourceRefs"):
            errors.append(f"{prefix}: sourceVerified true requires at least one sourceRef")
        if status == "verified" and entry.get("needsReview") is True:
            errors.append(f"{prefix}: verified answer cannot remain needsReview true")

    if errors:
        fail(errors)

    print("answer bank validation passed")
    print(f"questions={len(questions)}")
    print(f"answer_bank_entries={len(answer_bank)}")
    print(f"needs_review={sum(1 for entry in answer_bank if entry.get('needsReview'))}")


if __name__ == "__main__":
    main()
