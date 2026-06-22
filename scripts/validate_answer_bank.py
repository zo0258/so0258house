#!/usr/bin/env python3
import json
import hashlib
import re
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
ALLOWED_SOURCE_TYPES = {
    "official",
    "academic",
    "textbook",
    "trusted_web",
    "internal",
    "tier_s_internal",
}
ALLOWED_REVIEW_TAGS = {
    "[exam-ready-draft]",
    "[source-needed]",
    "[source-verified]",
    "[year-standard-conflict]",
    "[needs-tier-s-check]",
    "[needs-answer-source-check]",
    "[source-verifiable]",
    "[source-backed-draft]",
    "[guidebook-only]",
    "[conflicting-standard]",
    "[practical-demonstration-needed]",
    "[specialist-source-needed]",
    "[needs-specialist-check]",
    "[verified-maintained]",
    "[verified-candidate]",
    "[verified-rejected]",
}
PRIMARY_SOURCE_CLASSIFICATION_TAGS = {
    "[source-verifiable]",
    "[guidebook-only]",
    "[conflicting-standard]",
    "[practical-demonstration-needed]",
    "[specialist-source-needed]",
}
GUIDEBOOK_TITLE = "건강운동관리사 취득 기초 길잡이 2026"
GUIDEBOOK_URL = "internal://guidebook/2026"
EXPECTED_SOURCE_VERIFIABLE_COUNT = 27


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
        guidebook_refs = [
            source
            for source in entry["sourceRefs"]
            if source.get("title") == GUIDEBOOK_TITLE
            and source.get("url") == GUIDEBOOK_URL
            and source.get("type") == "tier_s_internal"
        ]
        if not guidebook_refs:
            errors.append(f"{prefix}: missing guidebook sourceRef")
        elif len(guidebook_refs) > 1:
            errors.append(f"{prefix}: duplicate guidebook sourceRef")
        elif not isinstance(guidebook_refs[0].get("page"), int):
            errors.append(f"{prefix}: guidebook sourceRef requires integer page")

        for source_index, source in enumerate(entry["sourceRefs"]):
            for field in ("title", "url", "type", "checkedAt"):
                if not source.get(field):
                    errors.append(f"{prefix}: sourceRefs[{source_index}] missing {field}")
            if source.get("type") not in ALLOWED_SOURCE_TYPES:
                errors.append(f"{prefix}: invalid source type {source.get('type')!r}")
            if "page" in source and not isinstance(source.get("page"), int):
                errors.append(f"{prefix}: sourceRefs[{source_index}] page must be an integer when present")

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
            answer_sources = [
                source
                for source in entry.get("sourceRefs", [])
                if not (
                    source.get("title") == GUIDEBOOK_TITLE
                    and source.get("url") == GUIDEBOOK_URL
                )
            ]
            if not answer_sources:
                errors.append(
                    f"{prefix}: verified answer requires at least one answer source beyond guidebook"
                )
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
        if entry.get("sourceVerified") is True:
            strong_source_types = {"official", "textbook", "internal", "tier_s_internal"}
            if not any(source.get("type") in strong_source_types for source in entry.get("sourceRefs", [])):
                errors.append(f"{prefix}: sourceVerified true requires official, textbook, or internal sourceRef")
            review_notes = entry.get("reviewNotes") or []
            if not any("검증 근거" in note for note in review_notes):
                errors.append(f"{prefix}: sourceVerified true requires reviewNotes with verification basis")
        if status == "verified" and entry.get("needsReview") is True:
            errors.append(f"{prefix}: verified answer cannot remain needsReview true")

        review_notes = entry.get("reviewNotes") or []
        review_tags = {
            token
            for note in review_notes
            for token in ALLOWED_REVIEW_TAGS
            if token in note
        }
        for note in review_notes:
            for token in re.findall(r"\[[A-Za-z0-9_-]+\]", note):
                if token not in ALLOWED_REVIEW_TAGS:
                    errors.append(f"{prefix}: unknown reviewNotes quality tag {token}")
        classification_tags = review_tags & PRIMARY_SOURCE_CLASSIFICATION_TAGS
        if len(classification_tags) != 1:
            errors.append(
                f"{prefix}: requires exactly one Pass 6 source classification tag, found "
                f"{sorted(classification_tags)}"
            )
        if "[exam-ready-draft]" in review_tags and status != "draft":
            errors.append(f"{prefix}: [exam-ready-draft] tag is only valid for draft entries")
        if "[exam-ready-draft]" in review_tags and entry.get("sourceVerified") is True:
            errors.append(f"{prefix}: [exam-ready-draft] cannot be sourceVerified true")
        if "[source-verified]" in review_tags and status != "verified":
            errors.append(f"{prefix}: [source-verified] tag requires verified status")
        if "[source-backed-draft]" in review_tags:
            if status != "draft":
                errors.append(f"{prefix}: [source-backed-draft] tag is only valid for draft entries")
            if entry.get("sourceVerified") is True:
                errors.append(f"{prefix}: [source-backed-draft] cannot be sourceVerified true")
            answer_sources = [
                source
                for source in entry.get("sourceRefs", [])
                if not (
                    source.get("title") == GUIDEBOOK_TITLE
                    and source.get("url") == GUIDEBOOK_URL
                )
            ]
            if not answer_sources:
                errors.append(f"{prefix}: [source-backed-draft] requires sourceRef beyond guidebook")
        if "[verified-maintained]" in review_tags and status != "verified":
            errors.append(f"{prefix}: [verified-maintained] tag requires verified status")
        if "[verified-candidate]" in review_tags and status == "verified":
            errors.append(f"{prefix}: [verified-candidate] is for non-verified entries only")
        if "[verified-rejected]" in review_tags and status == "verified":
            errors.append(f"{prefix}: [verified-rejected] is for non-verified entries only")
        if "[year-standard-conflict]" in review_tags and status == "verified":
            errors.append(f"{prefix}: verified entry cannot retain [year-standard-conflict]")

    if errors:
        fail(errors)

    exam_ready_count = sum(
        1
        for entry in answer_bank
        if any("[exam-ready-draft]" in note for note in entry.get("reviewNotes") or [])
    )
    guidebook_ref_count = sum(
        1
        for entry in answer_bank
        if any(
            source.get("title") == GUIDEBOOK_TITLE
            and source.get("url") == GUIDEBOOK_URL
            and source.get("type") == "tier_s_internal"
            for source in entry.get("sourceRefs", [])
        )
    )
    source_verifiable_count = sum(
        1
        for entry in answer_bank
        if any("[source-verifiable]" in note for note in entry.get("reviewNotes") or [])
    )
    source_backed_draft_count = sum(
        1
        for entry in answer_bank
        if any("[source-backed-draft]" in note for note in entry.get("reviewNotes") or [])
    )
    if source_verifiable_count != EXPECTED_SOURCE_VERIFIABLE_COUNT:
        fail(
            [
                "source-verifiable count mismatch: "
                f"{source_verifiable_count} != {EXPECTED_SOURCE_VERIFIABLE_COUNT}"
            ]
        )
    print("answer bank validation passed")
    print(f"questions={len(questions)}")
    print(f"answer_bank_entries={len(answer_bank)}")
    print(f"needs_review={sum(1 for entry in answer_bank if entry.get('needsReview'))}")
    print(f"exam_ready_draft={exam_ready_count}")
    print(f"guidebook_source_refs={guidebook_ref_count}")
    print(f"source_verifiable={source_verifiable_count}")
    print(f"source_backed_draft={source_backed_draft_count}")


if __name__ == "__main__":
    main()
