#!/usr/bin/env python3
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_PATH = ROOT / "data" / "practical-questions.json"
ANSWER_BANK_PATH = ROOT / "data" / "practical-answer-bank.json"
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
    errors = []

    question_ids = {question["id"] for question in questions}
    bank_ids = [entry.get("questionId") for entry in answer_bank]
    bank_id_set = set(bank_ids)

    if len(questions) != 199:
        errors.append(f"expected 199 questions, found {len(questions)}")
    if len(answer_bank) != len(questions):
        errors.append(f"answer bank count mismatch: {len(answer_bank)} != {len(questions)}")
    if len(bank_ids) != len(bank_id_set):
        errors.append("duplicate questionId in answer bank")

    missing = sorted(question_ids - bank_id_set)
    extra = sorted(bank_id_set - question_ids)
    if missing:
        errors.append(f"missing answer bank entries: {', '.join(missing[:20])}")
    if extra:
        errors.append(f"unknown answer bank entries: {', '.join(extra[:20])}")

    for index, entry in enumerate(answer_bank):
        prefix = entry.get("questionId") or f"index:{index}"
        status = entry.get("answerStatus")
        if status not in ALLOWED_STATUSES:
            errors.append(f"{prefix}: invalid answerStatus {status!r}")
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
