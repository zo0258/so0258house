#!/usr/bin/env python3
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return path.read_text(encoding="utf-8")


def assert_true(condition, message):
    if not condition:
        raise AssertionError(message)


def main():
    data_path = ROOT / "data" / "practical-questions.json"
    index_path = ROOT / "index.html"
    quiz_path = ROOT / "quizzes" / "quiz-today.html"
    wrong_path = ROOT / "wrong-note.html"

    assert_true(data_path.exists(), "data/practical-questions.json missing")
    questions = json.loads(read(data_path))
    assert_true(isinstance(questions, list) and questions, "practical question data is empty")
    for item in questions:
        for key in ("id", "subject", "section", "type", "year", "question", "methodGuide", "memoryTip", "answerGuide", "sourceRefs", "sourceVerified", "needsReview"):
            assert_true(key in item, f"missing key {key} in {item.get('id')}")
        assert_true(item["type"] in ("실기", "구술", "공통"), f"unexpected type {item['type']}")
        assert_true(item["question"].strip(), f"empty question in {item['id']}")
    assert_true(any(item["type"] == "실기" for item in questions), "no practical questions")
    assert_true(any(item["type"] == "구술" for item in questions), "no oral questions")

    index = read(index_path)
    assert_true("건강운동관리사 실기 대비" in index, "index title text not converted")
    assert_true("오늘 실기·구술 4문제" in index, "today CTA text not converted")
    assert_true("미풀이 · 4문항 남음" in index, "4-question pending copy missing")
    assert_true("복습노트 보기" in index, "review-note copy missing")
    assert_true("오늘 완료 <strong id=\"todayDoneCount\">0</strong>/4" in index, "today completion count missing")
    assert_true("복습 <strong id=\"reviewCount\">0</strong>" in index, "dashboard review count missing")
    assert_true("어려움 <strong id=\"hardCount\">0</strong>" in index, "dashboard hard count missing")
    assert_true("today-question-data" in index, "dashboard daily question data missing")
    assert_true("10문항" not in index, "old 10-question copy remains in index")

    quiz = read(quiz_path)
    match = re.search(r'<script id="quiz-data" type="application/json">(.*?)</script>', quiz, re.S)
    assert_true(match, "quiz data script missing")
    payload = json.loads(match.group(1))
    assert_true(len(payload["questions"]) == 4, "today quiz does not contain exactly 4 questions")
    type_counts = {}
    for item in payload["questions"]:
        type_counts[item["type"]] = type_counts.get(item["type"], 0) + 1
    assert_true(type_counts.get("실기") == 2 and type_counts.get("구술") == 2, "today quiz is not practical 2 + oral 2")
    assert_true(len({item["subject"] for item in payload["questions"]}) >= 2, "today quiz is concentrated in one subject")
    assert_true(len({item["section"] for item in payload["questions"]}) >= 3, "today quiz sections are not sufficiently distributed")
    assert_true("data-choice" not in quiz, "choice buttons remain in quiz page")
    assert_true('id="nextBtn"' not in quiz, "next button should not allow skipping status selection")
    assert_true("1/4 문제" in quiz and "기록 0/4" in quiz, "separate progress labels missing")
    assert_true("type-badge practical" in quiz, "practical type badge missing")
    assert_true("type-badge oral" in quiz, "oral type badge missing")
    assert_true("q-meta" in quiz and "q-topic" in quiz, "topic metadata structure missing")
    for label in ("답변 순서", "실기/구술 체크포인트", "암기 포인트"):
        assert_true(label in quiz, f"guide structure missing: {label}")
    for label in ("수행 순서 중심으로 직접 말해보기", "정의 → 기준 → 적용 → 주의사항 순서로 답변하기", "자세 / 호흡 / 안전 / 기록 순서로 점검하기"):
        assert_true(label in quiz, f"friendly guide copy missing: {label}")
    assert_true("추후 입력" not in quiz, "unfinished guide copy remains visible")
    assert_true("sourceVerified" not in quiz, "internal sourceVerified state should not be visible in quiz")
    assert_true("needsReview" not in quiz, "internal needsReview state should not be visible in quiz")
    for label in ("완료", "다시 보기", "어려움"):
        assert_true(label in quiz, f"{label} action missing")

    wrong = read(wrong_path)
    assert_true("어려움·다시 볼 문제" in wrong, "wrong-note meaning not converted")
    assert_true("복습노트" in wrong, "wrong-note display name not converted")
    for label in ("전체", "다시 보기", "어려움"):
        assert_true(f'data-filter="{label}"' in wrong, f"review-note filter missing: {label}")
    assert_true("activeFilter" in wrong, "review-note filter state missing")
    assert_true("sourceVerified" not in wrong, "internal sourceVerified state should not be visible in wrong-note")
    assert_true("needsReview" not in wrong, "internal needsReview state should not be visible in wrong-note")
    assert_true("health-exercise-practical-records" in quiz, "record localStorage key missing in quiz")
    assert_true("health-exercise-practical-records" in wrong, "record localStorage key missing in wrong-note")


if __name__ == "__main__":
    main()
